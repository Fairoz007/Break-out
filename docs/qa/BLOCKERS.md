# Phase 01.5 blockers and disposition

Reviewed 18 October 2026, after the resumed Phase 01.5 session.

- **Core gameplay programming:** no asset blocker remains.
- **Realistic production quality:** still blocked.

Status per item comes from [assets.json](../../asset_library/manifests/assets.json) and `asset_library/manifests/phase15/integration_summary.json`. A functional substitute never closes a production blocker. History is in the [independent review](PHASE15_INDEPENDENT_REVIEW.md) and the [Phase 01.5 report](PHASE_01_5_REPORT.md).

## Resolved this phase

| Former blocker | Resolution | Evidence |
|---|---|---|
| B01 Rigged characters, CRITICAL | Realistic Rocketbox cast (Adrian, Noah, Rusk/guard, Mara, Silas, inmate) plus a UBC proxy cast. Valid skeletons, skinning and clothing in Blender and Godot | [Character report](CHARACTER_RIG_VALIDATION.md) |
| B02 Baseline animation, CRITICAL | 37 clips on every character, rendered in Blender and played in Godot | [Animation report](ANIMATION_VALIDATION.md) |
| Severe MPFB deformation (QA15-002) | Base replaced after 5 failed cycles; old files marked FAILED | Same |
| M02 ball, M05 lifting grille and pump | Original assets `P15_BASKETBALL`, `P15_SECURITY_GRILLE_4M`, `P15_PUMP_UNIT` | [Architecture report](PRISON_ARCHITECTURE_VALIDATION.md) |
| Architecture defects (shelves 10× scale, 1.8 m stair, no hinge pivots, single-leaf spillway door, fence overlap) | Repair cycle 1: 0 of 70 assets failing on retest | `asset_library/manifests/phase15/architecture_repairs.json` |
| Godot import of non-PCM WAV / corrupt extracted PNGs (earlier session) | PCM16 conversion; 60 textures restored from GLB bufferViews | 908/908 Godot jobs load |

## Open blockers

| ID | Severity | Blocks | Requirement | Evidence needed to close |
|---|---|---|---|---|
| P01 | CRITICAL for cinematics | Cinematics, dialogue | Facial performance and lip-sync. Rocketbox `_facial.fbx` (176 blendshapes) is preserved but not converted; there is no VO | Converted blendshape GLBs, a viseme test on an authored line, recorded VO |
| P02 | CRITICAL for co-op set pieces | M04 brace, M05/M06 paired actions, M06 restraint | Paired, contact-aligned animation: assisted climb, help-up, panel brace, two-hand handle pull, cuffed walk/search, kneel-and-shim, selector/brake hold, underhand roll, turn-in-place, pull | Licensed or captured clips, alignment markers, partner sync test in Godot |
| P03 | MAJOR | Realistic look | Character likeness and art approval: Mara age/hair, Rusk build, Noah hair, Adrian layered overshirt, scars/burn/incisor, calibrated PBR from specular, more guard/inmate identities | Art-direction sign-off on Godot close-up renders |
| P04 | MAJOR | M01 presentation | Body scanner (missing); realistic bus with interior (current bus is a stylised blockout) | Authorised assets or an approved scope change |
| P05 | MAJOR | Level construction quality | Collision shapes, navigation bake, door swing in-engine, LOD for the 5 assets over 20k triangles, institutional texturing (rust/white-floor calibration), realistic watchtower, court markings | Collision/nav scene test, profiler capture in split-screen |
| P06 | MAJOR | Audio presentation | Original VO, PA speech, crowd walla, diesel bus engine, radio speech, score. **No clip has been listened to** | Listening/mix session, licensed or recorded additions |
| P07 | IMPORTANT | Props close-up | Readable ledger page and later full ledger, badge legibility, photo hand contact, selector lamp states and brake pivot motion | Close-up camera renders and interaction rig test |
| P08 | IMPORTANT | UI/VFX | Half-screen localised subtitle layout; alarm beacon light and particle appearance in scene; reduced-flash test | Godot capture at split-screen resolution |
| P09 | MINOR | Licensing hygiene | Ship MIT notice for Rocketbox; CC-BY credit for the Ouren basketball hoop/rack/ball. (The stale `phase15_bulk_audio_corrections.json` checksums are fixed: 112 records now carry `current_runtime_checksum`, with the historical value kept.) | Draft written: [THIRD_PARTY_NOTICES.md](../assets/THIRD_PARTY_NOTICES.md); it still has to be placed in the shipped build's credits |

Not blocked:

- Core gameplay programming: locomotion, interaction prompts, co-op state, and blockout levels using the current assets.
- Missing optional dressing (extra crates, stools and UI sounds).

Account-gated sources (Freesound, Sketchfab, Mixamo, Fab) were not accessed. Using them requires the owner's own login and licence acceptance.
