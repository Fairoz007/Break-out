extends Node
## Static validation inside the running project (autoloads present): loads and compiles every GDScript under
## res://scripts, res://tests and res://tools and reports any that fail to compile or cannot be instantiated.
## godot --headless --path . res://tests/phase04/parse_check.tscn

var checked := 0
var failed := []


func _ready() -> void:
	for root in ["res://scripts", "res://tests", "res://tools"]:
		_walk(root)
	var f := FileAccess.open("res://tests/phase04/evidence/parse_check.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"checked": checked, "failed": failed}, "\t"))
	f.close()
	print("PARSE CHECK checked=%d failed=%d %s" % [checked, failed.size(), failed])
	get_tree().quit(0 if failed.is_empty() else 1)


func _walk(dir: String) -> void:
	for d in DirAccess.get_directories_at(dir):
		if d.begins_with(".") or d == "evidence":
			continue
		_walk(dir + "/" + d)
	for file in DirAccess.get_files_at(dir):
		if not file.ends_with(".gd"):
			continue
		var path := dir + "/" + file
		if path == get_script().resource_path:
			continue
		checked += 1
		var s := ResourceLoader.load(path, "GDScript", ResourceLoader.CACHE_MODE_IGNORE) as GDScript   # fresh compile
		if s == null or not s.can_instantiate():
			failed.append(path)
