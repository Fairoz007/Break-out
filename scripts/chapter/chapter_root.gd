class_name ChapterRoot
extends Control
## Chapter 1 runtime root (REQ-ARCH-001/005, REQ-SPLIT-001, REQ-SAVE-001..003).
## One authoritative World3D rendered by two SubViewports (vertical split: P1 Adrian left, P2 Noah right).
## Owns the players, the dialogue and cinematic directors, the HUDs, checkpoints and mission transitions.

signal chapter_completed
signal quit_to_menu

const MISSION_SCRIPTS := ["", "res://scripts/missions/mission_01.gd", "res://scripts/missions/mission_02.gd",
	"res://scripts/missions/mission_03.gd", "res://scripts/missions/mission_04.gd", "res://scripts/missions/mission_05.gd",
	"res://scripts/missions/mission_06.gd"]

var views: BoxContainer
var containers: Array = []
var viewports: Array = []
var cams: Array = []
var world: Node3D
var players: Array = []
var rigs: Array = []
var huds: Array = []
var hud_row: BoxContainer
var dialogue: DialogueDirector
var cinematic: CinematicDirector
var mission: Mission
var cine_overlay: Control
var cine_subs: Subtitles
var cine_info: Label
var fade: ColorRect
var pause_menu: Control
var last_snapshot := {}
var in_cinematic := false
var transitioning := false


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	process_mode = Node.PROCESS_MODE_ALWAYS
	# Split layout (docs/phase04/CONFLICTS.md C1): canonical vertical split = side by side; horizontal = stacked.
	views = VBoxContainer.new() if Settings.split_mode == "horizontal" else HBoxContainer.new()
	views.name = "SplitScreen"
	views.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	views.add_theme_constant_override("separation", 4)
	add_child(views)
	for i in 2:
		var svc := SubViewportContainer.new()
		svc.name = "View_P%d" % (i + 1)
		svc.stretch = true
		svc.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		svc.size_flags_vertical = Control.SIZE_EXPAND_FILL
		svc.process_mode = Node.PROCESS_MODE_PAUSABLE
		views.add_child(svc)
		var sv := SubViewport.new()
		sv.name = "Viewport_P%d" % (i + 1)
		sv.audio_listener_enable_3d = i == 0
		sv.msaa_3d = Viewport.MSAA_2X
		sv.use_taa = true
		sv.positional_shadow_atlas_size = 4096
		sv.positional_shadow_atlas_quad_0 = Viewport.SHADOW_ATLAS_QUADRANT_SUBDIV_4
		sv.positional_shadow_atlas_quad_1 = Viewport.SHADOW_ATLAS_QUADRANT_SUBDIV_4
		svc.add_child(sv)
		containers.append(svc)
		viewports.append(sv)
	world = Node3D.new()
	world.name = "World"
	viewports[0].add_child(world)
	viewports[1].world_3d = viewports[0].find_world_3d()
	for i in 2:
		var cam := Camera3D.new()
		cam.name = "Camera_P%d" % (i + 1)
		viewports[i].add_child(cam)
		cam.current = true
		cams.append(cam)
	dialogue = DialogueDirector.new()
	dialogue.name = "DialogueDirector"
	dialogue.chapter = self
	dialogue.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(dialogue)
	cinematic = CinematicDirector.new()
	cinematic.name = "Cinematics"
	cinematic.chapter = self
	world.add_child(cinematic)
	for i in 2:
		var p := Player.new().setup(i, ["ADRIAN", "NOAH"][i])
		world.add_child(p)
		players.append(p)
		var rig := PlayerCamera.new().setup(p, cams[i])
		world.add_child(rig)
		rigs.append(rig)
	_build_ui()
	Devices.device_lost.connect(_on_device_lost)
	GameState.checkpoint_committed.connect(_on_checkpoint_sound)


