extends Node
## Authoritative story state for Chapter 1 (REQ-ARCH-002, REQ-SAVE-001/002/004).
## Only MissionDirector-derived mission scripts write flags, through commit(); every write is a named,
## idempotent transaction so repeated inputs can never duplicate a pickup or double-advance an objective.

signal objective_changed(objective_id: String, text: String)
signal objective_completed(objective_id: String)
signal checkpoint_committed(checkpoint_id: String)
signal event_logged(kind: String, data: Dictionary)

const SCHEMA := 2

var mission_index := 1
var checkpoint_id := "CP01_A"
var flags := {}             # story/puzzle/prop state, e.g. "m01.badge_seen": true
var inventory := {}         # item -> owner/location, e.g. "photo": "NOAH_SHIRT"
var knowledge := {}         # character knowledge snapshot, e.g. "noah.recognized_mark": true
var consumed_dialogue := {} # line id -> true
var transactions := {}      # committed transaction id -> true
var current_objective := ""
var completed_objectives := {}

# Runtime-only (never saved)
var cinematic_active := false
var locks := {}             # name -> true while a door/machine/transfer is mid-motion
var events: Array = []      # evidence log for tests and QA
var session_start_msec := 0


func _ready() -> void:
	session_start_msec = Time.get_ticks_msec()


func reset_new_game() -> void:
	mission_index = 1
	checkpoint_id = "CP01_A"
	flags = {}
	knowledge = {}
	consumed_dialogue = {}
	transactions = {}
	completed_objectives = {}
	current_objective = ""
	# Canon intake starting inventory: Noah carries the photograph and his property.
	inventory = {"photo": "NOAH_HAND", "property": "NOAH_HAND", "shim": "NONE", "diagram": "WORKSHOP_PANEL", "ledger": "PUMP_CONSOLE"}
	log_event("new_game", {})


## Apply a set of changes exactly once. Returns false when the transaction was already committed.
func commit(tx_id: String, changes := {}) -> bool:
	if transactions.has(tx_id):
		log_event("tx_duplicate_ignored", {"tx": tx_id})
		return false
	transactions[tx_id] = true
	for key in changes:
		var k: String = key
		if k.begins_with("inv:"):
			inventory[k.substr(4)] = changes[key]
		elif k.begins_with("know:"):
			knowledge[k.substr(5)] = changes[key]
		else:
			flags[k] = changes[key]
	log_event("tx", {"tx": tx_id, "changes": changes})
	return true


func flag(key: String, default = false):
	return flags.get(key, default)


func set_objective(objective_id: String) -> void:
	if current_objective == objective_id:
		return
	current_objective = objective_id
	var text := DialogueDB.objective_text(objective_id)
	log_event("objective_set", {"id": objective_id, "text": text})
	objective_changed.emit(objective_id, text)


func complete_objective(objective_id: String) -> bool:
	if completed_objectives.has(objective_id):
		return false
	completed_objectives[objective_id] = true
	log_event("objective_completed", {"id": objective_id})
	objective_completed.emit(objective_id)
	return true


func can_save() -> bool:
	return not cinematic_active and locks.is_empty()


## Build the full checkpoint snapshot. Actor transforms and patrol phases come from the chapter.
func snapshot(cp_id: String, actors: Dictionary) -> Dictionary:
	return {
		"schema": SCHEMA, "chapter": "CH01", "mission": "CH01_M0%d" % mission_index, "mission_index": mission_index,
		"checkpoint": cp_id, "saved_unix": Time.get_unix_time_from_system(),
		"players": actors.get("players", []), "patrol": actors.get("patrol", {}),
		"flags": flags.duplicate(true), "inventory": inventory.duplicate(true), "knowledge": knowledge.duplicate(true),
		"consumed_dialogue": consumed_dialogue.keys(), "transactions": transactions.keys(),
		"completed_objectives": completed_objectives.keys(), "objective": current_objective,
	}


func restore(snap: Dictionary) -> void:
	assert(int(snap.get("schema", 0)) == SCHEMA, "Unsupported save schema")
	mission_index = int(snap["mission_index"])
	checkpoint_id = snap["checkpoint"]
	flags = snap["flags"].duplicate(true)
	inventory = snap["inventory"].duplicate(true)
	knowledge = snap["knowledge"].duplicate(true)
	consumed_dialogue = {}
	for id in snap["consumed_dialogue"]:
		consumed_dialogue[id] = true
	transactions = {}
	for t in snap["transactions"]:
		transactions[t] = true
	completed_objectives = {}
	for o in snap["completed_objectives"]:
		completed_objectives[o] = true
	current_objective = ""
	cinematic_active = false
	locks = {}
	log_event("restored", {"checkpoint": checkpoint_id, "mission": mission_index})


func log_event(kind: String, data: Dictionary) -> void:
	var e := {"t": (Time.get_ticks_msec() - session_start_msec) / 1000.0, "kind": kind}
	e.merge(data)
	events.append(e)
	event_logged.emit(kind, e)
