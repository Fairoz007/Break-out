extends Node
## Persistent checkpoint saves (REQ-SAVE-001..003). One slot for Chapter 1 in user://.

const DIR := "user://saves"
var save_path := DIR + "/ch01_slot1.json"


func _ready() -> void:
	DirAccess.make_dir_recursive_absolute(DIR)
	# Tests and the graphical playthrough use a separate slot so they never touch a player's save.
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--save-slot="):
			save_path = DIR + "/" + arg.get_slice("=", 1) + ".json"


func has_save() -> bool:
	return FileAccess.file_exists(save_path)


func write(snapshot: Dictionary) -> bool:
	var tmp := save_path + ".tmp"
	var f := FileAccess.open(tmp, FileAccess.WRITE)
	if f == null:
		push_error("Cannot write save " + tmp)
		return false
	f.store_string(JSON.stringify(snapshot, "\t"))
	f.flush()
	var write_error := f.get_error()
	f.close()
	if write_error != OK:
		return false
	# Rename replaces the destination. Never delete the last valid checkpoint first:
	# if writing or replacement fails, it must remain available to Continue.
	return DirAccess.rename_absolute(tmp, save_path) == OK


func read() -> Dictionary:
	if not has_save():
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(save_path))
	return parsed if parsed is Dictionary else {}


## File existence alone cannot enable Continue: interrupted or incompatible saves must not
## reach GameState.restore(), whose required keys otherwise raise runtime errors.
func can_continue() -> bool:
	return valid_checkpoint(read())


func valid_checkpoint(snap: Dictionary) -> bool:
	if snap.get("schema") != GameState.SCHEMA or snap.get("chapter") != "CH01":
		return false
	var index = snap.get("mission_index")
	if not (index is int or index is float) or index != int(index) or index < 1 or index > 6:
		return false
	if not snap.get("checkpoint") is String:
		return false
	for key in ["flags", "inventory", "knowledge", "patrol"]:
		if not snap.get(key) is Dictionary:
			return false
	for key in ["consumed_dialogue", "transactions", "completed_objectives"]:
		if not snap.get(key) is Array:
			return false
		for value in snap[key]:
			if not value is String:
				return false
	if not snap.get("players") is Array or snap["players"].size() != 2:
		return false
	for actor in snap["players"]:
		if not actor is Dictionary or not actor.get("pos") is Array or actor["pos"].size() != 3:
			return false
		for value in actor["pos"] + [actor.get("yaw")]:
			if not (value is int or value is float) or not is_finite(float(value)):
				return false
	return true


func erase() -> void:
	if has_save():
		DirAccess.remove_absolute(save_path)
