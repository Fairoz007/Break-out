# Phase 02.5 reality audit

19 October 2026. **INCOMPLETE — initial forensic review; fresh runtime review pending.** This report classifies evidence conservatively. WORKING applies only to the narrow independently repeated check. Existing source, exported binaries and logged events do not establish human playability or production art acceptance.

## Independently established facts

- Canonical export check rerun: `python -I tools/phase02_export_data.py --check` succeeds with 145 dialogue lines, 36 shots, six missions, 19 objectives and no drift. Full screenplay contains exactly the same 145 dialogue ID set; camera register the same 36 shot IDs. Text/blocking/performance acceptance is separate.
- `python -I tests/phase02/test_completion_audit.py`: four tests pass. These validate bookkeeping safeguards, not gameplay.
- Prior Phase02 explicitly says INCOMPLETE: 305 requirements, ten VERIFIED, 290 IMPLEMENTED_UNTESTED, five BLOCKED. The premise that all prior phases were completed conflicts with the actual reports.
- Existing Windows build and export preset exist. All eight recorded source hashes matched the existing `tests/phase02/evidence/windows_build_manifest.json` before recovery changes. The manifest covers only eight files, not the complete source tree.
- Godot executable exists: `C:/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe`. Blender executable exists: `C:/Program Files/Blender Foundation/Blender 5.1/blender.exe`.
- Existing `full_current_gfx.json` records chapter_complete, 429.675 real seconds and 133 captures at speed3. Existing `export_run.json` is headless, 29.534 seconds, zero screenshots. These are not fresh normal-speed full exported graphical acceptance.

## Feature reality classification

| Feature | Status | Actual evidence / missing proof |
|---|---|---|
| Canonical runtime data counts/ID sets | WORKING | Independently repeated export drift and ID-set checks above |
| Completion bookkeeping safeguards | WORKING | Four focused Python tests; no gameplay claim |
| Existing project launch/menu/New Game | NOT TESTED | Source entry exists; fresh graphical button path pending |
| Walking/jog/crouch/gravity/collision | PARTIALLY WORKING | Code and old virtual-device suite; fresh physical input and believable motion pending |
| Separate running versus sprint speed | MISSING | Initial Player has WALK1.5/JOG3.4/CROUCH0.8 only; no distinct sprint state |
| Jump/landing | MISSING | Initial device ACTIONS omits jump; Player has no jump impulse. Available animation clip is not implemented jumping |
| Crouch physical clearance | PARTIALLY WORKING | Initial crouch changes speed/clip but capsule remains1.8m; low-ceiling/stand tests needed |
| Recovery during scripted traversal | BROKEN | Initial recover clears scripted path without restoring collision_mask, which traverse sets0; source-proven collision-loss risk |
| Camera collision | PARTIALLY WORKING | SpringArm exists but forced0.45m minimum can push camera beyond a closer obstacle; scalar distance test cannot approve wall clipping |
| Independent split-screen/shared world | PARTIALLY WORKING | Two viewports/devices and old narrow tests; fresh graphical exclusive physical input pending |
| Interaction/objective/mission chain | PARTIALLY WORKING | Six mission scripts,19 objectives and prior virtual full runs; fresh authored full chain pending |
| Guard/NPC behavior | PARTIALLY WORKING | Existing source and limited detection/escort tests; routes/occlusion/restore review pending |
| Pause/disconnect/settings | NOT TESTED | Source and old suite exist; fresh interactive path pending |
| Checkpoints/save/load | PARTIALLY WORKING | Prior generic save/CP04_A tests; exact all12 checkpoint restore coverage absent |
| Characters/rigs/locomotion | PARTIALLY WORKING | Real Rocketbox 3D assets and clips; pose/motion/likeness/contact acceptance incomplete |
| Paired/contact animation | MISSING | Generic Push/Interact/OverhandThrow substitutions do not establish authored aligned actions |
| Facial acting/voice synchronization | MISSING | Blendshape derivatives exist; sine jaw/random blink do not provide authored visemes; original VO absent |
| Canonical dialogue display | PARTIALLY WORKING | Correct145 runtime register; fresh all-line triggers/timing and optional/retry paths pending |
| Cinematic shots/blocking | PARTIALLY WORKING |36 registered shots and old activation samples; moving framing/contact acceptance absent |
| Realistic prison environment | PARTIALLY WORKING | PBR/3D modules coexist with blockout construction; production-ready visual approval absent |
| PBR/material/lighting support | PARTIALLY WORKING | Materials/render configuration present; matched current screenshots and compatibility/performance review pending |
| Windows export | PARTIALLY WORKING | Existing1.13GB executable/manifest; refreshed build and runtime after recovery pending |
| 1080p60/performance | NOT TESTED | Speed3 or fixed-step headless metrics cannot certify target frame rate |
| Full current Chapter1 human playthrough | NOT TESTED | Automated internal virtual driver is not two hardware-controlled humans |

