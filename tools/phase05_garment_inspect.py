"""Blender: inspect Rocketbox rest GLBs for garment surgery (Phase 05, D05-001/002).
blender -b -P tools/phase05_garment_inspect.py -- <glb> [<glb> ...]"""
import bpy, sys, collections
args = sys.argv[sys.argv.index('--') + 1:]
for path in args:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    print('=====', path)
    for ob in bpy.data.objects:
        if ob.type != 'MESH':
            print(' obj', ob.name, ob.type); continue
        me = ob.data
        sk = len(me.shape_keys.key_blocks) if me.shape_keys else 0
        print(' mesh', ob.name, 'verts', len(me.vertices), 'faces', len(me.polygons), 'shape_keys', sk, 'mats', [m.name if m else None for m in me.materials], 'groups', len(ob.vertex_groups))
        gname = {g.index: g.name for g in ob.vertex_groups}
        dom = []
        for v in me.vertices:
            best = max(v.groups, key=lambda g: g.weight, default=None)
            dom.append(gname[best.group] if best else '-')
        hist = collections.defaultdict(collections.Counter)
        for p in me.polygons:
            c = collections.Counter(dom[i] for i in p.vertices)
            hist[p.material_index][c.most_common(1)[0][0].replace('Bip01 ', '')] += 1
        for mi, h in hist.items():
            print('   mat', mi, me.materials[mi].name if mi < len(me.materials) and me.materials[mi] else None, dict(h.most_common(40)))
        for m in me.materials:
            if m and m.use_nodes:
                imgs = [n.image.name + ' %dx%d' % tuple(n.image.size) for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image]
                print('   tex', m.name, imgs)
