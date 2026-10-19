extends Control
## Pause menu available to either player (REQ-UI-002/004, REQ-INPUT-002). Pausing stops gameplay, dialogue and
## cinematic clocks. Every button performs a real action.

var chapter: ChapterRoot
var panel: PanelContainer
var title: Label
var message: Label
var box: VBoxContainer
var settings_box: VBoxContainer
var devices_box: VBoxContainer
var opened_by := -1


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.6)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	panel = PanelContainer.new()
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.custom_minimum_size = Vector2(620, 0)
	add_child(panel)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 10)
	panel.add_child(v)
	title = _label(v, "PAUSED", 40)
	message = _label(v, "", 22)
	message.autowrap_mode = TextServer.AUTOWRAP_WORD
	box = VBoxContainer.new()
	v.add_child(box)
	_button(box, "Resume", close)
	_button(box, "Restart from last checkpoint", _restart)
	_button(box, "Settings", func(): _show(settings_box))
	_button(box, "Controls and devices", func(): _show(devices_box))
	_button(box, "Quit to main menu", _quit)
	settings_box = SettingsPanel.build(v, func(): _show(box))
	devices_box = DevicesPanel.build(v, func(): _show(box))
	_show(box)


static func _label(parent: Node, text: String, size_px: int) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", size_px)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	parent.add_child(l)
	return l


static func _button(parent: Node, text: String, cb: Callable) -> Button:
	var b := Button.new()
	b.text = text
	b.add_theme_font_size_override("font_size", 26)
	b.custom_minimum_size = Vector2(0, 52)
	b.pressed.connect(cb)
	parent.add_child(b)
	return b


func _show(which: Control) -> void:
	for c in [box, settings_box, devices_box]:
		c.visible = c == which
	await get_tree().process_frame
	for c in which.get_children():
		if c is Button:
			c.grab_focus()
			break


func toggle(player: int) -> void:
	if visible:
		close()
	else:
		open(player)


func open(player: int, msg := "") -> void:
	opened_by = player
	message.text = msg if msg != "" else "Paused by %s" % ["Adrian (P1)", "Noah (P2)"][player]
	visible = true
	get_tree().paused = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	GameState.log_event("pause", {"player": player})
	_show(box)


func close() -> void:
	visible = false
	get_tree().paused = false
	if Devices.owners[0]["kind"] == Devices.Kind.KEYBOARD_MOUSE or Devices.owners[1]["kind"] == Devices.Kind.KEYBOARD_MOUSE:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	GameState.log_event("resume", {})


func _restart() -> void:
	close()
	chapter.reload_checkpoint()


func _quit() -> void:
	close()
	get_tree().paused = false
	chapter.quit_to_menu.emit()
