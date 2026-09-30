"""Palette and SVG helpers shared by the profile README generators.

Every SVG is self-contained: GitHub serves README images through a sandboxed
proxy, so there are no web fonts, scripts or remote images. Motion is CSS
keyframes where possible and SMIL where an attribute (width, x, a path) has to
move. Each element's resting state is its final, readable state, so a viewer
that does not animate still shows a complete picture.
"""

from __future__ import annotations

from xml.sax.saxutils import escape

# ── palette: charcoal and off-white, with muted, earthy accents ────────────
PANEL = "#111113"
INSET = "#18181B"
LINE = "#27272A"
TEXT = "#EDEDEF"
SUB = "#A1A1AA"
MUTED = "#71717A"

SAND = "#D4B483"  # the primary accent
SLATE = "#8EA4C2"
SAGE = "#9CB89A"
CLAY = "#CF8E7C"
LILAC = "#A9A1C8"
ROSE = "#C99BA8"
STONE = "#B8B2A7"
GREEN = "#8DBF8B"
RED = "#D97A6C"

SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,Inter,'Helvetica Neue',Arial,sans-serif"
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype',Palatino,'Times New Roman',serif"
MONO = "'JetBrains Mono','Cascadia Code','Fira Code',Consolas,'SF Mono',Menlo,monospace"
MONO_W = 0.6  # advance of one monospace glyph, in em

BASE_CSS = (
    "text{font-kerning:normal}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def num(value: float) -> str:
    """Compact number for SVG attributes."""
    return f"{value:.2f}".rstrip("0").rstrip(".")


def mono_width(text: str, size: float) -> float:
    return len(text) * MONO_W * size


def mono(x, y, text, size, fill, *, anchor="start", weight=None, cls=None, attrs="", track=0.0):
    """Monospace text pinned to an exact width, so layouts do not depend on the font.

    `track` adds letter-spacing, in px, between glyphs.
    """
    extra = f' font-weight="{weight}"' if weight else ""
    extra += f' class="{cls}"' if cls else ""
    extra += f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{num(x)}" y="{num(y)}" font-family="{MONO}" font-size="{num(size)}" fill="{fill}"'
        f' textLength="{num(mono_width(text, size) + track * (len(text) - 1))}" lengthAdjust="spacing"'
        ' xml:space="preserve"'
        f"{extra}{attrs}>{esc(text)}</text>"
    )


def sans(x, y, text, size, fill, *, weight=400, anchor="start", cls=None, attrs=""):
    extra = f' class="{cls}"' if cls else ""
    extra += f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{num(x)}" y="{num(y)}" font-family="{SANS}" font-size="{num(size)}"'
        f' font-weight="{weight}" fill="{fill}"{extra}{attrs}>{esc(text)}</text>'
    )


def frame(w, h, r, uid, fill=PANEL):
    """Panel background, hairline border and a faint highlight along the top edge.

    Returns (defs, background, border); draw the border last so it sits on top.
    """
    defs = (
        f'<clipPath id="{uid}-clip"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>'
        f'<linearGradient id="{uid}-edge"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".14"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        "</linearGradient>"
    )
    background = f'<rect width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
    border = (
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{r - 0.5}" fill="none" stroke="{LINE}"/>'
        f'<rect x="{r}" y=".5" width="{w - 2 * r}" height="1" fill="url(#{uid}-edge)"/>'
    )
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
