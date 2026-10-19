extends Node
## P04-UI / P04-COOP-001: UI walkthrough through real GUI input. Clicks real Buttons/CheckBoxes with synthesized mouse
## events (canvas coordinates), presses Escape as a key event for the pause menu, and records a screenshot per step:
## Settings → horizontal split on → Back → Controls and devices → Back → New Game (horizontal split) → pause → Resume →
## pause → Quit to main menu → Continue (resumes the save) → restore the setting. Pass = every step's effect observed.
## godot --path . --resolution 1600x900 res://tests/phase04/ui_walkthrough.tscn -- --save-slot=p04_ui

const OUT := "res://tests/phase04/evidence/ui_walkthrough.json"
const SHOTS := "res://tests/phase04/evidence/ui_walkthrough"

var main: Node
var steps := []
var original_split := ""


func _ready() -> void:
	DirAccess.make_dir_recursive_absolute(SHOTS)
	original_split = Settings.split_mode
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate()
	get_tree().root.add_child.call_deferred(main)
	_run.call_deferred()


func _frames(n: int) -> void:
	for i in n:
		await get_tree().process_frame


func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("%s/%02d_%s.png" % [SHOTS, steps.size(), name])


func _find(cls: String, text: String) -> Control:
	for c in get_tree().root.find_children("*", cls, true, false):
		var b := c as BaseButton
		if b and b.is_visible_in_tree() and (b as Button).text.begins_with(text):
			return b
	return null


func _click(cls: String, text: String) -> bool:
	var b := _find(cls, text)
	if b == null:
		return false
	var c := b.get_global_rect().get_center()
	var hover := InputEventMouseMotion.new()
	hover.position = c
	hover.global_position = c
	get_viewport().push_input(hover, true)
	await get_tree().process_frame
	for pressed in [true, false]:
		var e := InputEventMouseButton.new()
		e.button_index = MOUSE_BUTTON_LEFT
		e.pressed = pressed
		e.position = c
		e.global_position = c
		get_viewport().push_input(e, true)
		await get_tree().process_frame
	return true


func _key(code: Key) -> void:
	for pressed in [true, false]:
		var e := InputEventKey.new()
		e.physical_keycode = code
		e.keycode = code
		e.pressed = pressed
		Input.parse_input_event(e)
		await _frames(3)


func _step(name: String, ok: bool, detail := "") -> void:
	await _shot(name)
	steps.append({"step": name, "pass": ok, "detail": detail})
	print("UI ", name, " ", "PASS" if ok else "FAIL " + detail)


func _run() -> void:
	await _frames(30)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	await _step("main_menu", _find("Button", "New Game") != null and _find("Button", "Settings") != null)
	await _step("open_settings", await _click("Button", "Settings") and _find("CheckBox", "Horizontal split") != null)
	var cb := _find("CheckBox", "Horizontal split") as CheckBox
	if cb and not cb.button_pressed:
		await _click("CheckBox", "Horizontal split")
	await _step("horizontal_split_on", Settings.split_mode == "horizontal", Settings.split_mode)
	await _step("settings_back", await _click("Button", "Back") and _find("Button", "New Game") != null)
	await _step("controls_and_devices", await _click("Button", "Controls and devices") and _find("Button", "Back") != null)
	await _click("Button", "Back")
	await _step("new_game", await _click("Button", "New Game"))
	await _frames(240)
	var chapter = main.get("chapter")
	var views: Node = chapter.get("views") if chapter else null
	await _step("horizontal_layout_in_game", views is VBoxContainer, str(views.get_class()) if views else "no chapter")
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	await _key(KEY_ESCAPE)
	await _frames(10)
	await _step("pause_opens", get_tree().paused and _find("Button", "Resume") != null)
	await _click("Button", "Resume")
	await _frames(10)
	await _step("resume", not get_tree().paused)
	await _key(KEY_ESCAPE)
	await _frames(10)
	await _click("Button", "Quit to main menu")
	await _frames(30)
	await _step("quit_to_menu", main.get("chapter") == null and _find("Button", "Continue") != null)
	var cont := _find("Button", "Continue") as Button
	await _step("continue_enabled", cont != null and not cont.disabled)
	await _click("Button", "Continue")
	await _frames(240)
	await _step("continue_resumes", main.get("chapter") != null and GameState.mission_index >= 1, "mission %d" % GameState.mission_index)
	Settings.set_value("split_mode", original_split)
	var ok := steps.all(func(s): return s["pass"])
	var f := FileAccess.open(OUT, FileAccess.WRITE)
	f.store_string(JSON.stringify({"pass": ok, "steps": steps}, "\t"))
	f.close()
	print("UI WALKTHROUGH ", "PASS" if ok else "FAIL")
	get_tree().quit(0 if ok else 1)
