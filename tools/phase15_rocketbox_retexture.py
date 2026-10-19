"""Swap one embedded image in a built Rocketbox GLB for a regenerated recolour PNG, without re-running convert/animate.
Geometry, skin and the 37 clips are untouched; only the named image's bufferView bytes change (later views are shifted).
python -I tools/phase15_rocketbox_retexture.py <glb> <image_name> <png> [<glb> ...more copies to write]"""
import hashlib, json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / 'tools'))
from phase15_gltf_util import read_glb, write_glb

src, name, png = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
js, bin_ = read_glb(src)
img = next(i for i in js['images'] if i.get('name') == name)
bv = js['bufferViews'][img['bufferView']]; start, old_len = bv.get('byteOffset', 0), bv['byteLength']
old_sha = hashlib.sha256(bin_[start:start + old_len]).hexdigest()
data = png.read_bytes(); pad = (4 - len(data) % 4) % 4; new = data + b'\0' * pad
old_span = old_len + (4 - old_len % 4) % 4
bin_ = bin_[:start] + new + bin_[start + old_span:]
delta = len(new) - old_span
for v in js['bufferViews']:
    if v is not bv and v.get('byteOffset', 0) > start: v['byteOffset'] = v.get('byteOffset', 0) + delta
bv['byteLength'] = len(data); js['buffers'][0]['byteLength'] = len(bin_)
for out in [src] + [Path(p) for p in sys.argv[4:]]:
    write_glb(out, js, bin_)
print(json.dumps({'image': name, 'old_png_sha256': old_sha, 'new_png_sha256': hashlib.sha256(data).hexdigest(),
                  'glb_sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'written': [str(src)] + sys.argv[4:]}))
