# Phase 04 baseline audit

20 October 2026. Baseline = commit `0fb705c` (branch `phase03`, pushed to `origin/phase03`), the recoverable checkpoint
before Phase 04 modifications. Fresh evidence produced by `tools/phase04_baseline.sh` → `tests/phase04/evidence/baseline_*`
(the export step already included the new split-screen setting, default unchanged). Earlier reports were not trusted:
every row below cites a run made for this audit. Hardware: RTX 2060, Ryzen 7 5700X, Windows 11, Godot 4.7.2 Forward+/D3D12.

Classification: WORKING (fresh test shows it) · PARTIAL (works with a recorded gap) · BROKEN · MISSING · NOT_TESTED.

| System | Class | Evidence | Gap |
|---|---|---|---|
| Project imports | WORKING | `baseline_import.log`, 0 error lines | — |
| Main menu opens | WORKING | `baseline_first_objective_shots/01_main_menu.png` | — |
| New Game (real button click) | WORKING | `baseline_first_objective.json` pass, 28.7 s to first objective complete | — |
| Both players spawn | WORKING | `baseline_exe_shots/` M01–M06 mission_loaded frames; regression `floor_detected` | — |
| Movement (walk/jog/sprint/crouch/jump), collision | WORKING | `regress_gameplay.log` 14/14, `regress_system_suite.log` movement_speeds, wall_collision | Feel not judged by a human |
| Split-screen | WORKING | system `split_screen_world`; every exe frame shows two views | Horizontal layout option new (C1), not yet tested |
| Independent input | WORKING | system `device_exclusive`, `simultaneous_movement`, `input_between_physics_ticks` | Two physical controllers untested |
| Mission objectives | WORKING | `baseline_exe.json`: all 19 objectives, chapter_complete | Autopilot (virtual input, speed 3) |
| Characters animate | PARTIAL | clip events + screenshots | Likeness/wardrobe vs character docs; cap-like hair; no authored contact animation |
| Guard AI | PARTIAL | system `guard_detection_and_cover`; Phase 04 additions tested separately (`guard_ai_tests.json`) | Hearing/search/alert added in Phase 04 |
| Cutscenes play | WORKING | 36/36 shot_activated in `baseline_exe.json` | Several framings still under QA review |
| Save/load, checkpoints | WORKING | `regress_checkpoints.log` 12/12, `regress_save_validation.log` | Continue-after-corrupt-save UI path BLOCKED in Phase 03 QA |
| Crashes | WORKING | `baseline_exe.log` 0 error lines over a full chapter | — |
| Windows export exists and runs | WORKING | `baseline_export.log`; `baseline_exe.json` chapter_complete, 134 frames | Exported run is automated |
| Bus | PARTIAL | `docs/phase04/visual_evidence/baseline/bus*.png` | Doors static |
| Basketball court | PARTIAL | `baseline/court_layout.png`, `hoop_detail.png` | Phase 02.5 hoop geometry; plain backboards |
| Environments | PARTIAL | `baseline/*.png` (32 captures) | See Phase 03 QA FAILED rows |
| Audio | NOT_TESTED | cue log only | Listening review needs a person |
| Performance | PARTIAL | Phase 03 `perf_m01.json` (91 fps mean, p99 13.6 ms) | Only M01 measured |
| Human two-player playthrough | NOT_TESTED | — | Needs two people |

Exported-build frame cadence during the automated run (speed 3, 1280x720 window, two 958x1080 views): M01 79, M02 113,
M03 94, M04 114, M05 123, M06 125 fps.
