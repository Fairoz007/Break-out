#!/usr/bin/env bash
# Import new resources, enforce 3D texture settings (mipmaps, VRAM compression, normal-map flag) for
# Phase 03 material/prop textures, then import again so the settings take effect.
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
timeout 900 "$G" --headless --path . --import > /dev/null 2>&1
for f in assets/materials/phase03/*.import assets/props/phase03/*.png.import assets/props/phase03/*.jpg.import assets/characters/phase03/*.import assets/characters/phase04/*.import; do
  [ -f "$f" ] || continue
  sed -i 's/^mipmaps\/generate=false/mipmaps\/generate=true/; s/^compress\/mode=0/compress\/mode=2/; s/^detect_3d\/compress_to=1/detect_3d\/compress_to=0/' "$f"
  case "$f" in *nor*) sed -i 's/^compress\/normal_map=0/compress\/normal_map=1/' "$f";; esac
done
timeout 900 "$G" --headless --path . --import > /dev/null 2>&1
echo reimport-done
