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
	f.close()
	# Atomic replace so a crash mid-write never corrupts the slot.
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(save_path)
	return DirAccess.rename_absolute(tmp, save_path) == OK


func read() -> Dictionary:
	if not has_save():
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(save_path))
	return parsed if parsed is Dictionary else {}


func erase() -> void:
	if has_save():
		DirAccess.remove_absolute(save_path)
