class_name CharacterVisual
extends Node3D
## Realistic Rocketbox character with its 37 retargeted clips (REQ-CHAR-001/002, REQ-ANIM-001/002).
## Locomotion is chosen from speed; actions play once or loop and return to locomotion.

# Rocketbox derivatives with 175 ARKit-style facial blendshapes (acquisition 2026-10-19, MIT); same 80-joint rig
# and 37 clips as the Phase 01.5 bodies.
const FACIAL := "res://assets/characters/acquisition_20261019/rocketbox_facial/"
const MODELS := {
	"ADRIAN": "res://assets/characters/phase05/rb_adrian_cross_p05.glb",   # Phase 05 short hair: tools/phase05_hair.py
	"NOAH": "res://assets/characters/phase05/rb_noah_reyes_p05.glb",   # Phase 05 garments: tools/phase05_noah_garment.py
	"RUSK": FACIAL + "rb_tomas_rusk.glb",
	"GUARD": FACIAL + "rb_tomas_rusk.glb",
	"SILAS": FACIAL + "rb_silas_bell.glb",
	"MARA": FACIAL + "rb_mara_sen.glb",
	"INMATE": FACIAL + "rb_prisoner_npc.glb",
}
# Phase 03 texture repairs applied at load (GLB rigs/blendshapes untouched): original texture file -> fixed copy.
# D03-009: Adrian's recoloured sweater had trouser-grey zigzags along the hem and cuffs.
# Phase 04 likeness pass (tools/phase04_character_textures.py): Adrian grey temple, healed brow cut, grey shirt in
# the V-neck; Noah chambray prison shirt, leather boots, wrist burn (docs/characters/*.md).
const TEXTURE_FIXES := {
	# Adrian's head texture (brow cut) is baked into the Phase 05 GLB with the new hair base; the long hair cards are gone.
	"ADRIAN": {"m003_body_color_prison": "res://assets/characters/phase03/adrian_body_prison_p03.png"},
	"NOAH": {"m007_body_color_prison": "res://assets/characters/phase04/noah_body_prison_p04.png"},
}
# Bespoke performances requested by the screenplay -> nearest available clip (documented substitution table).
const SUBSTITUTE := {
	"search_hands_open": "Idle_No", "badge_look": "Idle_Rail", "inspect": "Interact", "lever_hold": "Push",
	"screen_clear": "Fixing_Kneeling", "lamp_hold": "Idle_Rail", "diagram_read": "Idle_Rail", "shim_palm": "PickUp_Table",
	"shim_work": "Kneel_Work", "hatch_hold": "Push", "crawl": "Crouch_Fwd", "handset": "Handset",
	"brake_hold": "Push", "selector_turn": "Interact", "ledger_inspect": "Idle_Rail", "listen": "Idle_FoldArms",
	"handle_pull": "Push", "shim_work_standing": "Interact", "surrender": "Idle_No", "kneel": "Kneel_Surrender", "solitary_sit": "Sitting_Idle",
	"pipe_knock": "Interact", "talk": "Idle_Talking", "shove": "Push", "mediate": "Idle_Talking", "ball_roll": "OverhandThrow",
	"patrol": "Walk_Formal", "count": "Idle_Talking", "palm_up": "Idle_No", "cuff": "Interact", "flinch": "Hit_Chest",
}

const HAIR_SHELL := preload("res://assets/shaders/hair_shell.gdshader")
## Shim pinched between thumb and fingers, blade out past the fingertips (hand bone +X runs toward the fingers).
static var SHIM_GRIP := Transform3D(Basis(Vector3.UP, PI / 2), Vector3(0.13, -0.01, 0.0))

var character := ""
var anim: AnimationPlayer
var model: Node3D
var _action := ""
var _action_loop := false
var _crouched := false
var _action_left := 0.0
var talking := false            # set by DialogueDirector while this character's line is on screen
var face: MeshInstance3D
var _jaw := -1
var _funnel := -1
var _blinks := []
var _t := 0.0
var _next_blink := 2.0
var _was_grounded := true
var _air_time := 0.0
var _ik := {}
var _stride := 0.0              # metres walked since the last footstep
var footstep_db := -14.0        # players; guards override (heard by the stealth design)                   # "L"/"R" -> {mod: TwoBoneIK3D, target, pole}


