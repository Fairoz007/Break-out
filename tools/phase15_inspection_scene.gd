extends SceneTree
# Builds and renders an ASSET INSPECTION scene (no gameplay, no input, no mission logic).
# godot --path . --rendering-method gl_compatibility --script tools/phase15_inspection_scene.gd
# Output: tests/asset_inspection/phase15_asset_inspection.tscn and PNG/JSON evidence in
# asset_library/manifests/phase15/inspection/.
const SCENE = "res://tests/asset_inspection/phase15_asset_inspection.tscn"
const OUT = "res://asset_library/manifests/phase15/inspection/"
const ENV = "res://assets/environments/phase15/"
const PROP = "res://assets/props/phase15/"
const PH = "res://assets/props/phase15_polyhaven/"
const CHAR = "res://assets/characters/phase15/rocketbox/"
const PROXY = "res://assets/characters/phase15/ubc/"
const DISC = "res://assets/props/phase15_discovery/"
var root3d: Node3D
var placements = []

func _initialize():
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://tests/asset_inspection"))
	call_deferred("run")

func walk(n: Node, all: Array):
	all.append(n)
	for c in n.get_children(): walk(c, all)

func aabb_of(n: Node3D) -> AABB:
	var nodes = []; walk(n, nodes); var box = AABB(); var first = true
	for m in nodes:
		if m is MeshInstance3D and m.mesh:
			var b = m.global_transform * m.get_aabb()
			box = b if first else box.merge(b); first = false
	return box

func own(n: Node):
	for c in n.get_children():
		c.owner = root3d
		if c.scene_file_path == "": own(c)

func origin_marker(at: Vector3):
	# RGB axis gizmo (X red, Y green, Z blue, 0.5 m) so the origin render shows where each pivot sits.
	for axis in [[Vector3(0.25, 0, 0), Vector3(0.5, 0.03, 0.03), Color.RED], [Vector3(0, 0.25, 0), Vector3(0.03, 0.5, 0.03), Color.GREEN], [Vector3(0, 0, 0.25), Vector3(0.03, 0.03, 0.5), Color.BLUE]]:
		var m = MeshInstance3D.new(); var b = BoxMesh.new(); b.size = axis[1]; m.mesh = b
		var mat = StandardMaterial3D.new(); mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED; mat.albedo_color = axis[2]
		mat.no_depth_test = true; m.material_override = mat
		root3d.add_child(m); m.owner = root3d; m.position = at + axis[0]

func place(id: String, path: String, slot: Vector3, mode := "aabb", rot_y := 0.0) -> Node3D:
	# mode "aabb": AABB min corner (x,z) and floor (y) snapped to slot -> dimension-based placement.
	# mode "origin": raw asset origin at slot -> exposes pivot conventions for modular snapping.
	var res = load(path)
	if res == null:
		placements.append({"id": id, "path": path, "load": "FAILED"}); return null
	var inst: Node3D = res.instantiate(); inst.name = id
	root3d.add_child(inst); inst.owner = root3d
	inst.rotation_degrees.y = rot_y
	var box = aabb_of(inst)
	if mode == "aabb":
		inst.position = slot - Vector3(box.position.x, box.position.y, box.position.z)
	else:
		inst.position = slot
	var after = aabb_of(inst)
	placements.append({"id": id, "path": path, "load": "VERIFIED", "mode": mode,
		"origin_to_aabb_min_m": [snapped(box.position.x, 0.001), snapped(box.position.y, 0.001), snapped(box.position.z, 0.001)],
		"size_m": [snapped(box.size.x, 0.001), snapped(box.size.y, 0.001), snapped(box.size.z, 0.001)],
		"placed_aabb_min": [snapped(after.position.x, 0.001), snapped(after.position.y, 0.001), snapped(after.position.z, 0.001)]})
	return inst

func label(text: String, pos: Vector3):
	var l = Label3D.new(); l.text = text; l.font_size = 48; l.pixel_size = 0.004; l.position = pos
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED; root3d.add_child(l); l.owner = root3d

