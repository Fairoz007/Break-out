# Phase 04 session state

Updated 20 October 2026. **Phase 04: IN PROGRESS / INCOMPLETE.** Branch `phase04` (stacked on `phase03`, commit
`0fb705c`, pushed to `origin/phase03`). Read with `BASELINE_AUDIT.md`, `DEFECT_QUEUE.md`, `CONFLICTS.md`,
`COMPLETION_AUDIT.md` and the Phase 03 files it builds on.

## Current milestone

Release-candidate verification: `tools/phase04_release_check.sh` (regressions, guard AI, parse check, UI walkthrough,
export, full chapter on the exported exe), then independent QA (Agent 14) on Phase 04 evidence.

## Completed (requirement groups → evidence)

- P04-BASE: baseline from the Phase 03 commit, all fresh runs green (`tests/phase04/evidence/baseline_*`, `BASELINE_AUDIT.md`).
- P04-AI: hearing + suspicion/search/alert/return state machine (`scripts/npc/guard_ai.gd`); `guard_ai_tests.json` 5/5;
  system suite 24/24; Mission 04 still completes with hearing active.
- P04-COOP-001: horizontal split option (`Settings.split_mode`, settings panel); verified through the UI walkthrough.
- P04-UI: real-click walkthrough of menu, settings, devices, New Game, pause/resume, quit, Continue (`ui_walkthrough.json`).
- P04-CHAR (texture): Adrian temple/brow/shirt, Noah chambray/boots/burn (`tools/phase04_character_textures.py`).
- P04-BUS-007: folding entry door. P04-COURT: gooseneck hoop units.
- P04-PERF: all six missions measured in real time at 1920x1080 (`perf_m0N.json`): 91–139 fps mean, p99 ≤ 13.6 ms.
- P04-QA-003: compile check of all 60 scripts (`parse_check.json`).
- Registry: `requirements.json` 1,034 rows (Phase 04 clauses + all Phase 03 rows carried as P04-C-*), audit tool.

## Blockers

- Human two-controller playthrough and audio listening review (people required).
- Hair geometry (Adrian length, cap-like shells), authored likeness/facial performance, paired-contact animation.
- Independent QA verdicts for Phase 04 not yet produced.

## Modified files (Phase 04)

`scripts/npc/guard_ai.gd`, `scripts/chapter/chapter_root.gd`, `scripts/core/settings.gd`, `scripts/ui/settings_panel.gd`,
`scripts/player/character_visual.gd`, `scripts/world/{env_intake,prison_court,env_yard}.gd`,
`assets/characters/phase04/*`, `assets/props/phase03/{hoop_gooseneck,blackridge_transport_bus_p03}.glb`,
`tools/phase03_{props_build,bus_detail,reimport}.py|sh`, `tools/phase04_*`, `tests/phase04/*`, `docs/phase04/*`.

## Next executable task

When `final_summary.txt` reads all exit=0, run the collector/registry/audit, then the independent QA review.
