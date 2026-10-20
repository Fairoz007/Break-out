extends SceneTree
func _initialize() -> void:
	for p in ClassDB.class_get_enum_constants("Performance", "Monitor"):
		print(p, " = ", ClassDB.class_get_integer_constant("Performance", p))
	quit()
