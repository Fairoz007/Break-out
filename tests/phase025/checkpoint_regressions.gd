extends Node
## Real fresh-game input driver captures disk checkpoints, then reconstructs each saved mission.
## This checks reconstruction at load time, NOT completion from every restored checkpoint or visual quality.
## Run: Godot --headless --fixed-fps 60 --path . res://tests/phase025/checkpoint_regressions.tscn -- --save-slot=phase025_checkpoint_suite

class CheckpointDriver:
	extends "res://tests/phase02/autopilot.gd"
	signal driver_finished(reason: String, detail: Dictionary)
	func _finish(reason: String, detail := {}) -> void:
		if _done:
			return
		_done = true
		driver_finished.emit(reason, detail)

var chapter: ChapterRoot
var driver: CheckpointDriver
var snapshots := {}
var capture_errors: Array = []
var results: Array = []
var started := 0

func _ready() -> void:
	started = Time.get_ticks_msec()
	if not SaveService.save_path.contains("phase025"):
		push_error("Checkpoint tests require a dedicated --save-slot=phase025... argument")
		get_tree().quit(3)
		return
	GameState.event_logged.connect(_capture_checkpoint)
	chapter = ChapterRoot.new()
	add_child(chapter)
	driver = CheckpointDriver.new()
	driver.chapter = chapter
	driver.args = {"timeout": "4000", "fixed": true}
	driver.driver_finished.connect(_driver_finished)
	add_child(driver)
	chapter.start_new_game()

func _capture_checkpoint(kind: String, event: Dictionary) -> void:
	if kind != "checkpoint":
		return
	var cp := str(event["checkpoint"])
	if not event.get("written", false):
		capture_errors.append(cp + ": disk write failed")
		return
	var disk := SaveService.read()
	if disk.get("checkpoint", "") != cp:
		capture_errors.append(cp + ": disk checkpoint mismatch")
		return
	snapshots[cp] = disk.duplicate(true)

func _driver_finished(reason: String, detail: Dictionary) -> void:
	call_deferred("_verify_all", reason, detail)

func _verify_all(reason: String, detail: Dictionary) -> void:
	GameState.event_logged.disconnect(_capture_checkpoint)
	var original_events := GameState.events.duplicate(true)
	driver.queue_free()
	chapter.queue_free()
	await get_tree().process_frame
	GameState.cinematic_active = false
	GameState.locks = {}
	for mission in range(1, 7):
		for suffix in ["A", "B"]:
			var cp := "CP%02d_%s" % [mission, suffix]
			var errors: Array = []
			if not snapshots.has(cp):
				results.append({"checkpoint": cp, "pass": false, "errors": ["not reached by fresh-game input driver"]})
				continue
			var snap: Dictionary = snapshots[cp]
			chapter = ChapterRoot.new()
			add_child(chapter)
			for p in 2:
				Devices.set_virtual(p, true)
			chapter.continue_game(snap.duplicate(true))
			# continue_game/build/place/restore_patrol execute synchronously before mission.run.
			# Inspect before physics/cinematic scripts can legitimately advance the restored state.
			if chapter.mission == null or chapter.mission.index != mission:
				errors.append("wrong reconstructed mission")
			for p in 2:
				var saved: Dictionary = snap["players"][p]
				var expected := Vector3(saved["pos"][0], saved["pos"][1], saved["pos"][2])
				if chapter.players[p].global_position.distance_to(expected) > 0.001:
					errors.append("P%d position differs" % (p + 1))
				if absf(angle_difference(chapter.players[p].rotation.y, float(saved["yaw"]))) > 0.001:
					errors.append("P%d yaw differs" % (p + 1))
				if chapter.players[p].crouched != bool(saved["crouched"]):
					errors.append("P%d crouch differs" % (p + 1))
			var rebuilt := GameState.snapshot(cp, {})
			for key in ["schema", "mission_index", "checkpoint", "flags", "inventory", "knowledge", "consumed_dialogue", "transactions", "completed_objectives"]:
				if not _same(rebuilt.get(key), snap.get(key)):
					errors.append(key + " differs")
			if not _same(chapter.mission.patrol_state(), snap.get("patrol", {})):
				errors.append("patrol phase/position differs")
			results.append({"checkpoint": cp, "pass": errors.is_empty(), "errors": errors, "players": snap["players"], "objective_saved": snap.get("objective", ""), "patrol": snap.get("patrol", {})})
			chapter.queue_free()
			await get_tree().process_frame
	var failed := results.filter(func(row): return not row["pass"]).size()
	var report := {"fresh_playthrough_reason": reason, "driver_detail": detail, "snapshots_captured": snapshots.size(), "capture_errors": capture_errors, "passed": results.size() - failed, "failed": failed, "results": results, "snapshots": snapshots, "fresh_playthrough_events": original_events, "real_seconds": (Time.get_ticks_msec() - started) / 1000.0, "limitation": "Input-driven fresh run plus disk checkpoint reconstruction before mission coroutine advances. Does not prove continued progression from each save, objective HUD restoration, animated prop contact, visual quality, hardware inputs or performance."}
	DirAccess.make_dir_recursive_absolute("res://tests/phase025/evidence")
	var file := FileAccess.open("res://tests/phase025/evidence/checkpoint_regressions.json", FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(report, "\t"))
		file.close()
	print("CHECKPOINT REGRESSIONS ", results.size() - failed, "/", results.size(), " reason=", reason, " capture_errors=", capture_errors)
	get_tree().quit(0 if failed == 0 and capture_errors.is_empty() and reason == "chapter_complete" and file != null else 1)

func _same(a: Variant, b: Variant) -> bool:
	if a is Dictionary and b is Dictionary:
		if a.size() != b.size():
			return false
		for key in a:
			if not b.has(key) or not _same(a[key], b[key]):
				return false
		return true
	if a is Array and b is Array:
		if a.size() != b.size():
			return false
		for i in a.size():
			if not _same(a[i], b[i]):
				return false
		return true
	if (a is float or a is int) and (b is float or b is int):
		return absf(float(a) - float(b)) < 0.001
	return a == b
