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


func _ready() -> void:
	load_settings()
	_ensure_buses()
	apply()


func _ensure_buses() -> void:
	for bus in ["Music", "Voice", "SFX"]:
		if AudioServer.get_bus_index(bus) == -1:
			AudioServer.add_bus()
			var i := AudioServer.bus_count - 1
			AudioServer.set_bus_name(i, bus)
			AudioServer.set_bus_send(i, "Master")


func apply() -> void:
	for pair in [["Music", music_volume], ["Voice", voice_volume], ["SFX", sfx_volume]]:
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
	for key in ["subtitle_scale", "music_volume", "voice_volume", "sfx_volume", "camera_sensitivity", "invert_y", "hold_toggle", "reduced_flash"]:
		cfg.set_value("options", key, get(key))
	cfg.save(PATH)


func load_settings() -> void:
	var cfg := ConfigFile.new()
	if cfg.load(PATH) != OK:
		return
	for key in cfg.get_section_keys("options"):
		set(key, cfg.get_value("options", key))
