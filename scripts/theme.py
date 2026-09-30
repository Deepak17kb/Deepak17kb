"""Palette and SVG helpers shared by the profile README generators.

Every SVG is self-contained: GitHub serves README images through a sandboxed
proxy, so there are no web fonts, scripts or remote images. Motion is CSS
keyframes where possible and SMIL where an attribute (width, x, a path) has to
move. Each element's resting state is its final, readable state, so a viewer
that does not animate still shows a complete picture.
"""

from __future__ import annotations

from xml.sax.saxutils import escape

# ── palette ────────────────────────────────────────────────────────────────
PANEL = "#0A0A13"
INSET = "#0E0E1A"
LINE = "#1E1E30"
TEXT = "#ECECF4"
SUB = "#A9A9C2"
MUTED = "#6A6A80"

CYAN = "#00FFF2"
BLUE = "#7AA2FF"
VIOLET = "#B199FF"
MINT = "#5CF2B0"
PINK = "#FF7AC6"
AMBER = "#FFC069"
RED = "#FF4D6D"

SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,Inter,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code','Fira Code',Consolas,'SF Mono',Menlo,monospace"
MONO_W = 0.6  # advance of one monospace glyph, in em

BASE_CSS = (
    "text{font-kerning:normal}"
    ".comet{fill:none;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:90 910;"
    "animation:comet 10s linear infinite}"
    ".halo{stroke-width:7;opacity:.22}"
    "@keyframes comet{from{stroke-dashoffset:0}to{stroke-dashoffset:-1000}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def num(value: float) -> str:
    """Compact number for SVG attributes."""
    return f"{value:.2f}".rstrip("0").rstrip(".")


def mono_width(text: str, size: float) -> float:
    return len(text) * MONO_W * size


def mono(x, y, text, size, fill, *, anchor="start", weight=None, cls=None, attrs=""):
    """Monospace text pinned to an exact width, so layouts do not depend on the font."""
    extra = f' font-weight="{weight}"' if weight else ""
    extra += f' class="{cls}"' if cls else ""
    extra += f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{num(x)}" y="{num(y)}" font-family="{MONO}" font-size="{num(size)}" fill="{fill}"'
        f' textLength="{num(mono_width(text, size))}" lengthAdjust="spacing" xml:space="preserve"'
        f"{extra}{attrs}>{esc(text)}</text>"
    )


def sans(x, y, text, size, fill, *, weight=400, anchor="start", cls=None, attrs=""):
    extra = f' class="{cls}"' if cls else ""
    extra += f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{num(x)}" y="{num(y)}" font-family="{SANS}" font-size="{num(size)}"'
        f' font-weight="{weight}" fill="{fill}"{extra}{attrs}>{esc(text)}</text>'
    )


def rounded_path(x, y, w, h, r):
    """A rounded rectangle as a path, so pathLength works in every browser."""
    return (
        f"M{num(x + r)},{num(y)}H{num(x + w - r)}A{num(r)},{num(r)} 0 0 1 {num(x + w)},{num(y + r)}"
        f"V{num(y + h - r)}A{num(r)},{num(r)} 0 0 1 {num(x + w - r)},{num(y + h)}"
        f"H{num(x + r)}A{num(r)},{num(r)} 0 0 1 {num(x)},{num(y + h - r)}"
        f"V{num(y + r)}A{num(r)},{num(r)} 0 0 1 {num(x + r)},{num(y)}Z"
    )


def frame(w, h, r, uid, accents=(CYAN, VIOLET), period=10.0, fill=PANEL):
    """Panel background, hairline border and light 'comets' orbiting the edge.

    Returns (defs, background, border); draw the border last so it sits on top.
    """
    d = rounded_path(0.75, 0.75, w - 1.5, h - 1.5, r)
    comets = []
    for i, color in enumerate(accents):
        delay = -period * i / len(accents)
        style = f"animation-duration:{num(period)}s;animation-delay:{num(delay)}s"
        comets.append(
            f'<path d="{d}" pathLength="1000" class="comet halo" stroke="{color}" style="{style}"/>'
            f'<path d="{d}" pathLength="1000" class="comet" stroke="{color}" style="{style}"/>'
        )
    defs = f'<clipPath id="{uid}-clip"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>'
    background = f'<rect width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
    border = f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5"/>' + "".join(comets)
    return defs, background, border


def document(width, height, body, *, label, css="", defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        f' viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">'
        f"<title>{esc(label)}</title><style>{BASE_CSS}{css}</style>"
        f"<defs>{defs}</defs>{body}</svg>\n"
    )


def discrete(attribute, frames, total, *, extra=""):
    """SMIL step animation from (time, value) frames, holding the last value.

    The first frame must be at t=0; every animation starts at load and runs
    `total` seconds, so elements stay hidden until their own moment arrives.
    """
    times = ";".join(f"{t / total:.5f}" if t else "0" for t, _ in frames)
    values = ";".join(v if isinstance(v, str) else num(v) for _, v in frames)
    return (
        f'<animate attributeName="{attribute}" values="{values}" keyTimes="{times}"'
        f' dur="{num(total)}s" calcMode="discrete" fill="freeze"{extra}/>'
    )
