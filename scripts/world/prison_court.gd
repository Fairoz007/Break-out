extends RefCounted
## Original 28 x 15 m outdoor court. Metric layout from FIBA court dimensions;
## recreation environment, not a certified sports installation. Paint has no collision.

static func build(b: EnvBuilder) -> void:
	var surface := b.mat("asphalt_02", Color(0.85, 0.85, 0.85), 0.1)
	surface.roughness = 0.95
	# Thin visual overlay; the original continuous yard floor owns collision/navigation.
	var pavement := b.box(Vector3(20, 0.004, -14), Vector3(28, 0.008, 15), surface, b.root)
	pavement.collision_layer = 0
	var paint := b.flat(Color(0.76, 0.76, 0.68))
	paint.roughness = 1.0
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	# Outer bounds, halfway line, centre circle, keys, free throws and three-point arcs.
	for pair in [[Vector2(6,-6.5),Vector2(34,-6.5)], [Vector2(6,-21.5),Vector2(34,-21.5)], [Vector2(6,-6.5),Vector2(6,-21.5)], [Vector2(34,-6.5),Vector2(34,-21.5)], [Vector2(20,-6.5),Vector2(20,-21.5)]]:
		line(st, pair[0], pair[1])
	arc(st, Vector2(20,-14), 1.8, 0, TAU)
	for side in [-1.0,1.0]:
		var baseline: float = 20.0 + side*14.0
		var free_x: float = baseline-side*5.8
		for z in [-11.55,-16.45]:line(st,Vector2(baseline,z),Vector2(free_x,z))
		line(st,Vector2(free_x,-11.55),Vector2(free_x,-16.45))
		arc(st,Vector2(free_x,-14),1.8,-PI/2,PI/2 if side<0 else -3*PI/2)
		var basket_x: float = baseline-side*1.575
		var theta := asin(6.6/6.75)
		if side<0:
			arc(st,Vector2(basket_x,-14),6.75,-theta,theta)
		else:
			arc(st,Vector2(basket_x,-14),6.75,PI-theta,PI+theta)
		var arc_x: float = basket_x-side*sqrt(6.75*6.75-6.6*6.6)
		for z in [-7.4,-20.6]:line(st,Vector2(baseline,z),Vector2(arc_x,z))
		arc(st,Vector2(basket_x,-14),1.25,-PI/2,PI/2 if side<0 else -3*PI/2)
		hoop(b,baseline,side)
	var mesh := MeshInstance3D.new()
	st.generate_normals()
	mesh.mesh=st.commit()
	paint.cull_mode=BaseMaterial3D.CULL_DISABLED
	mesh.material_override=paint
	mesh.name="CourtPaint_50mm"
	b.root.add_child(mesh)

static func line(st: SurfaceTool, a: Vector2, c: Vector2, width:=0.05) -> void:
	var offset := (c-a).orthogonal().normalized()*width*0.5
	var p := [a-offset,a+offset,c+offset,c-offset]
	for i in [0,1,2,0,2,3]:
		st.set_uv(p[i]*0.1)
		st.add_vertex(Vector3(p[i].x,0.018,p[i].y))

static func arc(st: SurfaceTool, center: Vector2, radius: float, first: float, last: float) -> void:
	var count := maxi(32,int(absf(last-first)*48))
	for i in count:
		var a := lerpf(first,last,float(i)/count)
		var c := lerpf(first,last,float(i+1)/count)
		line(st,center+Vector2(cos(a),sin(a))*radius,center+Vector2(cos(c),sin(c))*radius)

static func tube(parent: Node3D, a: Vector3, c: Vector3, radius: float, material: Material, segments:=24, collector: SurfaceTool = null) -> void:
	var node:=MeshInstance3D.new()
	var mesh:=CylinderMesh.new()
	mesh.top_radius=radius;mesh.bottom_radius=radius;mesh.height=a.distance_to(c);mesh.radial_segments=segments
	node.mesh=mesh;node.material_override=material
	node.position=(a+c)*0.5
	var direction:=(c-a).normalized()
	node.quaternion=Quaternion(Vector3.UP,direction)
	if collector != null:
		collector.append_from(mesh, 0, node.transform)
		node.free()
	else:
		parent.add_child(node)

