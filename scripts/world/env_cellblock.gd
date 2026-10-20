class_name EnvCellblock
extends RefCounted
## ENV_CELLBLOCK (docs/environments/CELL_BLOCK.md), Godot coordinates = drafting (x + 26, y, 3 - z).
## Hall x26..56 / z3..-15, hero cells C13 x36..39 and C14 x39..42 (3 m frontage, doors at x37.5/40.5 on z=-3),
## common service chase behind the south bank (z3..4.8) turning north at x52.4..54.4 to exit beside the C5 pier,
## service door on the east wall into the restricted corridor (x56..64) ending at the manual gate C6.
## Approved alternative: hall east wall at drafting x30 (not 32) so the corridor starts at the service door.

const OX := 26.0
const OZ := 3.0


static func build(b: EnvBuilder, night: bool) -> Dictionary:
	# Phase 03: sealed slab, painted CMU (cream upper, slate-blue dado), painted soffits; the service chase
	# keeps bare concrete. Door frames and skirting come from wall_trim.
	var concrete := b.sealed_floor(Color(0.6, 0.6, 0.58), 0.22, true)
	var wallm := b.paint(Color(0.82, 0.81, 0.75), true)
	var cellwall := b.paint(Color(0.84, 0.83, 0.78), true)
	var soffit := b.paint(Color(0.72, 0.72, 0.7))
	var dark := b.mat("concrete_slab_wall", Color(0.7, 0.7, 0.7), 0.4)
	var steel := b.paint(Color(0.2, 0.24, 0.26), false, 0.42)
	var hall_trim := {"dado": b.paint(Color(0.24, 0.31, 0.38), false, 0.45), "dado_h": 1.3, "line": b.paint(Color(0.1, 0.12, 0.13), false, 0.4),
		"skirt": b.paint(Color(0.12, 0.13, 0.13), false, 0.5), "frame": steel}
	var out := {"doors": {}}
	# floors and ceilings
	b.floor_rect(26, 3, 56, -15, concrete)
	b.floor_rect(35.6, 4.8, 54.4, 3, dark)          # chase south strip
	b.floor_rect(52.15, 3, 54.4, -3, dark)           # chase north leg (widened 0.25 m: D04-011 wall snag)
	b.floor_rect(56, -5, 64, -8, concrete)           # restricted corridor
	b.floor_rect(24, -5, 26, -7, concrete)           # vestibule from intake
	b.ceiling_rect(26, -3, 56, -15, 6.0, soffit)
	b.ceiling_rect(26, 3, 56, -3, 6.0, soffit)       # over the south upper tier and its walkway
	b.ceiling_beams(26, -3, 56, -9, 6.0, 4.0, false, soffit, 0.5)
	b.ceiling_rect(28, 3, 52, -3, 3.0, soffit)       # cell ceilings 3 m
	b.ceiling_rect(35.6, 4.8, 54.4, 3, 2.4, dark)
	b.ceiling_rect(52.15, 3, 54.4, -3, 2.4, dark)
	b.ceiling_rect(56, -5, 64, -8, 3.0, dark)
	# hall perimeter
	b.wall_trim = hall_trim
	b.wall(Vector2(26, 3), Vector2(26, -15), 6.0, wallm, 0.3, [[8.0, 10.0]])          # west, C0 entry gap z-5..-7
	b.wall(Vector2(26, -15), Vector2(56, -15), 6.0, wallm, 0.3)                        # north
	b.wall(Vector2(56, -15), Vector2(56, 4.8), 6.0, wallm, 0.3, [[7.5, 9.5]])          # east, service door z-7.5..-5.5
	b.box(Vector3(27, 3.0, 0), Vector3(2, 6, 6), wallm)                                # filler west of cell bank
	b.box(Vector3(55.2, 3.0, 0.9), Vector3(1.6, 6, 7.8), wallm)                       # filler east of chase leg
	b.wall(Vector2(28, 3), Vector2(52, 3), 3.0, cellwall, 0.25)                        # cell rear wall (chase side)
	b.wall_trim = {}
	b.wall(Vector2(35.6, 4.8), Vector2(54.4, 4.8), 2.4, dark, 0.25)                   # chase outer wall
	b.wall(Vector2(35.6, 3), Vector2(35.6, 4.8), 2.4, dark, 0.25)                     # chase west end
	b.wall(Vector2(54.4, 4.8), Vector2(54.4, -3), 2.4, dark, 0.25)                    # chase leg east wall
	# Inaccessible upper tier over the south cells (was an invisible cap, which left sky visible over the
	# bank): set-back cell wall with steel doors, walkway slab and an edge railing. No stairs reach it.
	_upper_tier(b, 0.0, 3.0, -3.0, wallm, steel, hall_trim)
	# south cells: dividers, fronts, hero cells 13/14
	b.wall_trim = hall_trim
	for x in [28.0, 32.0, 36.0, 39.0, 42.0, 46.0, 49.0, 52.0]:
		b.wall(Vector2(x, 3), Vector2(x, -3), 3.0, cellwall, 0.2)
	b.wall_trim = {}
	b.wall(Vector2(52.15, 3), Vector2(52.15, -3), 2.4, dark, 0.2)                     # chase leg west wall
	for c in [[28.0, 32.0], [32.0, 36.0], [42.0, 46.0], [46.0, 49.0], [49.0, 52.0]]:
		_cell_front(b, c[0], c[1], -3.0, false)
		_bed(b, Vector3(c[0] + 0.6, 0, 0.4))
		b.omni(Vector3((c[0] + c[1]) * 0.5, 2.6, 0), Color(0.95, 0.94, 0.90), 0.65 if not night else 0.18, 4.0)
	for c in [[13, 36.0, 39.0], [14, 39.0, 42.0]]:
		_cell_front(b, c[1], c[2], -3.0, true)
		var door := Door.make(b, "CellDoor%d" % c[0], EnvBuilder.ENV + "cell_door_1m.glb", Vector3(c[1] + 1.0, 0, -3.0), 0, Vector3(1.0, 2.2, 0.12))
		door.open_angle = 95.0
		out["doors"]["C%d" % c[0]] = door
		_bed(b, Vector3(c[1] + 0.55, 0, 1.6))
		b.model(EnvBuilder.PROP + "sink.glb", Vector3(c[2] - 0.35, 0, 2.6), 180, "box")
		b.model(EnvBuilder.PROP + "toilet.glb", Vector3(c[2] - 0.35, 0, 1.4), 270, "box")
		out["panel%d_in" % c[0]] = b.model(EnvBuilder.PROP + "service_panel.glb", Vector3(c[1] + 1.5, 0.15, 2.84), 180, "none")
		for mi in (out["panel%d_in" % c[0]] as Node3D).find_children("*", "MeshInstance3D", true, false):   # light painted steel reads against the dado
			(mi as MeshInstance3D).material_override = b.paint(Color(0.6, 0.62, 0.6), false, 0.45)
		out["panel%d_out" % c[0]] = b.model(EnvBuilder.PROP + "service_panel.glb", Vector3(c[1] + 1.5, 0.15, 3.16), 0, "none")
		b.model(EnvBuilder.PROP + "pipe_straight_2m.glb", Vector3(c[2] - 0.12, 0, 2.85), 0, "none")
		b.omni(Vector3(c[1] + 1.5, 2.7, 0), Color(1.0, 0.92, 0.8) if not night else Color(0.55, 0.65, 1.0), 0.9 if not night else 0.6, 5.0)
	out["cell13"] = {"inside": Vector3(37.5, 0, -1.0), "mark": Vector3(37.5, 0, -2.0), "door_out": Vector3(37.5, 0, -4.2), "sink": Vector3(38.5, 0, 2.3),
		"door": Vector3(37.5, 0, -2.6), "panel": Vector3(37.5, 0, 2.4), "panel_chase": Vector3(37.5, 0, 3.9)}
	out["cell14"] = {"inside": Vector3(40.5, 0, -1.0), "mark": Vector3(40.5, 0, -2.0), "door_out": Vector3(40.5, 0, -4.2), "sink": Vector3(41.5, 0, 2.3),
		"door": Vector3(40.5, 0, -2.6), "panel": Vector3(40.5, 0, 2.4), "panel_chase": Vector3(40.5, 0, 3.9)}
	# north cell bank (inaccessible, visible locked fronts)
	b.wall(Vector2(26, -9), Vector2(28, -9), 6.0, wallm, 0.3)
	b.wall(Vector2(52, -9), Vector2(56, -9.0), 6.0, wallm, 0.3)
	b.wall_trim = hall_trim
	for c in [[28.0, 32.0], [32.0, 36.0], [36.0, 40.0], [40.0, 44.0], [44.0, 48.0], [48.0, 52.0]]:
		_cell_front(b, c[0], c[1], -9.0, false, 180.0)
		b.wall(Vector2(c[0], -9), Vector2(c[0], -15), 3.0, cellwall, 0.2)
		_bed(b, Vector3(c[0] + 0.6, 0, -13.6))
	b.wall_trim = {}
	b.ceiling_rect(28, -9, 52, -15, 3.0, soffit)
	_upper_tier(b, -12.0, -15.0, -9.0, wallm, steel, hall_trim, 26)
	# cell numbers over every door (south bank faces the hall to the north, north bank to the south)
	var south_cells := [[28.0, 11], [32.0, 12], [36.0, 13], [39.0, 14], [42.0, 15], [46.0, 16], [49.0, 17]]
	for c in south_cells:
		b.sign("A-%02d" % c[1], Vector3(c[0] + 1.5, 2.62, -3.09), 180.0, 0.34)
	for i in 6:
		b.sign("A-%02d" % (i + 1), Vector3(28.0 + i * 4.0 + 1.5, 2.62, -8.91), 0.0, 0.34)
	b.sign("CELL BLOCK A", Vector3(26.16, 3.0, -6.0), 90.0, 1.4)
	b.sign("STAFF ONLY — SERVICE CORRIDOR", Vector3(55.84, 2.7, -4.6), -90.0, 1.0, Color(0.75, 0.12, 0.08), Color(0.97, 0.97, 0.95))
	b.floor_line(Vector3(28.0, 0, -3.65), Vector3(52.0, 0, -3.65), 0.08, Color(0.7, 0.12, 0.1))
	b.floor_line(Vector3(28.0, 0, -8.35), Vector3(52.0, 0, -8.35), 0.08, Color(0.7, 0.12, 0.1))
	# piers (genuine occluders) and restricted corridor
	for p in [Vector3(53.1, 0, -4.3), Vector3(31.0, 0, -9.6), Vector3(41.0, 0, -9.6), Vector3(47.0, 0, -3.5)]:
		b.model(EnvBuilder.ENV + "corner_pier.glb", p, 0, "none")
		b.box(p + Vector3(0, 1.5, 0), Vector3(0.7, 3.0, 0.7), null, null, false)
	out["pier_c5"] = Vector3(53.1, 0, -4.3)
	out["chase_exit"] = Vector3(53.4, 0, -2.3)
	out["chase_mid"] = Vector3(45.0, 0, 3.9)
	out["chase_corner"] = Vector3(53.4, 0, 3.9)
	out["behind_pier"] = Vector3(53.5, 0, -5.3)
	b.wall(Vector2(56, -5), Vector2(64, -5), 3.0, cellwall, 0.25)
	b.wall(Vector2(56, -8), Vector2(64, -8), 3.0, cellwall, 0.25)
	b.wall(Vector2(64, -5), Vector2(64, -8), 3.0, cellwall, 0.25)
	b.model(EnvBuilder.ENV + "security_door_12.glb", Vector3(63.8, 0, -7.1), 90, "none")
	out["gate_c6"] = Vector3(62.8, 0, -6.5)
	out["service_door"] = Vector3(56.0, 0, -6.5)
	out["corridor_mid"] = Vector3(59.0, 0, -6.5)
	b.wall(Vector2(24, -5), Vector2(26, -5), 4.0, wallm, 0.25)
	b.wall(Vector2(24, -7), Vector2(26, -7), 4.0, wallm, 0.25)
	out["c0"] = Vector3(27.0, 0, -6.0)
	out["c1"] = Vector3(30.0, 0, -6.0)
	out["c2"] = Vector3(52.0, 0, -9.6)
	# guard desk and fixtures
	b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(29.0, 0, -12.5), 90, "box")
	b.scanned_prop("SchoolChair_01", Vector3(29.9, 0, -12.5), 270, 0.95)
	b.box(Vector3(29.9, 0.45, -12.5), Vector3(0.6, 0.9, 0.55), null, null, false)
	b.model("res://assets/props/acquisition_20261019/radio_yaesu_single_metric.glb", Vector3(29.0, 0.79, -12.2), 20, "none")
	# Wall-mounted scanned fittings add construction detail above the walkable corridor.
	for x in [33.0, 45.0, 53.5]:
		var practical := b.model("res://assets/props/phase025/industrial_wall_lamp/industrial_wall_lamp_1k.gltf", Vector3(x, 2.6, -3.12), 180, "none")
		practical.name = "CagedWallPractical"
	b.scanned_prop("utility_box_01", Vector3(63.55, 0.7, -5.5), 270, 0.9)
	if night:
		b.environment(Color(0.02, 0.03, 0.06), Color(0.05, 0.06, 0.1), Color(0.35, 0.42, 0.6), 0.25, 0.0, 0.9)
		for x in range(28, 56, 4):
			b.model(EnvBuilder.PROP + "fluorescent_fixture.glb", Vector3(x, 5.42, -6), 90, "none")   # switched off at count
		for x in [32.0, 44.0, 54.0]:
			b.omni(Vector3(x, 4.5, -6.5), Color(0.45, 0.55, 1.0), 1.1, 12.0)
		b.omni(Vector3(29.0, 2.2, -12.0), Color(1.0, 0.75, 0.45), 2.2, 6.0, true)   # warm guard desk
		b.omni(Vector3(53.4, 2.0, 0.0), Color(1.0, 0.6, 0.25), 0.6, 5.0)            # dim amber chase practical
		for x in [38.0, 43.5, 49.0]:                                                # caged service lamps along the chase
			EnvBuilder.no_shadow(b.model("res://assets/props/phase025/industrial_wall_lamp/industrial_wall_lamp_1k.gltf", Vector3(x, 2.05, 4.68), 180, "none"))
			b.omni(Vector3(x, 1.95, 4.3), Color(1.0, 0.68, 0.36), 0.75, 4.5)
		b.omni(Vector3(60.0, 2.6, -6.5), Color(1.0, 0.65, 0.3), 1.0, 6.0)
	else:
		b.environment(Color(0.55, 0.6, 0.68), Color(0.7, 0.72, 0.75), Color(0.75, 0.8, 0.9), 0.32, 0.0, 1.0)
		# High-bay fluorescent run hung below the beams down the circulation lane.
		for x in range(28, 56, 4):
			b.ceiling_light(Vector3(x, 5.42, -6), Color(0.94, 0.96, 1.0), 3.2, 10.0, x in [36, 48])
		b.omni(Vector3(60.0, 2.6, -6.5), Color(0.92, 0.96, 1.0), 1.4, 6.0)
	return out


