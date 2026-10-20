extends Node
func _ready() -> void:
 var root3 := Node3D.new()
 add_child(root3)
 var b := EnvBuilder.new(root3)
 var points := EnvWorkshop.build(b)
 var result := {"mission_points":{},"models":[],"collision_shapes":root3.find_children("*","CollisionShape3D",true,false).size()}
 for key in points:
  if points[key] is Vector3: result.mission_points[key]=var_to_str(points[key])
 for path in ["res://assets/props/phase04_architecture/industrial_dryer.glb","res://assets/props/phase04_architecture/ironing_station.glb"]:
  var inst := (load(path) as PackedScene).instantiate()
  var bounds := EnvBuilder.local_aabb(inst)
  result.models.append({"path":path,"bounds":var_to_str(bounds),"height_m":bounds.size.y,"floor_y":bounds.position.y})
  inst.free()
 var baseline_root := Node3D.new()
 add_child(baseline_root)
 var baseline_points: Dictionary = load("res://tools/phase04_architecture_baseline.gd").build(EnvBuilder.new(baseline_root))
 var baseline_shapes := baseline_root.find_children("*","CollisionShape3D",true,false)
 var changed_shapes := root3.find_children("*","CollisionShape3D",true,false)
 var collision_equal := baseline_shapes.size() == changed_shapes.size()
 for i in mini(baseline_shapes.size(), changed_shapes.size()):
  collision_equal = collision_equal and baseline_shapes[i].global_transform.is_equal_approx(changed_shapes[i].global_transform)
  collision_equal = collision_equal and str(baseline_shapes[i].shape.get_debug_mesh().get_aabb()) == str(changed_shapes[i].shape.get_debug_mesh().get_aabb())
 var points_equal := true
 for key in result.mission_points: points_equal = points_equal and points[key] == baseline_points[key]
 result["collision_comparison_pass"] = collision_equal
 result["mission_points_comparison_pass"] = points_equal
 result["baseline_collision_shapes"] = baseline_shapes.size()
 var f:= FileAccess.open("res://assets/props/phase04_architecture/validation.json",FileAccess.WRITE)
 f.store_string(JSON.stringify(result,"\t"));f.close()
 get_tree().quit()


