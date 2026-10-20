extends SceneTree
func _initialize() -> void:
	for c in ["TwoBoneIK3D", "IKModifier3D", "SkeletonModifier3D", "ChainIK3D"]:
		if not ClassDB.class_exists(c): print(c, " missing"); continue
		print("== ", c, " <- ", ClassDB.get_parent_class(c))
		for p in ClassDB.class_get_property_list(c, true):
			print("  prop ", p.name, " ", type_string(p.type), " ", p.hint_string.left(60))
		for m in ClassDB.class_get_method_list(c, true):
			print("  meth ", m.name, " ", m.args.map(func(a): return a.name))
	quit()
