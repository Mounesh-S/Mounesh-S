"""Generate a compact, repository-hosted calendar from GitHub's contribution data."""
import argparse
import json
import os
import subprocess
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
QUERY = '''query { user(login:"Mounesh-S") { contributionsCollection { contributionCalendar {
 totalContributions weeks { contributionDays { date contributionCount contributionLevel weekday } }
} } } }'''
COLORS = {'NONE': '#1C2934', 'FIRST_QUARTILE': '#254A54', 'SECOND_QUARTILE': '#397C83',
          'THIRD_QUARTILE': '#78B5AE', 'FOURTH_QUARTILE': '#D3B67C'}


def fetch():
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        request = urllib.request.Request('https://api.github.com/graphql',
            data=json.dumps({'query': QUERY}).encode(),
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    return json.loads(subprocess.run(['gh', 'api', 'graphql', '-f', f'query={QUERY}'],
        check=True, text=True, capture_output=True).stdout)


def render(data):
    if data.get('errors'):
        raise ValueError('GitHub returned a GraphQL error; previous calendar preserved')
    calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
    weeks = calendar['weeks']
    if not weeks or len(weeks) > 54:
        raise ValueError('Unexpected calendar width; previous calendar preserved')
    total = calendar['totalContributions']
    days = [day for week in weeks for day in week['contributionDays']]
    cells, months, last_month = [], [], None
    for col, week in enumerate(weeks):
        first = week['contributionDays'][0]['date']
        month = first[:7]
        if month != last_month and col < len(weeks)-2:
            months.append(f'<text x="{48+col*14}" y="65">{datetime.fromisoformat(first).strftime("%b")}</text>')
            last_month = month
        for day in week['contributionDays']:
            title = escape(f"{day['date']}: {day['contributionCount']} contributions")
            color = COLORS[day['contributionLevel']]
            cells.append(f'<rect x="{48+col*14}" y="{78+day["weekday"]*14}" width="11" height="11" rx="2" fill="{color}"><title>{title}</title></rect>')
    period = escape(f'{days[0]["date"]} — {days[-1]["date"]}')
    legend = ''.join(f'<rect x="{695+i*16}" y="190" width="11" height="11" rx="2" fill="{c}"/>' for i,c in enumerate(COLORS.values()))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="224" viewBox="0 0 860 224" role="img" aria-labelledby="title desc">
<title id="title">Mounesh S — {total:,} GitHub contributions</title><desc id="desc">Contribution calendar, {period}. Updated {datetime.now(timezone.utc).strftime('%Y-%m-%d')} UTC.</desc>
<rect x=".5" y=".5" width="859" height="223" rx="10" fill="#101923" stroke="#2B3C46"/>
<g font-family="Arial,sans-serif"><text x="28" y="34" font-size="17" fill="#D5E0E6">The voyage, one contribution at a time.</text>
<text x="832" y="34" text-anchor="end" font-size="16" fill="#D3B67C">{total:,} contributions</text>
<g fill="#A0B4BE" font-size="10">{''.join(months)}<text x="15" y="101">M</text><text x="15" y="129">W</text><text x="15" y="157">F</text></g>
{''.join(cells)}
<text x="28" y="200" font-size="11" fill="#A0B4BE">{period}</text>
<text x="658" y="200" font-size="10" fill="#A0B4BE">Less</text>{legend}<text x="786" y="200" font-size="10" fill="#A0B4BE">More</text>
</g></svg>'''
    ElementTree.fromstring(svg)
    return svg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, help='Use a previously fetched GitHub GraphQL response')
    args = parser.parse_args()
    data = json.loads(args.input.read_text()) if args.input else fetch()
    svg = render(data)
    target = ROOT / 'assets' / 'contributions.svg'
    target.write_text(svg)
    print(f'Updated {target.name} from GitHub contribution data.')
