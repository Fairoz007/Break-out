extends Node
## Ambience beds and one-shot cues per scene (REQ-AUDIO-001). Only usable, licensed files from assets/audio.
## Every playback is logged so tests can confirm cues fired; listening quality remains a human check.

const A := "res://assets/audio/"
const CUES := {
	"bus_diesel": A + "phase15/100-cc0-sfx-2/sfx100v2_loop_machine_02.ogg",
	"ocean": A + "phase15_discovery/oga_vistula_waves_randommind/vistula_waves_short.ogg",
	"wind": A + "phase15_discovery/oga_wind_whoosh_loop_sketchman3/wind_woosh_loop.ogg",
	"ventilation": A + "phase15_original/fan_loop.wav",
	"fluorescent": A + "phase15_original/fluorescent_buzz.wav",
	"crowd": A + "phase15_discovery/oga_crowd_shouting_starninjas/crowd_shouting.ogg",
	"washer": A + "phase15_discovery/oga_30_cc0_sfx_loops_rubberduck/machine_03.ogg",
	"belt": A + "phase15_discovery/oga_30_cc0_sfx_loops_rubberduck/machine_07.ogg",
	"pump": A + "phase15_discovery/oga_30_cc0_sfx_loops_rubberduck/pump_01.ogg",
	"water": A + "phase15/100-cc0-sfx-2/sfx100v2_loop_water_01.ogg",
	"alarm": A + "phase15_original/alarm_siren.wav",
	"radio": A + "phase15_discovery/oga_radio_noise_kresiek/radio_noise_loop.wav",
	"gate_latch": A + "phase15/rpg-audio/metallatch.wav",
	"keys": A + "phase15/100-cc0-metal-and-wood-sfx/keys_01.ogg",
	"door_open": A + "phase15/rpg-audio/dooropen_1.wav",
	"door_close": A + "phase15/rpg-audio/doorclose_2.ogg",
	"cell_slam": A + "phase15/100-cc0-metal-and-wood-sfx/metal_slam_01.wav",
	"fence_rattle": A + "phase15/100-cc0-metal-and-wood-sfx/metal_sheet_03.ogg",
	"ball_bounce": A + "impactMetal_light_002.ogg",
	"whistle": A + "phase15_original/alert_double.wav",
	"count_bell": A + "phase15_discovery/oga_bell_dings_pwl/bell_ding1.wav",
	"pipe_knock": A + "impactMetal_heavy_001.ogg",
	"pipe_reply": A + "impactMetal_medium_003.ogg",
	"lever": A + "phase15/rpg-audio/metalclick.ogg",
	"panel": A + "phase15/100-cc0-metal-and-wood-sfx/metal_open_01.wav",
	"relay_click": A + "phase15_original/relay_click.wav",
	"breaker_trip": A + "phase15_original/alert_double.wav",
	"grille": A + "phase15/100-cc0-metal-and-wood-sfx/metal_spring_01.ogg",
	"handset": A + "phase15/rpg-audio/metalclick.ogg",
	"pa_chime": A + "phase15_original/pa_chime.wav",
	"paper": A + "phase15/rpg-audio/bookflip1.wav",
	"cloth": A + "phase15/rpg-audio/cloth1.ogg",
	"cuffs": A + "phase15/100-cc0-metal-and-wood-sfx/keys_03.ogg",
	"footstep": A + "footstep_concrete_001.ogg",
	"ui_confirm": A + "phase15/interface-sounds/confirmation_001.ogg",
	"ui_back": A + "phase15/interface-sounds/back_001.ogg",
	"checkpoint": A + "phase15/interface-sounds/confirmation_002.ogg",
	"detect_warn": A + "phase15_original/alert_double.wav",
}
const SCENE_AMBIENCE := {
	1: [["ocean", -18.0], ["ventilation", -20.0], ["bus_diesel", -14.0]],
	2: [["wind", -16.0], ["crowd", -26.0], ["ocean", -24.0]],
	3: [["washer", -14.0], ["belt", -20.0], ["fluorescent", -26.0]],
	4: [["ventilation", -22.0], ["radio", -34.0]],
	5: [["pump", -12.0], ["water", -20.0]],
	6: [["water", -22.0], ["ventilation", -24.0]],
}

var _beds := {}
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
