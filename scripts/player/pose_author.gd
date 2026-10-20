class_name PoseAuthor
extends RefCounted
## Authored key poses for the Rocketbox Biped rig, baked into clips at load time (Phase 05, D05-005).
## The retargeted clip set has no kneel (the old substitute, Fixing_Kneeling, is a bent-over repair crouch
## that stands back up after 4 s), and Mixamo retargets were rejected (crossed arms). Poses here are built
## by aiming limbs in skeleton space from the character's own Idle pose, so they fit every body.
## Skeleton space: +X forward, +Y up, -Z = character's left, centimetres; the floor is at y = FLOOR_Y.

const PREFIX := "Bip01/Skeleton3D:"
const FLOOR_Y := -90.87          # Bip01 node sits 0.895 m up with a 0.009851 scale
const KNEE_ON_FLOOR := 6.0       # knee joint centre above the floor when kneeling (cm)

var skel: Skeleton3D
var rot: Array[Quaternion] = []
var pos: Array[Vector3] = []
var glob: Array[Transform3D] = []


func _init(skeleton: Skeleton3D, base: Animation, time := 0.0) -> void:
	skel = skeleton
	for i in skel.get_bone_count():
		rot.append(skel.get_bone_rest(i).basis.get_rotation_quaternion())
		pos.append(skel.get_bone_rest(i).origin)
	for t in base.get_track_count():
		var bone := String(base.track_get_path(t)).trim_prefix(PREFIX)
		var i := skel.find_bone(bone)
		if i < 0:
			continue
		if base.track_get_type(t) == Animation.TYPE_ROTATION_3D:
			rot[i] = base.rotation_track_interpolate(t, time)
		elif base.track_get_type(t) == Animation.TYPE_POSITION_3D:
			pos[i] = base.position_track_interpolate(t, time)
	_fk()


func copy() -> PoseAuthor:
	var p: PoseAuthor = PoseAuthor.new(skel, Animation.new())
	p.rot = rot.duplicate()
	p.pos = pos.duplicate()
	p._fk()
	return p


func _fk() -> void:
	glob.resize(skel.get_bone_count())
	for i in skel.get_bone_count():
		var local := Transform3D(Basis(rot[i]), pos[i])
		var parent := skel.get_bone_parent(i)
		glob[i] = local if parent < 0 else glob[parent] * local


func b(name: String) -> int:
	return skel.find_bone("Bip01 " + name)


func joint(name: String) -> Vector3:
	return glob[b(name)].origin


## Rotate bone `name` (in skeleton space) so the segment to `child` points along `dir`.
## With `bend_toward`, the bone is also twisted so its hinge flexes the child toward that direction
## (elbows, knees): the hinge axis measured in the current pose is carried to the new plane.
func aim(name: String, child: String, dir: Vector3, bend_toward := Vector3.ZERO, grandchild := "") -> void:
	var i := b(name)
	var cur := (joint(child) - joint(name)).normalized()
	var want := dir.normalized()
	var g := glob[i].basis.orthonormalized()
	var target: Basis
	if bend_toward != Vector3.ZERO and grandchild != "":
		var lower := (joint(grandchild) - joint(child)).normalized()
		var hinge := cur.cross(lower)
		if hinge.length() < 0.05:
			hinge = cur.cross(Vector3.FORWARD if absf(cur.dot(Vector3.FORWARD)) < 0.9 else Vector3.UP)
		hinge = hinge.normalized()
		var want_hinge := want.cross(bend_toward.normalized()).normalized()
		var from := Basis(cur, hinge, cur.cross(hinge).normalized())
		var to := Basis(want, want_hinge, want.cross(want_hinge).normalized())
		target = to * from.inverse() * g
	else:
		target = Basis(_arc(cur, want)) * g
	_set_global_basis(i, target)


## Twist a bone about its own segment axis (forearm roll for palm orientation).
func twist(name: String, child: String, degrees: float) -> void:
	var i := b(name)
	var axis := (joint(child) - joint(name)).normalized()
	_set_global_basis(i, Basis(axis, deg_to_rad(degrees)) * glob[i].basis.orthonormalized())


