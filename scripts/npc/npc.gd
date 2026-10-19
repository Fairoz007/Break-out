class_name Npc
extends CharacterBody3D
## Non-player character on the level navmesh (REQ-NPC-001/002, REQ-ENV-008). Walks at blocking speed 1.2 m/s,
## holds its mark while it is speaking, and pauses during cinematics unless the cinematic is staging it.

signal arrived

var character := ""
var visual: CharacterVisual
var speaking := false
var speed := 1.2
var _path: PackedVector3Array = []
var _target := Vector3.INF
var _face_target := Vector3.INF
var cinematic_controlled := false


func setup(npc_name: String, character_key: String) -> Npc:
	name = npc_name
	character = character_key
	collision_layer = EnvBuilder.LAYER_NPC
	collision_mask = EnvBuilder.LAYER_WORLD
	var cs := CollisionShape3D.new()
	var cap := CapsuleShape3D.new()
	cap.radius = 0.3
	cap.height = 1.8
	cs.shape = cap
	cs.position.y = 0.9
	add_child(cs)
	visual = CharacterVisual.new().setup(character_key)
	add_child(visual)
	add_to_group("npcs")
	return self


func place(pos: Vector3, yaw_deg := 0.0) -> void:
	global_position = pos
	rotation_degrees.y = yaw_deg
	_path = []
	_target = Vector3.INF


func go_to(pos: Vector3, walk_speed := 1.2) -> void:
	speed = walk_speed
	_target = pos
	var map := get_world_3d().navigation_map
	_path = NavigationServer3D.map_get_path(map, global_position, pos, true)
	if _path.is_empty():
		_path = PackedVector3Array([pos])
	GameState.log_event("npc_move", {"npc": name, "to": [snappedf(pos.x, 0.1), snappedf(pos.y, 0.1), snappedf(pos.z, 0.1)], "path_points": _path.size()})


func is_moving() -> bool:
	return not _path.is_empty()


func stop() -> void:
	_path = []
	_target = Vector3.INF
	velocity = Vector3.ZERO


func face(pos: Vector3) -> void:
	_face_target = pos


func act(action: String, loop := false) -> void:
	visual.act(action, loop)


func paused() -> bool:
	return speaking or (GameState.cinematic_active and not cinematic_controlled)


func _physics_process(delta: float) -> void:
	velocity.y = 0.0 if is_on_floor() else velocity.y - 9.8 * delta
	if _path.is_empty() or paused():
		velocity.x = 0
		velocity.z = 0
		move_and_slide()
		_turn_to_face(delta)
		visual.locomote(0.0, false)
		return
	var next := _path[0]
	var to := Vector3(next.x - global_position.x, 0, next.z - global_position.z)
	if to.length() < 0.15:
		_path.remove_at(0)
		if _path.is_empty():
			velocity = Vector3.ZERO
			arrived.emit()
			GameState.log_event("npc_arrived", {"npc": name})
		return
	var v := to.normalized() * speed
	velocity.x = v.x
	velocity.z = v.z
	move_and_slide()
	rotation.y = lerp_angle(rotation.y, atan2(-v.x, -v.z), clampf(8.0 * delta, 0.0, 1.0))
	visual.locomote(speed, false)


func _turn_to_face(delta: float) -> void:
	if _face_target == Vector3.INF:
		return
	var d := _face_target - global_position
	if Vector2(d.x, d.z).length() > 0.05:
		rotation.y = lerp_angle(rotation.y, atan2(-d.x, -d.z), clampf(6.0 * delta, 0.0, 1.0))