func _build_ui() -> void:
	hud_row = VBoxContainer.new() if Settings.split_mode == "horizontal" else HBoxContainer.new()
	hud_row.name = "HUDs"
	hud_row.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	hud_row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud_row.add_theme_constant_override("separation", 4)
	add_child(hud_row)
	for i in 2:
		var slot := Control.new()
		slot.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		slot.size_flags_vertical = Control.SIZE_EXPAND_FILL
		slot.mouse_filter = Control.MOUSE_FILTER_IGNORE
		hud_row.add_child(slot)
		var h := PlayerHud.new().setup(players[i])
		slot.add_child(h)
		huds.append(h)
	cine_overlay = Control.new()
	cine_overlay.name = "CinematicOverlay"
	cine_overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	cine_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cine_overlay.visible = false
	add_child(cine_overlay)
	for top in [true, false]:
		var bar := ColorRect.new()
		bar.color = Color.BLACK
		bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
		bar.anchor_right = 1.0
		bar.anchor_top = 0.0 if top else 1.0
		bar.anchor_bottom = 0.0 if top else 1.0
		bar.offset_top = 0.0 if top else -120.0
		bar.offset_bottom = 120.0 if top else 0.0
		cine_overlay.add_child(bar)
	cine_subs = Subtitles.new()
	cine_subs.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	cine_overlay.add_child(cine_subs)
	cine_info = Label.new()
	cine_info.position = Vector2(40, 30)
	cine_info.add_theme_font_size_override("font_size", 22)
	cine_info.modulate = Color(1, 1, 1, 0.8)
	cine_overlay.add_child(cine_info)
	fade = ColorRect.new()
	fade.color = Color(0, 0, 0, 0)
	fade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fade)
	pause_menu = load("res://scripts/ui/pause_menu.gd").new()
	pause_menu.chapter = self
	add_child(pause_menu)


func _on_checkpoint_sound(_cp: String) -> void:
	AudioDirector.cue("checkpoint", null, -14.0)


func camera(i: int) -> Camera3D:
	return cams[i]


# ------------------------------------------------------------------ subtitles
func show_subtitle(line: Dictionary, duration: float) -> void:
	if in_cinematic:
		cine_subs.show_line(line, duration)
	else:
		for h in huds:
			h.subtitles.show_line(line, duration)


func clear_subtitle() -> void:
	cine_subs.clear()
	for h in huds:
		h.subtitles.clear()


func visible_subtitle_text() -> String:
	return cine_subs.visible_text() if in_cinematic else huds[0].subtitles.visible_text()


# ------------------------------------------------------------------ cinematics
func enter_cinematic() -> void:
	in_cinematic = true
	for p in players:
		p.input_locked = true
	for r in rigs:
		r.override_active = true
	containers[1].visible = false
	hud_row.visible = false
	cine_overlay.visible = true
	cine_info.text = ""


func use_cinematic_camera(cam: Camera3D) -> void:
	cam.current = true


func exit_cinematic(last: Transform3D, last_fov: float) -> void:
	in_cinematic = false
	cams[0].current = true
	containers[1].visible = true
	hud_row.visible = true
	cine_overlay.visible = false
	cine_subs.clear()
	for i in 2:
		players[i].input_locked = false
		rigs[i].snap_behind(players[i])
		rigs[i].blend_back(last, last_fov)


func cinematic_skip_status(votes: Array) -> void:
	var n := int(votes[0]) + int(votes[1])
	cine_info.text = "Skip requested (%d/2) — both players press Skip" % n


func cinematic_recap(text: String) -> void:
	cine_info.text = "Skipped. " + text


# ------------------------------------------------------------------ missions and checkpoints
func start_new_game() -> void:
	GameState.reset_new_game()
	load_mission(1, {})


func continue_game(snap: Dictionary) -> void:
	last_snapshot = snap
	GameState.restore(snap)
	if GameState.flag("chapter1.complete"):
		GameState.log_event("chapter_complete_save_loaded", {})
		chapter_completed.emit.call_deferred()
		return
	load_mission(int(snap["mission_index"]), snap)