func setup(character_key: String) -> CharacterVisual:
	character = character_key
	name = "Visual"
	model = (load(MODELS[character_key]) as PackedScene).instantiate()
	model.name = "Model"
	# Rocketbox glTF faces +Z; Godot characters face -Z.
	model.rotation.y = PI
	add_child(model)
	_apply_texture_fixes()
	_setup_hair_shells()
	anim = model.find_children("*", "AnimationPlayer", true, false)[0]
	anim.playback_default_blend_time = 0.2
	PoseAuthor.install(anim, model.find_children("*", "Skeleton3D", true, false)[0])   # authored kneel (Phase 05)
	anim.play("Idle")
	for m in model.find_children("*", "MeshInstance3D", true, false):
		var mi: MeshInstance3D = m
		if mi.mesh and mi.mesh.get_blend_shape_count() > 0:
			face = mi
			for i in mi.mesh.get_blend_shape_count():
				var n := String(mi.mesh.get_blend_shape_name(i))
				if n.ends_with("_JawOpen"): _jaw = i
				elif n.ends_with("_MouthFunnel"): _funnel = i
				elif "EyeBlink" in n: _blinks.append(i)
			break
	_next_blink = randf_range(1.5, 4.0)
	return self


func _apply_texture_fixes() -> void:
	var fixes: Dictionary = TEXTURE_FIXES.get(character, {})
	if fixes.is_empty():
		return
	for m in model.find_children("*", "MeshInstance3D", true, false):
		var mi: MeshInstance3D = m
		if mi.mesh == null:
			continue
		for i in mi.mesh.get_surface_count():
			var mat := mi.mesh.surface_get_material(i) as BaseMaterial3D
			if mat == null or mat.albedo_texture == null:
				continue
			for key in fixes:
				if key in mat.albedo_texture.resource_path and ResourceLoader.exists(fixes[key]):
					var fixed := mat.duplicate() as BaseMaterial3D
					fixed.albedo_texture = load(fixes[key])
					mi.set_surface_override_material(i, fixed)


## Hair shells (Phase 05, tools/phase05_hair.py): shell k of N shows strands taller than k/N, so each shell is
## alpha-scissored at its own height. Imported glTF alpha arrives as blending; scissor sorts correctly and casts
## shadows.
func _setup_hair_shells() -> void:
	for m in model.find_children("*", "MeshInstance3D", true, false):
		var mi: MeshInstance3D = m
		if mi.mesh == null:
			continue
		var shells := {}
		for i in mi.mesh.get_surface_count():
			var mat := mi.mesh.surface_get_material(i) as BaseMaterial3D
			if mat and mat.resource_name.begins_with("hair_shell_"):
				shells[i] = mat
		var n := shells.size()
		for i in shells:
			var src: BaseMaterial3D = shells[i]
			var k := int(src.resource_name.get_slice("_", 3))
			var mat := ShaderMaterial.new()
			mat.shader = HAIR_SHELL
			mat.set_shader_parameter("strands", src.albedo_texture)
			mat.set_shader_parameter("shell_height", (float(k) - 0.5) / float(n))
			mat.set_shader_parameter("tint", 0.5 + 0.35 * float(k) / float(n))    # darker roots, lighter tips
			mi.set_surface_override_material(i, mat)


## Footsteps by surface (Phase 05 audio): one step per stride while grounded, a heavier one on landing.
func _footsteps(speed: float, crouched: bool, grounded: bool, landed: bool) -> void:
	if landed:
		AudioDirector.footstep(self, _surface_under(), footstep_db + 4.0)
		_stride = 0.0
		return
	if not grounded or speed < 0.4:
		_stride = 0.0 if speed < 0.4 else _stride
		return
	_stride += speed * get_physics_process_delta_time()
	var length := 0.62 if crouched else (0.95 if speed > 2.6 else 0.72)
	if _stride >= length:
		_stride = 0.0
		AudioDirector.footstep(self, _surface_under(), footstep_db - (8.0 if crouched else 0.0) + (3.0 if speed > 4.2 else 0.0))


## Surface below the character from the floor body's material (EnvBuilder tags its materials); cached per body.
func _surface_under() -> String:
	if not is_inside_tree():
		return "concrete"
	var from := global_position + Vector3(0, 0.3, 0)
	var q := PhysicsRayQueryParameters3D.create(from, from + Vector3(0, -0.8, 0), EnvBuilder.LAYER_WORLD)
	var hit := get_world_3d().direct_space_state.intersect_ray(q)
	if hit.is_empty() or not (hit["collider"] is Node):
		return "concrete"
	var body: Node = hit["collider"]
	if body.has_meta("surface"):
		return body.get_meta("surface")
	var surface := "concrete"
	for c in body.get_children():
		if c is MeshInstance3D and (c as MeshInstance3D).material_override:
			var m: Material = (c as MeshInstance3D).material_override
			var tag := str(m.get_meta("surface_name", "")) + " " + (str((m as BaseMaterial3D).albedo_texture.resource_path) if m is BaseMaterial3D and (m as BaseMaterial3D).albedo_texture else "")
			if "metal" in tag or "grate" in tag:
				surface = "metal"
			elif "asphalt" in tag:
				surface = "asphalt"
			elif "tile" in tag:
				surface = "tile"
			break
	body.set_meta("surface", surface)
	return surface


