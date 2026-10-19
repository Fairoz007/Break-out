extends Node
## Automated two-player driver for verification runs (REQ-TEST-001/002). It owns both players' VIRTUAL devices
## and produces only stick and button input, exactly like a controller: no teleporting, no direct state writes.
## It reads what a human would read: ready prompts, the HUD guide marker, and enabled interaction points.
## Args (after --): --autopilot --mission=N --until=N --report=path --timeout=s --shots=dir --skip-cinematics
##                  --chaos (simulate wrong actions: early lever release, wrong selector, detection, solo attempts)

var chapter: ChapterRoot
var args := {}
var _pulse := [{}, {}]
var _path := [PackedVector3Array(), PackedVector3Array()]
var _path_target := [Vector3.INF, Vector3.INF]
var _replan := [0.0, 0.0]
var _stuck_t := [0.0, 0.0]
var _last_pos := [Vector3.ZERO, Vector3.ZERO]
var _start_msec := 0
var _done := false
var _shots_dir := ""
var _shot_queue: Array = []
var _shot_count := 0
var _mission_times := {}
var _fps_samples := {}
var _chaos := ""
var _chaos_done := {}
var _hesitate := {}   # item id -> time first targeted (idle chaos)


func _ready() -> void:
	process_priority = -200   # before DeviceRouter edge detection
	process_mode = Node.PROCESS_MODE_ALWAYS
	Devices.set_virtual(0, true)
	Devices.set_virtual(1, true)
	_start_msec = Time.get_ticks_msec()
	if args.has("speed"):
		Engine.time_scale = float(args["speed"])
	_chaos = str(args.get("chaos", ""))
	_shots_dir = str(args.get("shots", ""))
	if _shots_dir != "":
		DirAccess.make_dir_recursive_absolute(_shots_dir)
	GameState.event_logged.connect(_on_event)
	chapter.chapter_completed.connect(func(): _finish("chapter_complete"))
	print("AUTOPILOT start args=", args)


func _on_event(kind: String, e: Dictionary) -> void:
	if kind == "mission_loaded":
		_mission_times[e["mission"]] = {"start": e["t"]}
	if kind == "mission_complete":
		_mission_times.get(e["mission"], {})["end"] = e["t"]
		if args.has("until") and int(args["until"]) == int(e["mission"]):
			call_deferred("_finish", "until_reached")
	if _shots_dir != "" and kind in ["shot_activated", "objective_set", "mission_loaded", "checkpoint", "ready_request", "guard_warning", "cinematic_end", "door", "hold_started"]:
		_shot_queue.append({"label": "%s_%s" % [kind, e.get("id", e.get("checkpoint", e.get("door", e.get("where", str(e.get("mission", "")))))) ], "delay": 0.6 if kind == "shot_activated" else 0.35})


func _process(delta: float) -> void:
	if _done or chapter == null or not is_instance_valid(chapter):
		return
	var limit := float(args.get("timeout", 3600))
	if (Time.get_ticks_msec() - _start_msec) / 1000.0 * Engine.time_scale > limit and not args.has("fixed"):
		_finish("timeout_real", {"real": (Time.get_ticks_msec() - _start_msec) / 1000.0, "limit": limit})
		return
	if chapter.mission == null and not chapter.transitioning and (Time.get_ticks_msec() - _start_msec) > 20000:
		_finish("mission_load_failed")
		return
	if chapter.mission and chapter.mission.now() > limit:
		_finish("timeout_game", {"game": chapter.mission.now(), "limit": limit})
		return
	_capture(delta)
	_sample_fps(delta)
	if get_tree().paused or chapter.mission == null or chapter.transitioning:
		for p in 2:
			Devices.virtual_state[p]["move"] = Vector2.ZERO
		return
	for p in 2:
		_drive(p, delta)


func _press(p: int, action: String, want: bool) -> void:
	# Edge-pressing: a press is down for one frame, then released, like a quick button tap.
	# Alternates down/up every frame while wanted, so consecutive prompts each receive a fresh press edge.
	var btn: Dictionary = Devices.virtual_state[p]["buttons"]
	if want:
		var down: bool = not _pulse[p].get(action, false)
		btn[action] = down
		_pulse[p][action] = down
	else:
		btn[action] = false
		_pulse[p][action] = false


func _hold(p: int, action: String, down: bool) -> void:
	Devices.virtual_state[p]["buttons"][action] = down
	_pulse[p][action] = down


