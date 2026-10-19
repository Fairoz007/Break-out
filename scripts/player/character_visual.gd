class_name CharacterVisual
extends Node3D
## Realistic Rocketbox character with its 37 retargeted clips (REQ-CHAR-001/002, REQ-ANIM-001/002).
## Locomotion is chosen from speed; actions play once or loop and return to locomotion.

# Rocketbox derivatives with 175 ARKit-style facial blendshapes (acquisition 2026-10-19, MIT); same 80-joint rig
# and 37 clips as the Phase 01.5 bodies.
const FACIAL := "res://assets/characters/acquisition_20261019/rocketbox_facial/"
const MODELS := {
	"ADRIAN": FACIAL + "rb_adrian_cross.glb",
	"NOAH": FACIAL + "rb_noah_reyes.glb",
	"RUSK": FACIAL + "rb_tomas_rusk.glb",
	"GUARD": FACIAL + "rb_tomas_rusk.glb",
	"SILAS": FACIAL + "rb_silas_bell.glb",
	"MARA": FACIAL + "rb_mara_sen.glb",
	"INMATE": FACIAL + "rb_prisoner_npc.glb",
}
# Bespoke performances requested by the screenplay -> nearest available clip (documented substitution table).
const SUBSTITUTE := {
	"search_hands_open": "Idle_No", "badge_look": "Idle_Rail", "inspect": "Interact", "lever_hold": "Push",
	"screen_clear": "Fixing_Kneeling", "lamp_hold": "Idle_Rail", "diagram_read": "Idle_Rail", "shim_palm": "PickUp_Table",
	"shim_work": "Fixing_Kneeling", "hatch_hold": "Push", "crawl": "Crouch_Fwd", "handset": "Idle_TalkingPhone",
	"brake_hold": "Push", "selector_turn": "Interact", "ledger_inspect": "Idle_Rail", "listen": "Idle_FoldArms",
	"handle_pull": "Push", "surrender": "Idle_No", "kneel": "Fixing_Kneeling", "solitary_sit": "Sitting_Idle",
	"pipe_knock": "Interact", "talk": "Idle_Talking", "shove": "Push", "mediate": "Idle_Talking", "ball_roll": "OverhandThrow",
	"patrol": "Walk_Formal", "count": "Idle_Talking", "palm_up": "Idle_No", "cuff": "Interact", "flinch": "Hit_Chest",
}

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


func setup(character_key: String) -> CharacterVisual:
	character = character_key
	name = "Visual"
	model = (load(MODELS[character_key]) as PackedScene).instantiate()
	model.name = "Model"
	# Rocketbox glTF faces +Z; Godot characters face -Z.
	model.rotation.y = PI
	add_child(model)
	anim = model.find_children("*", "AnimationPlayer", true, false)[0]
	anim.playback_default_blend_time = 0.2
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


## Attach a prop model to a hand bone (Rocketbox Biped naming). Returns the prop node.
func attach_to_hand(scene_path: String, right := true, offset := Transform3D.IDENTITY) -> Node3D:
	var skel: Skeleton3D = model.find_children("*", "Skeleton3D", true, false)[0]
	var bone := "Bip01 R Hand" if right else "Bip01 L Hand"
	var ba := BoneAttachment3D.new()
	ba.name = "Hand_" + scene_path.get_file().get_basename()
	ba.bone_name = bone
	skel.add_child(ba)
	var prop: Node3D = (load(scene_path) as PackedScene).instantiate()
	prop.transform = offset
	ba.add_child(prop)
	return prop


func clip_for(action: String) -> String:
	if anim.has_animation(action):
		return action
	return SUBSTITUTE.get(action, "Idle")


## Locomotion from horizontal speed (m/s).
func locomote(speed: float, crouched: bool) -> void:
	_crouched = crouched
	if _action != "":
		return
	var clip := "Idle"
	if crouched:
		clip = "Crouch_Fwd" if speed > 0.15 else "Crouch_Idle"
	elif speed > 2.6:
		clip = "Jog_Fwd"
	elif speed > 0.15:
		clip = "Walk"
	_play(clip, 0.2)
	if clip in ["Walk", "Jog_Fwd", "Crouch_Fwd"]:
		var native: float = {"Walk": 1.35, "Jog_Fwd": 3.4, "Crouch_Fwd": 0.8}[clip]
		anim.speed_scale = clampf(speed / native, 0.6, 1.5)
	else:
		anim.speed_scale = 1.0


## Play a performance; loop=true keeps it until stop_action(). Returns the clip actually used.
func act(action: String, loop := false) -> String:
	var clip := clip_for(action)
	_action = clip
	_action_loop = loop
	anim.speed_scale = 1.0
	_play(clip, 0.15)
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
