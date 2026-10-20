class_name EnvBuilder
extends RefCounted
## Builds blockout-to-asset environments in code from the Phase 01.5 modules (REQ-ENV-001..009).
## Geometry that must be solid gets an explicit box collider; GLB modules are visual unless asked to collide.
## All static colliders sit under one NavigationRegion3D so each level bakes its own navmesh.

const ENV := "res://assets/environments/phase15/"
const PROP := "res://assets/props/phase15/"
const MAT := "res://assets/materials/phase15/"
const SURFACE_UPGRADES := {
	"concrete_block_wall": "concrete_wall_008", "concrete_wall_004": "concrete_wall_005",
	"painted_concrete_02": "grey_plaster", "concrete_wall_001": "concrete_wall_008",
	"concrete_slab_wall": "concrete_wall_005", "painted_concrete": "grey_plaster",
	"worn_asphalt": "worn_asphalt", "asphalt_02": "asphalt_02",
	"concrete_floor_painted": "brushed_concrete", "anti_slip_concrete": "brushed_concrete",
	"concrete_floor_worn_001": "brushed_concrete", "hangar_concrete_floor": "brushed_concrete"
}
const LAYER_WORLD := 1
const LAYER_PLAYER := 2
const LAYER_NPC := 4
## Solid geometry that stops third-person/cinematic cameras. See-through runs (bars, fences, railings, grilles) keep
## LAYER_WORLD for bodies, navigation and guard sight but not this layer, so cameras look through them instead of
## collapsing onto the character's face (D03-014).
const LAYER_CAMERA := 16
const SEE_THROUGH := ["cell_bars", "cell_door", "fence", "railing", "grille", "gate", "razor_wire"]

var root: Node3D
var nav: NavigationRegion3D
var dynamic: Node3D      # doors/grilles: excluded from nav baking so doorways stay walkable
var markers := {}
var _mats := {}
## Interior finish applied by wall() while non-empty (Phase 03): {"dado": Material, "dado_h": float,
## "line": Material, "skirt": Material, "frame": Material}. Visual only; collision, navigation and gaps unchanged.
var wall_trim := {}


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
		var selected := "res://assets/materials/phase025/%s/%s.tres" % [SURFACE_UPGRADES.get(name, ""), SURFACE_UPGRADES.get(name, "")]
		var m: StandardMaterial3D = load(selected if ResourceLoader.exists(selected) else (hi if ResourceLoader.exists(hi) else MAT + name + ".tres")).duplicate()
		m.uv1_triplanar = true
		m.uv1_world_triplanar = true
		m.uv1_scale = Vector3.ONE * scale
		# Full-strength scan normals produced sparkling, gravel-like surfaces at gameplay distance.
		m.normal_scale = 0.25
		m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
		if "concrete" in name or "asphalt" in name:
			m.metallic = 0.0
			m.metallic_specular = 0.18
		m.albedo_color = m.albedo_color * tint
		m.set_meta("surface_name", name)   # footstep surface (CharacterVisual._surface_under)
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
	body.collision_layer = LAYER_WORLD | LAYER_CAMERA
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
		if not wall_trim.is_empty():
			_trim_segment(mid, dir, e - s, thickness, base_y)
	# lintels over door gaps
	for g in gaps:
		if height > 2.4:
			var mid2: Vector2 = a + dir * ((g[0] + g[1]) / 2.0)
			var lintel := box(Vector3(mid2.x, base_y + (height + 2.4) / 2.0, mid2.y), Vector3(g[1] - g[0], height - 2.4, thickness), material)
			lintel.rotation.y = -atan2(dir.y, dir.x)
		if wall_trim.has("frame"):
			_door_frame(a + dir * g[0], a + dir * g[1], dir, thickness, base_y, minf(height, 2.4))


