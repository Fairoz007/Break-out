"""Evaluation: convert Microsoft Rocketbox avatars (MIT) from FBX to rest-pose GLB.
blender -b --factory-startup --python tools/phase15_rocketbox_convert.py
Originals in asset_library/original_downloads/phase15_discovery/microsoft_rocketbox are never modified."""
import bpy, json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
SRC = R / 'asset_library/original_downloads/phase15_discovery/microsoft_rocketbox'
OUT = R / 'asset_library/converted/phase15_characters/rocketbox'; OUT.mkdir(parents=True, exist_ok=True)
AVATARS = {'male_adult_01': 'Adults/Male_Adult_01', 'security_male_01': 'Professions/Security_Male_01', 'medical_female_01': 'Professions/Medical_Female_01'}
# Optional config: {"stem": {"src": "Adults/Male_Adult_02", "overrides": {"m003_body_color.tga": "path/to/recolored.png"}}}
CFG = OUT / 'avatars.json'
OVR = {}; HEIGHT = {}
if CFG.exists():
    for k, v in json.loads(CFG.read_text()).items():
        AVATARS[k] = v['src']; OVR[k] = {n.lower(): R / p for n, p in v.get('overrides', {}).items()}; HEIGHT[k] = v.get('height')
import sys
ONLY = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
if ONLY: AVATARS = {k: v for k, v in AVATARS.items() if k in ONLY}
rep = {}
for stem, rel in AVATARS.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    d = SRC / rel; name = Path(rel).name
    bpy.ops.import_scene.fbx(filepath=str(d / 'Export' / (name + '.fbx')), use_anim=False)
    tex = {p.name.lower(): p for p in (d / 'Textures').glob('*.tga')}
    for img in bpy.data.images:
        fn = Path(bpy.path.abspath(img.filepath)).name.lower() if img.filepath else ''
        if fn in OVR.get(stem, {}): img.filepath = str(OVR[stem][fn]); img.reload()
        elif fn in tex: img.filepath = str(tex[fn]); img.reload()
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt = m.node_tree; b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not b: continue
        # Rocketbox ships specular maps; glTF needs roughness. Use a constant until a calibrated conversion exists.
        for inp in ('Specular IOR Level', 'Roughness', 'Metallic'):
            if inp in b.inputs:
                for l in list(b.inputs[inp].links): nt.links.remove(l)
        b.inputs['Roughness'].default_value = 0.62; b.inputs['Metallic'].default_value = 0.0
        if 'opacity' in m.name.lower() or any(n.type == 'TEX_IMAGE' and n.image and 'opacity' in n.image.name.lower() for n in nt.nodes):
            m.blend_method = 'HASHED' if hasattr(m, 'blend_method') else None
    rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    zs = [(o.matrix_world @ v.co).z for o in meshes for v in o.data.vertices]
    missing = sorted({img.name for img in bpy.data.images if img.source == 'FILE' and not Path(bpy.path.abspath(img.filepath)).exists()})
    if HEIGHT.get(stem):  # uniform scale to the character sheet height
        f = HEIGHT[stem] / (max(zs) - min(zs)); rig.scale = [x * f for x in rig.scale]
        bpy.context.view_layer.update(); zs = [(o.matrix_world @ v.co).z for o in meshes for v in o.data.vertices]
    out = OUT / (stem + '_rest.glb')
    bpy.ops.export_scene.gltf(filepath=str(out), export_format='GLB', export_animations=False, export_skins=True)
    rep[stem] = {'bones': len(rig.data.bones), 'bone_names': [b.name for b in rig.data.bones], 'meshes': [(o.name, len(o.data.polygons)) for o in meshes],
                 'height_m': round(max(zs) - min(zs), 3), 'rig_scale': list(rig.scale), 'missing_images': missing, 'file': str(out.relative_to(R))}
old = json.loads((OUT / 'convert_report.json').read_text()) if (OUT / 'convert_report.json').exists() else {}
old.update(rep); (OUT / 'convert_report.json').write_text(json.dumps(old, indent=1))
print('RB_DONE ' + json.dumps({k: (v['bones'], v['height_m'], v['missing_images']) for k, v in rep.items()}))
