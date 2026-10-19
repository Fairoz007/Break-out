class_name CharacterVisual
extends Node3D
## Realistic Rocketbox character with its 37 retargeted clips (REQ-CHAR-001/002, REQ-ANIM-001/002).
## Locomotion is chosen from speed; actions play once or loop and return to locomotion.

const MODELS := {
	"ADRIAN": "res://assets/characters/phase15/rocketbox/adrian_cross.glb",
	"NOAH": "res://assets/characters/phase15/rocketbox/noah_reyes.glb",
	"RUSK": "res://assets/characters/phase15/rocketbox/tomas_rusk.glb",
	"GUARD": "res://assets/characters/phase15/rocketbox/tomas_rusk.glb",
	"SILAS": "res://assets/characters/phase15/rocketbox/silas_bell.glb",
	"MARA": "res://assets/characters/phase15/rocketbox/mara_sen.glb",
	"INMATE": "res://assets/characters/phase15/rocketbox/prisoner_npc.glb",
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
	return self


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
	# One-shot performances (including looping clips used once) return to locomotion after one cycle.
	if _action != "" and not _action_loop:
		_action_left -= delta
		if _action_left <= 0.0:
			_action = ""
			locomote(0.0, _crouched)
