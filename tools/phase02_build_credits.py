"""Build data/credits.txt (shown on the in-game Credits screen and shipped in the export) from the licence notices.
Sources: docs/assets/THIRD_PARTY_NOTICES.md and asset_library/licenses/acquisition_20261019/ATTRIBUTIONS.md.
python -I tools/phase02_build_credits.py"""
import re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
def plain(md):
    md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', md)
    md = md.replace('**', '').replace('`', '').replace('```', '')
    return '\n'.join(l.lstrip('#').strip() if l.startswith('#') else l for l in md.splitlines())
parts = ['BREAKOUT: NO WAY BACK — CREDITS AND THIRD-PARTY NOTICES', '',
         plain((R / 'docs/assets/THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')), '',
         plain((R / 'asset_library/licenses/acquisition_20261019/ATTRIBUTIONS.md').read_text(encoding='utf-8'))]
(R / 'data').mkdir(exist_ok=True)
(R / 'data/credits.txt').write_text('\n'.join(parts) + '\n', encoding='utf-8', newline='\n')
print('credits lines:', sum(1 for _ in (R / 'data/credits.txt').open(encoding='utf-8')))
