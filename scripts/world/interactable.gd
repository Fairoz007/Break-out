class_name Interactable
extends Node3D
## A world interaction point with role ownership and a lease (REQ-COOP-002).
## PRESS fires once per press. HOLD_ACTIVE stays active only while its holder keeps holding (lever, lamp, brake,
## handles). HOLD_COMPLETE must be held for hold_seconds (shim). A lease belongs to exactly one player at a time;
## the other player can never consume it. Missions listen to signals; this node never writes story state.

signal used(player: int)
signal hold_changed(player: int, holding: bool)
signal completed(player: int)

enum Mode { PRESS, HOLD_ACTIVE, HOLD_COMPLETE }
const ANY := -1

@export var id := ""
@export var label := "Interact"
@export var allowed := ANY            # 0 = P1 Adrian, 1 = P2 Noah, -1 = either
@export var mode := Mode.PRESS
@export var hold_seconds := 2.0
@export var radius := 1.4
@export var enabled := true
@export var status_text := ""         # e.g. "Waiting for Noah" (partner waiting state)

var holder := -1
var progress := 0.0
var uses := 0
## Repeatable press controls (selectors, switches) ignore re-presses inside this window so a quick
## double tap or a frame hitch cannot advance a rotary control twice.
var repress_cooldown := 0.25
var _last_press_msec := -100000


func _ready() -> void:
	add_to_group("interactables")


func setup(p_id: String, p_label: String, p_allowed := ANY, p_mode := Mode.PRESS, p_radius := 1.4) -> Interactable:
	id = p_id
	name = p_id
	label = p_label
	allowed = p_allowed
	mode = p_mode
	radius = p_radius
	return self


func can_use(player: int) -> bool:
	return enabled and (allowed == ANY or allowed == player) and (holder == -1 or holder == player)


func role_name() -> String:
	return ["Adrian (P1)", "Noah (P2)"][allowed] if allowed != ANY else "Either player"


func press(player: int) -> bool:
	if not can_use(player):
		GameState.log_event("interact_rejected", {"id": id, "player": player})
		return false
	match mode:
		Mode.PRESS:
			var t := Time.get_ticks_msec()
			if t - _last_press_msec < int(repress_cooldown * 1000.0 / maxf(Engine.time_scale, 0.01)):
				return false
			_last_press_msec = t
			uses += 1
			GameState.log_event("interact", {"id": id, "player": player})
			used.emit(player)
		Mode.HOLD_ACTIVE, Mode.HOLD_COMPLETE:
			_begin(player)
	return true


## Called every physics frame by the holding player with whether the hold input is still down.
func hold_update(player: int, holding: bool, delta: float) -> void:
	if holder != player:
		return
	if not holding or not enabled:
		release(player)
		return
	if mode == Mode.HOLD_COMPLETE:
		progress += delta / max(hold_seconds, 0.01)
		if progress >= 1.0:
			progress = 1.0
			var p := holder
			holder = -1
			uses += 1
			GameState.log_event("interact_complete", {"id": id, "player": p})
			completed.emit(p)


func release(player: int) -> void:
	if holder != player:
		return
	holder = -1
	if mode == Mode.HOLD_COMPLETE and progress < 1.0:
		progress = 0.0
	GameState.log_event("hold_released", {"id": id, "player": player})
	hold_changed.emit(player, false)


func is_held() -> bool:
	return holder != -1


func _begin(player: int) -> void:
	holder = player
	progress = 0.0
	GameState.log_event("hold_started", {"id": id, "player": player})
	hold_changed.emit(player, true)


func force_release() -> void:
	if holder != -1:
		release(holder)
