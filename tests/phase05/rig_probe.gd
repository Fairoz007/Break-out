extends SceneTree
func _initialize() -> void:
	for c in ["TwoBoneIK3D", "SkeletonIK3D", "LookAtModifier3D", "FABRIK3D", "CCDIK3D", "SplineIK3D", "SkeletonModifier3D", "LimitAngularVelocityModifier3D"]:
		print(c, " ", ClassDB.class_exists(c))
	var m: Node3D = (load("res://assets/characters/acquisition_20261019/rocketbox_facial/rb_noah_reyes.glb") as PackedScene).instantiate()
	root.add_child(m)
	var sk: Skeleton3D = m.find_children("*", "Skeleton3D", true, false)[0]
	print("bones ", sk.get_bone_count(), " skel path ", m.get_path_to(sk), " skel scale ", sk.global_transform.basis.get_scale())
	for i in sk.get_bone_count():
		var g := sk.get_bone_global_rest(i)
		print(i, " ", sk.get_bone_name(i), " parent=", sk.get_bone_parent(i), " pos=", (sk.global_transform * g).origin)
	quit()
