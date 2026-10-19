class_name EnvBuilder
extends RefCounted
## Builds blockout-to-asset environments in code from the Phase 01.5 modules (REQ-ENV-001..009).
## Geometry that must be solid gets an explicit box collider; GLB modules are visual unless asked to collide.
## All static colliders sit under one NavigationRegion3D so each level bakes its own navmesh.

const ENV := "res://assets/environments/phase15/"
const PROP := "res://assets/props/phase15/"
const MAT := "res://assets/materials/phase15/"
const LAYER_WORLD := 1
const LAYER_PLAYER := 2
const LAYER_NPC := 4

var root: Node3D
var nav: NavigationRegion3D
var dynamic: Node3D      # doors/grilles: excluded from nav baking so doorways stay walkable
var markers := {}
var _mats := {}


func _init(parent: Node3D) -> void:
	root = Node3D.new()
	root.name = "Environment"
	parent.add_child(root)
	nav = NavigationRegion3D.new()
	nav.name = "Navigation"
	var nm := NavigationMesh.new()
	nm.agent_radius = 0.35
	nm.agent_height = 1.8
	nm.agent_max_climb = 0.3
	nm.agent_max_slope = 40.0
	nm.cell_size = 0.1
	nm.cell_height = 0.1
	nm.geometry_parsed_geometry_type = NavigationMesh.PARSED_GEOMETRY_STATIC_COLLIDERS
	nm.geometry_collision_mask = LAYER_WORLD
	nav.navigation_mesh = nm
	root.add_child(nav)
	dynamic = Node3D.new()
	dynamic.name = "Dynamic"
	root.add_child(dynamic)


## World-space triplanar copy of a PBR material so boxes of any size keep a 1 m texture scale.
func mat(name: String, tint := Color(1, 1, 1), scale := 0.5) -> StandardMaterial3D:
	var key := "%s|%s|%s" % [name, tint, scale]
	if not _mats.has(key):
		# Prefer the 2K upgrade from the 2026-10-19 acquisition when one exists for this material.
		var hi := "res://assets/materials/acquisition_20261019/%s/%s_2k.tres" % [name, name]
		var m: StandardMaterial3D = load(hi if ResourceLoader.exists(hi) else MAT + name + ".tres").duplicate()
		m.uv1_triplanar = true
		m.uv1_world_triplanar = true
		m.uv1_scale = Vector3.ONE * scale
		m.albedo_color = m.albedo_color * tint
		_mats[key] = m
	return _mats[key]


func flat(color: Color, emissive := false) -> StandardMaterial3D:
	var key := "flat|%s|%s" % [color, emissive]
	if not _mats.has(key):
		var m := StandardMaterial3D.new()
		m.albedo_color = color
		m.roughness = 0.8
		if emissive:
			m.emission_enabled = true
			m.emission = color
			m.emission_energy_multiplier = 2.0
		_mats[key] = m
	return _mats[key]


## Solid box: collider + mesh. center/size in metres, Godot axes.
func box(center: Vector3, size: Vector3, material: Material, parent: Node3D = null, visible := true, name := "") -> StaticBody3D:
	var body := StaticBody3D.new()
	body.collision_layer = LAYER_WORLD
	body.collision_mask = 0
	if name != "":
		body.name = name
	body.position = center
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	cs.shape = shape
	body.add_child(cs)
	if visible:
		var mi := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = size
		mi.mesh = bm
		mi.material_override = material
		body.add_child(mi)
	(parent if parent else nav).add_child(body)
	return body


func floor_rect(x0: float, z0: float, x1: float, z1: float, material: Material, y := 0.0, thickness := 0.3) -> StaticBody3D:
	return box(Vector3((x0 + x1) / 2.0, y - thickness / 2.0, (z0 + z1) / 2.0), Vector3(absf(x1 - x0), thickness, absf(z1 - z0)), material)


func ceiling_rect(x0: float, z0: float, x1: float, z1: float, height: float, material: Material) -> StaticBody3D:
	var b := box(Vector3((x0 + x1) / 2.0, height + 0.15, (z0 + z1) / 2.0), Vector3(absf(x1 - x0), 0.3, absf(z1 - z0)), material)
	return b


## Straight wall from a to b (XZ), full collision, with optional door gaps [[t0, t1], ...] in metres along the wall.
func wall(a: Vector2, b: Vector2, height: float, material: Material, thickness := 0.25, gaps := [], base_y := 0.0) -> void:
	var length := a.distance_to(b)
	var dir := (b - a).normalized()
	var cuts := [0.0]
	for g in gaps:
		cuts.append(g[0])
		cuts.append(g[1])
	cuts.append(length)
	for i in range(0, cuts.size(), 2):
		var s: float = cuts[i]
		var e: float = cuts[i + 1]
		if e - s < 0.01:
			continue
		var mid := a + dir * ((s + e) / 2.0)
		var body := box(Vector3(mid.x, base_y + height / 2.0, mid.y), Vector3(e - s, height, thickness), material)
		body.rotation.y = -atan2(dir.y, dir.x)
	# lintels over door gaps
	for g in gaps:
		if height > 2.4:
			var mid2: Vector2 = a + dir * ((g[0] + g[1]) / 2.0)
			var lintel := box(Vector3(mid2.x, base_y + (height + 2.4) / 2.0, mid2.y), Vector3(g[1] - g[0], height - 2.4, thickness), material)
			lintel.rotation.y = -atan2(dir.y, dir.x)


