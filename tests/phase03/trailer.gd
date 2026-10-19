extends Node
## Chapter 1 cinematic trailer (~70 s). Renders real game environments, characters, animation and audio beds
## with scripted camera moves; title cards use canonical STORY.md facts and on-screen lines are verbatim from
## data/ch01/dialogue.json. Record with Godot Movie Maker (fixed 30 fps, PNG frames + WAV), then encode:
##   godot --path . --resolution 1920x1080 --fixed-fps 30 --write-movie build/trailer/frames/f.png res://tests/phase03/trailer.tscn
##   ffmpeg -framerate 30 -i build/trailer/frames/f%08d.png -i build/trailer/frames/f.wav -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac build/trailer/BreakoutNoWayBack_Ch1_Trailer.mp4

const FPS := 30.0
const BAR := 138                 # 2.39:1 letterbox inside 1920x1080

var root_vp: Viewport
var world: Node3D
var cam: Camera3D
var fade: ColorRect
var card: Label
var card_small: Label
var subtitle: Label
var actors := []                 # [{"node", "from", "to", "speed", "start", "act"}]
var lines := {}


func _ready() -> void:
	root_vp = get_tree().root
	root_vp.msaa_3d = Viewport.MSAA_2X
	root_vp.use_taa = true
	root_vp.positional_shadow_atlas_size = 4096
	for l in JSON.parse_string(FileAccess.get_file_as_string("res://data/ch01/dialogue.json"))["lines"]:
		lines[l["id"]] = l
	_build_overlay()
	_run.call_deferred()


func _build_overlay() -> void:
	var layer := CanvasLayer.new()
	layer.layer = 10
	add_child(layer)
	for top in [true, false]:
		var bar := ColorRect.new()
		bar.color = Color.BLACK
		bar.size = Vector2(1920, BAR)
		bar.position = Vector2(0, 0 if top else 1080 - BAR)
		layer.add_child(bar)
	fade = ColorRect.new()
	fade.color = Color.BLACK
	fade.size = Vector2(1920, 1080)
	layer.add_child(fade)
	card = _label(layer, 64, Vector2(0, 470))
	card_small = _label(layer, 30, Vector2(0, 560))
	subtitle = _label(layer, 34, Vector2(0, 1080 - BAR - 120))
	subtitle.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.9))
	subtitle.add_theme_constant_override("shadow_offset_x", 2)
	subtitle.add_theme_constant_override("shadow_offset_y", 2)


func _label(layer: CanvasLayer, size: int, pos: Vector2) -> Label:
	var l := Label.new()
	l.size = Vector2(1920, 100)
	l.position = pos
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", Color(0.93, 0.93, 0.9))
	layer.add_child(l)
	return l


# ------------------------------------------------------------------------------------------------ shots

