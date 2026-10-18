"""Read-only cross-reference audit; exits nonzero for broken local links/asset IDs."""
from pathlib import Path
import re,json,hashlib,sys
R=Path(__file__).resolve().parents[1]
files=[*R.glob('*.md'),*(R/'docs').rglob('*.md')]
manifest=json.loads((R/'asset_library/manifests/assets.json').read_text())
ids={x['asset_id'] for x in manifest};errors=[];links=0
for p in files:
    text=p.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if target.startswith(('http:','https:','mailto:','#')):continue
        dest=target.split('#')[0].replace('%20',' ')
        if not dest:continue
        links+=1
        if not (p.parent/dest).exists():errors.append(f'{p.relative_to(R)} broken link {target}')
    for aid in set(re.findall(r'\b(?:CHAR|PROP|ENV|ANIM|AUDIO|MAT|UI|VFX)_[A-Z][A-Z0-9_]*(?![A-Za-z0-9_]*\.md)',text)):  # filenames such as AUDIO_MATERIALS_AUDIT.md are not asset IDs
        # Story-only character IDs are not Chapter 1 assets.
        if aid not in ids and aid not in {'CHAR_ELENA','CHAR_VOSS','CHAR_VALE','CHAR_MERCER','CHAR_IRIS'}:errors.append(f'{p.relative_to(R)} unknown asset ID {aid}')
for a in manifest:
    if a['download_status']!='DOWNLOADED':continue
    for key in ['original_file','runtime_file']:
        paths=a[key] if isinstance(a[key],list) else [a[key]]
        for path in paths:
            if path and not (R/path).is_file():errors.append(f'{a["asset_id"]} missing {key}: {path}')
for c in json.loads((R/'asset_library/manifests/download_checks.json').read_text()):
    if hashlib.sha256((R/c['path']).read_bytes()).hexdigest()!=c['sha256']:errors.append('Checksum drift '+c['path'])
print(json.dumps(dict(documents=len(files),local_links=links,manifest_records=len(manifest),errors=errors),indent=2))
sys.exit(bool(errors))
