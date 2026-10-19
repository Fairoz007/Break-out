# Phase 03 character and animation source audit

19 October 2026. Source acquisition and read-only inspection only. No runtime edits or Godot jobs. Read STORY.md, ASSET_MANIFEST.md, CHARACTER_RIG_VALIDATION.md, ACQUISITION_20261019_REPORT.md and MIXAMO_20261019_REPORT.md before downloading.

## Existing verified files

`characters_existing_verification.json` records fresh SHA256/bytes for six facial actor GLBs and fourteen Mixamo FBXs. Every Mixamo source matches its historical checksum and has a valid FBX Binary header. Each current acquisition_20261019 facial actor GLB contains **80 joints, 37 animations and 175 facial targets**. Historical documentation saying facial targets are absent does not apply to these later derivatives. Targets do not supply performed dialogue.

| Character | Prior validated height | Suitability and remaining gaps |
|---|---:|---|
| Adrian, Male_Adult_02 | 1.84m | Rig candidate; recoloured sweater replaces layered shirt/overshirt; temple grey, eyebrow scar, likeness and close-up review missing. |
| Noah, Male_Adult_12 | 1.78m | Rig candidate; jacket replaces undershirt; hair/skin likeness, wrist burn and photo contact missing. |
| Rusk, Security_Male_01 | 1.83m | Same identity as generic guards; heavy-build brief, age and radio/cuff/wedding-chain props need work. |
| Mara, Medical_Female_01 | 1.67m | Younger/dark-haired than canonical46/silver-streaked brief; cardigan/badge and facial performance missing. |
| Silas, Male_Adult_11 | 1.80m | Uniform/teeth detail and performed dialogue unfinished. |
| Inmate, Male_Adult_14 | 1.79m | Additional crowd identities and seated/working activity needed. |

Heights are prior validated configuration values, not newly repeated graphical measurements. This task verified existing file structure and checksums. Foot sliding, blend transitions, contacts and in-game lighting remain graphical QA work.

## Official sources and legal decisions

[Microsoft Rocketbox](https://github.com/microsoft/Microsoft-Rocketbox) publishes115 avatars and417 motions under [MIT](https://github.com/microsoft/Microsoft-Rocketbox/blob/master/LICENSE.md). The notice is preserved beside new payloads and must ship with the game.

[Adobe Mixamo FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) permits royalty-free commercial video-game use and requires an Adobe ID. Existing14 authenticated sources cover door opening/cabinet closing,90degree turns, heavy pulling, kneeling and body conversation gestures. No existing files were downloaded again. No login bypass or unofficial mirror used. They do not supply paired choreography or final facial acting.

## New cleared acquisitions

**26 payload files,136,243,963 bytes: one new guard identity (base/facial variants plus textures/preview),10 motion takes and MIT license.** Texture channels and base/facial variants do not inflate asset counts.

Source root: `asset_library/original_downloads/phase03/characters_animations/microsoft_rocketbox/`.

Exact commit-pinned source URLs, measured SHA256, bytes and official Git blob hashes are recorded in `new_acquisition_inventory.json` and CSV beside sources. Every file matches official Git content hash and size. `official_tree.json` pins the repository tree; `new_blender_source_validation.json` records source import evidence. No previously verified asset was redownloaded.

### Additional guard

`Assets/Avatars/Professions/Security_Female_01/`: both FBX variants imported in Blender5.1.1;80bones, one mesh, facial variant175targets. Source Blender XYZ bound dimensions **1.2173 x0.3386 x1.7388m**; minimumZ approximately -0.000855m. Width includes A-pose arms. Official source preview visually inspected: believable woman in fitted dark security uniform/cap, suitable additional crowd candidate. Not an approved Rusk replacement. Diffuse/normal/specular textures preserved. Needs calibrated PBR conversion, floor grounding, prison insignia, animation transfer and Godot graphical review.

### Targeted motion sources

| Take | Main body frame range | Evaluation purpose |
|---|---:|---|
| m_documents_check.max.fbx | 1-484 | Intake/evidence paperwork |
| m_documents_note.max.fbx | 1-303 | Guard/medical notes |
| m_documents_take.max.fbx | 1-151 | Paper handoff reference |
| m_knock_door.max.fbx | 1-241 | Cell-door knock |
| m_listen_door.max.fbx | 1-251 | Stealth listening |
| m_sit_chair_idle_look_around.max.fbx | 1-261 | Bus/intake seated activity |
| m_sit_chair_idle_nervous_01.max.fbx | 1-1335 | Prisoner seated activity |
| m_sit_down_chair_01.max.fbx | 1-88 | Seat entry |
| m_sit_stand_up_chair_01.max.fbx | 1-76 | Seat exit |
| m_gestic_talk_sad_01.max.fbx | 1-971 | Conversation body reference |

All10 imported successfully: one121bone armature each and three action records (Bip01 body, footsteps, motion extraction helper). These are10 performances, not30. They require body-action filtering,121-to-80bone mapping, rest alignment and extraction/root policy. No mesh dimensions apply to animation-only sources. No new take has been retargeted or certified contact-ready.

## Requirements tracker

| ID | Requirement | Status | Next concrete work |
|---|---|---|---|
| CHAR03-01 | Adrian wardrobe/age/scars | BLOCKED on authored character work | Fit layered garment and details on licensed rig, verify deformation. |
| CHAR03-02 | Noah shirt/hair/burn/photo | BLOCKED on authored character work | Correct garment/hair/wound texture, stage photo sockets. |
| CHAR03-03 | Guard diversity | SOURCE ACQUIRED, NOT INTEGRATED | Evaluate new female guard, preserve Rusk identity. |
| CHAR03-04 | Inmate diversity | PARTIAL | Select additional unused official identities against art direction before more downloads. |
| ANIM03-01 | Bus/intake seating | SOURCE ACQUIRED, NOT INTEGRATED | Retarget seated reference takes at exact seat height and review full motion. |
| ANIM03-02 | Paper/door acting | SOURCE ACQUIRED, NOT INTEGRATED | Retarget takes, then hand targets against actual props. |
| ANIM03-03 | Paired climb/help-up/dual handles | BLOCKED on choreography | Author synchronized two-actor actions at real anchors. Single-body generic clips cannot close it. |
| ANIM03-04 | Cuffing/restrained walk/capture | BLOCKED on source or authoring | Authenticated Mixamo reference search possible; cuff spacing and paired guard contact still need staged authoring. |
| ANIM03-05 | Facial performance | PARTIAL channels, performance missing | Author visemes/emotion against canonical dialogue and final VO. |
| ANIM03-06 | Feet/root/blending | NOT TESTED this pass | Full-motion Godot graphical tests with turns, steps, collisions and both players. |

Acquisition improves candidate coverage; it does not certify runtime playability or production readiness.
