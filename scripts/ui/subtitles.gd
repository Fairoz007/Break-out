class_name Subtitles
extends Control
## Speaker-labelled subtitles (REQ-DLG-002). Two lines of about 42 characters, reflowed at word boundaries.
## Text is never truncated: a line that needs more than two rows is shown as consecutive two-row pages.

const MAX_CHARS := 42
const MAX_ROWS := 2

var panel: PanelContainer
var label: RichTextLabel
var _pages: Array = []
var _page_time := 0.0
var _elapsed := 0.0
var current_id := ""


static func wrap_text(text: String, width := MAX_CHARS) -> Array:
	var rows := []
	var row := ""
	for word in text.split(" ", false):
		if row == "":
			row = word
		elif row.length() + 1 + word.length() <= width:
			row += " " + word
		else:
			rows.append(row)
			row = word
	if row != "":
		rows.append(row)
	return rows


static func paginate(text: String) -> Array:
	var rows := wrap_text(text)
	var pages := []
	for i in range(0, rows.size(), MAX_ROWS):
		pages.append("\n".join(rows.slice(i, i + MAX_ROWS)))
	return pages


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel = PanelContainer.new()
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0, 0, 0, 0.72)
	sb.set_corner_radius_all(6)
	sb.content_margin_left = 18
	sb.content_margin_right = 18
	sb.content_margin_top = 10
	sb.content_margin_bottom = 10
	panel.add_theme_stylebox_override("panel", sb)
	add_child(panel)
	label = RichTextLabel.new()
	label.bbcode_enabled = true
	label.fit_content = true
	label.scroll_active = false
	label.autowrap_mode = TextServer.AUTOWRAP_OFF
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(label)
	panel.visible = false
	Settings.changed.connect(_apply_size)
	_apply_size()


func _apply_size() -> void:
	var size_px := int(30 * Settings.subtitle_scale)
	label.add_theme_font_size_override("normal_font_size", size_px)
	label.add_theme_font_size_override("bold_font_size", size_px)


func show_line(line: Dictionary, duration: float) -> void:
	current_id = line["id"]
	var speaker: String = line["speaker"]
	var text: String = line["text"]
	_pages = paginate(text)
	_page_time = duration / _pages.size()
	_elapsed = 0.0
	label.set_meta("page", 0)
	_render(speaker, 0)
	panel.visible = true


func clear() -> void:
	panel.visible = false
	current_id = ""
	_pages = []


func _render(speaker: String, page: int) -> void:
	var colour: String = {"ADRIAN": "#9ec9ff", "NOAH": "#ffc27a", "RECORDING": "#c6c6c6"}.get(speaker, "#e6e6e6")
	label.text = "[b][color=%s]%s[/color][/b]\n%s" % [colour, speaker, _pages[page]]
	label.set_meta("speaker", speaker)
	await get_tree().process_frame
	panel.reset_size()
	panel.position = Vector2((size.x - panel.size.x) / 2.0, size.y - panel.size.y - 48.0)


func visible_text() -> String:
	return label.get_parsed_text() if panel.visible else ""


func _process(delta: float) -> void:
	if not panel.visible or _pages.size() < 2:
		return
	_elapsed += delta
	var page := mini(int(_elapsed / _page_time), _pages.size() - 1)
	if label.get_meta("page", 0) != page:
		label.set_meta("page", page)
		_render(label.get_meta("speaker"), page)
