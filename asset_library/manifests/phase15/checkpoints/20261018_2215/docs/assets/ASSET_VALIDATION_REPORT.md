# Asset validation report — 2026-10-18

Scope: real downloads and Godot 4.7.2.stable.steam.ed1daf0bf on Windows. No gameplay implemented. PASS means only the named test passed. NOT TESTED is never PASS.

| Test | Result | Evidence / limits |
|---|---|---|
| Provider checksums | PASS | 25 Poly Haven files match provider MD5; SHA-256 and byte sizes in download_checks.json (read actual count there). |
| Kenney archive integrity | PASS | Python ZipFile.testzip returns no corrupt member; original ZIP SHA-256 in manifest. |
| PNG/JPEG decode | PASS | Pillow verify on downloaded maps; no image decode errors. |
| Godot imports / resource load | PASS | Three glTF scenes, external bins/textures resolved; selected OGG load and positive duration; machine output godot_resource_validation.json. Texture .import resources generated. |
| Static model visual inspection | PASS | Three rendered PNG previews inspected: cart textured, pipe modules intact, lamp variant/component atlas visible. One camera only; no exhaustive topology review. |
| Material assignment | PASS | 20 MeshInstance3D surfaces total, no null active materials; diffuse/roughness appear in previews. Does not certify physically correct calibrated values. |
| Scale / orientation | NOT TESTED | Imported AABBs recorded below; plausible human-sized props, no measured reference object or modular snap test. Godot Y-up render upright. |
| Collision / navigation / performance | NOT TESTED | No gameplay level, collision generation, navigation bake, LOD, split-screen GPU budget, or repeated-instance test. |
| Characters / skin / skeleton | BLOCKED | No character downloads; bone map, skin deformation and proportions cannot be tested. |
| Animations / root motion / sliding | BLOCKED | No animation deliverables. |
| Audio decoded waveform | PASS | FFmpeg decoded all 20 selected OGGs: maximum sample peak 0.898954, zero samples at/above full scale. audio_waveform_validation.json. This does not exclude source clipping below full scale. |
| Audio listening / mix suitability | NOT TESTED | No listening session or in-scene mix review. |
| Concrete/metal PBR assembly | NOT TESTED | Maps verified and imported, no assembled/rendered wall material. |

Geometry: lamp 26,576 triangles / 11 meshes (multiple variants and loose parts, isolate selected variant); cart 18,902 / 1 mesh (1.603 × 1.377 × 1.103 m); pipe collection 12,340 / 8 meshes. Triangle counts are Godot primitive counts, not source quads. Lamp and pipe aggregate bounds cover source layout, not an individual module. These source models need LOD/collision authoring before repeated scene use.

Evidence: [resource JSON](../../asset_library/manifests/godot_resource_validation.json), [file checks](../../asset_library/manifests/download_checks.json), [cart render](../../asset_library/manifests/industrial_storage_cart_1k_preview.png), [lamp render](../../asset_library/manifests/industrial_caged_sconce_1k_preview.png), [pipes render](../../asset_library/manifests/modular_industrial_pipes_01_1k_preview.png). Empty GUI stdout logs alone are not proof; JSON and saved framebuffer images prove this invocation executed. Reproduce: import editor first, then run tools/validate_resources.gd using a real rendering backend (GL compatibility used). Headless dummy rendering does not certify visuals.

Overall asset acceptance: BLOCKED by explicitly inventoried missing requirements. No 3D conversion performed because selected assets already provide glTF 2.0. No runtime-ready completeness claimed.
