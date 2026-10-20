extends Node
## Ambience beds and one-shot cues per scene (REQ-AUDIO-001). Only usable, licensed files from assets/audio.
## Every playback is logged so tests can confirm cues fired; listening quality remains a human check.

const A := "res://assets/audio/"
## Phase 05: ElevenLabs-generated effects and beds (tools/phase05_elevenlabs_sfx.py, sfx_manifest.json) replace the
## synthetic placeholders and mismatched stand-ins; footsteps by surface were missing entirely.
const E := "res://assets/audio/phase05_elevenlabs/"
const P6 := "res://assets/audio/phase06_elevenlabs/"   # Phase 06 batch (tools/phase06_elevenlabs_sfx.py)
const STEPS := {"concrete": 9, "metal": 9, "asphalt": 15, "tile": 9}
const CUES := {
	"bus_diesel": E + "bus_diesel.ogg",
	"ocean": A + "phase15_discovery/oga_vistula_waves_randommind/vistula_waves_short.ogg",
	"wind": A + "phase15_discovery/oga_wind_whoosh_loop_sketchman3/wind_woosh_loop.ogg",
	"ventilation": E + "ventilation.ogg",
	"fluorescent": E + "fluorescent.ogg",
	"crowd": E + "crowd.ogg",
	"washer": A + "phase15_discovery/oga_30_cc0_sfx_loops_rubberduck/machine_03.ogg",
	"belt": A + "phase15_discovery/oga_30_cc0_sfx_loops_rubberduck/machine_07.ogg",
	"pump": A + "phase15_discovery/oga_30_cc0_sfx_loops_rubberduck/pump_01.ogg",
	"water": A + "phase15/100-cc0-sfx-2/sfx100v2_loop_water_01.ogg",
	"alarm": E + "alarm.ogg",
	"radio": E + "radio.ogg",
	"gate_latch": A + "phase15/rpg-audio/metallatch.wav",
	"keys": A + "phase15/100-cc0-metal-and-wood-sfx/keys_01.ogg",
	"door_open": E + "door_open.ogg",
	"door_close": E + "door_close.ogg",
	"cell_slam": E + "cell_slam.ogg",
	"fence_rattle": A + "phase15/100-cc0-metal-and-wood-sfx/metal_sheet_03.ogg",
	"ball_bounce": E + "ball_bounce.ogg",
	"whistle": E + "whistle.ogg",
	"count_bell": E + "count_bell.ogg",
	"pipe_knock": E + "pipe_knock.ogg",
	"pipe_reply": E + "pipe_reply.ogg",
	"lever": E + "lever.ogg",
	"panel": E + "panel.ogg",
	"relay_click": E + "relay_click.ogg",
	"breaker_trip": E + "breaker_trip.ogg",
	"grille": E + "grille.ogg",
	"handset": E + "handset.ogg",
	"pa_chime": E + "pa_chime.ogg",
	"paper": A + "phase15/rpg-audio/bookflip1.wav",
	"cloth": A + "phase15/rpg-audio/cloth1.ogg",
	"cuffs": E + "cuffs.ogg",
	"footstep": A + "footstep_concrete_001.ogg",
	"ui_confirm": A + "phase15/interface-sounds/confirmation_001.ogg",
	"ui_back": A + "phase15/interface-sounds/back_001.ogg",
	"checkpoint": A + "phase15/interface-sounds/confirmation_002.ogg",
	"detect_warn": E + "detect_warn.ogg",
	"bus_doors": E + "bus_doors.ogg",
	"cellblock_night": E + "cellblock_night.ogg",
	"music_tension": P6 + "music_tension.ogg",
	"music_chase": P6 + "music_chase.ogg",
	"music_betrayal": P6 + "music_betrayal.ogg",
	"sting_capture": P6 + "sting_capture.ogg",
	"dryer": P6 + "dryer.ogg",
	"cart": P6 + "cart.ogg",
	"tools": P6 + "tools.ogg",
	"switch": P6 + "switch.ogg",
	"pipe_groan": P6 + "pipe_groan.ogg",
	"drips": P6 + "drips.ogg",
	"electric_hum": P6 + "electric_hum.ogg",
	"bus_arrive": P6 + "bus_arrive.ogg",
	"bus_engine_off": P6 + "bus_engine_off.ogg",
	"cellblock_day": P6 + "cellblock_day.ogg",
}
const SCENE_AMBIENCE := {
	1: [["ocean", -18.0], ["ventilation", -20.0], ["bus_diesel", -14.0], ["cellblock_day", -26.0]],
	2: [["wind", -18.0], ["crowd", -22.0], ["ocean", -24.0]],
	3: [["washer", -14.0], ["belt", -20.0], ["dryer", -22.0], ["fluorescent", -26.0]],
	4: [["ventilation", -22.0], ["cellblock_night", -20.0], ["radio", -34.0]],
	5: [["pump", -12.0], ["water", -20.0], ["drips", -20.0], ["electric_hum", -28.0]],
	6: [["water", -22.0], ["ventilation", -24.0]],
}