func load_mission(index: int, snap: Dictionary) -> void:
	transitioning = true
	cinematic.abort()
	dialogue.clear()
	if mission:
		world.remove_child(mission)
		mission.queue_free()
		mission = null
	for p in players:
		p.input_locked = false
		p.crouched = false
		p.focus = null
		p.holding = null
	GameState.mission_index = index
	GameState.locks = {}
	var m: Mission = load(MISSION_SCRIPTS[index]).new()
	m.name = "Mission_%02d" % index
	m.index = index
	m.chapter = self
	m.p1 = players[0]
	m.p2 = players[1]
	m.players = players
	world.add_child(m)
	m.b = EnvBuilder.new(m)
	mission = m
	m.build()
	m.b.bake()
	var entry: bool = snap.is_empty() or snap.get("entry", false)
	if entry:
		var sp: Array = m.spawn("CP%02d_A" % index)
		for i in 2:
			players[i].place(sp[i])
	else:
		for i in 2:
			var d: Dictionary = snap["players"][i]
			players[i].place(Transform3D(Basis(Vector3.UP, float(d["yaw"])), Vector3(d["pos"][0], d["pos"][1], d["pos"][2])))
			players[i].crouched = bool(d.get("crouched", false))
		m.restore_patrol(snap.get("patrol", {}))
	AudioDirector.play_scene_ambience(index)
	m.mission_finished.connect(_on_mission_finished.bind(index), CONNECT_ONE_SHOT)
	GameState.log_event("mission_loaded", {"mission": index, "from_snapshot": not snap.is_empty(), "checkpoint": snap.get("checkpoint", "")})
	for h in huds:
		h.objective.text = ""
	_fade_in()
	await get_tree().physics_frame
	if entry:
		commit_checkpoint("CP%02d_A" % index)
	transitioning = false
	m.run()


func commit_checkpoint(cp: String) -> bool:
	if not GameState.can_save():
		GameState.log_event("checkpoint_rejected", {"checkpoint": cp, "cinematic": GameState.cinematic_active, "locks": GameState.locks.keys()})
		return false
	GameState.checkpoint_id = cp
	var actors := {"players": [], "patrol": mission.patrol_state() if mission else {}}
	for p in players:
		actors["players"].append({"pos": [p.global_position.x, p.global_position.y, p.global_position.z], "yaw": p.global_rotation.y, "crouched": p.crouched})
		p.safe_point = p.global_transform
	last_snapshot = GameState.snapshot(cp, actors)
	var ok := SaveService.write(last_snapshot)
	GameState.log_event("checkpoint", {"checkpoint": cp, "written": ok})
	GameState.checkpoint_committed.emit(cp)
	return ok


## Retry from the last committed checkpoint (detection, pause menu). Restores both players atomically.
func reload_checkpoint() -> void:
	if last_snapshot.is_empty():
		return
	GameState.log_event("reload_checkpoint", {"checkpoint": last_snapshot["checkpoint"]})
	call_deferred("_reload_now")


func _reload_now() -> void:
	var snap := last_snapshot.duplicate(true)
	GameState.restore(snap)
	load_mission(int(snap["mission_index"]), snap)


func _on_mission_finished(index: int) -> void:
	if index >= 6:
		GameState.log_event("chapter_complete", {"seconds": (Time.get_ticks_msec() - GameState.session_start_msec) / 1000.0})
		chapter_completed.emit()
		return
	await _fade_out()
	GameState.mission_index = index + 1
	load_mission(index + 1, {})


func _fade_out(seconds := 0.6) -> void:
	var t := create_tween()
	t.tween_property(fade, "color:a", 1.0, seconds)
	await t.finished


func _fade_in(seconds := 0.6) -> void:
	fade.color.a = 1.0
	var t := create_tween()
	t.tween_property(fade, "color:a", 0.0, seconds)


func fade_to_black(seconds := 1.0) -> void:
	await _fade_out(seconds)


func fade_from_black(seconds := 1.0) -> void:
	_fade_in(seconds)


# ------------------------------------------------------------------ pause and devices
func _process(_delta: float) -> void:
	if transitioning:
		return
	for p in 2:
		if Devices.just_pressed(p, "pause"):
			pause_menu.toggle(p)
			break


func _on_device_lost(player: int) -> void:
	GameState.log_event("device_lost", {"player": player})
	pause_menu.open(player, "Controller for %s disconnected. Reconnect it or reassign devices." % ["Adrian (P1)", "Noah (P2)"][player])