## Rotate a bone by `degrees` about a skeleton-space axis (spine lean, head nod).
func turn(name: String, axis: Vector3, degrees: float) -> void:
	var i := b(name)
	_set_global_basis(i, Basis(axis.normalized(), deg_to_rad(degrees)) * glob[i].basis.orthonormalized())


## Move the whole body vertically (pelvis root) so `name` sits `height` cm above the floor.
func settle(name: String, height: float) -> void:
	var dy := FLOOR_Y + height - joint(name).y
	pos[b("Pelvis")] += _to_local_dir(b("Pelvis"), Vector3(0, dy, 0))
	_fk()


func _to_local_dir(i: int, v: Vector3) -> Vector3:
	var parent := skel.get_bone_parent(i)
	return v if parent < 0 else glob[parent].basis.orthonormalized().inverse() * v


func _set_global_basis(i: int, g: Basis) -> void:
	var parent := skel.get_bone_parent(i)
	var local := g if parent < 0 else glob[parent].basis.orthonormalized().inverse() * g
	rot[i] = local.orthonormalized().get_rotation_quaternion()
	_fk()


static func _arc(a: Vector3, c: Vector3) -> Quaternion:
	var axis := a.cross(c)
	if axis.length() < 1e-6:
		return Quaternion.IDENTITY
	return Quaternion(axis.normalized(), a.angle_to(c))


# ---------------------------------------------------------------------------------------------------------
# Pose library. Directions are in skeleton space: F = forward (+X), U = up, L = character's left (-Z).

const F := Vector3(1, 0, 0)
const U := Vector3(0, 1, 0)
const L := Vector3(0, 0, -1)


## Hands raised beside the head, palms out (the surrender in M06 SH04). `lift` 0..1 blends from
## shoulder height to fully up.
func hands_up(lift := 1.0) -> void:
	for s: float in [1.0, -1.0]:       # left, right
		var side: String = "L" if s > 0 else "R"
		var out: Vector3 = L * s
		var upper: Vector3 = (out * 1.0 + F * 0.28 + U * lerpf(-0.25, 0.12, lift)).normalized()
		var fore: Vector3 = (U * 1.0 + F * 0.12 - out * 0.12).normalized()
		aim(side + " UpperArm", side + " Forearm", upper, fore, side + " Hand")
		aim(side + " Forearm", side + " Hand", fore)
		aim(side + " Hand", side + " Finger2", (fore + F * 0.05).normalized())


## Upright kneel on both knees, shins flat behind, insteps on the floor.
func kneel_both() -> void:
	for s: float in [1.0, -1.0]:
		var side: String = "L" if s > 0 else "R"
		aim(side + " Thigh", side + " Calf", (-U + F * 0.12 + L * s * 0.07).normalized(), -F, side + " Foot")
		aim(side + " Calf", side + " Foot", (-F + -U * 0.12).normalized())
		aim(side + " Foot", side + " Toe0", (-F * 1.0 - U * 0.55).normalized())
	settle("R Calf", KNEE_ON_FLOOR)


## Half kneel: right knee down, left foot planted in front (the step between standing and both knees).
func kneel_right() -> void:
	aim("R Thigh", "R Calf", (-U + F * 0.05 - L * 0.07).normalized(), -F, "R Foot")
	aim("R Calf", "R Foot", (-F - U * 0.15).normalized())
	aim("R Foot", "R Toe0", (-F - U * 0.9).normalized())
	aim("L Thigh", "L Calf", (F * 1.0 - U * 0.22 + L * 0.12).normalized(), -U, "L Foot")
	aim("L Calf", "L Foot", (-U + F * 0.04).normalized())
	aim("L Foot", "L Toe0", (F * 1.0 - U * 0.25).normalized())
	settle("R Calf", KNEE_ON_FLOOR)


