"""Compare Quaternius Universal Base Character skeleton with UAL animation skeleton (read-only probe)."""
import bpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
UBC=R/'asset_library/extracted_sources/phase15_characters/universal-base-characters/Universal Base Characters[Standard]/Base Characters/Godot - UE/Superhero_Male_FullBody.gltf'
UAL=R/'assets/animations/phase15/UAL1_Standard.glb'
bpy.ops.wm.read_factory_settings(use_empty=True)
def imp(p):
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(p));return [o for o in bpy.data.objects if o not in before]
a=imp(UBC);b=imp(UAL)
ra=[o for o in a if o.type=='ARMATURE'][0];rb=[o for o in b if o.type=='ARMATURE'][0]
out={'ubc_objects':[(o.name,o.type) for o in a],'ual_objects':[(o.name,o.type) for o in b],'ubc_bones':len(ra.data.bones),'ual_bones':len(rb.data.bones)}
na={x.name for x in ra.data.bones};nb={x.name for x in rb.data.bones}
out['only_ubc']=sorted(na-nb);out['only_ual']=sorted(nb-na)
diffs=[]
for n in sorted(na&nb):
    ma=ra.matrix_world@ra.data.bones[n].matrix_local;mb=rb.matrix_world@rb.data.bones[n].matrix_local
    d=max(abs(ma[i][j]-mb[i][j]) for i in range(4) for j in range(4))
    diffs.append((n,round(d,4)))
out['max_rest_diff']=max(d for _,d in diffs);out['worst']=sorted(diffs,key=lambda x:-x[1])[:10]
out['ual_actions']=sorted(x.name for x in bpy.data.actions)
for o in a:
    if o.type=='MESH':out.setdefault('ubc_meshes',[]).append({'name':o.name,'verts':len(o.data.vertices),'groups':len(o.vertex_groups),'mats':[m.name for m in o.data.materials],'dims':[round(v,3) for v in o.dimensions]})
print('PROBE_JSON'+json.dumps(out))
