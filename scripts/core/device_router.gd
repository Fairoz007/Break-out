extends Node
## Explicit per-player device ownership (REQ-INPUT-001/002).
## Each player reads only its own device: keyboard+mouse, the right-hand keyboard cluster, or one joypad.
## Tests and the autopilot drive players through the same API by switching a player to the VIRTUAL device.

signal assignment_changed
signal device_lost(player: int)

enum Kind { KEYBOARD_MOUSE, KEYBOARD_RIGHT, JOYPAD, VIRTUAL, NONE }
const ACTIONS := ["interact", "sprint", "crouch", "pause", "recover", "skip"]

# player index (0 = P1 Adrian, 1 = P2 Noah) -> {kind, id}
var owners := [{"kind": Kind.KEYBOARD_MOUSE, "id": -1}, {"kind": Kind.KEYBOARD_RIGHT, "id": -1}]
var virtual_state := [_blank_virtual(), _blank_virtual()]
var _mouse_delta := Vector2.ZERO
var _pressed := [{}, {}]
var _just := [{}, {}]

const KEYS := {
	Kind.KEYBOARD_MOUSE: {"up": KEY_W, "down": KEY_S, "left": KEY_A, "right": KEY_D,
		"interact": KEY_E, "sprint": KEY_SHIFT, "crouch": KEY_C, "pause": KEY_ESCAPE, "recover": KEY_R, "skip": KEY_X,
		"look_left": KEY_Q, "look_right": KEY_Z},
	Kind.KEYBOARD_RIGHT: {"up": KEY_I, "down": KEY_K, "left": KEY_J, "right": KEY_L,
		"interact": KEY_O, "sprint": KEY_H, "crouch": KEY_N, "pause": KEY_P, "recover": KEY_Y, "skip": KEY_B,
		"look_left": KEY_LEFT, "look_right": KEY_RIGHT, "look_up": KEY_UP, "look_down": KEY_DOWN},
}
const JOY_BUTTONS := {"interact": JOY_BUTTON_A, "crouch": JOY_BUTTON_B, "sprint": JOY_BUTTON_LEFT_STICK,
	"pause": JOY_BUTTON_START, "recover": JOY_BUTTON_Y, "skip": JOY_BUTTON_BACK}


static func _blank_virtual() -> Dictionary:
	return {"move": Vector2.ZERO, "look": Vector2.ZERO, "buttons": {}}


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	process_priority = -100  # edge detection runs before gameplay reads it
	Input.joy_connection_changed.connect(_on_joy_changed)
	auto_assign()


## Default ownership: P1 keyboard+mouse; P2 first joypad, else right keyboard cluster.
func auto_assign() -> void:
	var pads := Input.get_connected_joypads()
	if pads.size() >= 2:
		owners = [{"kind": Kind.JOYPAD, "id": pads[0]}, {"kind": Kind.JOYPAD, "id": pads[1]}]
	elif pads.size() == 1:
		owners = [{"kind": Kind.KEYBOARD_MOUSE, "id": -1}, {"kind": Kind.JOYPAD, "id": pads[0]}]
	else:
		owners = [{"kind": Kind.KEYBOARD_MOUSE, "id": -1}, {"kind": Kind.KEYBOARD_RIGHT, "id": -1}]
	assignment_changed.emit()


func assign(player: int, kind: int, id := -1) -> void:
	# A device can belong to only one player.
	var other := 1 - player
	if owners[other]["kind"] == kind and owners[other]["id"] == id and kind != Kind.VIRTUAL:
		owners[other] = owners[player].duplicate()
	owners[player] = {"kind": kind, "id": id}
	assignment_changed.emit()


func set_virtual(player: int, enabled: bool) -> void:
	if enabled:
		owners[player] = {"kind": Kind.VIRTUAL, "id": -1}
	virtual_state[player] = _blank_virtual()


func describe(player: int) -> String:
	var o: Dictionary = owners[player]
	match o["kind"]:
		Kind.KEYBOARD_MOUSE: return "Keyboard + mouse (WASD, E interact)"
		Kind.KEYBOARD_RIGHT: return "Keyboard right (IJKL, O interact)"
		Kind.JOYPAD: return "Controller %d: %s" % [o["id"] + 1, Input.get_joy_name(o["id"])]
		Kind.VIRTUAL: return "Autopilot"
	return "Unassigned"