## Analytic two-bone placement: the `side` wrist goes to `target` (skeleton space) with the elbow bending toward
## `pole` (a direction), keeping the elbow hinge anatomical.
func place_wrist(side: String, target: Vector3, pole: Vector3) -> void:
	var s := joint(side + " UpperArm")
	var a := s.distance_to(joint(side + " Forearm"))
	var c := joint(side + " Forearm").distance_to(joint(side + " Hand"))
	var to := target - s
	var d := clampf(to.length(), absf(a - c) + 0.5, a + c - 0.5)
	var dir := to.normalized()
	var cos_s := clampf((a * a + d * d - c * c) / (2.0 * a * d), -1.0, 1.0)
	var perp := (pole - dir * pole.dot(dir)).normalized()
	var upper := (dir * cos_s + perp * sqrt(1.0 - cos_s * cos_s)).normalized()
	var fore := (s + dir * d - (s + upper * a)).normalized()
	aim(side + " UpperArm", side + " Forearm", upper, fore, side + " Hand")
	aim(side + " Forearm", side + " Hand", fore)


## Palm normal of a hand from its own landmarks (index/pinky knuckles, middle finger), skeleton space.
func palm_normal(side: String) -> Vector3:
	var f := (joint(side + " Finger2") - joint(side + " Hand")).normalized()
	var w := (joint(side + " Finger1") - joint(side + " Finger4")).normalized()
	return f.cross(w).normalized() * (1.0 if side == "L" else -1.0)


## Turn a hand so its fingers point along `fingers` and its palm faces `palm` (skeleton space).
func orient_hand(side: String, fingers: Vector3, palm: Vector3) -> void:
	var i := b(side + " Hand")
	var f := (joint(side + " Finger2") - joint(side + " Hand")).normalized()
	var n := palm_normal(side)
	var from := Basis(f, n.cross(f).normalized(), n)
	var ft := fingers.normalized()
	var nt := (palm - ft * palm.dot(ft)).normalized()
	var to := Basis(ft, nt.cross(ft).normalized(), nt)
	_set_global_basis(i, to * from.inverse() * glob[i].basis.orthonormalized())


## Curl the four fingers toward the palm (degrees per joint) and the thumb across it. The axis is
## segment x palm normal, so a positive turn always bends a joint toward the palm.
func curl(side: String, degrees: float, thumb := 25.0) -> void:
	for k in [1, 2, 3, 4]:
		var chain: Array[String] = ["%s Finger%d" % [side, k], "%s Finger%d1" % [side, k], "%s Finger%d2" % [side, k]]
		for j in chain.size():
			var seg := (joint(chain[j + 1]) - joint(chain[j])) if j < 2 else (joint(chain[2]) - joint(chain[1]))
			turn(chain[j], seg.normalized().cross(palm_normal(side)).normalized(), degrees * (0.8 if j == 0 else 1.0))
	var thumb_chain: Array[String] = ["%s Finger0" % side, "%s Finger01" % side, "%s Finger02" % side]
	for j in 2:
		var seg := joint(thumb_chain[j + 1]) - joint(thumb_chain[j])
		turn(thumb_chain[j], seg.normalized().cross(palm_normal(side)).normalized(), thumb)


## Wired handset held to the ear: wrist under the ear, fingers wrapped forward round the handle, palm to the cheek.
func handset_to_ear(side := "R") -> void:
	var out := L * (1.0 if side == "L" else -1.0)
	var head := joint("Head")
	place_wrist(side, head + out * 10.5 - F * 1.5 + U * 0.5, (-U * 1.0 + out * 0.5 - F * 0.3).normalized())
	orient_hand(side, (F * 1.0 + U * 0.35 - out * 0.15).normalized(), -out)
	curl(side, 55.0)


## Torso settles back over the knees and the head drops slightly toward the guards.
func kneel_posture() -> void:
	turn("Spine1", L, -4.0)
	turn("Head", L, 8.0)


# ---------------------------------------------------------------------------------------------------------