func _shots() -> Array:
	return [
		{"card": "BLACKRIDGE PRISON", "small": "OCTOBER 2028", "dur": 4.0, "beds": [["wind", -14.0], ["ocean", -20.0]]},
		{"env": "yard", "dur": 5.5, "from": [Vector3(38.5, 9.6, -30.5), Vector3(20, 0, -14)], "to": [Vector3(33.5, 8.4, -31.2), Vector3(20, 0, -17)],
			"beds": [["wind", -12.0], ["crowd", -24.0]],
			"actors": [["INMATE", Vector3(25.5, 0, -4.6), Vector3(25.5, 0, -4.6)], ["SILAS", Vector3(24.6, 0, -5.4), Vector3(24.6, 0, -5.4)],
				["INMATE", Vector3(12, 0, -10), Vector3(20, 0, -16)], ["INMATE", Vector3(30, 0, -20), Vector3(26, 0, -12)]]},
		{"env": "intake", "dur": 6.5, "bus": true, "from": [Vector3(5.6, 0.55, -18.6), Vector3(2.4, 1.3, -12.0)], "to": [Vector3(5.3, 0.75, -18.2), Vector3(2.6, 1.4, -11.0)],
			"beds": [["bus_diesel", -6.0], ["wind", -18.0]], "end_cue": ["gate_latch", -4.0]},
		{"env": "intake", "dur": 5.0, "from": [Vector3(17.0, 1.6, -7.7), Vector3(19.4, 1.45, -10.3)], "to": [Vector3(17.5, 1.6, -7.8), Vector3(19.3, 1.45, -10.4)],
			"beds": [["ventilation", -18.0], ["fluorescent", -26.0]], "line": "CH01_M01_DLG001",
			"actors": [["RUSK", Vector3(19, 0, -11.0), Vector3(19, 0, -11.0), Vector3(19, 0, -8.6), "talk"], ["NOAH", Vector3(19, 0, -8.7), Vector3(19, 0, -8.7), Vector3(19, 0, -11)],
				["ADRIAN", Vector3(21.6, 0, -12.6), Vector3(21.6, 0, -12.6), Vector3(19, 0, -9)]]},
		{"env": "cellblock", "dur": 5.5, "from": [Vector3(29.5, 1.75, -5.6), Vector3(48, 1.3, -6)], "to": [Vector3(34.5, 1.7, -5.8), Vector3(52, 1.3, -6)],
			"beds": [["ventilation", -16.0]], "card": "ONE MAN WAS FRAMED.", "lower": true, "start_cue": ["cell_slam", -8.0],
			"actors": [["GUARD", Vector3(47, 0, -6.2), Vector3(40, 0, -6.2)], ["ADRIAN", Vector3(37.5, 0, -4.4), Vector3(37.5, 0, -4.4), Vector3(37.5, 0, -8)],
				["NOAH", Vector3(40.5, 0, -4.4), Vector3(40.5, 0, -4.4), Vector3(40.5, 0, -8)]]},
		{"env": "yard", "dur": 5.5, "fov": 30.0, "from": [Vector3(23.6, 1.62, -3.4), Vector3(24.3, 1.5, -6.2)], "to": [Vector3(23.8, 1.6, -3.7), Vector3(24.3, 1.5, -6.2)],
			"beds": [["wind", -16.0], ["crowd", -28.0]], "line": "CH01_M02_DLG014",
			"actors": [["NOAH", Vector3(24.3, 0, -6.2), Vector3(24.3, 0, -6.2), Vector3(23.6, 0, -3.4)], ["INMATE", Vector3(20, 0, -14), Vector3(26, 0, -18)]]},
		{"env": "workshop", "dur": 5.5, "from": [Vector3(6.5, 1.6, -11.6), Vector3(13, 1.2, -7.0)], "to": [Vector3(13.0, 1.6, -11.6), Vector3(19, 1.2, -7.0)],
			"beds": [["washer", -10.0], ["belt", -18.0]], "card": "ONE MAN LOST HIS SISTER.", "lower": true,
			"actors": [["ADRIAN", Vector3(8.0, 0, -10.4), Vector3(15.0, 0, -10.4)], ["NOAH", Vector3(7.2, 0, -11.0), Vector3(14.2, 0, -11.0)], ["MARA", Vector3(22, 0, -13.5), Vector3(22, 0, -13.5), Vector3(18, 0, -11)]]},
		{"env": "cellblock_night", "dur": 5.0, "from": [Vector3(29.5, 2.5, -6.0), Vector3(45, 1.3, -6.0)], "to": [Vector3(32.5, 2.2, -6.0), Vector3(46, 1.3, -6.0)],
			"beds": [["ventilation", -18.0], ["radio", -26.0]], "card": "TRUST IS THE ONLY WAY OUT.", "lower": true,
			"actors": [["GUARD", Vector3(50, 0, -6.4), Vector3(44, 0, -6.4)]]},
		{"env": "maintenance", "dur": 4.0, "from": [Vector3(22.6, 0.85, -21.9), Vector3(22.2, 1.25, -12.0)], "to": [Vector3(22.4, 0.95, -21.9), Vector3(22.2, 1.3, -12.0)],
			"beds": [["pump", -8.0], ["water", -16.0]], "actors": [["NOAH", Vector3(22.2, 0, -8.5), Vector3(22.2, 0, -17.4), Vector3.ZERO, "", 5.2]]},
		{"env": "maintenance", "dur": 4.0, "from": [Vector3(11.8, 3.6, -13.0), Vector3(9.2, 3.0, -18.5)], "to": [Vector3(11.4, 3.4, -14.5), Vector3(9.2, 3.0, -20.5)],
			"beds": [["pump", -10.0]], "fill": [Vector3(10.6, 4.0, -17.5), 2.2], "actors": [["ADRIAN", Vector3(9.2, 2.5, -15.0), Vector3(9.2, 2.5, -19.6)]]},
		{"env": "yard", "dur": 1.3, "from": [Vector3(10, 2.3, -10), Vector3(7.575, 3, -14)], "to": [Vector3(9.6, 2.4, -10.4), Vector3(7.575, 3, -14)], "beds": [["wind", -14.0]], "start_cue": ["ball_bounce", -4.0]},
		{"env": "workshop", "dur": 1.3, "from": [Vector3(12.5, 1.75, -10.6), Vector3(12.5, 1.0, -6.0)], "to": [Vector3(12.0, 1.7, -10.4), Vector3(12.5, 1.0, -6.0)], "beds": [["washer", -8.0]]},
		{"env": "maintenance", "dur": 1.3, "from": [Vector3(19.0, 1.8, -14.5), Vector3(16.0, 0.8, -14.5)], "to": [Vector3(18.6, 1.6, -15.2), Vector3(16.0, 0.8, -14.5)], "beds": [["pump", -6.0]], "start_cue": ["relay_click", -2.0]},
		{"env": "maintenance", "dur": 1.3, "from": [Vector3(22.4, 1.6, -15.5), Vector3(23.9, 1.0, -19.0)], "to": [Vector3(22.6, 1.5, -16.0), Vector3(23.9, 1.0, -19.0)], "beds": [["alarm", -16.0]]},
		{"env": "solitary", "dur": 6.5, "from": [Vector3(101.2, 1.65, 1.2), Vector3(101.0, 1.0, -2.2)], "to": [Vector3(101.1, 1.5, 0.35), Vector3(101.0, 1.0, -2.2)],
			"beds": [["water", -24.0], ["ventilation", -26.0]], "knocks": true,
			"actors": [["ADRIAN", Vector3(101.0, 0, -1.78), Vector3(101.0, 0, -1.78), Vector3(101.0, 0, 2.0), "solitary_sit"]]},
		{"card": "BREAKOUT: NO WAY BACK", "small": "CHAPTER 1  —  BLACKRIDGE        LOCAL TWO-PLAYER SPLIT-SCREEN CO-OP", "dur": 6.0, "start_cue": ["cell_slam", -2.0], "title": true},
	]


