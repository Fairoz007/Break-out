# Asset validation report — Phase 01.5 (18 October 2026)

Engine: Godot `4.7.2.stable.steam.ed1daf0bf`, Windows, NVIDIA RTX 2060 (OpenGL 3.3 compatibility renderer for graphical checks). DCC: Blender 5.1.1. No gameplay was implemented.

PASS means only the named test passed. NOT TESTED is never PASS. Headless import success does not prove visual correctness, so every visual claim below comes from rendered images that were actually viewed.

| Test | Result | Evidence and limits |
|---|---|---|
| Project import (headless editor `--import`) | PASS: exit 0, stderr empty | `asset_library/manifests/phase15/godot_import_final3_{stdout,stderr}.log` |
| Resource loading, all Phase 01.5 runtime files | PASS: 908/908 jobs `VERIFIED` (146 scenes, 621 audio, 118 textures, 20 materials, font, style, particle material) | `asset_library/manifests/phase15/godot_validation.json`. Jobs include texture/bin dependencies, so this is not an asset count |
| Meshes / materials | PASS: 0 null active materials on any surface | same file, `geometry.null_materials` |
| Textures | PASS: all decode and import. **Import settings risk:** 58 material textures use lossless, no-mipmap import. Set them to VRAM-compressed with mipmaps before production | [audio/material audit](../qa/AUDIO_MATERIALS_AUDIT.md) |
| Character rigs (13) | PASS: skeletons valid (Rocketbox 80 joints, UBC 65), all meshes skinned, 0 null materials | `asset_library/manifests/phase15_characters_previews/godot/godot_character_report.json` |
| Animations | PASS: 37 clips per character, 17 looping. 14 poses × 2 views rendered in Godot and inspected; all 37 rendered in Blender | [animation report](../qa/ANIMATION_VALIDATION.md) |
| Character visual deformation | PASS (functional): no severe deformation in any sampled pose. Production likeness PARTIAL | [character report](../qa/CHARACTER_RIG_VALIDATION.md) |
| Audio | PASS (technical): 614 audited clips decode, 0 header failures, 0 full-scale runtime samples. 25 REJECTED (11 source clipping, 10 setting/combat mismatch, 3 near-duplicates, 1 other). 27 discovery clips added. **Listening NOT TESTED** | `asset_library/manifests/phase15/audio_materials_audit.json`, `docs/assets/PHASE15_DISCOVERY.md` |
| PBR materials (19) on geometry | PASS (render): all 19 on 1 m cubes in the inspection scene. Physical UV scale NOT TESTED. 3 metal-named sets lack metallic maps | `asset_library/manifests/phase15/inspection/zoneC_materials.png` |
| Architecture geometry / scale / pivots | PASS on file checks: 70/70 PARTIALLY_VERIFIED after repair cycle 1, 0 FAILED. Snapping verified visually in the inspection scene | [architecture report](../qa/PRISON_ARCHITECTURE_VALIDATION.md) |
| Missing references | PASS: every runtime path and licence file in assets.json exists; checksums recomputed (single files and per-path dicts) | `tools/phase15_finalize.py` aborts on any missing path, licence or mismatch |
| Collision / navigation / LOD / split-screen performance | NOT TESTED | No collision or nav resources authored |
| Audio listening / mix | NOT TESTED | — |

## Rerun every check (PowerShell, project root)

```powershell
$G = "C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe"
$B = "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
python -I tools/phase15_prepare.py                                   # regenerate Godot validation jobs from all fragments
& $G --headless --path . --editor --import                            # import
& $G --path . --rendering-method gl_compatibility --script tools/phase15_validate.gd          # load + render every resource
& $G --path . --rendering-method gl_compatibility --script tools/phase15_character_godot.gd   # character skeleton/clip renders
& $G --path . --rendering-method gl_compatibility --script tools/phase15_inspection_scene.gd  # inspection scene + screenshots
& $B -b --factory-startup --python tools/phase15_rocketbox_render.py  # Blender re-import renders (realistic cast)
& $B -b --factory-startup --python tools/phase15_ubc_render.py        # Blender re-import renders (proxy cast)
python -I tools/phase15_finalize.py                                  # merge manifest; verifies paths, licences, checksums
python -I tools/phase15_coverage.py; python -I tools/phase15_manifest_docs.py
python tools/audit_documentation.py
```

The graphical commands open an engine window briefly and need a real GPU. Earlier Phase 01 results (Poly Haven MD5, Kenney ZIP integrity, three-prop previews) remain valid and are kept in `asset_library/manifests/godot_resource_validation.json` and `download_checks.json`.

## Overall

| Readiness | Verdict |
|---|---|
| Functional asset readiness for core gameplay | PASS |
| Production asset readiness | NOT READY (see [blockers](../qa/BLOCKERS.md)) |
