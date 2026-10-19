"""Stage selected verified bulk assets, keeping all original sources and provenance."""
from pathlib import Path
import json, shutil, hashlib
R=Path(__file__).resolve().parents[1]
S=R/'asset_library/original_downloads/phase025_bulk_20261019'
materials=['concrete_wall_005','concrete_wall_008','concrete_block_wall_03','grey_plaster','brushed_concrete','metal_plate_02','worn_asphalt','asphalt_02']
models=['metal_office_desk','tool_cart','steel_frame_shelves_02','worn_metal_rack','metal_toolbox','caged_hanging_light','industrial_wall_lamp','hanging_industrial_lamp','utility_box_01','garden_hose_wall_mounted_01','metal_trash_can','SchoolChair_01','cardboard_box_01','medical_box']
rows=[]
for aid in materials:
    source=S/'materials'/aid;dest=R/'assets/materials/phase025'/aid;dest.mkdir(parents=True,exist_ok=True)
    maps=json.loads((source/'pbr_maps.json').read_text())
    for name in maps.values():shutil.copy2(source/name,dest/name)
    channels=[('albedo_texture','Diffuse'),('normal_texture','nor_gl'),('roughness_texture','Rough')]
    if 'AO' in maps:channels.append(('ao_texture','AO'))
    lines=['[gd_resource type="StandardMaterial3D" load_steps=%d format=3]'%(len(channels)+1),'']
    for i,(prop,key) in enumerate(channels,1):lines.append('[ext_resource type="Texture2D" path="res://assets/materials/phase025/%s/%s" id="%s"]'%(aid,maps[key],i))
    lines+=['','[resource]','resource_name = "PH025 '+aid+'"','roughness = 1.0','metallic = 0.0','normal_enabled = true','normal_scale = 0.3','texture_filter = 4']
    if 'AO' in maps:lines+=['ao_enabled = true','ao_light_affect = 0.1']
    for i,(prop,key) in enumerate(channels,1):lines.append('%s = ExtResource("%s")'%(prop,i))
    (dest/(aid+'.tres')).write_text('\n'.join(lines)+'\n')
    rows.append({'id':aid,'kind':'PBR','source_url':'https://polyhaven.com/a/'+aid,'license':'CC0-1.0','runtime':str(dest.relative_to(R)).replace('\\','/')})
for aid in models:
    source=S/'models'/aid;dest=R/'assets/props/phase025'/aid
    shutil.copytree(source,dest,dirs_exist_ok=True)
    gltf=next(dest.glob('*.gltf'))
    rows.append({'id':aid,'kind':'3D','source_url':'https://polyhaven.com/a/'+aid,'license':'CC0-1.0','runtime':str(gltf.relative_to(R)).replace('\\','/')})
out=R/'asset_library/manifests/phase025_integration';out.mkdir(parents=True,exist_ok=True)
(out/'staging.json').write_text(json.dumps(rows,indent=2))
print('Staged',len(rows),'selected assets, originals retained.')
