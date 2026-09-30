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
    AMBER, BLUE, CYAN, INSET, LINE, MINT, MONO_W, MUTED, PINK, RED, SANS, SUB, TEXT, VIOLET,
    discrete, document, esc, frame, mono, mono_width, num, sans,
)

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# ── content ────────────────────────────────────────────────────────────────
ROLES = [
    "Data & AI, in the making",
    "Full stack with an intelligence layer",
    "Learning fast, building faster",
    "From Punjab, for the world",
]

CHIPS = [("pin", "Jalandhar, Punjab"), ("spark", "CSE · data science track"), ("dot", "Status: active")]

PROMPT = [("deepak", CYAN), ("@", MUTED), ("punjab", VIOLET), (" ~ ", BLUE), ("$ ", TEXT)]
SESSION = [
    ("cmd", "whoami"),
    ("out", [("Deepak", TEXT), (" · CSE undergrad, 2nd year · data science track", SUB)]),
    ("cmd", "cat focus.md"),
    ("out", [("▸ ", CYAN), ("full-stack development with AI layered in", SUB)]),
    ("out", [("▸ ", CYAN), ("always mid-project, always learning alongside it", SUB)]),
    ("out", [("▸ ", CYAN), ("goal: a full-stack engineer fluent in AI-native systems", SUB)]),
    ("cmd", "ls ~/learning"),
    ("out", [("design-analysis-of-algorithms/", BLUE), ("  data-structures/", BLUE),
             ("  data-analysis/", BLUE), ("  java/", BLUE)]),
    ("cmd", "cat interests.txt"),
    ("out", [("AI · automation · voice tech · ML apps · open source · cloud · UI", SUB)]),
    ("cmd", "echo $OFFLINE_MODE"),
    ("out", [("strategy games", TEXT)]),
    ("cmd", ""),
]
FACTS = [
    ("role", "CSE undergrad · year 2"),
    ("track", "data science"),
    ("builds", "full-stack × AI"),
    ("stack", "Python · JS/TS · C++ · SQL"),
    ("based", "Jalandhar, Punjab, IN"),
    ("status", "active"),
    ("mode", "learning, always"),
]

SECTIONS = [
    ("about", "01", "About", "whoami"),
    ("work", "02", "Featured work", "selected builds · click a card"),
    ("toolkit", "03", "Toolkit", "languages · frameworks · data"),
    ("activity", "04", "GitHub activity", "rebuilt by github actions"),
    ("connect", "05", "Connect", "say hello"),
]

PROJECTS = [
    dict(slug="broadbridge", title="BroadBridge", label="AI · FINTECH", accent=VIOLET, icon="bridge",
         viz="fan", live=True, tags=["TypeScript", "React", "Node.js", "239 tests"],
         blurb="Agentic wealth navigator. A shared TypeScript engine runs Monte "
               "Carlo projections in browser and server."),
    dict(slug="ner-saferoute", title="NER SafeRoute", label="GEOSPATIAL · ML · SIH", accent=CYAN, icon="pin",
         viz="route", live=True, tags=["FastAPI", "PostGIS", "React", "Leaflet"],
         blurb="Hazard-safe routing for Northeast India: ML road-risk scores, live "
               "hazard feeds and a vehicle-aware A* router."),
    dict(slug="agriflow", title="AgriFlow AI", label="DATA · FORECASTING", accent=MINT, icon="leaf",
         viz="yield", live=True, tags=["Python", "Streamlit", "scikit-learn", "Plotly"],
         blurb="Crop and food-security analytics for 68 countries and 22 crops, with "
               "a RandomForest outlook and yield ranges."),
    dict(slug="krishimitra", title="KrishiMitra", label="GEN AI · AGRITECH", accent=AMBER, icon="chat",
         viz="chat", live=False, tags=["Node.js", "Express", "Gemini", "Vanilla JS"],
         blurb="AI farming companion in Hindi and English: crop advice, live weather, "
               "mandi prices and government schemes."),
    dict(slug="deadlock-lab", title="Deadlock Runtime Lab", label="OPERATING SYSTEMS", accent=PINK, icon="lock",
         viz="cycle", live=True, tags=["React 19", "Vite", "Express 5", "SQLite"],
         blurb="A resource-allocation graph you can run: a deterministic scheduler "
               "exposes contention and DFS finds the deadlock."),
    dict(slug="hiring-analytics", title="Hiring Analytics", label="BUSINESS INTELLIGENCE", accent=BLUE, icon="bars",
         viz="dash", live=False, tags=["Power BI", "Dashboards", "Workforce data"],
         blurb="Power BI dashboard on global hiring trends, salaries and workforce "
               "insights, built on real-world datasets."),
]

LINKS = [
    ("linkedin", "user", "LinkedIn", "in/deepak-kumar-behera-", CYAN),
    ("github", "branch", "Follow on GitHub", "@Deepak17kb", VIOLET),
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
    ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite both}"
    "@keyframes ping{0%{transform:scale(1);opacity:.8}70%,100%{transform:scale(3.2);opacity:0}}"
    ".blink{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    ".scan{animation:scan 9s linear infinite}"
    "@keyframes scan{from{transform:translateY(0)}to{transform:translateY(900px)}}"
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
        "bars": "M-10,9H10M-6,9V2M-1,9V-3M4,9V-8",
        "user": "M0,-2A4.5,4.5 0 1 0 0,-11A4.5,4.5 0 1 0 0,-2ZM-9,10C-9,4 -5,1 0,1C5,1 9,4 9,10",
        "branch": "M-5,-4.4V5.4M6,-0.4C6,4 -5,2 -5,5.4M-2.4,-7A2.6,2.6 0 1 1 -7.6,-7A2.6,2.6 0 1 1 -2.4,-7"
                  "M-2.4,8A2.6,2.6 0 1 1 -7.6,8A2.6,2.6 0 1 1 -2.4,8M8.6,-3A2.6,2.6 0 1 1 3.4,-3A2.6,2.6 0 1 1 8.6,-3",
    }[name]