func _build(kind: String) -> Dictionary:
	if world:
		root_vp.remove_child(world)
		world.free()
	actors.clear()
	world = Node3D.new()
	root_vp.add_child(world)
	var b := EnvBuilder.new(world)
	var env := {}
	match kind:
		"intake": env = EnvIntake.build(b)
		"cellblock": env = EnvCellblock.build(b, false)
		"cellblock_night": env = EnvCellblock.build(b, true)
		"yard": env = EnvYard.build(b)
		"workshop": env = EnvWorkshop.build(b)
		"maintenance": env = EnvMaintenance.build(b)
		"solitary": env = EnvSolitary.build(b)
	cam = Camera3D.new()
	cam.near = 0.05
	cam.far = 250.0
	world.add_child(cam)
	cam.current = true
	return env


func _spawn(a: Array) -> void:
	var v := CharacterVisual.new().setup(a[0])
	world.add_child(v)
	var from: Vector3 = a[1]
	var to: Vector3 = a[2]
	v.position = from
	var face: Vector3 = a[3] if a.size() > 3 and a[3] != Vector3.ZERO else (to if to.distance_to(from) > 0.05 else from + Vector3(0, 0, 1))
	var d := face - from
	v.rotation.y = atan2(-d.x, -d.z)
	var action: String = a[4] if a.size() > 4 else ""
	if action != "":
		v.act(action, true)
	actors.append({"node": v, "from": from, "to": to, "speed": a[5] if a.size() > 5 else 1.35, "action": action})


func _ease(t: float) -> float:
	return t * t * (3.0 - 2.0 * t)


