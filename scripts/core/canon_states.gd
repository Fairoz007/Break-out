class_name CanonStates
extends RefCounted
## Canonical continuity per mission (REQ-SAVE-004), taken from the "Exit state" sections of the mission docs.
## exit_changes(i) is what mission i commits on completion; entry_snapshot(i) composes all earlier exits so a
## mission can be started (and tested) on its own from its intended checkpoint CP0i_A.

const START_INVENTORY := {"photo": "NOAH_HAND", "property": "NOAH_HAND", "shim": "NONE", "diagram": "WORKSHOP_PANEL", "ledger": "PUMP_CONSOLE"}


static func exit_changes(i: int) -> Dictionary:
	match i:
		1: return {"inv:photo": "NOAH_SHIRT", "inv:property": "LOCKER42", "know:adrian.knows_noah_recognized_mark": true,
			"know:noah.knows_adrian_noticed": true, "m01.confined_east_landing": true}
		2: return {"know:pact.exchange_info_in_laundry": true, "know:noah.told_adrian_about_elena": true, "m02.silas_hostile": true}
		3: return {"inv:shim": "ADRIAN", "inv:diagram": "WORKSHOP_PANEL", "know:route.diagram_memorized": true,
			"know:plan.cell_panel_corridor_spillway": true}
		4: return {"m04.panels_flush": true, "m04.cells_empty_undiscovered": true}
		5: return {"inv:ledger": "PUMP_CONSOLE", "know:noah.phrase_harbor_light": true, "know:both.thursday_transfer_schedule": true,
			"know:noah.elena_unconfirmed": true}
		6: return {"inv:shim": "CONFISCATED", "inv:photo": "NOAH_SHIRT", "know:both.rusk_betrayal_known": true,
			"m06.separately_confined": true, "chapter1.complete": true}
	return {}


## Expected continuity values at the END of mission i, used by the automated continuity assertions.
static func expected_after(i: int) -> Dictionary:
	var inv := START_INVENTORY.duplicate()
	var know := {}
	for m in range(1, i + 1):
		for k in exit_changes(m):
			if k.begins_with("inv:"):
				inv[k.substr(4)] = exit_changes(m)[k]
			elif k.begins_with("know:"):
				know[k.substr(5)] = exit_changes(m)[k]
	return {"inventory": inv, "knowledge": know}


static func entry_snapshot(i: int) -> Dictionary:
	var flags := {}
	var inv := START_INVENTORY.duplicate()
	var know := {}
	var tx := []
	for m in range(1, i):
		var ch := exit_changes(m)
		for k in ch:
			if k.begins_with("inv:"):
				inv[k.substr(4)] = ch[k]
			elif k.begins_with("know:"):
				know[k.substr(5)] = ch[k]
			else:
				flags[k] = ch[k]
		tx.append("m%02d.complete" % m)
		tx.append("m%02d.exit" % m)
	return {"schema": GameState.SCHEMA, "chapter": "CH01", "mission": "CH01_M%02d" % i, "mission_index": i,
		"checkpoint": "CP%02d_A" % i, "entry": true, "players": [], "patrol": {}, "flags": flags, "inventory": inv,
		"knowledge": know, "consumed_dialogue": [], "transactions": tx, "completed_objectives": [], "objective": ""}
