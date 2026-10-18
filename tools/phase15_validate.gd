extends SceneTree
# Isolated asset inspection utility. No game scenes, input or mission state.
var results = []
var jobs = []
func _initialize():
	var f = FileAccess.open("res://asset_library/manifests/phase15/validation_jobs.json",FileAccess.READ)
	jobs = JSON.parse_string(f.get_as_text())
	call_deferred("run")
func walk(node: Node, all: Array):
	all.append(node)
	for child in node.get_children(): walk(child,all)
func run():
	for job in jobs:
		var result = {"asset_id":job.asset_id,"path":job.path,"load":"FAILED"}
		var resource = load(job.path)
		if resource == null:
			results.append(result); continue
		result.load = "VERIFIED"
		result.resource_class = resource.get_class()
		if resource is AudioStream:
			result.duration_seconds = resource.get_length()
		elif resource is Texture2D:
			result.size = [resource.get_width(),resource.get_height()]
		elif resource is Font:
			result.glyphs_ascii = resource.get_string_size("ADRIAN: Hold the brake. NOAH: Ready.",HORIZONTAL_ALIGNMENT_LEFT,-1,26).x
		elif resource is Material:
			var holder = Node3D.new()
			var mesh = MeshInstance3D.new()
			mesh.mesh = SphereMesh.new()
			mesh.material_override = resource
			holder.add_child(mesh); mesh.owner = holder
			var packed = PackedScene.new(); packed.pack(holder)
			holder.free()
			await inspect_scene(packed,job,result)
		elif resource is PackedScene:
			await inspect_scene(resource,job,result)
		results.append(result)
		if results.size()%50 == 0: print("VALIDATED ",results.size(),"/",jobs.size())
	var file = FileAccess.open("res://asset_library/manifests/phase15/godot_validation.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(results,"\t"))
	await render_subtitles()
	print("PHASE15_VALIDATION_DONE ",results.size())
	quit()
func inspect_scene(packed,job,result):
	var view = SubViewport.new()
	view.size = Vector2i(512,512)
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	view.own_world_3d = true
	root.add_child(view)
	var instance = packed.instantiate()
	view.add_child(instance)
	var nodes = []; walk(instance,nodes)
	var box = AABB(); var first = true
	var meshes = 0; var triangles = 0; var nulls = 0; var surface_count = 0
	var skeletons = []; var animations = []
	for node in nodes:
		if node is MeshInstance3D and node.mesh:
			meshes += 1
			var b = node.global_transform * node.get_aabb()
			box = b if first else box.merge(b); first = false
			for i in node.mesh.get_surface_count():
				surface_count += 1
				if node.get_active_material(i) == null: nulls += 1
				var a = node.mesh.surface_get_arrays(i)
				triangles += (a[Mesh.ARRAY_INDEX].size() if a[Mesh.ARRAY_INDEX]!=null else a[Mesh.ARRAY_VERTEX].size())/3
		elif node is Skeleton3D:
			var bone_names = []
			for i in node.get_bone_count(): bone_names.append(node.get_bone_name(i))
			skeletons.append({"path":str(instance.get_path_to(node)),"bone_count":node.get_bone_count(),"bones":bone_names})
		elif node is AnimationPlayer:
			for name in node.get_animation_list():
				var a = node.get_animation(name)
				animations.append({"name":name,"duration":a.length,"tracks":a.get_track_count()})
	result.geometry = {"mesh_instances":meshes,"triangles":triangles,"surfaces":surface_count,"null_materials":nulls}
	result.bounds = {"position":[box.position.x,box.position.y,box.position.z],"size_m":[box.size.x,box.size.y,box.size.z]}
	result.skeletons = skeletons; result.animations = animations
	if meshes > 0:
		var center = box.get_center(); var radius = max(box.size.length(),0.15)
		var camera = Camera3D.new(); view.add_child(camera)
		camera.position = center + Vector3(0.8,0.55,1.05).normalized()*radius*1.2
		camera.near = 0.001; camera.far = max(radius*10,100)
		camera.look_at(center)
		var light = DirectionalLight3D.new(); view.add_child(light)
		light.rotation_degrees = Vector3(-35,-35,0); light.light_energy = 1.8
		var env = WorldEnvironment.new(); env.environment = Environment.new()
		env.environment.background_mode = Environment.BG_COLOR
		env.environment.background_color = Color(0.1,0.12,0.15)
		env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		env.environment.ambient_light_color = Color.WHITE
		env.environment.ambient_light_energy = 0.65
		view.add_child(env)
		for frame in range(5): await process_frame
		await RenderingServer.frame_post_draw
		var image_path = "res://asset_library/manifests/phase15/previews/"+job.asset_id+".png"
		view.get_texture().get_image().save_png(image_path)
		result.preview = image_path
		if skeletons.size() > 0:
			var pose_checks = []
			for node in nodes:
				if not node is AnimationPlayer: continue
				for name in node.get_animation_list():
					if not (name.ends_with("Walk_Loop") or name.ends_with("Crouch_Fwd_Loop") or name.ends_with("Jog_Fwd_Loop") or name == "Idle_Loop" or name.ends_with("Sprint_Loop") or name == "Interact" or name.ends_with("Crouch_Idle_Loop")): continue
					var duration = node.get_animation(name).length
					var samples = []
					node.play(name)
					for fraction in [0.25,0.75]:
						node.seek(duration*fraction,true)
						node.advance(0)
						await process_frame
						var bone_positions = []
						for sk in nodes:
							if sk is Skeleton3D:
								for bi in sk.get_bone_count():
									var p = sk.get_bone_global_pose(bi).origin
									bone_positions.append([p.x,p.y,p.z])
						await RenderingServer.frame_post_draw
						var shot = "res://asset_library/manifests/phase15/previews/"+job.asset_id+"_"+name.validate_filename()+"_"+str(int(fraction*100))+".png"
						view.get_texture().get_image().save_png(shot)
						samples.append({"fraction":fraction,"bones":bone_positions,"preview":shot})
					pose_checks.append({"animation":name,"samples":samples})
			result.animation_pose_samples = pose_checks
	view.queue_free()
	await process_frame
func render_subtitles():
	var view = SubViewport.new(); view.size = Vector2i(960,540)
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	var bg = ColorRect.new(); bg.color = Color(0.18,0.21,0.23); bg.size = Vector2(960,540); view.add_child(bg)
	var panel = PanelContainer.new(); panel.position = Vector2(60,375); panel.size = Vector2(840,110)
	panel.add_theme_stylebox_override("panel",load("res://assets/ui/phase15/subtitle_panel.tres")); view.add_child(panel)
	var label = Label.new(); label.text = "ADRIAN: Hold the brake.\nNOAH: I have it. Turn the selector to B."
	label.add_theme_font_override("font",load("res://assets/ui/phase15/noto_sans_variable.ttf"))
	label.add_theme_font_size_override("font_size",26); panel.add_child(label)
	for frame in range(5): await process_frame
	await RenderingServer.frame_post_draw
	view.get_texture().get_image().save_png("res://asset_library/manifests/phase15/subtitle_preview.png")
	view.queue_free()
