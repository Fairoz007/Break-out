class_name EnvWorkshop
extends RefCounted
## ENV_WORKSHOP (docs/environments/LAUNDRY_WORKSHOP.md), Godot coordinates as specified (x, y, -z north).
## 30x20 m, ceiling 4.5 m. Press enclosure x8..17 / z-4..-9 behind a solid guard rail (players never enter
## moving equipment); interaction marks on the aisle side: lever W1 (10), screen W2 (12), diagram W3 (15),
## scrap bin W4 (16,-10.6). Mara's blue medical table W5 (22,-14), guard office x25..30 / z-15..-20, exit (30,-10).


static func build(b: EnvBuilder) -> Dictionary:
	var floor_m := b.mat("anti_slip_concrete", Color(0.85, 0.86, 0.88), 0.35)
	var wallm := b.mat("painted_concrete", Color(0.8, 0.84, 0.86), 0.4)
	var block := b.mat("concrete_block_wall", Color(0.88, 0.88, 0.86), 0.4)
	var metal := b.mat("blue_metal_plate", Color(0.9, 0.9, 0.9), 0.5)
	var out := {"doors": {}}
	b.floor_rect(0, 0, 30, -20, floor_m)
	b.ceiling_rect(0, 0, 30, -20, 4.5, wallm)
	b.wall(Vector2(0, 0), Vector2(30, 0), 4.5, block, 0.3)
	b.wall(Vector2(0, -20), Vector2(30, -20), 4.5, block, 0.3)
	b.wall(Vector2(0, 0), Vector2(0, -20), 4.5, block, 0.3, [[9.1, 10.9]])      # entry W0
	b.wall(Vector2(30, 0), Vector2(30, -20), 4.5, block, 0.3, [[9.1, 10.9]])    # exit
	# guard office with 1.2 m door and window band
	b.wall(Vector2(25, -15), Vector2(30, -15), 4.5, wallm, 0.2, [[1.4, 2.6]])
	b.wall(Vector2(25, -15), Vector2(25, -20), 4.5, wallm, 0.2)
	b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(28.4, 0, -18.6), 0, "box")
	b.model(EnvBuilder.PROP + "steel_chair.glb", Vector3(28.4, 0, -19.3), 0, "box")
	b.model(EnvBuilder.PROP + "guard_radio.glb", Vector3(28.0, 0.79, -18.5), 0, "none")
	# press enclosure: machines behind a guard rail with full collision
	b.model(EnvBuilder.PROP + "laundry_press.glb", Vector3(10.6, 0, -6.6), 0, "box")
	b.model(EnvBuilder.PROP + "laundry_press.glb", Vector3(13.4, 0, -6.6), 0, "box")
	for x in [9.0, 10.2, 15.0, 16.2]:
		b.model(EnvBuilder.PROP + "laundry_washer.glb", Vector3(x, 0, -4.8), 180, "box")
	b.box(Vector3(12.5, 0.55, -9.15), Vector3(9.0, 1.1, 0.12), metal)                # enclosure guard rail
	b.box(Vector3(8.0, 0.55, -6.6), Vector3(0.12, 1.1, 5.2), metal)
	b.box(Vector3(17.0, 0.55, -6.6), Vector3(0.12, 1.1, 5.2), metal)
	b.box(Vector3(12.5, 1.6, -9.1), Vector3(9.0, 1.0, 0.02), null, null, false)       # invisible upper guard
	b.box(Vector3(11.95, 1.05, -9.25), Vector3(0.7, 0.55, 0.04), b.flat(Color(0.55, 0.57, 0.6)))  # lint screen frame
	b.model(EnvBuilder.PROP + "electrical_panel.glb", Vector3(10.0, 0.4, -9.3), 0, "none")
	b.model(EnvBuilder.PROP + "maintenance_diagram.glb", Vector3(15.0, 1.15, -9.22), 0, "none")
	# work benches, linens, Mara's blue table, scrap bin, trolley
	for x in [20.5, 23.5]:
		b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(x, 0, -5.5), 0, "box")
		b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(x, 0, -7.4), 0, "box")
		b.box(Vector3(x, 0.86, -5.5), Vector3(1.0, 0.14, 0.5), b.flat(Color(0.92, 0.92, 0.9)), null, true)
	b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(22, 0, -14.4), 0, "box")
	b.box(Vector3(22, 0.8, -14.4), Vector3(1.42, 0.03, 0.72), b.flat(Color(0.2, 0.35, 0.65)))
	b.box(Vector3(21.7, 0.88, -14.4), Vector3(0.6, 0.12, 0.4), b.flat(Color(0.95, 0.95, 0.95)))
	b.model(EnvBuilder.PROP + "scrap_bin.glb", Vector3(16.0, 0, -10.9), 0, "box")
	b.model(EnvBuilder.PROP + "linen_trolley.glb", Vector3(24.2, 0, -12.9), 90, "box")
	for x in [4.0, 10.0, 16.0, 22.0, 27.0]:
		b.model(EnvBuilder.PROP + "fluorescent_fixture.glb", Vector3(x, 4.35, -11.5), 0, "none")
	# light: warm task lights against cold strips, daylight from high windows
	b.environment(Color(0.5, 0.56, 0.62), Color(0.66, 0.68, 0.7), Color(0.72, 0.76, 0.8), 0.45, 0.0, 1.0)
	for x in [4.0, 10.0, 16.0, 22.0, 27.0]:
		b.omni(Vector3(x, 4.0, -11.5), Color(0.86, 0.92, 1.0), 2.0, 10.0, x == 16.0)
	b.omni(Vector3(12.0, 2.4, -8.6), Color(1.0, 0.8, 0.55), 1.6, 5.0)                 # warm press task light
	b.omni(Vector3(22.0, 2.6, -13.6), Color(1.0, 0.95, 0.85), 1.2, 5.0)
	out.merge({"adrian_start": Vector3(10.0, 0, -10.2), "noah_start": Vector3(12.0, 0, -10.6), "lever": Vector3(10.0, 1.0, -9.6),
		"screen": Vector3(11.95, 1.0, -9.6), "diagram": Vector3(14.7, 1.3, -9.6), "lamp_spot": Vector3(15.8, 1.0, -9.6),
		"scrap": Vector3(16.0, 0.8, -10.6), "mara": Vector3(22.0, 0, -13.5), "blue_table": Vector3(22.0, 0, -13.2),
		"office": Vector3(27.6, 0, -17.6), "office_door": Vector3(27.0, 0, -15.6), "rusk_aisle": Vector3(19.0, 0, -11.6),
		"rusk_lamp": Vector3(16.6, 0, -10.6), "rusk_mara": Vector3(23.2, 0, -13.0), "exit": Vector3(28.6, 0, -10.0)})
	return out
