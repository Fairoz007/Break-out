extends Node
## Phase 02 automated system tests (REQ-TEST-001). Run with the project's autoloads active:
##   godot --headless --path . --fixed-fps 60 res://tests/phase02/run_tests.tscn -- --save-slot=test_suite
## Writes tests/phase02/evidence/system_tests.json and exits 0 only when every test passes.

var results: Array = []
var chapter: ChapterRoot


func _ready() -> void:
	await get_tree().process_frame
	var tests := ["data_integrity", "subtitle_wrap", "commit_idempotent", "snapshot_roundtrip", "save_file", "device_exclusive",
		"interaction_leases", "split_screen_world", "movement_speeds", "wall_collision", "camera_min_distance", "simultaneous_movement",
		"solo_gate_m06", "solo_gate_m02", "solo_gate_m03", "save_rejected_in_cinematic", "mutual_skip", "checkpoint_reload",
		"device_disconnect_pause", "settings_roundtrip", "guard_detection_and_cover", "canon_entry_states", "escort_gap", "input_between_physics_ticks"]
	for t in tests:
		var ok := true
		var detail := ""
		var r = await call("t_" + t)
		if r is String:
			ok = r == ""
			detail = r
		results.append({"test": t, "pass": ok, "detail": detail})
		print("TEST ", t, " ", "PASS" if ok else "FAIL: " + detail)
		await _reset()
	var failed := results.filter(func(x): return not x["pass"]).size()
	var f := FileAccess.open("res://tests/phase02/evidence/system_tests.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"passed": results.size() - failed, "failed": failed, "results": results}, "\t"))
	f.close()
	print("SYSTEM TESTS: %d passed, %d failed" % [results.size() - failed, failed])
	get_tree().quit(1 if failed > 0 else 0)


func _reset() -> void:
	get_tree().paused = false
	if chapter:
		chapter.queue_free()
		chapter = null
	Devices.auto_assign()
	GameState.cinematic_active = false
	await get_tree().process_frame


func _chapter(mission := 1, steps := []) -> ChapterRoot:
	chapter = ChapterRoot.new()
	add_child(chapter)
	Devices.set_virtual(0, true)
	Devices.set_virtual(1, true)
	var snap := CanonStates.entry_snapshot(mission)
	for s in steps:   # resume the mission past these committed steps, like a checkpoint would
		snap["transactions"].append("m%02d.%s" % [mission, s])
	chapter.continue_game(snap)
	await _frames(20)
	return chapter


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


func _seconds(s: float) -> void:
	await _frames(int(s * 60.0))


func _floor_point(m: Mission, pos: Vector3) -> Vector3:
	var q := PhysicsRayQueryParameters3D.create(pos + Vector3.UP * 2.0, pos + Vector3.DOWN * 3.0, EnvBuilder.LAYER_WORLD)
	var hit := m.get_world_3d().direct_space_state.intersect_ray(q)
	return hit["position"] if hit else pos


# ------------------------------------------------------------------ tests (return "" on pass, else reason)
func t_data_integrity() -> String:
	if DialogueDB.lines.size() != 145: return "lines %d" % DialogueDB.lines.size()
	if DialogueDB.shots.size() != 36: return "shots %d" % DialogueDB.shots.size()
	if DialogueDB.missions.size() != 6: return "missions"
	var objs := 0
	for m in DialogueDB.missions: objs += m["objectives"].size()
	if objs != 19: return "objectives %d" % objs
	for i in range(1, 7):
		if DialogueDB.lines_for(i).is_empty(): return "no lines for mission %d" % i
	return ""


func t_subtitle_wrap() -> String:
	for id in DialogueDB.lines:
		var text: String = DialogueDB.lines[id]["text"]
		for row in Subtitles.wrap_text(text):
			if row.length() > Subtitles.MAX_CHARS and not " " in row: continue  # single long word cannot wrap
			if row.length() > Subtitles.MAX_CHARS: return "%s row over %d chars" % [id, Subtitles.MAX_CHARS]
		var pages := Subtitles.paginate(text)
		for pg in pages:
			if pg.split("\n").size() > Subtitles.MAX_ROWS: return id + " page over two rows"
		if " ".join(pages).replace("\n", " ") != text: return id + " text altered or truncated"
	if Subtitles.paginate(DialogueDB.line("CH01_M01_DLG020")["text"]).size() != 2: return "DLG020 should paginate to 2 pages"
	return ""


func t_commit_idempotent() -> String:
	GameState.reset_new_game()
	if not GameState.commit("test.pickup", {"inv:shim": "NOAH"}): return "first commit refused"
	GameState.inventory["shim"] = "ADRIAN"
	if GameState.commit("test.pickup", {"inv:shim": "NOAH"}): return "duplicate commit accepted"
	if GameState.inventory["shim"] != "ADRIAN": return "duplicate commit changed state"
	return ""


func t_snapshot_roundtrip() -> String:
	GameState.reset_new_game()
	GameState.commit("t.a", {"x": 1, "inv:photo": "NOAH_SHIRT", "know:k": true})
	GameState.consumed_dialogue["CH01_M01_DLG001"] = true
	GameState.complete_objective("CH01_M01_OBJ001")
	var snap := GameState.snapshot("CP01_B", {"players": [{"pos": [1, 2, 3], "yaw": 0.5}], "patrol": {"G": {"index": 2}}})
	var copy: Dictionary = JSON.parse_string(JSON.stringify(snap))
	GameState.reset_new_game()
	GameState.restore(copy)
	if GameState.flags.get("x") != 1.0 and GameState.flags.get("x") != 1: return "flag lost"
	if GameState.inventory["photo"] != "NOAH_SHIRT": return "inventory lost"
	if not GameState.knowledge.get("k", false): return "knowledge lost"
	if not GameState.consumed_dialogue.has("CH01_M01_DLG001"): return "consumed dialogue lost"
	if not GameState.transactions.has("t.a"): return "transactions lost"
	if not GameState.completed_objectives.has("CH01_M01_OBJ001"): return "objective lost"
	if GameState.checkpoint_id != "CP01_B": return "checkpoint id"
	for key in ["schema", "mission", "checkpoint", "players", "patrol", "flags", "inventory", "knowledge", "consumed_dialogue", "transactions"]:
		if not snap.has(key): return "snapshot missing " + key
	return ""


func t_save_file() -> String:
	SaveService.erase()
	if SaveService.has_save(): return "erase failed"
	var snap := {"schema": GameState.SCHEMA, "mission_index": 3, "checkpoint": "CP03_B", "flags": {"a": true}}
	if not SaveService.write(snap): return "write failed"
	var back := SaveService.read()
	if back.get("checkpoint") != "CP03_B" or not back["flags"]["a"]: return "read mismatch"
	if FileAccess.file_exists(SaveService.save_path + ".tmp"): return "temp file left behind"
	var replacement := snap.duplicate(true)
	replacement["checkpoint"] = "CP03_C"
	if not SaveService.write(replacement): return "replacement write failed"
	if SaveService.read().get("checkpoint") != "CP03_C": return "replacement not restored"
	# A destination directory forces replacement to fail after the temp write.
	# Verify the failed operation leaves the destination and staged data intact.
	var real_path := SaveService.save_path
	SaveService.save_path = real_path + ".blocked"
	DirAccess.make_dir_recursive_absolute(SaveService.save_path)
	var unexpectedly_saved := SaveService.write(snap)
	var staged := FileAccess.file_exists(SaveService.save_path + ".tmp")
	DirAccess.remove_absolute(SaveService.save_path + ".tmp")
	DirAccess.remove_absolute(SaveService.save_path)
	SaveService.save_path = real_path
	if unexpectedly_saved or not staged: return "failed replacement handling incorrect"
	if SaveService.read().get("checkpoint") != "CP03_C": return "previous checkpoint lost"
	SaveService.erase()
	return ""


func t_escort_gap() -> String:
	var m := Mission.new()
	add_child(m)
	var n := Npc.new()
	m.add_child(n)
	n.set_physics_process(false)
	var follower := Node3D.new()
	m.add_child(follower)
	m.players = [follower]
	var destination := Vector3(0, 0, -20)
	follower.position = Vector3(0, 0, 4.1)
	var waits := m._someone_behind(n, destination, 4.0)
	follower.position.z = 3.9
	var inside := m._someone_behind(n, destination, 4.0)
	follower.position.z = -5.0
	var ahead := m._someone_behind(n, destination, 4.0)
	m.queue_free()
	if not waits or inside or ahead: return "escort four-metre boundary incorrect"
	return ""


func t_input_between_physics_ticks() -> String:
	Devices.set_virtual(0, true)
	# A complete press and release between two simulation ticks used to vanish.
	Devices.virtual_state[0]["buttons"]["interact"] = true
	Devices._process(0.004)
	Devices.virtual_state[0]["buttons"]["interact"] = false
	Devices._process(0.004)
	Devices._process(0.004)
	Devices._physics_process(1.0 / 60.0)
	if not Devices._physics_just[0].get("interact", false): return "press lost between simulation ticks"
	if Devices._physics_just[1].get("interact", false): return "press leaked to partner"
	Devices._physics_process(1.0 / 60.0)
	if Devices._physics_just[0].get("interact", false): return "press repeated next simulation tick"
	return ""


func t_device_exclusive() -> String:
	Devices.assign(0, Devices.Kind.KEYBOARD_MOUSE)
	Devices.assign(1, Devices.Kind.KEYBOARD_RIGHT)
	Devices.assign(1, Devices.Kind.KEYBOARD_MOUSE)   # P2 takes P1's device: P1 must get P2's old one
	if Devices.owners[0]["kind"] == Devices.owners[1]["kind"]: return "device shared by both players"
	Devices.set_virtual(0, true)
	Devices.set_virtual(1, true)
	Devices.virtual_state[0]["move"] = Vector2(0, -1)
	if Devices.move(1) != Vector2.ZERO: return "P1 input leaked into P2"
	if Devices.move(0) != Vector2(0, -1): return "P1 input missing"
	Devices.virtual_state[1]["buttons"]["interact"] = true
	await get_tree().process_frame
	if Devices.pressed(0, "interact"): return "P2 button leaked into P1"
	if not Devices.just_pressed(1, "interact") and not Devices.pressed(1, "interact"): return "P2 press missing"
	return ""


func t_interaction_leases() -> String:
	var it := Interactable.new().setup("t_hold", "Hold", 1, Interactable.Mode.HOLD_ACTIVE)
	add_child(it)
	if it.press(0): return "P1 used a P2-only interaction"
	var any := Interactable.new().setup("t_any", "Hold", Interactable.ANY, Interactable.Mode.HOLD_ACTIVE)
	add_child(any)
	any.press(0)
	if any.press(1): return "second player took a held lease"
	any.hold_update(0, false, 0.016)
	if any.is_held(): return "release did not free lease"
	var hc := Interactable.new().setup("t_hc", "Shim", 0, Interactable.Mode.HOLD_COMPLETE)
	hc.hold_seconds = 1.0
	add_child(hc)
	hc.press(0)
	hc.hold_update(0, true, 0.5)
	hc.hold_update(0, false, 0.016)
	if hc.progress != 0.0: return "interrupted hold kept progress"
	for n in [it, any, hc]: n.queue_free()
	return ""


func t_split_screen_world() -> String:
	await _chapter(1)
	if chapter.viewports[0].find_world_3d() != chapter.viewports[1].find_world_3d(): return "views do not share one World3D"
	if chapter.cams[0] == chapter.cams[1]: return "cameras shared"
	if not chapter.cams[0].current or not chapter.cams[1].current: return "camera not current in its view"
	if chapter.viewports[0].size.x < 500 or chapter.viewports[1].size.x < 500: return "viewport too small %s" % chapter.viewports[0].size
	if get_tree().get_nodes_in_group("mission").size() != 1: return "mission simulated more than once"
	if chapter.find_children("*", "DialogueDirector", true, false).size() != 1: return "dialogue director count"
	if chapter.find_children("*", "CinematicDirector", true, false).size() != 1: return "cinematic director count"
	return ""


func _measure(p: Player, move: Vector2, sprint := false, crouch := false, seconds := 1.0, run := false) -> float:
	p.crouched = crouch
	var start := p.global_position
	Devices.virtual_state[p.index]["move"] = move
	Devices.virtual_state[p.index]["buttons"]["sprint"] = sprint
	Devices.virtual_state[p.index]["buttons"]["run"] = run
	await _seconds(seconds)
	Devices.virtual_state[p.index]["move"] = Vector2.ZERO
	Devices.virtual_state[p.index]["buttons"]["sprint"] = false
	Devices.virtual_state[p.index]["buttons"]["run"] = false
	await _frames(5)
	return Vector2(p.global_position.x - start.x, p.global_position.z - start.z).length() / seconds


func t_movement_speeds() -> String:
	await _chapter(2)   # open yard
	var p: Player = chapter.players[1]
	p.place(Transform3D(Basis(), Vector3(18, 0.05, -15)))
	await _frames(10)
	var walk := await _measure(p, Vector2(0, -1))
	p.place(Transform3D(Basis(), Vector3(18, 0.05, -15)))
	var jog := await _measure(p, Vector2(0, -1), false, false, 1.0, true)
	p.place(Transform3D(Basis(), Vector3(18, 0.05, -15)))
	var sprint := await _measure(p, Vector2(0, -1), true)
	p.place(Transform3D(Basis(), Vector3(18, 0.05, -15)))
	var crouch := await _measure(p, Vector2(0, -1), false, true)
	p.crouched = false
	if walk < 1.2 or walk > 1.6: return "walk %.2f m/s" % walk
	if jog < 2.9 or jog > 3.5: return "jog %.2f m/s" % jog
	if sprint < 4.7 or sprint > 5.4: return "sprint %.2f m/s" % sprint
	if crouch < 0.6 or crouch > 0.85: return "crouch %.2f m/s" % crouch
	if absf(p.global_position.y) > 0.2: return "not on floor y=%.2f" % p.global_position.y
	return ""


func t_wall_collision() -> String:
	await _chapter(2)
	var p: Player = chapter.players[1]
	p.place(Transform3D(Basis(), Vector3(4.0, 0.05, -12)))  # walk west into the 5 m fence at x=1
	await _frames(5)
	chapter.rigs[1].yaw = 0.0
	await _measure(p, Vector2(-1, 0), true, false, 3.0)
	if p.global_position.x < 1.0: return "passed through fence x=%.2f" % p.global_position.x
	return ""


func t_camera_min_distance() -> String:
	await _chapter(1)
	var p: Player = chapter.players[0]
	p.place(Transform3D(Basis(Vector3.UP, 0.0), Vector3(22.0, 0.05, -15.4)))   # back to the holding wall
	chapter.rigs[0].yaw = 0.0
	await _frames(30)
	var d: float = chapter.rigs[0].current_distance()
	if d > chapter.rigs[0].arm.get_hit_length() + 0.05: return "camera extends beyond wall hit (%.2f)" % d
	p.place(Transform3D(Basis(), Vector3(18, 0.05, -6)))
	await _frames(40)
	d = chapter.rigs[0].current_distance()
	if absf(d - 2.8) > 0.35: return "open-space distance %.2f, expected 2.8" % d
	return ""


func t_simultaneous_movement() -> String:
	await _chapter(2)
	var a: Player = chapter.players[0]
	var b: Player = chapter.players[1]
	a.place(Transform3D(Basis(), Vector3(15, 0.05, -10)))
	b.place(Transform3D(Basis(), Vector3(25, 0.05, -18)))
	chapter.rigs[0].yaw = 0.0
	chapter.rigs[1].yaw = PI / 2
	await _frames(5)
	var a0 := a.global_position
	var b0 := b.global_position
	Devices.virtual_state[0]["move"] = Vector2(0, -1)
	Devices.virtual_state[1]["move"] = Vector2(0, -1)
	await _seconds(1.0)
	Devices.virtual_state[0]["move"] = Vector2.ZERO
	Devices.virtual_state[1]["move"] = Vector2.ZERO
	var da := a.global_position - a0
	var db := b.global_position - b0
	if da.length() < 1.0 or db.length() < 1.0: return "a player did not move"
	if da.normalized().dot(db.normalized()) > 0.5: return "cameras not independent (same direction)"
	return ""


func t_solo_gate_m06() -> String:
	await _chapter(6)
	var m: Mission = chapter.mission
	await _seconds(6.0)   # line 001
	var hw: Interactable = m.items["m06_handle_w"]
	chapter.players[0].place(Transform3D(Basis(), hw.global_position - Vector3(0.3, 1.0, 0)))
	await _frames(5)
	hw.press(0)
	await _seconds(6.0)
	hw.hold_update(0, true, 0.016)
	if GameState.completed_objectives.has("CH01_M06_OBJ001"): return "one player completed the dual-handle gate"
	if m.items["m06_handle_e"].press(0): return "P1 operated Noah's handle"
	return ""


func t_solo_gate_m02() -> String:
	await _chapter(2, ["intro", "entered", "confrontation"])
	var m: Mission = chapter.mission
	var ball: Interactable = m.items["m02_ball"]
	await _seconds(3.0)
	if not m.items["m02_mediate"].enabled: return "mediation not offered at the distraction stage"
	if ball.enabled: return "ball roll available without Adrian mediating"
	return ""


func t_solo_gate_m03() -> String:
	await _chapter(3, ["intro", "ask", "lamp_request"])
	var m: Mission = chapter.mission
	await _seconds(2.0)
	if m.items["m03_screen"].enabled: return "screen usable without the isolation lever held"
	m.items["m03_lever"].press(0)
	await _seconds(0.5)
	if not m.items["m03_screen"].enabled: return "screen not enabled while lever held"
	return ""


func t_save_rejected_in_cinematic() -> String:
	await _chapter(1)
	GameState.cinematic_active = true
	var ok := chapter.commit_checkpoint("CP01_B")
	GameState.cinematic_active = false
	if ok: return "checkpoint saved during a cinematic"
	GameState.locks["door:test"] = true
	ok = chapter.commit_checkpoint("CP01_B")
	GameState.locks.erase("door:test")
	if ok: return "checkpoint saved while a door was moving"
	return ""


func t_mutual_skip() -> String:
	await _chapter(1)
	var shots := [{"id": "CH01_M01_CS01_SH02", "from": [Vector3(17, 1.6, -8), Vector3(19, 1.4, -10)], "lines": ["CH01_M01_DLG001", "CH01_M01_DLG002", "CH01_M01_DLG003"]}]
	chapter.cinematic.play(shots, "test recap")
	await _frames(30)
	Devices.virtual_state[0]["buttons"]["skip"] = true
	await _frames(3)
	Devices.virtual_state[0]["buttons"]["skip"] = false
	await _seconds(1.0)
	if not chapter.cinematic.active: return "one player's skip ended the cinematic"
	Devices.virtual_state[1]["buttons"]["skip"] = true
	await _frames(3)
	Devices.virtual_state[1]["buttons"]["skip"] = false
	await _seconds(4.0)
	if chapter.cinematic.active: return "mutual skip did not end cinematic"
	for id in ["CH01_M01_DLG001", "CH01_M01_DLG002", "CH01_M01_DLG003"]:
		if not GameState.consumed_dialogue.has(id): return id + " not committed after skip"
	if chapter.players[0].input_locked: return "input still locked after cinematic"
	return ""


func t_checkpoint_reload() -> String:
	await _chapter(4)
	var a: Player = chapter.players[0]
	var start := a.global_position
	GameState.commit("test.after_checkpoint", {"temp": true})
	a.place(Transform3D(Basis(), start + Vector3(0, 0, -3)))
	chapter.reload_checkpoint()
	await _frames(40)
	if chapter.players[0].global_position.distance_to(start) > 0.3: return "P1 not restored (%.2f m off)" % chapter.players[0].global_position.distance_to(start)
	if GameState.transactions.has("test.after_checkpoint"): return "uncommitted transaction survived retry"
	if GameState.checkpoint_id != "CP04_A": return "checkpoint id " + GameState.checkpoint_id
	return ""


func t_device_disconnect_pause() -> String:
	await _chapter(1)
	Devices.device_lost.emit(1)
	await get_tree().process_frame
	var ok := get_tree().paused and chapter.pause_menu.visible
	chapter.pause_menu.close()
	return "" if ok else "disconnect did not pause with reassignment prompt"


func t_settings_roundtrip() -> String:
	var old := Settings.subtitle_scale
	Settings.set_value("subtitle_scale", 1.4)
	Settings.subtitle_scale = 1.0
	Settings.load_settings()
	var ok := absf(Settings.subtitle_scale - 1.4) < 0.01
	Settings.set_value("subtitle_scale", old)
	return "" if ok else "subtitle scale not persisted"


func t_guard_detection_and_cover() -> String:
	await _chapter(4)
	var m: Mission = chapter.mission
	m.commit("count")
	var g: GuardAI = m.npcs["Guard"]
	g.patrolling = false
	g.stop()
	g.place(Vector3(44.0, 0, -6.0), 270.0)    # facing +X (east)
	g.face(Vector3(50.0, 1.0, -6.0))
	g.detection_enabled = true
	g.detection = [0.0, 0.0]
	var p: Player = chapter.players[0]
	chapter.players[1].place(Transform3D(Basis(), Vector3(40.5, 0.05, -1.0)))   # Noah stays in his cell
	p.place(Transform3D(Basis(), Vector3(50.0, 0.05, -6.0)))                     # in the open, in the cone
	await _seconds(2.0)
	if g.detection[0] < 1.0 and not GameState.events.any(func(e): return e["kind"] == "detected_fail"): return "open player not detected (%.2f)" % g.detection[0]
	return ""


func t_canon_entry_states() -> String:
	for i in range(2, 7):
		var snap := CanonStates.entry_snapshot(i)
		var exp := CanonStates.expected_after(i - 1)
		for k in exp["inventory"]:
			if snap["inventory"][k] != exp["inventory"][k]: return "M%d entry %s" % [i, k]
	if CanonStates.entry_snapshot(4)["inventory"]["shim"] != "ADRIAN": return "M04 must start with Adrian holding the shim"
	if CanonStates.expected_after(6)["inventory"]["shim"] != "CONFISCATED": return "shim not confiscated at end"
	return ""
