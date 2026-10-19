class_name EnvMaintenance
extends RefCounted
## ENV_MAINTENANCE (docs/environments/MAINTENANCE_NETWORK.md), Godot coordinates as specified (x, y, -z north).
## Entrance N0 (2,-3), manual gate (4,-6), split (8,-10). P1 west catwalk deck x8.4..10 / z-14..-23.5 at y2.5,
## reached by stairs from the split (approved alternative to the ladder, which stays as set dressing) and left by
## the north stair down to the reunion; P2 east floor route x21..23 blocked at z-23 by the 4 m lifting grille.
## A fenced, non-traversable pump well separates the routes. Reunion N6 (16,-24), pump console (18,-25.2),
## spillway door N7 at x30 (two handles 1.4 m apart), security grille beyond it, loading interception x30..38.

static func _ramp(b: EnvBuilder, from: Vector3, to: Vector3, width: float, material: Material) -> void:
	var run := Vector2(to.x - from.x, to.z - from.z)
	var length := Vector3(to - from).length()
	var body := b.box((from + to) / 2.0 + Vector3(0, -0.1, 0), Vector3(width, 0.2, length), material)
	body.look_at_from_position(body.position, body.position + (to - from), Vector3.UP)
	# visual stairs always rise from the low end toward the high end
	var lo := from if from.y <= to.y else to
	var hi := to if from.y <= to.y else from
	var up := Vector2(hi.x - lo.x, hi.z - lo.z)
	b.model(EnvBuilder.ENV + "stairs_17_risers_3m.glb", lo, rad_to_deg(atan2(-up.x, -up.y)), "none").scale = Vector3(width / 1.5, (hi.y - lo.y) / 3.0, up.length() / 4.5)


