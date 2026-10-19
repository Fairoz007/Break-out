class_name EnvWorkshop
extends RefCounted
## ENV_WORKSHOP (docs/environments/LAUNDRY_WORKSHOP.md), Godot coordinates as specified (x, y, -z north).
## 30x20 m, ceiling 4.5 m. Press enclosure x8..17 / z-4..-9 behind a solid guard rail (players never enter
## moving equipment); interaction marks on the aisle side: lever W1 (10), screen W2 (12), diagram W3 (15),
## scrap bin W4 (16,-10.6). Mara's blue medical table W5 (22,-14), guard office x25..30 / z-15..-20, exit (30,-10).


static var _linen_mat: StandardMaterial3D


## Woven linen (Fabric030, ambientCG CC0), world-triplanar so folded stacks keep a fine weave.
static func _linen() -> StandardMaterial3D:
	if _linen_mat == null:
		_linen_mat = (load("res://assets/materials/acquisition_20261019/Fabric030/fabric030_godot4.tres") as StandardMaterial3D).duplicate()
		_linen_mat.uv1_triplanar = true
		_linen_mat.uv1_world_triplanar = true
		_linen_mat.uv1_scale = Vector3.ONE * 2.0
		_linen_mat.albedo_color = Color(0.95, 0.95, 0.93)
	return _linen_mat


