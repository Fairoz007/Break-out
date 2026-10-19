"""Stage only the new CC0 resources in a small isolated Godot project."""
from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[1]
P=R/'asset_library/converted/acquisition_20261019/material_validation';P.mkdir(parents=True,exist_ok=True)
for cat in ['materials','props']:
 src=R/'assets'/cat/'acquisition_20261019'
 dst=P/'assets'/cat/'acquisition_20261019'
 shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.import','*.blend','*.mtlx','Fabric030_2K-JPG.tres'))
(P/'project.godot').write_text('config_version=5\n[application]\nconfig/name="Acquisition material validation"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n[filesystem]\nimport/blender/enabled=false\n')
paths=[p.relative_to(P).as_posix() for p in P.rglob('*.tres') if p.name!='Fabric030_2K-JPG.tres']
paths+=['assets/props/acquisition_20261019/signal_flashlight_2k.glb']
radio=R/'asset_library/converted/acquisition_20261019/radio_yaesu/radio_yaesu_single_metric.glb'
if radio.exists():
 dst=P/'assets/props/acquisition_20261019/radio_yaesu_single_metric.glb'
 shutil.copyfile(radio,dst)
 paths.append(dst.relative_to(P).as_posix())
(P/'validate.gd').write_text('''extends SceneTree
func inspect_node(n:Node, row:Dictionary):
 if n is MeshInstance3D:
  row["mesh_instances"] += 1
  if n.mesh:
   for s in n.mesh.get_surface_count():
    if n.get_active_material(s) == null: row["null_materials"] += 1
 for c in n.get_children(): inspect_node(c,row)
func _initialize():
 var paths = PATHS
 var rows = []
 var failed = false
 for path in paths:
  var resource = load("res://" + path)
  var row = {"path":path,"loaded":resource != null}
  if resource is StandardMaterial3D:
   var m = resource as StandardMaterial3D
   row["albedo"] = m.albedo_texture != null
   row["normal"] = m.normal_texture != null
   row["roughness"] = m.roughness_texture != null
   row["ao"] = m.ao_texture != null
   row["metallic"] = m.metallic_texture != null
   if m.albedo_texture: row["albedo_size"] = str(m.albedo_texture.get_size())
   if m.normal_texture: row["normal_size"] = str(m.normal_texture.get_size())
   if not row.albedo or not row.normal or not row.roughness: failed = true
  elif resource is PackedScene:
   var n = resource.instantiate()
   row["instantiated"] = n != null
   row["mesh_instances"] = 0
   row["null_materials"] = 0
   if n:
    inspect_node(n,row)
    n.free()
   if row["null_materials"] > 0: failed = true
  if resource == null: failed = true
  rows.append(row)
 var out = FileAccess.open("res://godot_report.json",FileAccess.WRITE)
 out.store_string(JSON.stringify({"engine":Engine.get_version_info(),"scope":"Resource loading and bound PBR references; rendered scene NOT TESTED", "resources":rows,"failed":failed},"  "))
 out.close()
 quit(1 if failed else 0)
'''.replace('PATHS',json.dumps(paths)))
print(str(P))
