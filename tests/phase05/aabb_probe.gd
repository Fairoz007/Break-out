extends SceneTree
func _initialize() -> void:
	for path in OS.get_cmdline_user_args():
		var n: Node3D = (load(path) as PackedScene).instantiate()
		root.add_child(n)
		var box := AABB()
		var first := true
		for m in n.find_children("*", "MeshInstance3D", true, false):
			var bb: AABB = (m as MeshInstance3D).global_transform * (m as MeshInstance3D).get_aabb()
			box = bb if first else box.merge(bb)
			first = false
		print(path, " aabb pos=", box.position, " size=", box.size)
	quit()
