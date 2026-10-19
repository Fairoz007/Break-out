class_name EnvYard
extends RefCounted
## ENV_YARD (docs/environments/PRISON_YARD.md), Godot coordinates = drafting (x, y, -z). 40x30 m yard inside an
## 8 m wall, 5 m fence on the west and north sides, court x10..30 / z-6..-22, confrontation bench (23..27, -11..-13),
## tap alcove Y3 (9,-24), loose ball (22,-12), empty west fence target (3,-12), west gate D1 (2,-15), north-east
## work-call gate D2 (38,-24). Guard lanes east (x35) and north (z-28). Ball lane x3..22 at z-12 kept clear.


static func build(b: EnvBuilder) -> Dictionary:
	var ground := b.mat("concrete_floor_worn_001", Color(0.82, 0.82, 0.82), 0.3)
	var court := b.mat("smooth_concrete_floor", Color(0.9, 0.9, 0.92), 0.3)
	var wallm := b.mat("concrete_wall_004", Color(0.85, 0.85, 0.85), 0.25)
	var out := {"doors": {}}
	b.floor_rect(-3, 3, 43, -33, ground)
	b.box(Vector3(20, 0.005, -14), Vector3(20, 0.01, 16), court)
	for line in [[Vector3(20, 0.012, -6), Vector3(20, 0.01, 0.08)], [Vector3(20, 0.012, -22), Vector3(20, 0.01, 0.08)], [Vector3(10, 0.012, -14), Vector3(0.08, 0.01, 16)],
			[Vector3(30, 0.012, -14), Vector3(0.08, 0.01, 16)], [Vector3(20, 0.012, -14), Vector3(0.08, 0.01, 16)]]:
		b.box(line[0], line[1], b.flat(Color(0.92, 0.92, 0.88)))
	# perimeter wall 8 m
	b.wall(Vector2(-3, 3), Vector2(43, 3), 8.0, wallm, 0.6)
	b.wall(Vector2(-3, -33), Vector2(43, -33), 8.0, wallm, 0.6)
	b.wall(Vector2(-3, 3), Vector2(-3, -33), 8.0, wallm, 0.6)
	b.wall(Vector2(43, 3), Vector2(43, -33), 8.0, wallm, 0.6)
	# fences: west (x=1) with gate D1 at z-14..-16, north (z=-29) with gate D2 at x37..39
	b.run(EnvBuilder.ENV + "fence_2x5.glb", Vector3(1, 0, 1), Vector3(1, 0, -14), 2.05, 5.0, 0.15)
	b.run(EnvBuilder.ENV + "fence_2x5.glb", Vector3(1, 0, -16), Vector3(1, 0, -29), 2.05, 5.0, 0.15)
	b.run(EnvBuilder.ENV + "fence_2x5.glb", Vector3(1, 0, -29), Vector3(37, 0, -29), 2.05, 5.0, 0.15)
	b.run(EnvBuilder.ENV + "fence_2x5.glb", Vector3(39, 0, -29), Vector3(43, 0, -29), 2.05, 5.0, 0.15)
	var d1 := Door.make(b, "GateD1", EnvBuilder.ENV + "yard_gate_2m.glb", Vector3(1, 0, -14), 90, Vector3(2.0, 3.0, 0.15))
	out["doors"]["D1"] = d1
	var d2 := Door.make(b, "GateD2", EnvBuilder.ENV + "yard_gate_2m.glb", Vector3(37, 0, -29), 0, Vector3(2.0, 3.0, 0.15))
	out["doors"]["D2"] = d2
	# tap alcove (three-sided niche) and benches
	b.wall(Vector2(7, -22.5), Vector2(7, -26), 3.0, wallm, 0.3)
	b.wall(Vector2(7, -26), Vector2(11, -26), 3.0, wallm, 0.3)
	b.wall(Vector2(11, -26), Vector2(11, -24.6), 3.0, wallm, 0.3)
	b.model(EnvBuilder.PROP + "water_tap.glb", Vector3(9, 0, -25.7), 0, "box")
	b.model(EnvBuilder.PROP + "drain_grate.glb", Vector3(9, 0, -25.2), 0, "none")
	b.model(EnvBuilder.PROP + "yard_bench.glb", Vector3(25, 0, -12.6), 0, "box")
	b.model(EnvBuilder.PROP + "yard_bench.glb", Vector3(8.6, 0, -22.9), 90, "box")
	b.model("res://assets/props/phase15_discovery/oga_basketball_hoop_ouren/basketball_hoop.glb", Vector3(20, 0, -5.2), 180, "box")
	b.model("res://assets/props/phase15_discovery/oga_basketball_hoop_ouren/basketball_hoop.glb", Vector3(20, 0, -22.8), 0, "box")
	b.model("res://assets/props/phase15_discovery/oga_basketball_hoop_ouren/ball_rack.glb", Vector3(31, 0, -20), 270, "box")
	for p in [Vector3(1.4, 0, -6), Vector3(38, 0, -2), Vector3(1.4, 0, -27), Vector3(30, 0, -28.5)]:
		b.model(EnvBuilder.PROP + "floodlight.glb", p + Vector3(0, 5.2, 0), 0, "none")
	b.model(EnvBuilder.PROP + "cctv_camera.glb", Vector3(42.5, 6.0, -1.5), 220, "none")
	var tower := b.model("res://assets/environments/acquisition_20261019/guard_tower.glb", Vector3(40.6, 0.72, -31.0), 225, "box")
	out["tower"] = tower
	# light: hazy morning sun, overcast fill
	b.environment(Color(0.55, 0.65, 0.78), Color(0.8, 0.82, 0.84), Color(0.75, 0.78, 0.82), 0.55, 0.006, 1.0)
	b.sun(Vector3(-38, 35, 0), Color(1.0, 0.95, 0.85), 1.4)
	out.merge({"noah_start": Vector3(-0.5, 0, -15), "adrian_start": Vector3(9, 0, -24.2), "court_center": Vector3(18, 0, -15),
		"bench": Vector3(24.2, 0, -13.6), "mediate": Vector3(22.8, 0, -12.2), "silas": Vector3(25.0, 0, -13.0), "ball": Vector3(21.6, 0.12, -11.6),
		"fence_target": Vector3(1.6, 0.12, -11.6), "tap": Vector3(9, 0, -24.4), "tap_p1": Vector3(8.3, 0, -24.4), "tap_p2": Vector3(9.8, 0, -24.0),
		"gate_d2": Vector3(38, 0, -27.8), "inmate_a": Vector3(27, 0, -14), "inmate_b": Vector3(27, 0, -16), "north_fence": Vector3(24, 0, -27.5)})
	return out
