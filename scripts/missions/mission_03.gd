extends Mission
## CH01_M03 THE WORKSHOP — scene CH01_M03_SC01, cinematic CH01_M03_CS01 (docs/missions/CH01_MISSION_03.md).
## Noah opens the doctor conversation (Rusk interrupts, then fetches the inspection lamp: the nonviolent guard
## distraction). Two-stage interlock: Adrian must keep the isolation lever held while Noah's hands are in the
## lint screen; releasing it withdraws Noah's hands before anything changes. Noah then holds the lamp while each
## player reads their half of the diagram on their own screen. Screen restored, shim palmed, CS01, shim handoff.

const NORTH_HALF := "MAINTENANCE DIAGRAM — your half (north route)\n\nService corridor E runs behind the east cell landing.\nRear service panels in cells 13 and 14 open into a common chase.\nChase exits by the C5 pier → service door → restricted corridor → manual gate C6 → maintenance spillway door."
const RELAY_HALF := "MAINTENANCE DIAGRAM — your half (relay key)\n\nTwo relays on one circuit, in different rooms.\nRelay 1 lifts the spillway grille.  Relay 2 feeds the lock.\nSelector positions A / B / C — grille feed marked B.\nApply the brake before energising."

var env: Dictionary
var lamp: Node3D


func build() -> void:
	env = EnvWorkshop.build(b)
	var rusk := npc("Rusk", "RUSK", env["office_door"], 0.0)
	var mara := npc("Mara", "MARA", env["mara"], 180.0)
	mara.act("Idle_FoldArms", true)
	for i in 3:
		var w := npc("Worker%d" % i, "INMATE", Vector3(20.5 + 3.0 * (i % 2), 0, -6.5 + (i / 2) * 0.0 - 1.9 * float(i == 2)), 0.0)
		w.act("Interact", true)
	lamp = b.model(EnvBuilder.PROP + "inspection_lamp.glb", env["office"] + Vector3(0.6, 0.79, -0.9), 0, "none", self)
	item("m03_ask", "Ask the doctor about the linen", env["blue_table"] + Vector3(0, 1, 0.6), 1, Interactable.Mode.PRESS, 1.4)
	item("m03_lever", "Hold the isolation lever down (keep holding)", env["lever"], 0, Interactable.Mode.HOLD_ACTIVE, 1.1)
	item("m03_screen", "Clear the lint screen (hold)", env["screen"], 1, Interactable.Mode.HOLD_COMPLETE, 1.1).hold_seconds = 2.5
	item("m03_lamp", "Hold the inspection lamp on the diagram (keep holding)", env["lamp_spot"], 1, Interactable.Mode.HOLD_ACTIVE, 1.1)
	item("m03_diagram", "Read the maintenance diagram", env["diagram"], 0, Interactable.Mode.PRESS, 1.1)
	item("m03_replace", "Replace the lint screen", env["screen"], 1, Interactable.Mode.PRESS, 1.1)
	item("m03_scrap", "Palm the discarded spring strip from the scrap bin", env["scrap"], 1, Interactable.Mode.PRESS, 1.1)
	item("m03_handoff", "Pass the shim to Adrian", env["exit"] + Vector3(0, 1, 0), 1, Interactable.Mode.PRESS, 2.2)
	for id in items:
		items[id].enabled = false
	if done("lamp_delivered"):
		lamp.position = env["lamp_spot"] + Vector3(0.2, -0.2, 0.3)
	if done("rusk_occupied"):
		rusk.place(env["rusk_mara"], 270.0)


func spawn(_cp: String) -> Array:
	return [xf(env["adrian_start"], 0.0), xf(env["noah_start"], 0.0)]


