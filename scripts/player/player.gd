class_name Player
extends CharacterBody3D
## Third-person cooperative player (REQ-MOVE-001, REQ-COOP-001/002/005).
## Reads its owned device only. Walk, jog and sprint have distinct speeds; crouch checks headroom.

signal interacted(interactable: Interactable)

const WALK := 1.5
const JOG := 3.4
const SPRINT := 5.2
const JUMP_SPEED := 4.4
const STANDING_HEIGHT := 1.8
const CROUCH_HEIGHT := 1.1
const BODY_MASK := EnvBuilder.LAYER_WORLD | EnvBuilder.LAYER_PLAYER | EnvBuilder.LAYER_NPC
const CROUCH := 0.8
const ACCEL := 10.0
const GRAVITY := 9.8
const INTERACT_HEIGHT := 1.6

var body_shape: CollisionShape3D
var index := 0
var character := "ADRIAN"
var visual: CharacterVisual
var rig: PlayerCamera
var crouched := false
var input_locked := false       # cinematics / scripted traversal
var focus: Interactable = null  # best interaction in reach this frame
var holding: Interactable = null
var safe_point := Transform3D.IDENTITY
var _hold_toggled := false
var _scripted_path: Array = []
var _scripted_speed := 1.0
var _scripted_done := Callable()


func setup(player_index: int, character_key: String) -> Player:
	index = player_index
	character = character_key
	name = "P%d_%s" % [index + 1, character_key.capitalize()]
	collision_layer = EnvBuilder.LAYER_PLAYER
	collision_mask = EnvBuilder.LAYER_WORLD | EnvBuilder.LAYER_PLAYER | EnvBuilder.LAYER_NPC
	floor_snap_length = 0.4
	var cs := CollisionShape3D.new()
	body_shape = cs
	var cap := CapsuleShape3D.new()
	cap.radius = 0.3
	cap.height = 1.8
	cs.shape = cap
	cs.position.y = 0.9
	add_child(cs)
	visual = CharacterVisual.new().setup(character_key)
	add_child(visual)
	add_to_group("players")
	return self


func place(xf: Transform3D) -> void:
	_cancel_traversal()
	_release_hold()
	global_transform = Transform3D(Basis(Vector3.UP, xf.basis.get_euler().y), xf.origin)
	velocity = Vector3.ZERO
	safe_point = global_transform
	if rig:
		rig.snap_behind(self)


func yaw() -> float:
	return global_rotation.y


func _physics_process(delta: float) -> void:
	if _scripted_path.size() > 0:
		_run_scripted(delta)
		return
	var move := Vector2.ZERO if input_locked else Devices.move(index)
	if not input_locked and Devices.just_pressed(index, "crouch"):
		set_crouched(not crouched)
	var speed := WALK
	if crouched:
		speed = CROUCH
	elif not input_locked and Devices.pressed(index, "sprint"):
		speed = SPRINT
	elif not input_locked and Devices.pressed(index, "run"):
		speed = JOG
	# Restored checkpoint crouch state must also update the collision body.
	_update_capsule()
	var cam_yaw := rig.yaw if rig else 0.0
	var dir := Vector3(move.x, 0, move.y).rotated(Vector3.UP, cam_yaw)
	var target := dir * speed
	var hv := Vector3(velocity.x, 0, velocity.z).move_toward(target, ACCEL * speed * delta)
	velocity.x = hv.x
	velocity.z = hv.z
	velocity.y = 0.0 if is_on_floor() else velocity.y - GRAVITY * delta
	if not input_locked and not holding and is_on_floor() and Devices.just_pressed(index, "jump"):
		if not crouched or set_crouched(false):
			velocity.y = JUMP_SPEED
	move_and_slide()
	if hv.length() > 0.1:
		rotation.y = lerp_angle(rotation.y, atan2(-hv.x, -hv.z), clampf(12.0 * delta, 0.0, 1.0))
	visual.locomote(Vector3(velocity.x, 0, velocity.z).length(), crouched, is_on_floor(), velocity.y)
	if global_position.y < -15.0:
		recover()
	if input_locked:
		_release_hold()
		focus = null
		return
	if Devices.just_pressed(index, "recover"):
		recover()
	_update_interaction(delta)


