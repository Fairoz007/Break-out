# Phase 04 character and animation audit

Date: 20 October 2026. Result: INCOMPLETE. This audit inspected actual GLB headers, mesh index counts, skins, animation names and material definitions. It also visually inspected the existing Godot captures `docs/phase04/visual_evidence/iter02/adrian_close.png` and `noah_close.png`. These are historical baseline captures, not newly rendered proof. No character replacement was integrated by this audit.

## Runtime reuse decision

`scripts/player/character_visual.gd` loads the six facial Rocketbox derivatives below. GUARD and RUSK share the same model. These are recognisable human models with believable anatomy, facial geometry, clothing folds and skinned hands. They are usable candidates for medium-distance gameplay. They do not satisfy the requested final cinematic quality: Adrian retains long swept hair and an orange sweater; Noah retains jacket seams and chest pockets; hair reads as a solid cap, faces lack modern skin response, and likeness/garment corrections are still required. Recolouring these assets again would not solve the geometry deficiencies.

No specific separate prison officer or workshop staff model is wired in the model dictionary. Do not claim dedicated coverage from the generic guard/inmate aliases.

## License and originals

Official source: https://github.com/microsoft/Microsoft-Rocketbox . Individual source families are Adult Male 02 (Adrian), Adult Male 12 (Noah), Adult Male 11 (Silas), Adult Male 14 (inmate), Security Male 01 (Rusk/guard), and Medical Female 01 (Mara). Original FBX and facial FBX files are preserved under `asset_library/original_downloads/phase15_discovery/microsoft_rocketbox/`. The repository MIT license was rechecked against https://github.com/microsoft/Microsoft-Rocketbox/blob/master/LICENSE.md ; local notice is `asset_library/licenses/phase15_discovery/microsoft_rocketbox/LICENSE.md`. Preserve the Microsoft copyright and MIT notice in distribution. The repository describes its own meshes as relatively low poly; more animation or textures do not make them an ultra-realistic replacement.

The bulk Phase 02.5 inventory is predominantly environment models/materials and is not an alternative source of protagonist humans. Earlier MPFB candidates were explicitly rejected after repeated retarget and garment deformation failures (`asset_library/manifests/phase15_characters_records.json`); do not reactivate them as quality upgrades. UBC candidates are also earlier evaluation alternatives, not approved final characters.

## Actual payload inspection

| Runtime file | Triangles | Joints | Clips | Facial targets | Materials / normal maps | Status |
|---|---:|---:|---:|---:|---:|---|
| `assets/characters/acquisition_20261019/rocketbox_facial/rb_adrian_cross.glb` | 7312 | 80 | 37 | 175 | 3 / 2 | INTEGRATED, not VERIFIED |
| `assets/characters/acquisition_20261019/rocketbox_facial/rb_mara_sen.glb` | 8328 | 80 | 37 | 175 | 3 / 2 | INTEGRATED, not VERIFIED |
| `assets/characters/acquisition_20261019/rocketbox_facial/rb_noah_reyes.glb` | 6722 | 80 | 37 | 175 | 2 / 2 | INTEGRATED, not VERIFIED |
| `assets/characters/acquisition_20261019/rocketbox_facial/rb_prisoner_npc.glb` | 6842 | 80 | 37 | 175 | 2 / 2 | INTEGRATED, not VERIFIED |
| `assets/characters/acquisition_20261019/rocketbox_facial/rb_silas_bell.glb` | 6740 | 80 | 37 | 175 | 2 / 2 | INTEGRATED, not VERIFIED |
| `assets/characters/acquisition_20261019/rocketbox_facial/rb_tomas_rusk.glb` | 9515 | 80 | 37 | 175 | 3 / 3 | INTEGRATED, not VERIFIED |

## Animation coverage and blockers

The runtime has locomotion, crouch, jumping, sitting, picking up, push, climb and reaction candidate clips. Presence of tracks proves data availability only. Existing independent QA (`docs/phase04/QA_REVIEW.md`, characters section) fails reversed Push used as Pull, missing visible climb proof, cooperative hands touching nothing, and dialogue staging facing a wall. Those require contact staging and actual motion review, not additional downloads.

Sixteen Mixamo animation sources were already downloaded on 19 October. They include actual door opening/closing, heavy pull start/loop/stop, lever, kneeling, pointing, arguing and turns. Originals, checksums and license records are in `asset_library/manifests/mixamo_20261019/inventory.csv` and `asset_library/licenses/mixamo_20261019/LICENSE_RECORD.md`. Official usage FAQ: https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html . These are commercial game dependencies under Adobe's terms, not CC0 or an asset pack for redistribution. Two actual skeleton retarget trial GLBs exist below; they are not wired into the game. Their rendered poses do not constitute full contact/locomotion validation. Preserve the canonical tested rig until trials are reviewed through full motion.

