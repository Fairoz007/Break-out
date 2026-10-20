extends "res://tests/phase03/visual_capture.gd"
## Uses the actual environment builders, autoloads and normal renderer.
func _ready() -> void:
	samples = [
		["tier_door_detail", "cellblock", Vector3(28.4, 4.65, -1.6), Vector3(29.5, 4.48, -0.07)],
		["dryer_front", "workshop", Vector3(7.4, 1.6, -6.1), Vector3(9.6, 1.0, -4.8)],
		["ironing_station", "workshop", Vector3(25.4, 1.4, -4.3), Vector3(24.0, 0.7, -2.8)],
		["ball_detail", "yard_ball", Vector3(22.1, 0.6, -10.9), Vector3(21.6, 0.24, -11.6)],
		["bus_chassis_detail", "intake", Vector3(5.0, 0.25, -8.0), Vector3(2.5, 0.45, -9.0)],
	]
	super._ready()

func _build(kind: String, b: EnvBuilder) -> void:
	if kind == "yard_ball":
		var env := EnvYard.build(b)
		# Same model/transform as Mission02.build; mission integration tested separately by autopilot.
		b.model("res://assets/props/phase04_realistic/basketball_recessed_channels.glb", env["ball"], 0, "none")
	else:
		super._build(kind, b)