func _drive(p: int, delta: float) -> void:
	var pl: Player = chapter.players[p]
	var m: Mission = chapter.mission
	var vs: Dictionary = Devices.virtual_state[p]
	vs["move"] = Vector2.ZERO
	vs["look"] = Vector2.ZERO
	if GameState.cinematic_active:
		_press(p, "interact", false)
		_press(p, "skip", args.has("skip-cinematics"))
		return
	var hud: PlayerHud = chapter.huds[p]
	if hud.ready_requested and not hud.ready_confirmed:
		_press(p, "interact", true)
		return
	# stealth posture requested by the mission (a HUD hint for players too)
	var want_crouch: bool = m.get_meta("crouch_p%d" % p, false)
	_press(p, "crouch", want_crouch != pl.crouched)
	if pl.holding:
		var keep: bool = pl.holding.enabled and not pl.holding.get_meta("release_p%d" % p, false)
		if _chaos == "mistakes":
			keep = keep and not _mistake_release(pl.holding, m)
		_hold(p, "interact", keep)
		return
	if _chaos == "mistakes" and _mistake_detect(p, pl, m, delta):
		return
	var target := _pick_item(p, pl, m)
	if target and _chaos == "idle" and target.uses == 0 and target.mode != Interactable.Mode.HOLD_COMPLETE:
		# hesitate before the first use of every interaction so idle/reminder lines get their chance
		if not _hesitate.has(target.id):
			_hesitate[target.id] = m.now()
		if m.now() - _hesitate[target.id] < (32.0 if p == 0 else 45.0):
			_press(p, "interact", false)
			return
	if _chaos == "mistakes" and m.index == 5 and p == 0 and not _chaos_done.has("wrong_selector"):
		if GameState.events.any(func(e): return e["kind"] == "breaker_trip"):
			_chaos_done["wrong_selector"] = true
		elif m.items["m05_selector"].enabled:
			target = m.items["m05_selector"] if m.selector != 1 else m.items["m05_power"]
	if target:
		var d := _flat_dist(pl.global_position, target.global_position)
		if d <= target.radius - 0.25 and pl.focus == target:
			if target.mode == Interactable.Mode.PRESS:
				_press(p, "interact", true)
			else:
				_hold(p, "interact", true)
			return
		_press(p, "interact", false)
		# close in further when a neighbouring interaction currently has focus
		var stop := target.radius - 0.4 if (pl.focus == null or pl.focus == target) else 0.1
		_steer(p, pl, target.global_position, delta, stop)
		return
	_press(p, "interact", false)
	if not m.guide[p].is_empty():
		_steer(p, pl, m.guide[p]["pos"], delta, 0.35)


## Deliberate mistakes (verification of retry paths); each fires once.
func _mistake_release(it: Interactable, m: Mission) -> bool:
	if it.id == "m02_mediate" and not _chaos_done.has("m02") and m.items["m02_ball"].enabled:
		_chaos_done["m02"] = true
		return true
	if it.id == "m03_lever" and not _chaos_done.has("m03") and m.items["m03_screen"].progress > 0.3:
		_chaos_done["m03"] = true
		return true
	return false


func _mistake_detect(p: int, pl: Player, m: Mission, delta: float) -> bool:
	if p != 0 or m.index != 4 or _chaos_done.has("m04") or GameState.current_objective != "CH01_M04_OBJ003":
		return false
	if GameState.events.any(func(e): return e["kind"] == "detected_fail"):
		_chaos_done["m04"] = true
		return false
	var g: Node3D = m.npcs["Guard"]
	_steer(p, pl, g.global_position + (-g.global_transform.basis.z) * 4.0, delta, 0.5)
	return true


func _pick_item(p: int, pl: Player, m: Mission) -> Interactable:
	var best: Interactable = null
	var best_d := INF
	for id in m.items:
		var it: Interactable = m.items[id]
		if not it.enabled or not it.get_meta("ready_now", true):
			continue
		if it.allowed != Interactable.ANY and it.allowed != p:
			continue
		if it.allowed == Interactable.ANY and int(it.get_meta("autopilot_player", 0)) != p:
			continue
		if it.mode == Interactable.Mode.PRESS and it.get_meta("once", true) and it.uses > 0:
			continue
		if it.holder != -1 and it.holder != p:
			continue
		var d := _flat_dist(pl.global_position, it.global_position)
		if d < best_d:
			best = it
			best_d = d
	return best


func _flat_dist(a: Vector3, b: Vector3) -> float:
	return Vector2(a.x - b.x, a.z - b.z).length()