## Scene music bed (crossfaded on load; guards' alerts switch M04 to the chase bed until the next load).
const SCENE_MUSIC := {4: "music_tension"}
## Occasional positional one-shots that make a scene feel used: [cue, min s, max s, volume].
const SCENE_SPOTS := {3: [["cart", 18.0, 40.0, -14.0], ["tools", 12.0, 30.0, -16.0]], 5: [["pipe_groan", 20.0, 45.0, -12.0]]}
var _spot_timer: Timer
var _spots: Array = []
var _missing := {}
var _last_cue := {}
var _beds := {}
var step_counts := {}   # surface -> footsteps played (verification reports)
var _cache := {}


var _music: AudioStreamPlayer = null
var music_name := ""
var _duck_tween: Tween
## Per-scene acoustic space for the SFX bus reverb: [room_size, damping, wet]. M02 is the open yard (dry).
const SPACES := {1: [0.45, 0.6, 0.10], 2: [0.0, 0.5, 0.0], 3: [0.6, 0.4, 0.12], 4: [0.7, 0.5, 0.14], 5: [0.8, 0.35, 0.16], 6: [0.55, 0.5, 0.12]}
const UI_CUES := ["ui_confirm", "ui_back", "checkpoint"]


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS


func _bus_for(cue_name: String) -> String:
	if cue_name in UI_CUES:
		return "UI"
	if cue_name == "radio":
		return "Radio"
	return "SFX"


## Light reverb on the SFX bus matched to the scene; dialogue and music stay dry.
func set_space(mission_index: int) -> void:
	var bus := AudioServer.get_bus_index("SFX")
	if bus < 0 or AudioServer.get_bus_effect_count(bus) == 0:
		return
	var rv := AudioServer.get_bus_effect(bus, 0) as AudioEffectReverb
	var sp: Array = SPACES.get(mission_index, [0.5, 0.5, 0.1])
	rv.room_size = sp[0]
	rv.damping = sp[1]
	rv.wet = sp[2]
	rv.dry = 1.0


## Dialogue ducking: ambience -8 dB and music -5 dB while a voice take plays, eased in and out.
func duck(on: bool) -> void:
	if _duck_tween:
		_duck_tween.kill()
	_duck_tween = create_tween().set_parallel(true)
	for pair in [["Ambience", -8.0], ["Music", -5.0]]:
		var i := AudioServer.get_bus_index(pair[0])
		if i < 0:
			continue
		var from := AudioServer.get_bus_volume_db(i) if pair[0] == "Ambience" else 0.0
		_duck_tween.tween_method(func(v): AudioServer.set_bus_volume_db(i, v) if pair[0] == "Ambience" else _set_music_duck(v),
			from if pair[0] == "Ambience" else _music_duck, pair[1] if on else 0.0, 0.25 if on else 0.8)


var _music_duck := 0.0
func _set_music_duck(v: float) -> void:
	_music_duck = v
	if is_instance_valid(_music):
		_music.volume_db = _music_base + v


## Current speech level on the Dialogue bus, 0..1 (drives speaking characters' jaws); -1 when unavailable.
func speech_level() -> float:
	var bus := AudioServer.get_bus_index("Dialogue")
	if bus < 0 or AudioServer.get_bus_effect_count(bus) == 0:
		return -1.0
	var inst := AudioServer.get_bus_effect_instance(bus, 0) as AudioEffectSpectrumAnalyzerInstance
	if inst == null:
		return -1.0
	var m := inst.get_magnitude_for_frequency_range(120.0, 3200.0)
	return clampf((linear_to_db(maxf(m.length(), 1e-6)) + 52.0) / 34.0, 0.0, 1.0)


var _music_base := -10.0
## Music / tension bed with a crossfade (`name` is a CUES key, "" fades out).
func play_music(name: String, volume_db := -10.0, fade := 2.0) -> void:
	if name == music_name:
		return
	if is_instance_valid(_music):
		var old := _music
		var t := create_tween()
		t.tween_property(old, "volume_db", -60.0, fade)
		t.tween_callback(old.queue_free)
	_music = null
	music_name = name
	GameState.log_event("music", {"cue": name})
	if name == "" or not CUES.has(name) or stream(name) == null:
		return
	var s: AudioStream = stream(name).duplicate()
	if s is AudioStreamOggVorbis:
		s.loop = true
	_music = AudioStreamPlayer.new()
	_music.stream = s
	_music.bus = "Music"
	_music.volume_db = -60.0
	_music_base = volume_db
	add_child(_music)
	_music.play()
	create_tween().tween_property(_music, "volume_db", volume_db + _music_duck, fade)


