"""Draw the live GitHub cards (activity and languages) for the profile README.

    GITHUB_TOKEN=... python scripts/build_stats.py --user Deepak17kb --out dist

The profile workflow runs this on a schedule and publishes the cards to the
`output` branch, next to the contribution snake. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from theme import (
    CLAY, LILAC, LINE, MUTED, ROSE, SAGE, SAND, SANS, SLATE, STONE, SUB, TEXT,
    document, esc, frame, mono, num, sans,
)

API = "https://api.github.com/graphql"
# Notebook JSON (outputs, embedded images) dwarfs the code around it.
EXCLUDED_LANGUAGES = {"Jupyter Notebook"}
LANGUAGE_COLORS = (SAND, SLATE, SAGE, CLAY, LILAC, ROSE, STONE, MUTED)
MIN_SHARE = 0.01

PROFILE = """
query($login: String!) {
  user(login: $login) {
    createdAt
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 20, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}"""

CALENDAR = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}"""

CSS = (
    ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
    "@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
    ".grow{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.1s cubic-bezier(.3,.7,.2,1) both}"
    "@keyframes grow{from{transform:scaleY(0)}}"
    ".growx{transform-box:fill-box;transform-origin:0 50%;animation:growx 1.3s cubic-bezier(.3,.7,.2,1) both}"
    "@keyframes growx{from{transform:scaleX(0)}}"
)


def graphql(query: str, token: str, **variables) -> dict:
    request = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-readme-stats"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload["data"]["user"]


def iso(moment: datetime) -> str:
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def calendar(login: str, token: str, start: datetime, end: datetime) -> dict:
    return graphql(CALENDAR, token, login=login, **{"from": iso(start), "to": iso(end)})["contributionsCollection"]


def collect(login: str, token: str) -> dict:
    profile = graphql(PROFILE, token, login=login)
    now = datetime.now(timezone.utc)
    joined = datetime.fromisoformat(profile["createdAt"].replace("Z", "+00:00"))

    # The API serves at most a year per request, so walk the account's history.
    days: dict[str, int] = {}
    start = joined
    while start < now:
        end = min(start + timedelta(days=365), now)
        for week in calendar(login, token, start, end)["contributionCalendar"]["weeks"]:
            for day in week["contributionDays"]:
                days[day["date"]] = day["contributionCount"]
        start = end

    year = calendar(login, token, now - timedelta(days=365), now)
    year_weeks = year["contributionCalendar"]["weeks"]
    weekly = [sum(d["contributionCount"] for d in week["contributionDays"]) for week in year_weeks][-26:]
    active = sum(1 for week in year_weeks for d in week["contributionDays"] if d["contributionCount"])

    sizes: Counter[str] = Counter()
    for repo in profile["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            if edge["node"]["name"] not in EXCLUDED_LANGUAGES:
                sizes[edge["node"]["name"]] += edge["size"]

    longest = longest_streak(days)
    return {
        "joined": joined.date(),
        "updated": now.date(),
        "total": sum(days.values()),
        "commits": year["totalCommitContributions"],
        "active": active,
        "stars": sum(r["stargazerCount"] for r in profile["repositories"]["nodes"]),
        "repos": profile["repositories"]["totalCount"],
        "longest": longest,
        "weekly": weekly,
        "languages": sizes,
    }


def longest_streak(days: dict[str, int]) -> int:
    """Longest run of consecutive days with at least one contribution."""
    longest = run = 0
    for _, count in sorted(days.items()):
        run = run + 1 if count else 0
        longest = max(longest, run)
    return longest


def odometer(x: float, baseline: float, value: int, size: float, uid: str) -> str:
    """A number whose digits spin into place, each column a little later than the last."""
    text = f"{value:,}"
    cw, lh = size * 0.6, size * 1.25
    out, col_x = [], x
    for i, ch in enumerate(text):
        if not ch.isdigit():
            out.append(f'<text x="{num(col_x + cw * 0.25)}" y="{num(baseline)}" font-family="{SANS}" font-size="{num(size)}"'
                       f' font-weight="600" fill="{TEXT}" text-anchor="middle">{esc(ch)}</text>')
            col_x += cw * 0.5
            continue
        shift = -(10 + int(ch)) * lh
        strip = "".join(
            f'<text x="{num(col_x + cw / 2)}" y="{num(baseline + k * lh)}" text-anchor="middle">{k % 10}</text>'
            for k in range(20)
        )
        delay = 0.25 + i * 0.12
        out.append(
            f'<clipPath id="{uid}-{i}"><rect x="{num(col_x)}" y="{num(baseline - size)}" width="{num(cw)}"'
            f' height="{num(size * 1.2)}"/></clipPath>'
            f'<g clip-path="url(#{uid}-{i})"><g transform="translate(0 {num(shift)})" font-family="{SANS}"'
            f' font-size="{num(size)}" font-weight="600" fill="{TEXT}">{strip}'
            f'<animateTransform attributeName="transform" type="translate" dur="{num(delay + 1.6)}s"'
            f' values="0 0;0 0;0 {num(shift)}" keyTimes="0;{delay / (delay + 1.6):.4f};1" calcMode="spline"'
            f' keySplines="0 0 1 1;.2 .75 .15 1" fill="freeze"/></g></g>'
        )
        col_x += cw
    return "".join(out)


def activity_card(s: dict, login: str) -> str:
    W, H = 480, 280
    defs, back, border = frame(W, H, 18, "act")
    defs += (f'<linearGradient id="spark" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{SAND}"'
             f' stop-opacity=".45"/><stop offset="1" stop-color="{SAND}"/></linearGradient>')
    out = [back, '<g clip-path="url(#act-clip)">',
           mono(24, 36, f"GITHUB · @{login.upper()}", 11, SAND),
           mono(W - 24, 36, f"updated {s['updated']:%d %b %Y}", 10, MUTED, anchor="end"),
           odometer(24, 98, s["total"], 46, "odo"),
           mono(24, 122, f"contributions since {s['joined']:%b %Y}", 10.5, SUB)]

    # Last 26 weeks as bars.
    peak = max(s["weekly"] or [1]) or 1
    left, width, top, bottom = 252, W - 24 - 252, 58, 112
    step = width / max(len(s["weekly"]), 1)
    for i, count in enumerate(s["weekly"]):
        h = max(2.0, (bottom - top) * count / peak)
        out.append(f'<rect x="{num(left + i * step)}" y="{num(bottom - h)}" width="{num(step * 0.62)}" height="{num(h)}"'
                   f' rx="1.5" fill="{LINE if count == 0 else 'url(#spark)'}" class="grow"'
                   f' style="animation-delay:{num(0.3 + i * 0.03)}s"/>')
    out.append(mono(W - 24, 126, "last 26 weeks", 9, MUTED, anchor="end"))
    out.append(f'<path d="M24,146H{W - 24}" stroke="{LINE}"/>')

    metrics = [
        (s["commits"], "commits", "12 mo", SAND),
        (s["active"], "active days", "12 mo", SAGE),
        (s["longest"], "longest streak", "days", SLATE),
        (s["repos"], "repositories", "public", CLAY),
        (len(s["languages"]), "languages", "in use", LILAC),
        (s["stars"], "stars", "earned", ROSE),
    ]
    for i, (value, label, note, color) in enumerate(metrics):
        x, y = 24 + (i % 3) * 148, 186 + (i // 3) * 58
        out.append(
            f'<g class="rise" style="animation-delay:{num(0.5 + i * 0.1)}s">'
            f'<rect x="{x}" y="{y - 22}" width="3" height="38" rx="1.5" fill="{color}"/>'
            + sans(x + 14, y, f"{value:,}", 24, TEXT, weight=600)
            + mono(x + 14, y + 16, f"{label} · {note}", 9.5, MUTED) + "</g>"
        )
    out.append("</g>" + border)
    label = (f"GitHub activity for @{login}: {s['total']:,} contributions since {s['joined']:%B %Y}; "
             f"{s['commits']:,} commits and {s['active']} active days in the past year; longest streak "
             f"{s['longest']} days; {s['repos']} public repositories; {len(s['languages'])} languages; "
             f"{s['stars']:,} stars.")
    return document(W, H, "".join(out), label=label, css=CSS, defs=defs)


def languages_card(s: dict) -> str:
    W, H = 480, 280
    defs, back, border = frame(W, H, 18, "lang")
    ranked = s["languages"].most_common()
    total = sum(size for _, size in ranked) or 1
    # Languages under 1% are noise at this size; they fold into "Other" when that adds up to something.
    shown = [(name, size) for name, size in ranked if size / total >= MIN_SHARE][:7]
    rest = total - sum(size for _, size in shown)
    if rest / total >= MIN_SHARE:
        shown.append(("Other", rest))
    shares = [(name, size / total, LANGUAGE_COLORS[i]) for i, (name, size) in enumerate(shown)]

    bar_w = W - 48
    defs += (f'<clipPath id="stack"><rect x="24" y="56" width="{bar_w}" height="12" rx="6">'
             f'<animate attributeName="width" values="0;{bar_w}" dur="1.4s" calcMode="spline"'
             ' keySplines=".3 .7 .2 1" fill="freeze"/></rect></clipPath>')
    out = [back, '<g clip-path="url(#lang-clip)">',
           mono(24, 36, "LANGUAGES · BY BYTES", 11, SAND),
           mono(W - 24, 36, "public repos · excl. notebooks", 10, MUTED, anchor="end"),
           f'<rect x="24" y="56" width="{bar_w}" height="12" rx="6" fill="{LINE}"/>',
           '<g clip-path="url(#stack)">']
    x = 24.0
    for name, share, color in shares:
        out.append(f'<rect x="{num(x)}" y="56" width="{num(bar_w * share + 0.5)}" height="12" fill="{color}"/>')
        x += bar_w * share
    out.append("</g>")

    top = max((share for _, share, _ in shares), default=1)
    rows = (len(shares) + 1) // 2
    gap = min(56, 132 / max(rows - 1, 1))
    for i, (name, share, color) in enumerate(shares):
        x, y = 24 + (i % 2) * 224, 108 + (i // 2) * gap
        track = 190
        out.append(
            f'<g class="rise" style="animation-delay:{num(0.4 + i * 0.08)}s">'
            f'<circle cx="{x + 5}" cy="{y - 5}" r="5" fill="{color}"/>'
            + sans(x + 18, y, name, 14, TEXT, weight=600)
            + mono(x + 18 + track, y, f"{share * 100:.1f}%", 11.5, SUB, anchor="end")
            + f'<rect x="{x + 18}" y="{y + 9}" width="{track}" height="4" rx="2" fill="{LINE}"/>'
            f'<rect x="{x + 18}" y="{y + 9}" width="{num(max(track * share / top, 4))}" height="4" rx="2" fill="{color}"'
            f' class="growx" style="animation-delay:{num(0.6 + i * 0.08)}s"/></g>'
        )
    out.append("</g>" + border)
    label = "Languages by bytes across public repositories: " + ", ".join(
        f"{name} {share * 100:.1f}%" for name, share, _ in shares)
    return document(W, H, "".join(out), label=label, css=CSS, defs=defs)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--user", default=os.environ.get("GITHUB_REPOSITORY_OWNER", "Deepak17kb"))
    parser.add_argument("--out", default="dist", type=Path)
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("Set GITHUB_TOKEN (the workflow token is enough).")

    stats = collect(args.user, token)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "activity.svg").write_text(activity_card(stats, args.user), encoding="utf-8", newline="\n")
    (args.out / "languages.svg").write_text(languages_card(stats), encoding="utf-8", newline="\n")
    summary = {k: v for k, v in stats.items() if k not in ("languages", "weekly")}
    print(json.dumps(summary, default=str, indent=2))


if __name__ == "__main__":
    main()