## Phase 04: vandal-resistant gooseneck unit built in Blender (tools/phase03_props_build.py hoop_gooseneck): bolted
## base plate on a concrete footing, perforated steel backboard, spring-mount double rim, steel chain net. Same
## metric layout as the earlier primitive hoop (board 1.2 m inside the baseline, rim 3.05 m); the post keeps its
## collider and the previous geometry is retained below as hoop_primitive() for reference.
static func hoop(b: EnvBuilder, baseline: float, side: float) -> void:
	var post_x := baseline + side * 1.5
	b.box(Vector3(post_x, 1.8, -14), Vector3(0.22, 3.6, 0.22), null, null, false)
	b.model("res://assets/props/phase03/hoop_gooseneck.glb", Vector3(post_x, 0, -14), 0.0 if side < 0 else 180.0, "none")


static func hoop_primitive(b: EnvBuilder, baseline: float, side: float) -> void:
	var steel:=b.flat(Color(0.22,0.25,0.26));steel.metallic=0.7;steel.roughness=0.45
	var white:=b.flat(Color(0.66,0.68,0.65));white.roughness=0.7
	var orange:=b.flat(Color(0.55,0.12,0.025));orange.metallic=0.4;orange.roughness=0.45
	var basket_x:=baseline-side*1.575
	var board_x:=baseline-side*1.2
	var post_x:=baseline+side*1.5
	b.box(Vector3(post_x,1.8,-14),Vector3(0.22,3.6,0.22),steel)
	tube(b.root,Vector3(post_x,3.5,-14),Vector3(board_x,3.5,-14),0.07,steel)
	tube(b.root,Vector3(post_x,2.3,-14),Vector3(board_x,3.4,-14),0.045,steel)
	b.box(Vector3(board_x,3.4,-14),Vector3(0.045,1.05,1.8),white,b.root)
	# Target rectangle on the playing face of the backboard.
	var face_x:=board_x-side*0.027
	for z in [-14.295,-13.705]:b.box(Vector3(face_x,3.275,z),Vector3(.005,.45,.035),steel,b.root)
	for y in [3.05,3.5]:b.box(Vector3(face_x,y,-14),Vector3(.005,.035,.59),steel,b.root)
	# Bolted rim mounting plate and projecting bracket join the ring to its board.
	b.box(Vector3(face_x-side*.012,3.10,-14),Vector3(.024,.18,.16),orange,b.root)
	b.box(Vector3(board_x-side*.12,3.05,-14),Vector3(.24,.045,.12),orange,b.root)
	for z in [-14.05,-13.95]:
		for y in [3.05,3.15]:
			tube(b.root,Vector3(face_x-side*.025,y,z),Vector3(face_x-side*.04,y,z),.009,steel,12)
	var ring:=MeshInstance3D.new()
	var torus:=TorusMesh.new()
	torus.inner_radius=.225;torus.outer_radius=.245;torus.rings=96;torus.ring_segments=12
	ring.mesh=torus;ring.material_override=orange;ring.position=Vector3(basket_x,3.05,-14);b.root.add_child(ring)
	# Woven net: each adjacent diagonal strand joins the next ring, with a tapered opening.
	var rope:=b.flat(Color(.60,.60,.54))
	var net_surface := SurfaceTool.new()
	net_surface.begin(Mesh.PRIMITIVE_TRIANGLES)
	for level in 4:
		var y0:=3.03-level*.10
		var y1:=y0-.10
		var r0:=lerpf(.225,.14,float(level)/4)
		var r1:=lerpf(.225,.14,float(level+1)/4)
		for i in 16:
			var angle:=TAU*i/16
			for diagonal in [-1,1]:
				var end_angle: float = angle+diagonal*PI/16
				tube(b.root,Vector3(basket_x+cos(angle)*r0,y0,-14+sin(angle)*r0),Vector3(basket_x+cos(end_angle)*r1,y1,-14+sin(end_angle)*r1),.003,rope,6,net_surface)
	var net_mesh := MeshInstance3D.new()
	net_mesh.name = "WovenBasketNet"
	net_mesh.mesh = net_surface.commit()
	net_mesh.material_override = rope
	b.root.add_child(net_mesh)
