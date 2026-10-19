# Sketchfab conversion and compatibility — 19 October 2026

Three real downloaded ZIP archives and source/GLB downloads are preserved; CRC and safe extraction passed. Official public metadata JSON saved for all three verifies CC BY 4.0, creator attribution and commercial use. Earlier zero-byte HTML was inadequate; metadata supersedes it. See sketchfab_inventory.json for hashes, paths and source URLs.

Blender 5.1.1 imported actual geometry/textures and rendered all three. No missing image paths, no animation actions, no skeletons. Exported GLBs passed isolated Godot 4.7.2 import and instantiation with 0 null materials (12 tower, 11 laundry, 2 handcuff mesh instances). Godot validation log has no reported warning/error. This is isolated load validation, not final in-game render/playtest.

| Asset | Embedded textures | Converted bounds XYZ in Blender metres | Acceptance limits |
|---|---|---|---|
| Handcuffs with keys | Three 4096 maps | .224 x .299 x .0136 | Detailed worn metal actual render. Source multiplied .05; physical measurement unverified. Static open cuff pose, no hinge rig/restraint animation. |
| Industrial dryer/ironing | Two 2048 maps | 4.463 x 1.769 x 2.154 | Actual render shows realistic laundry/ironing equipment. Removed large display backdrop; source multiplied .45. Branding review, doors/buttons, jammed press and relay interactions still required. |
| Guard tower | Four 1024 maps | 3.707 x 3.375 x 7.118 | Actual render shows concrete pillars, stairway, railings, cabin and mounted light. Plausible scale, no measured reference. 1k maps limit close-up texel density; no working light. |

Derivatives are ready as Phase 02 static placement candidates. Collision/navigation, LOD/performance, interaction mechanisms, final scale calibration and cinematic/split-screen quality remain NOT TESTED. These files do not certify mission completeness or AAA readiness. The handcuff source material is named None but is a real material: exported Godot material check passes; it is not a missing assignment.

Actual previews: simple_handcuffs_actual.png, industrial_dryer_ironing_actual.png, guard_tower_actual.png. Scripts and logs are preserved in tools/ and this manifest folder.