## Visual-only box (no collider, not part of navigation baking): trims, plates, beams under a solid ceiling.
func visual_box(center: Vector3, size: Vector3, material: Material, yaw := 0.0, parent: Node3D = null) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	mi.mesh = bm
	mi.material_override = material
	mi.position = center
	mi.rotation.y = yaw
	(parent if parent else root).add_child(mi)
	return mi


func _trim_segment(mid: Vector2, dir: Vector2, length: float, thickness: float, base_y: float) -> void:
	var yaw := -atan2(dir.y, dir.x)
	var n := Vector2(-dir.y, dir.x)
	var dado_h: float = wall_trim.get("dado_h", 1.2)
	for side in [-1.0, 1.0]:
		var off: Vector2 = n * side * (thickness / 2.0 + 0.006)
		var c := mid + off
		if wall_trim.has("dado"):
			visual_box(Vector3(c.x, base_y + dado_h / 2.0, c.y), Vector3(length, dado_h, 0.008), wall_trim["dado"], yaw)
			var line: Vector2 = mid + n * side * (thickness / 2.0 + 0.011)
			visual_box(Vector3(line.x, base_y + dado_h, line.y), Vector3(length, 0.045, 0.012), wall_trim.get("line", wall_trim["dado"]), yaw)
		if wall_trim.has("skirt"):
			var sk: Vector2 = mid + n * side * (thickness / 2.0 + 0.012)
			visual_box(Vector3(sk.x, base_y + 0.06, sk.y), Vector3(length, 0.12, 0.02), wall_trim["skirt"], yaw)


## Pressed-steel door frame (jambs + head) around a wall opening; visual only so doorway clearance is unchanged.
func _door_frame(p0: Vector2, p1: Vector2, dir: Vector2, thickness: float, base_y: float, h: float) -> void:
	var yaw := -atan2(dir.y, dir.x)
	var m: Material = wall_trim["frame"]
	for p in [p0 - dir * 0.04, p1 + dir * 0.04]:
		visual_box(Vector3(p.x, base_y + h / 2.0, p.y), Vector3(0.08, h, thickness + 0.05), m, yaw)
	var c := (p0 + p1) / 2.0
	visual_box(Vector3(c.x, base_y + h + 0.04, c.y), Vector3(p0.distance_to(p1) + 0.16, 0.08, thickness + 0.05), m, yaw)


## Painted finish for walls, trims and steel: CC0 painted-plaster maps tinted, world triplanar at 1 m.
## block=true overlays a concrete-masonry normal map so painted CMU walls show coursed blocks and mortar.
func paint(color: Color, block := false, rough := 0.62) -> StandardMaterial3D:
	var key := "paint|%s|%s|%s" % [color, block, rough]
	if not _mats.has(key):
		var m := StandardMaterial3D.new()
		m.albedo_texture = load(P3 + "paint_diff.jpg")
		m.albedo_color = color * Color(1.35, 1.35, 1.35)     # source plaster albedo averages ~0.74
		m.roughness_texture = load(P3 + "paint_micro_rough.jpg")
		m.roughness = rough * 1.3
		m.normal_enabled = true
		m.normal_texture = load(P3 + ("block_nor.jpg" if block else "paint_micro_nor.jpg"))
		m.normal_scale = 0.45 if block else 0.25
		m.uv1_triplanar = true
		m.uv1_world_triplanar = true
		m.uv1_scale = Vector3.ONE * (1.6 if block else 0.8)    # 1.6/m gives 400 x 200 mm masonry courses
		m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
		_mats[key] = m
	return _mats[key]


