class_name Mission
extends Node3D
## Base for the six Chapter 1 missions (REQ-ARCH-002, REQ-COOP-003). The mission script is the only writer of
## objective and story state, always through GameState.commit() transactions, so steps are idempotent and a
## checkpoint restore can resume a mission by skipping already-committed steps.
## All waits poll on this node's own tick, so freeing the mission (checkpoint reload) cancels it cleanly.

signal tick
signal mission_finished

var index := 1
var chapter: Node
var b: EnvBuilder
var p1: Player
var p2: Player
var players: Array = []
var npcs := {}
var items := {}       # interactable id -> Interactable
var guards: Array = []
var guide := [{}, {}]   # per-player objective marker {"pos": Vector3, "label": String}; shown in the HUD
var _time := 0.0


func _ready() -> void:
	add_to_group("mission")


func _physics_process(delta: float) -> void:
	_time += delta
	tick.emit()


func now() -> float:
	return _time


# ------------------------------------------------------------------ to override
func build() -> void:
	pass

func spawn(_cp: String) -> Array:
	return [Transform3D.IDENTITY, Transform3D.IDENTITY]

func run() -> void:
	pass


# ------------------------------------------------------------------ construction helpers
func npc(npc_name: String, character_key: String, pos: Vector3, yaw := 0.0) -> Npc:
	var n := Npc.new().setup(npc_name, character_key)
	add_child(n)
	n.place(pos, yaw)
	npcs[npc_name] = n
	return n


func guard(npc_name: String, pos: Vector3, yaw := 0.0, torch := false, character_key := "GUARD") -> GuardAI:
	var g := GuardAI.new().setup_guard(npc_name, character_key, torch)
	add_child(g)
	g.place(pos, yaw)
	npcs[npc_name] = g
	guards.append(g)
	return g


func item(id: String, label: String, pos: Vector3, allowed := Interactable.ANY, mode := Interactable.Mode.PRESS, radius := 1.4) -> Interactable:
	var it := Interactable.new().setup(id, label, allowed, mode, radius)
	add_child(it)
	it.global_position = pos
	items[id] = it
	return it


func xf(pos: Vector3, yaw_deg := 0.0) -> Transform3D:
	return Transform3D(Basis(Vector3.UP, deg_to_rad(yaw_deg)), pos)


func guide_to(p: int, pos: Vector3, label: String) -> void:
	guide[p] = {"pos": pos, "label": label}


func clear_guide(p := -1) -> void:
	for i in 2:
		if p == -1 or p == i:
			guide[i] = {}


## Escort: the NPC walks the route but waits whenever a player falls more than max_gap metres behind it
## (behind = farther from the destination than the escort). Players ahead of the escort never stall it.
func escort(n: Npc, route: Array, max_gap := 4.0) -> void:
	var dest: Vector3 = route[-1]
	for pt in route:
		n.go_to(pt)
		while n.is_moving():
			await tick
			if _someone_behind(n, dest, max_gap) and not n.speaking:
				n.speaking = true      # holds position like a listen mark
				GameState.log_event("escort_wait", {"npc": n.name})
				await until(func(): return not _someone_behind(n, dest, max_gap - 1.5))
				n.speaking = false


func _someone_behind(n: Npc, dest: Vector3, gap: float) -> bool:
	var nd := n.global_position.distance_to(dest)
	for p in players:
		if p.global_position.distance_to(n.global_position) > gap and p.global_position.distance_to(dest) > nd:
			return true
	return false


# ------------------------------------------------------------------ flow helpers (await these)
func until(cond: Callable) -> void:
	while not cond.call():
		await tick


func wait(seconds: float) -> void:
	var end := _time + seconds
	while _time < end:
		await tick


func done(step: String) -> bool:
	return GameState.transactions.has("m%02d.%s" % [index, step])


func commit(step: String, changes := {}) -> bool:
	return GameState.commit("m%02d.%s" % [index, step], changes)


func objective(n: int) -> void:
	GameState.set_objective("CH01_M%02d_OBJ%03d" % [index, n])


func complete_objective(n: int) -> void:
	GameState.complete_objective("CH01_M%02d_OBJ%03d" % [index, n])


func line_id(n: int) -> String:
	return "CH01_M%02d_DLG%03d" % [index, n]


