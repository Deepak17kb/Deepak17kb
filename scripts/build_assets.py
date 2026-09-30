"""Render the animated SVGs under assets/ that the profile README shows.

    python scripts/build_assets.py

Edit the text below and re-run; the output is deterministic, so unchanged
content produces identical files. Live GitHub numbers are drawn separately by
build_stats.py, which a scheduled workflow runs.
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from textwrap import wrap

from theme import (
    CLAY, GREEN, INSET, LILAC, LINE, MONO_W, MUTED, RED, ROSE, SAGE, SAND, SANS, SERIF, SLATE, STONE, SUB, TEXT,
    discrete, document, esc, frame, mono, mono_width, num, sans,
)

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# ── content ────────────────────────────────────────────────────────────────
ROLES = [
    "Data & AI, in the making",
    "Turning messy data into insight",
    "Learning fast, building faster",
    "From Punjab, for the world",
]

CHIPS = [("pin", "Jalandhar, Punjab"), ("spark", "Data science track"), ("dot", "Status: active")]

# The statement is set by hand, one line at a time, as (text, highlighted) runs.
STATEMENT = [
    [("Data science with ", False), ("AI layered in", True), (" is where I", False)],
    [("spend most of my time. I like ", False), ("messy problems", True), (",", False)],
    [("interesting patterns, and the feeling of", False)],
    [("finally figuring something out", True), (" after", False)],
    [("staring at it for way too long.", False)],
]
CLOSING = "There’s always something new to figure out."
# (label, value or pills, optional aside set in italics beneath)
PROFILE = [
    ("Studying", "CSE · Data Science track", None),
    ("Works with", ["Python", "SQL", "AI / ML", "Power BI"], "…and whatever catches my curiosity"),
    ("Interests", "AI · data · psychology · how things work · new ideas", None),
    ("Drawn to", "automation · systems · things that shouldn't work but do", None),
    ("Off the clock", "Gaming · movies · music · exploring · traveling", "…and pretending I'll sleep early"),
]

SECTIONS = [
    ("about", "01", "About", "who I am"),
    ("work", "02", "Featured work", "selected builds · click a card"),
    ("toolkit", "03", "Toolkit", "languages · frameworks · data"),
    ("activity", "04", "GitHub activity", "updated automatically"),
    ("connect", "05", "Connect", "say hello"),
]

PROJECTS = [
    dict(slug="broadbridge", title="BroadBridge", label="AI · FINTECH", accent=SLATE, icon="bridge",
         viz="fan", live=True, tags=["TypeScript", "React", "Node.js", "239 tests"],
         blurb="Agentic wealth navigator. A shared TypeScript engine runs Monte "
               "Carlo projections in browser and server."),
    dict(slug="ner-saferoute", title="NER SafeRoute", label="GEOSPATIAL · ML · SIH", accent=SAND, icon="pin",
         viz="route", live=True, tags=["FastAPI", "PostGIS", "React", "Leaflet"],
         blurb="Hazard-safe routing for Northeast India: ML road-risk scores, live "
               "hazard feeds and a vehicle-aware A* router."),
    dict(slug="agriflow", title="AgriFlow AI", label="DATA · FORECASTING", accent=SAGE, icon="leaf",
         viz="yield", live=True, tags=["Python", "Streamlit", "scikit-learn", "Plotly"],
         blurb="Crop and food-security analytics for 68 countries and 22 crops, with "
               "a RandomForest outlook and yield ranges."),
    dict(slug="krishimitra", title="KrishiMitra", label="GEN AI · AGRITECH", accent=CLAY, icon="chat",
         viz="chat", live=False, tags=["Node.js", "Express", "Gemini", "Vanilla JS"],
         blurb="AI farming companion in Hindi and English: crop advice, live weather, "
               "mandi prices and government schemes."),
    dict(slug="deadlock-lab", title="Deadlock Runtime Lab", label="OPERATING SYSTEMS", accent=ROSE, icon="lock",
         viz="cycle", live=True, tags=["React 19", "Vite", "Express 5", "SQLite"],
         blurb="A resource-allocation graph you can run: a deterministic scheduler "
               "exposes contention and DFS finds the deadlock."),
    dict(slug="upi-risk-desk", title="UPI Risk Desk", label="TEAM COLLABORATION · RISK", accent=LILAC, icon="shield",
         viz="ring", team=["A", "I", "P", "D"], tags=["Python", "pandas", "NetworkX", "ECharts"],
         blurb="Fraud-ring detection and merchant risk analytics for UPI "
               "payments, with a team of AI risk agents."),
]

LINKS = [
    ("linkedin", "user", "LinkedIn", "in/deepak-kumarbehera", SLATE),
    ("github", "branch", "Follow on GitHub", "@Deepak17kb", SAND),
]

CLOSERS = [
    "I am the one who codes.",
    "Still building, still learning.",
    "Every project is a step forward.",
    "Punjab to the world, one commit at a time.",
]

RISE = (
    ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
    "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
    ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.6s ease-out infinite both}"
    "@keyframes ping{0%{transform:scale(1);opacity:.6}70%,100%{transform:scale(2.8);opacity:0}}"
    ".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    ".rule{stroke-dasharray:1 1;animation:rule 1.4s cubic-bezier(.5,0,.2,1) both}"
    "@keyframes rule{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
)


def path_from(points) -> str:
    return "M" + "L".join(f"{num(x)},{num(y)}" for x, y in points)


def icon_path(name: str) -> str:
    return {
        "bridge": "M-11,5H11M-11,5Q0,-13 11,5M-5.5,5V-1.75M0,5V-4M5.5,5V-1.75",
        "pin": "M0,9C-5,3 -7,0 -7,-3A7,7 0 0 1 7,-3C7,0 5,3 0,9ZM2.4,-3A2.4,2.4 0 1 1 -2.4,-3A2.4,2.4 0 1 1 2.4,-3",
        "leaf": "M0,10V-1M0,3C-8,3 -9,-5 -9,-7C-3,-7 0,-4 0,3M0,-1C0,-7 4,-10 9,-10C9,-4 5,-1 0,-1",
        "chat": "M-8,-8H8A3,3 0 0 1 11,-5V2A3,3 0 0 1 8,5H-1L-6,9V5H-8A3,3 0 0 1 -11,2V-5A3,3 0 0 1 -8,-8Z"
                "M-5,-1.5H-4.5M0,-1.5H0.5M5,-1.5H5.5",
        "lock": "M-8,-1H8V10H-8ZM-4.5,-1V-4.5A4.5,4.5 0 0 1 4.5,-4.5V-1M0,3.5V6",
        "shield": "M0,-10L8,-7V0C8,5 4.5,8.5 0,10C-4.5,8.5 -8,5 -8,0V-7ZM-3.5,0L-1,2.5L3.5,-2",
        "user": "M0,-2A4.5,4.5 0 1 0 0,-11A4.5,4.5 0 1 0 0,-2ZM-9,10C-9,4 -5,1 0,1C5,1 9,4 9,10",
        "branch": "M-5,-4.4V5.4M6,-0.4C6,4 -5,2 -5,5.4M-2.4,-7A2.6,2.6 0 1 1 -7.6,-7A2.6,2.6 0 1 1 -2.4,-7"
                  "M-2.4,8A2.6,2.6 0 1 1 -7.6,8A2.6,2.6 0 1 1 -2.4,8M8.6,-3A2.6,2.6 0 1 1 3.4,-3A2.6,2.6 0 1 1 8.6,-3",
    }[name]


# ── hero ───────────────────────────────────────────────────────────────────
def contours(cx0, cy0, levels, rnd):
    """Closed, nested contour lines around one summit, like a topographic map."""
    phases = [rnd.uniform(0, 2 * math.pi) for _ in range(3)]
    rings = []
    for k in range(levels):
        base = 16 + k * 19
        cx, cy = cx0 - k * 4, cy0 + k * 2.2
        pts = []
        for i in range(120):
            th = 2 * math.pi * i / 120
            f = (1 + (0.10 + k * 0.006) * math.sin(2 * th + phases[0] + k * 0.05)
                 + (0.07 + k * 0.004) * math.sin(3 * th + phases[1] - k * 0.04)
                 + 0.035 * math.sin(5 * th + phases[2] + k * 0.08))
            pts.append((cx + base * f * math.cos(th), cy + base * f * 0.82 * math.sin(th)))
        rings.append(path_from(pts) + "Z")
    return rings


def hero() -> str:
    W, H = 1200, 400
    rnd = random.Random(11)
    defs, back, border = frame(W, H, 24, "hero")
    css = RISE + (
        ".reveal{animation:reveal 1.4s cubic-bezier(.2,.7,.2,1) .45s both}"
        "@keyframes reveal{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
        ".contour{stroke-dasharray:1 1;animation:rule 2.6s cubic-bezier(.4,0,.2,1) both}"
        ".ripple{animation:ripple 10s ease-in-out infinite both}"
        "@keyframes ripple{0%,100%{stroke-opacity:0}7%{stroke-opacity:.6}22%{stroke-opacity:0}}"
    )
    defs += (
        '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        '<circle cx="1" cy="1" r="1" fill="#fff" fill-opacity=".06"/></pattern>'
        '<radialGradient id="dots-fade" cx=".3" cy=".45" r=".7"><stop offset="0" stop-color="#fff"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="dots-mask"><rect width="{W}" height="{H}" fill="url(#dots-fade)"/></mask>'
        '<linearGradient id="map-fade"><stop offset=".5" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".7" stop-color="#fff"/></linearGradient>'
        f'<mask id="map-mask"><rect width="{W}" height="{H}" fill="url(#map-fade)"/></mask>'
        f'<radialGradient id="warm" cx=".8" cy=".48" r=".45"><stop offset="0" stop-color="{SAND}" stop-opacity=".08"/>'
        f'<stop offset="1" stop-color="{SAND}" stop-opacity="0"/></radialGradient>'
    )

    out = [back, '<g clip-path="url(#hero-clip)">',
           f'<rect width="{W}" height="{H}" fill="url(#warm)"/>',
           f'<rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#dots-mask)"/>']

    # Topographic contours; a highlight ripples outward from the summit every few seconds.
    cx0, cy0 = 968, 196
    topo = []
    for k, d in enumerate(contours(cx0, cy0, 13, rnd)):
        topo.append(f'<path d="{d}" pathLength="1" class="contour" fill="none" stroke="{STONE}"'
                    f' stroke-opacity="{num(0.42 - k * 0.022)}" style="animation-delay:{num(0.2 + k * 0.09)}s"/>')
        topo.append(f'<path d="{d}" fill="none" stroke="{SAND}" stroke-width="1.4" stroke-opacity="0" class="ripple"'
                    f' style="animation-delay:{num(3 + k * 0.32)}s"/>')
    out.append(f'<g mask="url(#map-mask)">{"".join(topo)}</g>')
    place = "Jalandhar, IN"
    out.append(
        f'<g class="rise" style="animation-delay:1.6s">'
        f'<circle cx="{cx0}" cy="{cy0}" r="4" fill="{SAND}" opacity="0" class="ping"/>'
        f'<circle cx="{cx0}" cy="{cy0}" r="4" fill="{SAND}"/>'
        f'<rect x="{cx0 + 14}" y="{cy0 - 32}" width="{num(mono_width(place, 11) + 18)}" height="22" rx="11"'
        f' fill="{INSET}" stroke="{LINE}"/>{mono(cx0 + 23, cy0 - 17, place, 11, SUB)}</g>'
    )

    # Greeting, typed.
    greet = "Hello, I'm"
    cw = 15 * MONO_W
    frames = [(0, 0)] + [(0.3 + k * 0.06, num((k + 1) * cw + 2)) for k in range(len(greet))]
    out.append(
        f'<clipPath id="greet-clip"><rect x="82" y="98" width="{num(len(greet) * cw + 2)}" height="26">'
        f'{discrete("width", frames, 0.3 + len(greet) * 0.06 + 0.05)}</rect></clipPath>'
        f'<g clip-path="url(#greet-clip)">{mono(84, 118, greet, 15, SAND)}</g>'
    )

    # Name, set in a serif, with a short rule drawn beneath it.
    out.append(
        f'<g class="reveal"><text x="80" y="206" font-family="{SERIF}" font-size="104" fill="{TEXT}"'
        ' letter-spacing="-1">Deepak</text></g>'
        f'<path d="M84,236H156" pathLength="1" class="rule" stroke="{SAND}" stroke-width="2"'
        ' style="animation-delay:1.3s"/>'
    )

    # Rotating roles, typed and deleted.
    size, per = 19, 4.2
    cw = size * MONO_W
    px, base = 84, 276
    total = per * len(ROLES)
    widths = [(0, 0)]
    for i, phrase in enumerate(ROLES):
        start, n = i * per, len(phrase)
        widths += [(start + 0.25 + k * 0.055, (k + 1) * cw) for k in range(n)]
        erase = start + per - 0.75
        widths += [(erase + k * 0.014, (n - 1 - k) * cw) for k in range(n)]
    loop = ' repeatCount="indefinite"'
    first = mono_width(ROLES[0], size)
    phrases = []
    for i, phrase in enumerate(ROLES):
        start = i * per
        shown = [(0, 1 if i == 0 else 0)] + ([(start, 1)] if i else []) + ([(start + per, 0)] if i < len(ROLES) - 1 else [])
        phrases.append(
            f'<g opacity="{1 if i == 0 else 0}">{discrete("opacity", shown, total, extra=loop)}'
            f"{mono(px, base, phrase, size, SUB)}</g>"
        )
    out.append(
        f'<g class="rise" style="animation-delay:1.5s">'
        f'<clipPath id="role-clip"><rect x="{px - 1}" y="{base - 22}" width="{num(first + 2)}" height="32">'
        f'{discrete("width", [(t, num(w + 2)) for t, w in widths], total, extra=loop)}</rect></clipPath>'
        f'<g clip-path="url(#role-clip)">{"".join(phrases)}</g>'
        f'<rect x="{num(px + first + 3)}" y="{base - 17}" width="2" height="22" fill="{SAND}" class="blink">'
        f'{discrete("x", [(t, num(px + w + 3)) for t, w in widths], total, extra=loop)}</rect></g>'
    )

    # Chips.
    x = 84
    for i, (icon, text) in enumerate(CHIPS):
        w = 46 + mono_width(text, 12.5)
        cx, cy = x + 18, 315
        if icon == "dot":
            glyph = (f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{GREEN}" opacity="0" class="ping"/>'
                     f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{GREEN}"/>')
        elif icon == "pin":
            glyph = (f'<path transform="translate({cx},{cy}) scale(.68)" d="{icon_path("pin")}" fill="none"'
                     f' stroke="{STONE}" stroke-width="2.2"/>')
        else:
            glyph = (f'<path transform="translate({cx},{cy})" d="M0,-5.5L1.4,-1.4L5.5,0L1.4,1.4L0,5.5L-1.4,1.4L-5.5,0'
                     f'L-1.4,-1.4Z" fill="{STONE}"/>')
        out.append(
            f'<g class="rise" style="animation-delay:{num(2 + i * 0.12)}s">'
            f'<rect x="{num(x)}" y="300" width="{num(w)}" height="30" rx="15" fill="{INSET}" stroke="{LINE}"/>'
            f'{glyph}{mono(x + 32, 319.5, text, 12.5, SUB)}</g>'
        )
        x += w + 10

    out.append(mono(44, 46, "~/deepak17kb", 11, MUTED) + mono(1156, 46, "31.33°N · 75.58°E", 11, MUTED, anchor="end"))
    out.append("</g>" + border)
    return document(W, H, "".join(out), label="Deepak: Data & AI, turning messy data into insight. Jalandhar, Punjab.", css=css, defs=defs)


# ── about ──────────────────────────────────────────────────────────────────
def about_card() -> str:
    W, H = 1200, 460
    defs, back, border = frame(W, H, 22, "about")
    css = RISE + (
        ".breathe{animation:breathe 9s ease-in-out infinite}@keyframes breathe{0%,100%{opacity:.55}50%{opacity:1}}"
        ".pill{transform-box:fill-box;transform-origin:center;animation:pill .7s cubic-bezier(.3,1.4,.5,1) both}"
        "@keyframes pill{from{opacity:0;transform:scale(.85)}to{opacity:1;transform:none}}"
    )
    defs += (f'<radialGradient id="about-glow" cx=".12" cy=".9" r=".6"><stop offset="0" stop-color="{SAND}"'
             f' stop-opacity=".09"/><stop offset="1" stop-color="{SAND}" stop-opacity="0"/></radialGradient>')
    out = [back, '<g clip-path="url(#about-clip)">',
           f'<rect width="{W}" height="{H}" fill="url(#about-glow)" class="breathe"/>',
           f'<text x="52" y="136" font-family="{SERIF}" font-size="130" fill="{SAND}" fill-opacity=".16"'
           ' class="rise">“</text>']

    # Left: the statement, in the serif, with a few phrases picked out.
    for i, runs in enumerate(STATEMENT):
        spans = "".join(f'<tspan fill="{SAND}" font-style="italic">{esc(t)}</tspan>' if lit else esc(t)
                        for t, lit in runs)
        out.append(f'<g class="rise" style="animation-delay:{num(0.2 + i * 0.14)}s">'
                   f'<text x="72" y="{128 + i * 40}" font-family="{SERIF}" font-size="27" fill="{TEXT}"'
                   f' xml:space="preserve">{spans}</text></g>')
    out.append(f'<g class="rise" style="animation-delay:1.05s"><text x="72" y="352" font-family="{SERIF}" font-size="20"'
               f' font-style="italic" fill="{SUB}">{esc(CLOSING)}</text></g>')
    out.append(f'<g class="rise" style="animation-delay:1.35s"><text x="72" y="410" font-family="{SERIF}" font-size="22"'
               f' font-style="italic" fill="{SAND}">— Deepak</text></g>')

    # Right: a short profile sheet, separated by hairlines.
    out.append(f'<path d="M712,70V{H - 70}" pathLength="1" class="rule" stroke="{LINE}" style="animation-delay:.3s"/>')
    rx, y = 748, 72
    for i, (label, value, aside) in enumerate(PROFILE):
        delay = 0.4 + i * 0.12
        row = [mono(rx, y, label.upper(), 10.5, MUTED, track=1.6)]
        if isinstance(value, list):
            x = rx
            for j, item in enumerate(value):
                w = mono_width(item, 11) + 20
                row.append(f'<g class="pill" style="animation-delay:{num(delay + 0.3 + j * 0.08)}s">'
                           f'<rect x="{num(x)}" y="{y + 10}" width="{num(w)}" height="24" rx="12" fill="{INSET}"'
                           f' stroke="{LINE}"/>{mono(x + 10, y + 26, item, 11, TEXT)}</g>')
                x += w + 8
            bottom = y + 34
        else:
            row.append(sans(rx, y + 26, value, 15, TEXT, weight=500))
            bottom = y + 30
        if aside:
            row.append(f'<text x="{rx}" y="{bottom + 20}" font-family="{SERIF}" font-size="15" font-style="italic"'
                       f' fill="{SUB}">{esc(aside)}</text>')
            bottom += 24
        out.append(f'<g class="rise" style="animation-delay:{num(delay)}s">{"".join(row)}</g>')
        if i < len(PROFILE) - 1:
            out.append(f'<path d="M{rx},{bottom + 14}H{W - 64}" pathLength="1" class="rule" stroke="{LINE}"'
                       f' style="animation-delay:{num(delay + 0.1)}s"/>')
            y = bottom + 38

    out.append("</g>" + border)
    statement = " ".join(t for runs in STATEMENT for t, _ in runs).replace("  ", " ")
    facts = "; ".join(f"{k}: {', '.join(v) if isinstance(v, list) else v}{' ' + a if a else ''}" for k, v, a in PROFILE)
    label = f"About: {statement} {CLOSING} {facts}."
    return document(W, H, "".join(out), label=label, css=css, defs=defs)


# ── section bars ───────────────────────────────────────────────────────────
def section(index: str, title: str, caption: str) -> str:
    W, H = 1200, 72
    defs, back, border = frame(W, H, 16, "sec")
    upper = title.upper()
    size, track = 21, 5
    t_w = sum(0.29 if c == " " else 0.64 for c in upper) * size + track * (len(upper) - 1)
    cap = "// " + caption
    lx0, lx1 = 86 + t_w + 28, W - 40 - mono_width(cap, 13) - 28
    defs += (
        f'<linearGradient id="rule-grad" gradientUnits="userSpaceOnUse" x1="{num(lx0)}" x2="{num(lx1)}" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{SAND}" stop-opacity=".9"/><stop offset="1" stop-color="{SAND}" stop-opacity="0"/>'
        "</linearGradient>"
    )
    line = f"M{num(lx0)},36.5H{num(lx1)}"
    out = (
        back + '<g clip-path="url(#sec-clip)">'
        + '<g class="rise">' + mono(40, 43, index, 14, SAND, weight=700) + mono(63, 43, "/", 14, MUTED)
        + f'<text x="86" y="44" font-family="{SANS}" font-size="{size}" font-weight="600" fill="{TEXT}"'
          f' textLength="{num(t_w)}" lengthAdjust="spacing">{esc(upper)}</text></g>'
        + f'<path d="{line}" stroke="{LINE}"/>'
        + f'<path d="{line}" pathLength="1" class="rule" stroke="url(#rule-grad)" stroke-width="1.5"'
          ' style="animation-delay:.3s"/>'
        + f'<circle cx="{num(lx0)}" cy="36.5" r="3" fill="{SAND}"/>'
        + f'<circle cx="{num(lx1)}" cy="36.5" r="2.5" fill="{MUTED}"/>'
        + f'<g class="rise" style="animation-delay:.2s">{mono(W - 40, 42, cap, 13, MUTED, anchor="end")}</g>'
        + "</g>" + border
    )
    return document(W, H, out, label=f"{index} · {title}", css=RISE, defs=defs)


# ── project cards ──────────────────────────────────────────────────────────
CARD_CSS = (
    ".draw{stroke-dasharray:1 1;animation:draw 8s cubic-bezier(.5,0,.2,1) infinite both}"
    "@keyframes draw{0%{stroke-dashoffset:1}40%{stroke-dashoffset:0}88%{stroke-dashoffset:0;opacity:1}"
    "100%{stroke-dashoffset:0;opacity:0}}"
    ".fade{animation:fade 8s ease infinite both}@keyframes fade{0%,30%{opacity:0}45%,88%{opacity:1}100%{opacity:0}}"
    ".pop{transform-box:fill-box;transform-origin:center;animation:pop 8s ease infinite both}"
    "@keyframes pop{0%,38%{transform:scale(0)}44%{transform:scale(1.3)}48%,88%{transform:scale(1);opacity:1}100%{opacity:0}}"
    ".grow{transform-box:fill-box;transform-origin:50% 100%;animation:grow 8s cubic-bezier(.3,.7,.2,1) infinite both}"
    "@keyframes grow{0%{transform:scaleY(0)}25%,88%{transform:scaleY(1);opacity:1}100%{opacity:0}}"
    ".hold{animation:hold 8s infinite both}@keyframes hold{0%,88%{opacity:1}100%{opacity:0}}"
)


def viz_fan(a, rnd):
    steps = 38
    xs = [10 + i * 10 for i in range(steps + 1)]
    walks = []
    for _ in range(18):
        y, ys = 54.0, [54.0]
        for _ in range(steps):
            y = min(62.0, max(8.0, y + rnd.gauss(-0.62, 2.3)))
            ys.append(y)
        walks.append(ys)
    cols = [sorted(c) for c in zip(*walks)]
    lo, mid, hi = [c[3] for c in cols], [c[9] for c in cols], [c[-4] for c in cols]
    band = path_from(zip(xs, hi)) + "L" + "L".join(f"{num(x)},{num(y)}" for x, y in zip(reversed(xs), reversed(lo))) + "Z"
    svg = [
        f'<path d="M0,20H392" stroke="{MUTED}" stroke-dasharray="3 4" opacity=".6"/>',
        mono(10, 15, "goal", 9, MUTED),
        f'<path d="{band}" fill="{a}" fill-opacity=".1" class="fade"/>',
    ]
    svg += [f'<path d="{path_from(zip(xs, w))}" pathLength="1" class="draw" fill="none" stroke="{a}"'
            f' stroke-opacity=".26" style="animation-delay:{num(i * 0.04)}s"/>' for i, w in enumerate(walks)]
    svg.append(f'<path d="{path_from(zip(xs, mid))}" pathLength="1" class="draw" fill="none" stroke="{a}"'
               f' stroke-width="2.2" style="animation-delay:.3s"/>')
    svg.append(f'<circle cx="{xs[-1]}" cy="{num(mid[-1])}" r="3.5" fill="{a}" class="pop"/>')
    svg.append(mono(382, 62, "monte carlo · p20–p80", 9, SUB, anchor="end"))
    return "".join(svg)


def viz_route(a, rnd):
    route = "M18,48C70,70 150,70 206,60C262,50 320,50 374,20"
    svg = []
    for k, (amp, base) in enumerate(((6, 14), (7, 34), (5, 56))):
        pts = [(x, base + amp * math.sin(x / 38 + k * 1.7)) for x in range(0, 400, 8)]
        svg.append(f'<path d="{path_from(pts)}" fill="none" stroke="{STONE}" stroke-opacity=".12"/>')
    svg += [
        f'<path d="M18,48L374,20" stroke="{RED}" stroke-opacity=".55" stroke-dasharray="3 4"/>',
        f'<circle cx="200" cy="31" r="15" fill="{RED}" fill-opacity=".12"/>',
        f'<path transform="translate(200,31)" d="M0,-7L7,5H-7ZM0,-2.5V1M0,2.8V3.2" fill="none" stroke="{RED}"'
        ' stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/>',
        mono(200, 10, "landslide risk", 8.5, RED, anchor="middle"),
        f'<path d="{route}" pathLength="1" class="draw" fill="none" stroke="{a}" stroke-width="2"/>',
        f'<circle cx="18" cy="48" r="4.5" fill="{INSET}" stroke="{a}" stroke-width="1.6"/>',
        f'<circle cx="374" cy="20" r="4.5" fill="{a}"/>',
        f'<circle r="3.2" fill="{TEXT}" class="hold"><animateMotion dur="8s" repeatCount="indefinite" path="{route}"'
        ' keyPoints="0;0;1;1" keyTimes="0;.06;.42;1" calcMode="linear"/></circle>',
        mono(386, 62, "risk-aware A*", 9, a, anchor="end"),
    ]
    return "".join(svg)


def viz_yield(a, rnd):
    vals = (0.42, 0.47, 0.45, 0.52, 0.55, 0.53, 0.6, 0.63, 0.61, 0.68, 0.7, 0.74)
    svg = [f'<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}" stop-opacity=".8"/>'
           f'<stop offset="1" stop-color="{a}" stop-opacity=".15"/></linearGradient>',
           f'<path d="M0,62.5H392" stroke="{LINE}"/>']
    tops = []
    for i, v in enumerate(vals):
        h, x = v * 56, 12 + i * 24
        tops.append((x + 8, 62 - h))
        svg.append(f'<rect x="{x}" y="{num(62 - h)}" width="16" height="{num(h)}" rx="3" fill="url(#bar)" class="grow"'
                   f' style="animation-delay:{num(i * 0.06)}s"/>')
    n = len(tops)
    mx, my = sum(x for x, _ in tops) / n, sum(y for _, y in tops) / n
    slope = sum((x - mx) * (y - my) for x, y in tops) / sum((x - mx) ** 2 for x, _ in tops)
    fit = lambda x: my + slope * (x - mx)  # noqa: E731
    x_end, x_far = tops[-1][0], 382
    svg += [
        f'<path d="M{num(tops[0][0])},{num(fit(tops[0][0]))}L{num(x_end)},{num(fit(x_end))}" pathLength="1"'
        f' class="draw" stroke="{TEXT}" stroke-opacity=".6" stroke-width="1.4" style="animation-delay:.6s"/>',
        f'<path d="M{num(x_end)},{num(fit(x_end))}L{x_far},{num(fit(x_far) - 14)}L{x_far},{num(fit(x_far) + 14)}Z"'
        f' fill="{a}" fill-opacity=".14" class="fade"/>',
        f'<path d="M{num(x_end)},{num(fit(x_end))}L{x_far},{num(fit(x_far))}" stroke="{a}" stroke-dasharray="3 3"'
        ' class="fade"/>',
        mono(10, 12, "yield trend + 80% range", 9, a),
    ]
    return "".join(svg)


def viz_chat(a, rnd):
    ask, reply = "kal barish hogi?", "70% chance of rain · hold irrigation"
    ask_w, reply_w = mono_width(ask, 10.5) + 24, mono_width(reply, 10.5) + 24
    css = (
        "<style>.u{animation:u 8s ease infinite both}"
        "@keyframes u{0%{opacity:0;transform:translateY(6px)}7%,90%{opacity:1;transform:none}100%{opacity:0}}"
        ".ty{animation:ty 8s steps(1) infinite both}@keyframes ty{0%,11%{opacity:0}12%,29%{opacity:1}30%,100%{opacity:0}}"
        ".b{animation:b 8s ease infinite both}"
        "@keyframes b{0%,29%{opacity:0;transform:translateY(6px)}35%,90%{opacity:1;transform:none}100%{opacity:0}}"
        ".dot{animation:dot .9s ease-in-out infinite}@keyframes dot{0%,100%{transform:none}40%{transform:translateY(-3px)}}"
        "</style>"
    )
    return css + "".join([
        mono(10, 16, "HI / EN", 9, MUTED),
        f'<g class="u"><rect x="{num(382 - ask_w)}" y="6" width="{num(ask_w)}" height="24" rx="12" fill="{a}"'
        f' fill-opacity=".14" stroke="{a}" stroke-opacity=".4"/>{mono(370, 22, ask, 10.5, TEXT, anchor="end")}</g>',
        f'<g class="ty" opacity="0"><rect x="10" y="36" width="46" height="24" rx="12" fill="#1F1F23" stroke="{LINE}"/>'
        + "".join(f'<circle cx="{24 + i * 9}" cy="48" r="2.4" fill="{SUB}" class="dot" style="animation-delay:{i * 0.15}s"/>'
                  for i in range(3)) + "</g>",
        f'<g class="b"><rect x="10" y="36" width="{num(reply_w)}" height="24" rx="12" fill="#1F1F23" stroke="{LINE}"/>'
        f'{mono(22, 52, reply, 10.5, TEXT)}</g>',
    ])


def viz_cycle(a, rnd):
    css = (
        "<style>.pl{fill:none;stroke-width:2.4;stroke-linecap:round;stroke-dasharray:16 84;"
        "animation:pl 8s linear infinite both}"
        "@keyframes pl{0%{stroke-dashoffset:16;opacity:1}7.5%{stroke-dashoffset:-100;opacity:1}7.6%,100%{opacity:0}}"
        ".dl{animation:dl 8s ease infinite both}"
        "@keyframes dl{0%,32%{opacity:0}36%,58%{opacity:1}62%,100%{opacity:0}}"
        ".rs{animation:rs 8s ease infinite both}@keyframes rs{0%,62%{opacity:0}66%,90%{opacity:1}100%{opacity:0}}"
        "</style>"
    )
    marker = lambda k, c: (f'<marker id="arr-{k}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6"'  # noqa: E731
                           f' orient="auto"><path d="M0,0L8,4L0,8Z" fill="{c}"/></marker>')
    edges = ["M54,26H124", "M154,26H224", "M254,26H324", "M340,39C340,67 40,67 40,42"]
    nodes = [("P1", 40, "c"), ("R1", 140, "s"), ("P2", 240, "c"), ("R2", 340, "s")]

    def shape(kind, x, stroke, fill=INSET):
        if kind == "c":
            return f'<circle cx="{x}" cy="26" r="13" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        return f'<rect x="{x - 12}" y="14" width="24" height="24" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'

    svg = [css, "<defs>", marker("n", MUTED), marker("r", RED), "</defs>"]
    svg += [f'<path d="{d}" fill="none" stroke="{MUTED}" stroke-width="1.3" marker-end="url(#arr-n)"/>' for d in edges]
    svg += [f'<path d="{d}" pathLength="100" class="pl" stroke="{a}" style="animation-delay:{num(i * 0.6)}s"/>'
            for i, d in enumerate(edges)]
    for label, x, kind in nodes:
        svg.append(shape(kind, x, a) + mono(x, 29.5, label, 10, TEXT, anchor="middle"))
    svg.append('<g class="dl">' + "".join(
        f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="1.6" marker-end="url(#arr-r)"/>' for d in edges)
        + "".join(shape(kind, x, RED, fill="none") for _, x, kind in nodes)
        + mono(190, 52, "cycle detected", 9, RED, anchor="middle") + "</g>")
    svg.append('<g class="rs">' + shape("c", 240, MUTED) + mono(240, 29.5, "P2", 10, MUTED, anchor="middle")
               + f'<path d="M234,20L246,32M246,20L234,32" stroke="{RED}" stroke-width="1.5"/>'
               + mono(190, 52, "P2 terminated · resolved", 9, GREEN, anchor="middle") + "</g>")
    return "".join(svg)


def viz_ring(a, rnd):
    css = (
        "<style>.rp{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-dasharray:18 82;"
        "animation:rp 8s linear infinite both}"
        "@keyframes rp{0%{stroke-dashoffset:18;opacity:1}6%{stroke-dashoffset:-100;opacity:1}6.1%,100%{opacity:0}}"
        "</style>"
    )
    ring = [(196, 17), (238, 22), (250, 49), (210, 58), (178, 39)]
    others = [(20, 24), (52, 52), (86, 20), (118, 44), (146, 16), (292, 18), (320, 48), (352, 24), (378, 54), (150, 60)]
    links = [(0, 1), (1, 2), (2, 3), (3, 4), (3, 9), (4, 1)]
    bridges = [((118, 44), ring[4]), ((146, 16), ring[0]), (ring[1], (292, 18)), (ring[2], (320, 48))]
    cycle = [path_from((ring[i], ring[(i + 1) % len(ring)])) for i in range(len(ring))]
    hull = path_from(ring) + "Z"
    svg = [css, f'<g stroke="{MUTED}" stroke-opacity=".5">']
    svg += [f'<path d="{path_from((others[i], others[j]))}"/>' for i, j in links]
    svg += [f'<path d="{path_from((u, v))}"/>' for u, v in bridges]
    svg += [f'<path d="{path_from(((292, 18), (320, 48)))}"/><path d="{path_from(((320, 48), (352, 24)))}"/>'
            f'<path d="{path_from(((352, 24), (378, 54)))}"/>']
    svg += [f'<path d="{d}"/>' for d in cycle] + ["</g>"]
    svg += [f'<path d="{d}" pathLength="100" class="rp" stroke="{a}" style="animation-delay:{num(i * 0.48)}s"/>'
            for i, d in enumerate(cycle)]
    svg += [f'<circle cx="{x}" cy="{y}" r="3.2" fill="{INSET}" stroke="{SUB}" stroke-width="1.2"/>' for x, y in others]
    svg += [f'<circle cx="{x}" cy="{y}" r="4" fill="{INSET}" stroke="{a}" stroke-width="1.5"/>' for x, y in ring]
    svg.append(f'<g class="fade"><path d="{hull}" fill="{RED}" fill-opacity=".1" stroke="{RED}" stroke-width="1.5"'
               ' stroke-linejoin="round"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{RED}"/>' for x, y in ring)
               + mono(386, 12, "ring flagged · 5 accounts", 9, RED, anchor="end") + "</g>")
    return "".join(svg)


VIZ = {"fan": viz_fan, "route": viz_route, "yield": viz_yield, "chat": viz_chat, "cycle": viz_cycle, "ring": viz_ring}


def card(p: dict, seed: int) -> str:
    W, H = 440, 262
    a = p["accent"]
    defs, back, border = frame(W, H, 18, "card")
    defs += (f'<radialGradient id="card-glow"><stop offset="0" stop-color="{a}" stop-opacity=".08"/>'
             f'<stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
             '<clipPath id="band"><rect width="392" height="68" rx="10"/></clipPath>')
    out = [back, '<g clip-path="url(#card-clip)">',
           f'<circle cx="{W - 40}" cy="0" r="220" fill="url(#card-glow)"/>',
           f'<rect x="24" y="22" width="44" height="44" rx="12" fill="{a}" fill-opacity=".08" stroke="{a}" stroke-opacity=".35"/>',
           f'<path transform="translate(46,44)" d="{icon_path(p["icon"])}" fill="none" stroke="{a}" stroke-width="1.7"'
           ' stroke-linecap="round" stroke-linejoin="round"/>',
           mono(84, 38, p["label"], 10.5, a),
           sans(84, 61, p["title"], 21, TEXT, weight=600)]

    if p.get("team"):
        members = p["team"]
        for i, initial in enumerate(members):
            x = W - 24 - 11 - (len(members) - 1 - i) * 17
            ring = SAND if i == len(members) - 1 else LINE
            out.append(f'<circle cx="{x}" cy="37" r="12" fill="{INSET}" stroke="#111113" stroke-width="3"/>'
                       f'<circle cx="{x}" cy="37" r="11" fill="{INSET}" stroke="{ring}"/>'
                       + mono(x, 40.5, initial, 10, TEXT if ring == SAND else SUB, anchor="middle"))
    else:
        chip = "LIVE" if p["live"] else "CODE"
        chip_w = mono_width(chip, 10) + 32
        cx = W - 24 - chip_w
        dot = GREEN if p["live"] else MUTED
        out.append(f'<rect x="{num(cx)}" y="26" width="{num(chip_w)}" height="22" rx="11" fill="{INSET}" stroke="{LINE}"/>'
                   + (f'<circle cx="{num(cx + 12)}" cy="37" r="3" fill="{dot}" opacity="0" class="ping"/>' if p["live"] else "")
                   + f'<circle cx="{num(cx + 12)}" cy="37" r="3" fill="{dot}"/>' + mono(cx + 21, 40.5, chip, 10, SUB))

    viz = VIZ[p["viz"]](a, random.Random(seed))
    out.append(f'<g transform="translate(24,80)"><rect width="392" height="68" rx="10" fill="{INSET}" stroke="{LINE}"/>'
               f'<g clip-path="url(#band)">{viz}</g></g>')

    lines = wrap(p["blurb"], 56)
    assert len(lines) <= 2, f"{p['slug']}: blurb wraps to {len(lines)} lines"
    out += [sans(24, 176 + i * 20, line, 13.5, SUB) for i, line in enumerate(lines)]

    x = 24
    for tag in p["tags"]:
        w = mono_width(tag, 10.5) + 20
        out.append(f'<rect x="{num(x)}" y="214" width="{num(w)}" height="24" rx="12" fill="{INSET}" stroke="{LINE}"/>'
                   + mono(x + 10, 230, tag, 10.5, SUB))
        x += w + 8
    assert x <= W - 16, f"{p['slug']}: tags overflow"
    out.append("</g>" + border)
    label = f"{p['title']} — {p['blurb']} Built with {', '.join(p['tags'])}."
    return document(W, H, "".join(out), label=label, css=RISE + CARD_CSS, defs=defs)


# ── connect buttons ────────────────────────────────────────────────────────
def button(icon: str, title: str, sub: str, a: str) -> str:
    W, H = 400, 76
    defs, back, border = frame(W, H, 16, "btn")
    css = (".nudge{animation:nudge 3s ease-in-out infinite}"
           "@keyframes nudge{0%,60%,100%{transform:none}30%{transform:translate(2px,-2px)}}")
    out = (
        back + '<g clip-path="url(#btn-clip)">'
        + f'<rect x="16" y="16" width="44" height="44" rx="12" fill="{a}" fill-opacity=".08" stroke="{a}" stroke-opacity=".35"/>'
        + f'<path transform="translate(38,38)" d="{icon_path(icon)}" fill="none" stroke="{a}" stroke-width="1.7"'
          ' stroke-linecap="round" stroke-linejoin="round"/>'
        + sans(76, 36, title, 17, TEXT, weight=600) + mono(76, 56, sub, 12, MUTED)
        + f'<g class="nudge"><path transform="translate({W - 36},38)" d="M-6,6L6,-6M-3,-6H6V3" fill="none" stroke="{SUB}"'
          ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>'
        + "</g>" + border
    )
    return document(W, H, out, label=f"{title}: {sub}", css=css, defs=defs)


# ── footer ─────────────────────────────────────────────────────────────────
def footer() -> str:
    W, H = 1200, 200
    defs, back, border = frame(W, H, 24, "foot")
    css = (
        ".say{animation:say 16s ease infinite both}"
        "@keyframes say{0%{opacity:0;transform:translateY(6px)}4%,21%{opacity:1;transform:none}"
        "25%,100%{opacity:0;transform:translateY(-6px)}}"
        ".wv{animation:wv linear infinite}@keyframes wv{to{transform:translateX(-300px)}}"
        ".wr{animation:wr linear infinite}@keyframes wr{from{transform:translateX(-300px)}to{transform:none}}"
    )
    waves = []
    for amp, base, color, opacity, dur, cls in ((7, 160, STONE, ".22", 24, "wv"), (9, 170, SAND, ".3", 32, "wr"),
                                                (6, 181, SLATE, ".2", 40, "wv")):
        pts = [(x, base + amp * math.sin(2 * math.pi * x / 300)) for x in range(0, W + 310, 10)]
        waves.append(f'<g class="{cls}" style="animation-duration:{dur}s"><path d="{path_from(pts)}" fill="none"'
                     f' stroke="{color}" stroke-opacity="{opacity}" stroke-width="1.2"/></g>')
    says = "".join(
        f'<text x="600" y="90" text-anchor="middle" font-family="{SERIF}" font-size="30" font-style="italic"'
        f' fill="{TEXT}" opacity="{1 if i == 0 else 0}" class="say" style="animation-delay:{i * 4}s">{esc(line)}</text>'
        for i, line in enumerate(CLOSERS)
    )
    out = (back + '<g clip-path="url(#foot-clip)">' + "".join(waves) + says
           + mono(600, 126, "thanks for stopping by  ·  github.com/Deepak17kb", 12.5, MUTED, anchor="middle")
           + "</g>" + border)
    return document(W, H, out, label="Punjab to the world, one commit at a time.", css=css, defs=defs)


def main() -> None:
    files = {"hero.svg": hero(), "about.svg": about_card(), "footer.svg": footer()}
    files |= {f"sections/{slug}.svg": section(i, title, cap) for slug, i, title, cap in SECTIONS}
    files |= {f"projects/{p['slug']}.svg": card(p, seed) for seed, p in enumerate(PROJECTS)}
    files |= {f"connect/{slug}.svg": button(icon, title, sub, a) for slug, icon, title, sub, a in LINKS}
    for name, svg in files.items():
        path = ASSETS / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg, encoding="utf-8", newline="\n")
        print(f"{name:32} {len(svg.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
