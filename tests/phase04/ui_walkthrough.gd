extends Node
## P04-UI / P04-COOP-001: UI walkthrough through real GUI input. Clicks real Buttons/CheckBoxes with synthesized mouse
## events (canvas coordinates), presses Escape as a key event for the pause menu, and records a screenshot per step:
## Settings → horizontal split on → Back → Controls and devices → Back → New Game (horizontal split) → pause → Resume →
## pause → Quit to main menu → Continue (resumes the save) → restore the setting. Pass = every step's effect observed.
## godot --path . --resolution 1600x900 res://tests/phase04/ui_walkthrough.tscn -- --save-slot=p04_ui

var OUT := "res://tests/phase04/evidence/ui_walkthrough.json"
var SHOTS := "res://tests/phase04/evidence/ui_walkthrough"

var main: Node
var steps := []
var original_split := ""


func _ready() -> void:
	for a in OS.get_cmdline_user_args():   # --ui-out=res://dir (Phase 05 runs write their own evidence)
		if a.begins_with("--ui-out="):
			SHOTS = a.trim_prefix("--ui-out=")
			OUT = SHOTS + ".json"
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
	# D05-022: the device controls themselves
	var owners_before: Array = Devices.owners.duplicate(true)
	await _step("change_device_p1", await _click("Button", "Change device for P1 Adrian") and Devices.owners[0] != owners_before[0],
		"%s -> %s" % [owners_before[0], Devices.owners[0]])
	await _step("change_device_p2", await _click("Button", "Change device for P2 Noah") and Devices.owners[0] != Devices.owners[1],
		"p1 %s p2 %s" % [Devices.owners[0], Devices.owners[1]])
	await _step("auto_detect", await _click("Button", "Auto-detect (controllers first)") and Devices.owners[0] != Devices.owners[1],
		"p1 %s p2 %s" % [Devices.owners[0], Devices.owners[1]])
	await _step("devices_back", await _click("Button", "Back") and _find("Button", "New Game") != null)
	await _step("credits", await _click("Button", "Credits") and _find("Button", "Back") != null)
	await _step("credits_back", await _click("Button", "Back") and _find("Button", "New Game") != null)
	await _click("Button", "Settings")
	var slider: HSlider = null
	for c in get_tree().root.find_children("*", "HSlider", true, false):
		if (c as HSlider).is_visible_in_tree():
			slider = c
			break
	var before := Settings.subtitle_scale
	if slider:
		slider.value = clampf(before + 0.2, slider.min_value, slider.max_value)   # same signal path as a drag
	await _frames(2)
	await _step("settings_slider", slider != null and absf(Settings.subtitle_scale - before) > 0.05, "subtitle %.1f -> %.1f" % [before, Settings.subtitle_scale])
	Settings.set_value("subtitle_scale", before)
	# D05-022: graphics dropdown (real click opens the popup, keyboard picks the next item) and the toggles
	var q_before := Settings.graphics_quality
	var opened := await _click("OptionButton", "Graphics:")
	await _frames(3)
	var popup: PopupMenu = (_find("OptionButton", "Graphics:") as OptionButton).get_popup() if opened else null
	opened = opened and popup != null and popup.visible
	if opened:   # keys go to the popup's own window (the real click opened it)
		for code in [KEY_DOWN if q_before < 2 else KEY_UP, KEY_ENTER]:
			for pressed in [true, false]:
				var e := InputEventKey.new()
				e.keycode = code
				e.physical_keycode = code
				e.pressed = pressed
				popup.push_input(e)
				await _frames(2)
	await _frames(3)
	await _step("graphics_dropdown", opened and Settings.graphics_quality != q_before, "%d -> %d" % [q_before, Settings.graphics_quality])
	Settings.set_value("graphics_quality", q_before)
	for t in ["Reduced flashing", "Hold actions toggle"]:
		var key := "reduced_flash" if t.begins_with("Reduced") else "hold_toggle"
		var was: bool = Settings.get(key)
		await _step("toggle_" + key, await _click("CheckBox", t) and Settings.get(key) != was)
		await _click("CheckBox", t)
		await _step("toggle_" + key + "_back", Settings.get(key) == was)
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
	var cp_before := GameState.checkpoint_id
	await _step("pause_restart", await _click("Button", "Restart from last checkpoint"))
	await _frames(120)
	await _step("restart_resumes", main.get("chapter") != null and not get_tree().paused and GameState.checkpoint_id == cp_before, "cp %s" % GameState.checkpoint_id)
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
	# D05-022: the main-menu Quit button must end the process (the runner checks the exit and that the
	# "QUIT DID NOT EXIT" line never prints)
	await _key(KEY_ESCAPE)
	await _frames(10)
	await _click("Button", "Quit to main menu")
	await _frames(30)
	print("UI QUIT CLICKED ", await _click("Button", "Quit"))
	await _frames(120)
	print("UI QUIT DID NOT EXIT")
	get_tree().quit(0 if ok else 1)
