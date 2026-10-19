extends Node
## P03-PERF: real-time performance capture of actual gameplay. Instantiates scenes/main.tscn, which reads the same
## command-line user args (e.g. --autopilot --mission=3 --until=3 --save-slot=...), and samples engine monitors
## every 0.5 s at speed 1 (no time scaling). Writes --perf=<json> when the game quits.
##   godot --path . --resolution 1920x1080 res://tests/phase03/perf_capture.tscn -- --autopilot --mission=1 --until=1 --save-slot=p03_perf --perf=res://tests/phase03/evidence/perf_m01.json

var samples := []
var out := "res://tests/phase03/evidence/perf.json"
var _t := 0.0
var _frames := []
var _load_ms := 0.0
var _t0 := 0


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--perf="):
			out = a.trim_prefix("--perf=")
	process_mode = Node.PROCESS_MODE_ALWAYS
	_t0 = Time.get_ticks_usec()
	var main: Node = (load("res://scenes/main.tscn") as PackedScene).instantiate()
	get_tree().root.add_child.call_deferred(main)
	GameState.event_logged.connect(func(kind, e):
		if kind == "mission_loaded" and _load_ms == 0.0:
			_load_ms = (Time.get_ticks_usec() - _t0) / 1000.0)


func _process(delta: float) -> void:
	_frames.append(delta * 1000.0)
	_t += delta
	if _t < 0.5:
		return
	_t = 0.0
	samples.append({
		"fps": Performance.get_monitor(Performance.TIME_FPS),
		"process_ms": Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0,
		"physics_ms": Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0,
		"draw_calls": Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),
		"primitives": Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME),
		"objects": Performance.get_monitor(Performance.RENDER_TOTAL_OBJECTS_IN_FRAME),
		"video_mem_mb": Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED) / 1048576.0,
		"texture_mem_mb": Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED) / 1048576.0,
		"static_mem_mb": Performance.get_monitor(Performance.MEMORY_STATIC) / 1048576.0,
		"nodes": Performance.get_monitor(Performance.OBJECT_NODE_COUNT),
	})


func _exit_tree() -> void:
	var f := _frames.duplicate()
	f.sort()
	var n := f.size()
	var summary := {}
	if n > 0:
		var tot := 0.0
		for v in f:
			tot += v
		summary = {"frames": n, "mean_ms": tot / n, "fps_mean": n * 1000.0 / tot, "p50_ms": f[int(n * 0.5)], "p95_ms": f[int(n * 0.95)],
			"p99_ms": f[int(n * 0.99)], "max_ms": f[n - 1], "frames_over_16_7ms_pct": 100.0 * f.filter(func(x): return x > 16.7).size() / n}
	for k in ["draw_calls", "primitives", "video_mem_mb", "static_mem_mb", "process_ms"]:
		var vals := samples.map(func(s): return s[k])
		if not vals.is_empty():
			vals.sort()
			summary[k + "_p50"] = vals[vals.size() / 2]
			summary[k + "_max"] = vals[-1]
	var report := {"summary": summary, "first_mission_load_ms": _load_ms, "adapter": RenderingServer.get_video_adapter_name(),
		"api": RenderingServer.get_video_adapter_api_version(), "window": [DisplayServer.window_get_size().x, DisplayServer.window_get_size().y],
		"quality": Settings.graphics_quality, "cpu": OS.get_processor_name(), "cores": OS.get_processor_count(), "samples": samples}
	var file := FileAccess.open(out, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(report, "\t"))
	print("PERF ", JSON.stringify(summary))