## Prioritized defects and credible verification

1. P1: Missing jump and distinct sprint, fixed crouch capsule, recover collision restoration. Gameplay agent owns repairs; QA must test actual movement and edge states.
2. P1: Camera minimum-distance logic can override collision retraction. Multiplayer/camera agent owns repair; test thin walls/corners at close range in both views.
3. P1 acceptance gap: fresh menu-to-ending normal-speed graphical playthrough, exclusive input and all six mission dependency gates.
4. P1 visual gap: older reports themselves retain realism/paired contact/VO blockers. Screenshot capture and authored motion review are mandatory; imported meshes alone cannot close them.
5. P1 acceptance gap: all12 checkpoint exact restoration, final exported graphical runtime and meaningful performance capture.
6. P2 documentation inconsistencies: mission headers claim no implementation despite runtime scripts; README/manifest usable counts differ; old blocker prose predates facial derivatives. Current acceptance must use actual asset references and evidence, not stale labels.

Every defect follows inspect → reproduce → root cause → fix → retest → regression, with no more than five repair attempts per defect. This initial audit does not count historical corrections as new repair attempts.

## Reproducible commands and evidence limits

Use unique save slots/evidence paths. Only one engine/import/render job at a time until the lead clears parallel work.

```powershell
$G = 'C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe'
& $G --path .
& $G --headless --path . --fixed-fps 60 res://tests/phase02/run_tests.tscn -- --save-slot=phase025_qa_suite
& $G --headless --fixed-fps 60 --path . -- --autopilot --new --save-slot=phase025_qa --report=tests/phase02/evidence/phase025_full.json --timeout=4000
& $G --path . -- --autopilot --new --save-slot=phase025_gfx --report=tests/phase02/evidence/phase025_gfx.json --shots=tests/phase02/evidence/shots_phase025 --timeout=4000
& $G --headless --path . --export-release 'Windows Desktop' build/windows/BreakoutNoWayBack.exe
```

The virtual autopilot reads internal enabled interaction/meta state and navigation paths, plus HUD guides. This is useful progression regression but gives the driver more information than a player. Existing24 system tests cover only one checkpoint restore, narrow camera distance, selected solo gates and synthetic input ownership; no jump/landing, animation quality or hardware completion. A normal graphical launch with menu button activation remains separate from `--autopilot`, which bypasses the menu choice.

## Document corpus inventory

All files below were byte-read for inventory and screened for status/blocker/design sections; core reports, canonical registers, mission sequence source and test harnesses received targeted review. This is documentary evidence only. CP1252 fallback is recorded for legacy files; no originals changed. Hashes are SHA256 prefixes of the pre-recovery corpus and establish which version was examined. No standalone Phase01 report exists beyond PREPRODUCTION_REVIEW and asset reports in this inventory.

