# Character rig validation — Phase 01.5

Date: 18 October 2026. Readiness: **BLOCKED**. Technical presence is PARTIALLY_VERIFIED; rendered character acceptance is FAILED.

Four licensed-source human derivatives were exported to `assets/characters/phase15/`: Adrian, Noah, guard and prisoner NPC. They use the MPFB game-engine skeleton with eyes and original simple shirt/trouser/boot/scalp geometry. They are development experiments, not accepted realistic protagonists or final uniforms. The variants share a base mesh and are not four unique scanned identities.

Sources: MPFB 2.0.18 archive preserved in `asset_library/original_downloads/phase15_characters/`; full asset CC0 and tool GPL terms copied into `asset_library/licenses/phase15_characters/`. MPFB's `LICENSE.md` explicitly separates GPL program logic from CC0 graphical assets and output. No GPL program logic is embedded in the GLBs. Quaternius CC0 source pages are preserved alongside those terms. Original archives have not been overwritten.

Evidence: saved authoring sources are `asset_library/converted/phase15_characters/prison_humanoid_source.blend` and `prison_humanoid_repaired.blend`. The latter is an unsuccessful repair experiment. The original `tools/phase15_characters_build.py` was found to contain NUL bytes after interruption; recovery used the saved Blender source, not that script. `tools/phase15_characters_repair.py` records the current attempted conversion.

Two repair cycles were rendered from actual exported Adrian GLB in Blender 5.1.1. First used world rest rotation compensation; second transferred local rotations after basis resets. Both failed visual acceptance: shoulder/arm collapse, severe anatomical distortion, and clothing disappearing into skin geometry. Skin weights were limited to four influences and normalized and mesh parents set to the armature, but these operations did not establish correct deformation. Neither counts as a successful skin test.

Final evidence images are under `asset_library/manifests/phase15_characters_previews/`, with logs `phase15_characters_repair.log` and `phase15_characters_render_repaired.log`. Earlier previews were overwritten by the final cycle; timestamps distinguish them from earlier reviewer observations.

| Criterion | Result |
|---|---|
| Four files exist and GLB parses | PARTIALLY_VERIFIED |
| Skeleton and skins present | PARTIALLY_VERIFIED |
| Eyes/clothing meshes and material definitions present | PARTIALLY_VERIFIED |
| Visible properly fitted prison/guard uniforms | FAILED |
| Healthy arm deformation and proportions in animation | FAILED |
| Distinct protagonist faces and production facial geometry | BLOCKED |
| PBR cinematic appearance / realistic skin textures | BLOCKED |
| Foot contacts and full animation sweep | BLOCKED |
| Final Godot import | Coordinator report; import alone does not clear above failures |

Required next action: obtain or author two properly clothed rigged realistic humans plus reusable uniformed guard/prisoner variants, or repair rest transforms and clothing bind offsets in these authoring sources. Re-render both protagonists at walk and crouch extremes before accepting. Current experimental GLBs must not be used as evidence that CHAR_ADRIAN/CHAR_NOAH/guard/prisoner bundles are resolved.

## Follow-up repair cycles 3–5

Cycles 3 and 4 tested computed world rest compensation with transformed parent heads, then explicit hierarchy-depth ordering. Both native Blender previews still show collapsed upper arms, so the failing runtime outputs were not replaced. Source-rest render `cycle3_rest_0.png` shows a healthy A-like pose. Hiding the base body in `cycle3_clothes_only.png` exposes the orange/gray clothing surfaces: they exist but are occluded by the body, rather than absent material definitions.

Cycle 5 authored an original 33-frame native-rig sine walk, independent of UAL. It also assigned uniform colors directly to covered body surfaces to diagnose occlusion. `cycle5_native_8.png` shows intact upper arms, an orange torso and gray legs, with a changed leg pose. This is a diagnostic proxy with stiff A-like arms and painted uniform boundaries, without convincing cloth thickness, folds, boots or skin textures. It is not an accepted realistic protagonist or full locomotion set. Source and experimental GLB are isolated under `asset_library/converted/phase15_characters/cycle5/`; they do not overwrite failed runtime hashes or establish mission readiness. See `tools/phase15_characters_cycle5.py` and `cycle5_export.py`. Five automated repair cycles are now exhausted; critical character readiness remains blocked.

Coordinator-requested prototype exports: `assets/characters/phase15/adrian_native_proxy.glb` and `noah_native_proxy.glb` (manifest IDs P15_PROXY_ADRIAN / P15_PROXY_NOAH) preserve the cycle 5 native walk only. They differ in shirt color, not face/body identity. They are PARTIALLY_VERIFIED diagnostic proxies, not accepted realistic protagonists or baseline locomotion. The two runtime exports were produced after the same underlying diagnostic GLB had been rendered; their Godot loading is recorded by the coordinator. The four failed retarget exports remain separately classified FAILED and are not replaced by these proxies.
