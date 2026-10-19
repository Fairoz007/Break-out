import bpy, sys, json
from mathutils import Vector
R=sys.argv[sys.argv.index('--')+1]; out={}
for n in ['adrian_cross','noah_reyes','silas_bell','prisoner_npc','tomas_rusk','mara_sen']:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=f'{R}/assets/characters/phase15/rocketbox/{n}.glb')
    for o in bpy.data.objects:
        if o.type=='ARMATURE': o.data.pose_position='REST'
    bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get()
    lo=Vector((1e9,)*3); hi=Vector((-1e9,)*3)
    for o in bpy.data.objects:
        if o.type!='MESH' or o.name.startswith('Icosphere'): continue  # importer bone-shape helper, not in the GLB
        e=o.evaluated_get(dg); m=e.to_mesh()
        for v in m.vertices:
            w=e.matrix_world@v.co
            for i in range(3): lo[i]=min(lo[i],w[i]); hi[i]=max(hi[i],w[i])
        e.to_mesh_clear()
    # Blender Z-up -> glTF/Godot Y-up: (x, z, -y)
    size=[hi.x-lo.x, hi.z-lo.z, hi.y-lo.y]; c=(lo+hi)/2
    out[n]={'position':[lo.x, lo.z, -hi.y],'size_m':size}
print('BOUNDS'+json.dumps(out))
