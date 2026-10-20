class_name Door
extends StaticBody3D
## Hinged door, sliding panel or lifting grille with a solid collider (REQ-ENV-007). While it moves it holds a
## GameState lock so no checkpoint can be saved mid-motion (REQ-SAVE-002). Open state disables the collider.

enum Kind { SWING, LIFT, SLIDE }

var kind := Kind.SWING
var is_open := false
var visual: Node3D
var hinge: Node3D
var shape: CollisionShape3D
var open_angle := -100.0
var lift_height := 2.8
var slide := Vector3(1.0, 0, 0)
var seconds := 0.8
var model_file := ""
## Phase 06: each door sounds at the moment it moves, from its own position: [open cue, close cue] by model.
const SOUNDS := {"cell_door": ["gate_latch", "cell_slam"], "yard_gate": ["fence_rattle", "gate_latch"],
	"security_grille": ["grille", "grille"], "security_door": ["door_open", "door_close"], "spillway": ["door_open", "door_close"]}


static func make(b: EnvBuilder, door_name: String, model_path: String, pos: Vector3, yaw_deg: float, size: Vector3, p_kind := Kind.SWING) -> Door:
	var d := Door.new()
	d.name = door_name
	d.kind = p_kind
	d.collision_layer = EnvBuilder.LAYER_WORLD | (0 if EnvBuilder.SEE_THROUGH.any(func(k): return k in model_path.get_file()) else EnvBuilder.LAYER_CAMERA)
	d.collision_mask = 0
	d.position = pos
	d.rotation_degrees.y = yaw_deg
	b.dynamic.add_child(d)
	d.model_file = model_path.get_file()
	d.hinge = Node3D.new()
	d.add_child(d.hinge)
	if model_path != "":
		d.visual = (load(model_path) as PackedScene).instantiate()
		EnvBuilder.apply_finish(d.visual, model_path)
		d.hinge.add_child(d.visual)
	d.shape = CollisionShape3D.new()
	var bs := BoxShape3D.new()
	bs.size = size
	d.shape.shape = bs
	# Collider spans from the hinge (local origin) along +X, like the door modules.
	d.shape.position = Vector3(size.x / 2.0 if p_kind == Kind.SWING else 0.0, size.y / 2.0, 0)
	d.add_child(d.shape)
	return d


func set_open(open: bool, animate := true) -> void:
	if open == is_open:
		return
	is_open = open
	var lock_name := "door:" + name
	if animate and is_inside_tree():
		for k in SOUNDS:
			if k in model_file:
				AudioDirector.cue(SOUNDS[k][0 if open else 1], self, -4.0)
				break
		GameState.locks[lock_name] = true
		if not open:
			shape.disabled = false
		var t := create_tween()
		match kind:
			Kind.SWING: t.tween_property(hinge, "rotation_degrees:y", open_angle if open else 0.0, seconds)
			Kind.LIFT: t.tween_property(hinge, "position:y", lift_height if open else 0.0, seconds * 2.0)
			Kind.SLIDE: t.tween_property(hinge, "position", slide if open else Vector3.ZERO, seconds)
		await t.finished
		GameState.locks.erase(lock_name)
	else:
		match kind:
			Kind.SWING: hinge.rotation_degrees.y = open_angle if open else 0.0
			Kind.LIFT: hinge.position.y = lift_height if open else 0.0
			Kind.SLIDE: hinge.position = slide if open else Vector3.ZERO
	shape.disabled = open
	GameState.log_event("door", {"door": name, "open": open})
