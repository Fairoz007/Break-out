# Phase 04 architecture / workshop work — 2026-10-20

Status: INTEGRATED, pending final visual QA and full mission regression. Phase 04 remains INCOMPLETE.

Final integration addendum: original detailed single beds were also integrated in EnvCellblock and EnvSolitary.
They retain the original hidden bed instance/collider and use the new visual within its footprint. Source
`asset_library/original_created/phase04/prison_bunk.blend`; builder `tools/phase04_architecture_bunk.py`;
runtime/metadata/1K Fabric030-derived maps under `assets/props/phase04_architecture/`. It is a single bed,
not a two-tier bunk. Fresh final cell_interior/solitary screenshots confirm visible placement. Final source and
Windows executable chapter runs passed without errors; all accepted test gates are in realistic_validation.json.
Independent QA still withholds complete architecture/scene approval. The first missing-import test was rejected.

## Audit and priorities

Reviewed prior Phase 04 workshop_machines capture and the phase025 bulk inventory. The machinery enclosure's generic washers are a high-impact weak point: simplified housings, circular disk doors and minimal industrial detail. The presses have several modeled components but still read as clean procedural approximations; they remain ACCEPTABLE BUT NEED IMPROVEMENT. Folded linen stacks remain simple blocks; full realistic laundry production dressing remains incomplete. Workshop shell has believable scale and layered wall finish but is still largely generated architecture. Existing Poly Haven scanned rack, tool cart, utility box, medical box and wall hose are suitable reuse candidates already present; downloading duplicates is unnecessary.

The maintenance pump models, tunnel shell and safety rails remain outside this change and need independent final assessment. No new architecture, pump, character or transport asset was acquired in this subtask.

## Actual replacement work

Reused the legally acquired **Industrial Dryer Machine & Ironing** by **karakocyunus**. Source: https://sketchfab.com/3d-models/industrial-dryer-machine-ironing-9716a3b43fa54cf282706601526b7f73 ; license CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ . Official saved API metadata explicitly says commercial use permitted and attribution required. See `assets/props/phase04_architecture/LICENSE_AND_PROVENANCE.md` for exact original archive and credit.

Blender 5.1.1 imported the actual existing GLB; `source_inspection.png` records the viewed assembly, including the textured industrial dryer front, visible drum/door, controls and ironing equipment. Separated components, baked transforms, centered floor origins, retained original texture materials, and reduced exceptionally dense ironing components to 25% geometry. This is model replacement, not texture-only modification. No complete PBR map-set claim is made: original source supplies textured materials, with lighting detail baked into the source color texture.

- `industrial_dryer.glb`: 1,856 triangles; source dimensions normalized to 1.9m high, 1.9m wide, 1.348m deep. Two units placed at x9.6 and15.6, z-4.8, behind the existing press safety rail. Original four washer mesh instances are hidden, preserving all collision bodies. Front orientation corrected to yaw180 after an initial rear-facing render was rejected.
- `ironing_station.glb`: 23,447 triangles; 1.25m high, approximately1.323m wide and0.662m deep after reduction. Replaces the offset combined assembly with a correctly floor-centered station at (24,0,-2.8). Original assembly collision remains unchanged and hidden.

Actual gameplay scene integration is in `scripts/world/env_workshop.gd`, which is used by EnvWorkshop.build for mission03. Presses, controls, nav geometry, mission points, spawn anchors and safety rail remain intact. Original geometry remains hidden to preserve the collision envelopes exactly; this has a memory/draw-resource cost and is a deliberate conservative integration choice. The old meshes are not rendered.

## Validation and evidence

`tools/phase04_architecture_validate.tscn` was run headlessly in Godot. Successful exit0; final validator stderr empty. `assets/props/phase04_architecture/validation.json` records:

- 59 collision shapes before and after; global transform and debug-mesh AABB comparison PASS.
- All 15 existing mission/spawn point values equal to HEAD snapshot PASS.
- Both GLBs load as PackedScene, floor_y=0, expected metric height PASS.

Conversion hashes, dimensions and triangle counts are in `conversion.json`. Blender source render at `source_inspection.png`. Existing prior workshop image is the before comparison. The local `evidence/` camera capture is an intermediate REJECTED iteration (rear-facing dryer); it must not be treated as final proof. Root final capture after yaw correction is required. Full mission gameplay regression and final visual review are owned by the main session and pending at this handoff. No asset in this subtask is claimed VERIFIED.

## Remaining blockers

Final camera must confirm visible dryer front, texture appearance and floor contact after yaw fix. Washer requirement is not fulfilled by the two dryer replacements: detailed realistic industrial washers remain missing. Presses, folded linens and maintenance pumps remain quality gaps. Source dryer is a textured modest-poly model rather than a fully modeled close-up production hero asset; baked detail limits its cinematic close-up quality. Complete high-quality prison architecture remains incomplete.