## Bake `poses` ([time, PoseAuthor]) into an Animation with rotation tracks for every bone and the pelvis position.
func bake(poses: Array, loop := false) -> Animation:
	var a := Animation.new()
	a.length = float(poses[-1][0])
	a.loop_mode = Animation.LOOP_LINEAR if loop else Animation.LOOP_NONE
	var pt := a.add_track(Animation.TYPE_POSITION_3D)
	a.track_set_path(pt, PREFIX + "Bip01 Pelvis")
	for i in skel.get_bone_count():
		var t := a.add_track(Animation.TYPE_ROTATION_3D)
		a.track_set_path(t, PREFIX + skel.get_bone_name(i))
		for key in poses:
			a.rotation_track_insert_key(t, key[0], (key[1] as PoseAuthor).rot[i])
	for key in poses:
		a.position_track_insert_key(pt, key[0], (key[1] as PoseAuthor).pos[b("Pelvis")])
	return a


## Add the authored performances to a character's AnimationPlayer (called once per character load).
static func install(anim: AnimationPlayer, skeleton: Skeleton3D) -> void:
	if anim.has_animation("Kneel_Surrender") or not anim.has_animation("Idle"):
		return
	var idle := PoseAuthor.new(skeleton, anim.get_animation("Idle"))
	var raise := idle.copy()
	raise.hands_up(0.35)
	var half := idle.copy()
	half.hands_up(0.7)
	half.kneel_right()
	var down := idle.copy()
	down.hands_up(1.0)
	down.kneel_both()
	down.kneel_posture()
	var breathe := down.copy()
	breathe.turn("Spine2", L, -1.2)
	var lib := anim.get_animation_library("")
	lib.add_animation("Kneel_Surrender", idle.bake([[0.0, idle], [0.3, raise], [0.75, half], [1.25, down]]))
	lib.add_animation("Kneel_Surrender_Hold", idle.bake([[0.0, down], [1.6, breathe], [3.2, down]], true))
	# M04 shim work (the Fixing_Kneeling clip lunges ~0.7 m forward into the insert camera): half kneel in place;
	# the hand itself is placed on the panel seam by CharacterVisual.reach() IK.
	var work := idle.copy()
	work.kneel_right()
	work.turn("Spine1", F.cross(U), -6.0)
	var work_b := work.copy()
	work_b.turn("Spine2", L, -1.0)
	lib.add_animation("Kneel_Work", idle.bake([[0.0, idle], [0.6, work]]))
	lib.add_animation("Kneel_Work_Hold", idle.bake([[0.0, work], [1.5, work_b], [3.0, work]], true))
	# M05 handset (QA 0101: the open-hand phone clip hid the handset): raise and hold to the ear.
	var phone := idle.copy()
	phone.handset_to_ear("R")
	var phone_b := phone.copy()
	phone_b.turn("Head", F, 2.5)
	lib.add_animation("Handset", idle.bake([[0.0, idle], [0.45, phone]]))
	lib.add_animation("Handset_Hold", idle.bake([[0.0, phone], [1.8, phone_b], [3.6, phone]], true))


## Handset fitted across the curled fingers of a posed hand (hand-bone space, metres before the attach
## scale correction): long axis along the knuckle line (earpiece toward the index), back against the palm.
static func palm_grip(skeleton: Skeleton3D, side := "R", flip := false) -> Transform3D:
	var hand := skeleton.find_bone("Bip01 %s Hand" % side)
	var idx := skeleton.get_bone_rest(skeleton.find_bone("Bip01 %s Finger1" % side)).origin
	var pky := skeleton.get_bone_rest(skeleton.find_bone("Bip01 %s Finger4" % side)).origin
	var mid := skeleton.get_bone_rest(skeleton.find_bone("Bip01 %s Finger2" % side)).origin
	var f := mid.normalized()
	var w := (idx - pky).normalized()
	var n := f.cross(w).normalized() * (1.0 if side == "L" else -1.0)
	var y := (w - f * w.dot(f)).normalized() * (-1.0 if flip else 1.0)
	var basis := Basis(y.cross(n).normalized(), y, n)
	var s: float = skeleton.get_parent().transform.basis.get_scale().x if skeleton.get_parent() is Node3D else 1.0
	assert(hand >= 0)
	return Transform3D(basis, ((idx + pky) * 0.5 * 0.92 + n * 2.6) * s)
