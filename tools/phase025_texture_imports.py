"""Enable filtered distance sampling for staged runtime PBR textures, preserving originals."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
changed = []
for folder in [ROOT / 'assets/materials/phase025', ROOT / 'assets/props/phase025']:
    for path in folder.rglob('*.import'):
        if path.name.lower().endswith(('.jpg.import', '.png.import', '.exr.import')):
            text = path.read_text()
            updated = text.replace('mipmaps/generate=false', 'mipmaps/generate=true')
            if '_nor_gl_' in path.name:
                updated = updated.replace('compress/normal_map=0', 'compress/normal_map=1')
            if updated != text:
                path.write_text(updated)
                changed.append(str(path.relative_to(ROOT)))
out = ROOT / 'tests/phase025/evidence/integration/texture_import_settings.json'
out.write_text(json.dumps({'changed': changed, 'count': len(changed)}, indent=2))
print(f'Updated {len(changed)} texture imports; Godot reimport required.')