# ── hero ───────────────────────────────────────────────────────────────────
def hero() -> str:
    W, H, HOR = 1200, 440, 352
    rnd = random.Random(17)
    defs, back, border = frame(W, H, 28, "hero", period=14)
    css = RISE + (
        ".tw{animation:tw 4s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.12}50%{opacity:1}}"
        ".d1{animation:d1 16s ease-in-out infinite alternate}@keyframes d1{to{transform:translate(90px,40px)}}"
        ".d2{animation:d2 20s ease-in-out infinite alternate}@keyframes d2{to{transform:translate(-80px,50px)}}"
        ".d3{animation:d3 24s ease-in-out infinite alternate}@keyframes d3{to{transform:translate(70px,-30px)}}"
        ".sig{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-dasharray:10 190;"
        "animation:sig 3.6s cubic-bezier(.45,0,.25,1) infinite both}"
        "@keyframes sig{0%{stroke-dashoffset:10}25%,100%{stroke-dashoffset:-100}}"
        ".node-ping{transform-box:fill-box;transform-origin:center;animation:np 3.6s ease-out infinite both}"
        "@keyframes np{0%{transform:scale(1);opacity:.85}28%,100%{transform:scale(3.4);opacity:0}}"
        ".draw{opacity:0;fill:none;stroke:#00FFF2;stroke-width:1.3;stroke-dasharray:620;"
        "animation:draw 3s cubic-bezier(.6,0,.3,1) both}"
        "@keyframes draw{0%{stroke-dashoffset:620;opacity:1}70%{stroke-dashoffset:0;opacity:1}"
        "100%{stroke-dashoffset:0;opacity:0}}"
        ".fill{animation:fillin 3s ease both}@keyframes fillin{0%,45%{opacity:0}100%{opacity:1}}"
        ".ga{opacity:0;animation:ga 7s steps(1) 3.4s infinite}"
        ".gb{opacity:0;animation:gb 7s steps(1) 3.45s infinite}"
        "@keyframes ga{0%,90%,100%{opacity:0;transform:none}91%{opacity:.9;transform:translate(-7px,0)}"
        "92%{opacity:.9;transform:translate(4px,0)}93%{opacity:.6;transform:translate(-2px,0)}94%{opacity:0}}"
        "@keyframes gb{0%,90%,100%{opacity:0;transform:none}91%{opacity:.9;transform:translate(6px,0)}"
        "92%{opacity:.9;transform:translate(-5px,0)}93%{opacity:.6;transform:translate(3px,0)}94%{opacity:0}}"
    )
    defs += (
        '<linearGradient id="hero-bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#05050B"/><stop offset=".6" stop-color="#090817"/>'
        '<stop offset="1" stop-color="#0E0A1F"/></linearGradient>'
        + "".join(
            f'<radialGradient id="blob-{k}"><stop offset="0" stop-color="{c}" stop-opacity="{o}"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
            for k, c, o in (("v", VIOLET, ".40"), ("c", CYAN, ".30"), ("b", BLUE, ".30"))
        )
        + f'<linearGradient id="name-fill" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="520" y2="0"'
        f' spreadMethod="reflect"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/>'
        f'<stop offset="1" stop-color="{VIOLET}"/>'
        '<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="920 0"'
        ' dur="9s" repeatCount="indefinite"/></linearGradient>'
        '<filter id="soft" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>'
        '<linearGradient id="fade-y" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#fff"/></linearGradient>'
        '<linearGradient id="fade-x"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".3" stop-color="#fff"/><stop offset=".7" stop-color="#fff"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="floor-y" maskUnits="userSpaceOnUse" x="0" y="{HOR}" width="{W}" height="{H - HOR}">'
        f'<rect x="0" y="{HOR}" width="{W}" height="{H - HOR}" fill="url(#fade-y)"/></mask>'
        f'<mask id="floor-x" maskUnits="userSpaceOnUse" x="0" y="{HOR}" width="{W}" height="{H - HOR}">'
        f'<rect x="0" y="{HOR}" width="{W}" height="{H - HOR}" fill="url(#fade-x)"/></mask>'
        f'<linearGradient id="horizon"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{CYAN}" stop-opacity=".9"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>'
        '</linearGradient>'
        f'<linearGradient id="horizon-glow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}"'
        f' stop-opacity="0"/><stop offset="1" stop-color="{VIOLET}" stop-opacity=".16"/></linearGradient>'
        f'<linearGradient id="scan-band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"'
        f' stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".05"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>'
        '<clipPath id="slices"><rect x="60" y="148" width="480" height="20"/><rect x="60" y="186" width="480" height="14"/>'
        '<rect x="60" y="208" width="480" height="8"/></clipPath>'
    )

    out = [back, '<g clip-path="url(#hero-clip)">', f'<rect width="{W}" height="{H}" fill="url(#hero-bg)"/>']

    # Aurora and stars.
    out.append(
        '<ellipse cx="260" cy="60" rx="460" ry="230" fill="url(#blob-v)" class="d1"/>'
        '<ellipse cx="1000" cy="120" rx="400" ry="250" fill="url(#blob-c)" class="d2"/>'
        '<ellipse cx="640" cy="440" rx="560" ry="190" fill="url(#blob-b)" class="d3"/>'
    )
    for _ in range(95):
        x, y = rnd.uniform(12, W - 12), rnd.uniform(12, HOR - 24)
        r = rnd.choice((0.6, 0.8, 1.0, 1.2, 1.6))
        color = rnd.choice(("#FFFFFF", "#FFFFFF", CYAN, VIOLET))
        style = f"animation-duration:{num(rnd.uniform(2.8, 6.5))}s;animation-delay:{num(-rnd.uniform(0, 6))}s"
        out.append(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(r)}" fill="{color}" class="tw" style="{style}"/>')

    # Perspective floor: rails converge on a vanishing point, rungs roll toward the viewer.
    vp_y = HOR - 36
    floor = []
    for i in range(-18, 19):
        xb = 600 + i * 80
        xh = 600 + (xb - 600) * (HOR - vp_y) / (H - vp_y)
        floor.append(f'<path d="M{num(xh)},{HOR}L{num(xb)},{H}"/>')
    depth = H - HOR + 14
    for z in range(2, 16):
        a, b = num(HOR + depth / z), num(HOR + depth / (z - 1))
        floor.append(
            f'<line x1="0" x2="{W}" y1="{a}" y2="{a}">'
            f'<animate attributeName="y1" values="{a};{b}" dur="1.6s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="{a};{b}" dur="1.6s" repeatCount="indefinite"/></line>'
        )
    out.append(
        f'<rect x="0" y="{HOR - 60}" width="{W}" height="60" fill="url(#horizon-glow)"/>'
        f'<g mask="url(#floor-y)"><g mask="url(#floor-x)" stroke="{VIOLET}" stroke-opacity=".55" fill="none">'
        + "".join(floor)
        + f'</g></g><rect x="0" y="{HOR - 0.75}" width="{W}" height="1.5" fill="url(#horizon)"/>'
    )
    out.append(f'<rect class="scan" x="0" y="-160" width="{W}" height="160" fill="url(#scan-band)"/>')

    # A small network running a forward pass, left to right.
    layers, xs = (3, 5, 5, 2), (835, 935, 1035, 1125)
    colors = (CYAN, BLUE, BLUE, VIOLET)
    nodes = [[(xs[l], 186 + (j - (n - 1) / 2) * 46) for j in range(n)] for l, n in enumerate(layers)]
    edges, signals = [], []
    for l in range(len(layers) - 1):
        for a in nodes[l]:
            for b in nodes[l + 1]:
                d = path_from((a, b))
                edges.append(f'<path d="{d}"/>')
                if rnd.random() < 0.72:
                    delay = l * 0.9 + rnd.uniform(0, 0.18)
                    signals.append(
                        f'<path d="{d}" pathLength="100" class="sig" stroke="{colors[l + 1]}"'
                        f' style="animation-delay:{num(delay)}s"/>'
                    )
    out.append(f'<g stroke="#8E8EFF" stroke-opacity=".14" fill="none">{"".join(edges)}</g>')
    out.extend(signals)
    for l, column in enumerate(nodes):
        for x, y in column:
            out.append(
                f'<circle cx="{num(x)}" cy="{num(y)}" r="6" fill="none" stroke="{colors[l]}" opacity="0"'
                f' class="node-ping" style="animation-delay:{num(l * 0.9)}s"/>'
                f'<circle cx="{num(x)}" cy="{num(y)}" r="6.5" fill="#0A0A13" stroke="{colors[l]}" stroke-width="1.8"/>'
                f'<circle cx="{num(x)}" cy="{num(y)}" r="2.4" fill="{colors[l]}"/>'
            )

    # Greeting, typed.
    greet = "// hello world, i'm"
    cw = 17 * MONO_W
    frames = [(0, 0)] + [(0.3 + k * 0.05, num((k + 1) * cw + 2)) for k in range(len(greet))]
    out.append(
        f'<clipPath id="greet-clip"><rect x="82" y="96" width="{num(len(greet) * cw + 2)}" height="30">'
        f'{discrete("width", frames, 0.3 + len(greet) * 0.05 + 0.05)}</rect></clipPath>'
        f'<g clip-path="url(#greet-clip)">{mono(84, 118, greet, 17, CYAN)}</g>'
    )

    # Name: outline draws itself, fill fades up, an occasional glitch.
    name_attrs = f' font-family="{SANS}" font-size="112" font-weight="800" letter-spacing="-1.5"'
    name = f'<text x="78" y="216"{name_attrs} %s>Deepak</text>'
    out.append(
        '<g class="fill">' + name % f'fill="{VIOLET}" opacity=".35" filter="url(#soft)"' + "</g>"
        + name % 'fill="url(#name-fill)" class="fill"'
        + '<g clip-path="url(#slices)">' + name % f'fill="{CYAN}" class="ga"' + name % f'fill="{PINK}" class="gb"'
        + "</g>" + name % 'class="draw"'
    )

    # Rotating roles, typed and deleted.
    size, per = 22, 4.2
    cw = size * MONO_W
    px, base = 110.4, 268
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
            f"{mono(px, base, phrase, size, TEXT)}</g>"
        )
    out.append(
        f'<g class="rise" style="animation-delay:1.2s">{mono(84, base, ">", size, CYAN)}'
        f'<clipPath id="role-clip"><rect x="{num(px - 1)}" y="{base - 26}" width="{num(first + 2)}" height="36">'
        f'{discrete("width", [(t, num(w + 2)) for t, w in widths], total, extra=loop)}</rect></clipPath>'
        f'<g clip-path="url(#role-clip)">{"".join(phrases)}</g>'
        f'<rect x="{num(px + first + 3)}" y="{base - 19}" width="11" height="24" fill="{CYAN}" opacity=".85" class="blink">'
        f'{discrete("x", [(t, num(px + w + 3)) for t, w in widths], total, extra=loop)}</rect></g>'
    )

    # Chips.
    x = 84
    for i, (icon, label) in enumerate(CHIPS):
        w = 48 + mono_width(label, 13)
        cx, cy = x + 19, 308
        if icon == "dot":
            glyph = (f'<circle cx="{cx}" cy="{cy}" r="4" fill="{MINT}" opacity="0" class="ping"/>'
                     f'<circle cx="{cx}" cy="{cy}" r="4" fill="{MINT}"/>')
        elif icon == "pin":
            glyph = f'<path transform="translate({cx},{cy}) scale(.72)" d="{icon_path("pin")}" fill="none" stroke="{CYAN}" stroke-width="2.2"/>'
        else:
            glyph = (f'<path transform="translate({cx},{cy})" d="M0,-6L1.6,-1.6L6,0L1.6,1.6L0,6L-1.6,1.6L-6,0L-1.6,-1.6Z"'
                     f' fill="{VIOLET}"/>')
        out.append(
            f'<g class="rise" style="animation-delay:{num(2 + i * 0.14)}s">'
            f'<rect x="{num(x)}" y="292" width="{num(w)}" height="32" rx="16" fill="#10101D" stroke="{LINE}"/>'
            f'{glyph}{mono(x + 34, 312.5, label, 13, SUB)}</g>'
        )
        x += w + 10

    out.append(mono(44, 50, "~/deepak17kb", 12, MUTED) + mono(1156, 50, "31.33°N · 75.58°E", 12, MUTED, anchor="end"))
    out.append("</g>" + border)
    return document(W, H, "".join(out), label="Deepak: Data & AI, full stack. Jalandhar, Punjab.", css=css, defs=defs)