func prompt_key(player: int, action: String) -> String:
	var o: Dictionary = owners[player]
	match o["kind"]:
		Kind.KEYBOARD_MOUSE, Kind.KEYBOARD_RIGHT:
			return OS.get_keycode_string(KEYS[o["kind"]][action])
		Kind.JOYPAD:
			return {"interact": "A", "crouch": "B", "sprint": "L3", "pause": "Start", "recover": "Y", "skip": "Back"}[action]
	return action


func _input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and (owners[0]["kind"] == Kind.KEYBOARD_MOUSE or owners[1]["kind"] == Kind.KEYBOARD_MOUSE):
		if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
			_mouse_delta += event.relative


func _process(_delta: float) -> void:
	for p in 2:
		for a in ACTIONS:
			var now := _raw_pressed(p, a)
			_just[p][a] = now and not _pressed[p].get(a, false)
			_pressed[p][a] = now


func move(player: int) -> Vector2:
	var o: Dictionary = owners[player]
	var v := Vector2.ZERO
	match o["kind"]:
		Kind.KEYBOARD_MOUSE, Kind.KEYBOARD_RIGHT:
			var k: Dictionary = KEYS[o["kind"]]
			v = Vector2(float(Input.is_physical_key_pressed(k["right"])) - float(Input.is_physical_key_pressed(k["left"])),
				float(Input.is_physical_key_pressed(k["down"])) - float(Input.is_physical_key_pressed(k["up"])))
		Kind.JOYPAD:
			v = Vector2(Input.get_joy_axis(o["id"], JOY_AXIS_LEFT_X), Input.get_joy_axis(o["id"], JOY_AXIS_LEFT_Y))
			if v.length() < 0.2:
				v = Vector2.ZERO
		Kind.VIRTUAL:
			v = virtual_state[player]["move"]
	return v.limit_length(1.0)


## Camera look delta for this frame, in radians.
func look(player: int, delta: float) -> Vector2:
	var o: Dictionary = owners[player]
	var v := Vector2.ZERO
	match o["kind"]:
		Kind.KEYBOARD_MOUSE:
			v = _mouse_delta * 0.0035
			_mouse_delta = Vector2.ZERO
			var k: Dictionary = KEYS[o["kind"]]
			v.x += (float(Input.is_physical_key_pressed(k["look_right"])) - float(Input.is_physical_key_pressed(k["look_left"]))) * 2.2 * delta
		Kind.KEYBOARD_RIGHT:
			var k: Dictionary = KEYS[o["kind"]]
			v = Vector2(float(Input.is_physical_key_pressed(k["look_right"])) - float(Input.is_physical_key_pressed(k["look_left"])),
				float(Input.is_physical_key_pressed(k["look_down"])) - float(Input.is_physical_key_pressed(k["look_up"]))) * 2.2 * delta
		Kind.JOYPAD:
			var s := Vector2(Input.get_joy_axis(o["id"], JOY_AXIS_RIGHT_X), Input.get_joy_axis(o["id"], JOY_AXIS_RIGHT_Y))
			if s.length() > 0.15:
				v = s * 2.6 * delta
		Kind.VIRTUAL:
			v = virtual_state[player]["look"]
	v *= Settings.camera_sensitivity[player]
	if Settings.invert_y[player]:
		v.y = -v.y
	return v


func pressed(player: int, action: String) -> bool:
	return _pressed[player].get(action, false)


func just_pressed(player: int, action: String) -> bool:
	return _just[player].get(action, false)


func _raw_pressed(player: int, action: String) -> bool:
	var o: Dictionary = owners[player]
	match o["kind"]:
		Kind.KEYBOARD_MOUSE, Kind.KEYBOARD_RIGHT:
			return Input.is_physical_key_pressed(KEYS[o["kind"]][action])
		Kind.JOYPAD:
			if action == "sprint" and Input.get_joy_axis(o["id"], JOY_AXIS_TRIGGER_RIGHT) > 0.5:
				return true
			return Input.is_joy_button_pressed(o["id"], JOY_BUTTONS[action])
		Kind.VIRTUAL:
			return virtual_state[player]["buttons"].get(action, false)
	return false


func _on_joy_changed(device: int, connected: bool) -> void:
	if connected:
		return
	for p in 2:
		if owners[p]["kind"] == Kind.JOYPAD and owners[p]["id"] == device:
			device_lost.emit(p)
