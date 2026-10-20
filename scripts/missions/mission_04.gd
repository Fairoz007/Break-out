extends Mission
## CH01_M04 LIGHTS OUT — scene CH01_M04_SC01, cinematic CH01_M04_CS01 (docs/missions/CH01_MISSION_04.md).
## Night. Noah watches the patrol from his bars and calls the turn; only then can Adrian work the shim into his
## rear fastener (he cannot see the landing while shimming). Adrian crawls into the chase and unlatches cell 14
## from the rear while braced; Noah crawls through and holds the hatch while Adrian clears it; both return their
## panels flush, cross the chase, wait out the guard's pipe investigation behind the pier and cross to the gate
## unseen. Full detection plays the detected line and always reloads CP04_A. Patrol ~45 s loop, deterministic.

var env: Dictionary
var guard_n: GuardAI
var detected := false
var _hide_x := 52.4


func build() -> void:
	env = EnvCellblock.build(b, true)
	guard_n = guard("Guard", env["c1"], 270.0, true)
	guard_n.view_range = 9.5
	guard_n.start_patrol([
		{"pos": env["c1"], "wait": 4.0, "look": Vector3(20, 1.5, -6)},
		{"pos": Vector3(41.0, 0, -6.4), "wait": 0.0},
		{"pos": env["c2"], "wait": 4.0, "look": Vector3(56, 1.2, -6.5)},
		{"pos": Vector3(41.0, 0, -7.0), "wait": 0.0}])
	guard_n.detection_enabled = done("count")
	guard_n.detected.connect(_on_detected)
	if not done("count"):
		npc("Rusk", "RUSK", Vector3(36.0, 0, -5.2), 90.0)
	item("m04_call", "Call the patrol turn", env["cell14"]["door"] + Vector3(0, 1, -0.2), 1, Interactable.Mode.PRESS, 1.2)
	item("m04_shim", "Work the shim into the rear fastener (hold)", env["cell13"]["panel"] + Vector3(0, 0.8, 0), 0, Interactable.Mode.HOLD_COMPLETE, 1.2).hold_seconds = 3.0
	item("m04_crawl13", "Crawl through the service opening", env["cell13"]["panel"] + Vector3(0, 0.6, 0), 0, Interactable.Mode.PRESS, 1.2)
	item("m04_unlatch14", "Unlatch cell 14's panel from the rear", env["cell14"]["panel_chase"] + Vector3(0, 0.6, 0), 0, Interactable.Mode.PRESS, 1.2)
	item("m04_brace", "Brace the hatch for Noah (keep holding)", env["cell14"]["panel_chase"] + Vector3(-0.7, 0.6, 0), 0, Interactable.Mode.HOLD_ACTIVE, 1.0)
	item("m04_crawl14", "Crawl through into the chase", env["cell14"]["panel"] + Vector3(0, 0.6, 0), 1, Interactable.Mode.PRESS, 1.2)
	item("m04_hold", "Hold the hatch while Adrian clears it (keep holding)", env["cell14"]["panel_chase"] + Vector3(0.5, 0.6, 0.45), 1, Interactable.Mode.HOLD_ACTIVE, 1.0)
	item("m04_flush13", "Return panel 13 flush", env["cell13"]["panel_chase"] + Vector3(0, 0.6, 0), 0, Interactable.Mode.PRESS, 1.2)
	item("m04_flush14", "Return panel 14 flush", env["cell14"]["panel_chase"] + Vector3(0, 0.6, 0), 1, Interactable.Mode.PRESS, 1.2)
	for id in items:
		items[id].enabled = false
	if done("panel13_open") and not done("flush"):
		_slide_panel(13, true, false)
	if done("panel14_open") and not done("flush"):
		_slide_panel(14, true, false)


func hand_props() -> Array:
	return [EnvBuilder.PROP + "spring_shim.glb"]


func spawn(cp: String) -> Array:
	return [xf(env["cell13"]["door"] + Vector3(0, 0, 0.5), 180.0), xf(env["cell14"]["door"] + Vector3(0, 0, 0.5), 180.0)]


func _slide_panel(cell_n: int, open: bool, animate := true, seconds := 0.6) -> void:
	for side in ["_in", "_out"]:
		var node: Node3D = env["panel%d%s" % [cell_n, side]]
		var target := Vector3(0.75 if open else 0.0, 0, 0)
		var base: Vector3 = node.get_meta("base", node.position)
		node.set_meta("base", base)
		if animate:
			create_tween().tween_property(node, "position", base + target, seconds).set_trans(Tween.TRANS_SINE)
		else:
			node.position = base + target
	AudioDirector.cue("panel", p1 if cell_n == 13 else p2, -10.0)


