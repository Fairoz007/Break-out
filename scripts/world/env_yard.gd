class_name EnvYard
extends RefCounted
## ENV_YARD (docs/environments/PRISON_YARD.md), Godot coordinates = drafting (x, y, -z). 40x30 m yard inside an
## 8 m wall, 5 m fence on the west and north sides, court x6..34 / z-6.5..-21.5, confrontation bench (23..27, -4..-6),
## tap alcove Y3 (9,-24), loose ball (22,-12), empty west fence target (3,-12), west gate D1 (2,-15), north-east
## work-call gate D2 (38,-24). Guard lanes east (x35) and north (z-28). Ball lane x3..22 at z-12 kept clear.


static func build(b: EnvBuilder) -> Dictionary:
	var ground := b.mat("concrete_floor_worn_001", Color(0.82, 0.82, 0.82), 0.3)
	var wallm := b.surface("concrete_wall_007", Color(0.78, 0.8, 0.84), 0.22, 0.6)   # cooled toward grey precast (D03-008)
	var out := {"doors": {}}
	b.floor_rect(-3, 3, 43, -33, ground)
	load("res://scripts/world/prison_court.gd").build(b)
	# perimeter wall 8 m
	b.wall(Vector2(-3, 3), Vector2(43, 3), 8.0, wallm, 0.6)
	b.wall(Vector2(-3, -33), Vector2(43, -33), 8.0, wallm, 0.6)
	b.wall(Vector2(-3, 3), Vector2(-3, -33), 8.0, wallm, 0.6)
	b.wall(Vector2(43, 3), Vector2(43, -33), 8.0, wallm, 0.6)
	# Perimeter wall detail: precast coping, inner pilasters every 6 m and concertina razor wire on the coping.
	var coping := b.surface("concrete_wall_007", Color(0.7, 0.72, 0.75), 0.5, 0.4)
	for seg in [[Vector3(-3, 0, 3), Vector3(43, 0, 3)], [Vector3(-3, 0, -33), Vector3(43, 0, -33)], [Vector3(-3, 0, 3), Vector3(-3, 0, -33)], [Vector3(43, 0, 3), Vector3(43, 0, -33)]]:
		var a3: Vector3 = seg[0]
		var b3: Vector3 = seg[1]
		var d := b3 - a3
		var yaw := -atan2(d.z, d.x)
		b.visual_box((a3 + b3) / 2.0 + Vector3(0, 8.08, 0), Vector3(d.length() + 0.8, 0.16, 0.85), coping, yaw)
		b.run("res://assets/props/phase03/razor_wire_2m.glb", a3, b3, 2.0, 0.8, 0.8, false, 8.16)
		var n := int(d.length() / 6.0)
		var inward := Vector3(-d.z, 0, d.x).normalized()
		if (Vector3(20, 0, -15) - a3).dot(inward) < 0.0:
			inward = -inward
		for i in range(1, n):
			var c := a3 + d * (float(i) / n) + inward * 0.42
			b.visual_box(c + Vector3(0, 4.0, 0), Vector3(0.55, 8.0, 0.25), coping, yaw)
	# fences: west (x=1) with gate D1 at z-14..-16, north (z=-29) with gate D2 at x37..39
	b.run("res://assets/environments/phase025/chain_link_fence_2x5.glb", Vector3(1, 0, 1), Vector3(1, 0, -14), 2.05, 5.0, 0.15)
	b.run("res://assets/environments/phase025/chain_link_fence_2x5.glb", Vector3(1, 0, -16), Vector3(1, 0, -29), 2.05, 5.0, 0.15)
	b.run("res://assets/environments/phase025/chain_link_fence_2x5.glb", Vector3(1, 0, -29), Vector3(37, 0, -29), 2.05, 5.0, 0.15)
	b.run("res://assets/environments/phase025/chain_link_fence_2x5.glb", Vector3(39, 0, -29), Vector3(43, 0, -29), 2.05, 5.0, 0.15)
	# Distance stand-in for the woven wire: beyond ~10 m the 2.8 mm wires are sub-pixel and vanish, so a mipmapped
	# chain-link alpha plane fades in on the same line (posts and rails are in the same mesh and stay visible).
	for seg in [[Vector3(1, 0, 1), Vector3(1, 0, -14)], [Vector3(1, 0, -16), Vector3(1, 0, -29)], [Vector3(1, 0, -29), Vector3(37, 0, -29)], [Vector3(39, 0, -29), Vector3(43, 0, -29)]]:
		_fence_far(b, seg[0], seg[1])
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
	b.model(EnvBuilder.PROP + "yard_bench.glb", Vector3(25, 0, -4.5), 0, "box")
	b.model(EnvBuilder.PROP + "yard_bench.glb", Vector3(8.6, 0, -22.9), 90, "box")
	b.model("res://assets/props/phase15_discovery/oga_basketball_hoop_ouren/ball_rack.glb", Vector3(38, 0, -20), 270, "box")
	# Yard lighting columns (galvanised, twin LED heads) replace the floating floodlight heads.
	for p in [[Vector3(1.6, 0, -6), 90.0], [Vector3(38, 0, -1.6), 180.0], [Vector3(1.6, 0, -27), 90.0], [Vector3(30, 0, -28.4), 0.0]]:
		b.model("res://assets/props/phase03/floodlight_pole.glb", p[0], p[1], "none")
		b.box(p[0] + Vector3(0, 4.0, 0), Vector3(0.45, 8.0, 0.45), null, null, false)   # column only; arms are overhead
	b.model(EnvBuilder.PROP + "cctv_camera.glb", Vector3(42.5, 6.0, -1.5), 220, "none")
	var tower := b.model("res://assets/environments/acquisition_20261019/guard_tower.glb", Vector3(40.6, 0.72, -31.0), 225, "box")
	out["tower"] = tower
	# light: hazy morning sun, overcast fill
	b.environment(Color(0.43, 0.55, 0.69), Color(0.7, 0.74, 0.77), Color(0.75, 0.78, 0.82), 0.32, 0.0008, 1.0)
	b.sun(Vector3(-38, 35, 0), Color(1.0, 0.95, 0.85), 1.4)
	out.merge({"noah_start": Vector3(-0.5, 0, -15), "adrian_start": Vector3(9, 0, -24.2), "court_center": Vector3(18, 0, -15),
		"bench": Vector3(24.2, 0, -5.5), "mediate": Vector3(22.8, 0, -4.1), "silas": Vector3(25.0, 0, -4.9), "ball": Vector3(21.6, 0.12, -11.6),
		"fence_target": Vector3(1.6, 0.12, -11.6), "tap": Vector3(9, 0, -24.4), "tap_p1": Vector3(8.3, 0, -24.4), "tap_p2": Vector3(9.8, 0, -24.0),
		"gate_d2": Vector3(38, 0, -27.8), "inmate_a": Vector3(27, 0, -4.5), "inmate_b": Vector3(29, 0, -4.5), "north_fence": Vector3(24, 0, -27.5)})
	return out


static var _fence_mat: StandardMaterial3D


static func _fence_far(b: EnvBuilder, a: Vector3, c: Vector3) -> void:
	if _fence_mat == null:
		_fence_mat = StandardMaterial3D.new()
		_fence_mat.albedo_texture = load("res://assets/materials/phase03/chainlink_alpha.png")
		_fence_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_DEPTH_PRE_PASS
		_fence_mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		_fence_mat.metallic = 0.6
		_fence_mat.roughness = 0.45
		_fence_mat.uv1_scale = Vector3(1.0 / 0.13, 1.0 / 0.13, 1)
		_fence_mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	var d := c - a
	var mi := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(d.length(), 4.75)
	mi.mesh = q
	mi.material_override = _fence_mat
	q.material = _fence_mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.visibility_range_begin = 9.0
	mi.visibility_range_begin_margin = 6.0
	mi.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
	b.root.add_child(mi)
	mi.position = (a + c) / 2.0 + Vector3(0, 2.45, 0)
	mi.rotation.y = -atan2(d.z, d.x)
	# QuadMesh UVs span 0..1; scale them to the metric wire pitch along the run and up the module
	_fence_mat.uv1_triplanar = true
	_fence_mat.uv1_world_triplanar = true

