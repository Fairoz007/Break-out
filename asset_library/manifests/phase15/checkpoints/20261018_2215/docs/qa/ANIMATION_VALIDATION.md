# Animation validation — Phase 01.5

Date: 18 October 2026. Readiness: **BLOCKED for project characters**.

Quaternius Universal Animation Library standard editions 1 and 2 were downloaded through the author's official itch.io distribution. Source archives and source-page CC0 license evidence are preserved. Four runtime GLBs contain UAL1 and UAL2 in-place and root-motion variants under `assets/animations/phase15/`. Count clips by unique source animation, excluding repeated T-poses and duplicate RM variants. Do not count the same 19 clips embedded in four character derivatives as 76 acquired animations.

19 experimental retargeted actions were embedded in each character export. `asset_library/manifests/phase15_characters_repair.json` records durations; Blender FPS is 24. Its historical PARTIALLY_VERIFIED action labels describe baked-file presence, not visual acceptance. The current aggregate outcome is FAILED on rendered deformation (see character report).

| Requirement | Available source / attempted clip | Acceptance |
|---|---|---|
| Idle | Idle_Loop | BLOCKED retarget |
| Walk | Walk_Loop | FAILED visual deformation |
| Run | Jog_Fwd_Loop | BLOCKED retarget |
| Sprint | Sprint_Loop | BLOCKED retarget |
| Crouch idle | Crouch_Idle_Loop | BLOCKED retarget |
| Crouch walk | Crouch_Fwd_Loop | BLOCKED retarget |
| Jump | Jump_Start | BLOCKED retarget |
| Land | Jump_Land | BLOCKED retarget |
| Turn | No dedicated accepted clip | BLOCKED |
| Pick up | PickUp_Table | BLOCKED retarget |
| Open door | Interact is generic, door match untested | BLOCKED |
| Repair | Fixing_Kneeling | BLOCKED retarget |
| Push | Push_Loop | BLOCKED retarget |
| Pull | No accepted dedicated clip | BLOCKED |
| Sit | Sitting_Enter / Sitting_Idle_Loop | BLOCKED retarget |
| Stand | Sitting_Exit | BLOCKED retarget |
| Machinery | Interact generic, lever alignment untested | BLOCKED |
| Assisted climb | Missing paired animation | BLOCKED |
| Help up | Missing paired animation | BLOCKED |
| Heavy-object movement | Push_Loop is not paired heavy-object animation | BLOCKED |
| Synchronized interaction | No contact-aligned pair | BLOCKED |
| Punch | Punch_Jab | BLOCKED retarget |
| Block | Missing accepted dedicated clip | BLOCKED |
| Stagger | No accepted dedicated clip | BLOCKED |
| Hit reaction | Hit_Chest | BLOCKED retarget |
| Talking | Idle_Talking_Loop | BLOCKED retarget |
| Looking around | No accepted dedicated clip | BLOCKED |
| Emotional reactions | No accepted face/body performance | BLOCKED |
| Restrained walking | Walk_Formal_Loop is not cuffed-walk acceptance | BLOCKED |

Root translation was intentionally not transferred in the experimental retarget; this is not proof of correct root motion. Raw source `_RM` files preserve author variants. Loop seams, foot sliding, blend transitions, finger contacts, facial performance, paired contacts and Godot playback on accepted protagonists remain unverified. No gameplay animation controller was implemented.

Follow-up: cycle 5 produced one original native-rig walk diagnostic, `asset_library/converted/phase15_characters/cycle5/native_walk_proxy.glb`. This is not sourced from UAL. Native render shows improved anatomy and uniform surface visibility but stiff arm posture and no full baseline set. It does not resolve any required animation acceptance row above. Cycles 3 and 4 of UAL retargeting also failed rendered arm deformation. Five repair cycles are exhausted; source libraries remain available for a qualified retarget/rebind pass.

Two coordinator-requested prototype exports P15_PROXY_ADRIAN and P15_PROXY_NOAH contain the single original native walk only. They do not contain the 19 failed UAL retarget clips. They support diagnosis of resource loading and basic native-rig deformation, and do not satisfy the full idle/walk/run/crouch animation requirements. Critical readiness remains BLOCKED.