## Sealed / painted industrial floor slab (CC0 Poly Haven garage_floor relief and roughness), tinted.
## clean=true keeps the relief but takes albedo from the painted-plaster scan: a maintained painted epoxy floor
## instead of a stained garage slab.
func sealed_floor(tint := Color(1, 1, 1), scale := 0.3, clean := false) -> StandardMaterial3D:
	var key := "sealed|%s|%s|%s" % [tint, scale, clean]
	if not _mats.has(key):
		var m := StandardMaterial3D.new()
		m.albedo_texture = load(P3 + ("paint_diff.jpg" if clean else "floor_sealed_diff.jpg"))
		m.albedo_color = tint
		m.normal_enabled = true
		m.normal_texture = load(P3 + "floor_sealed_nor.jpg")
		m.normal_scale = 0.4
		m.roughness_texture = load(P3 + "floor_sealed_rough.jpg")
		m.roughness = 0.85
		m.metallic_specular = 0.35
		m.uv1_triplanar = true
		m.uv1_world_triplanar = true
		m.uv1_scale = Vector3.ONE * scale
		m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
		_mats[key] = m
	return _mats[key]


## Phase 03 PBR surface copied from the verified CC0 library: P3/<prefix>_diff|_nor_gl|_rough.jpg, world triplanar.
func surface(prefix: String, tint := Color(1, 1, 1), scale := 0.25, normal_scale := 0.5) -> StandardMaterial3D:
	var key := "surface|%s|%s|%s" % [prefix, tint, scale]
	if not _mats.has(key):
		var m := StandardMaterial3D.new()
		m.albedo_texture = load(P3 + prefix + "_diff.jpg")
		m.albedo_color = tint
		m.normal_enabled = true
		m.normal_texture = load(P3 + prefix + "_nor_gl.jpg")
		m.normal_scale = normal_scale
		m.roughness_texture = load(P3 + prefix + "_rough.jpg")
		m.roughness = 1.0
		m.metallic_specular = 0.3
		m.uv1_triplanar = true
		m.uv1_world_triplanar = true
		m.uv1_scale = Vector3.ONE * scale
		m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
		_mats[key] = m
	return _mats[key]


## Straight visual pipe between two points (service headers, conduit), with collar rings every ~3 m.
func pipe_run(a: Vector3, b: Vector3, radius: float, material: Material, collars := true) -> void:
	var d := b - a
	var mi := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = radius
	cm.bottom_radius = radius
	cm.height = d.length()
	cm.radial_segments = 20
	cm.rings = 1
	mi.mesh = cm
	mi.material_override = material
	root.add_child(mi)
	mi.position = (a + b) / 2.0
	mi.quaternion = Quaternion(Vector3.UP, d.normalized())
	if collars:
		var n := int(d.length() / 3.0)
		for i in range(1, n + 1):
			var c := MeshInstance3D.new()
			var cc := CylinderMesh.new()
			cc.top_radius = radius * 1.18
			cc.bottom_radius = radius * 1.18
			cc.height = 0.06
			cc.radial_segments = 20
			c.mesh = cc
			c.material_override = material
			root.add_child(c)
			c.position = a + d * (float(i) / (n + 1))
			c.quaternion = mi.quaternion


## Painted floor marking (walkway/hazard line) between two floor points; visual only.
func floor_line(a: Vector3, b: Vector3, width: float, color: Color) -> void:
	var d := b - a
	var m := paint(color, false, 0.5)
	visual_box((a + b) / 2.0 + Vector3(0, 0.004, 0), Vector3(Vector2(d.x, d.z).length(), 0.004, width), m, -atan2(d.z, d.x))


## Reinforced-concrete downstand beams under a ceiling slab, every spacing metres across the room.
func ceiling_beams(x0: float, z0: float, x1: float, z1: float, height: float, spacing: float, along_x: bool, material: Material, depth := 0.45) -> void:
	if along_x:
		var z := minf(z0, z1) + spacing
		while z < maxf(z0, z1) - 0.2:
			box(Vector3((x0 + x1) / 2.0, height - depth / 2.0, z), Vector3(absf(x1 - x0), depth, 0.3), material)
			z += spacing
	else:
		var x := minf(x0, x1) + spacing
		while x < maxf(x0, x1) - 0.2:
			box(Vector3(x, height - depth / 2.0, (z0 + z1) / 2.0), Vector3(0.3, depth, absf(z1 - z0)), material)
			x += spacing


