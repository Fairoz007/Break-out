#!/usr/bin/env bash
# Phase 05 character close-ups on the real CharacterVisual (pose_preview.tscn), Linux software renderer or GPU.
# usage: tools/phase05_char_closeups.sh <CHAR> <clip> <times> <outdir-relative-to-repo> [extra pose_preview args]
G="${GODOT:-/opt/tools/Godot_v4.7.2-stable_linux.x86_64}"
C=$1; CLIP=$2; T=$3; OUT=$4; shift 4
CAMS="full@0.2,1.1,-3.2>0,0.95,0;torso@0.15,1.35,-1.25>0,1.3,0;collar@0.08,1.55,-0.6>0,1.47,0;threeq@-0.9,1.45,-0.9>0,1.3,0;side@1.2,1.35,0>0,1.3,0;back@-0.3,1.4,1.4>0,1.3,0;rwrist@-0.55,1.0,-0.45>-0.25,0.95,0"
rm -rf "$OUT"; mkdir -p "$OUT"
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json xvfb-run -a -s "-screen 0 1600x1000x24" timeout 900 "$G" --path . --resolution 800x800 \
  res://tests/phase05/pose_preview.tscn -- --chars=$C --clip=$CLIP --times=$T --out=res://$OUT "--cams=$CAMS" "$@" > "$OUT.log" 2>&1
montage "$OUT"/*.png -tile 7x -geometry 400x400+2+2 -background '#111' "$OUT.jpg"
echo "$OUT.jpg"
