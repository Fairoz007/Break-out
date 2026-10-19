class_name PlayerHud
extends Control
## One HUD per split-screen half (REQ-UI-003, REQ-COOP-004, REQ-OBJ-001): objective, role-labelled prompt,
## partner waiting state, hold progress, detection warning, checkpoint notice, ready prompt and info panels.

var player: Player
var objective: Label
var prompt: Label
var status: Label
var bar: ProgressBar
var detect: ProgressBar
var notice: Label
var info: Label
var ready_label: Label
var subtitles: Subtitles
var _notice_left := 0.0
var ready_requested := false
var ready_confirmed := false


func setup(p: Player) -> PlayerHud:
	player = p
	name = "HUD_P%d" % (p.index + 1)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var tag := _label(Vector2(24, 18), 22, ["ADRIAN — P1", "NOAH — P2"][p.index])
	tag.modulate = [Color("#9ec9ff"), Color("#ffc27a")][p.index]
	objective = _label(Vector2(24, 50), 24, "")
	objective.autowrap_mode = TextServer.AUTOWRAP_WORD
	objective.size.x = 520
	notice = _label(Vector2(24, 120), 22, "")
	notice.modulate = Color("#b9f6b0")
	prompt = _label(Vector2(0, 0), 28, "")
	prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status = _label(Vector2(0, 0), 22, "")
	status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status.modulate = Color("#ffd27a")
	bar = ProgressBar.new()
	bar.size = Vector2(260, 14)
	bar.max_value = 1.0
	bar.show_percentage = false
	bar.visible = false
	add_child(bar)
	detect = ProgressBar.new()
	detect.size = Vector2(300, 16)
	detect.max_value = 1.0
	detect.show_percentage = false
	detect.modulate = Color(1, 0.35, 0.3)
	detect.visible = false
	add_child(detect)
	info = _label(Vector2(40, 170), 26, "")
	info.autowrap_mode = TextServer.AUTOWRAP_WORD
	info.size.x = 600
	var ib := StyleBoxFlat.new()
	ib.bg_color = Color(0.08, 0.08, 0.06, 0.85)
	ib.content_margin_left = 16
	ib.content_margin_right = 16
	ib.content_margin_top = 12
	ib.content_margin_bottom = 12
	info.add_theme_stylebox_override("normal", ib)
	info.visible = false
	ready_label = _label(Vector2(0, 0), 30, "")
	ready_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ready_label.modulate = Color("#ffffff")
	subtitles = Subtitles.new()
	subtitles.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(subtitles)
	GameState.objective_changed.connect(_on_objective)
	GameState.checkpoint_committed.connect(_on_checkpoint)
	return self


func _label(pos: Vector2, font: int, text: String) -> Label:
	var l := Label.new()
	l.position = pos
	l.text = text
	l.add_theme_font_size_override("font_size", font)
	l.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.9))
	l.add_theme_constant_override("shadow_offset_x", 2)
	l.add_theme_constant_override("shadow_offset_y", 2)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(l)
	return l


func _on_objective(_id: String, text: String) -> void:
	objective.text = ("Objective: " + text) if text != "" else ""


func _on_checkpoint(cp: String) -> void:
	flash_notice("Checkpoint saved — " + cp)


func flash_notice(text: String, seconds := 3.0) -> void:
	notice.text = text
	_notice_left = seconds


func show_info(text: String) -> void:
	info.text = text
	info.visible = text != ""


func ask_ready() -> void:
	ready_requested = true
	ready_confirmed = false


func _process(delta: float) -> void:
	var w := size.x
	var h := size.y
	prompt.position = Vector2(0, h * 0.62)
	prompt.size.x = w
	status.position = Vector2(0, h * 0.62 + 40)
	status.size.x = w
	bar.position = Vector2((w - bar.size.x) / 2.0, h * 0.62 + 76)
	detect.position = Vector2((w - detect.size.x) / 2.0, 24)
	ready_label.position = Vector2(0, h * 0.42)
	ready_label.size.x = w
	if _notice_left > 0.0:
		_notice_left -= delta
		if _notice_left <= 0.0:
			notice.text = ""
	if not is_instance_valid(player):
		return
	var key := Devices.prompt_key(player.index, "interact")
	if ready_requested:
		ready_label.text = ("Ready — waiting for partner" if ready_confirmed else "Press [%s] when ready" % key)
	else:
		ready_label.text = ""
	var m = get_tree().get_first_node_in_group("mission")
	if m and not m.guide[player.index].is_empty() and not player.input_locked:
		var g: Dictionary = m.guide[player.index]
		var to: Vector3 = g["pos"] - player.global_position
		var rel := rad_to_deg(wrapf(atan2(-to.x, -to.z) - player.rig.yaw, -PI, PI)) if player.rig else 0.0
		var arrow := "↑" if absf(rel) < 30.0 else ("←" if rel > 0.0 else "→")
		notice.text = "%s %s  %.0f m" % [arrow, g["label"], Vector2(to.x, to.z).length()] if _notice_left <= 0.0 else notice.text
	var it: Interactable = player.holding if player.holding else player.focus
	if it and not player.input_locked:
		if player.holding:
			prompt.text = "%s — holding (release [%s] to let go)" % [it.label, key]
		else:
			prompt.text = "[%s] %s" % [key, it.label]
		status.text = it.status_text
		bar.visible = it.mode == Interactable.Mode.HOLD_COMPLETE and it.holder == player.index
		bar.value = it.progress
	else:
		prompt.text = ""
		status.text = ""
		bar.visible = false


func set_detection(level: float) -> void:
	detect.visible = level > 0.01
	detect.value = level
