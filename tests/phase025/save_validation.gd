extends Node

func _ready() -> void:
	call_deferred("run")

func run() -> void:
	var service := get_tree().root.get_node("SaveService")
	var snap := CanonStates.entry_snapshot(1)
	snap["players"] = [{"pos": [1, 0, 2], "yaw": 0}, {"pos": [2, 0, 2], "yaw": 1}]
	var checks := {"valid_snapshot": service.valid_checkpoint(snap), "empty_rejected": not service.valid_checkpoint({})}
	for key in ["schema", "chapter", "mission_index", "players", "flags", "inventory", "transactions"]:
		var broken := snap.duplicate(true)
		broken.erase(key)
		checks["missing_" + key] = not service.valid_checkpoint(broken)
	var bad_actor := snap.duplicate(true)
	bad_actor["players"][0]["pos"] = ["bad", 0, 0]
	checks["malformed_position"] = not service.valid_checkpoint(bad_actor)
	var bad_mission := snap.duplicate(true)
	bad_mission["mission_index"] = 99
	checks["invalid_mission"] = not service.valid_checkpoint(bad_mission)
	var bad_yaw := snap.duplicate(true)
	bad_yaw["players"][0]["yaw"] = INF
	checks["nonfinite_yaw"] = not service.valid_checkpoint(bad_yaw)
	var f := FileAccess.open("res://tests/phase025/evidence/save_validation.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(checks, "\t"))
	f.close()
	print("SAVE VALIDATION ", checks)
	get_tree().quit(0 if checks.values().all(func(v): return v) else 1)
