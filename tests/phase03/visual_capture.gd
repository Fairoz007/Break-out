extends Node
## Phase 03 deterministic environment captures. The first ten cameras match tests/phase025/visual_capture.gd
## exactly (before/after comparison); the rest are Phase 03 close-ups of rebuilt assets.
## Usage: godot --path . res://tests/phase03/visual_capture.tscn -- --output=<dir> [--only=a,b] [--quality=0..2]
## Captures only. No playability, animation or mission claims are made from these images.

var output := "res://docs/phase03/visual_evidence/after"
var only: PackedStringArray = []
var settle_frames := 90
var samples := [
	["bus", "intake", Vector3(-3, 2, 1), Vector3(2.5, 1.5, -9)],
	["bus_interior", "intake", Vector3(2.5, 1.8, -12), Vector3(2.5, 1.5, -6)],
	["intake", "intake", Vector3(22.7, 2.2, -3.5), Vector3(17.0, 1.2, -11.0)],
	["cellblock", "cellblock", Vector3(29, 3, -6), Vector3(45, 1.6, -6)],
	["yard", "yard", Vector3(4, 2.2, -2), Vector3(25, 1.5, -22)],
	["court_layout", "yard", Vector3(20, 23, 9), Vector3(20, 0, -14)],
	["hoop_detail", "yard", Vector3(10, 2.3, -10), Vector3(7.575, 3, -14)],
	["workshop", "workshop", Vector3(3, 2.2, -9), Vector3(17, 1.2, -10)],
	["maintenance", "maintenance", Vector3(22, 2, -9), Vector3(18, 1.4, -23)],
	["solitary", "solitary", Vector3(101.5, 1.7, 1), Vector3(101.5, 1.2, -2.6)],
	# Phase 03 close-ups
	["bus_front", "intake", Vector3(7.5, 1.7, -1.5), Vector3(2.5, 1.4, -6.0)],
	["intake_counter", "intake", Vector3(19.6, 1.65, -7.6), Vector3(19.0, 1.0, -10.0)],
	["intake_lockers", "intake", Vector3(21.2, 1.6, -9.6), Vector3(23.5, 1.0, -9.5)],
	["workshop_machines", "workshop", Vector3(12.5, 1.75, -10.6), Vector3(12.5, 1.0, -6.0)],
	["maintenance_pumps", "maintenance", Vector3(19.0, 1.8, -14.5), Vector3(16.0, 0.8, -14.5)],
	["cell_interior", "cellblock", Vector3(33.0, 1.6, -2.5), Vector3(33.0, 0.8, 1.0)],
	["yard_fence", "yard", Vector3(4.0, 1.7, -8.0), Vector3(1.0, 1.8, -12.0)],
	["court_ground", "yard", Vector3(16.0, 1.6, -12.0), Vector3(12.0, 0.0, -16.0)],
	["maint_east", "maintenance", Vector3(21.0, 1.6, -8.0), Vector3(24.3, 1.5, -12.5)],
	["maint_brake", "maintenance", Vector3(22.4, 1.6, -15.5), Vector3(23.9, 1.0, -19.0)],
	["holding_bay", "intake", Vector3(21.0, 1.6, -12.4), Vector3(22.0, 1.2, -15.5)],
	["cellblock_night", "cellblock_night", Vector3(29, 3, -6), Vector3(45, 1.6, -6)],
	# characters posed in the intake (idle clip, settled), full body and 3/4 close-up
	["adrian_full", "intake", Vector3(15.2, 1.2, -6.4), Vector3(14.0, 0.95, -9.0), "ADRIAN"],
	["adrian_close", "intake", Vector3(14.75, 1.62, -8.1), Vector3(14.0, 1.42, -9.0), "ADRIAN"],
	["noah_full", "intake", Vector3(15.2, 1.2, -6.4), Vector3(14.0, 0.95, -9.0), "NOAH"],
	["noah_close", "intake", Vector3(14.75, 1.62, -8.1), Vector3(14.0, 1.42, -9.0), "NOAH"],
	["adrian_face", "intake", Vector3(14.42, 1.71, -8.42), Vector3(14.0, 1.66, -9.0), "ADRIAN"],
	["adrian_face_left", "intake", Vector3(14.6, 1.72, -9.05), Vector3(14.0, 1.68, -9.02), "ADRIAN", "yaw:0"],
	["adrian_brow", "intake", Vector3(14.07, 1.71, -8.62), Vector3(14.02, 1.69, -9.0), "ADRIAN"],
	["noah_full_back", "intake", Vector3(13.2, 1.2, -11.2), Vector3(14.0, 0.95, -9.0), "NOAH"],
	["handset_grip", "intake", Vector3(14.6, 1.7, -8.4), Vector3(14.0, 1.55, -9.0), "ADRIAN", "handset"],
	["handset_grip_side", "intake", Vector3(13.2, 1.7, -8.5), Vector3(14.0, 1.6, -9.0), "ADRIAN", "handset"],
	["bus_front_true", "intake", Vector3(5.6, 1.7, -17.8), Vector3(2.5, 1.4, -13.0)],
	["bus_doors_open", "intake", Vector3(7.6, 1.6, -15.6), Vector3(3.6, 1.3, -13.6)],
	["bus_cabin_fwd", "intake", Vector3(2.5, 2.05, -6.5), Vector3(2.5, 1.7, -14.0)],
	["yard_far_fence", "yard", Vector3(30, 1.7, -8), Vector3(10, 2.0, -29)],
]


