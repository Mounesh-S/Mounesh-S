"""Generate the profile's code-native SVG illustrations. No external services."""
from pathlib import Path
from html import escape
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
TEAL, GOLD, BG = '#85b6b3', '#c4aa79', '#0e1921'

def svg(name, content, width=420, height=180, title='Engineering vessel illustration'):
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><style>@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}} .current{{stroke-dasharray:4 9;animation:flow 30s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-260}}}}</style>
<defs><pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25 0H0v25" fill="none" stroke="{TEAL}" stroke-opacity=".06"/></pattern><radialGradient id="glow"><stop stop-color="{TEAL}" stop-opacity=".1"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient></defs>
{content}</svg>'''
    ET.fromstring(document)
    (A/name).write_text(document)

def scene(content):
    return f'<rect width="420" height="180" fill="url(#grid)"/><ellipse cx="210" cy="98" rx="190" ry="87" fill="url(#glow)"/><g fill="none" stroke="{TEAL}" stroke-width="1.1" stroke-linejoin="round">{content}</g>'

waves = ''.join(f'<path d="M{x} {y}q18-7 36 0t36 0" opacity=".25"/>' for x,y in [(38,149),(105,162),(246,151),(313,138),(276,172),(13,126)])
ship = f'''<path d="M100 119q110 20 218-7l-21 33q-97 20-165-1z" fill="{BG}"/><path d="M116 129q88 19 188-6M156 119V51m-7 0h19M216 123V21m-7 0h18m43 94V62m-8 0h17"/><path d="M211 31q-55 14-41 71l41 6zM222 35q58 21 47 70l-47 3zM151 59q-39 13-26 45h26zM276 69q33 7 22 34h-22z" fill="{BG}"/><path d="M220 23q19-12 39-1v13q-19-11-39-1M142 141h128" stroke="{GOLD}"/><circle cx="309" cy="119" r="10" stroke="{GOLD}"/><circle cx="309" cy="119" r="4"/><path d="M194 54v33m-10-18h20" opacity=".45"/>'''
svg('vessel-routing.svg',scene(ship+waves))
svg('vessel-pulse.svg',scene('''<path d="M75 89h60m150 0h59M210 35v20m0 73v31" class="current"/><circle cx="210" cy="90" r="36"/><circle cx="210" cy="90" r="27" opacity=".4"/><path d="m185 92 11-2 8-16 10 32 9-18h13" stroke="#c4aa79"/><rect x="29" y="54" width="55" height="70" rx="4"/><path d="M40 67h31m-31 12h21m-21 12h29m-29 12h17" opacity=".5"/><rect x="337" y="54" width="55" height="70" rx="4"/><path d="m349 81 10-9 18 18m-28 9h29m-29 11h19" opacity=".5"/><path d="m134 33 24 18m111 78 21 17m-154 0 22-18m111-76 22-18" opacity=".4"/><circle cx="210" cy="20" r="6"/><circle cx="210" cy="166" r="6"/>'''))
svg('vessel-onboarding.svg',scene('''<path d="M56 133q148 36 306 0M67 142q145 30 284 0" opacity=".4"/><path d="M162 136V58q48-74 96 0v78M177 136V62q32-51 64 0v74"/><path d="m143 140 66 15 68-15-67-16z"/><path d="M210 51v73m-22-53 44 23m-44 0 44-23" opacity=".3"/><path d="M55 89h76m157 0h76" class="current"/><rect x="38" y="71" width="32" height="35" rx="3"/><path d="m49 82 10 0m-10 8h10m-10 8h6"/><path d="m339 84 11 10 17-22" stroke="#c4aa79"/><path d="M109 129V97m0 3q-20-21-26-4m26 4q20-19 26-1M304 133V103m0 3q-16-18-22-3m22 3q15-18 25-2"/>'''))
svg('vessel-streaming.svg',scene('''<path d="M28 60q80-42 158 0t193 0M28 86q80-42 158 0t193 0M28 112q80-42 158 0t193 0M28 138q80-42 158 0t193 0" opacity=".3"/><path d="M41 85q99-41 164 0t170 0" class="current" stroke="#c4aa79"/><g fill="#0e1921"><ellipse cx="210" cy="61" rx="39" ry="15"/><path d="M171 61v62c0 20 78 20 78 0V61"/><path d="M171 91c0 20 78 20 78 0M171 112c0 20 78 20 78 0"/></g><circle cx="74" cy="80" r="6" fill="#0e1921"/><circle cx="343" cy="90" r="6" fill="#0e1921"/><path d="M89 37h34m-22 6h33M292 145h34m-25 7h39" opacity=".5"/>'''))
svg('vessel-billing.svg',scene('''<path d="m112 132 92-29 101 30-93 31z" opacity=".4"/><path d="M128 122V67l79-36 81 36v59M115 70l92-43 95 43z"/><path d="M149 83v42m27-54v63m30-70v77m29-71v65m28-52v44M129 123l79 24 80-24"/><path d="M42 105h57m219 0h60" class="current"/><circle cx="64" cy="65" r="17" stroke="#c4aa79"/><path d="M64 53v24m5-18H60v6h9v6h-9" stroke="#c4aa79"/><rect x="322" y="40" width="36" height="44" rx="3"/><path d="M330 50h19m-19 9h19m-19 9h10" opacity=".7"/>'''))
svg('vessel-anomaly.svg',scene('''<path d="m210 25 53 19v42q-4 45-53 65c-49-20-49-54-53-65V44z"/><path d="m210 35 43 16v35q-5 36-43 55c-38-19-39-45-43-55V51z" opacity=".3"/><path d="M48 89h85l9-10 10 19 10-42 14 57 12-24h47l12-11 10 11h113" stroke="#c4aa79"/><path d="M51 114h13m6 0h13m6 0h13m6 0h13m179 0h13m6 0h13m6 0h13m6 0h13M57 125h13m6 0h13m6 0h13m199 0h13m6 0h13m6 0h13" opacity=".4"/>'''))

for key, colors in {'midnight':('#080f16','#c4aa79','#85b6b3'), 'dawn':('#f0ebdf','#7b522b','#367670'), 'wano':('#120f19','#dba5aa','#b0a2d4')}.items():
    bg,accent,teal=colors
    svg(f'voyage-{key}.svg',f'''<rect width="860" height="180" rx="5" fill="{bg}"/><g fill="none" stroke="{teal}"><path d="M100 98C235 15 318 147 420 94S606 36 760 95" class="current"/>{''.join(f'<circle cx="{x}" cy="95" r="7" fill="{bg}" stroke="{accent}"/><path d="M{x} 77v-8m-8 26h-8m32 0h-8"/>' for x in [110,430,750])}</g><g font-family="Georgia,serif" text-anchor="middle" fill="{accent}" font-size="20"><text x="110" y="51">East Blue</text><text x="430" y="51">Water 7</text><text x="750" y="51">The New World</text></g><g font-family="Arial,sans-serif" text-anchor="middle" fill="{teal}" font-size="11"><text x="110" y="134">2022–2026 · B.Tech AI &amp; DS</text><text x="430" y="134">2025–2026 · Engineering Intern</text><text x="750" y="134">Jul 2026–Present · Engineer</text></g>''',860,180,'Career voyage: education, internship, software engineer at CasaRetail AI')
    svg(f'banner-{key}.svg',f'''<rect width="860" height="140" rx="5" fill="{bg}"/><g stroke="{teal}" fill="none" opacity=".4"><path d="M0 119q107-20 215 0t215 0 215 0 215 0" class="current"/><path d="M0 129q107-20 215 0t215 0 215 0 215 0"/></g><text x="430" y="53" text-anchor="middle" font-family="Georgia,serif" font-size="29" fill="{accent}">A builder’s mind. A pirate’s freedom.</text><text x="430" y="85" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" letter-spacing="3" fill="{teal}">THE EMPEROR’S LOG · ONE PIECE / NEW WORLD</text>''',860,140,'A builder’s mind. A pirate’s freedom. The Emperor’s Log.')

svg('flag.svg','<rect width="40" height="40" rx="8" fill="#080f16"/><g fill="none" stroke="#c4aa79" stroke-width="1.5"><path d="M8 35V5c8-7 16 7 26 0v20c-10 7-18-7-26 0"/><circle cx="21" cy="13" r="4"/><path d="m15 19 12 5m0-5-12 5M19 16v3h4v-3"/></g>',40,40,'Mounesh pirate flag')
print('Generated 13 validated SVG assets.')