static func _bed(b: EnvBuilder, pos: Vector3) -> void:
	# Keep the original AABB collision/nav shape exactly. The more detailed welded frame,
	# sewn mattress, pillow and draped blanket fit within that same authored footprint.
	var envelope := b.model("res://assets/props/phase025/prison_bed.glb", pos, 0, "box")
	for mesh in envelope.find_children("*", "MeshInstance3D", true, false):
		(mesh as MeshInstance3D).visible = false
	b.model("res://assets/props/phase04_architecture/prison_bunk.glb", pos, 0, "none")


## Bars and a door along a cell front (static unless the hero door replaces the door module).
static func _cell_front(b: EnvBuilder, x0: float, x1: float, z: float, hero: bool, yaw := 0.0) -> void:
	var door_x := x0 + 1.0
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(x0, 0, z), Vector3(door_x, 0, z), 3.06, 3.0, 0.12)
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(door_x + 1.0, 0, z), Vector3(x1, 0, z), 3.06, 3.0, 0.12)
	b.box(Vector3(door_x + 0.5, 2.6, z), Vector3(1.0, 0.8, 0.12), null, null, false)
	if not hero:
		b.model(EnvBuilder.ENV + "cell_door_1m.glb", Vector3(door_x, 0, z), yaw, "none")
		b.box(Vector3(door_x + 0.5, 1.1, z), Vector3(1.0, 2.2, 0.12), null, null, false)