# ── terminal ───────────────────────────────────────────────────────────────
def terminal() -> str:
    W, H = 1200, 492
    fs, lh = 16, 29
    cw = fs * MONO_W
    x0, y0, split = 32, 90, 824
    defs, back, border = frame(W, H, 20, "term", period=16)
    prompt_len = sum(len(t) for t, _ in PROMPT)
    css = RISE + ".blk{animation:blk 3.2s ease-in-out infinite}@keyframes blk{50%{opacity:.35}}"
    defs += (f'<linearGradient id="term-scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="{CYAN}" stop-opacity=".035"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>')

    def segments(x, y, parts):
        col, svg = 0, []
        for text, color in parts:
            svg.append(mono(x + col * cw, y, text, fs, color))
            col += len(text)
        return "".join(svg)

    # Build the timeline first, then emit each line with its own reveal.
    t, lines, cursor, typing = 0.9, [], [], []
    for idx, (kind, content) in enumerate(SESSION):
        y = y0 + idx * lh
        lines.append((idx, kind, content, y, t))
        if kind == "cmd":
            xc = x0 + prompt_len * cw
            cursor.append((t, xc, y))
            t += 0.45
            steps = [(t + k * 0.06, (k + 1) * cw) for k in range(len(content))]
            typing.append(steps)
            cursor += [(s, xc + w, y) for s, w in steps]
            t += len(content) * 0.06 + 0.35
        else:
            typing.append(None)
            t += 0.14
            if idx + 1 < len(SESSION) and SESSION[idx + 1][0] == "cmd":
                t += 0.4
    total = t + 0.2

    body = []
    for (idx, kind, content, y, start), steps in zip(lines, typing):
        reveal = discrete("opacity", [(0, 0), (start, 1)], total)
        if kind == "out":
            body.append(f"<g>{reveal}{segments(x0, y, content)}</g>")
            continue
        body.append(f"<g>{reveal}{segments(x0, y, PROMPT)}</g>")
        if content:
            xc = x0 + prompt_len * cw
            full = num(len(content) * cw + 1)
            frames = [(0, 0)] + [(s, num(w + 1)) for s, w in steps]
            body.append(
                f'<clipPath id="type-{idx}"><rect x="{num(xc - 1)}" y="{y - fs - 4}" width="{full}" height="{lh}">'
                f'{discrete("width", frames, total)}</rect></clipPath>'
                f'<g clip-path="url(#type-{idx})">{mono(xc, y, content, fs, TEXT)}</g>'
            )
    _, cx_end, cy_end = cursor[-1]
    body.append(
        f'<rect x="{num(cx_end)}" y="{num(cy_end - fs * 0.92)}" width="{num(cw)}" height="{num(fs * 1.22)}"'
        f' fill="{CYAN}" opacity=".85" class="blink">'
        + discrete("x", [(0, num(cursor[0][1]))] + [(s, num(x)) for s, x, _ in cursor], total)
        + discrete("y", [(0, num(cursor[0][2] - fs * 0.92))] + [(s, num(y - fs * 0.92)) for s, _, y in cursor], total)
        + "</rect>"
    )

    # Right pane: a neofetch-style card.
    fx, fy = split + 32, 92
    side = [mono(fx, fy, "deepak", 15, CYAN, weight=700) + mono(fx + 6 * 9, fy, "@", 15, MUTED)
            + mono(fx + 7 * 9, fy, "punjab", 15, VIOLET, weight=700),
            mono(fx, fy + 20, "─" * 22, 13, LINE)]
    for i, (key, value) in enumerate(FACTS):
        y = fy + 52 + i * 27
        side.append(mono(fx, y, key, 14, MUTED) + mono(fx + 9 * 8.4, y, value, 14, TEXT))
        if key == "status":
            dot_x = fx + 9 * 8.4 + mono_width(value, 14) + 12
            side.append(f'<circle cx="{num(dot_x)}" cy="{y - 5}" r="4" fill="{MINT}" opacity="0" class="ping"/>'
                        f'<circle cx="{num(dot_x)}" cy="{y - 5}" r="4" fill="{MINT}"/>')
    palette = (CYAN, MINT, BLUE, VIOLET, PINK, AMBER, TEXT, MUTED)
    py = fy + 52 + len(FACTS) * 27 + 6
    for i, color in enumerate(palette):
        side.append(f'<rect x="{fx + i * 30}" y="{py}" width="24" height="24" rx="5" fill="{color}" class="blk"'
                    f' style="animation-delay:{num(i * 0.18)}s"/>')
    side.append(mono(fx, py + 60, "uptime: always building", 13, MUTED))

    bar_y = H - 30
    status = (
        f'<rect x="0" y="{bar_y}" width="{W}" height="30" fill="#0F0F1E"/>'
        f'<path d="M0,{bar_y}H{W}" stroke="{LINE}"/>'
        f'<rect x="0" y="{bar_y}" width="128" height="30" fill="{CYAN}"/>'
        + mono(18, bar_y + 20, "deepak17kb", 12, "#05050B", weight=700)
        + mono(146, bar_y + 20, "0:zsh*", 12, TEXT) + mono(210, bar_y + 20, "1:ml", 12, MUTED)
        + mono(258, bar_y + 20, "2:web", 12, MUTED)
        + mono(W - 20, bar_y + 20, "Jalandhar, IN · UTC+5:30", 12, MUTED, anchor="end")
    )
    title_bar = (
        f'<rect width="{W}" height="44" fill="#0D0D18"/><path d="M0,44H{W}" stroke="{LINE}"/>'
        + "".join(f'<circle cx="{26 + i * 20}" cy="22" r="6" fill="{c}" opacity=".85"/>'
                  for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")))
        + mono(600, 27, "deepak@punjab: ~/about — tmux", 13, MUTED, anchor="middle")
    )
    out = (
        back + '<g clip-path="url(#term-clip)">' + title_bar
        + f'<path d="M{split},44V{bar_y}" stroke="{LINE}"/>'
        + "".join(body)
        + '<g class="rise" style="animation-delay:.4s">' + "".join(side) + "</g>"
        + status
        + f'<rect class="scan" x="0" y="-160" width="{W}" height="160" fill="url(#term-scan)"/>'
        + "</g>" + border
    )
    label = ("Terminal: whoami — Deepak, CSE undergrad (2nd year) on the data science track. "
             "Focus: full-stack development with AI layered in. Learning: design and analysis of algorithms, "
             "data structures, data analysis, Java. Offline: strategy games.")
    return document(W, H, out, label=label, css=css, defs=defs)


# ── section bars ───────────────────────────────────────────────────────────
def section(index: str, title: str, caption: str) -> str:
    W, H = 1200, 72
    defs, back, border = frame(W, H, 18, "sec", period=12)
    upper = title.upper()
    size, track = 22, 5
    t_w = sum(0.29 if c == " " else 0.64 for c in upper) * size + track * (len(upper) - 1)
    cap = "// " + caption
    lx0, lx1 = 86 + t_w + 28, W - 40 - mono_width(cap, 13) - 28
    css = RISE + (
        ".run{fill:none;stroke-width:2;stroke-linecap:round;stroke-dasharray:22 78;animation:run 4s linear infinite}"
        "@keyframes run{to{stroke-dashoffset:-100}}"
        ".sheen{animation:sheen 8s ease-in-out infinite}"
        "@keyframes sheen{0%{transform:translateX(0)}55%,100%{transform:translateX(1700px)}}"
    )
    defs += (
        f'<linearGradient id="run-grad" gradientUnits="userSpaceOnUse" x1="{num(lx0)}" x2="{num(lx1)}" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
        '<linearGradient id="sheen-grad"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        "</linearGradient>"
    )
    line = f"M{num(lx0)},36.5H{num(lx1)}"
    out = (
        back + '<g clip-path="url(#sec-clip)">'
        + f'<rect class="sheen" x="-360" y="0" width="300" height="{H}" fill="url(#sheen-grad)" transform="skewX(-20)"/>'
        + '<g class="rise">' + mono(40, 43, index, 15, CYAN, weight=700) + mono(64, 43, "/", 15, MUTED)
        + f'<text x="86" y="44.5" font-family="{SANS}" font-size="{size}" font-weight="700"'
          f' fill="{TEXT}" textLength="{num(t_w)}" lengthAdjust="spacing">{esc(upper)}</text></g>'
        + f'<path d="{line}" stroke="{LINE}" stroke-width="1.5"/>'
        + f'<path d="{line}" pathLength="100" class="run" stroke="url(#run-grad)"/>'
        + f'<circle cx="{num(lx0)}" cy="36.5" r="3.5" fill="{CYAN}"/>'
        + f'<circle cx="{num(lx1)}" cy="36.5" r="3.5" fill="{VIOLET}" opacity="0" class="ping"/>'
        + f'<circle cx="{num(lx1)}" cy="36.5" r="3.5" fill="{VIOLET}"/>'
        + f'<g class="rise" style="animation-delay:.2s">{mono(W - 40, 42, cap, 13, MUTED, anchor="end")}</g>'
        + "</g>" + border
    )
    return document(W, H, out, label=f"{index} · {title}", css=css, defs=defs)


# ── project cards ──────────────────────────────────────────────────────────
CARD_CSS = (
    ".glow{animation:glow 6s ease-in-out infinite}@keyframes glow{0%,100%{opacity:.5}50%{opacity:1}}"
    ".draw{stroke-dasharray:1 1;animation:draw 7s cubic-bezier(.5,0,.2,1) infinite both}"
    "@keyframes draw{0%{stroke-dashoffset:1}40%{stroke-dashoffset:0}88%{stroke-dashoffset:0;opacity:1}"
    "100%{stroke-dashoffset:0;opacity:0}}"
    ".fade{animation:fade 7s ease infinite both}@keyframes fade{0%,30%{opacity:0}45%,88%{opacity:1}100%{opacity:0}}"
    ".pop{transform-box:fill-box;transform-origin:center;animation:pop 7s ease infinite both}"
    "@keyframes pop{0%,38%{transform:scale(0)}44%{transform:scale(1.4)}48%,88%{transform:scale(1);opacity:1}100%{opacity:0}}"
    ".grow{transform-box:fill-box;transform-origin:50% 100%;animation:grow 7s cubic-bezier(.3,.7,.2,1) infinite both}"
    "@keyframes grow{0%{transform:scaleY(0)}25%,88%{transform:scaleY(1);opacity:1}100%{opacity:0}}"
    ".hold{animation:hold 7s infinite both}@keyframes hold{0%,88%{opacity:1}100%{opacity:0}}"
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
        f'<path d="M0,20H392" stroke="{MUTED}" stroke-dasharray="3 4" opacity=".7"/>',
        mono(10, 15, "goal", 9, MUTED),
        f'<path d="{band}" fill="{a}" fill-opacity=".12" class="fade"/>',
    ]
    svg += [f'<path d="{path_from(zip(xs, w))}" pathLength="1" class="draw" fill="none" stroke="{a}"'
            f' stroke-opacity=".3" style="animation-delay:{num(i * 0.04)}s"/>' for i, w in enumerate(walks)]
    svg.append(f'<path d="{path_from(zip(xs, mid))}" pathLength="1" class="draw" fill="none" stroke="{a}"'
               f' stroke-width="2.4" style="animation-delay:.3s"/>')
    svg.append(f'<circle cx="{xs[-1]}" cy="{num(mid[-1])}" r="4" fill="{a}" class="pop"/>')
    svg.append(mono(382, 62, "monte carlo · p20–p80", 9, SUB, anchor="end"))
    return "".join(svg)


def viz_route(a, rnd):
    route = "M18,48C70,70 150,70 206,60C262,50 320,50 374,20"
    svg = []
    for k, (amp, base) in enumerate(((6, 14), (7, 34), (5, 56))):
        pts = [(x, base + amp * math.sin(x / 38 + k * 1.7)) for x in range(0, 400, 8)]
        svg.append(f'<path d="{path_from(pts)}" fill="none" stroke="{a}" stroke-opacity=".1"/>')
    svg += [
        f'<path d="M18,48L374,20" stroke="{RED}" stroke-opacity=".6" stroke-dasharray="3 4"/>',
        f'<circle cx="200" cy="31" r="15" fill="{RED}" fill-opacity=".14"/>',
        f'<circle cx="200" cy="31" r="15" fill="none" stroke="{RED}" opacity="0" class="ping"/>',
        f'<path transform="translate(200,31)" d="M0,-7L7,5H-7ZM0,-2.5V1M0,2.8V3.2" fill="none" stroke="{RED}"'
        f' stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/>',
        mono(200, 10, "landslide risk", 8.5, RED, anchor="middle"),
        f'<path d="{route}" pathLength="1" class="draw" fill="none" stroke="{a}" stroke-width="7" stroke-opacity=".16"/>',
        f'<path d="{route}" pathLength="1" class="draw" fill="none" stroke="{a}" stroke-width="2.2"/>',
        f'<circle cx="18" cy="48" r="4.5" fill="{INSET}" stroke="{a}" stroke-width="1.8"/>',
        f'<circle cx="374" cy="20" r="5" fill="{a}" opacity="0" class="ping"/><circle cx="374" cy="20" r="5" fill="{a}"/>',
        f'<circle r="3.6" fill="#fff" class="hold"><animateMotion dur="7s" repeatCount="indefinite" path="{route}"'
        ' keyPoints="0;0;1;1" keyTimes="0;.06;.42;1" calcMode="linear"/></circle>',
        mono(386, 62, "risk-aware A*", 9, a, anchor="end"),
    ]
    return "".join(svg)


def viz_yield(a, rnd):
    vals = (0.42, 0.47, 0.45, 0.52, 0.55, 0.53, 0.6, 0.63, 0.61, 0.68, 0.7, 0.74)
    svg = [f'<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}" stop-opacity=".85"/>'
           f'<stop offset="1" stop-color="{a}" stop-opacity=".12"/></linearGradient>',
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
        f' class="draw" stroke="{TEXT}" stroke-opacity=".75" stroke-width="1.5" style="animation-delay:.6s"/>',
        f'<path d="M{num(x_end)},{num(fit(x_end))}L{x_far},{num(fit(x_far) - 14)}L{x_far},{num(fit(x_far) + 14)}Z"'
        f' fill="{a}" fill-opacity=".16" class="fade"/>',
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
        f' fill-opacity=".16" stroke="{a}" stroke-opacity=".45"/>{mono(370, 22, ask, 10.5, TEXT, anchor="end")}</g>',
        f'<g class="ty" opacity="0"><rect x="10" y="36" width="46" height="24" rx="12" fill="#16162A" stroke="{LINE}"/>'
        + "".join(f'<circle cx="{24 + i * 9}" cy="48" r="2.6" fill="{SUB}" class="dot" style="animation-delay:{i * 0.15}s"/>'
                  for i in range(3)) + "</g>",
        f'<g class="b"><rect x="10" y="36" width="{num(reply_w)}" height="24" rx="12" fill="#16162A" stroke="{LINE}"/>'
        f'{mono(22, 52, reply, 10.5, TEXT)}</g>',
    ])


