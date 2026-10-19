class_name DevicesPanel
extends RefCounted
## Explicit device ownership screen (REQ-INPUT-001/002). Shows what each player owns; each player can be given
## keyboard+mouse, the right-hand keyboard cluster or any connected controller. A device belongs to one player.


static func build(parent: Node, back: Callable) -> VBoxContainer:
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	parent.add_child(v)
	var b := Button.new()
	b.text = "Back"
	b.add_theme_font_size_override("font_size", 24)
	b.pressed.connect(back)
	v.add_child(b)
	var labels := []
	for p in 2:
		var l := Label.new()
		l.add_theme_font_size_override("font_size", 22)
		v.add_child(l)
		labels.append(l)
		var cycle := Button.new()
		cycle.text = "Change device for " + ["P1 Adrian", "P2 Noah"][p]
		cycle.add_theme_font_size_override("font_size", 22)
		cycle.pressed.connect(func(): _cycle(p))
		v.add_child(cycle)
	var auto := Button.new()
	auto.text = "Auto-detect (controllers first)"
	auto.add_theme_font_size_override("font_size", 22)
	auto.pressed.connect(func(): Devices.auto_assign())
	v.add_child(auto)
	var help := Label.new()
	help.text = "Keyboard+mouse: WASD move, mouse look, E interact, Alt jog, Shift sprint, Space jump, C crouch, R recover, X skip, Esc pause.\nKeyboard right: IJKL move, arrows look, O interact, U jog, H sprint, M jump, N crouch, Y recover, B skip, P pause.\nController: left stick move, right stick look, A interact, LB jog, L3/RT sprint, X jump, B crouch, Y recover, Back skip, Start pause."
	help.autowrap_mode = TextServer.AUTOWRAP_WORD
	help.custom_minimum_size = Vector2(580, 0)
	help.add_theme_font_size_override("font_size", 18)
	v.add_child(help)
	var refresh := func():
		for p in 2:
			if is_instance_valid(labels[p]):
				labels[p].text = "%s: %s" % [["P1 Adrian", "P2 Noah"][p], Devices.describe(p)]
	Devices.assignment_changed.connect(refresh)
	# the panel dies with its menu; stop listening so no freed label is ever written
	v.tree_exiting.connect(func(): if Devices.assignment_changed.is_connected(refresh): Devices.assignment_changed.disconnect(refresh))
	refresh.call()
	return v


static func _cycle(player: int) -> void:
	var options := [[Devices.Kind.KEYBOARD_MOUSE, -1], [Devices.Kind.KEYBOARD_RIGHT, -1]]
	for pad in Input.get_connected_joypads():
		options.append([Devices.Kind.JOYPAD, pad])
	var cur: Dictionary = Devices.owners[player]
	var at := 0
	for i in options.size():
		if options[i][0] == cur["kind"] and options[i][1] == cur["id"]:
			at = i
	var next: Array = options[(at + 1) % options.size()]
	Devices.assign(player, next[0], next[1])
