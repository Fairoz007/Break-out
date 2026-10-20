extends SceneTree
func _initialize() -> void:
	var m: Node3D = (load("res://assets/characters/acquisition_20261019/rocketbox_facial/rb_noah_reyes.glb") as PackedScene).instantiate()
	root.add_child(m)
	var ap: AnimationPlayer = m.find_children("*", "AnimationPlayer", true, false)[0]
	print("ap path ", m.get_path_to(ap), " root_node ", ap.root_node, " libs ", ap.get_animation_library_list())
	var a := ap.get_animation("Idle")
	print("Idle len ", a.length, " loop ", a.loop_mode, " tracks ", a.get_track_count())
	for t in min(6, a.get_track_count()):
		print(a.track_get_path(t), " type ", a.track_get_type(t))
	var b := m.get_node("Bip01") if m.has_node("Bip01") else null
	print("Bip01 node ", b, " xf ", (b as Node3D).transform if b else "")
	for n in m.find_children("*", "Node3D", true, false):
		if n is Node3D and n.get_parent() == m or n.name == "Bip01":
			print(" child ", m.get_path_to(n), " ", (n as Node3D).transform)
	var fk := ap.get_animation("Fixing_Kneeling")
	print("Fixing_Kneeling len ", fk.length, " loop ", fk.loop_mode)
	quit()
