extends Node
## Deterministic environment review. No mission completion or playability claims.
var output := "res://tests/phase025/evidence/before"
var only := ""
var legacy_bus := false
var samples := [
	["bus", Vector3(-3, 2, 1), Vector3(2.5, 1.5, -9)],
	["bus_interior", Vector3(2.5, 1.8, -12), Vector3(2.5, 1.5, -6)],
	["intake", Vector3(22.7, 2.2, -3.5), Vector3(17.0, 1.2, -11.0)],
	["cellblock", Vector3(29, 3, -6), Vector3(45, 1.6, -6)],
	["yard", Vector3(4, 2.2, -2), Vector3(25, 1.5, -22)],
	["court_layout", Vector3(20, 23, 9), Vector3(20, 0, -14)],
	["hoop_detail", Vector3(10, 2.3, -10), Vector3(7.575, 3, -14)],
	["workshop", Vector3(3, 2.2, -9), Vector3(17, 1.2, -10)],
	["maintenance", Vector3(22, 2, -9), Vector3(18, 1.4, -23)],
	["solitary", Vector3(101.5, 1.7, 1), Vector3(101.5, 1.2, -2.6)],
]

func _ready() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="):
			output = arg.trim_prefix("--output=")
		if arg.begins_with("--only="):
			only = arg.trim_prefix("--only=")
		if arg == "--legacy-bus":
			legacy_bus = true
	call_deferred("run")

func run() -> void:
	var root := get_tree().root
	root.size = Vector2i(1280, 720)
	root.msaa_3d = Viewport.MSAA_2X
	root.use_taa = true
	DirAccess.make_dir_recursive_absolute(output)
	var evidence := []
	for sample in samples:
		if only != "" and sample[0] != only:
			continue
		var world := Node3D.new()
		root.add_child(world)
		var b := EnvBuilder.new(world)
		match sample[0]:
			"bus": EnvIntake.build(b)
			"bus_interior": EnvIntake.build(b)
			"intake": EnvIntake.build(b)
			"cellblock": EnvCellblock.build(b, false)
			"yard": EnvYard.build(b)
			"court_layout": EnvYard.build(b)
			"hoop_detail": EnvYard.build(b)
			"workshop": EnvWorkshop.build(b)
			"maintenance": EnvMaintenance.build(b)
			"solitary": EnvSolitary.build(b)
		if legacy_bus and sample[0] == "bus":
			var current := b.root.get_node("TransportBus")
			b.root.remove_child(current)
			current.free()
			var old := b.model("res://assets/props/phase15_discovery/quaternius_bus/quaternius_bus.glb", Vector3(2.5, 0, -9), 0, "none")
			var bounds := EnvBuilder.local_aabb(old)
			old.scale = Vector3.ONE * (11.0 / maxf(bounds.size.x, bounds.size.z))
			old.rotation_degrees.y = 90.0 if bounds.size.x > bounds.size.z else 0.0
		var camera := Camera3D.new()
		world.add_child(camera)
		camera.fov = 65.0
		camera.near = 0.1
		camera.far = 180.0
		camera.look_at_from_position(sample[1], sample[2])
		camera.current = true
		for i in 12:
			await get_tree().process_frame
		await RenderingServer.frame_post_draw
		var path: String = output + "/" + sample[0] + ".png"
		var error := root.get_texture().get_image().save_png(path)
		evidence.append({"environment": sample[0], "position": var_to_str(sample[1]), "target": var_to_str(sample[2]), "fov": camera.fov, "width": 1280, "height": 720, "written": error == OK})
		root.remove_child(world)
		world.queue_free()
		await get_tree().process_frame
	var f := FileAccess.open(output + "/cameras.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(evidence, "\t"))
	f.close()
	get_tree().quit()
