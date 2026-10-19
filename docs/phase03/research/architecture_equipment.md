# Phase 03 architecture and equipment acquisition

19 October 2026. Status: targeted source acquisition performed; production integration and graphical acceptance remain incomplete. No runtime scripts were edited and no Godot process was launched by this specialist.

## Existing library first

The 335-model bulk library and older acquisition folders were both searched. Existing glTF packages below were opened as JSON and their external buffer/image dependencies checked: **zero missing dependencies in five packages**. SHA256 values are retained in `asset_library/original_downloads/phase03/existing_library_review/verified_reuse.json`.

| Need | Existing reusable source | Finding |
|---|---|---|
| CCTV | `assets/props/phase15_discovery/security_camera_01/security_camera_01_1k.gltf` | Already acquired CC0 Poly Haven camera, complete dependencies. Reuse before buying/downloading another camera. |
| CCTV alternative | `asset_library/original_downloads/phase025_bulk_20261019/models/security_camera_02/security_camera_02_1k.gltf` | Complete two-mesh model. |
| Service/loading entrance | `assets/props/phase15_polyhaven/rollershutter_door/rollershutter_door_1k.gltf` | Complete two-mesh shutter, not a barred cell door. |
| Laundry support cart | `asset_library/original_downloads/industrial_storage_cart/industrial_storage_cart_1k.gltf` | Complete detailed cart; does not replace washers or presses. |
| Maintenance services | `asset_library/original_downloads/modular_industrial_pipes_01/modular_industrial_pipes_01_1k.gltf` | Eight mesh parts with complete dependencies. |

Existing bulk tool cart, metal toolbox, steel shelves, worn rack, hose reel, industrial lamps and utility cabinets are relevant support props. None is a prison structural shell, conveyor scanner, industrial washer or laundry press. Electric stove, industrial microscope, medieval castle door and concrete cat statue were rejected as category mismatches. A generic household appliance must not be enlarged and called industrial laundry equipment.

## New legally clear download

**[PBR Industrial Asset Pack](https://opengameart.org/content/pbr-industrial-asset-pack)** by a52, based on [rubberduck's original CC0 industrial pack](https://opengameart.org/content/high-quality-industrial-asset-pack). Both official author pages identify CC0. The PBR Blender source edition was chosen rather than the separately offered older baked edition.

- Download: `https://opengameart.org/sites/default/files/oga_industrial_a52_version_0.zip`
- Folder: `asset_library/original_downloads/phase03/oga_pbr_industrial/`
- Archive: 57,954,847 bytes.
- SHA256: `4499f14fa664e83fd2b746c0e88a12249e8143ec9cd2b7ca9dd3d75aad50da47`.
- Saved both official author/license pages, CC0 legal text and machine-readable provenance.
- Every archive entry was checked to remain within the extraction root before extraction.

Actual Blender 5.1.1 source inspection found **59 mesh objects**: control terminal, tank control panel, vents, tanks, pipes, stairs/concrete paths, railings, garage elements and support structures. Bundled `preview.png` and `render.png` were visually inspected: useful industrial forms with weathered materials, but quality varies and no prison-specific shell is present. This is a candidate support kit, not an approved complete environment replacement.

The source contains 97 resolved/packed image datablocks and 15 unresolved legacy image references. These are recorded in `geometry_inspection.json`; per-material usage and conversion must be checked before export. No missing map is silently represented as fixed. No GLB was integrated, no in-game screenshot was claimed, and the kit contains no washer or laundry press.

## Official-source search and rejections

| Source/candidate | Decision and evidence |
|---|---|
| [Poly Haven](https://polyhaven.com/) local catalog and originals | Relevant cameras, shutter, carts and pipes already acquired. No additional download needed for these. No complete modular prison shell, security monitor or industrial washer in inspected model catalog. |
| [ambientCG](https://ambientcg.com/) | Official site confirms CC0 commercial use. Existing large concrete/PBR library already sufficient; adding surface sets does not repair missing structural geometry. No suitable prison/scanner/equipment model was verified in this search. |
| [Fab Modular Prison Pack](https://www.fab.com/listings/3ec8a7f7-da30-4f77-ac66-9fb8c5d98cda?lang=en) | Listing requires purchase/license selection and advertises Unreal Engine format. No free license or direct Godot-ready acquisition verified; not bought or downloaded. |
| [Sketchfab security monitor by wilsz95](https://sketchfab.com/3d-models/security-monitor-937a329014d84410b6ef34acb55d7034) | Official indexed listing identifies CC Attribution and 1.1k triangles. Page fetch failed; no downloadable payload obtained. Geometry/material quality and file acquisition unverified. No authentication bypass. |
| [Sketchfab industrial washer by Peanut-Bar](https://sketchfab.com/3d-models/industrial-washing-machine-5fe4dce83a214c4ba935f3cb78831164) | Repeat official-page check returned HTTP403. Previous research notes generated geometry. Not downloaded; not approved. |
| [CGTrader industrial washer](https://www.cgtrader.com/3d-models/industrial/industrial-machine/industrial-washing-machine-4fecbb0e-9ae5-4b75-a55a-04c8011def97) | Official listing describes industrial stainless washer, but no legally clear free download verified. No purchase performed. |
| [OGA Modular Industrial Kit](https://opengameart.org/content/modular-industrial-kit) | Official description explicitly low-poly, stylized, single texture; rejected for this realism target. |
| [OGA low-poly monitor](https://opengameart.org/content/low-poly-monitor) | Explicit 564-triangle low-poly model; no evidence it improves existing realism. Rejected rather than padding acquisition count. |
| [Sketchfab MD-6350 metal detector](https://sketchfab.com/3d-models/metal-detector-2527ebf908e94ee88d00aad6fa062377) | Handheld detector, not walkthrough security arch or baggage scanner; rejected category mismatch. |

Earlier laundry research remains canonical at `asset_library/original_downloads/phase025_integration/laundry_research/CANDIDATES.md`: BlendSwap dryers/washers require sign-in; domestic sources do not meet industrial requirements; manufacturer BIM redistribution rights were not cleared. Those blocked downloads were not retried through alternate access routes.

## Remaining blockers and next integration gate

1. Detailed industrial washer, dryer row and laundry press: no freely downloadable verified replacement acquired. Existing acquired ironing/dryer prop does not close this gap.
2. Walkthrough scanner and baggage X-ray conveyor: no suitable legally clear downloadable model verified.
3. Security monitor: candidate discovery only, payload unavailable.
4. Modular prison architecture: no high-quality complete free kit verified. Existing gameplay architecture and original Blender fence remain the actual implementation.
5. New industrial kit: resolve used material dependencies, select useful elements, export with retained provenance, inspect scale/collisions and obtain in-game visual evidence before readiness approval.

Acquisition counts are not a production-quality verdict. These sources do not establish a realistic whole-game completion claim.