## Safe crossing window: the guard is walking away west, or holding at C1 facing west.
func guard_safe() -> bool:
	var gp := guard_n.global_position
	var heading_west := guard_n.patrol_index == 0 or guard_n.patrol_index == 3
	return (heading_west and gp.x < 46.0) or (guard_n.patrol_index == 1 and gp.x < 40.0)


func _hidden(p: Player) -> bool:
	var q := p.global_position
	var in_cell := q.z > -3.0 and q.z < 3.0 and q.x > 36.0 and q.x < 42.0
	var in_chase := q.z >= 2.9 and q.x > 35.6 and q.x < 54.4 or (q.x > 52.15 and q.x < 54.4 and q.z > -3.0)
	return in_cell or in_chase


func _physics_process(delta: float) -> void:
	super._physics_process(delta)
	if guard_n and guard_n.detection_enabled:
		for p in players:
			if _hidden(p):
				guard_n.detection[p.index] = 0.0
			chapter.huds[p.index].set_detection(guard_n.detection[p.index])


func _on_detected(_player: int) -> void:
	if detected or _hidden(players[_player]):
		return
	detected = true
	GameState.log_event("detected_fail", {"player": _player})
	guard_n.detection_enabled = false
	guard_n.stop()
	guard_n.face(players[_player].global_position)
	chapter.dialogue.clear()
	chapter.dialogue.say(line_id(20), guard_n)   # detected fail only
	for h in chapter.huds:
		h.flash_notice("DETECTED — returning to CP04_A", 4.0)
	await wait(3.0)
	GameState.flags["m04.retry_pending"] = true
	chapter.last_snapshot["flags"]["m04.retry_pending"] = true   # retry line plays after the reload
	chapter.reload_checkpoint()   # detection always reloads CP04_A


