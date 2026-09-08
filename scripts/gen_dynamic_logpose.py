"""Regenerates op_logpose.svg and op_shiplog.svg from real numbers already
computed by the Overview card (assets/metrics.svg) in the same workflow run.
No extra API calls, no extra token scope -- just re-reads what lowlighter/metrics
already fetched, so the three gauges and the Ship's Log always match Overview
exactly and refresh on the same daily/on-push schedule as everything else.

Run from the repo root: python3 scripts/gen_dynamic_logpose.py
"""
import math
import re
import pathlib
import xml.dom.minidom as minidom

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

GOLD, GOLD_SOFT = "#D4AF37", "#E8C766"
CRIMSON, AZURE = "#9E2A2B", "#38BDF8"
CANVAS2, BORDER, TEXT_HI = "#0B0F19", "#2A3447", "#F8FAFC"


def read_overview_stats():
    src = (ASSETS / "metrics.svg").read_text()
    commits = re.search(r'([\d,]+) Commits', src)
    repos = re.search(r'([\d,]+) Repositories', src)
    used = re.search(r'([\d,.]+) (MB|GB|kB) used', src)
    joined = re.search(r'Joined GitHub ([a-zA-Z0-9 ]+?) ago', src)
    return {
        "commits": int(commits.group(1).replace(",", "")) if commits else 0,
        "repos": int(repos.group(1).replace(",", "")) if repos else 0,
        "used_amount": used.group(1) if used else "0",
        "used_unit": used.group(2) if used else "MB",
        "joined": joined.group(1) if joined else "recently",
    }


def frac(value, cap, lo=0.04, hi=0.97):
    return max(lo, min(hi, value / cap))


