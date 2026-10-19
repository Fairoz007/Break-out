class_name DialogueDirector
extends Node
## Serialised dialogue playback (REQ-DLG-001/003). One intelligible line at a time; plot lines first,
## optional barks wait behind them. Each shown line is logged with its exact text for coverage tests.
## No voice-over exists yet (blocker P06), so a line holds for its screenplay duration.

signal line_started(id: String)
signal line_finished(id: String)

const GAP := 0.3

var chapter: Node
var _queue: Array = []        # [{"id", "speaker", "bark"}]
var _current := {}
var _left := 0.0


func say(id: String, speaker: Node3D = null) -> void:
	_queue.append({"id": id, "speaker": speaker, "bark": false})
	_pump()


## Optional bark: waits behind plot lines and is dropped if the same bark is already waiting.
func bark(id: String, speaker: Node3D = null) -> void:
	for q in _queue:
		if q["id"] == id:
			return
	_queue.append({"id": id, "speaker": speaker, "bark": true})
	_pump()


func busy() -> bool:
	return not _current.is_empty() or not _queue.is_empty()


func current_id() -> String:
	return _current.get("id", "")


func skip_all() -> void:
	for q in _queue:
		GameState.consumed_dialogue[q["id"]] = true
		GameState.log_event("dialogue_skipped", {"id": q["id"]})
	_queue.clear()
	if not _current.is_empty():
		_finish()


func clear() -> void:
	_queue.clear()
	if not _current.is_empty():
		_finish()


func _pump() -> void:
	if not _current.is_empty() or _queue.is_empty():
		return
	# Plot lines take precedence over waiting barks.
	var pick := 0
	for i in _queue.size():
		if not _queue[i]["bark"]:
			pick = i
			break
	_current = _queue.pop_at(pick)
	var line := DialogueDB.line(_current["id"])
	_left = float(line["duration"]) + GAP
	var spk = _current["speaker"]
	if spk is Npc:
		spk.speaking = true
		spk.act("talk")
	if (spk is Npc or spk is Player) and is_instance_valid(spk):
		spk.visual.talking = true
	GameState.consumed_dialogue[line["id"]] = true
	GameState.log_event("dialogue_shown", {"id": line["id"], "speaker": line["speaker"], "text": line["text"], "bark": _current["bark"],
		"cinematic": GameState.cinematic_active})
	chapter.show_subtitle(line, float(line["duration"]))
	line_started.emit(line["id"])


func _finish() -> void:
	var spk = _current.get("speaker")
	if is_instance_valid(spk) and (spk is Npc or spk is Player):
		spk.visual.talking = false
		if spk is Npc:
			spk.speaking = false
			spk.visual.stop_action()
	var id: String = _current["id"]
	_current = {}
	chapter.clear_subtitle()
	line_finished.emit(id)
	_pump()


func _process(delta: float) -> void:
	if _current.is_empty():
		return
	_left -= delta
	if _left <= 0.0:
		_finish()
