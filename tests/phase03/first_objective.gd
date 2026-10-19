extends Node
## P03-PLAY-017: fresh game -> first real mission objective, through the real main menu.
## Boots scenes/main.tscn, clicks the actual "New Game" Button with a synthesized mouse press/release at its
## on-screen centre (the GUI input path a player uses), then hands both players to the virtual-device autopilot
## and passes only when CH01_M01_OBJ001 is set and then completed. Graphical runs also save menu/objective PNGs.
## godot --path . res://tests/phase03/first_objective.tscn -- --save-slot=p03_first_objective

const OUT := "res://tests/phase03/evidence/first_objective.json"
const SHOTS := "res://tests/phase03/evidence/first_objective"

var main: Node
var result := {"menu_new_game": false, "chapter_started": false, "objective_set": -1.0, "objective_completed": -1.0, "pass": false, "errors": []}
var t0 := 0


func _ready() -> void:
	t0 = Time.get_ticks_msec()
	DirAccess.make_dir_recursive_absolute(SHOTS)
	GameState.event_logged.connect(_on_event)
	main = load("res://scenes/main.tscn").instantiate()
	get_tree().root.add_child.call_deferred(main)
	_run.call_deferred()


func _shot(name: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("%s/%s.png" % [SHOTS, name])


func _run() -> void:
	for i in 30:
		await get_tree().process_frame
	var button: Button = null
	for b in main.find_children("*", "Button", true, false):
		if (b as Button).text == "New Game" and (b as Button).is_visible_in_tree():
			button = b
	if button == null:
		result["errors"].append("New Game button not found in the main menu")
		_finish()
		return
	await _shot("01_main_menu")
	var centre := button.get_global_rect().get_center()
	var hover := InputEventMouseMotion.new()
	hover.position = centre
	hover.global_position = centre
	get_viewport().push_input(hover, true)        # canvas (local) coordinates: the menu is stretch-scaled
	await get_tree().process_frame
	for pressed in [true, false]:
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.pressed = pressed
		ev.position = centre
		ev.global_position = centre
		get_viewport().push_input(ev, true)
		await get_tree().process_frame
	result["menu_new_game"] = true
	for i in 120:
		await get_tree().process_frame
		if main.get("chapter") != null:
			break
	var chapter = main.get("chapter")
	if chapter == null:
		result["errors"].append("New Game click did not start Chapter 1")
		_finish()
		return
	result["chapter_started"] = true
	var ap = load("res://tests/phase02/autopilot.gd").new()
	ap.name = "Autopilot"
	ap.chapter = chapter
	ap.args = {"speed": "2", "timeout": "900"}
	main.add_child(ap)
	while (Time.get_ticks_msec() - t0) < 600000 and result["objective_completed"] < 0.0:
		await get_tree().process_frame
	_finish()


func _on_event(kind: String, e: Dictionary) -> void:
	if e.get("id", "") != "CH01_M01_OBJ001":
		return
	if kind == "objective_set" and result["objective_set"] < 0.0:
		result["objective_set"] = e["t"]
		_shot("02_objective_set")
	elif kind == "objective_completed":
		result["objective_completed"] = e["t"]


func _finish() -> void:
	result["pass"] = result["menu_new_game"] and result["chapter_started"] and result["objective_set"] >= 0.0 and result["objective_completed"] >= result["objective_set"]
	result["real_seconds"] = (Time.get_ticks_msec() - t0) / 1000.0
	result["renderer"] = DisplayServer.get_name()
	var f := FileAccess.open(OUT, FileAccess.WRITE)
	f.store_string(JSON.stringify(result, "\t"))
	f.close()
	print("FIRST OBJECTIVE ", JSON.stringify(result))
	get_tree().quit(0 if result["pass"] else 1)