func _ready() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="):
			output = arg.trim_prefix("--output=")
		if arg.begins_with("--only="):
			only = arg.trim_prefix("--only=").split(",")
		if arg.begins_with("--frames="):
			settle_frames = int(arg.trim_prefix("--frames="))
	call_deferred("run")


func _build(kind: String, b: EnvBuilder) -> void:
	match kind:
		"intake": EnvIntake.build(b)
		"cellblock": EnvCellblock.build(b, false)
		"cellblock_night": EnvCellblock.build(b, true)
		"yard": EnvYard.build(b)
		"workshop": EnvWorkshop.build(b)
		"maintenance": EnvMaintenance.build(b)
		"solitary": EnvSolitary.build(b)


func run() -> void:
	var root := get_tree().root
	root.size = Vector2i(1280, 720)
	root.msaa_3d = Viewport.MSAA_2X
	root.use_taa = true
	root.positional_shadow_atlas_size = 4096
	DirAccess.make_dir_recursive_absolute(output)
	var evidence := []
	for sample in samples:
		if not only.is_empty() and not only.has(sample[0]):
			continue
		var world := Node3D.new()
		root.add_child(world)
		var b := EnvBuilder.new(world)
		_build(sample[1], b)
		if sample.size() > 4:
			var v := CharacterVisual.new().setup(sample[4])
			world.add_child(v)
			v.position = Vector3(14.0, 0, -9.0)
			v.rotation.y = atan2(-(sample[2].x - 14.0), -(sample[2].z + 9.0))     # face the camera
			if sample.size() > 5 and String(sample[5]).begins_with("yaw:"):
				v.rotation.y = deg_to_rad(float(String(sample[5]).trim_prefix("yaw:")))
			if sample.size() > 5 and sample[5] == "handset":
				v.rotation.y = atan2(-(14.6 - 14.0), -(-8.4 + 9.0))
				v.act("handset", true)
				v.attach_to_hand(EnvBuilder.PROP + "wired_handset.glb", true, load("res://scripts/missions/mission_05.gd").HANDSET_GRIP)
		if sample[0] == "bus_doors_open":
			EnvIntake.open_doors(world.find_children("TransportBus", "Node3D", true, false)[0], 0.3)
		var camera := Camera3D.new()
		world.add_child(camera)
		camera.fov = 65.0
		camera.near = 0.05
		camera.far = 220.0
		camera.look_at_from_position(sample[2], sample[3])
		camera.current = true
		var t0 := Time.get_ticks_usec()
		for i in settle_frames:
			await get_tree().process_frame
		var frame_ms := (Time.get_ticks_usec() - t0) / 1000.0 / settle_frames
		await RenderingServer.frame_post_draw
		var path: String = output + "/" + sample[0] + ".png"
		var error := root.get_texture().get_image().save_png(path)
		var env_node := world.find_children("*", "WorldEnvironment", true, false)
		var env: Environment = (env_node[0] as WorldEnvironment).environment if not env_node.is_empty() else null
		evidence.append({"name": sample[0], "environment": sample[1], "position": var_to_str(sample[2]), "target": var_to_str(sample[3]),
			"fov": camera.fov, "width": 1280, "height": 720, "png_written": error == OK, "mean_frame_ms_single_view": snappedf(frame_ms, 0.01),
			"render": {"quality": Settings.graphics_quality, "sdfgi": env.sdfgi_enabled if env else false, "ssil": env.ssil_enabled if env else false,
				"ssao": env.ssao_enabled if env else false, "volumetric_fog": env.volumetric_fog_enabled if env else false,
				"tonemap": env.tonemap_mode if env else -1, "ambient_source": env.ambient_light_source if env else -1}})
		print("CAPTURE ", sample[0], " ", frame_ms, "ms")
		root.remove_child(world)
		world.queue_free()
		await get_tree().process_frame
	var f := FileAccess.open(output + "/cameras.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"renderer": RenderingServer.get_video_adapter_name(), "api": RenderingServer.get_video_adapter_api_version(),
		"godot": Engine.get_version_info()["string"], "captures": evidence}, "\t"))
	f.close()
	get_tree().quit()
