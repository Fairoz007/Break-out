extends Mission
## CH01_M01 NEW BLOOD — scene CH01_M01_SC01, cinematic CH01_M01_CS01 (docs/missions/CH01_MISSION_01.md).
## Parallel observation: P1 Adrian focuses the stamped badge from the holding bay while P2 Noah submits his
## property and reads the receipt; both acknowledge before the escort. Rusk escorts both to cells 13/14, each
## player inspects their sink and barred door, the pipe conversation plays, then the receipt handoff closes CS01.

var env: Dictionary
var cell: Dictionary


func build() -> void:
	env = EnvIntake.build(b)
	cell = EnvCellblock.build(b, false)
	var escorted := done("escort")
	npc("Rusk", "RUSK", Vector3(40.5, 0, -4.4) if escorted else env["rusk_desk"], 0.0 if escorted else 180.0)
	npc("Guard", "GUARD", env["guard_desk"], 200.0)
	for pos in [Vector3(10.8, 0, -10.6), Vector3(12.2, 0, -10.6)]:
		var inmate := npc("Inmate%d" % npcs.size(), "INMATE", pos, 180.0)
		inmate.act("Sitting_Idle", true)
	item("m01_tray", "Submit property at the tray", Vector3(19, 1.0, -9.2), 1, Interactable.Mode.PRESS, 1.3)
	item("m01_search", "Step onto the painted search mark", env["search_mark"] + Vector3(0, 0.5, 0), 1, Interactable.Mode.PRESS, 0.9)
	# Wrong interaction (CH01_MISSION_01.md "Wrong interaction waits with authored guard bark"): reaching back for the
	# surrendered tray during the search is refused; the guard redirects him and the mission waits.
	item("m01_tray_back", "Reach for your property tray", Vector3(19, 1.0, -9.2), 1, Interactable.Mode.PRESS, 1.3)
	items["m01_tray_back"].set_meta("wrong", true)
	items["m01_tray_back"].set_meta("once", false)
	item("m01_receipt", "Read the property receipt", Vector3(19, 1.0, -9.2), 1, Interactable.Mode.PRESS, 1.3)
	item("m01_badge", "Focus: the stamped badge on the guard desk", env["adrian_bars"] + Vector3(0, 1.0, 0), 0, Interactable.Mode.PRESS, 1.2)
	item("m01_sink13", "Inspect your sink", cell["cell13"]["sink"] + Vector3(0, 0.9, 0), 0)
	item("m01_door13", "Test the barred door", cell["cell13"]["door"] + Vector3(0, 1.0, 0), 0, Interactable.Mode.PRESS, 1.1)
	item("m01_sink14", "Inspect your sink", cell["cell14"]["sink"] + Vector3(0, 0.9, 0), 1)
	item("m01_door14", "Test the barred door", cell["cell14"]["door"] + Vector3(0, 1.0, 0), 1, Interactable.Mode.PRESS, 1.1)
	for id in items:
		items[id].enabled = false
	if escorted:
		env["doors"]["D3"].set_open(true, false)
		env["doors"]["holding"].set_open(true, false)
		cell["doors"]["C13"].set_open(true, false)
		cell["doors"]["C14"].set_open(true, false)
	else:
		cell["doors"]["C13"].set_open(true, false)
		cell["doors"]["C14"].set_open(true, false)


func spawn(_cp: String) -> Array:
	return [xf(env["adrian_hold"], 90.0), xf(env["noah_tray"], 0.0)]


