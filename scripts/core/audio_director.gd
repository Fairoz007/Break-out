extends Node
## Ambience beds and one-shot cues per scene (REQ-AUDIO-001). Only usable, licensed files from assets/audio.
## Every playback is logged so tests can confirm cues fired; listening quality remains a human check.

const A := "res://assets/audio/"
## Phase 05: ElevenLabs-generated effects and beds (tools/phase05_elevenlabs_sfx.py, sfx_manifest.json) replace the
## synthetic placeholders and mismatched stand-ins; footsteps by surface were missing entirely.
const E := "res://assets/audio/phase05_elevenlabs/"
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
}
const SCENE_AMBIENCE := {
	1: [["ocean", -18.0], ["ventilation", -20.0], ["bus_diesel", -14.0]],
	2: [["wind", -18.0], ["crowd", -22.0], ["ocean", -24.0]],
	3: [["washer", -14.0], ["belt", -20.0], ["fluorescent", -26.0]],
	4: [["ventilation", -22.0], ["cellblock_night", -20.0], ["radio", -34.0]],
	5: [["pump", -12.0], ["water", -20.0]],
	6: [["water", -22.0], ["ventilation", -24.0]],
}

var _beds := {}
var step_counts := {}   # surface -> footsteps played (verification reports)
var _cache := {}


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS


func stream(cue: String) -> AudioStream:
	if not _cache.has(cue):
		var s: AudioStream = load(CUES[cue])
		if s is AudioStreamOggVorbis:
			s = s.duplicate()
		_cache[cue] = s
	return _cache[cue]


func play_scene_ambience(mission_index: int) -> void:
	stop_all_beds()
	for pair in SCENE_AMBIENCE.get(mission_index, []):
		start_bed(pair[0], pair[1])


func start_bed(cue: String, volume_db := -14.0) -> void:
	if _beds.has(cue):
		return
	var p := AudioStreamPlayer.new()
	var s := stream(cue)
	if s is AudioStreamOggVorbis:
		s.loop = true
	elif s is AudioStreamWAV:
		s = s.duplicate()
		s.loop_mode = AudioStreamWAV.LOOP_FORWARD
		if s.loop_end == 0:
			s.loop_end = int(s.get_length() * s.mix_rate)
	p.stream = s
	p.volume_db = volume_db
	p.bus = "SFX"
	add_child(p)
	p.play()
	_beds[cue] = p
	GameState.log_event("audio_bed", {"cue": cue})


func stop_bed(cue: String) -> void:
	if _beds.has(cue):
		_beds[cue].queue_free()
		_beds.erase(cue)


func stop_all_beds() -> void:
	for cue in _beds.keys():
		stop_bed(cue)


## One-shot cue. With a world position and parent it plays positionally, otherwise as 2D.
func cue(name: String, at: Node3D = null, volume_db := -6.0) -> void:
	if not CUES.has(name):
		push_warning("Unknown audio cue " + name)
		return
	var s := stream(name)
	if at and at.is_inside_tree():
		var p := AudioStreamPlayer3D.new()
		p.stream = s
		p.volume_db = volume_db
		p.bus = "SFX"
		p.unit_size = 6.0
		at.add_child(p)
		p.finished.connect(p.queue_free)
		p.play()
	else:
		var p := AudioStreamPlayer.new()
		p.stream = s
		p.volume_db = volume_db
		p.bus = "SFX"
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
