extends Control
## Main menu (REQ-UI-001). New Game, Continue (only with a save), Controls and devices, Settings, Quit.

signal new_game
signal continue_game
signal quit_game

var main_box: VBoxContainer
var settings_box: VBoxContainer
var devices_box: VBoxContainer
var continue_button: Button
var credits_box: VBoxContainer


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var bg := ColorRect.new()
	bg.color = Color(0.05, 0.06, 0.07)
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(bg)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(center)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	center.add_child(v)
	var title := Label.new()
	title.text = "BREAKOUT: NO WAY BACK"
	title.add_theme_font_size_override("font_size", 64)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	v.add_child(title)
	var sub := Label.new()
	sub.text = "Chapter 1 — Blackridge · local two-player split-screen"
	sub.add_theme_font_size_override("font_size", 26)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.modulate = Color(0.75, 0.78, 0.8)
	v.add_child(sub)
	main_box = VBoxContainer.new()
	main_box.add_theme_constant_override("separation", 10)
	v.add_child(main_box)
	_button(main_box, "New Game", func(): new_game.emit())
	continue_button = _button(main_box, "Continue", func(): continue_game.emit())
	_button(main_box, "Controls and devices", func(): _show(devices_box))
	_button(main_box, "Settings", func(): _show(settings_box))
	_button(main_box, "Credits", func(): _show(credits_box))
	_button(main_box, "Quit", func(): quit_game.emit())
	settings_box = SettingsPanel.build(v, func(): _show(main_box))
	devices_box = DevicesPanel.build(v, func(): _show(main_box))
	credits_box = VBoxContainer.new()
	v.add_child(credits_box)
	_button(credits_box, "Back", func(): _show(main_box))
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(1100, 640)
	credits_box.add_child(scroll)
	var text := Label.new()
	text.text = FileAccess.get_file_as_string("res://data/credits.txt")   # MIT / CC BY notices required in the shipped build
	text.autowrap_mode = TextServer.AUTOWRAP_WORD
	text.custom_minimum_size = Vector2(1060, 0)
	text.add_theme_font_size_override("font_size", 18)
	scroll.add_child(text)
	refresh()
	_show(main_box)


func refresh() -> void:
	continue_button.disabled = not SaveService.has_save()


func _button(parent: Node, text: String, cb: Callable) -> Button:
	var b := Button.new()
	b.text = text
	b.custom_minimum_size = Vector2(460, 56)
	b.add_theme_font_size_override("font_size", 28)
	b.pressed.connect(cb)
	parent.add_child(b)
	return b


func _show(which: Control) -> void:
	for c in [main_box, settings_box, devices_box, credits_box]:
		c.visible = c == which
	await get_tree().process_frame
	for c in which.get_children():
		if c is Button and not c.disabled:
			c.grab_focus()
			break
