# Animation validation — Phase 01.5

Date: 18 October 2026 (resumed session). **Baseline gameplay animation: PASS. Cinematic and paired animation: BLOCKED.**

Source: Quaternius Universal Animation Library 1 and 2, Standard editions, CC0. The originals are preserved in `asset_library/original_downloads/phase15_characters/`, and the runtime libraries are in `assets/animations/phase15/` (in-place and `_RM` root-motion variants). **37 unique source clips** were transferred onto all 13 characters (6 Rocketbox, 7 UBC) in glTF space; see the [character report](CHARACTER_RIG_VALIDATION.md) for the method. Count each clip once: 13 characters × 37 embedded copies is not 481 animations.

Evidence:

- **Blender:** re-imported GLB renders at rest plus 11 clip poses, front and side, for every character. All 37 clips at mid-clip on both Adrian variants: `asset_library/manifests/phase15_characters_previews/all_clips/*/sheet_all_clips.png`.
- **Godot 4.7.2:** every character's AnimationPlayer lists 37 clips, 17 of them flagged looping. 14 poses × 2 views were rendered in-engine: `…/godot/gsheet_*.png`, `godot_character_report.json`.

| Requirement | Clip(s) | Result |
|---|---|---|
| Idle | `Idle_Loop` (Godot name `Idle`) | PASS: rendered Blender + Godot |
| Walk | `Walk_Loop` | PASS: two phases, front and side, Blender + Godot |
| Run | `Jog_Fwd_Loop` | PASS |
| Sprint | `Sprint_Loop` | PASS |
| Crouch idle / crouch walk | `Crouch_Idle_Loop`, `Crouch_Fwd_Loop` | PASS |
| Jump / land | `Jump_Start`, `Jump_Loop`, `Jump_Land` | PASS (`Jump_Land` mid-clip render only) |
| Turning | none | MISSING: needs a turn-in-place clip, or procedural yaw over idle/walk |
| Door interaction | `Interact` (generic reach), `Chest_Open` | PARTIAL: no handle-aligned door clip |
| Pick up | `PickUp_Table` | PASS (table height only) |
| Repair machinery | `Fixing_Kneeling` | PASS (kneeling only, no standing panel work) |
| Push / pull | `Push_Loop` / none | PASS for push; pull MISSING |
| Heavy object | `Walk_Carry_Loop` | PASS (single-person carry) |
| Climb | `ClimbUp_1m` | PASS solo 1 m; root displacement transferred |
| Co-operative assisted climb / help-up / brace for partner | none | MISSING: paired, contact-aligned animation required |
| Synchronised two-body contacts (handle pull, hand-off) | none | MISSING |
| Combat / reaction | `Punch_Jab`, `Punch_Cross`, `Hit_Chest`, `Hit_Head`, `Hit_Knockback`, `Roll`, `Death01` | PASS (mid-clip render); block/stagger dedicated clips MISSING |
| Sit / stand | `Sitting_Enter`, `Sitting_Idle_Loop`, `Sitting_Talking_Loop`, `Sitting_Exit` | PASS (tested without a chair) |
| Wake / get up (solitary) | `LayToIdle` | PASS |
| Talking / gestures | `Idle_Talking_Loop`, `Idle_FoldArms_Loop`, `Idle_No_Loop`, `Yes`, `Consume` | PASS for body gestures |
| Wired handset / radio | `Idle_TalkingPhone_Loop` | PASS |
| Lean on rail | `Idle_Rail_Loop` | PASS |
| Restrained walking | `Walk_Formal_Loop` | PARTIAL: hands not cuffed |
| Throw / roll ball (M02) | `OverhandThrow` | PARTIAL: overhand throw, not an underhand roll |
| Facial / lip-sync / emotional performance | none at runtime | BLOCKED: Rocketbox `_facial.fbx` has 176 blendshapes, but they are not converted. UBC has none |

## Not tested

- Foot sliding and root-motion contracts (`_RM` libraries not transferred).
- Blend-tree transitions and loop seams in motion. Stills were inspected, not motion video.
- Finger poses on props.
- IK alignment to doors, handles and handsets.
- Any gameplay animation controller. None was implemented, by design.

Rendered stills cannot prove the absence of motion artefacts between the sampled frames.

## Missing-animation list (to commission or capture)

1. Turn-in-place, left and right, at 90° and 180°.
2. Door push/pull with a handle grip.
3. Pull of a heavy object.
4. Paired boost / assisted climb.
5. Paired help-up.
6. Brace a panel for a partner (M04).
7. Synchronised two-hand handle pull (M06).
8. Underhand ball roll (M02).
9. Cuffed / restrained walk and restraint search (M06).
10. Kneel-and-shim at a low fastener (M04).
11. Selector switch and brake-wheel hold (M05).
12. Block and stagger.
13. Facial performance and lip-sync for all dialogue (convert the Rocketbox facial FBX or capture).

## History

The earlier session's 19 UAL→MPFB retargets failed rendered deformation across five repair cycles, and its native sine-walk proxy was a diagnostic only. Both are superseded by this report.
