extends Node3D
## Renders authored poses on the real protagonists: front and side, at each key time.
## Args (after --): --clip=Kneel_Surrender --times=0,0.3,0.75,1.25 --out=res://...
var args := {}

func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.trim_prefix("--").split("=", true, 1)
		args[kv[0]] = kv[1] if kv.size() > 1 else true
	var out := str(args.get("out", "res://tests/phase05/evidence/pose_preview"))
	DirAccess.make_dir_recursive_absolute(out)
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR
	env.environment.background_color = Color(0.32, 0.33, 0.35)
	env.environment.ambient_light_color = Color(0.6, 0.6, 0.62)
	env.environment.ambient_light_energy = 0.6
	add_child(env)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-40, 30, 0)
	sun.shadow_enabled = true
	add_child(sun)
	var floor := MeshInstance3D.new()
	floor.mesh = PlaneMesh.new()
	(floor.mesh as PlaneMesh).size = Vector2(8, 8)
	add_child(floor)
	var cam := Camera3D.new()
	cam.fov = 40
	add_child(cam)
	var chars := {}
	var x := -0.6
	for key in str(args.get("chars", "ADRIAN,NOAH")).split(","):
		var v: CharacterVisual = CharacterVisual.new()
		add_child(v)
		v.setup(key)
		v.position = Vector3(x, 0, 0)
		v.set_process(false)
		chars[key] = v
		x += 1.2
		if args.has("noshells"):   # debug: hide hair shells to inspect the scalp base
			for m in v.find_children("*", "MeshInstance3D", true, false):
				for i in (m as MeshInstance3D).mesh.get_surface_count():
					if (m as MeshInstance3D).get_surface_override_material(i) is ShaderMaterial:
						var hide := StandardMaterial3D.new()
						hide.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
						hide.albedo_color = Color(0, 0, 0, 0)
						(m as MeshInstance3D).set_surface_override_material(i, hide)
		if args.has("prop"):
			v.attach_to_hand(str(args["prop"]), true, v.palm_grip("R", args.has("flip")))
	var clip := str(args.get("clip", "Kneel_Surrender"))
	var times: Array = Array(str(args.get("times", "0,0.3,0.75,1.25")).split(",")).map(func(t): return float(t))
	for t in times:
		for k in chars:
			var ap: AnimationPlayer = chars[k].anim
			ap.play(clip, 0.0)
			ap.seek(t, true)
			ap.speed_scale = 0.0   # hold the sampled time while shaders compile
		var views := ["front", "side", "back3q"] if not args.has("close") else ["close_front", "close_right"]
		if args.has("cams"):   # --cams=name@px,py,pz>tx,ty,tz;name@... (relative to the first character)
			views = []
			for c in str(args["cams"]).split(";"):
				views.append(c)
		for view in views:
			var hx: float = chars.values()[0].position.x
			if "@" in view:
				var hx0: Vector3 = chars.values()[0].position
				var parts: PackedStringArray = view.split("@")[1].split(">")
				var pv: PackedFloat64Array = parts[0].split_floats(",")
				var tv: PackedFloat64Array = parts[1].split_floats(",")
				cam.fov = 30.0
				cam.look_at_from_position(hx0 + Vector3(pv[0], pv[1], pv[2]), hx0 + Vector3(tv[0], tv[1], tv[2]))
			match view:
				"close_front": cam.look_at_from_position(Vector3(hx + 0.15, 1.62, -0.75), Vector3(hx, 1.55, 0))
				"close_right": cam.look_at_from_position(Vector3(hx - 0.8, 1.62, -0.35), Vector3(hx, 1.55, 0))
				"front": cam.look_at_from_position(Vector3(0, 1.0, -4.2), Vector3(0, 0.75, 0))
				"side": cam.look_at_from_position(Vector3(4.2, 1.0, 0), Vector3(0, 0.75, 0))
				"back3q": cam.look_at_from_position(Vector3(-2.8, 1.6, 3.0), Vector3(0, 0.75, 0))
			await get_tree().process_frame
			await RenderingServer.frame_post_draw
			get_viewport().get_texture().get_image().save_png("%s/%s_t%.2f_%s.png" % [out, clip, t, view.split("@")[0]])
	get_tree().quit()
