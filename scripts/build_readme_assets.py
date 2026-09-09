"""Build the README's self-contained, script-free SVG animations."""
from pathlib import Path
from html import escape
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'


def save(name, width, height, title, body, css=''):
    source = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>{css}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}</style>
{body}
</svg>'''
    ElementTree.fromstring(source)
    (ASSETS / name).write_text(source)

save('grand-line.svg', 860, 116, 'Sailing the Grand Line — a gently moving ship and ocean current', '''
<defs><linearGradient id="sea" x2="1" y2="0"><stop stop-color="#0D1117"/><stop offset=".5" stop-color="#122B36"/><stop offset="1" stop-color="#0D1117"/></linearGradient></defs>
<rect width="860" height="116" rx="8" fill="url(#sea)"/>
<g fill="none" stroke="#45616C" opacity=".45"><path d="M0 77Q54 65 108 77T324 77T540 77T756 77T972 77"/><path d="M-108 93Q-54 81 0 93T216 93T432 93T648 93T864 93" class="waves"/></g>
<path d="M50 54H350M510 54H810" fill="none" stroke="#668286" stroke-width="1" stroke-dasharray="3 10" class="route"/>
<g fill="#C5A572"><circle cx="50" cy="54" r="3"/><circle cx="810" cy="54" r="3"/></g>
<g class="ship"><path d="M392 70H468L457 85H407Z" fill="#704F37" stroke="#C5A572"/><path d="M431 16V71" stroke="#C5A572" stroke-width="2"/><path d="M426 23Q398 29 401 60H426Z" fill="#D9D4C2"/><path d="M437 23Q463 36 464 60H437Z" fill="#B9C6C5"/><path d="M431 16V8L449 12 431 16" fill="#9E4147"/><path d="M392 70H468M409 77H453" stroke="#C5A572"/>
<g fill="#1B2931"><ellipse cx="414" cy="41" rx="5" ry="6"/><path d="M405 38H423V40H405Z"/><path d="M409 36Q414 30 419 36Z"/></g></g>
<g fill="#80A3AC"><circle cx="293" cy="24" r="1.5"/><circle cx="567" cy="22" r="1.5"/><path d="M619 30v8m-4-4h8M218 29v6m-3-3h6" stroke="#80A3AC" stroke-width="1"/></g>
''', '''.ship {transform-origin:430px 80px;animation:sail 5s ease-in-out infinite}
.waves{animation:wave 12s linear infinite}.route{animation:current 8s linear infinite}
@keyframes sail{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-4px) rotate(2deg)}}
@keyframes wave{to{transform:translateX(108px)}}@keyframes current{to{stroke-dashoffset:-104}}''')

save('haki.svg', 860, 72, 'Observation: AI. Armament: systems. Conqueror: ownership.', '''
<rect width="860" height="72" rx="8" fill="#111B24"/>
<g font-family="Arial, sans-serif" font-size="15" fill="#CDD9E5" text-anchor="middle">
<text x="145" y="29" fill="#BDA275" font-size="11" letter-spacing="2">OBSERVATION</text><text x="145" y="52">AI &amp; agent systems</text>
<text x="430" y="29" fill="#7DB5BB" font-size="11" letter-spacing="2">ARMAMENT</text><text x="430" y="52">Reliable data pipelines</text>
<text x="715" y="29" fill="#D49B9C" font-size="11" letter-spacing="2">CONQUEROR</text><text x="715" y="52">End-to-end ownership</text></g>
<path d="M287 19V53M574 19V53" stroke="#2C3B45"/>
<path d="M32 71H828" stroke="#2C3B45"/><path d="M32 71H828" stroke="#BDA275" stroke-dasharray="65 731" class="signal"/>
''', '.signal{animation:signal 14s linear infinite}@keyframes signal{to{stroke-dashoffset:-796}}')

for name, label, accent, icon in [
    ('contact-email.svg','LET’S BUILD','#C5A572','<rect x="15" y="12" width="17" height="12" rx="2"/><path d="m15 13 8.5 6 8.5-6"/>'),
    ('contact-linkedin.svg','LINKEDIN','#8CBAC8','<path d="M17 16v9m0-14v1m6 13v-9m0 4c0-6 8-6 8 0v5"/>'),
    ('contact-logbook.svg','SIGN THE LOGBOOK','#D49B9C','<path d="M16 11h16v12H22l-6 5Z"/>')
]:
    width = 190 if name=='contact-logbook.svg' else 145
    save(name, width, 38, label, f'''<rect x=".5" y=".5" width="{width-1}" height="37" rx="6" fill="#161F29" stroke="#34434D"/><g fill="none" stroke="{accent}" stroke-width="1.5">{icon}</g><text x="44" y="23" fill="{accent}" font-family="Arial,sans-serif" font-size="11" font-weight="bold" letter-spacing="1">{label}</text>''')
print('Built five local README SVGs, including two reduced-motion-aware animations.')

# A picture source lets the parent page select a still image even when the
# browser does not propagate a changed motion preference into an SVG image.
import re
for name in ('grand-line', 'haki'):
    source = (ASSETS / f'{name}.svg').read_text()
    still = re.sub(r'<style>.*?</style>', '', source, flags=re.S)
    ElementTree.fromstring(still)
    (ASSETS / f'{name}-still.svg').write_text(still)
print('Built two explicit still-image alternatives for reduced-motion picture sources.')