func run() -> void:
	var rusk: Npc = npcs["Rusk"]
	var mara: Npc = npcs["Mara"]
	if not done("intro"):
		await both_ready("CH01_M03_CS01 intro")
		await cinematic([{"id": "CH01_M03_CS01_SH01", "from": [Vector3(4.5, 1.8, -13.0), Vector3(16.0, 1.2, -9.0)], "to": [Vector3(5.5, 1.8, -13.2), Vector3(17.0, 1.2, -9.5)]}],
			"Laundry: protagonists at the press, Mara at the blue table, Rusk at the office.")
		commit("intro")
	if not done("ask"):
		objective(1)
		guide_to(1, env["blue_table"] + Vector3(0, 0, 0.8), "Mara's blue table")
		guide_to(0, env["adrian_start"], "Press operator mark")
		await use("m03_ask")
		items["m03_ask"].enabled = false
		clear_guide()
		await both_ready("CH01_M03_CS01_SH02")
		await cinematic([{"id": "CH01_M03_CS01_SH02", "from": [Vector3(20.2, 1.6, -11.6), Vector3(22.0, 1.45, -13.6)], "to": [Vector3(20.4, 1.6, -11.8), Vector3(22.2, 1.45, -13.6)],
			"lines": [line_id(1), line_id(2), line_id(3), line_id(4)], "speakers": {line_id(1): mara, line_id(3): mara, line_id(2): p2, line_id(4): rusk},
			"on_start": func():
				p2.place(xf(env["blue_table"] + Vector3(0, 0, 0.9), 180.0))
				mara.act("Interact")
				rusk.place(Vector3(24.5, 0, -14.8), 300.0)}], "Noah asks Mara why a doctor counts sheets; Rusk interrupts.")
		commit("ask")
	if not done("lamp_request"):
		guide_to(0, env["adrian_start"], "Press operator mark")
		guide_to(1, env["noah_start"], "Lint screen")
		rusk.go_to(env["rusk_aisle"])
		await until(func(): return not rusk.is_moving() and near(p1, env["adrian_start"], 2.5))
		await say([5, 6], {6: rusk})
		commit("lamp_request")
	# Rusk goes to the office for the lamp, brings it back, then Mara draws him to the linen inspection.
	if not done("rusk_occupied"):
		_rusk_errand(rusk, mara)
	if not done("isolated"):
		var lever: Interactable = items["m03_lever"]
		var screen: Interactable = items["m03_screen"]
		lever.enabled = true
		guide_to(0, env["lever"], "Isolation lever")
		guide_to(1, env["screen"], "Lint screen")
		var said_007 := false
		var last_progress := now()
		while not done("isolated"):
			await tick
			var held := lever.holder == 0
			screen.enabled = held
			screen.set_meta("ready_now", held and said_007)
			screen.status_text = "" if held else "Waiting for Adrian to lock out the press"
			lever.status_text = "" if held else "Noah needs the press isolated"
			if held and not said_007:
				await say([7])
				said_007 = true
			if not held and screen.holder == 1:
				# lever released early: Noah's hands withdraw first, progress resets, nothing else changes
				screen.force_release()
				p2.visual.stop_action()
				bark(24, p2)
				GameState.log_event("interlock_release", {"stage": "screen"})
			if screen.uses > 0:
				commit("screen_open")
				items["m03_screen"].enabled = false
				p2.visual.act("screen_clear")
				await say([8, 9])
				lever.enabled = false
				complete_objective(1)
				commit("isolated")
			if now() - last_progress > 30.0:
				bark(25, rusk)
				last_progress = now()
		clear_guide()
	# early lever release while Noah's hands are in the screen
	if not done("diagram"):
		objective(2)
		await until(func(): return done("lamp_delivered"))
		var lamp_it: Interactable = items["m03_lamp"]
		var diag: Interactable = items["m03_diagram"]
		lamp_it.enabled = true
		guide_to(1, env["lamp_spot"], "Inspection lamp")
		guide_to(0, env["diagram"], "Maintenance diagram")
		var p1_read := false
		var p2_read := false
		while not (p1_read and p2_read):
			await tick
			var lit := lamp_it.holder == 1
			diag.enabled = lit and not p1_read
			diag.set_meta("ready_now", lit)
			diag.status_text = "" if lit else "Too dark to read — Noah must hold the lamp"
			if lit and not p2_read:
				chapter.huds[1].show_info(RELAY_HALF)
				p2_read = true
				commit("p2_half", {"know:noah.relay_key_half": true})
			if diag.uses > 0 and not p1_read:
				chapter.huds[0].show_info(NORTH_HALF)
				p1_read = true
				commit("p1_half", {"know:adrian.north_route_half": true})
		await say([10, 11, 12, 13])
		chapter.huds[0].show_info("")
		chapter.huds[1].show_info("")
		lamp_it.enabled = false
		diag.enabled = false
		complete_objective(2)
		commit("diagram", {"know:route.diagram_memorized": true})
		clear_guide()
	if not done("restored"):
		objective(3)
		var rep: Interactable = items["m03_replace"]
		var scrap: Interactable = items["m03_scrap"]
		rep.enabled = not done("screen_replaced")
		scrap.enabled = not done("shim_palmed")
		guide_to(1, env["screen"], "Replace the screen, then the scrap bin")
		while not (done("screen_replaced") and done("shim_palmed")):
			await tick
			if rep.uses > 0 and not done("screen_replaced"):
				rep.enabled = false
				commit("screen_replaced", {"inv:diagram": "WORKSHOP_PANEL"})
				guide_to(1, env["scrap"], "Scrap bin")
				await say([14], {14: mara}, 20.0)
			if scrap.uses > 0 and not done("shim_palmed"):
				scrap.enabled = false
				p2.visual.act("shim_palm")
				commit("shim_palmed", {"inv:shim": "NOAH"})
		clear_guide()
		complete_objective(3)
		commit("restored")
		await until(func(): return done("rusk_occupied"))
		await checkpoint("CP03_B")   # after screen restored and shim collected, before the closing cinematic
	if not done("cs_final"):
		await both_ready("CH01_M03_CS01 final")
		await cinematic([
			{"id": "CH01_M03_CS01_SH03", "from": [Vector3(10.15, 1.42, -10.7), Vector3(10.0, 1.0, -9.42)], "to": [Vector3(11.75, 1.42, -10.7), Vector3(11.95, 1.02, -9.28)],
				"on_start": func():
					# hands clear: both step back from the rail, so the insert shows lever and replaced screen only
					p1.place(xf(env["adrian_start"] + Vector3(0, 0, -1.0), 0.0))
					p2.place(xf(env["noah_start"] + Vector3(0, 0, -0.8), 0.0))},
			# Keep the reaction camera outside Rusk's body. The sealed-envelope prop/contact
			# remains an explicit production blocker; a torso occlusion cannot stand in for it.
			{"id": "CH01_M03_CS01_SH04", "from": [Vector3(20.2, 1.55, -11.4), Vector3(23.2, 1.5, -13.0)], "to": [Vector3(20.6, 1.65, -11.4), Vector3(23.2, 1.6, -13.0)],
				"lines": [line_id(15), line_id(16)], "speakers": {line_id(15): rusk, line_id(16): mara},
				"on_start": func():
					rusk.act("Interact")
					# off-screen while we cut to Rusk: back on their authored marks for SH05/SH06
					p1.place(xf(env["adrian_start"], 0.0))
					p2.place(xf(env["noah_start"], 0.0))},
			{"id": "CH01_M03_CS01_SH05", "from": [Vector3(11.0, 1.6, -14.0), Vector3(11.0, 1.4, -10.4)], "to": [Vector3(11.1, 1.6, -13.6), Vector3(11.0, 1.4, -10.4)],
				"lines": [line_id(17), line_id(18)]},
			{"id": "CH01_M03_CS01_SH06", "from": [Vector3(10.6, 1.62, -11.3), Vector3(10.0, 1.6, -10.2)], "to": [Vector3(11.0, 1.62, -12.6), Vector3(11.0, 1.4, -10.4)],
				"lines": [line_id(19), line_id(20), line_id(21), line_id(22), line_id(23)],
				"on_start": func(): AudioDirector.cue("lever")},
		], "Rusk pockets a sealed clinic envelope; the pair agree to leave together.")
		AudioDirector.start_bed("belt", -18.0)   # belt restarts after both clear
		commit("cs_final")
	if not done("handoff"):
		guide_to(0, env["exit"], "Work exit")
		guide_to(1, env["exit"], "Work exit — pass the shim")
		var h: Interactable = items["m03_handoff"]
		await until(func(): return near(p1, env["exit"], 2.5))
		h.enabled = true
		h.status_text = "Adrian is at the exit"
		await use("m03_handoff")
		h.enabled = false
		commit("handoff", {"inv:shim": "ADRIAN"})
		clear_guide()
	commit("exit", CanonStates.exit_changes(3))
	finish()


func _rusk_errand(rusk: Npc, mara: Npc) -> void:
	rusk.go_to(env["office"])
	await until(func(): return not rusk.is_moving())
	await wait(1.5)
	lamp.reparent(rusk)
	lamp.position = Vector3(0.25, 0.9, -0.2)
	rusk.go_to(env["rusk_lamp"])
	await until(func(): return not rusk.is_moving())
	lamp.reparent(self)
	lamp.global_position = env["lamp_spot"] + Vector3(0.2, -0.2, 0.3)
	commit("lamp_delivered")
	await until(func(): return done("isolated"))
	# Mara's contaminated-linen inspection occupies the guard away from the aisle.
	rusk.go_to(env["rusk_mara"])
	await until(func(): return not rusk.is_moving())
	rusk.face(env["mara"])
	mara.act("Interact", true)
	commit("rusk_occupied")
