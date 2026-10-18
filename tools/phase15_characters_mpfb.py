import bpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'asset_library/extracted_sources/phase15_characters/mpfb2-2.0.18/src'))
original_extension_path_user=bpy.utils.extension_path_user
bpy.utils.extension_path_user=lambda package: str(R/'asset_library/converted/phase15_characters/mpfb_user') if package=='mpfb' else original_extension_path_user(package)
import mpfb
mpfb.get_preference=lambda name: 'MPFB' if name=='mpfb_shelf_label' else None
mpfb.register()
from mpfb.services.humanservice import HumanService
from mpfb.services.targetservice import TargetService
from mpfb.entities.objectproperties import HumanObjectProperties
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
h=HumanService.create_human()
HumanObjectProperties.set_value('gender',1.0,entity_reference=h)
TargetService.reapply_macro_details(h)
HumanService.add_builtin_rig(h,'game_engine')
print('HUMAN_SUCCESS',h.name,len(h.data.vertices))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/mpfb_test.blend'))
