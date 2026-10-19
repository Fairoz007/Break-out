class_name SettingsPanel
extends RefCounted
## Settings controls shared by the main and pause menus (REQ-UI-004, REQ-INPUT-003).


static func build(parent: Node, back: Callable) -> VBoxContainer:
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	parent.add_child(v)
	_slider(v, "Subtitle size", "subtitle_scale", 0.8, 1.6, 0.1)
	_slider(v, "Music volume", "music_volume", 0.0, 1.0, 0.05)
	_slider(v, "Voice volume", "voice_volume", 0.0, 1.0, 0.05)
	_slider(v, "Effects volume", "sfx_volume", 0.0, 1.0, 0.05)
	for p in 2:
		var who: String = ["P1 Adrian", "P2 Noah"][p]
		var s := _row(v, who + " camera sensitivity")
		var sl := HSlider.new()
		sl.min_value = 0.3
		sl.max_value = 2.5
		sl.step = 0.1
		sl.value = Settings.camera_sensitivity[p]
		sl.custom_minimum_size = Vector2(240, 30)
		sl.value_changed.connect(func(val):
			var arr: Array = Settings.camera_sensitivity.duplicate()
			arr[p] = val
			Settings.set_value("camera_sensitivity", arr))
		s.add_child(sl)
		var inv := CheckBox.new()
		inv.text = who + " invert vertical look"
		inv.button_pressed = Settings.invert_y[p]
		inv.toggled.connect(func(on):
			var arr: Array = Settings.invert_y.duplicate()
			arr[p] = on
			Settings.set_value("invert_y", arr))
		v.add_child(inv)
	var hold := CheckBox.new()
	hold.text = "Hold actions toggle (press once to hold, again to release)"
	hold.button_pressed = Settings.hold_toggle
	hold.toggled.connect(func(on): Settings.set_value("hold_toggle", on))
	v.add_child(hold)
	var flash := CheckBox.new()
	flash.text = "Reduced flashing (steady alarm light)"
	flash.button_pressed = Settings.reduced_flash
	flash.toggled.connect(func(on): Settings.set_value("reduced_flash", on))
	v.add_child(flash)
	var b := Button.new()
	b.text = "Back"
	b.add_theme_font_size_override("font_size", 24)
	b.pressed.connect(back)
	v.add_child(b)
	v.move_child(b, 0)
	return v


static func _row(v: VBoxContainer, text: String) -> HBoxContainer:
	var h := HBoxContainer.new()
	var l := Label.new()
	l.text = text
	l.custom_minimum_size = Vector2(300, 0)
	l.add_theme_font_size_override("font_size", 20)
	h.add_child(l)
	v.add_child(h)
	return h


static func _slider(v: VBoxContainer, text: String, key: String, lo: float, hi: float, step: float) -> void:
	var h := _row(v, text)
	var sl := HSlider.new()
	sl.min_value = lo
	sl.max_value = hi
	sl.step = step
	sl.value = Settings.get(key)
	sl.custom_minimum_size = Vector2(240, 30)
	sl.value_changed.connect(func(val): Settings.set_value(key, val))
	h.add_child(sl)
