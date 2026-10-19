extends Node
## Prop grip tuning aid: four Adrians playing the handset clip, each holding the wired handset with a different
## hand-bone rotation, captured to tests/phase03/evidence/grip_sweep.png. Visual tuning only.

const GRIPS := [Vector3(0, 0, 0), Vector3(0, 0, 90), Vector3(90, 0, 0), Vector3(0, 90, 0)]


func _ready() -> void:
	_run.call_deferred()


func _run() -> void:
	var root := get_tree().root
	root.size = Vector2i(1600, 600)
	var world := Node3D.new()
	root.add_child(world)
	var b := EnvBuilder.new(world)
	EnvIntake.build(b)
	for i in GRIPS.size():
		var v := CharacterVisual.new().setup("ADRIAN")
		world.add_child(v)
		v.position = Vector3(12.0 + i * 1.3, 0, -9.0)
		v.rotation.y = deg_to_rad(205)
		v.act("handset", true)
		var e: Vector3 = GRIPS[i]
		var prop := v.attach_to_hand(EnvBuilder.PROP + "wired_handset.glb", true,
			Transform3D(Basis.from_euler(Vector3(deg_to_rad(e.x), deg_to_rad(e.y), deg_to_rad(e.z))).scaled(Vector3.ONE * 0.55), Vector3(0.0, 0.04, 0.03)))
		var l := Label3D.new()
		l.text = str(e)
		l.pixel_size = 0.003
		l.position = Vector3(0, 2.05, 0)
		v.add_child(l)
	var cam := Camera3D.new()
	world.add_child(cam)
	cam.fov = 32
	cam.look_at_from_position(Vector3(13.95, 1.7, -6.0), Vector3(13.95, 1.62, -9.0))
	cam.current = true
	for i in 60:
		await get_tree().process_frame
	for ba in world.find_children("Hand_*", "BoneAttachment3D", true, false):
		var pr: Node3D = ba.get_child(0)
		print("GRIP ", ba.bone_name, " bone_idx=", (ba.get_parent() as Skeleton3D).find_bone(ba.bone_name), " scale=", pr.global_transform.basis.get_scale(), " pos=", pr.global_position, " ba_pos=", ba.global_position)
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://tests/phase03/evidence/grip_sweep.png")
	get_tree().quit()