| File | Lines | Decode | SHA256 prefix |
|---|---:|---|---|
| `README.md` | 143 | UTF-8 | `81c5a16fa18e6a76` |
| `STORY.md` | 443 | UTF-8 | `4cceee54f7e78911` |
| `GAME_DESIGN.md` | 17 | UTF-8 | `8242ed16a9fd10c8` |
| `DEVELOPMENT_PLAN.md` | 34 | UTF-8 | `08340cb14db19ff5` |
| `ASSET_MANIFEST.md` | 53 | UTF-8 | `874784e6024a53e4` |
| `docs/assets/acquisition_20261019_RESEARCH.md` | 49 | UTF-8 | `8fb4fbd503a16b93` |
| `docs/assets/ASSET_GAPS.md` | 30 | UTF-8 | `53ad3f7b94e433f6` |
| `docs/assets/ASSET_LICENSES.md` | 7 | UTF-8 | `69d04aacd59f023f` |
| `docs/assets/ASSET_REQUIREMENTS.md` | 30 | UTF-8 | `8e78718cf1794a63` |
| `docs/assets/ASSET_SOURCES.md` | 14 | UTF-8 | `611d021b856270fa` |
| `docs/assets/ASSET_VALIDATION_REPORT.md` | 47 | UTF-8 | `7c81b3f0dcdfb861` |
| `docs/assets/followup_20261019_ARCHITECTURE_RESEARCH.md` | 25 | UTF-8 | `73b3679fb6578dd7` |
| `docs/assets/PHASE15_BULK_ACQUISITION.md` | 39 | UTF-8 | `d0086cd056aeb2ed` |
| `docs/assets/PHASE15_DISCOVERY.md` | 139 | UTF-8 | `de425c397f677fda` |
| `docs/assets/THIRD_PARTY_NOTICES.md` | 61 | UTF-8 | `bf9dd501590c1a36` |
| `docs/chapters/CHAPTER_01_BLACKRIDGE.md` | 43 | UTF-8 | `6788eab697dd2167` |
| `docs/chapters/CHAPTER_02_NIGHT_SHIFT.md` | 40 | UTF-8 | `4aef8dfa6974d5fa` |
| `docs/chapters/CHAPTER_03_OTHER_SHORE.md` | 40 | UTF-8 | `af06fba45486e091` |
| `docs/chapters/CHAPTER_04_GHOSTS_OF_THE_CITY.md` | 40 | UTF-8 | `612b0a4be3eb9dd6` |
| `docs/chapters/CHAPTER_05_THE_SHIPMENT.md` | 40 | UTF-8 | `b6e0b869bc932160` |
| `docs/chapters/CHAPTER_06_TRUTH_BELOW.md` | 40 | UTF-8 | `9f0722635cfe92f5` |
| `docs/chapters/CHAPTER_07_NO_WAY_BACK.md` | 40 | UTF-8 | `a3f14ff467999b8f` |
| `docs/characters/ADRIAN_CROSS.md` | 51 | UTF-8 | `add2c67f9b85cfd6` |
| `docs/characters/CHARACTER_RELATIONSHIPS.md` | 21 | UTF-8 | `44cf049e4dd4f4f0` |
| `docs/characters/ELENA_REYES.md` | 51 | UTF-8 | `52835c0da1a5af51` |
| `docs/characters/GUARDS_AND_NPCS.md` | 126 | UTF-8 | `1e4bf35b39034d53` |
| `docs/characters/NOAH_REYES.md` | 51 | UTF-8 | `d6bfd4dc28bd1b72` |
| `docs/environments/CELL_BLOCK.md` | 31 | UTF-8 | `849762c5eecba63d` |
| `docs/environments/LAUNDRY_WORKSHOP.md` | 11 | UTF-8 | `1e9cc55f22da02c7` |
| `docs/environments/MAINTENANCE_NETWORK.md` | 14 | UTF-8 | `302b6ce986d78796` |
| `docs/environments/PRISON_INTAKE.md` | 24 | UTF-8 | `65d7e5634c297e9c` |
| `docs/environments/PRISON_YARD.md` | 19 | UTF-8 | `c1950340c3592d43` |
| `docs/missions/CH01_MISSION_01.md` | 104 | UTF-8 | `064af8795753ab97` |
| `docs/missions/CH01_MISSION_02.md` | 108 | UTF-8 | `2229aa3c85a546bf` |
| `docs/missions/CH01_MISSION_03.md` | 110 | UTF-8 | `82ad5ede016501ca` |
| `docs/missions/CH01_MISSION_04.md` | 104 | UTF-8 | `b2fc2a8449ac3502` |
| `docs/missions/CH01_MISSION_05.md` | 110 | UTF-8 | `c2ad7ac06d37f598` |
| `docs/missions/CH01_MISSION_06.md` | 117 | UTF-8 | `7272d0b6b58a098f` |
| `docs/PHASE_02_REQUIREMENTS_MATRIX.md` | 472 | UTF-8 | `05af1792ac64c016` |
| `docs/PHASE_02_SESSION_STATE.md` | 76 | UTF-8 | `b62443b8c495bed2` |
| `docs/qa/acquisition_20261019_QA.md` | 88 | UTF-8 | `c37fe68e5aed6196` |
| `docs/qa/ACQUISITION_20261019_REPORT.md` | 103 | UTF-8 | `061760ba0a1846ef` |
| `docs/qa/ANIMATION_VALIDATION.md` | 67 | UTF-8 | `fcee242a924d51ab` |
| `docs/qa/ASSET_COVERAGE_MATRIX.md` | 222 | UTF-8 | `91749460f90cbaa2` |
| `docs/qa/AUDIO_MATERIALS_AUDIT.md` | 204 | UTF-8 | `7b002126d73369ae` |
| `docs/qa/BLOCKERS.md` | 40 | UTF-8 | `d2678cfb3d0ac3ec` |
| `docs/qa/CHARACTER_RIG_VALIDATION.md` | 69 | UTF-8 | `4624fd5b0194ec7c` |
| `docs/qa/MIXAMO_20261019_QA.md` | 31 | UTF-8 | `4027ed7d4ad12d5b` |
| `docs/qa/MIXAMO_20261019_REPORT.md` | 27 | CP1252 fallback | `f350732b3d4ec05b` |
| `docs/qa/PHASE15_INDEPENDENT_REVIEW.md` | 81 | UTF-8 | `f7a530295b727cae` |
| `docs/qa/PHASE_01_5_REPORT.md` | 106 | UTF-8 | `66a916d1274dd150` |
| `docs/qa/PHASE_02_COMPLETION_AUDIT.md` | 355 | UTF-8 | `20b2171435426e26` |
| `docs/qa/PHASE_02_INDEPENDENT_REVIEW.md` | 55 | UTF-8 | `fea958cc9d0cded7` |
| `docs/qa/PREPRODUCTION_REVIEW.md` | 46 | UTF-8 | `68191621013fbd25` |
| `docs/qa/PRISON_ARCHITECTURE_VALIDATION.md` | 230 | UTF-8 | `d0cfc7b3f316e753` |
| `docs/qa/SCENE_COMPLETENESS_MATRIX.md` | 140 | UTF-8 | `c19540ca29641fb8` |
| `docs/screenplay/CH01_CAMERA_SHOTS.md` | 84 | UTF-8 | `bdc405b236290df9` |
| `docs/screenplay/CH01_CHARACTER_BLOCKING.md` | 140 | UTF-8 | `f5cc58d303c24f98` |
| `docs/screenplay/CH01_CUTSCENES.md` | 116 | UTF-8 | `b01edc2dea0346c8` |
| `docs/screenplay/CH01_DIALOGUE.md` | 302 | UTF-8 | `ad199fd4674fb519` |
| `docs/screenplay/CH01_FULL_SCRIPT.md` | 926 | UTF-8 | `76cd14b9b4368e5d` |
| `docs/technical/ANIMATION_REQUIREMENTS.md` | 21 | UTF-8 | `81b23aca95fcb026` |
| `docs/technical/COOP_REQUIREMENTS.md` | 16 | UTF-8 | `e5631074dbb4ca04` |
| `docs/technical/GODOT_ASSET_PIPELINE.md` | 16 | UTF-8 | `b6f1e59a140558a5` |
| `docs/technical/SCENE_ARCHITECTURE.md` | 17 | UTF-8 | `5157bb61c9ad05cd` |

