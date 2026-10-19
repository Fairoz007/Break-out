extends Mission
## CH01_M02 TROUBLE IN THE YARD — scene CH01_M02_SC01, cinematic CH01_M02_CS01 (docs/missions/CH01_MISSION_02.md).
## P1 Adrian holds Silas's attention at the mediation mark (hold) while P2 Noah rolls the loose ball into the
## empty west fence lane; the guard looks west, Silas withdraws, both withdraw to the tap alcove. Missed timing
## resets the standoff; the ball never strikes an NPC; there is no fight or damage.

var env: Dictionary
var ball: Node3D


func build() -> void:
	env = EnvYard.build(b)
	npc("Silas", "SILAS", env["silas"], 0.0 if not done("distraction") else 0.0)
	var ia := npc("InmateA", "INMATE", env["inmate_a"], 270.0)
	var ib := npc("InmateB", "INMATE", env["inmate_b"], 270.0)
	ia.act("Idle_FoldArms", true)
	ib.act("Idle_Rail", true)
	var g := guard("Guard", Vector3(35, 0, -6), 0.0)
	g.start_patrol([{"pos": Vector3(35, 0, -6), "wait": 3.0, "look": Vector3(20, 1, -6)}, {"pos": Vector3(35, 0, -24), "wait": 3.0, "look": Vector3(20, 1, -24)}])
	var g2 := guard("GuardNorth", Vector3(12, 0, -28), 90.0)
	g2.start_patrol([{"pos": Vector3(12, 0, -28), "wait": 2.0}, {"pos": Vector3(28, 0, -28), "wait": 2.0}])
	ball = b.model("res://assets/props/phase15/basketball.glb", env["ball"], 0, "none", self)
	item("m02_mediate", "Hold Silas's attention (keep holding)", env["mediate"] + Vector3(0, 1, 0), 0, Interactable.Mode.HOLD_ACTIVE, 1.2)
	item("m02_ball", "Roll the loose ball to the west fence", env["ball"] + Vector3(0, 0.8, 0), 1, Interactable.Mode.PRESS, 1.2)
	item("m02_doubt", "Voice your doubt (optional)", env["tap_p2"] + Vector3(0, 1, 0), 1, Interactable.Mode.PRESS, 2.0)
	for id in items:
		items[id].enabled = false
	if done("distraction"):
		ball.position = env["fence_target"]
		npcs["Silas"].place(env["north_fence"], 180.0)
		ia.place(env["north_fence"] + Vector3(2, 0, 0.5), 180.0)
		ib.place(env["north_fence"] + Vector3(-2, 0, 0.5), 180.0)
	if done("entered"):
		env["doors"]["D1"].set_open(true, false)


func spawn(_cp: String) -> Array:
	return [xf(env["adrian_start"], 180.0), xf(env["noah_start"], 270.0)]


