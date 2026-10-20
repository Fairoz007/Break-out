extends SceneTree
func _initialize() -> void:
	var names := ["rb_noah_reyes", "rb_silas_bell", "rb_adrian_cross", "rb_prisoner_npc", "rb_tomas_rusk"]
	var bones := ["Bip01 Pelvis", "Bip01 Neck", "Bip01 Head", "Bip01 R UpperArm", "Bip01 R Forearm", "Bip01 R Hand", "Bip01 R Thigh", "Bip01 R Calf", "Bip01 R Foot"]
	for n in names:
		var m: Node3D = (load("res://assets/characters/acquisition_20261019/rocketbox_facial/%s.glb" % n) as PackedScene).instantiate()
		var sk: Skeleton3D = m.find_children("*", "Skeleton3D", true, false)[0]
		var row := []
		for b in bones:
			row.append(sk.get_bone_global_rest(sk.find_bone(b)).origin.snappedf(0.1))
		var meshes := []
		for mi in m.find_children("*", "MeshInstance3D", true, false):
			var surf := []
			for i in (mi as MeshInstance3D).mesh.get_surface_count():
				var mat: Material = (mi as MeshInstance3D).mesh.surface_get_material(i)
				surf.append(mat.resource_name if mat else "?")
			meshes.append("%s%s" % [mi.name, surf])
		print(n, " ", row)
		print("   meshes ", meshes)
		m.free()
	quit()