| Trial file | Clips | Status |
|---|---:|---|
| `asset_library/converted/mixamo_20261019/retarget_trials/male_adult_01_mixamo_evaluation.glb` | 6 | CONVERTED, motion/contact review required |
| `asset_library/converted/mixamo_20261019/retarget_trials/rb_adrian_cross_mixamo_evaluation.glb` | 14 | CONVERTED, motion/contact review required |
| `asset_library/converted/mixamo_20261019/retarget_trials/rb_noah_reyes_mixamo_evaluation.glb` | 14 | CONVERTED, motion/contact review required |

## Replacement priority

1. Adrian and Noah: detailed garment geometry, hair and PBR skin. Preserve 80-joint Biped bone names or explicitly retarget all 37 clips and hand attachments. No suitable new licensed drop-in model was approved in this audit.
2. True pull and door clips: reuse existing acquired trials; fit hands to actual handles and replay gameplay/cinematic motion before promotion.
3. Cooperative assistance, vault and carry contacts: acquire or author task-specific motion and validate both participants and prop trajectories together.
4. Officer and workshop staff variety: explicit role-specific models remain missing; aliasing a guard does not close those requirements.

No purchase, access bypass or unverified asset was introduced. Further character work remains necessary for acceptance.

## Reproducible integrity evidence

Run `python tools/phase04_character_acquisition_audit.py` to regenerate this report. SHA-256 values and animation names are below; hashes establish payload identity, not visual or legal approval.

