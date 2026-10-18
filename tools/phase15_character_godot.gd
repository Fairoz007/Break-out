extends SceneTree
# Asset inspection utility only: renders imported character GLBs in Godot at named clip poses.
# godot --path . --rendering-method gl_compatibility --script tools/phase15_character_godot.gd
const CHAR_DIRS = ["res://assets/characters/phase15/ubc/", "res://assets/characters/phase15/rocketbox/"]
const POSES = [["REST", 0.0], ["Idle_Loop", 0.5], ["Walk_Loop", 0.25], ["Walk_Loop", 0.75], ["Jog_Fwd_Loop", 0.25],
	["Sprint_Loop", 0.25], ["Crouch_Idle_Loop", 0.5], ["Crouch_Fwd_Loop", 0.25], ["Jump_Start", 0.6], ["Interact", 0.5],
	["PickUp_Table", 0.5], ["Push_Loop", 0.5], ["Fixing_Kneeling", 0.5], ["ClimbUp_1m", 0.4]]
const OUT = "res://asset_library/manifests/phase15_characters_previews/godot/"
var report = {}

func _initialize():
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	call_deferred("run")

func walk(n: Node, all: Array):
	all.append(n)
	for c in n.get_children(): walk(c, all)

func run():
	var files = []
	for d in CHAR_DIRS:
		if DirAccess.dir_exists_absolute(d):
			for f in DirAccess.get_files_at(d):
				if f.ends_with(".glb"): files.append(d + f)
	for file in files:
		var stem = file.get_base_dir().get_file() + "/" + file.get_file().get_basename()
		var r = {"file": file}
		var packed = load(r.file)
		if packed == null:
			r.load = "FAILED"; report[stem] = r; continue
		r.load = "VERIFIED"
		var view = SubViewport.new(); view.size = Vector2i(420, 640); view.own_world_3d = true
		view.render_target_update_mode = SubViewport.UPDATE_ALWAYS; root.add_child(view)
		var inst = packed.instantiate(); view.add_child(inst)
		var nodes = []; walk(inst, nodes)
		var skel: Skeleton3D = null; var player: AnimationPlayer = null; var meshes = []
		for n in nodes:
			if n is Skeleton3D: skel = n
			elif n is AnimationPlayer: player = n
			elif n is MeshInstance3D: meshes.append(n)
		r.bone_count = skel.get_bone_count() if skel else 0
		r.animations = player.get_animation_list() if player else []
		r.looping = []
		if player:
			for a in r.animations:
				if player.get_animation(a).loop_mode != Animation.LOOP_NONE: r.looping.append(a)
		var nulls = 0; var unskinned = []; var tris = 0
		for m in meshes:
			if m.skin == null or m.get_node_or_null(m.skeleton) == null: unskinned.append(str(m.name))
			for i in m.mesh.get_surface_count():
				if m.get_active_material(i) == null: nulls += 1
				var a = m.mesh.surface_get_arrays(i); tris += a[Mesh.ARRAY_INDEX].size() / 3
		r.mesh_instances = meshes.size(); r.null_materials = nulls; r.unskinned_meshes = unskinned; r.triangles = tris
		var cam = Camera3D.new(); view.add_child(cam); cam.fov = 40
		var sun = DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-40, -30, 0); sun.light_energy = 1.6; view.add_child(sun)
		var env = WorldEnvironment.new(); env.environment = Environment.new()
		env.environment.background_mode = Environment.BG_COLOR; env.environment.background_color = Color(0.3, 0.32, 0.35)
		env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.environment.ambient_light_color = Color.WHITE
		env.environment.ambient_light_energy = 0.55; view.add_child(env)
		var floor = MeshInstance3D.new(); floor.mesh = PlaneMesh.new(); floor.mesh.size = Vector2(6, 6); view.add_child(floor)
		var shots = []
		for pose in POSES:
			var clip = pose[0]; var frac = pose[1]
			if clip == "REST":
				if player: player.stop()
				skel.reset_bone_poses()
			else:
				# Godot's glTF importer strips a trailing _Loop and enables looping instead
				var name = clip if player and player.has_animation(clip) else clip.trim_suffix("_Loop")
				if not player or not player.has_animation(name):
					shots.append({"pose": clip, "status": "MISSING"}); continue
				player.play(name); player.seek(player.get_animation(name).length * frac, true); player.advance(0)
			await process_frame
			var hb = skel.find_bone("Head") if skel.find_bone("Head") >= 0 else skel.find_bone("Bip01 Head")
			var head = skel.get_bone_global_pose(hb).origin
			var fl = skel.find_bone("foot_l") if skel.find_bone("foot_l") >= 0 else skel.find_bone("Bip01 L Foot")
			var foot_l = skel.get_bone_global_pose(fl).origin
			var fr = skel.find_bone("foot_r") if skel.find_bone("foot_r") >= 0 else skel.find_bone("Bip01 R Foot")
			var foot_r = skel.get_bone_global_pose(fr).origin
			for view_name in ["front", "side"]:
				cam.position = Vector3(0, 1.0, 5.0) if view_name == "front" else Vector3(5.0, 1.0, 0)
				cam.look_at(Vector3(0, 0.92, 0))
				for i in 3: await process_frame
				await RenderingServer.frame_post_draw
				var p = OUT + "%s__%s_%02d_%s.png" % [stem.replace("/", "__"), clip, int(frac * 100), view_name]
				view.get_texture().get_image().save_png(p)
				shots.append({"pose": clip, "fraction": frac, "view": view_name, "png": p,
					"head_y": head.y, "foot_l": [foot_l.x, foot_l.y, foot_l.z], "foot_r": [foot_r.x, foot_r.y, foot_r.z]})
		r.shots = shots
		report[stem] = r
		view.queue_free(); await process_frame
	var f = FileAccess.open(OUT + "godot_character_report.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, "\t"))
	print("PHASE15_CHARACTER_GODOT_DONE")
	quit()
