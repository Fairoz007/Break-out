# Realistic asset acquisition and integration — 20 October 2026

**INCOMPLETE.** This session integrates genuine geometry improvements, but does not satisfy the production character, animation, bus and complete environment acceptance criteria. No downloaded asset or newly exported model is automatically VERIFIED.

Read `ASSET_COVERAGE_MATRIX.md`, `phase04_realistic_assets.csv` in the asset-library manifests, `CHARACTER_ASSET_AUDIT.md`, `ARCHITECTURE_WORK.md`, `BUS_COURT_WORK.md`, `MATERIALS_AUDIT.md` and `REALISTIC_INDEPENDENT_QA.md` together.

## Library reuse and legal sources

Read the requested `asset_library/manifests/phase025_bulk_20261019/inventory.csv` and its detailed JSON. Its recorded inventory contains 1,000 assets: 335 models and 665 materials, 4,545 files / 8,728,085,792 bytes. Its historical verification reports zero failed downloads. That record establishes acquisition integrity at that time, not current visual or integration approval. This session does not claim to have rerendered all 1,000 assets or rehashed the entire 8.7 GB library. The new manifest recomputes SHA256 for selected runtime payloads and the selected original files when identified.

Reused the actual already-downloaded sources before adding downloads. **No new third-party model purchase or download occurred this session.** New GLBs are conversions or original geometry. Original source downloads remain in the library.

