class_name PlayerCamera
extends Node3D
## Third-person camera rig per player (REQ-CAM-001/002): pivot 1.6 m above the feet, 2.8 m trailing,
## world collision retracts the arm; wall safety takes precedence over the preferred 0.45 m framing. The actual Camera3D lives in the player's own
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
var _camera_sweep := SphereShape3D.new()
## While a hold has an authored "face" point (Silas in M02), the camera eases its yaw so both the player and
## that point stay in view; any look input takes priority (Phase 05, D05-009).
var frame_target := Vector3.INF
var frame_yaw := 0.0            # extra yaw (radians) so the hands can be seen (M05 gate latch from the side)


func setup(p: Player, cam: Camera3D) -> PlayerCamera:
	player = p
	camera = cam
	name = "CameraRig_P%d" % (p.index + 1)
	top_level = true
	arm = SpringArm3D.new()
	arm.spring_length = DISTANCE
	arm.margin = 0.2
	arm.collision_mask = EnvBuilder.LAYER_CAMERA
	var sphere := SphereShape3D.new()
	sphere.radius = 0.2
	arm.shape = sphere
	add_child(arm)
	end = Node3D.new()
	arm.add_child(end)
	_camera_sweep.radius = 0.16
	p.rig = self
	camera.fov = 70.0
	camera.near = 0.05
	return self


func snap_behind(p: Player) -> void:
	yaw = p.global_rotation.y
	global_position = p.global_position + Vector3.UP * (0.95 if p.crouched else HEIGHT)
	_apply()


func _physics_process(delta: float) -> void:
	if not is_instance_valid(player):
		return
	if not player.input_locked:
		var look := Devices.look(player.index, delta)
		yaw -= look.x
		pitch = clampf(pitch - look.y, deg_to_rad(-60.0), deg_to_rad(35.0))
		if frame_target != Vector3.INF and look.length() < 0.0005:
			var mid := player.global_position.lerp(frame_target, 0.6) - global_position
			if Vector2(mid.x, mid.z).length() > 0.3:
				yaw = lerp_angle(yaw, atan2(-mid.x, -mid.z) + frame_yaw, clampf(3.0 * delta, 0.0, 1.0))
	global_position = global_position.lerp(player.global_position + Vector3.UP * (0.95 if player.crouched else HEIGHT), clampf(14.0 * delta, 0.0, 1.0))
	arm.spring_length = max_distance
	_apply()
	_update_camera(delta)


func _apply() -> void:
	rotation = Vector3(pitch, yaw, 0)


## Camera collision queries and interpolation run together on the physics tick.
func _update_camera(delta: float) -> void:
	if override_active or camera == null:
		return
	var target := end.global_transform
	# Retract fully when walls are closer than the preferred framing distance.
	if arm.get_hit_length() < MIN_DISTANCE:
		# A nearby wall takes precedence over framing distance: never extend through it.
		target.origin = arm.global_position + arm.global_transform.basis.z * maxf(0.0, arm.get_hit_length())
	if _blend_t < 1.0:
		_blend_t = min(1.0, _blend_t + delta / BLEND_TIME)
		var w := smoothstep(0.0, 1.0, _blend_t)
		camera.global_transform = _blend_from.interpolate_with(target, w)
		camera.fov = lerpf(_blend_fov_from, 70.0, w)
	else:
		camera.global_transform = target
		camera.fov = 70.0
	camera.global_position = _safe_camera_position(camera.global_position)


## Sweep the actual blended candidate, which can approach the pivot from a different
## direction than the spring arm after a cinematic. Never extend beyond a world hit.
func _safe_camera_position(candidate: Vector3) -> Vector3:
	var pivot := arm.global_position
	var motion := candidate - pivot
	if motion.length_squared() < 0.000001:
		return pivot
	var query := PhysicsShapeQueryParameters3D.new()
	query.shape = _camera_sweep
	query.transform = Transform3D(Basis.IDENTITY, pivot)
	query.motion = motion
	query.collision_mask = EnvBuilder.LAYER_CAMERA
	query.exclude = [player.get_rid()]
	var fractions := player.get_world_3d().direct_space_state.cast_motion(query)
	var fraction := float(fractions[0])
	# A thin wall ray also protects cases where the starting sphere overlaps geometry.
	var ray := PhysicsRayQueryParameters3D.create(pivot, candidate, EnvBuilder.LAYER_CAMERA)
	ray.exclude = [player.get_rid()]
	var hit := player.get_world_3d().direct_space_state.intersect_ray(ray)
	if not hit.is_empty():
		fraction = minf(fraction, maxf(0.0, pivot.distance_to(hit["position"]) - 0.16) / motion.length())
	return pivot + motion * maxf(0.0, fraction - 0.01 / motion.length())


## Hand the camera back after a cinematic, blending from wherever the cinematic left it.
func blend_back(from: Transform3D, from_fov: float) -> void:
	override_active = false
	_blend_from = from
	_blend_fov_from = from_fov
	_blend_t = 0.0
	GameState.log_event("camera_blend_back", {"player": player.index, "seconds": BLEND_TIME})


func current_distance() -> float:
	return camera.global_position.distance_to(arm.global_position)