## Hand props a mission will attach (MissionDirector.hand_props) start loading on a worker thread when the mission
## loads, so attach_to_hand never loads from disk mid-shot (D05-014: the 25 MB handcuffs GLB loaded synchronously
## on the first frame of M06 SH05 stalled the main thread 1.66 s).
static var _props := {}


static func warm_props(paths: Array) -> void:
	for p in paths:
		if not _props.has(p) and ResourceLoader.exists(p):
			_props[p] = null
			ResourceLoader.load_threaded_request(p)


static func prop_scene(path: String) -> PackedScene:
	if _props.get(path) != null:
		return _props[path]
	var scene: PackedScene
	if _props.has(path) and ResourceLoader.load_threaded_get_status(path) != ResourceLoader.THREAD_LOAD_INVALID_RESOURCE:
		scene = ResourceLoader.load_threaded_get(path)   # waits only for whatever is left of the background load
	if scene == null:
		scene = load(path)
	_props[path] = scene
	return scene


## Attach a prop model to a hand bone (Rocketbox Biped naming). Returns the prop node.
func attach_to_hand(scene_path: String, right := true, offset := Transform3D.IDENTITY) -> Node3D:
	var skel: Skeleton3D = model.find_children("*", "Skeleton3D", true, false)[0]
	var bone := "Bip01 R Hand" if right else "Bip01 L Hand"
	var ba := BoneAttachment3D.new()
	ba.name = "Hand_" + scene_path.get_file().get_basename()
	ba.bone_name = bone
	skel.add_child(ba)
	var prop: Node3D = prop_scene(scene_path).instantiate()
	# The Rocketbox skeleton sits under a 0.01-scaled armature, so a bone attachment inherits that scale.
	# Offsets are authored in metres at prop scale 1: undo the skeleton-to-character scale (was 100x too small).
	var chain := Transform3D.IDENTITY
	var cur: Node = skel
	while cur != null and cur != self and cur is Node3D:
		chain = (cur as Node3D).transform * chain
		cur = cur.get_parent()
	var s := chain.basis.get_scale().x
	if s > 0.0001 and absf(s - 1.0) > 0.001:
		offset = Transform3D(offset.basis.scaled(Vector3.ONE / s), offset.origin / s)
	prop.transform = offset
	ba.add_child(prop)
	return prop


## A handle fitted across this character's curled fingers (wired handset), for attach_to_hand.
func palm_grip(side := "R", flip := false) -> Transform3D:
	return PoseAuthor.palm_grip(model.find_children("*", "Skeleton3D", true, false)[0], side, flip)


## Hand contact (Phase 05, D05-008): two-bone IK puts the `side` ("L"/"R") wrist at the world point `target`,
## elbow toward `pole` (default: down and out from the shoulder). It layers over whatever clip is playing,
## so a hand lands on the actual lock or handle instead of pushing air. Fades in over `blend` seconds.
func reach(side: String, target: Vector3, pole := Vector3.INF, blend := 0.3) -> void:
	var skel: Skeleton3D = model.find_children("*", "Skeleton3D", true, false)[0]
	if not _ik.has(side):
		var mod := TwoBoneIK3D.new()
		mod.name = "Reach_" + side
		mod.set_setting_count(1)
		mod.set_root_bone_name(0, "Bip01 %s UpperArm" % side)
		mod.set_middle_bone_name(0, "Bip01 %s Forearm" % side)
		mod.set_end_bone_name(0, "Bip01 %s Hand" % side)
		mod.influence = 0.0
		var t := Marker3D.new()
		var p := Marker3D.new()
		t.top_level = true
		p.top_level = true
		add_child(t)
		add_child(p)
		skel.add_child(mod)
		mod.set_target_node(0, mod.get_path_to(t))
		mod.set_pole_node(0, mod.get_path_to(p))
		_ik[side] = {"mod": mod, "target": t, "pole": p}
	var e: Dictionary = _ik[side]
	(e["target"] as Marker3D).global_position = target
	if pole == Vector3.INF:
		var shoulder := skel.global_transform * skel.get_bone_global_pose(skel.find_bone("Bip01 %s UpperArm" % side)).origin
		var out := global_transform.basis.x * (1.0 if side == "R" else -1.0)
		pole = shoulder.lerp(target, 0.5) + Vector3.DOWN * 0.45 + out.normalized() * 0.3
	(e["pole"] as Marker3D).global_position = pole
	var tw := create_tween()
	tw.tween_property(e["mod"], "influence", 1.0, blend)


