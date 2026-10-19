class_name GuardAI
extends Npc
## Bounded deterministic patrol with attention and line-of-sight detection (REQ-GUARD-001..003).
## Patrol is a fixed loop of waypoints and holds; its phase is serialisable so checkpoints restore it exactly.
## Detection needs the player inside the flashlight cone, within range, with an unobstructed ray to the body.

signal warning(player: int, level: float)
signal detected(player: int)

var waypoints: Array = []       # [{"pos": Vector3, "wait": float}]
var patrol_index := 0
var wait_left := 0.0
var patrolling := false
var detection := [0.0, 0.0]
var detect_seconds := 1.5
var view_range := 9.0
var view_angle_deg := 32.0
var detection_enabled := false
var flashlight: SpotLight3D
var _attention := Vector3.INF
var _attention_left := 0.0


func setup_guard(npc_name: String, character_key := "GUARD", torch := false) -> GuardAI:
	setup(npc_name, character_key)
	if torch:
		flashlight = SpotLight3D.new()
		flashlight.name = "Flashlight"
		flashlight.position = Vector3(0.2, 1.35, -0.3)
		flashlight.rotation_degrees.x = -12.0
		flashlight.spot_range = view_range + 1.0
		flashlight.spot_angle = view_angle_deg
		flashlight.light_energy = 6.0
		flashlight.light_color = Color(1.0, 0.95, 0.82)
		flashlight.shadow_enabled = true
		add_child(flashlight)
	return self


func start_patrol(points: Array, from_index := 0, waited := 0.0) -> void:
	waypoints = points
	patrol_index = from_index % points.size()
	patrolling = true
	wait_left = waited
	if wait_left <= 0.0:
		go_to(waypoints[patrol_index]["pos"], 1.2)


func patrol_state() -> Dictionary:
	return {"index": patrol_index, "wait": wait_left, "pos": [global_position.x, global_position.y, global_position.z], "yaw": rotation.y}


func restore_patrol(state: Dictionary) -> void:
	place(Vector3(state["pos"][0], state["pos"][1], state["pos"][2]), rad_to_deg(state["yaw"]))
	start_patrol(waypoints, int(state["index"]), float(state["wait"]))


## Authored distraction: look at / walk toward a point for a while, then resume the loop (never a fail state).
func investigate(pos: Vector3, seconds := 6.0, walk := false) -> void:
	_attention = pos
	_attention_left = seconds
	face(pos)
	if walk:
		go_to(pos, 1.2)
	else:
		stop()
	GameState.log_event("guard_attention", {"guard": name, "seconds": seconds})


func back_turned_to(pos: Vector3) -> bool:
	var fwd := -global_transform.basis.z
	var to := (pos - global_position)
	to.y = 0
	return fwd.dot(to.normalized()) < -0.2


func _physics_process(delta: float) -> void:
	super._physics_process(delta)
	if paused():
		return
	if _attention_left > 0.0:
		_attention_left -= delta
		if _attention_left <= 0.0:
			_attention = Vector3.INF
			_face_target = Vector3.INF
			if patrolling:
				go_to(waypoints[patrol_index]["pos"], 1.2)
	elif patrolling and _path.is_empty():
		if wait_left > 0.0:
			wait_left -= delta
			if wait_left <= 0.0:
				patrol_index = (patrol_index + 1) % waypoints.size()
				go_to(waypoints[patrol_index]["pos"], 1.2)
		else:
			wait_left = float(waypoints[patrol_index].get("wait", 0.0)) + 0.001
			var look_at_pos = waypoints[patrol_index].get("look", null)
			if look_at_pos != null:
				face(look_at_pos)
	if detection_enabled:
		_update_detection(delta)


func can_see(p: Player) -> bool:
	var eye := global_position + Vector3.UP * 1.6
	var target := p.global_position + Vector3.UP * (0.7 if p.crouched else 1.2)
	var to := target - eye
	if to.length() > view_range:
		return false
	var fwd := -global_transform.basis.z
	if rad_to_deg(fwd.angle_to(Vector3(to.x, 0, to.z).normalized())) > view_angle_deg:
		return false
	var q := PhysicsRayQueryParameters3D.create(eye, target, EnvBuilder.LAYER_WORLD | EnvBuilder.LAYER_PLAYER)
	q.exclude = [get_rid()]
	var hit := get_world_3d().direct_space_state.intersect_ray(q)
	return not hit.is_empty() and hit["collider"] == p


func _update_detection(delta: float) -> void:
	for p in get_tree().get_nodes_in_group("players"):
		var pl: Player = p
		var before: float = detection[pl.index]
		if can_see(pl):
			detection[pl.index] = min(1.0, before + delta / detect_seconds)
		else:
			detection[pl.index] = max(0.0, before - delta * 0.5)
		if detection[pl.index] > 0.0 and before == 0.0:
			GameState.log_event("guard_warning", {"guard": name, "player": pl.index})
		warning.emit(pl.index, detection[pl.index])
		if detection[pl.index] >= 1.0 and before < 1.0:
			GameState.log_event("guard_detected", {"guard": name, "player": pl.index})
			detected.emit(pl.index)