func run() -> void:
	var rusk: Npc = npcs["Rusk"]
	var guard: Npc = npcs["Guard"]
	rusk.face(env["noah_tray"])
	if not done("intro"):
		await both_ready("CH01_M01_CS01 intro")
		await cinematic([
			{"id": "CH01_M01_CS01_SH01", "from": [Vector3(-3.0, 2.0, 1.0), Vector3(2.5, 1.5, -9.0)], "to": [Vector3(-2.0, 2.0, 1.0), Vector3(3.0, 1.5, -9.0)],
				"on_start": func():
					EnvIntake.arrive(env.get("bus_node"))
					AudioDirector.cue("gate_latch", null, -8.0)},
			{"id": "CH01_M01_CS01_SH02", "from": [Vector3(17.0, 1.6, -8.0), Vector3(19.4, 1.45, -10.3)], "to": [Vector3(17.3, 1.6, -7.9), Vector3(19.4, 1.45, -10.3)],
				"lines": [line_id(1), line_id(2), line_id(3), line_id(4)], "speakers": {line_id(1): rusk, line_id(3): rusk, line_id(2): p2, line_id(4): p2}},
		], "Intake: Rusk takes Noah's property; Adrian watches from the holding bay.")
		commit("intro")
	if not done("property"):
		objective(1)
		guide_to(1, Vector3(19, 0, -8.8), "Property tray")
		await say([5, 6])
		var t0 := now()
		items["m01_tray"].enabled = true
		while items["m01_tray"].uses == 0:
			await tick
			if now() - t0 > 20.0:
				bark(21, guard)   # intake idle after 20 s
		items["m01_tray"].enabled = false
		AudioDirector.cue("paper", p2)
		await both_ready("CH01_M01_CS01_SH03")
		await cinematic([{"id": "CH01_M01_CS01_SH03", "from": [Vector3(18.3, 1.75, -9.2), Vector3(19.0, 1.12, -9.95)], "to": [Vector3(18.4, 1.6, -9.3), Vector3(19.0, 1.12, -9.95)],
			"on_start": func(): rusk.act("Interact")}], "Rusk tags the photograph and returns it with receipt 42.")
		commit("property", {"inv:photo": "NOAH_HAND", "inv:property": "COUNTER_TRAY", "m01.receipt_number": 42})
		complete_objective(1)
		clear_guide(1)
	if not done("search"):
		guide_to(1, env["search_mark"], "Painted search mark")
		items["m01_search"].enabled = true
		items["m01_tray_back"].enabled = true
		var t1 := now()
		while items["m01_search"].uses == 0:
			await tick
			if items["m01_tray_back"].uses > 0:
				items["m01_tray_back"].uses = 0
				GameState.log_event("wrong_interaction", {"mission": 1, "item": "m01_tray_back"})
				guard.act("palm_up")
				bark(21, guard)   # "Step onto the painted mark. Both feet."
				t1 = now()
			if now() - t1 > 20.0:
				bark(21, guard)
		items["m01_search"].enabled = false
		items["m01_tray_back"].enabled = false
		clear_guide(1)
		p2.visual.act("search_hands_open")
		await say([7, 8, 9, 10, 11, 12], {9: rusk, 10: guard, 12: rusk})
		commit("search")
	if not done("observed"):
		objective(2)
		guide_to(0, env["adrian_bars"], "Holding grille — look at the guard desk")
		guide_to(1, Vector3(19, 0, -8.8), "Property tray — read the receipt")
		items["m01_badge"].enabled = not done("badge")
		items["m01_receipt"].enabled = not done("receipt")
		var t2 := now()
		while not (done("badge") and done("receipt")):
			await tick
			if items["m01_badge"].uses > 0 and not done("badge"):
				items["m01_badge"].enabled = false
				clear_guide(0)
				p1.visual.act("badge_look")
				await both_ready("CH01_M01_CS01_SH04")
				await cinematic([{"id": "CH01_M01_CS01_SH04", "from": [Vector3(17.5, 1.3, -10.9), Vector3(17.0, 0.82, -11.6)], "to": [Vector3(20.2, 1.65, -11.0), Vector3(22.0, 1.6, -12.6)]}],
					"Adrian finds the VANTAGE triangle stamped on the contractor badge.")
				commit("badge", {"know:adrian.saw_vantage_badge": true})
				complete_objective(2)
			if items["m01_receipt"].uses > 0 and not done("receipt"):
				items["m01_receipt"].enabled = false
				clear_guide(1)
				commit("receipt", {"know:noah.read_receipt_42": true})
			if not done("badge") and now() - t2 > 25.0:
				bark(22, p1)   # badge reminder
		# Both acknowledge their observation before the escort proceeds.
		await both_ready("acknowledge observations")
		await say([13, 14])
		commit("observed")
	if not done("escort"):
		objective(3)
		commit("photo_returned", {"inv:photo": "NOAH_SHIRT", "inv:property": "LOCKER42"})
		AudioDirector.cue("keys", rusk)
		env["doors"]["holding"].set_open(true)
		env["doors"]["D3"].set_open(true)
		guide_to(0, cell["cell13"]["door_out"], "Follow Rusk to the east landing")
		guide_to(1, cell["cell14"]["door_out"], "Follow Rusk to the east landing")
		await escort(rusk, [Vector3(19.5, 0, -7.0), Vector3(22.8, 0, -6.0), Vector3(26.5, 0, -6.0), Vector3(33.0, 0, -5.5), Vector3(39.0, 0, -4.6)])
		rusk.face(cell["cell14"]["door_out"])
		await until(func(): return both_near(cell["cell13"]["door_out"], cell["cell14"]["door_out"], 2.6))
		await say([15], {15: rusk})
		commit("escort")
		await checkpoint("CP01_B")   # both on the cell landing after observations, before the completion gate
	if not done("cells"):
		guide_to(0, cell["cell13"]["mark"], "Cell 13")
		guide_to(1, cell["cell14"]["mark"], "Cell 14")
		await until(func(): return near(p1, cell["cell13"]["mark"], 1.2) and near(p2, cell["cell14"]["mark"], 1.2))
		clear_guide()
		for id in ["m01_sink13", "m01_door13", "m01_sink14", "m01_door14"]:
			items[id].enabled = true
		await until(func(): return ["m01_sink13", "m01_door13", "m01_sink14", "m01_door14"].all(func(id): return items[id].uses > 0 or not items[id].enabled))
		complete_objective(3)
		commit("cells")
	if not done("pipe"):
		await say([16, 17, 18], {}, 20.0)
		commit("pipe")
	if not done("cs_final"):
		await both_ready("CH01_M01_CS01 final")
		await cinematic([
			{"id": "CH01_M01_CS01_SH05", "from": [Vector3(39.0, 1.7, -6.6), Vector3(39.0, 1.2, -2.0)], "to": [Vector3(39.4, 1.7, -6.4), Vector3(39.0, 1.2, -2.0)],
				"on_start": func():
					p1.place(xf(cell["cell13"]["mark"], 0.0))   # facing the bars and the landing
					# Keep Noah clear of the open door's thick hinge jamb in the two-cell shot.
					p2.place(xf(cell["cell14"]["mark"] + Vector3(0.45, 0, 0), 0.0))
					rusk.place(Vector3(40.5, 0, -4.0), 0.0)},
			{"id": "CH01_M01_CS01_SH06", "from": [Vector3(41.7, 1.6, -4.7), Vector3(40.95, 1.55, -2.0)], "to": [Vector3(39.6, 1.6, -4.9), Vector3(40.5, 1.6, -4.0)],
				"lines": [line_id(19), line_id(20)], "speakers": {line_id(19): p2, line_id(20): rusk},
				"on_start": func(): rusk.act("Interact")},
		], "Rusk hands Noah receipt 42 through the open door of cell 14; the doors lock.")
		AudioDirector.cue("cell_slam", rusk)
		cell["doors"]["C13"].set_open(false)
		cell["doors"]["C14"].set_open(false)
		await wait(1.0)
		commit("cs_final")
	commit("exit", CanonStates.exit_changes(1))
	finish()