func release_reach(side: String, blend := 0.25) -> void:
	if _ik.has(side):
		create_tween().tween_property(_ik[side]["mod"], "influence", 0.0, blend)


func reaching(side: String) -> float:
	return (_ik[side]["mod"] as TwoBoneIK3D).influence if _ik.has(side) else 0.0


func clip_for(action: String) -> String:
	if anim.has_animation(action):
		return action
	return SUBSTITUTE.get(action, "Idle")


## Locomotion from horizontal speed (m/s).
func locomote(speed: float, crouched: bool, grounded := true, vertical_speed := 0.0) -> void:
	_crouched = crouched
	# Observe grounding even during actions, so resuming control cannot replay an old landing.
	var landed := grounded and not _was_grounded and _air_time > 0.12
	if grounded:
		_air_time = 0.0
	_was_grounded = grounded
	_footsteps(speed, crouched, grounded, landed)
	if not grounded and _action == "Jump_Land":
		# A new jump takes precedence over the previous landing's visual recovery.
		stop_action()
	if _action != "":
		return
	if not grounded:
		# Godot strips the glTF _Loop suffix during import (Jump_Loop becomes Jump).
		var airborne := "Jump_Start" if vertical_speed > 1.5 else "Jump"
		_play(airborne, 0.12)
		anim.speed_scale = 1.0
		return
	if landed and anim.has_animation("Jump_Land"):
		act("Jump_Land")
		return
	var clip := "Idle"
	if crouched:
		clip = "Crouch_Fwd" if speed > 0.15 else "Crouch_Idle"
	elif speed > 4.2:
		clip = "Sprint"
	elif speed > 2.6:
		clip = "Jog_Fwd"
	elif speed > 0.15:
		clip = "Walk"
	_play(clip, 0.2)
	if clip in ["Walk", "Jog_Fwd", "Sprint", "Crouch_Fwd"]:
		var native: float = {"Walk": 1.35, "Jog_Fwd": 3.4, "Sprint": 5.2, "Crouch_Fwd": 0.8}[clip]
		anim.speed_scale = clampf(speed / native, 0.6, 1.5)
	else:
		anim.speed_scale = 1.0


## Play a performance; loop=true keeps it until stop_action(). Returns the clip actually used.
## No pull clip exists in the retargeted set: pulling plays the push performance in reverse (arms drawn back).
const REVERSED := ["handle_pull"]


func act(action: String, loop := false) -> String:
	var clip := clip_for(action)
	_action = clip
	_action_loop = loop
	anim.speed_scale = 1.0
	if action in REVERSED:
		anim.play_backwards(clip, 0.15)
	else:
		_play(clip, 0.15)
		if loop and anim.has_animation(clip + "_Hold"):
			anim.queue(clip + "_Hold")   # authored transition, then its held loop
	_action_left = anim.get_animation(clip).length if not loop else 0.0
	GameState.log_event("clip", {"character": character, "action": action, "clip": clip})
	return clip


func stop_action() -> void:
	_action = ""
	_action_loop = false


func current_clip() -> String:
	return anim.current_animation


func _play(clip: String, blend: float) -> void:
	if anim.current_animation != clip:
		anim.play(clip, blend)


func _process(delta: float) -> void:
	_t += delta
	if not _was_grounded:
		_air_time += delta
	if face:
		# Speech approximation from the subtitle timing (no voice-over or visemes exist yet: blocker P01/P06).
		if _jaw >= 0:
			var target := 0.0
			if talking:
				target = clampf(0.18 + 0.32 * absf(sin(_t * 9.0)) * (0.6 + 0.4 * sin(_t * 2.3)), 0.0, 0.55)
			face.set_blend_shape_value(_jaw, lerpf(face.get_blend_shape_value(_jaw), target, clampf(18.0 * delta, 0.0, 1.0)))
		if _funnel >= 0:
			face.set_blend_shape_value(_funnel, (0.15 * maxf(0.0, sin(_t * 5.0))) if talking else 0.0)
		_next_blink -= delta
		var b := 1.0 if _next_blink < 0.0 and _next_blink > -0.12 else 0.0
		for i in _blinks:
			face.set_blend_shape_value(i, b)
		if _next_blink <= -0.12:
			_next_blink = randf_range(2.0, 5.0)
	# One-shot performances (including looping clips used once) return to locomotion after one cycle.
	if _action != "" and not _action_loop:
		_action_left -= delta
		if _action_left <= 0.0:
			_action = ""
			locomote(0.0, _crouched)
