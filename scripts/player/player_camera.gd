class_name PlayerCamera
extends Node3D
## Third-person camera rig per player (REQ-CAM-001/002): pivot 1.6 m above the feet, 2.8 m trailing,
## world collision retracts the arm to no closer than 0.45 m. The actual Camera3D lives in the player's own
## SubViewport and copies this rig's end transform every frame, so both views render one shared world.

const HEIGHT := 1.6
const DISTANCE := 2.8
const MIN_DISTANCE := 0.45
const BLEND_TIME := 0.4

var player: Player
var camera: Camera3D            # lives in the player's SubViewport
var yaw := 0.0
var pitch := deg_to_rad(-12.0)
var arm: SpringArm3D
var end: Node3D
var override_active := false    # true while a cinematic owns the camera
var _blend_from := Transform3D.IDENTITY
var _blend_t := 1.0
var _blend_fov_from := 70.0
var max_distance := DISTANCE


func setup(p: Player, cam: Camera3D) -> PlayerCamera:
	player = p
	camera = cam
	name = "CameraRig_P%d" % (p.index + 1)
	top_level = true
	arm = SpringArm3D.new()
	arm.spring_length = DISTANCE
	arm.margin = 0.2
	arm.collision_mask = EnvBuilder.LAYER_WORLD
	var sphere := SphereShape3D.new()
	sphere.radius = 0.2
	arm.shape = sphere
	add_child(arm)
	end = Node3D.new()
	arm.add_child(end)
	p.rig = self
	camera.fov = 70.0
	camera.near = 0.05
	return self


func snap_behind(p: Player) -> void:
	yaw = p.global_rotation.y
	global_position = p.global_position + Vector3.UP * HEIGHT
	_apply()


func _physics_process(delta: float) -> void:
	if not is_instance_valid(player):
		return
	if not player.input_locked:
		var look := Devices.look(player.index, delta)
		yaw -= look.x
		pitch = clampf(pitch - look.y, deg_to_rad(-60.0), deg_to_rad(35.0))
	global_position = global_position.lerp(player.global_position + Vector3.UP * HEIGHT, clampf(14.0 * delta, 0.0, 1.0))
	arm.spring_length = max_distance
	_apply()


func _apply() -> void:
	rotation = Vector3(pitch, yaw, 0)


func _process(delta: float) -> void:
	if override_active or camera == null:
		return
	var target := end.global_transform
	# Enforce the 0.45 m minimum: if the arm collapsed further, hold the camera at the minimum distance.
	if arm.get_hit_length() < MIN_DISTANCE:
		target.origin = arm.global_position + arm.global_transform.basis.z * MIN_DISTANCE
	if _blend_t < 1.0:
		_blend_t = min(1.0, _blend_t + delta / BLEND_TIME)
		var w := smoothstep(0.0, 1.0, _blend_t)
		camera.global_transform = _blend_from.interpolate_with(target, w)
		camera.fov = lerpf(_blend_fov_from, 70.0, w)
	else:
		camera.global_transform = target
		camera.fov = 70.0


## Hand the camera back after a cinematic, blending from wherever the cinematic left it.
func blend_back(from: Transform3D, from_fov: float) -> void:
	override_active = false
	_blend_from = from
	_blend_fov_from = from_fov
	_blend_t = 0.0
	GameState.log_event("camera_blend_back", {"player": player.index, "seconds": BLEND_TIME})


func current_distance() -> float:
	return camera.global_position.distance_to(arm.global_position)