func run() -> void:
	if GameState.flag("m04.retry_pending"):
		GameState.flags.erase("m04.retry_pending")
		chapter.dialogue.say(line_id(21), p2)
	if not done("count"):
		var rusk: Npc = npcs["Rusk"]
		rusk.face(env["cell13"]["door"])
		await both_ready("CH01_M04_CS01 count")
		await cinematic([
			{"id": "CH01_M04_CS01_SH01", "from": [Vector3(38.0, 2.2, -8.6), Vector3(39.0, 1.6, -2.8)], "to": [Vector3(40.0, 2.2, -8.6), Vector3(39.0, 1.6, -2.8)],
				"lines": [line_id(1), line_id(2), line_id(3)], "speakers": {line_id(1): rusk},
				"on_start": func():
					# "Faces at the bars": both answer the count from their cell-front marks, facing the hall.
					p1.place(xf(env["cell13"]["mark"] + Vector3(0, 0, -0.6), 0.0))
					p2.place(xf(env["cell14"]["mark"] + Vector3(0, 0, -0.6), 0.0))
					AudioDirector.cue("pa_chime", null, -12.0)   # PA call for the count, then the bell
					AudioDirector.cue("count_bell", null, -8.0)
					rusk.act("count")},
			{"id": "CH01_M04_CS01_SH02", "from": [Vector3(32.0, 1.6, -8.4), Vector3(30.0, 1.5, -6.0)], "to": [Vector3(36.0, 1.6, -8.6), Vector3(34.0, 1.5, -6.4)],
				"lines": [line_id(4)], "speakers": {line_id(4): guard_n},
				"on_start": func(): rusk.go_to(Vector3(27.0, 0, -6.0))},
		], "Final count: both answer at the bars; the guard begins his night patrol.")
		if is_instance_valid(rusk):
			rusk.queue_free()
		guard_n.detection_enabled = true
		commit("count")
	if not done("panel13_open"):
		objective(1)
		guide_to(1, env["cell14"]["door"], "Watch the patrol from the bars")
		guide_to(0, env["cell13"]["panel"], "Rear service panel")
		await say([5, 6])
		var call: Interactable = items["m04_call"]
		var shim: Interactable = items["m04_shim"]
		call.enabled = true
		var called := false
		while not done("panel13_open"):
			await tick
			var safe := guard_safe()
			call.set_meta("ready_now", safe and not called)
			call.status_text = "His back is turning — call it" if safe else "He turns at the clock — wait"
			if call.uses > 0 and not called:
				call.uses = 0
				if safe:
					called = true
					call.enabled = false
					await say([7])
				else:
					AudioDirector.cue("ui_back", null, -12.0)   # too early: nothing happens
			shim.enabled = called and shim.uses == 0
			shim.status_text = "" if called else "Wait for Noah's call — you can't see the landing"
			if shim.uses > 0:
				shim.enabled = false
				p1.visual.act("shim_work")
				commit("panel13_open")   # the edge lift itself plays inside SH03
		await both_ready("CH01_M04_CS01_SH03")
		# Insert on the panel's east seam, low and along the wall from the west, so the hand and shim come toward the
		# lens with Adrian behind them. The shim in Adrian's fingers enters the gap under a cool spill from the
		# cell window (Phase 05, D05-006: the old frame was a dark wall and an empty hand, QA 0079).
		var shim_light := OmniLight3D.new()
		shim_light.light_color = Color(0.72, 0.8, 1.0)
		shim_light.light_energy = 1.6
		shim_light.omni_range = 1.8
		shim_light.shadow_enabled = true
		add_child(shim_light)
		shim_light.global_position = Vector3(38.0, 1.0, 2.15)
		var shim_prop: Node3D = null
		await cinematic([{"id": "CH01_M04_CS01_SH03", "from": [Vector3(37.05, 0.62, 2.35), Vector3(37.95, 0.47, 2.78)], "to": [Vector3(37.1, 0.6, 2.4), Vector3(38.0, 0.46, 2.78)],
			"on_start": func():
				# Adrian kneels at the panel's east edge working the shim, clear of the lens
				p1.place(xf(Vector3(38.35, 0, 2.3), 140.0))
				p1.visual.act("shim_work", true)
				shim_prop = p1.visual.attach_to_hand(EnvBuilder.PROP + "spring_shim.glb", true, CharacterVisual.SHIM_GRIP)
				p1.visual.reach("R", Vector3(37.95, 0.46, 2.74), Vector3(38.5, 0.3, 2.1), 0.5)
				_slide_panel(13, false, false)
				get_tree().create_timer(0.7).timeout.connect(func(): _slide_panel(13, true, true, 1.8))}],
			"The shim lifts the panel edge in cell 13.")
		shim_light.queue_free()
		p1.visual.release_reach("R")
		if is_instance_valid(shim_prop):
			shim_prop.get_parent().queue_free()
	if not done("adrian_in_chase"):
		await say([8, 9, 10])
		items["m04_crawl13"].enabled = true
		guide_to(0, env["cell13"]["panel"], "Crawl into the chase")
		await use("m04_crawl13")
		items["m04_crawl13"].enabled = false
		var done_flag := [false]
		p1.traverse([env["cell13"]["panel"] + Vector3(0, 0, 0.2), Vector3(37.5, 0, 3.0), env["cell13"]["panel_chase"]], 0.8, "crawl", func(): done_flag[0] = true)
		await until(func(): return done_flag[0])
		commit("adrian_in_chase")
	if not done("panel14_open"):
		guide_to(0, env["cell14"]["panel_chase"], "Cell 14's rear panel")
		await use("m04_unlatch14")
		items["m04_unlatch14"].enabled = false
		_slide_panel(14, true)
		await say([11])
		complete_objective(1)
		commit("panel14_open")
	if not done("noah_in_chase"):
		var brace: Interactable = items["m04_brace"]
		var crawl: Interactable = items["m04_crawl14"]
		brace.enabled = true
		guide_to(0, brace.global_position, "Brace the hatch")
		guide_to(1, env["cell14"]["panel"], "Crawl through")
		var crawling := [false, false]
		while not crawling[1]:
			await tick
			crawl.enabled = brace.holder == 0
			crawl.status_text = "" if brace.holder == 0 else "Wait for Adrian to brace the hatch"
			crawl.set_meta("ready_now", brace.holder == 0)
			if crawl.uses > 0 and not crawling[0]:
				crawling[0] = true
				crawl.enabled = false
				p2.traverse([env["cell14"]["panel"] + Vector3(0, 0, 0.2), Vector3(40.5, 0, 3.0), env["cell14"]["panel_chase"] + Vector3(0.5, 0, 0.45)], 0.8, "crawl", func(): crawling[1] = true)
		brace.enabled = false
		commit("noah_in_chase")
	if not done("hatch_cleared"):
		objective(2)
		var hold: Interactable = items["m04_hold"]
		hold.enabled = true
		guide_to(1, hold.global_position, "Hold the hatch")
		clear_guide(0)
		await until(func(): return hold.holder == 1)
		await say([12])
		guide_to(0, Vector3(44.0, 0, 3.9), "Move past Noah")
		await until(func(): return p1.global_position.x > 42.6)
		hold.enabled = false
		commit("hatch_cleared")
	if not done("flush"):
		# both physically clear of the hatch before either panel closes
		var f13: Interactable = items["m04_flush13"]
		var f14: Interactable = items["m04_flush14"]
		f13.enabled = true
		f14.enabled = true
		guide_to(0, env["cell13"]["panel_chase"], "Return panel 13 flush")
		guide_to(1, env["cell14"]["panel_chase"], "Return panel 14 flush")
		while f13.uses == 0 or f14.uses == 0:
			await tick
			if f13.uses > 0 and f13.enabled:
				f13.enabled = false
				_slide_panel(13, false)
			if f14.uses > 0 and f14.enabled:
				f14.enabled = false
				_slide_panel(14, false)
		commit("flush", {"m04.panels_flush": true})
	if not done("chase_crossed"):
		guide_to(0, env["chase_corner"], "End of the chase")
		guide_to(1, env["chase_corner"] + Vector3(-1.0, 0, 0), "End of the chase")
		await until(func(): return near(p1, env["chase_corner"], 2.0) and near(p2, env["chase_corner"], 2.4))
		complete_objective(2)
		commit("chase_crossed")
	if not done("investigation"):
		# an ambiguous pipe sound: the guard looks, then moves on (not a fail state)
		AudioDirector.cue("pipe_knock", guard_n, -14.0)
		guide_to(0, env["chase_exit"] + Vector3(0, 0, 1.6), "Stay in the chase")
		guide_to(1, env["chase_exit"] + Vector3(0, 0, 2.6), "Stay in the chase")
		await say([13], {13: guard_n}, 40.0)
		guard_n.investigate(Vector3(50.0, 1.0, -4.0), 6.0, false)
		await say([14, 15], {}, 40.0)
		commit("investigation")
	if not done("at_gate"):
		objective(3)
		var warned := false
		while not done("at_gate"):
			await tick
			var safe := guard_safe()
			var crossing := not _hidden(p1) or not _hidden(p2)
			for i in 2:
				if near(players[i], env["gate_c6"], 1.6):
					guide_to(i, env["gate_c6"], "Manual gate C6")
				elif safe or crossing:
					guide_to(i, env["gate_c6"] if not _hidden(players[i]) or safe else env["chase_exit"], "Manual gate C6 — move now" if safe else "Hold in cover")
				else:
					guide_to(i, env["chase_exit"] + Vector3(0, 0, 1.6 + i), "Hold in cover — guard approaching")
			# Patrol warning: the first unsafe approach while Adrian is at the chase exit or anyone is out of cover
			# (was also gated on guard x > 44, which no run reached while the pair waited: QA second review).
			if not safe and not warned and (crossing or near(p1, env["chase_exit"], 3.0)):
				warned = true
				bark(22, p1)   # patrol warning
			if near(p1, env["gate_c6"], 1.8) and near(p2, env["gate_c6"], 1.8):
				complete_objective(3)
				commit("at_gate", {"m04.cells_empty_undiscovered": true})
		clear_guide()
		guard_n.detection_enabled = false
		await checkpoint("CP04_B")   # both at the restricted gate after panels restored
	if not done("cs_gate"):
		await both_ready("CH01_M04_CS01 gate")
		await cinematic([
			{"id": "CH01_M04_CS01_SH04", "from": [Vector3(57.0, 1.3, -6.4), Vector3(62.5, 1.1, -6.6)], "to": [Vector3(57.6, 1.3, -6.5), Vector3(62.5, 1.1, -6.6)],
				"on_start": func():
					p1.place(xf(env["gate_c6"] + Vector3(-0.3, 0, 0.7), 270.0))
					p2.place(xf(env["gate_c6"] + Vector3(-0.3, 0, -0.7), 270.0))},
			# Whispered exchange at the gate: the two turn to each other; over-the-shoulder reverses (were backs of heads).
			{"id": "CH01_M04_CS01_SH05", "from": [Vector3(62.85, 1.66, -5.2), Vector3(62.5, 1.52, -7.2)], "lines": [line_id(16), line_id(17)],
				"on_start": func():
					p1.place(xf(env["gate_c6"] + Vector3(-0.3, 0, 0.7), 0.0))
					p2.place(xf(env["gate_c6"] + Vector3(-0.3, 0, -0.7), 180.0))},
			{"id": "CH01_M04_CS01_SH06", "from": [Vector3(62.15, 1.66, -7.8), Vector3(62.5, 1.55, -5.8)], "lines": [line_id(18), line_id(19)]},
		], "Both reach the manual maintenance gate unseen.")
		commit("cs_gate")
	commit("exit", CanonStates.exit_changes(4))
	finish()
