# Acquisition checkpoint — 19 October 2026

All 22 original missing bundles reconciled against current runtime files. Existing manifest retained. Prior import and visual claims are historical evidence; this audit checks file presence and recorded hashes.

| Bundle | Existing child records | Missing paths | Hash mismatches | Production | Remaining requirement |
|---|---:|---:|---:|---|---|
| CHAR_ADRIAN | 4 | 0 | 0 | PARTIAL | Facial blendshapes not exported; art-direction likeness approval; overshirt is a recoloured sweater (no layered garment); grey temple/eyebrow cut not authored; calibrated roughness from specular; close-up lighting review. |
| CHAR_NOAH | 4 | 0 | 0 | PARTIAL | Facial blendshapes not exported; likeness approval (skin darker than brief, hair not wavy); wrist burn not authored; recoloured jacket stands in for undershirt; photo-in-shirt contact. |
| CHAR_RUSK | 2 | 0 | 0 | PARTIAL | Average (not heavy) build; radio/keys/wedding band props; shares the only realistic guard identity with CHAR_GUARD. |
| CHAR_MARA | 2 | 0 | 0 | PARTIAL | Likeness mismatch: avatar is younger with dark hair (brief: 46, silver-streaked); cardigan and inspector badge missing. |
| CHAR_SILAS | 2 | 0 | 0 | PARTIAL | Uniform patches and chipped incisor not authored; facial performance. |
| CHAR_GUARD | 2 | 0 | 0 | PARTIAL | Only one realistic guard identity (shared with Rusk); radio/restraints props; more variants needed for crowds. |
| CHAR_INMATE | 3 | 0 | 0 | PARTIAL | Two realistic inmate identities; crowd variation and seated/working variants beyond shared clips. |
| PROP_PHOTO | 2 | 0 | 0 | PARTIAL | Hand contact and close-up art direction. |
| PROP_VANTAGE_BADGE | 1 | 0 | 0 | PARTIAL | Close-up legibility/art direction. |
| PROP_DIAGRAM | 1 | 0 | 0 | PARTIAL | Half-screen readability at authored camera. |
| PROP_SHIM | 1 | 0 | 0 | PARTIAL | Grip/contact and cinematic silhouette. |
| PROP_RELAY | 5 | 0 | 0 | PARTIAL | Selector lamp states, brake wheel pivot and interlock motion; grille drive animation untested. |
| PROP_LEDGER | 1 | 0 | 0 | BLOCKED | Readable close-up evidence page and later full VANTAGE ledger. |
| ENV_INTAKE | 10 | 0 | 0 | BLOCKED | Bus is a stylised exterior blockout (no interior); body scanner missing; realistic prison gate; assembled route and collision/nav. |
| ENV_CELLBLOCK | 21 | 0 | 0 | BLOCKED | Two-level assembled gallery, solitary annex, clinic envelope, hinge-pivot door motion, collision/nav. |
| ENV_YARD | 10 | 0 | 0 | BLOCKED | Watchtowers are stylised/medieval (blockout only); court markings and tray return missing; searchlight asset is a hand lantern; CC-BY hoop needs credit. |
| ENV_WORKSHOP | 12 | 0 | 1 | PARTIAL | Linen stacks/detail, ducts placement, assembled room and collision/nav; machines are simplified originals. |
| ENV_MAINTENANCE | 15 | 0 | 0 | BLOCKED | Crawlspace/service trench modules, cable trays, capture bay assembly, collision/nav; grille drive motion untested. |
| ANIM_HUMANOID | 8 | 0 | 0 | BLOCKED | 37 clips render correctly on realistic Rocketbox and UBC rigs (Blender + Godot); baseline locomotion/crouch/jump/interact/push/climb/pick-up/repair verified. Missing: turn-in-place, pull, door-specific, paired assisted climb/help-up, synchronized two-body contacts, restrained walk, facial/dialogue performance, cinematic takes; foot sliding/root motion untested. |
| AUDIO_PRISON | 596 | 0 | 0 | BLOCKED | Original VO, PA speech, crowd walla (only shouting crowd), diesel bus engine, radio speech and score missing; nothing has been listened to; mix review outstanding. |
| UI_SUBTITLES | 14 | 0 | 0 | PARTIAL | Half-screen/localized layout, accessibility and prompt composition untested. |
| VFX_ALARM | 2 | 0 | 0 | BLOCKED | Beacon light rig and particle emitter appearance in scene untested. |