| Source | License evidence and use |
|---|---|
| [3D Bus — ajanhallinta](https://opengameart.org/content/3d-bus) | Official source page rechecked: CC0. Original BUS.blend/FBX/OBJ remain under `asset_library/original_downloads/phase025_integration/oga_bus/`. Derivative conversion history in existing bus asset record. Source has no original cabin; project-authored cabin and hardware must not be attributed to source author. |
| [Industrial Dryer Machine & Ironing — karakocyunus](https://sketchfab.com/3d-models/industrial-dryer-machine-ironing-9716a3b43fa54cf282706601526b7f73) | Preserved official Sketchfab metadata explicitly identifies CC Attribution 4.0 and permits commercial use. Fresh source-page request returned 403; no restriction was bypassed. Original archive retained. Correct attribution and new derivative changes recorded in `data/credits.txt` and adjacent LICENSE_AND_PROVENANCE.md. |
| [Microsoft Rocketbox](https://github.com/microsoft/Microsoft-Rocketbox/blob/master/LICENSE.md) | Official MIT notice rechecked; preserve copyright and license. Six existing runtime bodies inspected structurally. No new character geometry approved. Animation rights are tracked separately from MIT body rights. |
| [Poly Haven](https://polyhaven.com/license) | Official CC0 policy rechecked. Existing individually identified assets/maps reused. This does not license unrelated sites or resolve untraced copied filenames. |
| [ambientCG Fabric030](https://ambientcg.com/view?id=Fabric030) | Existing recorded CC0 fabric source reused for original bed geometry; 1K runtime maps derived from preserved 2K originals. See bed source/metadata. |
| Mixamo | Existing source clips and license record reviewed. Commercial game use differs from CC0 asset redistribution. Retarget tests were visually rejected; none promoted into the game. |

## Actual changes in the game

| Runtime asset | Actual change | Integration |
|---|---|---|
| `phase04_realistic/blackridge_transport_bus_chassis.glb` | Existing detailed coach plus modeled frame rails, suspension, axles, differential, driveshaft and exhaust. Existing animated wheel/door node names and pivots preserved. | `EnvIntake.build`; original placement, scaling and collision retained. The added underside is mostly hidden from existing cameras, so this is a limited visible gain. Flat panels and simplified seats still fail the cinematic goal. |
| `phase04_realistic/hoop_perforated_steel.glb` | Replaces painted-dot backboard with 756 real through-holes; elongated chain geometry and refined bent support. Existing footing, rim and support sizes retained. | `prison_court.hoop`; both court ends, same post collider and 3.05 m rim height. |
| `phase04_realistic/basketball_recessed_channels.glb` | Smooth round shell with modeled recessed seams and independent rubber inserts. First jagged-pole iteration rejected and rebuilt. | Mission02 visual path only; interaction and rolling logic retained. Fine pebble skin remains below hero quality. |
| `phase04_cellblock/tier_security_door.glb` | Original 9,020-triangle assembly: frame, hinges, protected vision panel, lock, handle, food pass, louvres, kick plate and fasteners. | Upper cell tiers in daytime/night cellblock; visual only. Original wall/collision and number signs retained. |
| `phase04_architecture/industrial_dryer.glb` | Actual textured industrial machine separated from legally acquired source assembly, centered and metric-scaled. | Two units replace generic washer visuals in workshop. All original collision bodies retained and old meshes hidden. Dryers do not fulfil the remaining washing-machine requirement. |
| `phase04_architecture/ironing_station.glb` | Separate floor-centered ironing unit, reduced dense geometry, source materials preserved. | Workshop dressing; original collision envelope retained. |
| `phase04_architecture/prison_bunk.glb` | Original detailed single bed: welded tubes, braces, spindles, feet, slats, bolts, rounded stitched mattress, pillow and draped blanket mesh. Despite filename it is a **single bed**, not a two-tier bunk. | Cellblock visible beds; original collider instance kept with old meshes hidden, new visual within original footprint. Two-tier bunks remain an unmet requirement. |
| Court asphalt | Repeat changed from 10 m to approximately 2 m to reduce giant aggregate/cracks. | Supplementary material correction alongside real equipment geometry changes. |

## Inspection, evidence and regression limits

Godot 4.7.2 and Blender 5.1.1 were directly run. Existing Godot project was inspected through its window. Fresh deterministic captures use actual environment builders, project autoloads and D3D12 Forward+ on RTX2060. `visual_evidence/realistic_before/` is the start-of-session baseline, not the older `baseline/` folder. `realistic_after/`, `realistic_details/` and `realistic_comparisons/` hold current matched evidence. Camera metadata is adjacent. Actual mission screenshot evidence and current gameplay results are under `tests/phase04/evidence/realistic_*`.

The first post-integration parse check passed 60 scripts; final parse passed 63 scripts, and focused movement/camera suite passed 14/14. The corrected final source Chapter1 autopilot reached `chapter_complete` with no resource/script errors and no stuck events. One intermediate graphical run is explicitly rejected: it reached completion despite bed-loader errors. The missing import was repaired, its Blender source moved to `asset_library/original_created/phase04/`, and fresh captures/source/export tests run again. Accepted/rejected evidence is machine-recorded in `tests/phase04/evidence/realistic_validation.json`. Workshop-specific comparison verifies all 59 collision shapes/transforms/bounds and all 15 spawn/mission points match the preserved baseline. Navigation still logs its existing agent-radius voxel-rounding warning. Passing automation does not validate human controller play, animation quality, audio, every patrol route or every visual requirement.

Independent QA compares **this session's** before and after images and explicitly excludes old bus doors/partition and old curved hoop support from the new-change claims. No whole environment has been independently approved as cinematic or ultra-realistic.

## Remaining priorities

1. Production protagonist face/hair/wardrobe geometry and additional guard, officer and staff variants.
2. Validated pull, climb, vault and paired assistance clips with foot locking and actual prop/contact alignment. Existing and experimental Mixamo retargets failed multi-frame render review.
3. Bus exterior surfacing, credible close-up seats, dashboard and complete door/cabin review; new underside alone is insufficient.
4. Actual two-tier prison bunks, detailed sink/toilet fixtures, industrial washers, linen geometry, dense but functional scene dressing, architecture variation and staircase review.
5. Per-asset neutral-light material/UV review, copied map provenance reconciliation and final performance/human acceptance.

Downloads, generated triangle counts, passing imports and automated mission completion do not close these defects.