def gen_logpose(stats):
    W, H = 860, 168
    used_mb = float(stats["used_amount"].replace(",", "")) * (1000 if stats["used_unit"] == "GB" else 1 if stats["used_unit"] == "MB" else 0.001)
    spheres = [
        ("REPOSITORIES COMMISSIONED", f'{stats["repos"]} REPOS', frac(stats["repos"], 25), CRIMSON),
        ("COMMITS LOGGED AT SEA", f'{stats["commits"]} COMMITS', frac(stats["commits"], 200), AZURE),
        ("CARGO HELD IN THE HOLD", f'{stats["used_amount"]} {stats["used_unit"]}', frac(used_mb, 1500), GOLD),
    ]
    cx_positions = [W / 2 - 260, W / 2, W / 2 + 260]
    r = 42
    defs = f'''<linearGradient id="brass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GOLD_SOFT}"/><stop offset="50%" stop-color="{GOLD}"/><stop offset="100%" stop-color="#8A6A1C"/>
    </linearGradient>
    <radialGradient id="glassSheen" cx="35%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="40%" stop-color="#DCEBFF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="{CANVAS2}" stop-opacity="0.05"/>
    </radialGradient>
    <filter id="needleGlow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="barShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
    </filter>'''
    bracket_y = H / 2 - 10
    bracket = f'<rect x="60" y="{bracket_y}" width="{W-120}" height="20" rx="10" fill="url(#brass)" stroke="#6B5218" stroke-width="1.5" filter="url(#barShadow)"/>'
    rivets = "".join(f'<circle cx="{x}" cy="{H/2}" r="3" fill="#6B5218"/>' for x in range(90, W - 80, 40))

    domes = []
    for i, (label, pull, fr, color) in enumerate(spheres):
        cx = cx_positions[i]
        cy = H / 2
        ticks = []
        for t in range(24):
            a = 2 * math.pi * t / 24
            major = (t % 6 == 0)
            r0 = r - (7 if major else 4)
            r1 = r - 1
            x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
            x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
            ticks.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{GOLD_SOFT}" stroke-width="{1.6 if major else 0.8}" opacity="{0.85 if major else 0.4}"/>')

        start_a = -math.pi / 2
        end_a = start_a + 2 * math.pi * fr
        large = 1 if (end_a - start_a) > math.pi else 0
        ax0, ay0 = cx + (r - 11) * math.cos(start_a), cy + (r - 11) * math.sin(start_a)
        ax1, ay1 = cx + (r - 11) * math.cos(end_a), cy + (r - 11) * math.sin(end_a)
        arc = f'<path d="M {ax0:.1f} {ay0:.1f} A {r-11} {r-11} 0 {large} 1 {ax1:.1f} {ay1:.1f}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" opacity="0.85"/>'

        needle_a = start_a + 2 * math.pi * fr
        nx, ny = cx + (r - 13) * math.cos(needle_a), cy + (r - 13) * math.sin(needle_a)
        tail_a = needle_a + math.pi
        tx, ty = cx + 8 * math.cos(tail_a), cy + 8 * math.sin(tail_a)
        needle = (f'<g filter="url(#needleGlow)">'
                  f'<polygon points="{nx:.1f},{ny:.1f} {cx+3*math.cos(needle_a+1.7):.1f},{cy+3*math.sin(needle_a+1.7):.1f} {tx:.1f},{ty:.1f} {cx+3*math.cos(needle_a-1.7):.1f},{cy+3*math.sin(needle_a-1.7):.1f}" fill="{color}">'
                  f'<animateTransform attributeName="transform" type="rotate" values="-4 {cx} {cy};4 {cx} {cy};-4 {cx} {cy}" dur="4s" repeatCount="indefinite"/>'
                  f'</polygon></g>')

        domes.append(f'''
        <g>
          <circle cx="{cx}" cy="{cy}" r="{r+5}" fill="url(#brass)" stroke="#6B5218" stroke-width="1.5"/>
          <circle cx="{cx}" cy="{cy}" r="{r}" fill="{CANVAS2}" stroke="{BORDER}" stroke-width="1"/>
          {"".join(ticks)}
          {arc}
          {needle}
          <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#glassSheen)"/>
          <circle cx="{cx}" cy="{cy}" r="3.5" fill="{color}"/>
          <text x="{cx}" y="{cy+r+22}" text-anchor="middle" font-family="Georgia, serif" font-size="11" font-weight="700" fill="{TEXT_HI}">{label}</text>
          <text x="{cx}" y="{cy+r+37}" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="{color}" letter-spacing="1">READING: {pull}</text>
        </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="New World Triple Log Pose HUD -- live voyage instruments">
<title>New World Triple Log Pose -- live voyage instruments</title>
<defs>{defs}</defs>
<rect width="{W}" height="{H}" fill="{CANVAS2}"/>
{bracket}{rivets}
{"".join(domes)}
</svg>'''


def gen_shiplog(stats):
    W, H = 480, 166
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Ship's log -- live voyage stats">
<title>Ship's Log -- live voyage stats</title>
<defs>
  <linearGradient id="slLine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#D4AF37" stop-opacity="0"/><stop offset="50%" stop-color="#D4AF37" stop-opacity="0.6"/><stop offset="100%" stop-color="#D4AF37" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="10" fill="#0D1117" stroke="#2A3447" stroke-width="1.2"/>
<text x="18" y="27" font-family="Georgia, serif" font-size="14" font-weight="700" fill="#D4AF37">&#128220; SHIP&#8217;S LOG</text>
<text x="{W-18}" y="27" text-anchor="end" font-family="ui-monospace, monospace" font-size="9.5" fill="#94A3B8" font-style="italic">updated daily by Actions</text>
<line x1="18" y1="36" x2="{W-18}" y2="36" stroke="url(#slLine)" stroke-width="1"/>

<g font-family="ui-monospace, monospace" font-size="11" fill="#E2E8F0">
  <text x="18" y="58"><tspan fill="#38BDF8">&#9875; </tspan>{stats["commits"]} commits logged</text>
  <text x="18" y="78"><tspan fill="#38BDF8">&#9875; </tspan>{stats["repos"]} vessels commissioned</text>
  <text x="18" y="98"><tspan fill="#38BDF8">&#9875; </tspan>{stats["used_amount"]} {stats["used_unit"]} cargo held</text>
  <text x="18" y="118"><tspan fill="#38BDF8">&#9875; </tspan>sailing these waters {stats["joined"]}</text>
</g>

<line x1="18" y1="132" x2="{W-18}" y2="132" stroke="#2A3447" stroke-width="1"/>
<text x="18" y="150" font-family="Georgia, serif" font-size="9.5" fill="#94A3B8" font-style="italic">Live numbers -- refreshed on every metrics run, same as the cards above.</text>
</svg>'''


def main():
    stats = read_overview_stats()
    print("stats:", stats)

    logpose_svg = gen_logpose(stats)
    minidom.parseString(logpose_svg)
    (ASSETS / "op_logpose.svg").write_text(logpose_svg)
    print("wrote op_logpose.svg,", len(logpose_svg), "bytes")

    shiplog_svg = gen_shiplog(stats)
    minidom.parseString(shiplog_svg)
    (ASSETS / "op_shiplog.svg").write_text(shiplog_svg)
    print("wrote op_shiplog.svg,", len(shiplog_svg), "bytes")


if __name__ == "__main__":
    main()
