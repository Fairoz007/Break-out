# Animation requirements

All clips are production requirements; availability and actual skeleton compatibility are controlled by manifest ANIM_HUMANOID. No animation is validated merely by this list. Character specifications live under [characters](../characters/CHARACTER_RELATIONSHIPS.md). Scale target1.7–1.9m adults with individual canonical proportions; do not stretch a shared skeleton to hide differences.

Rig contract: single humanoid root→hips→spine/chest/neck/head, clavicles, upper/lower arms, hands, upper/lower legs, feet/toes. Fingers required for photo/shim/relay hero shots; facial blendshapes or jaw/eye controls required for close dialogue. Record source bone names and explicit retarget map; compatible humanoid label alone is insufficient. One reference T/A-pose per rig, neutral scale1, no negative scale. Root motion defaults off for navigation locomotion; authored contact clips may use controlled root motion with endpoint markers. Two-player interactions synchronize semantic events rather than assume clip lengths equal.

| Set | Required clips and contacts | Used scenes |
|---|---|---|
| Base | idle, walk forward/back/strafe, turn90/180, start/stop, crouch idle/walk, listen/peek, sit/stand | all |
| Intake | seated transport, restrained escort, hands-open search, property handover, badge look, sink/door inspect | M01 |
| Yard | threatening lean, mediation palms, glance, ball roll with foot/hand contact defined by selected asset, withdraw, conversation | M02 |
| Workshop | lever hold/release, screen open/clear/replace, lamp hold, diagram point/read, scrap shim palm, concealed handoff, linen inspection | M03 |
| Night | patrol walk/turn, barred lookout, shim rear fastener, panel open/close, crouch chase, hatch hold and handoff | M04 |
| Maintenance | ladder mount/climb/dismount, handset lift/talk/replace, brake hold, selector turn, energize press, gate pass, ledger inspect, recording listen | M05 |
| Capture | dual handle pull, alarm flinch, guarded surrender, restrained escort, confiscation, solitary sit, three pipe knocks/reply | M06 |

Facial/emotional layers: Adrian controlled suspicion→protectiveness; Noah guarded grief→uncertain hope; Rusk clipped authority→visible hesitation; Mara clinical restraint; Silas intimidation without slapstick. Dialogue duration follows screenplay estimates; lip sync/voice recording remains unacquired. Do not accelerate body clips to force whole sentences into short shots.

Contact acceptance: fixed prop grip markers, hand IK blend in/out; feet on floor at varied canonical heights; no shoulder penetration at bars; ladder hands/feet aligned; gate releases safe before root motion. Contact tolerance target3cm is a test target, not measured result. Validate each clip at normal and slow playback, loop seams, root displacement, foot sliding, skinning extremes, elbows, wrists, face and camera framing. Record rendered evidence and actual duration. Confirm retargeted poses on Adrian AND Noah; no single-rig blanket PASS. Blend proposed0.15–0.25s locomotion,0.1s hand contacts after testing. Shared actions have ready/active/release/interrupted states; interruption returns safe posture before a machine changes state.

Gaps: custom two-person door/dual handles, precise shim/finger contacts, facial acting, guard restraint, Mara clinical inspection and pipe knock are likely custom capture/animation tasks. Free generic locomotion cannot satisfy these performances. [Pipeline](GODOT_ASSET_PIPELINE.md), [mission index](../../README.md).