func _run() -> void:
	for s in _shots():
		await _play(s)
	AudioDirector.stop_all_beds()
	for i in int(FPS):
		await get_tree().process_frame
	get_tree().quit()


func _play(s: Dictionary) -> void:
	AudioDirector.stop_all_beds()
	for bed in s.get("beds", []):
		AudioDirector.start_bed(bed[0], bed[1])
	card.text = ""
	card_small.text = ""
	subtitle.text = ""
	var frames := int(s["dur"] * FPS)
	var env := {}
	if s.has("env"):
		env = _build(s["env"])
		for a in s.get("actors", []):
			_spawn(a)
		if s.has("fill"):                 # trailer-only key light for an otherwise unlit staging position
			var l := OmniLight3D.new()
			l.position = s["fill"][0]
			l.light_energy = s["fill"][1]
			l.omni_range = 7.0
			l.light_color = Color(0.85, 0.9, 1.0)
			world.add_child(l)
		if s.get("bus", false):
			EnvIntake.arrive(env.get("bus_node"), s["dur"] - 0.4, 6.0)
		cam.fov = s.get("fov", 42.0)
		cam.look_at_from_position(s["from"][0], s["from"][1])
		# warm-up under black so TAA, SSAO and volumetric fog history settle before the shot is seen
		fade.color.a = 1.0
		for i in 6:
			await get_tree().process_frame
	elif world:
		root_vp.remove_child(world)
		world.free()
		world = null
	if s.has("start_cue"):
		AudioDirector.cue(s["start_cue"][0], null, s["start_cue"][1])
	var knocks := [1.4, 1.9, 2.4, 3.9]
	for f in frames:
		var t := float(f) / frames
		var sec := f / FPS
		if cam and s.has("env"):
			var k := _ease(t)
			var p: Vector3 = (s["from"][0] as Vector3).lerp(s["to"][0], k)
			var q: Vector3 = (s["from"][1] as Vector3).lerp(s["to"][1], k)
			cam.look_at_from_position(p, q)
			for a in actors:
				var node: CharacterVisual = a["node"]
				var span: float = (a["from"] as Vector3).distance_to(a["to"])
				if span > 0.05:
					var travelled := minf(sec * a["speed"], span)
					var moving := travelled < span
					node.position = (a["from"] as Vector3).move_toward(a["to"], travelled)
					node.locomote(a["speed"] if moving else 0.0, false)
				elif a["action"] == "":
					node.locomote(0.0, false)
		# fades, cards and subtitles
		var fin := clampf(sec / 0.35, 0.0, 1.0)
		var fout := clampf((s["dur"] - sec) / 0.3, 0.0, 1.0)
		fade.color.a = 1.0 - minf(fin, fout) if s.has("env") else 1.0
		if s.has("card"):
			var ca := clampf((sec - 0.4) / 0.6, 0.0, 1.0) * clampf((s["dur"] - sec - 0.2) / 0.5, 0.0, 1.0)
			card.text = s["card"]
			card.position.y = 1080 - BAR - 220 if s.get("lower", false) else (430 if s.get("title", false) else 470)
			card.add_theme_font_size_override("font_size", 92 if s.get("title", false) else (44 if s.get("lower", false) else 64))
			card.modulate.a = ca
			card_small.text = s.get("small", "")
			card_small.position.y = 560 if not s.get("title", false) else 570
			card_small.modulate.a = clampf((sec - 1.0) / 0.6, 0.0, 1.0) * ca
		if s.has("line"):
			var l: Dictionary = lines[s["line"]]
			subtitle.text = "%s:  %s" % [String(l["speaker"]).capitalize(), l["text"]] if sec > 0.6 and sec < s["dur"] - 0.4 else ""
		if s.get("knocks", false):
			for i in knocks.size():
				if absf(sec - knocks[i]) < 0.5 / FPS:
					AudioDirector.cue("pipe_knock" if i < 3 else "pipe_reply", null, -4.0)
		await get_tree().process_frame
	if s.has("end_cue"):
		AudioDirector.cue(s["end_cue"][0], null, s["end_cue"][1])