```json
{
  "runtime": [
    {
      "path": "assets/characters/acquisition_20261019/rocketbox_facial/rb_adrian_cross.glb",
      "sha256": "37f03c19a48c6ff054c55cfeb1914cf5f991920edca28e6bee0a87595cd2a2f4",
      "bytes": 41185312,
      "triangles": 7312,
      "joints": 80,
      "animations": [
        "Idle_Loop",
        "Walk_Loop",
        "Jog_Fwd_Loop",
        "Sprint_Loop",
        "Crouch_Idle_Loop",
        "Crouch_Fwd_Loop",
        "Jump_Start",
        "Jump_Loop",
        "Jump_Land",
        "Interact",
        "PickUp_Table",
        "Push_Loop",
        "Fixing_Kneeling",
        "Sitting_Enter",
        "Sitting_Idle_Loop",
        "Sitting_Exit",
        "Sitting_Talking_Loop",
        "Idle_Talking_Loop",
        "Punch_Jab",
        "Punch_Cross",
        "Hit_Chest",
        "Hit_Head",
        "Walk_Formal_Loop",
        "Roll",
        "Death01",
        "ClimbUp_1m",
        "Chest_Open",
        "Hit_Knockback",
        "Idle_FoldArms_Loop",
        "Idle_No_Loop",
        "Yes",
        "Idle_Rail_Loop",
        "Idle_TalkingPhone_Loop",
        "LayToIdle",
        "Walk_Carry_Loop",
        "OverhandThrow",
        "Consume"
      ],
      "morphs": 175,
      "materials": 3,
      "normal_maps": 2
    },
    {
      "path": "assets/characters/acquisition_20261019/rocketbox_facial/rb_mara_sen.glb",
      "sha256": "38c1bec6eab0be95c633a00a264782438e5bb53d4b2439501db1b046dbac2bf4",
      "bytes": 45925768,
      "triangles": 8328,
      "joints": 80,
      "animations": [
        "Idle_Loop",
        "Walk_Loop",
        "Jog_Fwd_Loop",
        "Sprint_Loop",
        "Crouch_Idle_Loop",
        "Crouch_Fwd_Loop",
        "Jump_Start",
        "Jump_Loop",
        "Jump_Land",
        "Interact",
        "PickUp_Table",
        "Push_Loop",
        "Fixing_Kneeling",
        "Sitting_Enter",
        "Sitting_Idle_Loop",
        "Sitting_Exit",
        "Sitting_Talking_Loop",
        "Idle_Talking_Loop",
        "Punch_Jab",
        "Punch_Cross",
        "Hit_Chest",
        "Hit_Head",
        "Walk_Formal_Loop",
        "Roll",
        "Death01",
        "ClimbUp_1m",
        "Chest_Open",
        "Hit_Knockback",
        "Idle_FoldArms_Loop",
        "Idle_No_Loop",
        "Yes",
        "Idle_Rail_Loop",
        "Idle_TalkingPhone_Loop",
        "LayToIdle",
        "Walk_Carry_Loop",
        "OverhandThrow",
        "Consume"
      ],
      "morphs": 175,
      "materials": 3,
      "normal_maps": 2
    },
    {
      "path": "assets/characters/acquisition_20261019/rocketbox_facial/rb_noah_reyes.glb",
      "sha256": "e2b5fe1c580ba0e97f390af5c82a963667867d9c7c0cc07329c69063e832307b",
      "bytes": 35542380,
      "triangles": 6722,
      "joints": 80,
      "animations": [
        "Idle_Loop",
        "Walk_Loop",
        "Jog_Fwd_Loop",
        "Sprint_Loop",
        "Crouch_Idle_Loop",
        "Crouch_Fwd_Loop",
        "Jump_Start",
        "Jump_Loop",
        "Jump_Land",
        "Interact",
        "PickUp_Table",
        "Push_Loop",
        "Fixing_Kneeling",
        "Sitting_Enter",
        "Sitting_Idle_Loop",
        "Sitting_Exit",
        "Sitting_Talking_Loop",
        "Idle_Talking_Loop",
        "Punch_Jab",
        "Punch_Cross",
        "Hit_Chest",
        "Hit_Head",
        "Walk_Formal_Loop",
        "Roll",
        "Death01",
        "ClimbUp_1m",
        "Chest_Open",
        "Hit_Knockback",
        "Idle_FoldArms_Loop",
        "Idle_No_Loop",
        "Yes",
        "Idle_Rail_Loop",
        "Idle_TalkingPhone_Loop",
        "LayToIdle",
        "Walk_Carry_Loop",
        "OverhandThrow",
        "Consume"
      ],
      "morphs": 175,
      "materials": 2,
      "normal_maps": 2
    },
    {
      "path": "assets/characters/acquisition_20261019/rocketbox_facial/rb_prisoner_npc.glb",
      "sha256": "643572be1fe3c85723bb771b2fd329d5e7a8db20e11724b17b614c526b04ffa7",
      "bytes": 35354736,
      "triangles": 6842,
      "joints": 80,
      "animations": [
        "Idle_Loop",
        "Walk_Loop",
        "Jog_Fwd_Loop",
        "Sprint_Loop",
        "Crouch_Idle_Loop",
        "Crouch_Fwd_Loop",
        "Jump_Start",
        "Jump_Loop",
        "Jump_Land",
        "Interact",
        "PickUp_Table",
        "Push_Loop",
        "Fixing_Kneeling",
        "Sitting_Enter",
        "Sitting_Idle_Loop",
        "Sitting_Exit",
        "Sitting_Talking_Loop",
        "Idle_Talking_Loop",
        "Punch_Jab",
        "Punch_Cross",
        "Hit_Chest",
        "Hit_Head",
        "Walk_Formal_Loop",
        "Roll",
        "Death01",
        "ClimbUp_1m",
        "Chest_Open",
        "Hit_Knockback",
        "Idle_FoldArms_Loop",
        "Idle_No_Loop",
        "Yes",
        "Idle_Rail_Loop",
        "Idle_TalkingPhone_Loop",
        "LayToIdle",
        "Walk_Carry_Loop",
        "OverhandThrow",
        "Consume"
      ],
      "morphs": 175,
      "materials": 2,
      "normal_maps": 2
    },
    {
      "path": "assets/characters/acquisition_20261019/rocketbox_facial/rb_silas_bell.glb",
      "sha256": "aeffef6da2ec2f70ee057c939dd9fc97c388cd3b20eaf3fcbd11d487f0dd35fd",
      "bytes": 34969616,
      "triangles": 6740,
      "joints": 80,
      "animations": [
        "Idle_Loop",
        "Walk_Loop",
        "Jog_Fwd_Loop",
        "Sprint_Loop",
        "Crouch_Idle_Loop",
        "Crouch_Fwd_Loop",
        "Jump_Start",
        "Jump_Loop",
        "Jump_Land",
        "Interact",
        "PickUp_Table",
        "Push_Loop",
        "Fixing_Kneeling",
        "Sitting_Enter",
        "Sitting_Idle_Loop",
        "Sitting_Exit",
        "Sitting_Talking_Loop",
        "Idle_Talking_Loop",
        "Punch_Jab",
        "Punch_Cross",
        "Hit_Chest",
        "Hit_Head",
        "Walk_Formal_Loop",
        "Roll",
        "Death01",
        "ClimbUp_1m",
        "Chest_Open",
        "Hit_Knockback",
        "Idle_FoldArms_Loop",
        "Idle_No_Loop",
        "Yes",
        "Idle_Rail_Loop",
        "Idle_TalkingPhone_Loop",
        "LayToIdle",
        "Walk_Carry_Loop",
        "OverhandThrow",
        "Consume"
      ],
      "morphs": 175,
      "materials": 2,
      "normal_maps": 2
    },
    {
      "path": "assets/characters/acquisition_20261019/rocketbox_facial/rb_tomas_rusk.glb",
      "sha256": "c8d5fcdedb50292ba698f974988f233038e0774faf5eb901eb8879145214137f",
      "bytes": 49936320,
      "triangles": 9515,
      "joints": 80,
      "animations": [
        "Idle_Loop",
        "Walk_Loop",
        "Jog_Fwd_Loop",
        "Sprint_Loop",
        "Crouch_Idle_Loop",
        "Crouch_Fwd_Loop",
        "Jump_Start",
        "Jump_Loop",
        "Jump_Land",
        "Interact",
        "PickUp_Table",
        "Push_Loop",
        "Fixing_Kneeling",
        "Sitting_Enter",
        "Sitting_Idle_Loop",
        "Sitting_Exit",
        "Sitting_Talking_Loop",
        "Idle_Talking_Loop",
        "Punch_Jab",
        "Punch_Cross",
        "Hit_Chest",
        "Hit_Head",
        "Walk_Formal_Loop",
        "Roll",
        "Death01",
        "ClimbUp_1m",
        "Chest_Open",
        "Hit_Knockback",
        "Idle_FoldArms_Loop",
        "Idle_No_Loop",
        "Yes",
        "Idle_Rail_Loop",
        "Idle_TalkingPhone_Loop",
        "LayToIdle",
        "Walk_Carry_Loop",
        "OverhandThrow",
        "Consume"
      ],
      "morphs": 175,
      "materials": 3,
      "normal_maps": 3
    }
  ],
  "retarget_trials": [
    {
      "path": "asset_library/converted/mixamo_20261019/retarget_trials/male_adult_01_mixamo_evaluation.glb",
      "sha256": "e936f4bad2452ba1492ef0d5a49d9f590b6de5f492d93dcd5540b4268f3d2e17",
      "bytes": 26537412,
      "triangles": 7440,
      "joints": 80,
      "animations": [
        "opening_door_inwards",
        "pull_heavy_object",
        "pull_heavy_object_start",
        "pull_heavy_object_stop",
        "pulling_lever",
        "unarmed_turn_left_90"
      ],
      "morphs": 0,
      "materials": 3,
      "normal_maps": 2
    },
    {
      "path": "asset_library/converted/mixamo_20261019/retarget_trials/rb_adrian_cross_mixamo_evaluation.glb",
      "sha256": "b7f24858cbb440e2237593a8e8ba2e31f733eb3b1ba32f42371339f360e50ead",
      "bytes": 41014664,
      "triangles": 7312,
      "joints": 80,
      "animations": [
        "closing",
        "kneeling_down",
        "kneeling_inspecting",
        "open_door_outwards",
        "opening_door_inwards",
        "pointing_forward",
        "pull_heavy_object",
        "pull_heavy_object_start",
        "pull_heavy_object_stop",
        "pulling_lever",
        "standing_arguing",
        "talking",
        "unarmed_turn_left_90",
        "unarmed_turn_right_90"
      ],
      "morphs": 175,
      "materials": 3,
      "normal_maps": 2
    },
    {
      "path": "asset_library/converted/mixamo_20261019/retarget_trials/rb_noah_reyes_mixamo_evaluation.glb",
      "sha256": "5925a35817fd6877a213c1eeb254bfded8de59073a24e79ebc737dccd419df3c",
      "bytes": 35371732,
      "triangles": 6722,
      "joints": 80,
      "animations": [
        "closing",
        "kneeling_down",
        "kneeling_inspecting",
        "open_door_outwards",
        "opening_door_inwards",
        "pointing_forward",
        "pull_heavy_object",
        "pull_heavy_object_start",
        "pull_heavy_object_stop",
        "pulling_lever",
        "standing_arguing",
        "talking",
        "unarmed_turn_left_90",
        "unarmed_turn_right_90"
      ],
      "morphs": 175,
      "materials": 2,
      "normal_maps": 2
    }
  ]
}
```

## New Blender 5.1.1 motion review, 20 October

Rendered actual Adrian and Noah retarget trial skeletons at 10%, 50% and 90% of Pull Heavy Object and Opening Door Inwards (12 new images) using `tools/phase04_character_acquisition_motion.py`. Evidence: `assets/characters/phase04_realistic/inspection/`. Existing pull trial has a raised crossed knee and unsuitable stance, while door clips lack staged handle contacts. These trials are REJECTED for production integration.

A second isolated retarget attempt removed the additional rest swing from the world-delta transfer (`tools/phase04_character_acquisition_retarget.py`). Actual re-imported multi-phase renders in `assets/characters/phase04_realistic/inspection_fixed/` show crossed arms and the same raised-knee stance. This experiment also FAILED visual review. Rejected GLBs are preserved in `assets/characters/phase04_realistic/evaluation/` for reproducibility, with `.gdignore` to prevent accidental runtime import; they are not production character assets. No canonical animation or gameplay code was changed. Need a constrained retarget solution, foot planting and actual door/lever choreography before promotion.
