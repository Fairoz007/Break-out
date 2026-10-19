extends Node
## Graphical locomotion inspection using routed virtual input. Not a hardware playthrough.
var chapter: ChapterRoot
var rows := []
const DIR := "res://tests/phase025/evidence/movement_visual"

func frames(count: int) -> void:
	for i in count:
		await get_tree().physics_frame

func _ready() -> void:
	get_tree().root.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(DIR)
	chapter = ChapterRoot.new()
	add_child(chapter)
	EnvCellblock.build(EnvBuilder.new(chapter.world), false)
	for i in 2:
		Devices.set_virtual(i, true)
	reset_positions()
	await frames(30)
	await capture("idle")
	for state in ["walk", "run", "sprint", "crouch"]:
		reset_positions()
		for i in 2:
			Devices.virtual_state[i]["move"] = Vector2.UP
			Devices.virtual_state[i]["buttons"] = {state: true} if state != "walk" else {}
		await frames(35)
		await capture(state)
	reset_positions()
	await frames(10)
	for i in 2:
		Devices.virtual_state[i]["buttons"]["jump"] = true
	await frames(10)
	await capture("jump_rising")
	for i in 2:
		Devices.virtual_state[i]["buttons"]["jump"] = false
	await frames(28)
	await capture("jump_falling")
	await frames(17)
	await capture("landing")
	await frames(50)
	await capture("landed_idle")
	var file := FileAccess.open(DIR + "/states.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(rows, "\t"))
	file.close()
	print("MOVEMENT VISUAL CAPTURED ", rows.size(), " states")
	get_tree().quit()

func reset_positions() -> void:
	for i in 2:
		Devices.virtual_state[i] = Devices._blank_virtual()
		chapter.players[i].set_crouched(false)
		chapter.players[i].place(Transform3D(Basis(Vector3.UP, -PI / 2), Vector3(33, 0, -6 - i * 3)))

func capture(label: String) -> void:
	await RenderingServer.frame_post_draw
	var code := get_viewport().get_texture().get_image().save_png(DIR + "/" + label + ".png")
	rows.append({"state": label, "written": code == OK, "players": chapter.players.map(func(p): return {
		"clip": p.visual.current_clip(), "grounded": p.is_on_floor(), "crouched": p.crouched,
		"speed": Vector2(p.velocity.x, p.velocity.z).length(), "height": p.position.y})})
