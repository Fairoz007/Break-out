class_name CinematicDirector
extends Node3D
## Shared full-screen cinematics (REQ-CINE-001/002, REQ-CAM-002). Both control contexts are locked, the
## right view is hidden and the left view fills the screen behind letterbox bars. Every shot is a Camera3D
## named with its exact shot ID (CH01_Mnn_CS01_SHnn) that becomes current for its duration.
## A shot never shortens dialogue: it holds at least as long as its lines. Skip needs both players.

signal finished(skipped: bool)

var chapter: Node
var active := false
var skip_votes := [false, false]
var _skipped := false
var _aborted := false
var _last_cam: Camera3D


## shots: [{"id", "from": [pos, look], "to": [pos, look], "lines": [ids], "speakers": {id: node}, "on_start": Callable}]
func play(shots: Array, recap := "") -> bool:
	active = true
	_skipped = false
	_aborted = false
	skip_votes = [false, false]
	GameState.cinematic_active = true
	GameState.log_event("cinematic_start", {"shots": shots.map(func(s): return s["id"])})
	chapter.enter_cinematic()
	var dlg: DialogueDirector = chapter.dialogue
	for i in shots.size():
		var shot: Dictionary = shots[i]
		if _aborted:
			break
		if _skipped:
			for id in shot.get("lines", []):
				GameState.consumed_dialogue[id] = true
				GameState.log_event("dialogue_skipped", {"id": id})
			if shot.has("on_start"):
				shot["on_start"].call()
			continue
		await _play_shot(shot, dlg)
	if _skipped and recap != "" and not _aborted:
		chapter.cinematic_recap(recap)
		await _wait(3.0)
	var last: Transform3D = _last_cam.global_transform if is_instance_valid(_last_cam) else chapter.camera(0).global_transform
	var last_fov: float = _last_cam.fov if is_instance_valid(_last_cam) else 70.0
	for n in get_children():
		n.queue_free()
	chapter.exit_cinematic(last, last_fov)
	GameState.cinematic_active = false
	active = false
	GameState.log_event("cinematic_end", {"skipped": _skipped})
	finished.emit(_skipped)
	return _skipped


func _play_shot(shot: Dictionary, dlg: DialogueDirector) -> void:
	var data := DialogueDB.shot(shot["id"])
	var cam := Camera3D.new()
	cam.name = shot["id"]
	cam.fov = rad_to_deg(2.0 * atan(12.0 / float(data["lens_mm"])))  # full-frame vertical FOV from lens
	cam.near = 0.05
	add_child(cam)
	_last_cam = cam
	var a: Array = shot["from"]
	var b: Array = shot.get("to", a)
	cam.look_at_from_position(a[0], a[1])
	chapter.use_cinematic_camera(cam)
	GameState.log_event("shot_activated", {"id": shot["id"], "lens_mm": data["lens_mm"], "fov": snappedf(cam.fov, 0.1)})
	if shot.has("on_start"):
		shot["on_start"].call()
	var lines: Array = shot.get("lines", [])
	var speakers: Dictionary = shot.get("speakers", {})
	var min_time := float(data["duration"])
	if shot.has("duration"):
		min_time = float(shot["duration"])
	for id in lines:
		dlg.say(id, speakers.get(id))
	var t := 0.0
	var lines_time := 0.0
	for id in lines:
		lines_time += float(DialogueDB.line(id)["duration"]) + DialogueDirector.GAP
	var total := maxf(min_time, lines_time + 0.4)
	# optional hard cut inside a shot (matched cuts): {"at": fraction, "pose": [pos, look]}
	var cut: Dictionary = shot.get("cut", {})
	var cut_done := false
	while t < total:
		await get_tree().process_frame
		if not is_inside_tree():
			return
		var delta := get_process_delta_time()
		if get_tree().paused:
			continue
		t += delta
		if not cut.is_empty() and not cut_done and t / total >= float(cut["at"]):
			cut_done = true
			a = cut["pose"]
			b = cut["pose"]
			GameState.log_event("shot_cut", {"id": shot["id"]})
		var w := smoothstep(0.0, 1.0, clampf(t / total, 0.0, 1.0))
		var pos: Vector3 = (a[0] as Vector3).lerp(b[0], w)
		var look: Vector3 = (a[1] as Vector3).lerp(b[1], w)
		if pos.distance_to(look) > 0.01:
			cam.look_at_from_position(pos, look)
		_poll_skip()
		if _skipped:
			dlg.skip_all()
			return
	while dlg.busy():
		await get_tree().process_frame
		if not is_inside_tree():
			return
		_poll_skip()
		if _skipped:
			dlg.skip_all()
			return


## Used when a checkpoint reload interrupts a cinematic; the reload then restores the saved state.
func abort() -> void:
	if active:
		_skipped = true
		_aborted = true
		chapter.dialogue.clear()


func _poll_skip() -> void:
	for p in 2:
		if Devices.just_pressed(p, "skip") and not skip_votes[p]:
			skip_votes[p] = true
			GameState.log_event("skip_vote", {"player": p})
			chapter.cinematic_skip_status(skip_votes)
	if skip_votes[0] and skip_votes[1]:
		_skipped = true


func _wait(seconds: float) -> void:
	var t := 0.0
	while t < seconds:
		await get_tree().process_frame
		if not get_tree().paused:
			t += get_process_delta_time()
