class_name EnvIntake
extends RefCounted
## ENV_INTAKE (docs/environments/PRISON_INTAKE.md), Godot coordinates = drafting (x, y, -z).
## Apron x0..8 (outdoor, bus), reception x8..24, ceiling 4 m. Screenplay staging takes precedence for the tray
## scene (approved alternative): Noah at the tray (19,-8.6), Rusk across the counter, Adrian behind the holding
## grille 3 m east / 4 m north of Noah, so the holding bay sits at x20..24, z-11.5..-16 with a solid see-through grille.
## East exit D3 (24,-6) joins the cell block vestibule.


static func build(b: EnvBuilder) -> Dictionary:
	# Phase 03: sealed slab floor, painted CMU walls with a darker wipe-clean dado, painted concrete soffit.
	var floor_in := b.sealed_floor(Color(0.62, 0.63, 0.62), 0.22, true)
	var asphalt := b.mat("asphalt_01", Color(1, 1, 1), 0.25)
	var wallm := b.paint(Color(0.78, 0.78, 0.74))
	var block := b.paint(Color(0.80, 0.80, 0.75), true)
	var out_block := b.mat("concrete_block_wall", Color(0.92, 0.92, 0.9), 0.4)
	var out := {"doors": {}}
	b.floor_rect(-4, 4, 8, -20, asphalt)
	b.floor_rect(8, 0, 24, -16, floor_in)
	b.ceiling_rect(8, 0, 24, -16, 4.0, wallm)
	b.ceiling_beams(8, 0, 24, -16, 4.0, 4.0, true, wallm, 0.4)
	b.wall_trim = {"dado": b.paint(Color(0.26, 0.34, 0.36), false, 0.45), "dado_h": 1.25, "line": b.paint(Color(0.1, 0.12, 0.13), false, 0.4),
		"skirt": b.paint(Color(0.12, 0.13, 0.13), false, 0.5), "frame": b.paint(Color(0.2, 0.23, 0.25), false, 0.42)}
	# perimeter
	b.wall(Vector2(8, 0), Vector2(8, -16), 4.0, block, 0.3, [[3.0, 5.0]])     # west with gate D1 at z-3..-5
	b.wall(Vector2(8, 0), Vector2(24, 0), 4.0, block, 0.3)
	b.wall(Vector2(8, -16), Vector2(24, -16), 4.0, block, 0.3)
	b.wall(Vector2(24, 0), Vector2(24, -16), 4.0, block, 0.3, [[5.0, 7.0]])   # east with exit D3 at z-5..-7
	b.wall_trim = {}
	block = out_block
	b.wall(Vector2(-4, 4), Vector2(-4, -20), 5.0, block, 0.4)                 # apron boundary walls
	b.wall(Vector2(-4, 4), Vector2(8, 4), 5.0, block, 0.4)
	b.wall(Vector2(-4, -20), Vector2(8, -20), 5.0, block, 0.4)
	b.box(Vector3(8, 2.0, -18), Vector3(0.4, 4.0, 4.0), block)
	b.box(Vector3(8, 2.0, 2), Vector3(0.4, 4.0, 4.0), block)
	var gate := Door.make(b, "GateD1", EnvBuilder.ENV + "yard_gate_2m.glb", Vector3(8, 0, -3), 90, Vector3(2.0, 3.0, 0.15))
	out["doors"]["D1"] = gate
	var exit := Door.make(b, "ExitD3", EnvBuilder.ENV + "security_door_12.glb", Vector3(24, 0, -5.4), 90, Vector3(1.3, 2.25, 0.15))
	exit.open_angle = 100.0
	out["doors"]["D3"] = exit
	b.box(Vector3(24, 1.1, -6.85), Vector3(0.3, 2.2, 0.3), block)
	# CC0 ajanhallinta coach conversion with the Phase 02.5 interior and the Phase 03 detail pass
	# (tools/phase03_bus_detail.py): coach proportions, 1 m wheels as separate Wheel_* nodes, lamps, livery.
	var bus := b.model("res://assets/props/phase03/blackridge_transport_bus_p03.glb", Vector3(2.5, 0, -9), 90, "none")
	bus.name = "TransportBus"
	var ab := EnvBuilder.local_aabb(bus)
	if ab.size.length() > 0.01:
		var s := 12.0 / maxf(ab.size.x, ab.size.z)
		bus.scale = Vector3.ONE * s
		bus.rotation_degrees.y = 90.0 if ab.size.x > ab.size.z else 0.0
	b.box(Vector3(2.5, 1.6, -9), Vector3(2.6, 3.2, 12.2), null, null, false)
	# holding bay (Adrian) with solid transparent grille
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(20, 0, -11.5), Vector3(24, 0, -11.5), 3.06, 3.0, 0.12)
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(20, 0, -11.5), Vector3(20, 0, -14.5), 3.06, 3.0, 0.12)
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(20, 0, -15.5), Vector3(20, 0, -16), 3.06, 3.0, 0.12)
	b.box(Vector3(22, 3.5, -11.5), Vector3(4, 1, 0.12), block)
	b.model(EnvBuilder.PROP + "yard_bench.glb", Vector3(22.5, 0, -15.4), 180, "box")
	# property counter, tray, guard desk with the VANTAGE badge, locker 42
	b.model(EnvBuilder.PROP + "intake_counter.glb", Vector3(19, 0, -10.0), 180, "box")
	b.box(Vector3(19, 1.13, -9.9), Vector3(0.55, 0.06, 0.38), b.flat(Color(0.25, 0.27, 0.3)))
	b.model(EnvBuilder.PROP + "photo_sleeve_empty.glb", Vector3(18.85, 1.17, -9.92), 0, "none")
	b.model(EnvBuilder.PROP + "steel_table.glb", Vector3(16.8, 0, -11.8), 0, "box")
	# Replace the faceted chair visual, retaining the original footprint collision.
	b.scanned_prop("SchoolChair_01", Vector3(16.8, 0, -12.6), 0, 0.95)
	b.box(Vector3(16.8, 0.45, -12.6), Vector3(0.55, 0.9, 0.6), null, null, false)
	var badge := b.model(EnvBuilder.PROP + "vantage_badge.glb", Vector3(17.0, 0.8, -11.6), 0, "none")
	badge.scale = Vector3.ONE * 2.0
	b.model("res://assets/props/acquisition_20261019/radio_yaesu_single_metric.glb", Vector3(16.3, 0.79, -11.95), 30, "none")
	b.model("res://assets/props/acquisition_20261019/simple_handcuffs.glb", Vector3(16.6, 0.80, -12.0), 70, "none")
	b.spot(Vector3(17.0, 2.0, -11.2), Vector3(17.0, 0.8, -11.6), Color(1.0, 0.93, 0.8), 6.0, 4.0, 25.0)
	b.box(Vector3(16.3, 0.005, -9.4), Vector3(0.9, 0.01, 0.9), b.flat(Color(0.85, 0.75, 0.15)))   # painted search mark
	for i in 3:
		b.model(EnvBuilder.PROP + "locker.glb", Vector3(23.5, 0, -9.0 - i * 0.55), 270, "box")
	b.model(EnvBuilder.PROP + "yard_bench.glb", Vector3(11.5, 0, -10.6), 0, "box")
	b.model(EnvBuilder.PROP + "cctv_camera.glb", Vector3(23.6, 3.6, -1.0), 225, "none")
	b.model("res://assets/props/phase025/metal_office_desk/metal_office_desk_1k.gltf", Vector3(10.2, 0, -2.0), 180, "box")
	b.model("res://assets/props/phase025/steel_frame_shelves_02/steel_frame_shelves_02_1k.gltf", Vector3(22.5, 0, -1.1), 180, "box")
	# Scanned service props stay at the perimeter, outside escort and player routes.
	b.scanned_prop("metal_trash_can", Vector3(9.0, 0, -14.8), 0, 0.75)
	b.scanned_prop("utility_box_01", Vector3(23.5, 0.9, -2.5), 270, 0.9)
	for x in [10.8, 11.4]:
		b.scanned_prop("cardboard_box_01", Vector3(x, 0.78, -2.0), 15, 0.28)
	# light: overcast exterior, cool interior strips
	b.environment(Color(0.55, 0.6, 0.66), Color(0.72, 0.74, 0.76), Color(0.72, 0.76, 0.82), 0.28, 0.0, 1.0)
	b.sun(Vector3(-35, -30, 0), Color(1.0, 0.96, 0.9), 1.3)
	# Recessed fluorescent grid between the beams (cool 4000 K); three fixtures carry shadows over the key
	# staging areas: tray/counter, holding bay, guard desk.
	for p in [Vector3(12, 3.92, -2), Vector3(17, 3.92, -2), Vector3(22, 3.92, -2), Vector3(12, 3.92, -6), Vector3(17, 3.92, -6),
			Vector3(22, 3.92, -6), Vector3(12, 3.92, -10), Vector3(19, 3.92, -10), Vector3(12, 3.92, -14), Vector3(16.5, 3.92, -13.2), Vector3(22, 3.92, -13.8)]:
		b.ceiling_light(p, Color(0.96, 0.97, 1.0), 2.6, 7.5, p in [Vector3(19, 3.92, -10), Vector3(22, 3.92, -13.8), Vector3(16.5, 3.92, -13.2)])
	# Processing floor markings and signage.
	b.floor_line(Vector3(17.6, 0, -8.15), Vector3(20.4, 0, -8.15), 0.1, Color(0.85, 0.68, 0.08))
	for z in [-2.0, -14.4]:
		b.floor_line(Vector3(9.0, 0, z), Vector3(19.6, 0, z), 0.08, Color(0.85, 0.68, 0.08))
	b.sign("INTAKE PROCESSING", Vector3(16.0, 2.75, -0.16), 180.0, 1.6)
	b.sign("HOLDING", Vector3(22.0, 3.25, -11.43), 0.0, 0.8)
	b.sign("WAIT BEHIND THE YELLOW LINE", Vector3(19.0, 0.62, -9.615), 0.0, 1.1, Color(0.85, 0.68, 0.08))
	b.sign("B BLOCK  →", Vector3(23.83, 2.6, -8.2), -90.0, 0.8)
	b.sign("NO PROPERTY BEYOND
THIS POINT", Vector3(23.83, 1.8, -3.0), -90.0, 0.9, Color(0.75, 0.12, 0.08), Color(0.97, 0.97, 0.95))
	out.merge({"noah_tray": Vector3(19, 0, -8.6), "rusk_desk": Vector3(19, 0, -11.0), "adrian_hold": Vector3(22, 0, -12.6),
		"adrian_bars": Vector3(20.6, 0, -12.2), "badge": Vector3(17.0, 0.8, -11.6), "search_mark": Vector3(16.3, 0, -9.4),
		"guard_desk": Vector3(16.2, 0, -12.4), "tray": Vector3(19, 1.1, -9.9), "locker42": Vector3(23.3, 0, -9.5),
		"exit_d3": Vector3(24.0, 0, -6.0), "bus": Vector3(2.5, 0, -9), "bus_node": bus, "holding_gate": Vector3(20.0, 0, -15.0)})
	# holding bay door on the west grille (opened for the escort)
	var hold_door := Door.make(b, "HoldingDoor", EnvBuilder.ENV + "cell_door_1m.glb", Vector3(20, 0, -14.5), 90, Vector3(1.0, 2.2, 0.12))
	out["doors"]["holding"] = hold_door
	return out


## CH01_M01_CS01_SH01 "bus stops before intake gate": roll the coach the last metres to its parked transform
## with an ease-out stop; every Wheel_* node turns by travelled distance / tyre radius (no wheel slip).
static func arrive(bus: Node3D, seconds := 7.0, distance := 5.5) -> void:
	if bus == null or not is_instance_valid(bus):
		return
	var final := bus.position
	var forward := bus.transform.basis.x.normalized()
	var wheels := bus.find_children("Wheel_*", "Node3D", true, false)
	var radius := 0.52 * bus.scale.x
	var rest := {}
	for w in wheels:
		rest[w] = (w as Node3D).rotation
	var step := func(t: float) -> void:
		var travelled := distance * t
		bus.position = final - forward * (distance - travelled)
		for w in wheels:
			(w as Node3D).rotation = rest[w] + Vector3(0, 0, -travelled / radius)
	step.call(0.0)
	var tw := bus.create_tween()
	tw.tween_method(step, 0.0, 1.0, seconds).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	GameState.log_event("bus_arrival", {"seconds": seconds, "distance": distance, "wheels": wheels.size()})

