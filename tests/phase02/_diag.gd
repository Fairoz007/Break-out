extends Node
var t := 0.0
func _process(d):
	t += d
	if t > 3.0:
		var c = get_tree().root.get_node("Main/Chapter01")
		print("DIAG chapter size=", c.size, " views=", c.views.size, " svc0=", c.containers[0].size, " sv0=", c.viewports[0].size, " svc1=", c.containers[1].size, " sv1=", c.viewports[1].size, " hud0=", c.huds[0].size, " hud1=", c.huds[1].size, " hud_row=", c.hud_row.size)
		print("DIAG cam0 current=", c.cams[0].current, " cam pos=", c.cams[0].global_position, " world=", c.viewports[0].find_world_3d(), " ", c.viewports[1].find_world_3d())
		get_tree().quit()
