#!/usr/bin/env bash
# Phase 05 character rebuild: Noah garments + hair, Adrian hair; 37-clip transfer; copy into the game; import.
set -e
B="${BLENDER:-/c/Program Files/Blender Foundation/Blender 5.1/blender.exe}"
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
D=asset_library/converted/acquisition_20261019/rocketbox_facial
E=tests/phase05/evidence
"$B" -b -P tools/phase05_noah_garment.py > $E/noah_garment_build.log 2>&1
"$B" -b -P tools/phase05_hair.py -- "$(pwd -W)/$D/rb_noah_reyes_p05_garment_rest.glb" "$(pwd -W)/$D/rb_noah_reyes_p05_rest.glb" noah > $E/hair_noah_build.log 2>&1
"$B" -b -P tools/phase05_hair.py -- "$(pwd -W)/$D/rb_adrian_cross_rest.glb" "$(pwd -W)/$D/rb_adrian_cross_p05_rest.glb" adrian > $E/hair_adrian_build.log 2>&1
python -I tools/acquisition_20261019_facial_animate.py rb_noah_reyes_p05 rb_adrian_cross_p05
mkdir -p assets/characters/phase05
cp $D/animated/rb_noah_reyes_p05.glb $D/animated/rb_adrian_cross_p05.glb assets/characters/phase05/
"$G" --headless --path . --import > $E/import_characters_p05.log 2>&1
grep -h "HAIR\|NOAH_GARMENT" $E/noah_garment_build.log $E/hair_noah_build.log $E/hair_adrian_build.log
