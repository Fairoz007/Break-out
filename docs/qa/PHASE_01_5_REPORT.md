# Phase 01.5 report — asset recovery, repair and verification

18 October 2026. Coordinator plus specialised agents:

| Agent | Area |
|---|---|
| 03 / C | Architecture |
| 04 / D | Audio and materials; discovery integration |
| E | Discovery |
| F | Independent QA |

The coordinator did the character and animation work and the manifest. No gameplay was programmed. STORY.md and the screenplay are unchanged.

## 1. Recovery checkpoint

The project is **not a Git repository**, so `git status` is unavailable. A file checkpoint of the docs and every manifest JSON was taken before editing: `asset_library/manifests/phase15/checkpoints/20261018_2215/`.

State recovered at the interruption point:

- Five MPFB character repair cycles were exhausted and FAILED.
- `tools/phase15_integrate.py` had been written but **never run**, so `assets.json` was still the Phase 01 baseline.
- Two proxy GLBs had been exported but never Godot-validated.
- The UBC character kit had been downloaded but **never evaluated**.

Completed work was kept: architecture, bulk audio and materials, the PCM16 and texture repairs, and the Godot import fixes. Nothing verified was redownloaded.

## 2. What changed

| Area | Result |
|---|---|
| Characters | Deformation solved by replacement rather than a sixth repair. A **realistic Rocketbox cast** (MIT) and a **UBC proxy cast** (CC0) were built with a glTF-space clip transfer, re-imported in Blender, imported into Godot, and rendered in neutral, walk, run, sprint, crouch, jump, interaction, push and climb poses. Every image was viewed. Recolour defects were fixed over 3 cycles. |
| Animations | 37 UAL clips on all 13 characters. Baseline locomotion and interaction PASS. Paired, cinematic and facial animation are missing (13 items listed). |
| Architecture | Agent 03 found 1 FAILED and 10 defect classes. Repair cycle 1 left 0 failing of 70. A 3 m stair, hinge pivots, a split spillway door, fixed fence and shelf scale were added, and 38 split kit pieces were created. |
| Critical props | Original lifting grille (M05/M06), pump (M05) and basketball (M02). |
| Discovery | 50 candidates evaluated. Acquired with checksums: 8 Rocketbox avatars, 11 props, 1 environment piece and 27 audio clips. Account-gated sources were recorded but not accessed. |
| Audio / materials | 614 clips audited, 25 rejected, 0 header failures. All 19 materials load and render. |
| Godot | Import exit 0 with empty stderr. **908/908** resource jobs load with 0 null materials. Character report covers 13/13. The asset inspection scene `tests/asset_inspection/phase15_asset_inspection.tscn` was saved and rendered. |
| Manifest | `assets.json` now has 831 records with evidence-based statuses and 22 bundles carrying functional and production status. The coverage matrix is generated from the manifest. |

## 3. Final counts (from `assets.json`, not estimates)

| Measure | Count | Notes |
|---|---:|---|
| Unique downloaded asset records (Phase 01.5) | **670** | 614 audio, 19 PBR sets, 31 props, 1 environment piece, 4 animation libraries, 1 font |
| Downloaded records carried from Phase 01 | 6 | 2 material sets, 3 prop sets, 1 foley selection (20 clips) |
| Character source packages downloaded | 12 | 8 Rocketbox avatars, UBC kit, UAL1, UAL2, MPFB (used to build the 19 character records) |
| Original created assets | **76** | 50 architecture modules and props (48 plus 2 from repairs), 3 critical originals, 14 UI, 2 VFX, 7 synthetic audio |
| Derived assets | 57 | 38 split kit pieces; 19 character builds (6 realistic, 7 proxy, 4 failed, 2 superseded) |
| Validated (usable: Godot load plus file, licence and checksum) | **772** | Most are PARTIALLY_VERIFIED. Listening, collision and nav are untested, so none is claimed fully VERIFIED |
| Rejected | **31** | 25 audio (incl. 3 near-duplicates), 4 FAILED MPFB characters, 2 SUPERSEDED proxies; plus 2 orphan builds moved to `rejected/` |
| Duplicates removed from usable count | 3 near-identical audio | 0 byte or PCM duplicates found; byte duplicates had already been excluded at acquisition |
| Godot resource jobs | 908 | All load |

## 4. Readiness gates

| Gate | Verdict | Evidence |
|---|---|---|
| **A: Core gameplay assets** (characters, basic animation, essential architecture usable) | **PASS** | 13 characters skinned and animated in Godot. Idle, walk, run, sprint, crouch, jump, interact, pick-up, push and climb are rendered in-engine. All six missions are functionally covered on critical assets ([coverage matrix](ASSET_COVERAGE_MATRIX.md)). 908/908 loads. |
| **B: Realistic character assets** (protagonists meet the realistic standard, validated rigs) | **PARTIAL** | Adrian and Noah are realistic Rocketbox avatars with validated rigs and correct deformation. Still open: no facial blendshapes at runtime, no likeness approval, uniforms are texture recolours, specular→roughness is not calibrated. |
| **C: Level construction** (mission-critical architecture and props available) | **PARTIAL** | Every named interactive object has an asset except the M01 body scanner and M06 restraints. Collision and nav are not authored. The bus and watchtower are stylised blockouts. |
| **D: Cinematic assets** (required actions, props and environments) | **BLOCKED** | No facial performance or VO. Paired, contact-aligned actions are missing. Close-up readable props are unfinished. |
| **E: Production asset quality** | **BLOCKED** | No listening review. Texture import settings not production-grade. Institutional art calibration, LOD, collision/nav and performance are untested. |

The original brief asked for five separate decisions. They map to the gates as follows:

| Original decision | Verdict | Gate |
|---|---|---|
| (1) Ready for core gameplay programming | **PASS** | Gate A |
| (2) Ready for realistic character gameplay | **PARTIAL** | Gate B |
| (3) Ready for Chapter 1 level construction | **PARTIAL** | Gate C; blockout can start now, with collision/nav authored as part of it |
| (4) Ready for cinematic animation production | **BLOCKED** | Gate D |
| (5) Ready for final visual polish | **BLOCKED** | Gate E |

## 5. Remaining blockers

See [BLOCKERS.md](BLOCKERS.md), P01–P09:

- Facial performance and VO
- Paired animation
- Likeness and art approval
- Scanner and realistic bus
- Collision, nav, LOD and texturing
- Audio listening and missing categories
- Close-up props
- Split-screen UI/VFX
- Licence credits

## 6. Recommended next milestone

**Phase 02a: core co-op gameplay on graybox.** Use the realistic Rocketbox cast (UBC as fallback) and the inspection-validated modules. Scope:

- Two-player split-screen controller.
- Animation state machine over the 37 clips.
- Interaction framework with alignment markers.
- Collision and nav authoring on an M02 yard and M05 maintenance blockout.

Run these art tasks in parallel:

- Convert the Rocketbox facial FBX.
- Commission or capture the 13 missing animations.
- Get likeness sign-off.
- Run an audio listening pass.

## 7. Agent F independent QA

Pending at the time of writing. The final findings are appended to [PHASE15_INDEPENDENT_REVIEW.md](PHASE15_INDEPENDENT_REVIEW.md) and summarised below once complete.
