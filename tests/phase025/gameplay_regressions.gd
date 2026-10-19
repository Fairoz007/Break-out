extends Node
## Focused movement safety regressions. Run with --headless --fixed-fps 60.
var failures: Array[String] = []
var results := {}

func check(label: String, ok: bool) -> void:
	results[label] = ok
	if not ok:
		failures.append(label)
	print(label, ": ", "PASS" if ok else "FAIL")

func frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame

func _ready() -> void:
	var old: Dictionary = Devices.owners[0].duplicate()
	Devices.set_virtual(0, true)
	Devices.virtual_state[0]["buttons"]["jump"] = true
	Devices._process(0.0)
	Devices.set_virtual(0, false)
	check("virtual_owner_restored", Devices.owners[0] == old)
	check("virtual_edges_cleared", not Devices.just_pressed(0, "jump"))
	Devices.set_virtual(0, true)
	Devices.set_virtual(1, true)
	var world := Node3D.new()
	add_child(world)
	var floor_body := StaticBody3D.new()
	floor_body.collision_layer = EnvBuilder.LAYER_WORLD | EnvBuilder.LAYER_CAMERA
	var floor_shape := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = Vector3(30, 1, 30)
	floor_shape.shape = box
	floor_shape.position.y = -0.5
	floor_body.add_child(floor_shape)
	world.add_child(floor_body)
	var p := Player.new().setup(0, "ADRIAN")
	world.add_child(p)
	p.place(Transform3D.IDENTITY)
	await frames(10)
	check("floor_detected", p.is_on_floor())
	p.set_crouched(true)
	check("crouch_capsule_reduced", is_equal_approx((p.body_shape.shape as CapsuleShape3D).height, Player.CROUCH_HEIGHT))
	var ceiling := StaticBody3D.new()
	ceiling.collision_layer = EnvBuilder.LAYER_WORLD | EnvBuilder.LAYER_CAMERA
	var ceiling_shape := CollisionShape3D.new()
	var ceiling_box := BoxShape3D.new()
	ceiling_box.size = Vector3(3, 0.2, 3)
	ceiling_shape.shape = ceiling_box
	ceiling_shape.position.y = 1.4
	ceiling.add_child(ceiling_shape)
	world.add_child(ceiling)
	await frames(3)
	check("blocked_stand_preserves_crouch", not p.set_crouched(false) and p.crouched)
	ceiling.queue_free()
	await frames(3)
	check("clear_headroom_stands", p.set_crouched(false) and not p.crouched)
	Devices.virtual_state[0]["buttons"]["jump"] = true
	await get_tree().process_frame
	await frames(3)
	check("jump_leaves_floor", p.position.y > 0.02 and p.velocity.y > 0.0)
	check("jump_input_isolated", not Devices.pressed(1, "jump"))
	Devices.virtual_state[0]["buttons"]["jump"] = false
	await frames(90)
	check("jump_lands", p.is_on_floor() and absf(p.position.y) < 0.05)
	p.traverse([Vector3(10, 0, 0)])
	p.recover()
	check("recovery_restores_collision", p.collision_mask == Player.BODY_MASK and not p.is_traversing())
	p.traverse([Vector3(10, 0, 0)])
	p.place(Transform3D.IDENTITY)
	check("place_cancels_traversal", p.collision_mask == Player.BODY_MASK and not p.is_traversing())
	var camera := Camera3D.new()
	world.add_child(camera)
	var rig := PlayerCamera.new().setup(p, camera)
	world.add_child(rig)
	p.place(Transform3D.IDENTITY)
	var wall := StaticBody3D.new()
	wall.collision_layer = EnvBuilder.LAYER_WORLD | EnvBuilder.LAYER_CAMERA
	var wall_shape := CollisionShape3D.new()
	var wall_box := BoxShape3D.new()
	wall_box.size = Vector3(3, 3, 0.1)
	wall_shape.shape = wall_box
	wall_shape.position = Vector3(0, 1.5, 0.4)
	wall.add_child(wall_shape)
	world.add_child(wall)
	await frames(10)
	await get_tree().process_frame
	check("camera_respects_near_wall", camera.global_position.z < 0.35)
	var blend_safe := true
	var cinematic_origin := Transform3D(Basis.IDENTITY, Vector3(0, 1.6, 2.0))
	rig.blend_back(cinematic_origin, 55.0)
	for tick in 30:
		await get_tree().physics_frame
		# The 10 cm wall spans z0.35..0.45. Every intermediate camera must remain near-side.
		if camera.global_position.z >= 0.35:
			blend_safe = false
	check("camera_blend_respects_thin_wall", blend_safe)
	p.set_crouched(true)
	rig.snap_behind(p)
	check("crouch_camera_follows_head", rig.global_position.y < 1.1)
	var f := FileAccess.open("res://tests/phase025/gameplay_results.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"results": results, "failures": failures}, "\t"))
	f.close()
	get_tree().quit(0 if failures.is_empty() else 1)

