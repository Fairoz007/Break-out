extends Node
## Player-facing options (REQ-UI-004, REQ-INPUT-003). Persisted to user://settings.cfg.

signal changed

const PATH := "user://settings.cfg"

var subtitle_scale := 1.0
var music_volume := 0.8
var voice_volume := 1.0
var sfx_volume := 0.9
var camera_sensitivity := [1.0, 1.0]
var invert_y := [false, false]
var hold_toggle := false
var reduced_flash := true
## 2 = high (SSIL, volumetric fog), 1 = medium (SSAO/SSIL only), 0 = low (SSAO only).
## Applied when an environment is built; --quality=<0..2> on the command line overrides it for tests.
var graphics_quality := 2
## "vertical" = side-by-side views (canonical default), "horizontal" = top/bottom. Applies when a chapter loads;
## --split=vertical|horizontal overrides it for tests.
var split_mode := "vertical"


func _ready() -> void:
	load_settings()
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--quality="):
			graphics_quality = clampi(int(a.get_slice("=", 1)), 0, 2)
		if a.begins_with("--split="):
			split_mode = "horizontal" if a.get_slice("=", 1) == "horizontal" else "vertical"
	_ensure_buses()
	apply()


## Phase 06 bus layout: Master <- Music, Dialogue (<- Radio), SFX (<- Ambience, UI). The three player sliders keep
## their meaning: Voice volume drives Dialogue (radio included), Effects volume drives SFX (ambience and UI included).
## Effects: Radio is band-limited and slightly driven; SFX carries a light per-scene reverb (AudioDirector.set_space);
## Dialogue stays dry for intelligibility and feeds a spectrum analyser that drives speaking characters' jaws.
const BUSES := [["Music", "Master"], ["Dialogue", "Master"], ["SFX", "Master"], ["Ambience", "SFX"], ["UI", "SFX"], ["Radio", "Dialogue"]]


func _ensure_buses() -> void:
	for pair in BUSES:
		if AudioServer.get_bus_index(pair[0]) == -1:
			AudioServer.add_bus()
			AudioServer.set_bus_name(AudioServer.bus_count - 1, pair[0])
	for pair in BUSES:
		AudioServer.set_bus_send(AudioServer.get_bus_index(pair[0]), pair[1])
	var radio := AudioServer.get_bus_index("Radio")
	if AudioServer.get_bus_effect_count(radio) == 0:
		var hp := AudioEffectHighPassFilter.new()
		hp.cutoff_hz = 320.0
		var lp := AudioEffectLowPassFilter.new()
		lp.cutoff_hz = 3400.0
		var dist := AudioEffectDistortion.new()
		dist.mode = AudioEffectDistortion.MODE_OVERDRIVE
		dist.drive = 0.18
		dist.post_gain = -3.0
		for e in [hp, lp, dist]:
			AudioServer.add_bus_effect(radio, e)
	var sfx := AudioServer.get_bus_index("SFX")
	if AudioServer.get_bus_effect_count(sfx) == 0:
		var rv := AudioEffectReverb.new()
		rv.wet = 0.0
		rv.dry = 1.0
		AudioServer.add_bus_effect(sfx, rv)
	var dlg := AudioServer.get_bus_index("Dialogue")
	if AudioServer.get_bus_effect_count(dlg) == 0:
		AudioServer.add_bus_effect(dlg, AudioEffectSpectrumAnalyzer.new())


func apply() -> void:
	for pair in [["Music", music_volume], ["Dialogue", voice_volume], ["SFX", sfx_volume]]:
		var i := AudioServer.get_bus_index(pair[0])
		if i >= 0:
			AudioServer.set_bus_volume_db(i, linear_to_db(max(pair[1], 0.0001)))
	changed.emit()


func set_value(key: String, value) -> void:
	set(key, value)
	apply()
	save_settings()


func save_settings() -> void:
	var cfg := ConfigFile.new()
	for key in ["subtitle_scale", "music_volume", "voice_volume", "sfx_volume", "camera_sensitivity", "invert_y", "hold_toggle", "reduced_flash", "graphics_quality", "split_mode"]:
		cfg.set_value("options", key, get(key))
	cfg.save(PATH)


func load_settings() -> void:
	var cfg := ConfigFile.new()
	if cfg.load(PATH) != OK:
		return
	for key in cfg.get_section_keys("options"):
		set(key, cfg.get_value("options", key))