## Instance a GLB. collide: "none", "box" (AABB box collider), or "thin" (AABB but at least 0.1 m deep).
func model(path: String, pos: Vector3, rot_y_deg := 0.0, collide := "none", parent: Node3D = null, scale := 1.0) -> Node3D:
	var res: PackedScene = load(path)
	assert(res != null, "Missing model " + path)
	var inst: Node3D = res.instantiate()
	inst.position = pos
	inst.rotation_degrees.y = rot_y_deg
	inst.scale = Vector3.ONE * scale
	var host: Node3D = parent if parent else root
	if collide == "none":
		host.add_child(inst)
		return inst
	var body := StaticBody3D.new()
	body.collision_layer = LAYER_WORLD
	body.collision_mask = 0
	body.position = pos
	body.rotation_degrees.y = rot_y_deg
	inst.position = Vector3.ZERO
	inst.rotation = Vector3.ZERO
	body.add_child(inst)
	var aabb := local_aabb(inst)
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	var size := aabb.size * scale
	if collide == "thin":
		size.z = max(size.z, 0.12)
	shape.size = size.max(Vector3(0.05, 0.05, 0.05))
	cs.shape = shape
	cs.position = (aabb.position + aabb.size / 2.0) * scale
	body.add_child(cs)
	(parent if parent else nav).add_child(body)
	return body


static func local_aabb(n: Node3D) -> AABB:
	var box_out := AABB()
	var first := true
	for m in n.find_children("*", "MeshInstance3D", true, false):
		var mi: MeshInstance3D = m
		if mi.mesh == null:
			continue
		var xf := Transform3D.IDENTITY
		var cur: Node = mi
		while cur != n and cur is Node3D:
			xf = (cur as Node3D).transform * xf
			cur = cur.get_parent()
		var b := xf * mi.get_aabb()
		box_out = b if first else box_out.merge(b)
		first = false
	return box_out


## Repeat a module along a line (bars, fences, railings) with one solid collider for the whole run.
func run(path: String, a: Vector3, b: Vector3, module_len: float, height: float, depth: float, collide := true, y_offset := 0.0) -> void:
	var length := Vector2(a.x, a.z).distance_to(Vector2(b.x, b.z))
	var dir := (b - a).normalized()
	var yaw := rad_to_deg(-atan2(dir.z, dir.x))
	var n := maxi(1, int(round(length / module_len)))
	var step := length / n
	for i in n:
		var p := a + dir * (step * (i + 0.5))
		var inst := model(path, p + Vector3(0, y_offset, 0), yaw, "none")
		inst.scale.x = step / module_len
	if collide:
		var mid := (a + b) / 2.0
		var body := box(Vector3(mid.x, a.y + y_offset + height / 2.0, mid.z), Vector3(length, height, depth), null, null, false)
		body.rotation.y = deg_to_rad(yaw)


func mark(name: String, pos: Vector3, yaw_deg := 0.0) -> Marker3D:
	var m := Marker3D.new()
	m.name = name
	m.position = pos
	m.rotation_degrees.y = yaw_deg
	root.add_child(m)
	markers[name] = m
	m.add_to_group("marks")
	return m


func omni(pos: Vector3, color: Color, energy := 1.5, range_m := 8.0, shadow := false) -> OmniLight3D:
	var l := OmniLight3D.new()
	l.position = pos
	l.light_color = color
	l.light_energy = energy
	l.omni_range = range_m
	l.shadow_enabled = shadow
	root.add_child(l)
	return l


func spot(pos: Vector3, look_at: Vector3, color: Color, energy := 3.0, range_m := 10.0, angle := 35.0) -> SpotLight3D:
	var l := SpotLight3D.new()
	root.add_child(l)
	l.position = pos
	l.look_at_from_position(pos, look_at, Vector3.UP if absf((look_at - pos).normalized().y) < 0.99 else Vector3.FORWARD)
	l.light_color = color
	l.light_energy = energy
	l.spot_range = range_m
	l.spot_angle = angle
	l.shadow_enabled = true
	return l


func sun(rot_deg: Vector3, color: Color, energy: float, shadows := true) -> DirectionalLight3D:
	var l := DirectionalLight3D.new()
	l.rotation_degrees = rot_deg
	l.light_color = color
	l.light_energy = energy
	l.shadow_enabled = shadows
	l.directional_shadow_max_distance = 60.0
	root.add_child(l)
	return l


func environment(sky_top: Color, sky_horizon: Color, ambient: Color, ambient_energy: float, fog := 0.0, exposure := 1.0) -> WorldEnvironment:
	var we := WorldEnvironment.new()
	var env := Environment.new()
	var sky := Sky.new()
	var psm := ProceduralSkyMaterial.new()
	psm.sky_top_color = sky_top
	psm.sky_horizon_color = sky_horizon
	psm.ground_horizon_color = sky_horizon
	psm.ground_bottom_color = sky_horizon.darkened(0.6)
	sky.sky_material = psm
	env.background_mode = Environment.BG_SKY
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = ambient
	env.ambient_light_energy = ambient_energy
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.tonemap_exposure = exposure
	env.ssao_enabled = true
	if fog > 0.0:
		env.fog_enabled = true
		env.fog_density = fog
		env.fog_light_color = sky_horizon
	we.environment = env
	root.add_child(we)
	return we


func bake() -> void:
	nav.bake_navigation_mesh(false)
