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
	var concrete := b.mat("concrete_floor_worn_001", Color(1, 1, 1), 0.35)
	var wallm := b.mat("painted_concrete", Color(0.85, 0.87, 0.9), 0.4)
	var cellwall := b.mat("concrete_block_wall", Color(0.9, 0.9, 0.88), 0.4)
	var dark := b.mat("concrete_slab_wall", Color(0.7, 0.7, 0.7), 0.4)
	var out := {"doors": {}}
	# floors and ceilings
	b.floor_rect(26, 3, 56, -15, concrete)
	b.floor_rect(35.6, 4.8, 54.4, 3, dark)          # chase south strip
	b.floor_rect(52.4, 3, 54.4, -3, dark)            # chase north leg
	b.floor_rect(56, -5, 64, -8, concrete)           # restricted corridor
	b.floor_rect(24, -5, 26, -7, concrete)           # vestibule from intake
	b.ceiling_rect(26, -3, 56, -15, 6.0, dark)
	b.ceiling_rect(28, 3, 52, -3, 3.0, dark)         # cell ceilings 3 m
	b.ceiling_rect(35.6, 4.8, 54.4, 3, 2.4, dark)
	b.ceiling_rect(52.4, 3, 54.4, -3, 2.4, dark)
	b.ceiling_rect(56, -5, 64, -8, 3.0, dark)
	# hall perimeter
	b.wall(Vector2(26, 3), Vector2(26, -15), 6.0, wallm, 0.3, [[8.0, 10.0]])          # west, C0 entry gap z-5..-7
	b.wall(Vector2(26, -15), Vector2(56, -15), 6.0, wallm, 0.3)                        # north
	b.wall(Vector2(56, -15), Vector2(56, 4.8), 6.0, wallm, 0.3, [[7.5, 9.5]])          # east, service door z-7.5..-5.5
	b.box(Vector3(27, 3.0, 0), Vector3(2, 6, 6), wallm)                                # filler west of cell bank
	b.box(Vector3(55.2, 3.0, 0.9), Vector3(1.6, 6, 7.8), wallm)                       # filler east of chase leg
	b.wall(Vector2(28, 3), Vector2(52, 3), 3.0, cellwall, 0.25)                        # cell rear wall (chase side)
	b.wall(Vector2(35.6, 4.8), Vector2(54.4, 4.8), 2.4, dark, 0.25)                   # chase outer wall
	b.wall(Vector2(35.6, 3), Vector2(35.6, 4.8), 2.4, dark, 0.25)                     # chase west end
	b.wall(Vector2(54.4, 4.8), Vector2(54.4, -3), 2.4, dark, 0.25)                    # chase leg east wall
	b.box(Vector3(40, 4.5, 0), Vector3(24, 3, 6), dark, null, false)                  # invisible cap above cell ceilings
	# south cells: dividers, fronts, hero cells 13/14
	for x in [28.0, 32.0, 36.0, 39.0, 42.0, 46.0, 49.0, 52.0]:
		b.wall(Vector2(x, 3), Vector2(x, -3), 3.0, cellwall, 0.2)
	b.wall(Vector2(52.4, 3), Vector2(52.4, -3), 2.4, dark, 0.2)                       # chase leg west wall
	for c in [[28.0, 32.0], [32.0, 36.0], [42.0, 46.0], [46.0, 49.0], [49.0, 52.0]]:
		_cell_front(b, c[0], c[1], -3.0, false)
		b.model(EnvBuilder.PROP + "cell_bed.glb", Vector3(c[0] + 0.6, 0, 0.4), 0, "box")
	for c in [[13, 36.0, 39.0], [14, 39.0, 42.0]]:
		_cell_front(b, c[1], c[2], -3.0, true)
		var door := Door.make(b, "CellDoor%d" % c[0], EnvBuilder.ENV + "cell_door_1m.glb", Vector3(c[1] + 1.0, 0, -3.0), 0, Vector3(1.0, 2.2, 0.12))
		door.open_angle = 95.0
		out["doors"]["C%d" % c[0]] = door
		b.model(EnvBuilder.PROP + "cell_bed.glb", Vector3(c[1] + 0.55, 0, 1.6), 0, "box")
		b.model(EnvBuilder.PROP + "sink.glb", Vector3(c[2] - 0.35, 0, 2.6), 180, "box")
		b.model(EnvBuilder.PROP + "toilet.glb", Vector3(c[2] - 0.35, 0, 1.4), 270, "box")
		out["panel%d_in" % c[0]] = b.model(EnvBuilder.PROP + "service_panel.glb", Vector3(c[1] + 1.5, 0.15, 2.84), 180, "none")
		out["panel%d_out" % c[0]] = b.model(EnvBuilder.PROP + "service_panel.glb", Vector3(c[1] + 1.5, 0.15, 3.16), 0, "none")
		b.model(EnvBuilder.PROP + "pipe_straight_2m.glb", Vector3(c[2] - 0.12, 0, 2.85), 0, "none")
		b.omni(Vector3(c[1] + 1.5, 2.7, 0), Color(1.0, 0.92, 0.8) if not night else Color(0.55, 0.65, 1.0), 0.9 if not night else 0.35, 5.0)
	out["cell13"] = {"inside": Vector3(37.5, 0, -1.0), "mark": Vector3(37.5, 0, -2.0), "door_out": Vector3(37.5, 0, -4.2), "sink": Vector3(38.5, 0, 2.3),
		"door": Vector3(37.5, 0, -2.6), "panel": Vector3(37.5, 0, 2.4), "panel_chase": Vector3(37.5, 0, 3.9)}
	out["cell14"] = {"inside": Vector3(40.5, 0, -1.0), "mark": Vector3(40.5, 0, -2.0), "door_out": Vector3(40.5, 0, -4.2), "sink": Vector3(41.5, 0, 2.3),
		"door": Vector3(40.5, 0, -2.6), "panel": Vector3(40.5, 0, 2.4), "panel_chase": Vector3(40.5, 0, 3.9)}
	# north cell bank (inaccessible, visible locked fronts)
	b.wall(Vector2(26, -9), Vector2(28, -9), 6.0, wallm, 0.3)
	b.wall(Vector2(52, -9), Vector2(56, -9.0), 6.0, wallm, 0.3)
	for c in [[28.0, 32.0], [32.0, 36.0], [36.0, 40.0], [40.0, 44.0], [44.0, 48.0], [48.0, 52.0]]:
		_cell_front(b, c[0], c[1], -9.0, false, 180.0)
		b.wall(Vector2(c[0], -9), Vector2(c[0], -15), 3.0, cellwall, 0.2)
		b.model(EnvBuilder.PROP + "cell_bed.glb", Vector3(c[0] + 0.6, 0, -13.6), 0, "box")
	b.box(Vector3(40, 4.5, -12), Vector3(24, 3, 6), wallm)                            # gallery slab above north cells
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
	b.model(EnvBuilder.PROP + "steel_chair.glb", Vector3(29.9, 0, -12.5), 270, "box")
	b.model("res://assets/props/acquisition_20261019/radio_yaesu_single_metric.glb", Vector3(29.0, 0.79, -12.2), 20, "none")
	for x in range(30, 56, 6):
		b.model(EnvBuilder.PROP + "fluorescent_fixture.glb", Vector3(x, 5.85, -6), 90, "none")
		b.model(EnvBuilder.PROP + "fluorescent_fixture.glb", Vector3(x, 5.85, -12), 90, "none")
	if night:
		b.environment(Color(0.02, 0.03, 0.06), Color(0.05, 0.06, 0.1), Color(0.35, 0.42, 0.6), 0.25, 0.0, 0.9)
		for x in [32.0, 44.0, 54.0]:
			b.omni(Vector3(x, 4.5, -6.5), Color(0.45, 0.55, 1.0), 1.1, 12.0)
		b.omni(Vector3(29.0, 2.2, -12.0), Color(1.0, 0.75, 0.45), 2.2, 6.0, true)   # warm guard desk
		b.omni(Vector3(53.4, 2.0, 0.0), Color(1.0, 0.6, 0.25), 0.6, 5.0)            # dim amber chase practical
		b.omni(Vector3(60.0, 2.6, -6.5), Color(1.0, 0.65, 0.3), 1.0, 6.0)
	else:
		b.environment(Color(0.55, 0.6, 0.68), Color(0.7, 0.72, 0.75), Color(0.75, 0.8, 0.9), 0.55, 0.0, 1.0)
		for x in range(30, 56, 6):
			b.omni(Vector3(x, 5.2, -6), Color(0.92, 0.96, 1.0), 2.4, 12.0, x == 36)
		b.omni(Vector3(60.0, 2.6, -6.5), Color(0.92, 0.96, 1.0), 1.4, 6.0)
	return out


## Bars and a door along a cell front (static unless the hero door replaces the door module).
static func _cell_front(b: EnvBuilder, x0: float, x1: float, z: float, hero: bool, yaw := 0.0) -> void:
	var door_x := x0 + 1.0
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(x0, 0, z), Vector3(door_x, 0, z), 3.06, 3.0, 0.12)
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(door_x + 1.0, 0, z), Vector3(x1, 0, z), 3.06, 3.0, 0.12)
	b.box(Vector3(door_x + 0.5, 2.6, z), Vector3(1.0, 0.8, 0.12), null, null, false)
	if not hero:
		b.model(EnvBuilder.ENV + "cell_door_1m.glb", Vector3(door_x, 0, z), yaw, "none")
		b.box(Vector3(door_x + 0.5, 1.1, z), Vector3(1.0, 2.2, 0.12), null, null, false)
