extends Mission
## CH01_M05 BEHIND THE WALLS — scene CH01_M05_SC01, cinematic CH01_M05_CS01 (docs/missions/CH01_MISSION_05.md).
## Adrian opens the manual gate with the shim. Routes split: P1 west catwalk to the A/B/C selector, P2 east floor
## to the mechanical brake, linked by wired handsets. Brake first, clear call, then B, then power. A wrong
## selector trips a safe breaker and resets the controls (no injury). The grille latches mechanically, both
## reunite, inspect the ledger (in place, never inventory) and the cached recording, and approach the door.

const POSITIONS := ["NEUTRAL", "A", "B", "C"]

var env: Dictionary
var selector := 0
var _handsets: Array = []


func build() -> void:
	env = EnvMaintenance.build(b)
	item("m05_gate", "Open the manual gate with the shim (hold)", env["gate"] + Vector3(0, 1, 0), 0, Interactable.Mode.HOLD_COMPLETE, 1.3).hold_seconds = 2.0
	items["m05_gate"].set_meta("act", "shim_work_standing")   # hand at the lock (Interact loop), facing the gate
	# Contact (Phase 05, D05-008): stand at the latch edge of the leaf (x3.2..4.8, z-6), face it, right wrist at
	# the lock with the shim in the fingers.
	items["m05_gate"].set_meta("stand", Vector3(4.3, 0, -5.42))
	items["m05_gate"].set_meta("face", Vector3(4.5, 1.05, -6.0))
	items["m05_gate"].set_meta("reach", Vector3(4.52, 1.08, -5.84))
	items["m05_gate"].set_meta("prop", EnvBuilder.PROP + "spring_shim.glb")
	items["m05_gate"].set_meta("prop_grip", CharacterVisual.SHIM_GRIP)
	items["m05_gate"].set_meta("frame_yaw", -50.0)   # swing the camera east of Adrian to see the hand at the latch
	item("m05_handset_p1", "Lift the maintenance handset", env["selector_stand"] + Vector3(-0.6, 1.0, -0.7), 0, Interactable.Mode.PRESS, 1.3)
	item("m05_handset_p2", "Lift the maintenance handset", env["brake_stand"] + Vector3(0.9, 1.0, 0.6), 1, Interactable.Mode.PRESS, 1.3)
	item("m05_brake", "Hold the mechanical brake (keep holding)", env["brake_stand"] + Vector3(0.6, 1.0, 0), 1, Interactable.Mode.HOLD_ACTIVE, 1.2)
	item("m05_selector", "Turn the selector", env["selector_stand"] + Vector3(-0.6, 1.0, 0), 0, Interactable.Mode.PRESS, 1.2)
	item("m05_power", "Energise", env["selector_stand"] + Vector3(-0.6, 1.0, -1.1), 0, Interactable.Mode.PRESS, 1.2)
	item("m05_ledger", "Inspect the transfer ledger", env["console"] + Vector3(-0.5, 1.0, 0), 0, Interactable.Mode.PRESS, 1.3)
	item("m05_recording", "Play the cached diagnostic recording", env["console"] + Vector3(0.6, 1.0, 0), 1, Interactable.Mode.PRESS, 1.3)
	items["m05_selector"].set_meta("once", false)
	items["m05_power"].set_meta("once", false)
	for id in items:
		items[id].enabled = false
	if done("gate_open"):
		env["doors"]["manual_gate"].set_open(true, false)
	if done("grille_up"):
		env["doors"]["grille"].set_open(true, false)


func hand_props() -> Array:
	return [EnvBuilder.PROP + "spring_shim.glb", EnvBuilder.PROP + "wired_handset.glb"]


func spawn(_cp: String) -> Array:
	return [xf(env["n0"] + Vector3(-0.6, 0, 0), 180.0), xf(env["n0"] + Vector3(0.6, 0, 0), 180.0)]


func _selector_label() -> String:
	return "Selector: %s" % POSITIONS[selector]


