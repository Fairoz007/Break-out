extends SceneTree
## Phase 06 audio performance probe (headless): load cost and memory of every bundled voice take and effect.
## Ogg Vorbis streams stay compressed in memory and decode on the mixer thread, so memory ~= file size.
## godot --headless --path . --script res://tests/phase06/audio_perf_probe.gd

func _init() -> void:
	var dirs := ["res://assets/audio/voice/ch01/", "res://assets/audio/phase05_elevenlabs/", "res://assets/audio/phase05_elevenlabs/footsteps/", "res://assets/audio/phase06_elevenlabs/"]
	var report := {}
	var mem0 := OS.get_static_memory_usage()
	var held: Array = []
	for d in dirs:
		var da := DirAccess.open(d)
		if da == null:
			continue
		var n := 0
		var ms := 0.0
		var worst := 0.0
		var secs := 0.0
		for f in da.get_files():
			if not f.ends_with(".ogg"):
				continue
			var t0 := Time.get_ticks_usec()
			var s: AudioStream = load(d + f)
			var dt := (Time.get_ticks_usec() - t0) / 1000.0
			held.append(s)
			n += 1
			ms += dt
			worst = maxf(worst, dt)
			secs += s.get_length()
		report[d] = {"files": n, "audio_seconds": snappedf(secs, 0.1), "load_ms_total": snappedf(ms, 0.01), "load_ms_mean": snappedf(ms / maxf(n, 1), 0.001), "load_ms_max": snappedf(worst, 0.01)}
	report["static_memory_delta_mb_all_loaded"] = snappedf((OS.get_static_memory_usage() - mem0) / 1048576.0, 0.01)
	report["stream_class"] = held[0].get_class() if not held.is_empty() else ""
	var f := FileAccess.open("res://tests/phase06/evidence/audio_perf.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, "\t"))
	print("AUDIO PERF ", JSON.stringify(report))
	quit()
