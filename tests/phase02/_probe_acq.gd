extends SceneTree
func _initialize():
	for p in ["res://assets/props/acquisition_20261019/simple_handcuffs.glb", "res://assets/props/acquisition_20261019/industrial_dryer_ironing.glb",
			"res://assets/environments/acquisition_20261019/guard_tower.glb", "res://assets/props/acquisition_20261019/radio_yaesu_single_metric.glb",
			"res://assets/props/acquisition_20261019/signal_flashlight/signal_flashlight_2k.gltf", "res://assets/props/acquisition_20261019/signal_flashlight_2k.glb"]:
		var r = load(p)
		if r == null:
			print("PROBE ", p, " LOAD FAIL"); continue
		var n: Node3D = r.instantiate(); root.add_child(n)
		print("PROBE ", p.get_file(), " aabb=", EnvBuilder.local_aabb(n))
	var c = load("res://assets/characters/acquisition_20261019/rocketbox_facial/rb_adrian_cross.glb").instantiate()
	root.add_child(c)
	var ap: AnimationPlayer = c.find_children("*", "AnimationPlayer", true, false)[0]
	print("PROBE anims=", ap.get_animation_list().size(), " has Walk=", ap.has_animation("Walk"))
	for m in c.find_children("*", "MeshInstance3D", true, false):
		var mi: MeshInstance3D = m
		var names := []
		for i in mi.mesh.get_blend_shape_count(): names.append(mi.mesh.get_blend_shape_name(i))
		print("PROBE mesh ", mi.name, " blend=", names.size(), " ", names.filter(func(x): return "jaw" in x.to_lower() or "mouth" in x.to_lower() or "vis" in x.to_lower()).slice(0, 30))
	quit()
