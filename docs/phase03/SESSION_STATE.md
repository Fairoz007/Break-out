# Phase 03 session state

Updated 20 October 2026. **Phase 03: INCOMPLETE** (see "Blockers"). This is the resume point; Phase 04 builds on it.
Read with `DEFECT_QUEUE.md`, `QA_REVIEW.md`, `COMPLETION_AUDIT.md`.

## Current milestone

All Phase 03 milestones have implementation and runtime evidence; independent QA approval is pending on the items in
"Blockers". Next work continues as Phase 04 (`docs/phase04/`).

## Completed (evidence)

- Playability: real-menu New Game → first objective (`tests/phase03/evidence/first_objective.json`, pass). Regression
  battery after the last engine-facing change: gameplay 14/14, save validation, system 24/24, checkpoints 12/12
  (`regress_summary.txt`, all exit 0).
- Full Chapter 1 on the **exported Windows build** (built after all fixes): `exe_chapter.json` chapter_complete,
  134 screenshots in `exe_chapter_shots/`, no script errors. Source run: `chapter_gfx.json` chapter_complete.
  Conditional dialogue: `chaos_idle.json`, `chaos_mistakes.json` (all 145 lines have runtime events).
- Performance (real time, 1920x1080 split-screen, RTX 2060 / Ryzen 7 5700X, quality 2, M01 — heaviest mission):
  91 fps mean, p99 13.6 ms, 0.1 % of frames > 16.7 ms, draw calls p50 3.9k (max 14k), VRAM ~2.5 GB (`perf_m01.json`).
- Hard-surface props (`tools/phase03_props_build.py`): washer-extractor, garment press, pump set, intake counter,
  locker, razor wire, floodlight pole, lint screen, isolation switch.
- Bus (`tools/phase03_bus_detail.py`): proportions, rotating wheels, lamps, glazing, cage partition, livery, arrival roll.
- Environments/lighting: all six areas (`env_*.gd`, helpers in `env_builder.gd`); matched captures in
  `docs/phase03/visual_evidence/` (before vs iter05/07/08).
- Fixes found by graphical review: M05 selector stall, M06 pipe stall (regression from a bunk change), invisible hand
  props (1/100 scale), camera collapsing on see-through bars (`LAYER_CAMERA`), Adrian hem texture, five cinematic
  reframes, fence distance stand-in, bus single-sided roof.
- Trailer: `build/trailer/BreakoutNoWayBack_Ch1_Trailer.mp4` (72 s, 1080p30) from `tests/phase03/trailer.tscn`.
- Requirements system: 646 rows; independent QA verdicts in `qa_verdicts.json`; audit exits 1 while incomplete.

## Blockers (why Phase 03 is INCOMPLETE)

1. Character likeness/wardrobe vs documents (D03-032) — character art; carried into Phase 04 Milestone 03.
2. Human two-controller playthrough and audio listening review (D03-034) — need people.
3. Bus doors static; court/hoops are the Phase 02.5 geometry (QA); remaining dim M04 shim insert (D03-025).
4. Mandatory requirements not yet independently VERIFIED (see `COMPLETION_AUDIT.md`).

## Modified files

`scripts/world/*`, `scripts/player/{character_visual,player_camera}.gd`, `scripts/missions/mission_0{1,3,4,5,6}.gd`,
`scripts/core/settings.gd`, `scripts/chapter/chapter_root.gd`, `project.godot`, `export_presets.cfg`,
`tests/phase02/autopilot.gd`, `tests/phase025/gameplay_regressions.gd`, `tests/phase03/*`, `tools/phase03_*`,
`assets/props/phase03/*`, `assets/props/phase15/{laundry_washer,laundry_press,pump_unit,intake_counter,locker}.glb`,
`assets/materials/phase03/*`, `assets/characters/phase03/*`, `docs/phase03/*`.

## Commands

See `LAUNCH_AND_TEST.md`.

## Next executable task

Phase 04 baseline audit (`docs/phase04/BASELINE_AUDIT.md`) from the committed Phase 03 state.