static func build(b: EnvBuilder) -> Dictionary:
	var floor_m := b.sealed_floor(Color(0.72, 0.73, 0.74), 0.25)
	var wallm := b.mat("concrete_slab_wall", Color(0.62, 0.64, 0.66), 0.35)
	var metal := b.mat("rusty_painted_metal", Color(0.85, 0.85, 0.85), 0.5)
	var grate := b.mat("metal_plate", Color(0.75, 0.75, 0.75), 0.6)
	var out := {"doors": {}}
	b.floor_rect(0, 0, 38, -27, floor_m)
	b.ceiling_rect(0, 0, 38, -27, 6.0, wallm)
	b.ceiling_beams(0, 0, 38, -27, 6.0, 6.0, false, wallm, 0.6)
	# Plant-room finish: bare board-formed concrete above a painted grey wear band; pressed-steel door frames.
	b.wall_trim = {"dado": b.paint(Color(0.3, 0.32, 0.33), false, 0.5), "dado_h": 1.5, "line": b.paint(Color(0.78, 0.6, 0.08), false, 0.45),
		"skirt": b.paint(Color(0.1, 0.1, 0.1), false, 0.5), "frame": b.paint(Color(0.22, 0.24, 0.25), false, 0.42)}
	b.wall(Vector2(0, 0), Vector2(38, 0), 6.0, wallm, 0.4)
	b.wall(Vector2(0, -27), Vector2(38, -27), 6.0, wallm, 0.4)
	b.wall(Vector2(0, 0), Vector2(0, -27), 6.0, wallm, 0.4)
	b.wall(Vector2(38, 0), Vector2(38, -27), 6.0, wallm, 0.4)
	# entrance chase and manual gate
	b.wall(Vector2(0, -6), Vector2(3.2, -6), 6.0, wallm, 0.3)
	b.wall(Vector2(4.8, -6), Vector2(20, -6), 6.0, wallm, 0.3)
	b.wall(Vector2(25, -6), Vector2(38, -6), 6.0, wallm, 0.3)
	var gate := Door.make(b, "ManualGate", EnvBuilder.ENV + "security_door_12.glb", Vector3(3.2, 0, -6), 0, Vector3(1.6, 2.25, 0.15))
	out["doors"]["manual_gate"] = gate
	b.wall_trim = {}
	# pump well between the routes: fenced, closed, non-traversable (not a lethal pit)
	b.box(Vector3(16.0, 0.03, -16.5), Vector3(7.6, 0.06, 13.0), b.flat(Color(0.08, 0.11, 0.12)))
	b.box(Vector3(16.0, 1.5, -16.5), Vector3(7.8, 3.0, 13.2), null, null, false)
	b.run(EnvBuilder.ENV + "railing_2m.glb", Vector3(12.1, 0, -10), Vector3(12.1, 0, -23), 2.0, 1.1, 0.05, false)
	b.run(EnvBuilder.ENV + "railing_2m.glb", Vector3(19.9, 0, -10), Vector3(19.9, 0, -23), 2.0, 1.1, 0.05, false)
	b.model(EnvBuilder.PROP + "pump_unit.glb", Vector3(16.0, 0, -16.5), 90, "none")
	b.model(EnvBuilder.PROP + "pump_unit.glb", Vector3(16.0, 0, -12.5), 90, "none")
	# east floor route walls (x 20..24) and the shared lifting grille at z-23
	b.wall(Vector2(24.4, -6), Vector2(24.4, -22.6), 6.0, wallm, 0.3)
	var grille := Door.make(b, "LiftingGrille", EnvBuilder.ENV + "security_grille_4m.glb", Vector3(22.2, 0, -23.0), 0, Vector3(4.4, 3.0, 0.3), Door.Kind.LIFT)
	grille.shape.position = Vector3(0, 1.5, 0)
	grille.lift_height = 2.9
	out["doors"]["grille"] = grille
	b.model(EnvBuilder.PROP + "mechanical_latch.glb", Vector3(22.2, 3.3, -22.7), 0, "none")
	b.model(EnvBuilder.PROP + "brake_station.glb", Vector3(23.9, 0, -19.0), 270, "box")
	b.model(EnvBuilder.PROP + "wired_handset.glb", Vector3(23.85, 1.25, -18.4), 270, "none")
	# west catwalk: stairs up from the split, deck at 2.5 m, north stair down to the reunion
	_ramp(b, Vector3(9.2, 0, -9.0), Vector3(9.2, 2.5, -14.0), 1.6, grate)
	b.box(Vector3(9.2, 2.4, -18.75), Vector3(1.6, 0.2, 9.5), grate)
	b.run(EnvBuilder.ENV + "railing_2m.glb", Vector3(10.05, 2.5, -14.0), Vector3(10.05, 2.5, -23.5), 2.0, 1.1, 0.06)
	b.run(EnvBuilder.ENV + "railing_2m.glb", Vector3(8.35, 2.5, -14.0), Vector3(8.35, 2.5, -23.5), 2.0, 1.1, 0.06)
	for z in range(-15, -23, -2):
		b.model(EnvBuilder.ENV + "catwalk_2m.glb", Vector3(9.2, 2.5, z), 90, "none")
	b.box(Vector3(10.7, 2.4, -24.3), Vector3(3.0, 0.2, 1.6), grate)                       # landing
	_ramp(b, Vector3(12.2, 2.5, -24.3), Vector3(16.2, 0.0, -24.3), 1.6, grate)
	b.model(EnvBuilder.ENV + "ladder_28.glb", Vector3(10.6, 0, -11.0), 270, "none")
	b.model(EnvBuilder.PROP + "electrical_panel.glb", Vector3(8.15, 2.5, -19.0), 90, "box")
	b.model(EnvBuilder.PROP + "wired_handset.glb", Vector3(8.2, 3.75, -19.7), 90, "none")
	b.box(Vector3(5.0, 3.0, -16.5), Vector3(6.0, 6.0, 15.0), wallm)                         # west solid mass (catwalk wall)
	b.box(Vector3(10.1, 1.1, -18.9), Vector3(4.2, 2.2, 9.4), wallm)                         # no floor passage under the deck
	b.box(Vector3(11.15, 1.1, -11.6), Vector3(2.1, 2.2, 5.2), wallm)                        # nor beside the stairs
	# reunion, pump console with the ledger, spillway door N7 and the loading interception
	b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(18.0, 0, -25.6), 0, "box")
	b.model(EnvBuilder.PROP + "electrical_panel.glb", Vector3(18.9, 0.79, -25.9), 0, "none")
	out["ledger_node"] = b.model(EnvBuilder.PROP + "transfer_ledger.glb", Vector3(17.6, 0.8, -25.5), 0, "none")
	b.model(EnvBuilder.PROP + "guard_radio.glb", Vector3(18.6, 0.79, -25.4), 0, "none")
	b.wall(Vector2(30, -6), Vector2(30, -23), 6.0, wallm, 0.4)
	b.wall(Vector2(30, -25), Vector2(30, -27), 6.0, wallm, 0.4)
	var spill := Door.make(b, "SpillwayDoor", EnvBuilder.ENV + "double_spillway_door.glb", Vector3(30.0, 0, -24.0), 90, Vector3(2.0, 2.5, 0.15), Door.Kind.SLIDE)
	spill.shape.position = Vector3(0, 1.25, 0)
	spill.slide = Vector3(0, 0, 0)
	out["doors"]["spillway"] = spill
	b.model(EnvBuilder.PROP + "dual_door_handle.glb", Vector3(29.85, 1.0, -24.0), 90, "none")
	var sec := Door.make(b, "SecurityGrille", EnvBuilder.ENV + "security_grille_4m.glb", Vector3(31.4, 0, -24.0), 90, Vector3(4.4, 3.0, 0.3), Door.Kind.LIFT)
	sec.shape.position = Vector3(0, 1.5, 0)
	out["doors"]["security_grille"] = sec
	var rear := Door.make(b, "RearGrille", EnvBuilder.ENV + "security_grille_4m.glb", Vector3(26.5, 0, -24.4), 90, Vector3(4.4, 3.0, 0.3), Door.Kind.LIFT)
	rear.shape.position = Vector3(0, 1.5, 0)
	rear.lift_height = 3.2
	out["doors"]["rear_grille"] = rear
	rear.set_open(true, false)   # raised until the capture
	b.model(EnvBuilder.ENV + "security_door_12.glb", Vector3(37.8, 0, -23.6), 270, "none")
	b.model(EnvBuilder.ENV + "yard_gate_2m.glb", Vector3(35.0, 0, -26.8), 0, "none")
	b.model(EnvBuilder.PROP + "cctv_camera.glb", Vector3(29.6, 3.4, -21.0), 200, "none")
	for x in [6.0, 14.0, 22.0, 34.0]:
		b.model(EnvBuilder.PROP + "pipe_straight_2m.glb", Vector3(x, 4.2, -6.4), 0, "none").rotation_degrees.z = 90
	# Photographed industrial cabinets and suspended fittings occupy closed service areas.
	b.scanned_prop("utility_box_01", Vector3(1.0, 0.7, -1.0), 90, 1.1)
	b.scanned_prop("worn_metal_rack", Vector3(35.8, 0, -8.0), 180, 1.9)
	b.scanned_prop("metal_toolbox", Vector3(35.8, 0.85, -8.0), 0, 0.3)
	# Pendant high-bay lamps; each emits downward from its shade (spot) so the ceiling no longer receives a
	# hard black disc shadow from an omni placed beneath the fixture.
	for p in [Vector3(4, 5.7, -3), Vector3(10.5, 5.7, -9.5), Vector3(9, 5.7, -18), Vector3(16, 5.7, -12.5), Vector3(16, 5.7, -18.5), Vector3(22, 5.7, -10),
			Vector3(22, 5.7, -16), Vector3(22, 5.7, -21), Vector3(27, 5.7, -11), Vector3(34, 5.7, -12), Vector3(34, 5.7, -23)]:
		EnvBuilder.no_shadow(b.model("res://assets/props/phase025/hanging_industrial_lamp/hanging_industrial_lamp_1k.gltf", p, 0, "none"))
		var lamp := b.spot(p - Vector3(0, 0.55, 0), p - Vector3(0, 8, 0), Color(0.8, 0.88, 1.0), 4.5, 9.0, 62.0)
		lamp.shadow_enabled = p in [Vector3(22, 5.7, -16), Vector3(9, 5.7, -18), Vector3(16, 5.7, -12.5)]
	# Service headers along the north and east walls with drops from the pump set, and a cable tray.
	var pipe_paint := EnvBuilder.p3_material("P3_PaintSteelGrey", null)
	var green := b.paint(Color(0.16, 0.32, 0.24), false, 0.45)
	b.pipe_run(Vector3(0.6, 4.6, -26.4), Vector3(37.4, 4.6, -26.4), 0.16, green)
	b.pipe_run(Vector3(0.6, 5.1, -26.5), Vector3(37.4, 5.1, -26.5), 0.10, pipe_paint)
	b.pipe_run(Vector3(37.4, 4.6, -26.4), Vector3(37.4, 4.6, -6.6), 0.16, green)
	for z in [-12.5, -16.5]:
		b.pipe_run(Vector3(15.34, 1.96, z), Vector3(15.34, 5.6, z), 0.075, pipe_paint)
		b.pipe_run(Vector3(15.34, 5.6, z), Vector3(15.34, 5.6, -26.4), 0.075, pipe_paint)
	b.visual_box(Vector3(19, 5.35, -6.45), Vector3(36, 0.06, 0.4), b.paint(Color(0.55, 0.57, 0.58), false, 0.4))   # cable tray
	# Walkway and hazard markings on the east floor route and around the pump well.
	for x in [20.6, 23.9]:
		b.floor_line(Vector3(x, 0, -6.6), Vector3(x, 0, -22.4), 0.09, Color(0.85, 0.68, 0.08))
	for z in [-9.8, -23.2]:
		b.floor_line(Vector3(12.1, 0, z), Vector3(19.9, 0, z), 0.12, Color(0.85, 0.68, 0.08))
	b.sign("PUMP HALL 2  \u2014  AUTHORISED STAFF ONLY", Vector3(10.0, 3.2, -6.16), 180.0, 1.8, Color(0.75, 0.12, 0.08), Color(0.97, 0.97, 0.95))
	b.sign("DANGER\nAUTOMATIC EQUIPMENT", Vector3(19.8, 1.6, -9.85), 0.0, 0.7, Color(0.85, 0.68, 0.08))
	b.sign("SPILLWAY", Vector3(29.78, 2.9, -24.0), -90.0, 0.7)
	# light: cold task lights, amber console practical, amber spillway practical
	var we := b.environment(Color(0.04, 0.05, 0.06), Color(0.08, 0.09, 0.1), Color(0.4, 0.46, 0.55), 0.24, 0.002, 1.0)
	out["world_env"] = we
	b.omni(Vector3(16, 4.0, -24.5), Color(0.75, 0.85, 1.0), 1.0, 8.0)
	# The entrance chase had no practical between its corners and read as a black void.
	b.model(EnvBuilder.PROP + "fluorescent_fixture.glb", Vector3(3.0, 3.0, -3.0), 0, "none")
	b.omni(Vector3(3.0, 2.8, -3.0), Color(0.9, 0.94, 1.0), 1.4, 6.0, true)
	b.omni(Vector3(18.0, 1.9, -25.0), Color(1.0, 0.65, 0.3), 1.6, 4.0)
	out["spill_light"] = b.omni(Vector3(29.0, 3.0, -24.0), Color(1.0, 0.6, 0.25), 1.6, 6.0, true)
	out.merge({"n0": Vector3(2.0, 0, -3.0), "gate": Vector3(4.0, 0, -5.2), "split": Vector3(8.6, 0, -8.6),
		"selector_stand": Vector3(9.1, 2.5, -19.0), "brake_stand": Vector3(22.8, 0, -19.0), "grille_south": Vector3(22.2, 0, -21.6),
		"grille_north": Vector3(22.2, 0, -24.6), "reunion": Vector3(16.6, 0, -24.4), "console": Vector3(18.0, 0, -24.6),
		"handle_w": Vector3(29.2, 0, -23.3), "handle_e": Vector3(29.2, 0, -24.7), "door_approach": Vector3(27.6, 0, -24.0),
		"catwalk_top": Vector3(9.2, 2.5, -15.0), "rusk_hidden": Vector3(34.5, 0, -22.0)})
	return out
