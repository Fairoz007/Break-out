# Next asset candidates — read-only payload audit, 2026-10-20

No runtime/source changes were made for this audit. Existing manifests, actual GLB/glTF payload structure and saved model previews were inspected. A source link or inventory row alone is not treated as delivered suitability.

## Qualified reusable frame candidate

**Poly Haven Old Bed Frame, Luca B, CC0** — https://polyhaven.com/a/old_bed_frame .

- Runtime candidate: `assets/props/phase15_discovery/old_bed_frame/old_bed_frame_1k.gltf`; companion `old_bed_frame.bin` and `textures/` are already present. Original payload: `asset_library/original_downloads/phase15_discovery/polyhaven_old_bed_frame/`.
- License evidence: `asset_library/licenses/phase15_discovery/polyhaven_old_bed_frame/polyhaven_license.html`, author/dimensions in `polyhaven_info.json`.
- Actual mesh: 1 mesh,49,990 indexed triangles,3 source images (color, OpenGL normal, ARM). Source dimensions approximately0.905m wide ×2.002m long ×1.201m high. glTF SHA256 `661055e76d292ae5ec812f05077a6870414527c2d63947574ea8fc739e16de08` (companion files also needed).
- Actual saved render reviewed: `asset_library/manifests/phase15/previews_discovery/old_bed_frame_1k.png`. It visibly has rounded tubular bent ends, narrow vertical rails, modeled wire mattress support, joints and localized chipped paint/rust. This is a realistic detailed frame, not the broad flat headboard of the old prison_bed asset.
- Suitability: **qualified for controlled reuse as a single bed FRAME**, especially solitary/infirmary or older prison wing. Not a complete bunk, has no mattress/pillow/blanket. Its1.201m height and0.905m width exceed the existing0.95m /0.85m envelope; safe reuse needs deliberate fit/collision review. The49,990 triangles are unnecessarily heavy for many cells; create LODs and choose selective placement. Existing new `phase04_architecture/prison_bunk.glb` supplies a lighter project-authored complete single bed; frame replacement is optional, not a proven mandatory improvement. No current final-test mutation is warranted.

## Available payloads rejected for critical replacement

| Need | Actual existing file | Direct evidence | Verdict |
|---|---|---|---|
| Prison toilet | `assets/props/phase15/toilet.glb` |24,320bytes;4 meshes;384 triangles;0 images; nodes Pedestal/Bowl/Seat_opening/Cistern. Saved actual preview `asset_library/manifests/phase15/previews/P15_TOILET.png` inspected: block-like cistern, broad flat dark seat opening. | No qualified realistic institutional toilet; current placeholder is not a new candidate. Rejected older copies under `asset_library/rejected/phase15_architecture_prerepair/` are not upgrades. |
| Prison sink | `assets/props/phase15/sink.glb` |4 meshes;464 triangles;3 images; Pedestal/Bowl/Recess/Faucet. Actual preview `asset_library/manifests/phase15/previews/P15_SINK.png` inspected: block pedestal, flat dark recess and rudimentary faucet. | No qualified realistic prison sink; scan textures on simple geometry do not solve it. |
| Previous complete bed | `assets/props/phase025/prison_bed.glb` |1 combined mesh;34,952 triangles;3 images; already visually superseded by authored tubular bed in this pass. | Not an alternate production-quality bunk. |
| Modern city bus | `asset_library/original_downloads/phase025_integration/city_bus.glb` |803,152bytes;83 meshes;18,780 indexed triangles;9 materials;0 images. Existing measured dimensions3.2×11.985×3.11m in `tests/phase025/evidence/integration/bus_geometry.json`. Actual `bus_candidate.png` inspected: rectangular body, flat blank glazing and simple wheels; no visible production interior. | Reject as superior realistic transport replacement. Mesh count is mostly separated wheel spokes/windows, not sufficient visual complexity. |
| CC0 exterior coach | `asset_library/original_downloads/phase025_integration/oga_bus/BUS.blend`, OBJ/BUS.obj,FBX/BUS.fbx | Author README explicitly says CC0, no textures and **no interior**;14,507tris stated. Actual `Screens/bus1.png` inspected. Existing derivative already used by current transport bus. | Useful preserved base, not a newly found superior bus. Author ajanhallinta, https://opengameart.org/content/3d-bus . |
| Quaternius bus | `assets/props/phase15_discovery/quaternius_bus/quaternius_bus.glb`; original Public_Transport.zip |77,060bytes;3 meshes;1,530tris;7 materials;0 images. Clearly low-poly scope. License record `asset_library/licenses/phase15_discovery/quaternius_public_transport/source_page.html`. | Reject: stylized exterior without required detail/interior. |

The city bus saved official page is `asset_library/licenses/phase025_integration/city_bus.html`, titled Low-floor city bus /CC0, canonical https://www.innerscene.com/tools/library/3d-parts/low-floor-city-bus-9e7ce899 . Legal availability does not establish realism.

## Other bulk bed payload: wrong furnishing class

`asset_library/original_downloads/phase025_bulk_20261019/models/vintage_day_bed/vintage_day_bed_1k.gltf` and companion BIN/textures are present. Bulk manifest records Aron Łyczek, CC0, https://polyhaven.com/a/vintage_day_bed . Actual glTF has1 mesh,2,715 triangles and3 texture images; accessor bounds approximately1.973m ×1.127m ×0.855m before node transforms. Source categories/tags describe a wooden antique couch/bench/sofa-bed/chaise. No actual render was reviewed in this read-only audit. This is **not qualified as a prison bunk candidate**; do not promote it based on its filename.

## Scanner gap remains open

No suitable present-day walk-through/body-scanner model payload was found in the existing downloaded library. Security-light/camera assets are not scanners. The historic research rejects a noncommercial security machine and futuristic scanner gate; see `docs/assets/acquisition_20261019_RESEARCH.md`. `docs/assets/followup_20261019_ARCHITECTURE_RESEARCH.md` records a conditional airport pack link but no validated delivered payload. No link-only candidate closes this requirement.

## Practical next priorities

1. Obtain or author a detailed institutional stainless toilet/sink combination with basin cavity, flush valve, taps, drain, mounting hardware and realistic plumbing.
2. Obtain or author a present-day walk-through security scanner with believable proportions, control panel and ground mounting.
3. Obtain a genuinely detailed transport bus with modeled cabin/interior, beyond the current coach derivative. Existing alternatives do not clear this gate.
4. For bed variation, selectively reuse the licensed Old Bed Frame after LOD/fit checks, supplying bedding from the newly authored project assets. A complete bunk stack still requires design/integration work.

No new candidate is VERIFIED. Apart from the reusable frame, there is **no qualified existing superior payload** for these critical gaps in the audited library.