func run() -> void:
	var silas: Npc = npcs["Silas"]
	var guard_e: GuardAI = npcs["Guard"]
	silas.face(env["bench"])
	if not done("intro"):
		await both_ready("CH01_M02_CS01 intro")
		await cinematic([{"id": "CH01_M02_CS01_SH01", "from": [Vector3(5, 5, -4), Vector3(20, 1.2, -15)], "to": [Vector3(6, 5, -4.5), Vector3(20, 1.2, -16)],
			"on_start": func(): AudioDirector.cue("fence_rattle", null, -14.0)}], "The yard: west fence, tap alcove and Silas's bench.")
		commit("intro")
	if not done("entered"):
		objective(1)
		env["doors"]["D1"].set_open(true)
		guide_to(0, env["court_center"] + Vector3(-2, 0, -2), "Into the yard")
		guide_to(1, env["court_center"], "Into the yard")
		var court := func(p: Player): return p.global_position.x > 10.0 and p.global_position.x < 30.0 and p.global_position.z < -6.0 and p.global_position.z > -22.0
		await until(func(): return court.call(p1) and court.call(p2))
		complete_objective(1)
		commit("entered")
	if not done("confrontation"):
		guide_to(1, env["bench"], "Exercise bench")
		guide_to(0, env["mediate"], "Mediation space beside the bench")
		await until(func(): return near(p2, env["bench"], 1.6) and near(p1, env["mediate"], 3.5))
		clear_guide()
		await both_ready("CH01_M02_CS01_SH02")
		await cinematic([
			{"id": "CH01_M02_CS01_SH02", "from": [Vector3(21.0, 1.6, -14.6), Vector3(24.6, 1.5, -13.2)], "to": [Vector3(21.2, 1.6, -14.2), Vector3(24.4, 1.5, -13.0)],
				"lines": [line_id(1), line_id(2), line_id(3), line_id(4)], "speakers": {line_id(1): silas, line_id(3): silas, line_id(2): p2, line_id(4): p1},
				"on_start": func():
					silas.act("shove")
					p2.place(xf(env["bench"], 0.0))},
			{"id": "CH01_M02_CS01_SH03", "from": [Vector3(23.4, 1.5, -11.6), Vector3(24.2, 1.2, -12.9)], "to": [Vector3(23.6, 1.45, -11.8), Vector3(24.3, 1.2, -12.9)],
				"lines": [line_id(5), line_id(6)], "speakers": {line_id(5): silas, line_id(6): p1},
				"on_start": func():
					p1.place(xf(env["mediate"], 200.0))
					p1.visual.act("palm_up")},
		], "Silas blocks Noah; Adrian steps between them with an open hand.")
		commit("confrontation")
	if not done("distraction"):
		objective(2)
		var mediate: Interactable = items["m02_mediate"]
		var roll: Interactable = items["m02_ball"]
		guide_to(0, env["mediate"], "Hold Silas's attention")
		guide_to(1, env["ball"], "Loose basketball")
		mediate.enabled = true
		var window_lines_done := false
		var t_window := -1.0
		while not done("distraction"):
			await tick
			var mediating := mediate.holder == 0
			mediate.status_text = "" if mediating else "Hold to keep Silas talking"
			roll.status_text = "Adrian is holding Silas's attention — roll now" if mediating else "Wait: Adrian must hold Silas's attention"
			roll.set_meta("ready_now", mediating and window_lines_done)
			roll.enabled = mediating and window_lines_done
			if mediating and not window_lines_done:
				await say([7, 8, 9])
				window_lines_done = true
				t_window = now()
			if window_lines_done and not mediating:
				# missed timing: the conversation window closed before the ball rolled
				if roll.uses == 0 and t_window > 0.0:
					bark(22, p1)
					GameState.log_event("distraction_reset", {})
					t_window = -1.0
			if mediating and window_lines_done and t_window > 0.0 and now() - t_window > 20.0:
				bark(21, silas)   # distraction idle after 20 s
				t_window = now()
			if roll.uses > 0:
				if not mediating:
					roll.uses = 0
					continue
				roll.enabled = false
				p2.visual.act("ball_roll")
				var t := create_tween()
				t.tween_property(ball, "position", env["fence_target"], 3.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
				t.parallel().tween_property(ball, "rotation:z", 18.0, 3.5)
				AudioDirector.cue("ball_bounce", p2)
				await wait(3.5)
				AudioDirector.cue("fence_rattle", ball)
				guard_e.investigate(Vector3(2, 1, -12), 8.0)
				mediate.enabled = false
				await say([10, 11], {10: guard_e, 11: silas}, 40.0)
				silas.go_to(env["north_fence"])
				npcs["InmateA"].go_to(env["north_fence"] + Vector3(2, 0, 0.5))
				npcs["InmateB"].go_to(env["north_fence"] + Vector3(-2, 0, 0.5))
				complete_objective(2)
				commit("distraction", {"m02.ball_at_west_fence": true})
	if not done("alcove"):
		objective(3)
		guide_to(0, env["tap_p1"], "Tap alcove")
		guide_to(1, env["tap_p2"], "Tap alcove")
		await until(func(): return near(p1, env["tap"], 2.2) and near(p2, env["tap"], 2.2))
		clear_guide()
		AudioDirector.cue("whistle", null, -10.0)
		complete_objective(3)
		commit("alcove")
		await checkpoint("CP02_B")   # both at tap alcove before the cinematic
	if not done("cs_alcove"):
		await both_ready("CH01_M02_CS01 alcove")
		await cinematic([
			{"id": "CH01_M02_CS01_SH04", "from": [Vector3(11.5, 1.6, -22.2), Vector3(8.9, 1.5, -24.6)], "to": [Vector3(11.2, 1.6, -22.0), Vector3(8.9, 1.5, -24.6)],
				"lines": [line_id(12), line_id(13)],
				"on_start": func():
					p1.place(xf(env["tap_p1"], 270.0))
					p2.place(xf(env["tap_p2"] + Vector3(0.4, 0, 0), 90.0))},
			{"id": "CH01_M02_CS01_SH05", "from": [Vector3(8.6, 1.62, -23.6), Vector3(10.2, 1.6, -24.0)], "to": [Vector3(8.7, 1.62, -23.7), Vector3(10.2, 1.6, -24.0)],
				"lines": [line_id(14), line_id(15), line_id(16)]},
			{"id": "CH01_M02_CS01_SH06", "from": [Vector3(9.9, 1.62, -23.5), Vector3(8.3, 1.62, -24.4)], "to": [Vector3(9.8, 1.62, -23.6), Vector3(8.3, 1.62, -24.4)],
				"lines": [line_id(17), line_id(18), line_id(19), line_id(20)]},
		], "At the tap Noah tells Adrian about Elena; they agree to keep asking in the laundry.")
		commit("cs_alcove")
	if not done("stance"):
		# optional skeptical stance; never a branching plot dependency, reconverges before the next objective
		var doubt: Interactable = items["m02_doubt"]
		doubt.enabled = true
		var t0 := now()
		while doubt.uses == 0 and now() - t0 < 8.0:
			await tick
		doubt.enabled = false
		if doubt.uses > 0:
			await say([23, 24])
		commit("stance")
	guide_to(0, env["gate_d2"], "Work-call gate")
	guide_to(1, env["gate_d2"], "Work-call gate")
	env["doors"]["D2"].set_open(true)
	await until(func(): return near(p1, env["gate_d2"], 2.5) and near(p2, env["gate_d2"], 2.5))
	clear_guide()
	commit("exit", CanonStates.exit_changes(2))
	finish()