func run():
	# root must be inside the tree so global AABBs are valid during placement
	var view = SubViewport.new(); view.size = Vector2i(1600, 900); view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	view.own_world_3d = true; root.add_child(view)
	root3d = Node3D.new(); root3d.name = "Phase15AssetInspection"; view.add_child(root3d)
	var env = WorldEnvironment.new(); env.name = "Env"; env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR; env.environment.background_color = Color(0.42, 0.45, 0.5)
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.environment.ambient_light_color = Color.WHITE
	env.environment.ambient_light_energy = 0.35; env.environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	root3d.add_child(env); env.owner = root3d
	var sun = DirectionalLight3D.new(); sun.name = "Sun"; sun.rotation_degrees = Vector3(-50, -35, 0); sun.light_energy = 0.9
	sun.shadow_enabled = true; root3d.add_child(sun); sun.owner = root3d
	var ground = MeshInstance3D.new(); ground.name = "InspectionGround"; ground.mesh = PlaneMesh.new(); ground.mesh.size = Vector2(90, 90)
	var gm = StandardMaterial3D.new(); gm.albedo_color = Color(0.32, 0.33, 0.34); ground.material_override = gm
	ground.position = Vector3(20, -0.01, 10); root3d.add_child(ground); ground.owner = root3d
	# ---- Zone A: modular cell-block test on a 4 m grid (dimension-snapped) ----
	label("ZONE A  modular 4 m grid", Vector3(0, 4.5, -1))
	for i in 3:
		place("floor_%d" % i, ENV + "floor_4m.glb", Vector3(i * 4.0, -0.0001, 0), "aabb")
		place("floor_b%d" % i, ENV + "floor_4m.glb", Vector3(i * 4.0, -0.0001, 4), "aabb")
		place("wall_%d" % i, ENV + "wall_4m.glb", Vector3(i * 4.0, 0, -0.3), "aabb")
	place("pier", ENV + "corner_pier.glb", Vector3(12.0, 0, -0.3), "aabb")
	place("cell_bars", ENV + "cell_bars_3m.glb", Vector3(0.2, 0, 3.0), "aabb")
	place("cell_door", ENV + "cell_door_1m.glb", Vector3(3.4, 0, 3.0), "aabb")
	place("security_door", ENV + "security_door_12.glb", Vector3(5.0, 0, 3.0), "aabb")
	place("spillway_door", ENV + "double_spillway_door.glb", Vector3(7.0, 0, 3.0), "aabb")
	place("barred_window", ENV + "barred_window.glb", Vector3(9.5, 1.2, -0.2), "aabb")
	place("stairs", ENV + "stairs_10_risers.glb", Vector3(9.0, 0, 3.0), "aabb")
	for path in DirAccess.get_files_at(ENV):
		if path.begins_with("stairs") and path.ends_with(".glb") and path != "stairs_10_risers.glb":
			place("stairs_new", ENV + path, Vector3(13.0, 0, 3.0), "aabb")
	place("catwalk_0", ENV + "catwalk_2m.glb", Vector3(0, 3.0, 6.0), "aabb")
	place("catwalk_1", ENV + "catwalk_2m.glb", Vector3(2.0, 3.0, 6.0), "aabb")
	place("railing_0", ENV + "railing_2m.glb", Vector3(0, 3.1, 7.4), "aabb")
	place("railing_1", ENV + "railing_2m.glb", Vector3(2.0, 3.1, 7.4), "aabb")
	place("ladder", ENV + "ladder_28.glb", Vector3(4.2, 0, 6.0), "aabb")
	place("hatch", ENV + "service_hatch_11.glb", Vector3(6.0, 0, 6.0), "aabb")
	place("fence_0", ENV + "fence_2x5.glb", Vector3(0, 0, 10.0), "aabb")
	place("fence_1", ENV + "fence_2x5.glb", Vector3(5.0, 0, 10.0), "aabb")
	place("yard_gate", ENV + "yard_gate_2m.glb", Vector3(10.2, 0, 10.0), "aabb")
	# raw origins (pivot convention evidence)
	place("wall_origin_test", ENV + "wall_4m.glb", Vector3(0, 0, -6), "origin")
	place("door_origin_test", ENV + "cell_door_1m.glb", Vector3(5, 0, -6), "origin")
	origin_marker(Vector3(0, 0, -6)); origin_marker(Vector3(5, 0, -6))
	# scale references: both protagonists inside the cell row
	for ref in [["adrian", CHAR + "adrian_cross.glb", Vector3(1.0, 0, 1.2)], ["noah", CHAR + "noah_reyes.glb", Vector3(3.6, 0, 1.2)]]:
		var n = place(ref[0], ref[1], ref[2], "origin")  # skinned AABBs are bind-space; character origins are at the feet
		if n:
			var nodes = []; walk(n, nodes)
			for p in nodes:
				if p is AnimationPlayer and p.has_animation("Idle"): p.play("Idle")
	# ---- Zone B: prop line-up (dimension-snapped, 1 m pitch rows) ----
	label("ZONE B  props (original row 1-2, Poly Haven row 3-4)", Vector3(20, 3.5, -1))
	var x = 18.0; var z = 0.0
	for f in DirAccess.get_files_at(PROP):
		if not f.ends_with(".glb"): continue
		var n = place("prop_" + f.get_basename(), PROP + f, Vector3(x, 0, z), "aabb")
		if n: x += max(aabb_of(n).size.x, 0.3) + 0.4
		if x > 38.0: x = 18.0; z += 3.0
	x = 18.0; z += 3.5
	for d in DirAccess.get_directories_at(PH):
		for f in DirAccess.get_files_at(PH + d):
			if not f.ends_with("_1k.gltf"): continue
			var n = place("ph_" + d, PH + d + "/" + f, Vector3(x, 0, z), "aabb")
			if n: x += min(max(aabb_of(n).size.x, 0.3), 12.0) + 0.6
			if x > 40.0: x = 18.0; z += 4.0
	place("guard_scale_ref", CHAR + "tomas_rusk.glb", Vector3(16.5, 0, 0.5), "origin")
	# discovery props (Agent D runtime integration), if present
	x = 18.0; z += 4.5
	if DirAccess.dir_exists_absolute(DISC):
		for d in DirAccess.get_directories_at(DISC):
			for f in DirAccess.get_files_at(DISC + d):
				if not (f.ends_with(".glb") or f.ends_with(".gltf")): continue
				var n = place("disc_" + d + "_" + f.get_basename(), DISC + d + "/" + f, Vector3(x, 0, z), "aabb")
				if n: x += min(max(aabb_of(n).size.x, 0.3), 14.0) + 0.8
				if x > 44.0: x = 18.0; z += 6.0
	# ---- Zone C: PBR material test cubes ----
	label("ZONE C  PBR materials on 1 m cubes", Vector3(2, 2.5, 15))
	var mats = DirAccess.get_files_at("res://assets/materials/phase15/")
	var i = 0
	for m in mats:
		if not m.ends_with(".tres"): continue
		var cube = MeshInstance3D.new(); cube.name = "mat_" + m.get_basename(); cube.mesh = BoxMesh.new()
		cube.material_override = load("res://assets/materials/phase15/" + m)
		cube.position = Vector3((i % 10) * 1.5, 0.5, 15.0 + int(i / 10) * 1.6)
		root3d.add_child(cube); cube.owner = root3d
		placements.append({"id": cube.name, "path": "res://assets/materials/phase15/" + m, "load": "VERIFIED" if cube.material_override else "FAILED"})
		i += 1
	# ---- Zone D: characters ----
	var cx = 14.0
	var cast = []
	for c in ["adrian_cross", "noah_reyes", "tomas_rusk", "mara_sen", "silas_bell", "prisoner_npc"]: cast.append([CHAR, c, 0.0])
	for c in ["adrian_cross", "noah_reyes", "tomas_rusk", "mara_sen", "silas_bell", "prisoner_npc", "prison_guard"]: cast.append([PROXY, c, 1.0])
	for e in cast:
		if e[2] > 0 and e[1] == "adrian_cross": cx = 26.0
		var n = place("char_" + e[0].get_base_dir().get_file() + "_" + e[1], e[0] + e[1] + ".glb", Vector3(cx, 0, 34.0), "origin"); cx += 1.6
		if n:
			var nodes = []; walk(n, nodes)
			for p in nodes:
				if p is AnimationPlayer and p.has_animation("Idle"): p.autoplay = "Idle"; p.play("Idle")
	var packed = PackedScene.new(); var err = packed.pack(root3d)
	var save_err = ResourceSaver.save(packed, SCENE)
	# ---- render evidence ----
	var cam = Camera3D.new(); view.add_child(cam); cam.far = 400
	var shots = {"zoneA_overview": [Vector3(6, 9, 20), Vector3(6, 1, 3)], "zoneA_cells": [Vector3(4, 1.7, 9), Vector3(4, 1.2, 1)],
		"zoneA_doors_stairs": [Vector3(9, 2.2, 10.5), Vector3(9, 1.2, 3)], "zoneA_catwalk": [Vector3(-3, 4.5, 11), Vector3(2, 3, 6.5)],
		"zoneA_origins": [Vector3(2.5, 2.4, -11.5), Vector3(2.5, 0.6, -6)], "zoneB_props": [Vector3(28, 10, 24), Vector3(28, 0, 5)],
		"zoneB_props_close": [Vector3(24, 3, 8), Vector3(24, 0.6, 2)], "zoneB_discovery": [Vector3(30, 9, 24), Vector3(30, 1, 13)], "zoneC_materials": [Vector3(7, 4, 23), Vector3(7, 0.5, 15.8)],
		"zoneD_characters_realistic": [Vector3(18.4, 1.2, 39.5), Vector3(18.4, 0.95, 34.3)], "zoneD_characters_proxy": [Vector3(31.2, 1.2, 40.0), Vector3(31.2, 0.95, 34.3)]}
	var out = []
	for k in shots:
		cam.position = shots[k][0]; cam.look_at(shots[k][1])
		for f in 6: await process_frame
		await RenderingServer.frame_post_draw
		var p = OUT + k + ".png"; view.get_texture().get_image().save_png(p); out.append(p)
	var rep = {"scene": SCENE, "pack_error": err, "save_error": save_err, "placements": placements, "screenshots": out}
	var f = FileAccess.open(OUT + "inspection_report.json", FileAccess.WRITE); f.store_string(JSON.stringify(rep, "\t"))
	print("PHASE15_INSPECTION_DONE ", placements.size(), " save_err=", save_err)
	quit()