## Play main-sequence lines in order, waiting for each. Lines already consumed (before a checkpoint) are skipped.
## A plot line waits until its listeners are within hearing distance of the speaker.
func say(nums: Array, speakers := {}, hearing := 14.0) -> void:
	for n in nums:
		var id := line_id(n)
		if GameState.consumed_dialogue.has(id):
			continue
		var spk: Node3D = speakers.get(n, _default_speaker(id))
		if spk:
			await until(func(): return _in_hearing(spk, hearing))
		chapter.dialogue.say(id, spk)
		await until(func(): return not chapter.dialogue.busy())


## Optional conditional line; never blocks progress, never repeats once consumed.
func bark(n: int, speaker: Node3D = null) -> void:
	var id := line_id(n)
	if GameState.consumed_dialogue.has(id) or GameState.cinematic_active:
		return
	chapter.dialogue.bark(id, speaker if speaker else _default_speaker(id))


func _default_speaker(id: String) -> Node3D:
	var who: String = DialogueDB.line(id)["speaker"]
	match who:
		"ADRIAN": return p1
		"NOAH": return p2
		"RUSK": return npcs.get("Rusk")
		"GUARD": return npcs.get("Guard")
		"SILAS": return npcs.get("Silas")
		"MARA": return npcs.get("Mara")
	return null


func _in_hearing(spk: Node3D, hearing: float) -> bool:
	if not is_instance_valid(spk):
		return true
	for p in players:
		if p != spk and p.global_position.distance_to(spk.global_position) > hearing:
			return false
	return true


func near(p: Player, pos: Vector3, r := 1.5) -> bool:
	var d := p.global_position - pos
	return Vector2(d.x, d.z).length() <= r and absf(d.y) < 1.5


func both_near(a: Vector3, bpos: Vector3, r := 1.5) -> bool:
	return near(p1, a, r) and near(p2, bpos, r)


func both_in(center: Vector3, r: float) -> bool:
	return near(p1, center, r) and near(p2, center, r)


## Wait for a PRESS interaction (or HOLD_COMPLETE completion) by the allowed actor.
func use(id: String) -> int:
	var it: Interactable = items[id]
	it.enabled = true
	var who := [-1]
	var cb := func(p): who[0] = p
	var sig := it.completed if it.mode == Interactable.Mode.HOLD_COMPLETE else it.used
	sig.connect(cb)
	await until(func(): return who[0] != -1)
	sig.disconnect(cb)
	return who[0]


## Both players confirm ready (REQ-CINE-001 precondition). Shown in each half; interact confirms.
func both_ready(where := "") -> void:
	if where != "":
		GameState.log_event("ready_request", {"where": where})
	for h in chapter.huds:
		h.ask_ready()
	var ok := [false, false]
	while not (ok[0] and ok[1]):
		await tick
		for p in 2:
			if not ok[p] and Devices.just_pressed(p, "interact") and not players[p].input_locked:
				ok[p] = true
				chapter.huds[p].ready_confirmed = true
				GameState.log_event("ready", {"player": p})
	for h in chapter.huds:
		h.ready_requested = false


func cinematic(shots: Array, recap := "") -> void:
	await until(func(): return not chapter.dialogue.busy())
	chapter.cinematic.play(shots, recap)
	await until(func(): return not chapter.cinematic.active)


func checkpoint(cp: String) -> void:
	await until(func(): return GameState.can_save() and not chapter.dialogue.busy())
	chapter.commit_checkpoint(cp)


func set_safe_points() -> void:
	for p in players:
		p.safe_point = p.global_transform


func finish() -> void:
	commit("complete", {})
	GameState.log_event("mission_complete", {"mission": index, "game_seconds": snappedf(_time, 0.1)})
	mission_finished.emit()


# ------------------------------------------------------------------ checkpoint support
func patrol_state() -> Dictionary:
	var out := {}
	for g in guards:
		if is_instance_valid(g) and g.patrolling:
			out[g.name] = g.patrol_state()
	return out


func restore_patrol(state: Dictionary) -> void:
	for g in guards:
		if is_instance_valid(g) and state.has(g.name) and g.waypoints.size() > 0:
			g.restore_patrol(state[g.name])
