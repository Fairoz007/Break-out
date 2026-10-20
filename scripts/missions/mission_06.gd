extends Mission
## CH01_M06 THE BETRAYAL — scene CH01_M06_SC01, cinematic CH01_M06_CS01 (docs/missions/CH01_MISSION_06.md).
## Both pull the two handles together (no false escape test). The rear grille drops once both stand on their
## marks, the door stops at the security grille, the steady red alarm comes on and Rusk arrives with two guards:
## an authored, uninterrupted capture reel (lines 003-021). After the fade both are in separate solitary cells;
## each answers the pipe independently (P1 knocks three times, P2 answers), lines 022-026 play through the pipe,
## and the chapter ends with the CH02 NIGHT SHIFT card. Capture is success, never a fail state.

var env: Dictionary
var sol: Dictionary


func build() -> void:
	env = EnvMaintenance.build(b)
	sol = EnvSolitary.build(b)
	var captured := done("capture")
	if not captured:
		npc("Rusk", "RUSK", env["rusk_hidden"], 90.0)
		guard("Guard", env["rusk_hidden"] + Vector3(1.4, 0, -1.2), 90.0)
		guard("Guard2", env["rusk_hidden"] + Vector3(1.4, 0, 1.4), 90.0)
	item("m06_handle_w", "Pull the west handle (keep holding)", env["handle_w"] + Vector3(0.5, 1.0, 0), 0, Interactable.Mode.HOLD_ACTIVE, 1.1)
	item("m06_handle_e", "Pull the east handle (keep holding)", env["handle_e"] + Vector3(0.5, 1.0, 0), 1, Interactable.Mode.HOLD_ACTIVE, 1.1)
	item("m06_pipe_p1", "Knock three times on the pipe", sol["pipe_p1"], 0, Interactable.Mode.PRESS, 1.4)
	item("m06_pipe_p2", "Answer the knocks", sol["pipe_p2"], 1, Interactable.Mode.PRESS, 1.4)
	for id in items:
		items[id].enabled = false


func hand_props() -> Array:
	return ["res://assets/props/acquisition_20261019/simple_handcuffs.glb"]


func spawn(cp: String) -> Array:
	return [xf(env["handle_w"], -90.0), xf(env["handle_e"], -90.0)]


func _alarm(on: bool) -> void:
	# steady red wash, never strobing (reduced-flash default; GAME_DESIGN accessibility)
	var we: WorldEnvironment = env["world_env"]
	we.environment.ambient_light_color = Color(0.9, 0.12, 0.1) if on else Color(0.4, 0.46, 0.55)
	we.environment.ambient_light_energy = 0.6 if on else 0.3
	var l: OmniLight3D = env["spill_light"]
	l.light_color = Color(1.0, 0.1, 0.08) if on else Color(1.0, 0.6, 0.25)
	l.light_energy = 3.0 if on else 1.6
	if on:
		AudioDirector.start_bed("alarm", -16.0)
	else:
		AudioDirector.stop_bed("alarm")
	GameState.log_event("alarm", {"on": on, "steady": true})