def viz_cycle(a, rnd):
    css = (
        "<style>.pl{fill:none;stroke-width:2.6;stroke-linecap:round;stroke-dasharray:16 84;"
        "animation:pl 7s linear infinite both}"
        "@keyframes pl{0%{stroke-dashoffset:16;opacity:1}8.5%{stroke-dashoffset:-100;opacity:1}8.6%,100%{opacity:0}}"
        ".dl{animation:dl 7s steps(1) infinite both}"
        "@keyframes dl{0%,34%{opacity:0}36%,42%{opacity:1}44%{opacity:.25}46%,60%{opacity:1}62%,100%{opacity:0}}"
        ".rs{animation:rs 7s ease infinite both}@keyframes rs{0%,62%{opacity:0}66%,90%{opacity:1}100%{opacity:0}}"
        "</style>"
    )
    marker = lambda k, c: (f'<marker id="arr-{k}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6"'  # noqa: E731
                           f' orient="auto"><path d="M0,0L8,4L0,8Z" fill="{c}"/></marker>')
    edges = ["M54,26H124", "M154,26H224", "M254,26H324", "M340,39C340,67 40,67 40,42"]
    nodes = [("P1", 40, "c"), ("R1", 140, "s"), ("P2", 240, "c"), ("R2", 340, "s")]

    def shape(kind, x, stroke, fill=INSET, extra=""):
        if kind == "c":
            return f'<circle cx="{x}" cy="26" r="13" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{extra}/>'
        return f'<rect x="{x - 12}" y="14" width="24" height="24" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{extra}/>'

    svg = [css, "<defs>", marker("n", SUB), marker("r", RED), "</defs>"]
    svg += [f'<path d="{d}" fill="none" stroke="{SUB}" stroke-opacity=".5" stroke-width="1.4" marker-end="url(#arr-n)"/>'
            for d in edges]
    svg += [f'<path d="{d}" pathLength="100" class="pl" stroke="{a}" style="animation-delay:{num(i * 0.6)}s"/>'
            for i, d in enumerate(edges)]
    for label, x, kind in nodes:
        svg.append(shape(kind, x, a) + mono(x, 29.5, label, 10, TEXT, anchor="middle"))
    svg.append('<g class="dl">' + "".join(
        f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="1.8" marker-end="url(#arr-r)"/>' for d in edges)
        + "".join(shape(kind, x, RED, fill="none") for _, x, kind in nodes)
        + mono(190, 52, "cycle detected", 9, RED, anchor="middle") + "</g>")
    svg.append('<g class="rs">' + shape("c", 240, MUTED, fill=INSET) + mono(240, 29.5, "P2", 10, MUTED, anchor="middle")
               + f'<path d="M234,20L246,32M246,20L234,32" stroke="{RED}" stroke-width="1.6"/>'
               + mono(190, 52, "P2 terminated · resolved", 9, MINT, anchor="middle") + "</g>")
    return "".join(svg)


def viz_dash(a, rnd):
    css = ("<style>.donut{transform-box:fill-box;transform-origin:center;animation:donut 7s cubic-bezier(.3,.7,.2,1) infinite both}"
           "@keyframes donut{0%{transform:rotate(-140deg) scale(.5);opacity:0}22%,88%{transform:none;opacity:1}100%{opacity:0}}"
           "</style>")
    seg, acc = [], 0
    for share, color in ((46, a), (30, VIOLET), (24, CYAN)):
        seg.append(f'<circle cx="36" cy="36" r="21" fill="none" stroke="{color}" stroke-width="9" pathLength="100"'
                   f' stroke-dasharray="{share - 2} {102 - share}" stroke-dashoffset="{-acc}" transform="rotate(-90 36 36)"/>')
        acc += share
    svg = [css, f'<g class="donut"><circle cx="36" cy="36" r="21" fill="none" stroke="{LINE}" stroke-width="9"/>{"".join(seg)}</g>',
           mono(82, 11, "salary distribution", 8.5, MUTED), mono(252, 11, "hiring trend", 8.5, MUTED),
           f'<path d="M80,62.5H232M250,62.5H386" stroke="{LINE}"/>']
    for i in range(11):
        h = 40 * math.exp(-((i - 4) ** 2) / (2 * 2.3 ** 2)) + 4
        svg.append(f'<rect x="{82 + i * 14}" y="{num(62 - h)}" width="10" height="{num(h)}" rx="2" fill="{a}"'
                   f' fill-opacity=".75" class="grow" style="animation-delay:{num(i * 0.05)}s"/>')
    pts, y = [], 54.0
    for i in range(12):
        pts.append((252 + i * 12, y))
        y = max(20.0, y - rnd.uniform(-1.5, 5.5))
    area = path_from(pts) + f"L{num(pts[-1][0])},62L252,62Z"
    svg += [f'<path d="{area}" fill="{a}" fill-opacity=".12" class="fade"/>',
            f'<path d="{path_from(pts)}" pathLength="1" class="draw" fill="none" stroke="{a}" stroke-width="2"/>',
            f'<circle cx="{num(pts[-1][0])}" cy="{num(pts[-1][1])}" r="3.5" fill="{a}" class="pop"/>']
    return "".join(svg)


VIZ = {"fan": viz_fan, "route": viz_route, "yield": viz_yield, "chat": viz_chat, "cycle": viz_cycle, "dash": viz_dash}


def card(p: dict, seed: int) -> str:
    W, H = 440, 262
    a = p["accent"]
    defs, back, border = frame(W, H, 20, "card", accents=(a,), period=9)
    defs += (f'<radialGradient id="card-glow"><stop offset="0" stop-color="{a}" stop-opacity=".22"/>'
             f'<stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
             '<clipPath id="band"><rect width="392" height="68" rx="10"/></clipPath>')
    out = [back, '<g clip-path="url(#card-clip)">',
           f'<circle cx="{W - 30}" cy="10" r="210" fill="url(#card-glow)" class="glow"/>',
           f'<rect x="24" y="22" width="44" height="44" rx="12" fill="{a}" fill-opacity=".1" stroke="{a}" stroke-opacity=".45"/>',
           f'<path transform="translate(46,44)" d="{icon_path(p["icon"])}" fill="none" stroke="{a}" stroke-width="1.8"'
           ' stroke-linecap="round" stroke-linejoin="round"/>',
           mono(84, 38, p["label"], 10.5, a),
           sans(84, 61, p["title"], 21, TEXT, weight=700)]

    chip = "LIVE" if p["live"] else "CODE"
    chip_w = mono_width(chip, 10) + 32
    cx = W - 24 - chip_w
    dot = MINT if p["live"] else MUTED
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
        out.append(f'<rect x="{num(x)}" y="214" width="{num(w)}" height="24" rx="12" fill="{a}" fill-opacity=".08"'
                   f' stroke="{a}" stroke-opacity=".3"/>' + mono(x + 10, 230, tag, 10.5, TEXT))
        x += w + 8
    assert x <= W - 16, f"{p['slug']}: tags overflow"
    out.append("</g>" + border)
    label = f"{p['title']} — {p['blurb']} Built with {', '.join(p['tags'])}."
    return document(W, H, "".join(out), label=label, css=RISE + CARD_CSS, defs=defs)


# ── connect buttons ────────────────────────────────────────────────────────
def button(icon: str, title: str, sub: str, a: str) -> str:
    W, H = 400, 76
    defs, back, border = frame(W, H, 16, "btn", accents=(a,), period=7)
    defs += ('<linearGradient id="sheen-grad"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
             "</linearGradient>")
    css = (".nudge{animation:nudge 2.4s ease-in-out infinite}"
           "@keyframes nudge{0%,60%,100%{transform:none}30%{transform:translate(3px,-3px)}}"
           ".sheen{animation:sheen 6s ease-in-out infinite}"
           "@keyframes sheen{0%{transform:translateX(0)}50%,100%{transform:translateX(700px)}}")
    out = (
        back + '<g clip-path="url(#btn-clip)">'
        + f'<rect class="sheen" x="-200" y="0" width="160" height="{H}" fill="url(#sheen-grad)" transform="skewX(-20)"/>'
        + f'<rect x="16" y="16" width="44" height="44" rx="12" fill="{a}" fill-opacity=".1" stroke="{a}" stroke-opacity=".45"/>'
        + f'<path transform="translate(38,38)" d="{icon_path(icon)}" fill="none" stroke="{a}" stroke-width="1.8"'
          ' stroke-linecap="round" stroke-linejoin="round"/>'
        + sans(76, 36, title, 18, TEXT, weight=700) + mono(76, 56, sub, 12, MUTED)
        + f'<g class="nudge"><path transform="translate({W - 36},38)" d="M-6,6L6,-6M-3,-6H6V3" fill="none" stroke="{a}"'
          ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>'
        + "</g>" + border
    )
    return document(W, H, out, label=f"{title}: {sub}", css=css, defs=defs)


# ── footer ─────────────────────────────────────────────────────────────────
def footer() -> str:
    W, H = 1200, 210
    defs, back, border = frame(W, H, 28, "foot", period=14)
    defs += (f'<linearGradient id="say" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/>'
             f'<stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    css = RISE + (
        ".say{animation:say 16s ease infinite both}"
        "@keyframes say{0%{opacity:0;transform:translateY(8px)}4%,21%{opacity:1;transform:none}"
        "25%,100%{opacity:0;transform:translateY(-8px)}}"
        ".wv{animation:wv linear infinite}@keyframes wv{to{transform:translateX(-300px)}}"
        ".wr{animation:wr linear infinite}@keyframes wr{from{transform:translateX(-300px)}to{transform:none}}"
    )
    waves = []
    for amp, base, color, dur, cls in ((9, 168, CYAN, 9, "wv"), (12, 176, BLUE, 13, "wr"), (8, 186, VIOLET, 17, "wv")):
        pts = [(x, base + amp * math.sin(2 * math.pi * x / 300)) for x in range(0, W + 310, 10)]
        line = path_from(pts)
        waves.append(f'<g class="{cls}" style="animation-duration:{dur}s">'
                     f'<path d="{line}L{W + 300},{H}L0,{H}Z" fill="{color}" fill-opacity=".045"/>'
                     f'<path d="{line}" fill="none" stroke="{color}" stroke-opacity=".5" stroke-width="1.4"/></g>')
    says = "".join(
        f'<text x="600" y="92" text-anchor="middle" font-family="{SANS}" font-size="30"'
        f' font-weight="600" fill="url(#say)" opacity="{1 if i == 0 else 0}" class="say"'
        f' style="animation-delay:{i * 4}s">{esc(line)}</text>'
        for i, line in enumerate(CLOSERS)
    )
    out = (back + '<g clip-path="url(#foot-clip)">' + "".join(waves) + says
           + mono(600, 132, "thanks for stopping by  ·  github.com/Deepak17kb", 13, MUTED, anchor="middle")
           + "</g>" + border)
    return document(W, H, out, label="Punjab to the world, one commit at a time.", css=css, defs=defs)


def main() -> None:
    files = {"hero.svg": hero(), "about.svg": terminal(), "footer.svg": footer()}
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