## Upper cell tier seen from the ground gallery: cell wall set back to z_wall, slab edge at z_edge, railing.
static func _upper_tier(b: EnvBuilder, z_wall: float, z_back: float, z_edge: float, wallm: Material, steel: Material, trim: Dictionary, first_number := 18) -> void:
	var zc := (z_wall + z_back) / 2.0
	b.box(Vector3(40, 4.65, zc), Vector3(24, 2.7, absf(z_back - z_wall)), wallm)
	b.box(Vector3(40, 3.16, (z_edge + z_wall) / 2.0), Vector3(24, 0.3, absf(z_wall - z_edge)), steel)     # walkway slab (1 cm proud of the cell soffit slab)
	var out_z := z_wall - 0.01 if z_edge < z_wall else z_wall + 0.01
	var yaw := 180.0 if z_edge < z_wall else 0.0
	var x := 29.5
	while x < 52.0:
		# Original detailed welded assembly: framed vision grille, food pass, lock, hinges,
		# pull handle, louvres and kick plate. Visual only; inaccessible tier collision unchanged.
		b.model("res://assets/props/phase04_cellblock/tier_security_door.glb", Vector3(x, 3.3, out_z + (-0.04 if yaw == 180.0 else 0.04)), yaw, "none")
		b.sign("A-%02d" % (first_number + int((x - 29.5) / 3.0)), Vector3(x, 3.3 + 2.3, out_z + (-0.03 if yaw == 180.0 else 0.03)), yaw, 0.32)
		x += 3.0
	if not trim.is_empty():
		var dado: Material = trim["dado"]
		b.visual_box(Vector3(40, 3.3 + 0.65, out_z + (-0.006 if yaw == 180.0 else 0.006)), Vector3(24, 1.3, 0.008), dado)
	b.run(EnvBuilder.ENV + "railing_2m.glb", Vector3(28, 3.3, z_edge), Vector3(52, 3.3, z_edge), 2.0, 1.1, 0.05, false)
	b.visual_box(Vector3(40, 3.0, z_edge), Vector3(24, 0.3, 0.12), steel)                                  # slab edge fascia

