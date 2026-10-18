extends SceneTree
var frames := 0
var assets: Array = []
func _initialize():
	var directory = DirAccess.open("res://assets/props")
	for folder in directory.get_directories():
		var sub = DirAccess.open("res://assets/props/" + folder)
		for file in sub.get_files():
			if file.ends_with(".gltf"):
				assets.append("res://assets/props/" + folder + "/" + file)
	call_deferred("validate")
func validate():
	var output = []
	for path in assets:
		var packed = load(path)
		if packed == null:
			output.append({"path":path,"load":"FAIL"}); continue
		var instance = packed.instantiate()
		var view = SubViewport.new()
		view.size = Vector2i(768,768)
		view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(view)
		view.add_child(instance)
		var box = AABB()
		var first = true
		var counts = {"meshes":0,"triangles":0,"surfaces":0,"null_materials":0}
		for node in instance.find_children("*","MeshInstance3D",true,false):
			var local_box = node.global_transform * node.get_aabb()
			box = local_box if first else box.merge(local_box)
			first = false
			counts.meshes += 1
			for i in node.mesh.get_surface_count():
				counts.surfaces += 1
				if node.get_active_material(i) == null: counts.null_materials += 1
				var arrays = node.mesh.surface_get_arrays(i)
				counts.triangles += (arrays[Mesh.ARRAY_INDEX].size() if arrays[Mesh.ARRAY_INDEX] != null else arrays[Mesh.ARRAY_VERTEX].size()) / 3
		var camera = Camera3D.new()
		view.add_child(camera)
		var center = box.get_center()
		var radius = max(box.size.length(),0.2)
		camera.position = center + Vector3(0.9,0.65,1.1).normalized()*radius*1.25
		camera.look_at(center)
		camera.near = 0.001
		var light = DirectionalLight3D.new()
		view.add_child(light)
		light.rotation_degrees = Vector3(-40,-30,0)
		light.light_energy = 2.0
		var environment = WorldEnvironment.new()
		environment.environment = Environment.new()
		environment.environment.background_mode = Environment.BG_COLOR
		environment.environment.background_color = Color(0.12,0.14,0.17)
		environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		environment.environment.ambient_light_color = Color.WHITE
		environment.environment.ambient_light_energy = 0.7
		view.add_child(environment)
		for frame in range(15): await process_frame
		var image_path = "res://asset_library/manifests/"+path.get_file().get_basename()+"_preview.png"
		view.get_texture().get_image().save_png(image_path)
		output.append({"path":path,"load":"PASS","bounds_m":str(box),"geometry":counts,"preview":image_path})
		view.queue_free()
	var dir = DirAccess.open("res://assets/audio")
	if dir:
		for file in dir.get_files():
			if file.ends_with(".ogg"):
				var audio = load("res://assets/audio/"+file)
				output.append({"path":"res://assets/audio/"+file,"load":"PASS" if audio else "FAIL","duration_seconds":audio.get_length() if audio else 0})
	var report = FileAccess.open("res://asset_library/manifests/godot_resource_validation.json",FileAccess.WRITE)
	report.store_string(JSON.stringify(output,"\t"))
	quit()