## Authored mission-gate source review (initial)

These are implemented gates, not a completed playtest. No completion jump was found in the reviewed normal mission run paths.

| Mission | Required implemented sequence | Negative/regression checks still needed |
|---|---|---|
| M01 New Blood | Both property/inspection marks → Adrian badge + Noah receipt → both acknowledge → escort → each cell and sink/door interactions → pipe exchange/cinematic → next mission | Wrong actor, one observer missing, escort gap, CP01_B resume |
| M02 Yard | Both enter court → confrontation → P1 hold mediation enables P2 ball → moving distraction/guard response → both alcove → stance acknowledgements → both exit | Early mediation release resets opportunity, solo ball refusal, CP02_B resume |
| M03 Workshop | Ask Mara → Rusk lamp errand → P1 isolation hold enables P2 screen → P2 lamp reveals separate halves → P1 diagram read → replace screen/collect shim → closing cinematic → physical handoff | Early lever release resets hold, lamp release, correct owner, CP03_B resume |
| M04 Lights Out | Count cinematic → shim panel → P1 scripted crawl/unlatch → P1 brace admits P2 crawl → P2 hatch hold admits P1 → flush both panels → patrol-safe crossing → both restricted gate | Detection retries CP04_A, patrol/crouch occlusion, interrupted traverse, CP04_B resume |
| M05 Behind Walls | Gate → split → both handsets → P2 brake + P1 selector B + power → grille latch → reunion → evidence inspection → both final handles | Wrong selector trips/reset, no brake, independent information, CP05_B resume |
| M06 Betrayal | Simultaneous correctly owned handles → count → authored capture/confiscation → solitary → P1 three knocks then P2 reply → canonical dialogue → completion save/end | Solo handle refusal, release/reacquire, P2 cannot answer first, CP06_B resume, completion save load |

New `tests/phase025/checkpoint_regressions.tscn` captures actual disk snapshots during fresh input-driven progression and reconstructs each of 12 saves. It is prepared but NOT RUN pending lead engine-job clearance. Its deliberately narrow assertions compare mission, both transforms/crouch, flags, inventory, knowledge, consumed dialogue, transaction/objective sets and patrol immediately before resumed mission coroutines advance. It does not prove that every restored mission subsequently completes.

## Recovery source changes observed — runtime verification pending

The gameplay owner has now added distinct SPRINT5.2, JUMP_SPEED4.4, standing/crouching capsule heights and an overhead shape check. Recovery calls `_cancel_traversal()` restoring BODY_MASK and clears callbacks; camera minimum logic now respects shorter SpringArm collision. These corrections address the initial source findings, but remain **IMPLEMENTED — NOT VERIFIED** until fresh targeted tests and graphical motion review. The initial classification table deliberately records original defects rather than silently erasing them.

Residual review item: camera cinematic blend interpolates from the prior shot to collision-safe target; intermediate blend positions can still cross intervening walls. No graphical approval is claimed.
