extends Node
## Lists the animation clips each character actually has, and which Phase 04 animation requirement each covers.
const NEEDED := {"Idle": "Idle", "Walk": "Walk", "Run": "Jog_Fwd", "Sprint": "Sprint", "Crouch": "Crouch_Idle", "Crouch move": "Crouch_Fwd",
	"Jump": "Jump_Start", "Land": "Jump_Land", "Sit": "Sitting_Idle", "Stand": "Sitting_Exit", "Open door": "Interact", "Pick up": "PickUp_Table",
	"Push": "Push", "Pull": "Push", "Climb": "ClimbUp_1m", "Cooperative assistance": "Push", "Combat reaction": "Hit_Chest", "Cinematic gestures": "Idle_Talking"}
func _ready() -> void:
	var out := {}
	for key in ["ADRIAN", "NOAH", "GUARD", "INMATE"]:
		var v := CharacterVisual.new().setup(key)
		add_child(v)
		var clips := Array(v.anim.get_animation_list())
		out[key] = {"clips": clips, "coverage": {}}
		for need in NEEDED:
			out[key]["coverage"][need] = (NEEDED[need] + (" (played in reverse)" if need == "Pull" else "")) if clips.has(NEEDED[need]) else "MISSING"
	var f := FileAccess.open("res://tests/phase04/evidence/anim_inventory.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, "\t"))
	f.close()
	print("ANIM ", JSON.stringify(out["ADRIAN"]["clips"]))
	print("COVER ", JSON.stringify(out["ADRIAN"]["coverage"]))
	get_tree().quit()
