extends Node
## Application entry: main menu <-> Chapter 1. Command-line user arguments (after "--") support automated
## verification without changing gameplay: --autopilot drives both players through DeviceRouter's virtual
## devices, --mission=N starts at a mission's canonical entry state, --continue resumes the save.

var menu: Control
var chapter: ChapterRoot
var args := {}
var end_card: Control


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.trim_prefix("--").split("=", true, 1)
		args[kv[0]] = kv[1] if kv.size() > 1 else true
	_show_menu()
	if args.has("autopilot") or args.has("mission") or args.has("new"):
		_start(false)
	elif args.has("continue"):
		_start(true)


func _show_menu() -> void:
	if chapter:
		chapter.queue_free()
		chapter = null
	if end_card:
		end_card.queue_free()
		end_card = null
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	AudioDirector.stop_all_beds()
	AudioDirector.play_music("", -10.0, 0.5)
	menu = load("res://scripts/ui/main_menu.gd").new()
	menu.new_game.connect(func(): _start(false))
	menu.continue_game.connect(func(): _start(true))
	menu.quit_game.connect(func(): get_tree().quit())
	add_child(menu)


func _start(resume: bool) -> void:
	if menu:
		menu.queue_free()
		menu = null
	chapter = ChapterRoot.new()
	chapter.name = "Chapter01"
	add_child(chapter)
	chapter.quit_to_menu.connect(_show_menu)
	chapter.chapter_completed.connect(_on_chapter_complete)
	if args.has("diag"):
		add_child(load("res://tests/phase02/_diag.gd").new())
	if args.has("autopilot"):
		var ap = load("res://tests/phase02/autopilot.gd").new()
		ap.name = "Autopilot"
		ap.chapter = chapter
		ap.args = args
		add_child(ap)
	elif Devices.owners[0]["kind"] == Devices.Kind.KEYBOARD_MOUSE or Devices.owners[1]["kind"] == Devices.Kind.KEYBOARD_MOUSE:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	if resume and SaveService.can_continue():
		chapter.continue_game(SaveService.read())
	elif args.has("mission"):
		var snap := CanonStates.entry_snapshot(int(args["mission"]))
		chapter.continue_game(snap)
	else:
		chapter.start_new_game()


func _on_chapter_complete() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	end_card = Control.new()
	end_card.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	end_card.process_mode = Node.PROCESS_MODE_ALWAYS
	var bg := ColorRect.new()
	bg.color = Color.BLACK
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	end_card.add_child(bg)
	var l := Label.new()
	l.text = "CHAPTER 1 COMPLETE\n\nCH02 — NIGHT SHIFT"
	l.add_theme_font_size_override("font_size", 56)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	l.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	end_card.add_child(l)
	var b := Button.new()
	b.text = "Return to main menu"
	b.add_theme_font_size_override("font_size", 28)
	b.position = Vector2(760, 820)
	b.size = Vector2(400, 60)
	b.pressed.connect(_show_menu)
	end_card.add_child(b)
	add_child(end_card)
	b.grab_focus()