func run() -> void:
	if not done("handles"):
		objective(1)
		var hw: Interactable = items["m06_handle_w"]
		var he: Interactable = items["m06_handle_e"]
		hw.enabled = true
		he.enabled = true
		await say([1])
		var counted := false
		var one_since := -1.0
		var both_since := -1.0
		while not done("handles"):
			await tick
			var a := hw.holder == 0
			var n := he.holder == 1
			hw.status_text = "" if n else "Waiting for Noah"
			he.status_text = "" if a else "Waiting for Adrian"
			if a != n:
				if one_since < 0.0:
					one_since = now()
				elif now() - one_since > 10.0:
					bark(27, p1)   # handle idle
					one_since = now()
			else:
				one_since = -1.0
			if a and n and not counted:
				await say([2])
				counted = true
				both_since = now()
			if counted and a and n and now() - both_since > 0.5:
				complete_objective(1)
				commit("handles")
			if counted and not (a and n):
				both_since = now()
		hw.enabled = false
		he.enabled = false
	if not done("capture"):
		var rusk: Npc = npcs["Rusk"]
		var g1: Npc = npcs["Guard"]
		var g2: Npc = npcs["Guard2"]
		for n in [rusk, g1, g2]:
			n.cinematic_controlled = true
		await cinematic([
			{"id": "CH01_M06_CS01_SH01", "from": [Vector3(26.0, 1.45, -24.3), Vector3(29.4, 0.85, -24.0)], "to": [Vector3(26.4, 1.45, -24.15), Vector3(29.6, 0.85, -24.0)],
				"on_start": func():
					p1.place(xf(env["handle_w"], -90.0))
					p2.place(xf(env["handle_e"], -90.0))
					p1.visual.act("handle_pull", true)
					p2.visual.act("handle_pull", true)
					env["doors"]["rear_grille"].set_open(false)
					env["doors"]["spillway"].hinge.position = Vector3(0, 0, -0.9)
					AudioDirector.cue("door_open", p1)},
			{"id": "CH01_M06_CS01_SH02", "from": [Vector3(29.4, 1.6, -24.0), Vector3(33.5, 1.55, -24.0)], "to": [Vector3(29.6, 1.6, -24.0), Vector3(33.0, 1.55, -24.0)],
				"lines": [line_id(3), line_id(4), line_id(5), line_id(6), line_id(7)], "speakers": {line_id(3): rusk, line_id(5): rusk, line_id(7): rusk},
				"on_start": func():
					_alarm(true)
					p1.visual.act("flinch")
					p2.visual.act("flinch")
					env["doors"]["security_grille"].set_open(true)
					rusk.place(Vector3(33.4, 0, -24.0), 90.0)
					g1.place(Vector3(33.0, 0, -22.4), 90.0)
					g2.place(Vector3(33.0, 0, -25.6), 90.0)
					rusk.act("palm_up", true)},
			{"id": "CH01_M06_CS01_SH03", "from": [Vector3(31.4, 1.62, -22.9), Vector3(33.4, 1.6, -24.0)], "to": [Vector3(31.2, 1.62, -25.1), Vector3(29.4, 1.6, -23.6)],
				"lines": [line_id(8), line_id(9), line_id(10), line_id(11), line_id(12), line_id(13)], "speakers": {line_id(9): rusk, line_id(11): rusk, line_id(13): rusk},
				"cut": {"at": 0.86, "pose": [Vector3(31.2, 1.62, -23.2), Vector3(33.4, 1.6, -24.0)]}},
			{"id": "CH01_M06_CS01_SH04", "from": [Vector3(33.9, 1.45, -20.4), Vector3(30.5, 0.75, -24.0)], "to": [Vector3(33.6, 1.4, -20.7), Vector3(30.5, 0.75, -24.0)],
				"lines": [line_id(14), line_id(15), line_id(16), line_id(17), line_id(18)], "speakers": {line_id(14): g1},
				"on_start": func():
					# Through the opened spillway, turned to face the guards (the x30 wall hides the doorway from the north).
					p1.place(xf(env["handle_w"] + Vector3(1.3, 0, 0), -90.0))
					p2.place(xf(env["handle_e"] + Vector3(1.3, 0, 0), -90.0))
					# On the order (DLG014, 2.9 s): hands up and down onto both knees in 1.25 s (authored
					# Kneel_Surrender), Noah a beat behind Adrian; both are kneeling before the line ends.
					p1.visual.act("kneel", true)
					await wait(0.2)
					p2.visual.act("kneel", true)
					g1.go_to(Vector3(31.3, 0, -23.0))
					g2.go_to(Vector3(31.3, 0, -25.0))},
			{"id": "CH01_M06_CS01_SH05", "from": [Vector3(31.6, 1.6, -23.4), Vector3(33.4, 1.6, -24.0)], "to": [Vector3(32.2, 1.15, -24.6), Vector3(30.5, 0.95, -23.9)],
				"lines": [line_id(19), line_id(20), line_id(21)], "speakers": {line_id(19): rusk, line_id(20): g1, line_id(21): rusk},
				"on_start": func():
					AudioDirector.cue("cuffs", p1)
					for g in [g1, g2]:
						g.visual.attach_to_hand("res://assets/props/acquisition_20261019/simple_handcuffs.glb", true,
							Transform3D(Basis.from_euler(Vector3(PI / 2, 0, 0)), Vector3(0.06, 0.04, 0)))
					g1.act("cuff")
					g2.act("cuff")},
			{"id": "CH01_M06_CS01_SH06", "from": sol["face_p1"], "cut": {"at": 0.5, "pose": sol["face_p2"]},
				"on_start": func():
					_alarm(false)
					AudioDirector.stop_all_beds()
					AudioDirector.start_bed("ventilation", -26.0)
					p1.place(xf(sol["seat_p1"], 180.0))
					p2.place(xf(sol["seat_p2"], 180.0))
					p1.visual.act("solitary_sit", true)
					p2.visual.act("solitary_sit", true)
					rusk.visible = false
					g1.visible = false
					g2.visible = false},
		], "Rusk was waiting for them; both are captured, the shim confiscated, and separated into solitary.")
		for p in players:
			p.visual.stop_action()
		commit("capture", {"inv:shim": "CONFISCATED", "inv:photo": "NOAH_SHIRT", "know:both.rusk_betrayal_known": true, "m06.separately_confined": true})
		for n in [rusk, g1, g2]:
			n.queue_free()
		await checkpoint("CP06_B")   # after capture, in solitary, before the pipe responses
	if not done("pipe"):
		objective(2)
		var k1: Interactable = items["m06_pipe_p1"]
		var k2: Interactable = items["m06_pipe_p2"]
		k1.enabled = true
		guide_to(0, sol["pipe_p1"] - Vector3(0, 1.1, -0.5), "The pipe on the wall")
		guide_to(1, sol["pipe_p2"] - Vector3(0, 1.1, -0.5), "The pipe on the wall")
		k2.status_text = "Listen for Adrian's knocks"
		var t0 := now()
		while k1.uses == 0:
			await tick
			if now() - t0 > 15.0:
				bark(28, p2)   # pipe idle
				t0 = now() + 1000.0
		k1.enabled = false
		p1.visual.act("pipe_knock")
		for i in 3:
			AudioDirector.cue("pipe_knock", p1)
			await wait(0.55)
		k2.enabled = true
		k2.status_text = "Three knocks through the wall"
		await use("m06_pipe_p2")
		k2.enabled = false
		p2.visual.act("pipe_knock")
		for i in 3:
			AudioDirector.cue("pipe_reply", p2)
			await wait(0.55)
		await say([22, 23, 24, 25, 26], {}, 20.0)
		clear_guide()
		complete_objective(2)
		commit("pipe")
	commit("exit", CanonStates.exit_changes(6))
	chapter.commit_checkpoint("CH01_COMPLETE")   # chapter-end save commits the responses and confiscation once
	await chapter.fade_to_black(1.5)
	finish()
