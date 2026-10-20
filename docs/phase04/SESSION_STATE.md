# Phase 04 session state

## Latest realistic-asset session — 20 October 2026

**INCOMPLETE.** Latest authoritative asset scope is in REALISTIC_ASSET_REQUIREMENTS.md,
ASSET_ACQUISITION_REPORT.md, ASSET_COVERAGE_MATRIX.md and
`asset_library/manifests/phase04_realistic_assets.csv`. Older release-candidate notes below are retained history.

Integrated new coach chassis, true perforated/chain-net hoops, smooth recessed-seam ball, detailed upper-tier
security doors, two acquired industrial dryers, separated ironing station and original detailed single beds.
Corrected court asphalt repeat. Original colliders/mission anchors retained; workshop comparison is exact.
Preserved existing unrelated uncommitted work. No new purchases, external uploads or third-party downloads.

Evidence: `visual_evidence/realistic_before`, `realistic_after`, `realistic_details`, `realistic_comparisons`;
`tests/phase04/evidence/realistic_*`. Blender sources/build scripts, source licenses and SHA256 records are
adjacent to the new runtime assets. Rejected character trials stay excluded from Godot; canonical cast unchanged.

Final accepted validation: parse63/63; movement/camera14/14; source and newly exported Windows executable
both reached chapter_complete with zero resource/script errors and zero autopilot_stuck events. Sixteen
current environment captures and five detail captures completed without errors. Seven GLB integrity checks
and original dryer ZIP CRC passed. `realistic_validation.json` reports validation_pass=true and
production_complete=false. Initial graphical run and one capture/export iteration are REJECTED in that JSON:
they exposed a bed import failure, now corrected. Do not reuse their chapter_complete as acceptance.

Windows build: `build/windows/phase04_realistic/BreakoutNoWayBack.exe` (1,503,705,048 bytes), SHA256
`7af9e1dfc5f88a1e07f7197c4e5c00a8626defa2e751b7858007e1d516075604`.
81 asset requirement groups:47 INTEGRATED,22 MISSING,9 BLOCKED,3 CONVERTED,0 production-VERIFIED.
The 135-reference runtime index is an audit aid, not an exhaustive per-node visual approval. Independent
review confirms local improvements; no whole-scene production approval. Full human two-controller/animation/audio
acceptance is unperformed. Protagonists, contact animations, bus finish/cabin, two-tier bunks, washers,
fixtures and complete environment realism remain unresolved. **Do not mark Phase04 complete.**

Reproduce imports with the documented Steam Godot executable and `--headless --editor --path . --import`.
Use `tests/phase03/visual_capture.tscn` with `-- --output=<folder>` for matched environments;
`tests/phase04/realistic_detail_capture.tscn` for hardware/ball detail. Run
`python tools/phase04_realistic_manifest.py` after final captures for checksums/matrix/comparison sheets.
Run `python tools/phase04_realistic_verify.py` to audit current accepted and rejected test evidence.
The next-candidate library review is in NEXT_ASSET_CANDIDATES.md; a scanned old bed frame is reusable after
fit/LOD work, but no existing superior sink/toilet/scanner/bus payload qualified. No pending agents or jobs.

## Earlier Phase04 state (retained)

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