func _steer(p: int, pl: Player, target: Vector3, delta: float, stop_r: float) -> void:
	var pos := pl.global_position
	if _flat_dist(pos, target) <= max(stop_r, 0.2):
		Devices.virtual_state[p]["move"] = Vector2.ZERO
		return
	_replan[p] -= delta
	if _replan[p] <= 0.0 or _path_target[p].distance_to(target) > 0.3 or _path[p].is_empty():
		var map := pl.get_world_3d().navigation_map
		if NavigationServer3D.map_get_iteration_id(map) == 0:
			return
		var start := NavigationServer3D.map_get_closest_point(map, pos)
		var goal := NavigationServer3D.map_get_closest_point(map, target)
		_path[p] = NavigationServer3D.map_get_path(map, start, goal, true)
		if _path[p].is_empty():
			_path[p] = PackedVector3Array([target])
		elif _flat_dist(goal, target) > 0.3:
			_path[p].append(target)
		_path_target[p] = target
		_replan[p] = 0.5
	var next := target
	while _path[p].size() > 0:
		next = _path[p][0]
		if _flat_dist(pos, next) < 0.35 and _path[p].size() > 1:
			_path[p].remove_at(0)
		else:
			break
	var dir := Vector3(next.x - pos.x, 0, next.z - pos.z)
	if dir.length() < 0.01:
		return
	var stick := dir.normalized().rotated(Vector3.UP, -pl.rig.yaw)
	Devices.virtual_state[p]["move"] = Vector2(stick.x, stick.z)
	# turn the camera gently toward travel so screenshots look where the player goes
	var want_yaw := atan2(-dir.x, -dir.z)
	Devices.virtual_state[p]["look"] = Vector2(-wrapf(want_yaw - pl.rig.yaw, -PI, PI) * clampf(2.5 * delta, 0.0, 1.0), 0.0)
	# stuck handling: nudge sideways, then use the player's own recover action
	if pos.distance_to(_last_pos[p]) < 0.02:
		_stuck_t[p] += delta
		if _stuck_t[p] > 1.5:
			Devices.virtual_state[p]["move"] = Vector2(stick.z, -stick.x)
		if _stuck_t[p] > 6.0:
			GameState.log_event("autopilot_stuck", {"player": p, "pos": [pos.x, pos.y, pos.z], "target": [target.x, target.y, target.z]})
			_stuck_t[p] = 0.0
			_replan[p] = 0.0
	else:
		_stuck_t[p] = 0.0
	_last_pos[p] = pos


func _sample_fps(delta: float) -> void:
	if chapter.mission == null or delta <= 0.0:
		return
	var key := str(chapter.mission.index)
	if not _fps_samples.has(key):
		_fps_samples[key] = []
	_fps_samples[key].append(1.0 / delta)


func _capture(delta: float) -> void:
	if _shots_dir == "" or DisplayServer.get_name() == "headless" or _shot_queue.is_empty():
		return
	_shot_queue[0]["delay"] -= delta
	if _shot_queue[0]["delay"] > 0.0:
		return
	var s: Dictionary = _shot_queue.pop_front()
	_shot_count += 1
	var img := get_viewport().get_texture().get_image()
	var safe_label: String = str(s["label"]).replace("/", "_").replace(" ", "_").replace(":", "_")
	img.save_png("%s/%04d_%s.png" % [_shots_dir, _shot_count, safe_label.left(80)])


func _finish(reason: String, detail := {}) -> void:
	if _done:
		return
	_done = true
	var fps := {}
	for k in _fps_samples:
		var arr: Array = _fps_samples[k]
		arr.sort()
		var avg := 0.0
		for v in arr:
			avg += v
		fps[k] = {"avg": avg / max(arr.size(), 1), "p1_low": arr[int(arr.size() * 0.01)] if arr.size() > 0 else 0.0, "frames": arr.size()}
	var game_times := {}
	for e in GameState.events:
		if e["kind"] == "mission_complete":
			game_times[str(e["mission"])] = e.get("game_seconds", 0.0)
	var report := {"reason": reason, "detail": detail, "mission_game_seconds": game_times, "real_seconds": (Time.get_ticks_msec() - _start_msec) / 1000.0,
		"game_seconds": chapter.mission.now() if chapter and chapter.mission else 0.0, "args": args,
		"renderer": DisplayServer.get_name(), "missions": _mission_times, "fps": fps, "screenshots": _shot_count,
		"final_state": {"players": chapter.players.map(func(pl): return [snappedf(pl.global_position.x, 0.01), snappedf(pl.global_position.y, 0.01), snappedf(pl.global_position.z, 0.01)]) if chapter else [],
			"guides": chapter.mission.guide if chapter and chapter.mission else [], "mission": GameState.mission_index, "checkpoint": GameState.checkpoint_id, "inventory": GameState.inventory,
			"knowledge": GameState.knowledge, "objectives_completed": GameState.completed_objectives.keys()},
		"events": GameState.events}
	var path := str(args.get("report", "user://autopilot_report.json"))
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(report, "\t"))
		f.close()
	print("AUTOPILOT finished: ", reason, " real=", report["real_seconds"], "s report=", path)
	get_tree().quit(0 if reason in ["chapter_complete", "until_reached"] else 2)
