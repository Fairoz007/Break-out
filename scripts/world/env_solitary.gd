class_name EnvSolitary
extends RefCounted
## Solitary annex (docs/environments/CELL_BLOCK.md): a separate occluded set, not walkable from the hall.
## Two 3x4 m cells separated by a 0.25 m wall carrying a shared pipe; neither player can see through the wall.
## Built at an offset of x+100 from the maintenance network. Overhead light pools separated by the black wall.

const O := Vector3(100, 0, 0)


static func build(b: EnvBuilder) -> Dictionary:
	var floor_m := b.mat("dirty_tiles", Color(0.6, 0.6, 0.6), 0.5)
	# Phase 03: worn painted CMU (pale grey-green over a darker scuffed dado), painted soffit.
	var wallm := b.paint(Color(0.66, 0.68, 0.63), true)
	b.floor_rect(O.x, O.z + 2.0, O.x + 6.25, O.z - 4.0, floor_m)
	b.ceiling_rect(O.x, O.z + 2.0, O.x + 6.25, O.z - 4.0, 2.8, b.paint(Color(0.62, 0.63, 0.6)))
	b.wall_trim = {"dado": b.paint(Color(0.3, 0.34, 0.32), false, 0.55), "dado_h": 1.1, "skirt": b.paint(Color(0.1, 0.1, 0.1), false, 0.5)}
	b.wall(Vector2(O.x, O.z - 4.0), Vector2(O.x + 6.25, O.z - 4.0), 2.8, wallm, 0.3)
	b.wall(Vector2(O.x, O.z + 2.0), Vector2(O.x, O.z - 4.0), 2.8, wallm, 0.3)
	b.wall(Vector2(O.x + 6.25, O.z + 2.0), Vector2(O.x + 6.25, O.z - 4.0), 2.8, wallm, 0.3)
	b.wall(Vector2(O.x, O.z + 2.0), Vector2(O.x + 6.25, O.z + 2.0), 2.8, wallm, 0.3)
	b.wall(Vector2(O.x + 3.125, O.z), Vector2(O.x + 3.125, O.z - 4.0), 2.8, wallm, 0.25)    # shared wall
	b.wall_trim = {}
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(O.x, 0, O.z), Vector3(O.x + 3.0, 0, O.z), 3.06, 2.8, 0.12)
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(O.x + 3.25, 0, O.z), Vector3(O.x + 6.25, 0, O.z), 3.06, 2.8, 0.12)
	var pipe := b.model(EnvBuilder.PROP + "pipe_straight_2m.glb", Vector3(O.x + 2.1, 1.1, O.z - 3.8), 0, "none")
	pipe.rotation_degrees.z = 90
	pipe.scale = Vector3(1.0, 1.05, 1.0)
	# Bunks along the outer walls keep the pipe stances by the shared wall clear (CH01_M06_OBJ002).
	for x in [O.x + 1.0, O.x + 5.2]:
		var bed_envelope := b.model("res://assets/props/phase025/prison_bed.glb", Vector3(x, 0, O.z - 2.6), 0, "box")
		for mesh in bed_envelope.find_children("*", "MeshInstance3D", true, false):
			(mesh as MeshInstance3D).visible = false
		b.model("res://assets/props/phase04_architecture/prison_bunk.glb", Vector3(x, 0, O.z - 2.6), 0, "none")
	for x in [O.x + 1.5, O.x + 4.75]:
		b.model("res://assets/props/phase025/industrial_wall_lamp/industrial_wall_lamp_1k.gltf", Vector3(x, 2.35, O.z - 3.82), 0, "none")
	b.environment(Color(0, 0, 0), Color(0.02, 0.02, 0.02), Color(0.32, 0.34, 0.38), 0.3, 0.0, 1.0)
	# Separate bounded practical fills reveal faces and walls; shadows preserve the shared divider.
	for x in [O.x + 1.5, O.x + 4.75]:
		b.omni(Vector3(x, 2.0, O.z - 1.5), Color(0.82, 0.85, 0.9), 1.1, 3.6, true)
		EnvBuilder.no_shadow(b.model(EnvBuilder.PROP + "fluorescent_fixture.glb", Vector3(x, 2.76, O.z - 2.0), 0, "none"))   # flush: clear of the close camera
	b.spot(Vector3(O.x + 1.5, 2.7, O.z - 2.0), Vector3(O.x + 1.5, 0, O.z - 2.0), Color(0.95, 0.92, 0.85), 5.0, 4.0, 40.0)
	b.spot(Vector3(O.x + 4.75, 2.7, O.z - 2.0), Vector3(O.x + 4.75, 0, O.z - 2.0), Color(0.95, 0.92, 0.85), 5.0, 4.0, 40.0)
	# D03-016: seats on the foot end of each bunk, facing the bars (previously 0.5 m beside the bunk, mid-air).
	return {"seat_p1": O + Vector3(1.0, 0, -1.78), "seat_p2": O + Vector3(5.2, 0, -1.78),
		"pipe_p1": O + Vector3(2.6, 1.1, -3.55), "pipe_p2": O + Vector3(3.65, 1.1, -3.55),
		"face_p1": [O + Vector3(1.15, 1.4, -0.45), O + Vector3(1.0, 1.15, -1.95)], "face_p2": [O + Vector3(5.05, 1.4, -0.45), O + Vector3(5.2, 1.15, -1.95)]}