func _update_interaction(delta: float) -> void:
	if holding:
		var still := Devices.pressed(index, "interact")
		if Settings.hold_toggle:
			if Devices.just_pressed(index, "interact"):
				_hold_toggled = not _hold_toggled
			still = _hold_toggled
		if holding.global_position.distance_to(global_position) > holding.radius + 0.8:
			still = false
		holding.hold_update(index, still, delta)
		if holding.holder != index:
			holding = null
			_hold_toggled = false
			visual.stop_action()
		return
	focus = _find_focus()
	if focus and Devices.just_pressed(index, "interact"):
		if focus.press(index):
			interacted.emit(focus)
			if focus.mode != Interactable.Mode.PRESS and focus.holder == index:
				holding = focus
				_hold_toggled = true
				visual.act("Push", true)
			else:
				visual.act("Interact")


func _find_focus() -> Interactable:
	var best: Interactable = null
	var best_d := INF
	for n in get_tree().get_nodes_in_group("interactables"):
		var it: Interactable = n
		if not it.is_inside_tree() or not it.enabled or not (it.allowed == Interactable.ANY or it.allowed == index):
			continue
		var d3 := it.global_position - global_position
		if absf(d3.y - 0.9) > INTERACT_HEIGHT:
			continue
		var d := Vector2(d3.x, d3.z).length()
		if d <= it.radius and d < best_d:
			best = it
			best_d = d
	return best


func _release_hold() -> void:
	if holding:
		holding.release(index)
		holding = null
		visual.stop_action()


## Recover-stuck: return to the last safe mark (no death volumes anywhere).
func recover() -> void:
	_release_hold()
	_cancel_traversal()
	global_transform = safe_point
	if rig:
		rig.snap_behind(self)
	velocity = Vector3.ZERO
	GameState.log_event("recover", {"player": index})


## Scripted traversal (hatch crawl, ladder): move through points with collision off, then hand control back.
func traverse(points: Array, speed := 0.8, action := "crawl", done := Callable()) -> void:
	_release_hold()
	_scripted_path = points.duplicate()
	_scripted_speed = speed
	_scripted_done = done
	collision_mask = 0
	visual.act(action, true)
	GameState.log_event("traverse_start", {"player": index, "action": action})


func is_traversing() -> bool:
	return _scripted_path.size() > 0


func _run_scripted(delta: float) -> void:
	var target: Vector3 = _scripted_path[0]
	var to := target - global_position
	var step := _scripted_speed * delta
	if to.length() <= step:
		global_position = target
		_scripted_path.pop_front()
		if _scripted_path.is_empty():
			collision_mask = EnvBuilder.LAYER_WORLD | EnvBuilder.LAYER_PLAYER | EnvBuilder.LAYER_NPC
			visual.stop_action()
			safe_point = global_transform
			GameState.log_event("traverse_end", {"player": index})
			if _scripted_done.is_valid():
				_scripted_done.call()
		return
	global_position += to.normalized() * step
	var flat := Vector3(to.x, 0, to.z)
	if flat.length() > 0.01:
		rotation.y = atan2(-flat.x, -flat.z)


func _cancel_traversal() -> void:
	_scripted_path.clear()
	_scripted_done = Callable()
	collision_mask = BODY_MASK
	if visual:
		visual.stop_action()


func _update_capsule() -> void:
	if body_shape:
		var height := CROUCH_HEIGHT if crouched else STANDING_HEIGHT
		if not is_equal_approx((body_shape.shape as CapsuleShape3D).height, height):
			(body_shape.shape as CapsuleShape3D).height = height
			body_shape.position.y = height * 0.5


## Preserve the feet position; standing is rejected while a ceiling occupies headroom.
func set_crouched(want: bool) -> bool:
	if not want and crouched and is_inside_tree():
		var shape := CapsuleShape3D.new()
		shape.radius = 0.29
		shape.height = STANDING_HEIGHT - 0.04
		var q := PhysicsShapeQueryParameters3D.new()
		q.shape = shape
		q.transform = Transform3D(global_basis, global_position + Vector3.UP * (STANDING_HEIGHT * 0.5 + 0.02))
		q.collision_mask = BODY_MASK
		q.exclude = [get_rid()]
		if not get_world_3d().direct_space_state.intersect_shape(q, 1).is_empty():
			return false
	crouched = want
	_update_capsule()
	return true
