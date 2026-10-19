class_name EnvSolitary
extends RefCounted
## Solitary annex (docs/environments/CELL_BLOCK.md): a separate occluded set, not walkable from the hall.
## Two 3x4 m cells separated by a 0.25 m wall carrying a shared pipe; neither player can see through the wall.
## Built at an offset of x+100 from the maintenance network. Overhead light pools separated by the black wall.

const O := Vector3(100, 0, 0)


static func build(b: EnvBuilder) -> Dictionary:
	var floor_m := b.mat("dirty_tiles", Color(0.6, 0.6, 0.6), 0.5)
	var wallm := b.mat("concrete_wall_004", Color(0.5, 0.5, 0.5), 0.4)
	b.floor_rect(O.x, O.z + 2.0, O.x + 6.25, O.z - 4.0, floor_m)
	b.ceiling_rect(O.x, O.z + 2.0, O.x + 6.25, O.z - 4.0, 2.8, wallm)
	b.wall(Vector2(O.x, O.z - 4.0), Vector2(O.x + 6.25, O.z - 4.0), 2.8, wallm, 0.3)
	b.wall(Vector2(O.x, O.z + 2.0), Vector2(O.x, O.z - 4.0), 2.8, wallm, 0.3)
	b.wall(Vector2(O.x + 6.25, O.z + 2.0), Vector2(O.x + 6.25, O.z - 4.0), 2.8, wallm, 0.3)
	b.wall(Vector2(O.x, O.z + 2.0), Vector2(O.x + 6.25, O.z + 2.0), 2.8, wallm, 0.3)
	b.box(Vector3(O.x + 3.125, 1.4, O.z - 2.0), Vector3(0.25, 2.8, 4.0), wallm)             # shared wall
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(O.x, 0, O.z), Vector3(O.x + 3.0, 0, O.z), 3.06, 2.8, 0.12)
	b.run(EnvBuilder.ENV + "cell_bars_3m.glb", Vector3(O.x + 3.25, 0, O.z), Vector3(O.x + 6.25, 0, O.z), 3.06, 2.8, 0.12)
	var pipe := b.model(EnvBuilder.PROP + "pipe_straight_2m.glb", Vector3(O.x + 2.1, 1.1, O.z - 3.8), 0, "none")
	pipe.rotation_degrees.z = 90
	pipe.scale = Vector3(1.0, 1.05, 1.0)
	for x in [O.x + 1.0, O.x + 5.2]:
		b.model(EnvBuilder.PROP + "cell_bed.glb", Vector3(x, 0, O.z - 2.6), 0, "box")
	b.environment(Color(0, 0, 0), Color(0.02, 0.02, 0.02), Color(0.2, 0.22, 0.25), 0.15, 0.0, 1.0)
	b.spot(Vector3(O.x + 1.5, 2.7, O.z - 2.0), Vector3(O.x + 1.5, 0, O.z - 2.0), Color(0.95, 0.92, 0.85), 5.0, 4.0, 40.0)
	b.spot(Vector3(O.x + 4.75, 2.7, O.z - 2.0), Vector3(O.x + 4.75, 0, O.z - 2.0), Color(0.95, 0.92, 0.85), 5.0, 4.0, 40.0)
	return {"seat_p1": O + Vector3(1.5, 0, -2.0), "seat_p2": O + Vector3(4.75, 0, -2.0),
		"pipe_p1": O + Vector3(2.6, 1.1, -3.55), "pipe_p2": O + Vector3(3.65, 1.1, -3.55),
		"face_p1": [O + Vector3(1.6, 1.5, -0.6), O + Vector3(1.5, 1.4, -2.2)], "face_p2": [O + Vector3(4.65, 1.5, -0.6), O + Vector3(4.75, 1.4, -2.2)]}
