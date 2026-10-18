import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/mpfb_test.blend'))
for o in bpy.data.objects:
 print(o.name,o.type,list(o.dimensions),list(o.location))
 if o.type=='ARMATURE':
  print([(b.name,list(b.head_local),list(b.tail_local)) for b in o.data.bones])