func stream(cue: String) -> AudioStream:
	if not _cache.has(cue):
		if not ResourceLoader.exists(CUES[cue]):
			# a cue whose file is not generated yet is skipped (once logged), never an error
			if not _missing.has(cue):
				_missing[cue] = true
				GameState.log_event("audio_missing", {"cue": cue})
			return null
		var s: AudioStream = load(CUES[cue])
		if s is AudioStreamOggVorbis:
			s = s.duplicate()
		_cache[cue] = s
	return _cache[cue]


func play_scene_ambience(mission_index: int) -> void:
	stop_all_beds()
	set_space(mission_index)
	for pair in SCENE_AMBIENCE.get(mission_index, []):
		start_bed(pair[0], pair[1])
	play_music(SCENE_MUSIC.get(mission_index, ""))
	_spots = SCENE_SPOTS.get(mission_index, [])
	if _spot_timer == null:
		_spot_timer = Timer.new()
		_spot_timer.one_shot = true
		_spot_timer.process_mode = Node.PROCESS_MODE_PAUSABLE   # no scene one-shots under the pause menu
		_spot_timer.timeout.connect(_play_spot)
		add_child(_spot_timer)
	_spot_timer.stop()
	if not _spots.is_empty():
		_spot_timer.start(randf_range(8.0, 20.0))


func _play_spot() -> void:
	if _spots.is_empty():
		return
	var spot: Array = _spots.pick_random()
	cue(spot[0], null, spot[3])
	_spot_timer.start(randf_range(spot[1], spot[2]))


func start_bed(cue: String, volume_db := -14.0) -> void:
	if _beds.has(cue):
		return
	var src := stream(cue)
	if src == null:
		return
	var p := AudioStreamPlayer.new()
	var s := src.duplicate()   # the loop flag must not leak into one-shots of the same cue
	if s is AudioStreamOggVorbis:
		s.loop = true
	elif s is AudioStreamWAV:
		s = s.duplicate()
		s.loop_mode = AudioStreamWAV.LOOP_FORWARD
		if s.loop_end == 0:
			s.loop_end = int(s.get_length() * s.mix_rate)
	p.stream = s
	p.volume_db = -50.0
	p.bus = "Radio" if cue == "radio" else "Ambience"
	add_child(p)
	p.play()
	create_tween().tween_property(p, "volume_db", volume_db, 1.5)   # beds fade in, never pop
	_beds[cue] = p
	GameState.log_event("audio_bed", {"cue": cue})


func stop_bed(cue: String) -> void:
	if _beds.has(cue):
		_beds[cue].queue_free()
		_beds.erase(cue)


func stop_all_beds() -> void:
	_spots = []
	for cue in _beds.keys():
		stop_bed(cue)


## One-shot cue. With a world position and parent it plays positionally, otherwise as 2D.
func cue(name: String, at: Node3D = null, volume_db := -6.0) -> void:
	if not CUES.has(name):
		push_warning("Unknown audio cue " + name)
		return
	var s := stream(name)
	if s == null:
		return
	var now := Time.get_ticks_msec()
	if now - int(_last_cue.get(name, -1000)) < 120:
		return
	_last_cue[name] = now
	if at and at.is_inside_tree():
		var p := AudioStreamPlayer3D.new()
		p.stream = s
		p.volume_db = volume_db
		p.unit_size = 6.0
		p.bus = _bus_for(name)
		at.add_child(p)
		p.finished.connect(p.queue_free)
		p.play()
	else:
		var p := AudioStreamPlayer.new()
		p.stream = s
		p.volume_db = volume_db
		p.bus = _bus_for(name)
		add_child(p)
		p.finished.connect(p.queue_free)
		p.play()
	GameState.log_event("audio_cue", {"cue": name})


## One footstep on `surface` ("concrete", "metal", "asphalt", "tile"), positional at `at`, a random take each time.
func footstep(at: Node3D, surface: String, volume_db := -14.0) -> void:
	if not STEPS.has(surface):
		surface = "concrete"
	step_counts[surface] = int(step_counts.get(surface, 0)) + 1
	var path := "%sfootsteps/%s_%02d.ogg" % [E, surface, randi() % int(STEPS[surface])]
	var key := "step:" + path
	if not _cache.has(key):
		_cache[key] = load(path)
	if at == null or not at.is_inside_tree():
		return
	var p := AudioStreamPlayer3D.new()
	p.stream = _cache[key]
	p.volume_db = volume_db
	p.pitch_scale = randf_range(0.94, 1.06)
	p.unit_size = 3.0
	p.bus = "SFX"
	at.add_child(p)
	p.finished.connect(p.queue_free)
	p.play()
