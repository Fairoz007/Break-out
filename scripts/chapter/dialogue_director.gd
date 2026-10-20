class_name DialogueDirector
extends Node
## Serialised dialogue playback (REQ-DLG-001/003). One intelligible line at a time; plot lines first,
## optional barks wait behind them. Each shown line is logged with its exact text for coverage tests.
## Voice-over (Phase 05, ElevenLabs takes in assets/audio/voice/ch01/<LINE_ID>.ogg, tools/phase05_elevenlabs_voices.py):
## a line holds for its screenplay duration or its take, whichever is longer. Cinematic lines play flat on the Dialogue
## bus (ambience and music duck under them); in-world lines and barks play positionally from the speaker. Lines without a take stay subtitle-only.

signal line_started(id: String)
signal line_finished(id: String)

const GAP := 0.3
const VOICE_DIR := "res://assets/audio/voice/ch01/"

var chapter: Node
var _queue: Array = []        # [{"id", "speaker", "bark"}]
var _current := {}
var _left := 0.0
var _voice: Node = null


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
	var hold := float(line["duration"])
	var spk = _current["speaker"]
	var take: String = VOICE_DIR + str(line["id"]) + ".ogg"
	var voiced := ResourceLoader.exists(take)
	if voiced:
		var stream: AudioStream = load(take)
		hold = maxf(hold, stream.get_length())
		_play_voice(stream, spk)
	_left = hold + GAP
	if spk is Npc:
		spk.speaking = true
		spk.act("talk")
	if (spk is Npc or spk is Player) and is_instance_valid(spk):
		spk.visual.talking = true
	GameState.consumed_dialogue[line["id"]] = true
	GameState.log_event("dialogue_shown", {"id": line["id"], "speaker": line["speaker"], "text": line["text"], "bark": _current["bark"],
		"cinematic": GameState.cinematic_active, "voice": voiced, "hold": snappedf(hold, 0.01)})
	chapter.show_subtitle(line, hold)
	line_started.emit(line["id"])


func _play_voice(stream: AudioStream, spk) -> void:
	var v
	if not GameState.cinematic_active and is_instance_valid(spk) and spk is Node3D and (spk as Node3D).is_inside_tree():
		v = AudioStreamPlayer3D.new()
		v.unit_size = 8.0
		v.position = Vector3(0, 1.6, 0)   # mouth height
		spk.add_child(v)
	else:
		v = AudioStreamPlayer.new()
		add_child(v)
	v.stream = stream
	v.bus = "Dialogue"
	v.finished.connect(v.queue_free)
	v.play()
	_voice = v
	AudioDirector.duck(true)


func _finish() -> void:
	if is_instance_valid(_voice):
		_voice.queue_free()
		AudioDirector.duck(false)
	elif _voice != null:
		AudioDirector.duck(false)
	_voice = null
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
