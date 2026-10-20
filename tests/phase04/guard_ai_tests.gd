extends Node
## Phase 04 guard AI tests in the real Mission 04 cell block (night): hearing, silent crouch, independent per-player
## detection, the suspicious -> search -> patrol loop, and walls blocking sight. Players are driven through the
## virtual devices (real movement), not teleported while being judged.
## godot --headless --fixed-fps 60 --path . res://tests/phase04/guard_ai_tests.tscn

var chapter: ChapterRoot
var results := []


func _ready() -> void:
	_run.call_deferred()


func _run() -> void:
	for t in ["hearing_sprint_behind", "crouch_walk_silent", "independent_detection", "search_then_return", "wall_blocks_sight", "alert_chase"]:
		var r: String = await call("t_" + t)
		results.append({"test": t, "pass": r == "", "detail": r})
		print("TEST ", t, " ", "PASS" if r == "" else "FAIL: " + r)
		await _reset()
	var failed := results.filter(func(x): return not x["pass"]).size()
	var f := FileAccess.open("res://tests/phase04/evidence/guard_ai_tests.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"passed": results.size() - failed, "failed": failed, "results": results}, "\t"))
	f.close()
	print("GUARD AI TESTS: %d passed, %d failed" % [results.size() - failed, failed])
	get_tree().quit(1 if failed > 0 else 0)


func _reset() -> void:
	for p in 2:
		Devices.virtual_state[p]["move"] = Vector2.ZERO
		Devices.virtual_state[p]["buttons"] = {}
	if chapter:
		chapter.queue_free()
		chapter = null
	await get_tree().process_frame


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


## Mission 04 after the count, guard standing still at (44,-6) looking east, detection on; both players placed.
func _setup(p0: Vector3, p1: Vector3) -> GuardAI:
	chapter = ChapterRoot.new()
	add_child(chapter)
	Devices.set_virtual(0, true)
	Devices.set_virtual(1, true)
	chapter.continue_game(CanonStates.entry_snapshot(4))
	await _frames(20)
	var m: Mission = chapter.mission
	m.commit("count")
	var g: GuardAI = m.npcs["Guard"]
	g.patrolling = false
	g.stop()
	g.place(Vector3(44.0, 0, -6.0), 270.0)
	g.face(Vector3(50.0, 1.0, -6.0))
	g.detection = [0.0, 0.0]
	g.detection_enabled = true
	chapter.players[0].place(Transform3D(Basis(), p0))
	chapter.players[1].place(Transform3D(Basis(), p1))
	await _frames(5)
	return g


func _events(kind: String, since: int) -> Array:
	return GameState.events.slice(since).filter(func(e): return e["kind"] == kind)


func t_hearing_sprint_behind() -> String:
	var g := await _setup(Vector3(39.5, 0.05, -6.0), Vector3(40.5, 0.05, -1.0))
	var since := GameState.events.size()
	Devices.virtual_state[0]["move"] = Vector2(0, 1)       # camera-relative; any direction works for speed
	Devices.virtual_state[0]["buttons"] = {"sprint": true}
	await _frames(45)
	Devices.virtual_state[0]["move"] = Vector2.ZERO
	Devices.virtual_state[0]["buttons"] = {}
	if _events("guard_heard", since).is_empty():
		return "no guard_heard while sprinting %.1f m behind (speed %.1f)" % [g.global_position.distance_to(chapter.players[0].global_position), Vector2(chapter.players[0].velocity.x, chapter.players[0].velocity.z).length()]
	if g.alert_state == GuardAI.Alert.PATROL:
		return "heard but stayed in PATROL"
	return ""


func t_crouch_walk_silent() -> String:
	var g := await _setup(Vector3(40.5, 0.05, -6.0), Vector3(40.5, 0.05, -1.0))
	var since := GameState.events.size()
	Devices.virtual_state[0]["buttons"] = {"crouch": true}
	await _frames(2)
	Devices.virtual_state[0]["buttons"] = {}
	await _frames(10)
	if not chapter.players[0].crouched:
		return "player did not crouch"
	Devices.virtual_state[0]["move"] = Vector2(0, 1)
	await _frames(90)
	Devices.virtual_state[0]["move"] = Vector2.ZERO
	if not _events("guard_heard", since).is_empty():
		return "crouch-walk was heard"
	return ""


func t_independent_detection() -> String:
	# P1 in plain view 5 m in front; P2 far behind the guard. Only P1's meter may rise.
	var g := await _setup(Vector3(49.0, 0.05, -6.0), Vector3(34.0, 0.05, -6.0))
	await _frames(40)
	if g.detection[0] <= 0.2:
		return "visible P1 detection only %.2f" % g.detection[0]
	if g.detection[1] > 0.0:
		return "P2 behind the guard gained detection %.2f" % g.detection[1]
	return ""


func t_search_then_return() -> String:
	var g := await _setup(Vector3(49.0, 0.05, -6.0), Vector3(40.5, 0.05, -1.0))
	g.waypoints = [{"pos": Vector3(44.0, 0, -6.0), "wait": 30.0}]
	g.patrol_index = 0
	g.patrolling = true
	g.wait_left = 30.0
	var since := GameState.events.size()
	await _frames(40)                                        # partial sighting (~0.45 of 1.5 s)
	chapter.players[0].place(Transform3D(Basis(), Vector3(37.5, 0.05, -1.0)))   # duck into cell 13, out of sight
	for i in 60 * 20:
		await get_tree().physics_frame
		if not _events("guard_return", since).is_empty():
			break
	var kinds := GameState.events.slice(since).map(func(e): return e["kind"])
	if not kinds.has("guard_suspicious"):
		return "no SUSPICIOUS on a partial sighting"
	if not kinds.has("guard_search"):
		return "no SEARCH after losing sight"
	if not kinds.has("guard_return"):
		return "never returned to patrol (state %d)" % g.alert_state
	if kinds.has("guard_detected"):
		return "a partial sighting escalated to detection"
	return ""


func t_wall_blocks_sight() -> String:
	# P1 inside cell 13 behind the solid divider/rear wall, within range of a guard looking straight at it.
	var g := await _setup(Vector3(37.5, 0.05, 2.4), Vector3(40.5, 0.05, -1.0))
	g.place(Vector3(37.5, 0, -6.0), 180.0)
	g.face(Vector3(37.5, 1.0, 3.0))
	chapter.players[0].place(Transform3D(Basis(), Vector3(34.0, 0.05, 0.5)))    # cell A-12, behind the 36 m divider
	await _frames(60)
	if g.can_see(chapter.players[0]):
		return "guard sees through the cell divider"
	return ""


func t_alert_chase() -> String:
	# Full sighting: detection reaches 1.0 -> ALERT and the guard closes on the player (missions decide the outcome).
	var g := await _setup(Vector3(49.0, 0.05, -6.0), Vector3(40.5, 0.05, -1.0))
	# Mission 04 turns detection into its canonical retry (stop + reload); judge the guard's own reaction here.
	var m: Mission = chapter.mission
	if g.detected.is_connected(m._on_detected):
		g.detected.disconnect(m._on_detected)
	var since := GameState.events.size()
	var start := g.global_position.distance_to(chapter.players[0].global_position)
	var alerted := false
	var closest := start
	for i in 60 * 4:
		await get_tree().physics_frame
		if not _events("guard_alert", since).is_empty():
			alerted = true
		if alerted:
			closest = minf(closest, g.global_position.distance_to(chapter.players[0].global_position))
	if _events("guard_detected", since).is_empty():
		return "no detection while in plain view for 4 s"
	if not alerted:
		return "detected but no ALERT state"
	if closest > start - 0.5:
		return "guard did not close on the player (%.1f -> %.1f m)" % [start, closest]
	return ""