## Light fittings must not shadow their own emitter (a pendant shade otherwise throws a hard rim shadow).
static func no_shadow(n: Node) -> Node:
	for c in n.find_children("*", "GeometryInstance3D", true, false):
		(c as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	if n is GeometryInstance3D:
		(n as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return n


## Ceiling fitting that actually emits from the fixture: fluorescent model, a wide downward spot carrying
## shadows and the main contribution, plus a weak omni for the ceiling/upper-wall wash.
func ceiling_light(pos: Vector3, color: Color, energy := 2.0, reach := 9.0, shadow := false, fixture := true) -> SpotLight3D:
	if fixture:
		no_shadow(model(PROP + "fluorescent_fixture.glb", pos, 0, "none"))
	var s := spot(pos - Vector3(0, 0.12, 0), pos - Vector3(0, 10, 0), color, energy, reach, 72.0)
	s.shadow_enabled = shadow
	s.spot_angle_attenuation = 1.6
	omni(pos - Vector3(0, 0.3, 0), color, energy * 0.18, 3.5)
	return s


## Institutional wall sign: enamelled plate with black lettering (Label3D), facing +Z of yaw.
func sign(text: String, pos: Vector3, yaw_deg := 0.0, width := 0.9, plate := Color(0.9, 0.9, 0.86), ink := Color(0.05, 0.05, 0.05)) -> Node3D:
	var n := Node3D.new()
	n.position = pos
	n.rotation_degrees.y = yaw_deg
	root.add_child(n)
	var h := 0.22 * (1 + text.count("\n"))
	visual_box(Vector3.ZERO, Vector3(width, h, 0.012), paint(plate, false, 0.35), 0.0, n)
	var l := Label3D.new()
	l.text = text
	l.modulate = ink
	l.outline_size = 0
	l.pixel_size = 0.0022
	l.font_size = 48
	l.position = Vector3(0, 0, 0.0075)
	l.double_sided = false
	l.shaded = true
	l.width = width / l.pixel_size * 0.9
	l.autowrap_mode = TextServer.AUTOWRAP_WORD
	n.add_child(l)
	return n


const P3 := "res://assets/materials/phase03/"
static var _p3_cache := {}


## Phase 03 hard-surface props author P3_* slots; bind each to one shared PBR material with object-space
## micro-surface detail (CC0 Poly Haven maps, see assets/materials/phase03/SOURCES.md). Shared instances keep
## the material count per room low.
static func p3_material(name: String, src: Material) -> Material:
	if _p3_cache.has(name):
		return _p3_cache[name]
	var m := StandardMaterial3D.new()
	m.resource_name = name
	var base := src as BaseMaterial3D
	if base == null:
		m.albedo_color = Color(0.42, 0.44, 0.45)
		m.roughness = 0.5
	if base:
		m.albedo_color = base.albedo_color
		m.metallic = base.metallic
		m.roughness = base.roughness
		m.emission_enabled = base.emission_enabled
		m.emission = base.emission
		m.emission_energy_multiplier = base.emission_energy_multiplier
	m.uv1_triplanar = true
	m.uv1_scale = Vector3.ONE * 2.5
	m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	var painted := name.begins_with("P3_Paint") or name == "P3_BusPaint" or name in ["P3_PlasticDark", "P3_PlasticGrey", "P3_Laminate", "P3_LabelWhite", "P3_CastIron"]
	if painted or name in ["P3_Stainless", "P3_Rubber", "P3_Brass"]:
		# Roughness texture multiplies the authored value: lift it so the map averages back near it.
		m.roughness_texture = load(P3 + "paint_micro_rough.jpg")
		m.roughness = clampf(m.roughness * 1.35, 0.05, 1.0)
		m.normal_enabled = true
		m.normal_texture = load(P3 + "paint_micro_nor.jpg")
		m.normal_scale = 0.18 if name == "P3_Stainless" else (0.6 if name == "P3_CastIron" else 0.3)
		if name == "P3_Stainless":
			m.uv1_scale = Vector3(6.0, 0.6, 6.0)   # stretched micro-pattern reads as brushing
	match name:
		"P3_Concrete":
			m.albedo_texture = load(P3 + "plinth_concrete_diff.jpg")
			m.normal_enabled = true
			m.normal_texture = load(P3 + "plinth_concrete_nor.jpg")
			m.roughness_texture = load(P3 + "plinth_concrete_rough.jpg")
			m.roughness = 1.0
			m.uv1_scale = Vector3.ONE
		"P3_BusPaint":
			# Automotive gloss paint; the coach shell is single-skinned, so render both faces for the cabin view.
			m.clearcoat_enabled = true
			m.clearcoat = 0.7
			m.clearcoat_roughness = 0.12
			m.cull_mode = BaseMaterial3D.CULL_DISABLED
			m.normal_scale = 0.08
		"P3_Glass":
			m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			m.albedo_color = Color(0.62, 0.68, 0.68, 0.22)
			m.metallic = 0.0
			m.roughness = 0.04
			m.metallic_specular = 0.9
		"P3_Screen", "P3_ScreenBlue", "P3_LampAmber", "P3_LampGreen":
			m.emission_enabled = true
			if base:
				m.emission = base.emission if base.emission != Color.BLACK else base.albedo_color
			m.emission_energy_multiplier = maxf(m.emission_energy_multiplier, 1.2)
	_p3_cache[name] = m
	return m


static func _bind_p3(inst: Node3D) -> void:
	for child in inst.find_children("*", "MeshInstance3D", true, false):
		var mi := child as MeshInstance3D
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			var src := mi.mesh.surface_get_material(s)
			if src and src.resource_name.begins_with("P3_"):
				mi.set_surface_override_material(s, p3_material(src.resource_name, src))


## Shared visual treatment also used by animated doors, which instantiate their scenes directly.
static var _bus_glass: StandardMaterial3D


static func apply_finish(inst: Node3D, path: String) -> void:
	_bind_p3(inst)
	if "transport_bus" in path.get_file():
		# Laminated security glazing: faint green-grey tint and real reflections (was near-invisible alpha).
		if _bus_glass == null:
			_bus_glass = StandardMaterial3D.new()
			_bus_glass.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			_bus_glass.albedo_color = Color(0.22, 0.27, 0.27, 0.42)
			_bus_glass.roughness = 0.04
			_bus_glass.metallic = 0.0
			_bus_glass.metallic_specular = 1.0
			_bus_glass.cull_mode = BaseMaterial3D.CULL_DISABLED
		for child in inst.find_children("*", "MeshInstance3D", true, false):
			var mi := child as MeshInstance3D
			for i in mi.mesh.get_surface_count():
				var m := mi.mesh.surface_get_material(i)
				if m and m.resource_name == "Windows":
					mi.set_surface_override_material(i, _bus_glass)
	# Bars/guardrails are painted institutional steel, not uniformly orange rust.
	# Keep all original meshes and collision envelopes; replace only their exaggerated finish.
	if path.get_file() in ["cell_bars_3m.glb", "cell_door_1m.glb", "security_grille_4m.glb", "railing_2m.glb", "fence_2x5.glb", "fence_end_post_5m.glb", "yard_gate_2m.glb"]:
		var paint := StandardMaterial3D.new()
		paint.albedo_color = Color(0.19, 0.23, 0.24)
		paint.roughness = 0.58
		paint.metallic = 0.12
		for child in inst.find_children("*", "MeshInstance3D", true, false):
			(child as MeshInstance3D).material_override = paint
	elif path.get_file() == "pipe_straight_2m.glb":
		# Service pipework: grey gloss paint with light wear rather than uniform orange corrosion.
		for child in inst.find_children("*", "MeshInstance3D", true, false):
			(child as MeshInstance3D).material_override = p3_material("P3_PaintSteelGrey", null)


## Instance a GLB. collide: "none", "box" (AABB box collider), or "thin" (AABB but at least 0.1 m deep).
func model(path: String, pos: Vector3, rot_y_deg := 0.0, collide := "none", parent: Node3D = null, scale := 1.0) -> Node3D:
	var res: PackedScene = load(path)
	assert(res != null, "Missing model " + path)
	var inst: Node3D = res.instantiate()
	apply_finish(inst, path)
	inst.position = pos
	inst.rotation_degrees.y = rot_y_deg
	inst.scale = Vector3.ONE * scale
	var host: Node3D = parent if parent else root
	if collide == "none":
		host.add_child(inst)
		return inst
	var body := StaticBody3D.new()
	body.collision_layer = LAYER_WORLD | LAYER_CAMERA
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


## Photogrammetry prop resting on a horizontal support, preserving its authored proportions.
## Dressing is deliberately visual-only; collision and mission affordances remain authored separately.
func scanned_prop(asset: String, pos: Vector3, yaw := 0.0, target_height := 0.0) -> Node3D:
	var path := "res://assets/props/phase025/%s/%s_1k.gltf" % [asset, asset]
	var inst := model(path, pos, yaw, "none")
	var bounds := local_aabb(inst)
	var factor := target_height / bounds.size.y if target_height > 0.0 and bounds.size.y > 0.001 else 1.0
	inst.scale = Vector3.ONE * factor
	inst.position.y = pos.y - bounds.position.y * factor
	return inst


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
		if SEE_THROUGH.any(func(k): return k in path.get_file()):
			body.collision_layer = LAYER_WORLD


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
	l.omni_attenuation = 1.0
	l.light_size = 0.12               # soft PCSS penumbra from a fixture-sized emitter
	l.shadow_enabled = shadow
	l.shadow_bias = 0.04
	l.light_indirect_energy = 1.2
	l.light_volumetric_fog_energy = 0.6
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
	l.spot_angle_attenuation = 0.8
	l.light_size = 0.08
	l.shadow_enabled = true
	l.light_volumetric_fog_energy = 1.2
	return l


func sun(rot_deg: Vector3, color: Color, energy: float, shadows := true) -> DirectionalLight3D:
	var l := DirectionalLight3D.new()
	l.rotation_degrees = rot_deg
	l.light_color = color
	l.light_energy = energy
	l.light_angular_distance = 0.6    # sun-disc sized penumbra
	l.shadow_enabled = shadows
	l.shadow_blur = 1.2
	l.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_4_SPLITS
	l.directional_shadow_max_distance = 70.0
	l.directional_shadow_blend_splits = true
	l.light_volumetric_fog_energy = 0.4
	root.add_child(l)
	_has_sun = true
	if _environment:
		_configure_outdoor(_environment, l)
	return l


var _has_sun := false
var _environment: Environment


## One WorldEnvironment per level. Interior levels pass dark sky colours; a level that also calls sun()
## becomes sky-lit (ambient + reflections from the sky, aerial fog). Quality follows Settings.graphics_quality.
func environment(sky_top: Color, sky_horizon: Color, ambient: Color, ambient_energy: float, fog := 0.0, exposure := 1.0) -> WorldEnvironment:
	var we := WorldEnvironment.new()
	var env := Environment.new()
	var sky := Sky.new()
	var psm := ProceduralSkyMaterial.new()
	psm.sky_top_color = sky_top
	psm.sky_horizon_color = sky_horizon
	psm.sky_curve = 0.12
	psm.ground_horizon_color = sky_horizon.darkened(0.15)
	psm.ground_bottom_color = sky_horizon.darkened(0.7)
	psm.sun_angle_max = 12.0
	psm.sun_curve = 0.08
	psm.energy_multiplier = 1.0
	sky.sky_material = psm
	sky.radiance_size = Sky.RADIANCE_SIZE_256
	env.background_mode = Environment.BG_SKY
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = ambient
	env.ambient_light_energy = ambient_energy
	env.reflected_light_source = Environment.REFLECTION_SOURCE_SKY
	# AgX keeps practical lights and sunlit concrete from clipping to flat white.
	env.tonemap_mode = Environment.TONE_MAPPER_AGX
	env.tonemap_exposure = exposure * 1.6
	env.tonemap_white = 6.0
	env.ssao_enabled = true
	env.ssao_radius = 1.1
	env.ssao_intensity = 2.2
	env.ssao_power = 1.6
	env.ssao_detail = 0.6
	env.ssao_horizon = 0.06
	env.ssao_light_affect = 0.08
	env.ssao_ao_channel_affect = 0.4
	var q: int = Settings.graphics_quality
	if q >= 1:
		env.ssil_enabled = true
		env.ssil_radius = 4.0
		env.ssil_intensity = 0.9
		env.ssil_sharpness = 0.98
		env.ssil_normal_rejection = 1.0
	if q >= 2:
		# SDFGI was evaluated (docs/phase03/VISUAL_QUALITY_REPORT.md): in these enclosed concrete rooms it
		# replaced the ambient fill and leaked black through 0.25 m walls, so high quality uses SSIL + fog.
		env.volumetric_fog_enabled = true
		env.volumetric_fog_density = 0.006 + fog * 2.0
		env.volumetric_fog_albedo = Color(0.85, 0.85, 0.82)
		env.volumetric_fog_emission = Color.BLACK
		env.volumetric_fog_anisotropy = 0.35
		env.volumetric_fog_length = 48.0
		env.volumetric_fog_detail_spread = 2.0
		env.volumetric_fog_gi_inject = 0.6
		env.volumetric_fog_ambient_inject = 0.15
		env.volumetric_fog_temporal_reprojection_enabled = true
	elif fog > 0.0:
		env.fog_enabled = true
		env.fog_density = fog
		env.fog_light_color = sky_horizon
	env.glow_enabled = true
	env.glow_intensity = 0.35
	env.glow_strength = 0.9
	env.glow_bloom = 0.02
	env.glow_hdr_threshold = 1.4
	env.glow_blend_mode = Environment.GLOW_BLEND_MODE_SOFTLIGHT
	env.adjustment_enabled = true
	env.adjustment_contrast = 1.06
	env.adjustment_saturation = 0.92
	we.environment = env
	root.add_child(we)
	_environment = env
	if _has_sun:
		for n in root.get_children():
			if n is DirectionalLight3D:
				_configure_outdoor(env, n)
	return we


func _configure_outdoor(env: Environment, sun_light: DirectionalLight3D) -> void:
	env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	env.ambient_light_sky_contribution = 0.85
	env.ambient_light_energy = maxf(env.ambient_light_energy, 1.0)
	var psm := env.sky.sky_material as ProceduralSkyMaterial
	if psm:
		psm.sky_top_color = Color(0.22, 0.38, 0.62)
		psm.sky_horizon_color = Color(0.66, 0.72, 0.78)
		psm.ground_horizon_color = Color(0.55, 0.56, 0.55)
		psm.ground_bottom_color = Color(0.2, 0.2, 0.19)
		psm.sun_angle_max = 30.0
	if env.volumetric_fog_enabled:
		env.volumetric_fog_density = 0.0025
		env.volumetric_fog_anisotropy = 0.6
		env.volumetric_fog_ambient_inject = 0.3
	else:
		env.fog_enabled = true
		env.fog_density = 0.0015
		env.fog_light_color = Color(0.7, 0.75, 0.8)
		env.fog_sun_scatter = 0.25
		env.fog_sky_affect = 0.15


func bake() -> void:
	nav.bake_navigation_mesh(false)
