# Phase 02.5 visual quality audit

19 October 2026. **INCOMPLETE — production visual approval withheld.**

## Review method and reference targets

Reviewer: technical-art recovery agent. Source audit covered CharacterVisual, procedural environment builders, material resources, actual GLB animation names, character specifications, environment specifications, animation requirements, acquisition reports and historical independent QA. Runtime resource import is distinct from visible production readiness.

Institutional reference targets supplied by the lead reviewer: [NPS Alcatraz cellhouse](https://www.nps.gov/places/000/alcatraz-cellhouse.htm) and [NPS archival laundry photograph](https://www.nps.gov/media/photo/gallery-item.htm?gid=8e9e3257-155d-4519-3e625aa172220d4d&id=1D17A602-FD3D-3BAC-65E08E2FC092F33F). These concern historical prison architecture, not modern security standards. This agent has not independently opened the reference photographs; no claim of image-by-image reference approval is made. No reference image has been copied into the game.

Criteria: credible human proportions; plausible metric construction; restrained material roughness and normal intensity; readable passages and interactions; visible local lighting/contact shadows; coherent material scale; plausible equipment; absence of placeholder silhouettes; normal-speed animation transitions and feet/hand contact.

## Actual inspected evidence

- Historical `tests/phase02/evidence/shots_full_current/0003_mission_loaded_.png`: stylised faceted bus dominates the opening cinematic. **UNREALISTIC**, unresolved.
- Historical `tests/phase02/evidence/shots_windows_m03_hud/0002_checkpoint_CP03_A.png`: credible baseline Rocketbox humans, visibly primitive press machinery, noisy repeating floor and distressed teal ceiling, weak contact shadows. Characters are **ACCEPTABLE TEMPORARY**, machinery **UNREALISTIC**.
- New deterministic before captures: `tests/phase025/evidence/before/{intake,cellblock,yard,workshop,maintenance}.png`; camera transforms and dimensions recorded in `cameras.json`. All five were opened by this reviewer. Workshop shows intended room and equipment. Cellblock is a constrained cell-corner view. Maintenance is a constrained entrance view. Intake and yard show missing expected props/light contributions compared with source and historical gameplay; harness validity must be resolved before interpreting these samples as faithful appearance. Do not use these two images alone to claim before/after production approval.

## Changes awaiting graphical retest

| Area | Root cause | Implemented repair | Verification |
|---|---|---|---|
| Shared scanned materials | Full-strength normals and filtering produced excessive distant surface noise | Normal intensity 0.55; anisotropic mip filtering; explicit nonmetal concrete/asphalt | IMPLEMENTED — NOT VERIFIED |
| Workshop | Floor and ceiling material selection did not match sealed concrete/neutral lighting specification | Existing licensed 2K concrete floor and neutral concrete ceiling; neutral fluorescent color | IMPLEMENTED — NOT VERIFIED |
| Workshop enclosure | Solid blue box barriers visually read as primitive walls | Steel rail silhouette within retained safety collision envelopes | IMPLEMENTED — NOT VERIFIED |
| Workshop architecture | Large unarticulated surfaces lacked functional scale | Existing pipe modules along ceiling; low protective plinths | IMPLEMENTED — NOT VERIFIED |
| Interior depth | Insufficient contact lighting | SSAO tuning and two bounded workshop shadow keys | IMPLEMENTED — NOT VERIFIED |
| Cellblock | Teal scan dominated architecture; ordinary cells unlit | Neutral concrete and dim local cell practicals | IMPLEMENTED — NOT VERIFIED |
| Maintenance entrance | No local practical in first chase | Existing fluorescent fixture with bounded shadowed light | IMPLEMENTED — NOT VERIFIED |
| Locomotion | Sprint clip unused, jumping had no visual state | Backward-compatible grounding/vertical-speed arguments, Sprint, Jump_Start/Jump/Jump_Land transitions | IMPLEMENTED — NOT VERIFIED |

Godot strips `_Loop` from imported animation names. The first jump test exposed incorrect `Jump_Loop`; corrected to `Jump`. Runtime manifest lists `Jump_Start`, `Jump`, `Jump_Land`, and `Sprint`. Earlier failing log is retained; corrected rerun required.

## Asset readiness and unresolved gaps

| Category | Classification | Remaining gap |
|---|---|---|
| Adrian / Noah | ACCEPTABLE TEMPORARY | Rocketbox facial derivatives visibly integrated; canonical wardrobe/likeness, floor contacts and full motion review incomplete |
| Guards / prisoners | ACCEPTABLE TEMPORARY | Rusk and generic guards share one identity; crowd variety and authored work/seated actions incomplete |
| Intake bus | UNREALISTIC | No suitable realistic bus integrated; cannot be closed by material changes |
| Laundry machinery | UNREALISTIC | Simplified original press/washer silhouettes remain; realistic acquired dryer alone does not replace every machine |
| Cellblock architecture | ACCEPTABLE TEMPORARY | Basic assembled structure; upper gallery/stairs/signage/detail below intended production quality |
| Yard | ACCEPTABLE TEMPORARY | Acquired guard tower and basketball assets already integrated; lighting/collision/view acceptance pending |
| Maintenance | ACCEPTABLE TEMPORARY | Functional architecture/props present; contact choreography and production detail incomplete |
| Paired / precise interaction animation | MISSING | Generic Push/Interact substitutions do not prove paired grips, shim/handset contacts or cuff performance |
| Facial acting / audio sync | MISSING | Subtitle-driven jaw oscillation is not recorded voice, visemes or authored facial acting |

Rocketbox MIT, Quaternius CC0 and acquired material provenance remain in existing manifest/license files. No new third-party asset was downloaded during these changes. Existing Mixamo hero retarget trials have limited static-pose review only; they were not blindly promoted to gameplay.

No AAA-equivalent claim, full character readiness, full animation readiness, or production environment approval is supported. Same-camera after captures and full normal-speed two-player graphical review remain required.

## Corrected matched comparison review — lead integration pass

The standalone-script captures above are invalid. Root cause reproduced in `after_capture.log`: GameState failed to compile in Door, truncating intake, cellblock, yard and maintenance builders. Harness changed to a normal Node scene with project autoloads. `before_valid/` and `after_valid/` now contain all five complete environments with identical cameras; both valid logs have no ERROR markers. `comparison_manifest.json` records camera equality and the original/repaired environment source hashes. Current assets and renderer were held constant. Earlier captures are retained only as failed test evidence.

Lead directly opened corrected before/after workshop, yard, maintenance, plus corrected after intake/cellblock. Workshop now visibly has calm sealed concrete, a neutral ceiling, readable rail silhouette and contact shadows; primitive machine bodies still fail the realism target. Yard comparison shows minimal change and retains empty, repeated surfaces and excessive atmospheric washout. Maintenance comparison is near-identical from the puzzle-side view; added entrance practical is outside that camera and is not claimed as a visible puzzle-room upgrade. Cellblock has clearer concrete and cell lighting, but repeated rusty bars and simplified incomplete upper architecture remain below target. Intake retains over-worn floor/counter material and sparse primitive furnishings. **Production visual target FAILED**, despite a defensible limited workshop improvement.

Corrected images: `tests/phase025/evidence/{before_valid,after_valid}/{intake,cellblock,yard,workshop,maintenance}.png`. Graphical locomotion and full normal-speed screenshots remain separate evidence. New bulk CC0 asset acquisition is a library expansion; it does not automatically change these runtime environments or close any visual blocker.