func run() -> void:
	if not done("gate_open"):
		guide_to(0, env["gate"], "Manual gate")
		guide_to(1, env["gate"] + Vector3(1.4, 0, 1.2), "Manual gate")
		await use("m05_gate")
		items["m05_gate"].enabled = false
		AudioDirector.cue("gate_latch", p1)
		env["doors"]["manual_gate"].set_open(true)
		commit("gate_open")
	if not done("intro"):
		guide_to(0, env["split"], "Route split")
		guide_to(1, env["split"] + Vector3(1.0, 0, 0), "Route split")
		await until(func(): return near(p1, env["split"], 2.5) and near(p2, env["split"], 2.5))
		clear_guide()
		await both_ready("CH01_M05_CS01 split")
		await cinematic([{"id": "CH01_M05_CS01_SH01", "from": [Vector3(9.4, 3.7, -7.0), Vector3(15.5, 1.0, -20.0)], "to": [Vector3(10.6, 3.9, -7.3), Vector3(16.5, 1.0, -20.5)]}],
			"West catwalk and east floor route are separated by the pump well.")
		commit("intro")
	if not done("relays"):
		objective(1)
		guide_to(0, env["selector_stand"], "Selector panel (west catwalk)")
		guide_to(1, env["brake_stand"], "Brake station (east floor)")
		items["m05_handset_p1"].enabled = true
		items["m05_handset_p2"].enabled = true
		while items["m05_handset_p1"].uses == 0 or items["m05_handset_p2"].uses == 0:
			await tick
			for id in ["m05_handset_p1", "m05_handset_p2"]:
				if items[id].uses > 0 and items[id].enabled:
					items[id].enabled = false
					AudioDirector.cue("handset", players[int(id.ends_with("p2"))])
					var holder: Player = players[int(id.ends_with("p2"))]
					holder.visual.act("handset", true)
					_handsets.append(holder.visual.attach_to_hand(EnvBuilder.PROP + "wired_handset.glb", true, holder.visual.palm_grip()))
		clear_guide()
		complete_objective(1)
		await both_ready("CH01_M05_CS01_SH02")
		# Open on Adrian's handset side: front-right three-quarter from where he actually stands (the old fixed camera
		# sat behind his right shoulder and saw only the back of the hand, QA 0101).
		var head := p1.global_position + Vector3(0, 1.6, 0)
		var fwd := -p1.global_transform.basis.z
		var right := p1.global_transform.basis.x
		await cinematic([{"id": "CH01_M05_CS01_SH02", "from": [head + right * 0.85 + fwd * 0.7 + Vector3(0, 0.05, 0), head + right * 0.08], "to": [Vector3(22.0, 1.6, -17.6), Vector3(23.6, 1.5, -18.6)],
			"lines": [line_id(1), line_id(2), line_id(3), line_id(4)]}], "Handset test across the pump hall.")
		commit("relays")
	if not done("grille_up"):
		objective(2)
		var brake: Interactable = items["m05_brake"]
		var sel: Interactable = items["m05_selector"]
		var pwr: Interactable = items["m05_power"]
		await say([5, 6], {}, 40.0)
		brake.enabled = true
		var clear_called := false
		var held_since := -1.0
		selector = 0
		while not done("grille_up"):
			await tick
			var held := brake.holder == 1
			brake.status_text = "" if held else "Brake first"
			if held and held_since < 0.0:
				held_since = now()
			if not held:
				held_since = -1.0
			if held and not clear_called and now() - held_since > 1.0:
				await say([7], {}, 40.0)
				clear_called = true
			sel.enabled = clear_called
			pwr.enabled = clear_called
			sel.status_text = _selector_label() + ("" if clear_called else " — wait for Noah's clear call")
			pwr.status_text = _selector_label()
			sel.set_meta("ready_now", clear_called and selector != 2)
			pwr.set_meta("ready_now", clear_called and selector == 2 and held)
			if sel.uses > 0:
				sel.uses = 0
				selector = (selector + 1) % POSITIONS.size()
				AudioDirector.cue("relay_click", p1, -8.0)
				GameState.log_event("selector", {"position": POSITIONS[selector]})
			if pwr.uses > 0:
				pwr.uses = 0
				if selector == 2 and held:
					sel.enabled = false
					pwr.enabled = false
					await say([8], {}, 40.0)
					AudioDirector.cue("grille", env["doors"]["grille"])
					env["doors"]["grille"].set_open(true)
					await until(func(): return not GameState.locks.has("door:LiftingGrille"))
					await say([9], {}, 40.0)
					brake.enabled = false   # the mechanical latch now holds the grille
					sel.enabled = false
					pwr.enabled = false
					complete_objective(2)
					commit("grille_up", {"m05.grille_latched": true})
				else:
					# wrong selector or no brake: safe breaker trip, controls reset, no injury
					AudioDirector.cue("breaker_trip", p1, -6.0)
					GameState.log_event("breaker_trip", {"position": POSITIONS[selector], "brake": held})
					selector = 0
					await say_conditional([23, 24])
	if not done("reunited"):
		objective(3)
		await say([10], {}, 40.0)
		for p in players:
			p.visual.stop_action()
		for h in _handsets:
			if is_instance_valid(h):
				h.get_parent().queue_free()
		_handsets.clear()
		guide_to(0, env["reunion"], "Meet by the pump")
		guide_to(1, env["reunion"] + Vector3(0.9, 0, 0.4), "Meet by the pump")
		await until(func(): return near(p1, env["reunion"], 2.2) and near(p2, env["reunion"], 2.4))
		await say([11, 12])
		clear_guide()
		complete_objective(3)
		commit("reunited")
		await checkpoint("CP05_B")   # at reunion after grille latched, before evidence inspection
	if not done("evidence"):
		objective(4)
		items["m05_ledger"].enabled = true
		items["m05_recording"].enabled = true
		guide_to(0, env["console"], "Pump console — ledger")
		guide_to(1, env["console"], "Pump console — recording")
		while items["m05_ledger"].uses == 0 or items["m05_recording"].uses == 0:
			await tick
			for id in ["m05_ledger", "m05_recording"]:
				if items[id].uses > 0 and items[id].enabled:
					items[id].enabled = false
		clear_guide()
		AudioDirector.cue("paper", p1)
		await both_ready("CH01_M05_CS01 console")
		await cinematic([
			{"id": "CH01_M05_CS01_SH03", "from": [Vector3(17.6, 1.35, -24.9), Vector3(17.6, 0.8, -25.5)], "to": [Vector3(17.8, 1.3, -25.0), Vector3(17.7, 0.8, -25.5)],
				"lines": [line_id(13), line_id(14)],
				"on_start": func():
					p1.place(xf(env["console"] + Vector3(-0.4, 0, 0.3), 180.0))
					p2.place(xf(env["console"] + Vector3(0.6, 0, 0.3), 180.0))
					p1.visual.act("ledger_inspect")},
			{"id": "CH01_M05_CS01_SH04", "from": [Vector3(16.8, 1.6, -23.4), Vector3(18.4, 1.3, -25.2)], "lines": [line_id(15)],
				"on_start": func():
					AudioDirector.cue("radio", null, -12.0)
					p2.visual.act("listen")},
			{"id": "CH01_M05_CS01_SH05", "from": [Vector3(17.4, 1.62, -23.6), Vector3(18.6, 1.6, -24.3)], "to": [Vector3(19.2, 1.62, -23.6), Vector3(17.6, 1.6, -24.3)],
				"lines": [line_id(16), line_id(17), line_id(18)]},
			{"id": "CH01_M05_CS01_SH06", "from": [Vector3(20.5, 1.7, -22.6), Vector3(18.0, 1.3, -24.6)], "to": [Vector3(21.5, 1.7, -22.8), Vector3(26.0, 1.3, -24.0)],
				"lines": [line_id(19), line_id(20), line_id(21)]},
		], "The ledger shows a boat every Thursday, no names, no destination; a damaged recording copied yesterday.")
		complete_objective(4)
		commit("evidence", {"know:noah.phrase_harbor_light": true, "know:both.thursday_transfer_schedule": true})
	objective(5)
	guide_to(0, env["handle_w"], "Spillway door")
	guide_to(1, env["handle_e"], "Spillway door")
	await until(func(): return near(p1, env["handle_w"], 1.8) and near(p2, env["handle_e"], 1.8))
	await say([22])
	complete_objective(5)
	clear_guide()
	commit("exit", CanonStates.exit_changes(5))
	finish()


## Retry lines (wrong selector / puzzle retry) replay each time the breaker trips: they are not story lines.
func say_conditional(nums: Array) -> void:
	for n in nums:
		chapter.dialogue.say(line_id(n), _default_speaker(line_id(n)))
		await until(func(): return not chapter.dialogue.busy())
