extends SceneTree
func _initialize() -> void:
	for path in OS.get_cmdline_user_args():
		var n: Node3D = (load(path) as PackedScene).instantiate()
		for m in n.find_children("*", "MeshInstance3D", true, false):
			var mi: MeshInstance3D = m
			for i in mi.mesh.get_surface_count():
				var mat := mi.mesh.surface_get_material(i) as BaseMaterial3D
				if mat:
					print(mi.name, " ", i, " ", mat.resource_name, " tex=", mat.albedo_texture.resource_path if mat.albedo_texture else "none", " transp=", mat.transparency, " col=", mat.albedo_color)
		n.free()
	quit()