static func build(b: EnvBuilder) -> Dictionary:
	# Phase 03: epoxy-sealed slab, painted CMU with an institutional green dado, painted soffit and beams.
	var floor_m := b.sealed_floor(Color(0.5, 0.56, 0.54), 0.22, true)
	var wallm := b.paint(Color(0.8, 0.81, 0.77))
	var block := b.paint(Color(0.82, 0.83, 0.78), true)
	var metal := b.mat("blue_metal_plate", Color(0.9, 0.9, 0.9), 0.5)
	var out := {"doors": {}}
	b.floor_rect(0, 0, 30, -20, floor_m)
	b.ceiling_rect(0, 0, 30, -20, 4.5, wallm)
	b.ceiling_beams(0, 0, 30, -20, 4.5, 5.0, true, wallm, 0.45)
	b.wall_trim = {"dado": b.paint(Color(0.3, 0.38, 0.33), false, 0.45), "dado_h": 1.3, "line": b.paint(Color(0.12, 0.14, 0.13), false, 0.4),
		"skirt": b.paint(Color(0.12, 0.13, 0.13), false, 0.5), "frame": b.paint(Color(0.2, 0.23, 0.25), false, 0.42)}
	b.wall(Vector2(0, 0), Vector2(30, 0), 4.5, block, 0.3)
	b.wall(Vector2(0, -20), Vector2(30, -20), 4.5, block, 0.3)
	b.wall(Vector2(0, 0), Vector2(0, -20), 4.5, block, 0.3, [[9.1, 10.9]])      # entry W0
	b.wall(Vector2(30, 0), Vector2(30, -20), 4.5, block, 0.3, [[9.1, 10.9]])    # exit
	# guard office with 1.2 m door and window band
	b.wall(Vector2(25, -15), Vector2(30, -15), 4.5, wallm, 0.2, [[1.4, 2.6]])
	b.wall(Vector2(25, -15), Vector2(25, -20), 4.5, wallm, 0.2)
	b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(28.4, 0, -18.6), 0, "box")
	b.scanned_prop("SchoolChair_01", Vector3(28.4, 0, -19.3), 0, 0.95)
	b.box(Vector3(28.4, 0.45, -19.3), Vector3(0.55, 0.9, 0.6), null, null, false)
	b.model(EnvBuilder.PROP + "guard_radio.glb", Vector3(28.0, 0.79, -18.5), 0, "none")
	# press enclosure: machines behind a guard rail with full collision
	b.model(EnvBuilder.PROP + "laundry_press.glb", Vector3(10.6, 0, -6.6), 0, "box")
	b.model(EnvBuilder.PROP + "laundry_press.glb", Vector3(13.4, 0, -6.6), 0, "box")
	for x in [9.0, 10.2, 15.0, 16.2]:
		b.model(EnvBuilder.PROP + "laundry_washer.glb", Vector3(x, 0, -4.8), 180, "box")
	# Retain the safety collision envelope while showing steel guard rails instead of solid box walls.
	b.box(Vector3(12.5, 0.55, -9.15), Vector3(9.0, 1.1, 0.12), null, null, false)
	b.box(Vector3(8.0, 0.55, -6.6), Vector3(0.12, 1.1, 5.2), null, null, false)
	b.box(Vector3(17.0, 0.55, -6.6), Vector3(0.12, 1.1, 5.2), null, null, false)
	for rail_y in [0.15, 0.6, 1.1]:
		b.box(Vector3(12.5, rail_y, -9.15), Vector3(9.0, 0.07, 0.07), metal)
		for rail_x in [8.0, 17.0]:
			b.box(Vector3(rail_x, rail_y, -6.6), Vector3(0.07, 0.07, 5.2), metal)
	for rail_x in [8.0, 9.5, 11.0, 12.5, 14.0, 15.5, 17.0]:
		b.box(Vector3(rail_x, 0.55, -9.15), Vector3(0.08, 1.1, 0.08), metal)
	b.box(Vector3(12.5, 1.6, -9.1), Vector3(9.0, 1.0, 0.02), null, null, false)       # invisible upper guard
	b.model("res://assets/props/phase03/lint_screen.glb", Vector3(11.95, 1.05, -9.25), 180, "none")   # lint screen W2 (frame, mesh, pull handles)
	b.model("res://assets/props/phase03/isolation_switch.glb", Vector3(10.0, 0, -9.42), 0, "none")   # press isolation switch W1 (M03 lever)
	b.model(EnvBuilder.PROP + "maintenance_diagram.glb", Vector3(15.0, 1.15, -9.22), 0, "none")
	# work benches, linens, Mara's blue table, scrap bin, trolley
	for x in [20.5, 23.5]:
		b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(x, 0, -5.5), 0, "box")
		b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(x, 0, -7.4), 0, "box")
		b.box(Vector3(x, 0.86, -5.5), Vector3(1.0, 0.14, 0.5), _linen(), null, true)
	b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(22, 0, -14.4), 0, "box")
	b.box(Vector3(22, 0.8, -14.4), Vector3(1.42, 0.03, 0.72), b.flat(Color(0.2, 0.35, 0.65)))
	b.box(Vector3(21.7, 0.88, -14.4), Vector3(0.6, 0.12, 0.4), _linen())
	b.model(EnvBuilder.PROP + "scrap_bin.glb", Vector3(16.0, 0, -10.9), 0, "box")
	b.model("res://assets/props/acquisition_20261019/industrial_dryer_ironing.glb", Vector3(24.0, 0, -2.8), 0, "box")
	b.model(EnvBuilder.PROP + "linen_trolley.glb", Vector3(24.2, 0, -12.9), 90, "box")
	b.model("res://assets/props/phase025/tool_cart/tool_cart_1k.gltf", Vector3(3.5, 0, -2.0), 0, "box")
	b.model("res://assets/props/phase025/worn_metal_rack/worn_metal_rack_1k.gltf", Vector3(6, 0, -1.4), 180, "box")
	b.model("res://assets/props/phase025/metal_toolbox/metal_toolbox_1k.gltf", Vector3(20.6, 0.81, -7.4), 0, "none")
	# Real scanned support equipment; no new obstruction enters the cooperative aisle.
	b.model("res://assets/props/phase025/garden_hose_wall_mounted_01/garden_hose_wall_mounted_01_1k.gltf", Vector3(0.18, 1.2, -3.0), 90, "none")
	b.scanned_prop("utility_box_01", Vector3(29.5, 0.8, -3.6), 270, 1.1)
	b.scanned_prop("medical_box", Vector3(22.35, 0.83, -14.4), 10, 0.18)
	b.scanned_prop("metal_trash_can", Vector3(1, 0, -18.8), 0, 0.8)
	# Ceiling utility runs and wall plinths give the large room a functional industrial scale.
	var utility := b.mat("rusty_painted_metal", Color(0.65, 0.68, 0.66), 0.5)
	for pipe_z in [-3.0, -3.35]:
		for pipe_x in range(2, 29, 2):
			var pipe := b.model(EnvBuilder.PROP + "pipe_straight_2m.glb", Vector3(pipe_x, 3.85, pipe_z), 0, "none")
			pipe.rotation_degrees.z = 90.0
	# light: warm task lights against cold strips, daylight from high windows
	b.environment(Color(0.5, 0.56, 0.62), Color(0.66, 0.68, 0.7), Color(0.72, 0.76, 0.8), 0.3, 0.0, 1.0)
	b.wall_trim = {}
	# Fluorescent grid between the beams; shadowed fixtures over the press aisle, Mara's table and the bench line.
	for z in [-2.5, -7.5, -12.5, -17.5]:
		for x in [3.0, 8.0, 13.0, 18.0, 23.0, 28.0]:
			if z == -17.5 and x > 25.0:
				continue
			b.ceiling_light(Vector3(x, 4.42, z), Color(0.96, 0.97, 1.0), 2.4, 8.0, Vector2(x, z) in [Vector2(13.0, -7.5), Vector2(23.0, -12.5), Vector2(8.0, -12.5)])
	b.ceiling_light(Vector3(27.5, 4.42, -17.5), Color(1.0, 0.95, 0.86), 1.6, 6.0, false)    # guard office
	b.omni(Vector3(12.0, 2.4, -8.6), Color(1.0, 0.8, 0.55), 0.9, 4.0)                 # warm press task light
	# Aisle markings and signage
	for z in [-9.42, -12.6]:
		b.floor_line(Vector3(0.6, 0, z), Vector3(24.6, 0, z), 0.09, Color(0.85, 0.68, 0.08))
	b.sign("LAUNDRY  —  WORKSHOP 2", Vector3(12.0, 3.1, -0.16), 180.0, 1.8)
	b.sign("CAUTION
HOT SURFACES — KEEP BEHIND RAIL", Vector3(12.5, 2.3, -0.16), 180.0, 1.4, Color(0.85, 0.68, 0.08))
	b.sign("STAFF OFFICE", Vector3(27.0, 2.7, -14.89), 0.0, 0.9)
	b.sign("EXIT", Vector3(29.84, 2.7, -10.0), -90.0, 0.5, Color(0.1, 0.45, 0.2), Color(0.95, 0.97, 0.95))
	b.sign("ALL TOOLS SIGNED OUT
AND RETURNED BY COUNT", Vector3(0.16, 1.9, -6.0), 90.0, 1.1)
	out.merge({"adrian_start": Vector3(10.0, 0, -10.2), "noah_start": Vector3(12.0, 0, -10.6), "lever": Vector3(10.0, 1.0, -9.6),
		"screen": Vector3(11.95, 1.0, -9.6), "diagram": Vector3(14.7, 1.3, -9.6), "lamp_spot": Vector3(15.8, 1.0, -9.6),
		"scrap": Vector3(16.0, 0.8, -10.6), "mara": Vector3(22.0, 0, -13.5), "blue_table": Vector3(22.0, 0, -13.2),
		"office": Vector3(27.6, 0, -17.6), "office_door": Vector3(27.0, 0, -15.6), "rusk_aisle": Vector3(19.0, 0, -11.6),
		"rusk_lamp": Vector3(16.6, 0, -10.6), "rusk_mara": Vector3(23.2, 0, -13.0), "exit": Vector3(28.6, 0, -10.0)})
	return out
