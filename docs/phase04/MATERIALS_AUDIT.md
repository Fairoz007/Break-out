# Phase 04 materials audit — 2026-10-20

Final integration note: after the initial read-only review below, the court's asphalt repeat was changed from
0.1 to 0.5 repetitions/metre (approximately 2 m tiles). Fresh `realistic_after/court_ground.png` was independently
reviewed after that change; aggregate scale improved, repeated crack patterns remain. The earlier 10 m finding
below describes the pre-fix iteration. New bed uses recorded Fabric030 CC0 maps downsampled to 1K; Blender
source is preserved outside runtime assets at `asset_library/original_created/phase04/prison_bunk.blend`.

Scope: read-only audit of actual runtime material source and fresh realistic_after captures. No material edits in this audit. Overall: usable PBR inputs present; cinematic material completion remains INCOMPLETE.

## Sources and measured runtime files

EnvBuilder.mat prefers phase025 material resources through SURFACE_UPGRADES, then acquisition 2K, then phase15. These referenced resources bind separate albedo, OpenGL normal, roughness and AO maps. Concrete/asphalt metallic=0 is appropriate. EnvBuilder enables world triplanar mapping, anisotropic mip filtering, attenuated normals0.25, avoiding stretched UVs on large generated surfaces.

| Actual runtime surface | Source / license | Maps / dimensions observed |
|---|---|---|
| Yard ground, concrete_floor_worn_001 alias | https://polyhaven.com/a/brushed_concrete ; CC0, bulk inventory | diffuse measured2048x2048; resource also references2K normal/roughness/AO |
| Court | https://polyhaven.com/a/asphalt_02 ; CC0, bulk inventory | resource references2K diffuse/normal/roughness/AO; scale0.1 repetitions/metre |
| Yard precast walls | https://polyhaven.com/a/concrete_wall_008 ; CC0, bulk inventory | phase03 diffuse measured2048x2048; surface() binds normal/roughness; scale0.2 repetitions/metre |
| Sealed interior floors | garage_floor per EnvBuilder code comment, https://polyhaven.com/a/garage_floor ; CC0 bulk inventory | phase03 floor_sealed diffuse/normal/roughness all measured2048x2048; scale0.22 workshop,0.25 maintenance |
| Painted interior wall and workshop clean floor | phase03 paint_diff.jpg, code describes copied CC0 painted-plaster source | diffuse2048x2048; micro roughness/normal plus block normal2048x2048; exact copied source identity needs hash reconciliation, so not provenance-VERIFIED from filename alone |
| Linen stacks | https://ambientcg.com/view?id=Fabric030 ; acquisition manifest CC0 | Color2048x2048 measured; resource also binds NormalGL/Roughness/AO2K; world triplanar scale2.0 |
| Reused detailed industrial dryer | karakocyunus Sketchfab CC BY4.0, see architecture provenance | embedded/extracted color2048x2048 measured; source is largely baked color detail, not a fully supplied independent skin/metal roughness-normal set |

Dimensions measured directly with System.Drawing.Image, not inferred solely from names. Bulk inventory source/licenses were read locally. Runtime VRAM compression/residency and source-to-copied-phase03 hash matching were not measured.

## Visual findings from actual fresh renders

Reviewed realistic_after/workshop_machines.png, yard.png, maintenance.png and cellblock.png. Corrected dryer front is visible, textured and floor-seated. Compared with the previous washer geometry, this improves readable industrial detail, but its baked front shading/door reads flatter than a close-up hero machine. Press paint remains uniformly clean and the forms still look simplified.

Yard: court asphalt cracks visibly repeat in parallel across a small number of broad10m tiles; the large transverse crack is conspicuous. Ground outside the court has a much smaller grain scale, giving a discontinuity in texture frequency. Yard wall finish is calm rather than uniformly rusty, but large repeating precast wall bays and identical pillar finish remain obvious. Use localized joint variation, subtle low-frequency color variation and a few contact-specific wear decals in a later art pass, preserving legible markings. Do not uniformly increase dirt.

Workshop: upper wall masonry pattern is quite fine at camera distance; texture scaling is consistent across walls, with no gross stretch visible, but should be compared against400x200mm real CMU in close view. Floor is appropriately restrained and clean; linen stacks remain box forms despite valid woven cloth maps. This is geometry work, not a material deficit.

Maintenance: wall and floor textures appear plausible at this distance; uniformly smooth pumps, rails and exposed pipes need variation at joins/supports, not global rust. Large dark ceiling loses structural detail. This capture alone cannot diagnose whether the limitation is lighting exposure or surface roughness.

Cell block: paint, steel and concrete style are coherent; long repeated door/cell modules and identical bedding remain obvious. Upper doors look flat and uniformly colored. Floor normal detail is restrained; no major texture UV stretch visible. Generated bed geometry is a larger deficit than texture resolution.

## Remaining validation

No assertion of every glass/wood/rubber/leather/plastic/fabric material coverage, correct per-asset UV density or2K–4K optimization is warranted from these four views. Inspect close-up prop material response under neutral movable lighting, reconcile phase03 copy hashes, and profile compressed runtime textures. Complete material requirement remains unverified.
