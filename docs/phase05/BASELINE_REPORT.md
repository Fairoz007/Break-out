# Phase 05 baseline report

Written 20 October 2026, 07:20 (local) by Claude Code. Read-only audit; nothing launched yet.

## Repository state

| Item | Value |
|---|---|
| Branch | `phase04` |
| HEAD | `95a69eb` (= the reported Phase 04 checkpoint; verified with `git log`) |
| Remote | `phase04` **not pushed**; `origin/phase03` = `0fb705c`; `origin/main` is 1 behind local `main` (`f1de48a`) |
| Uncommitted | 7 modified tracked files + new asset folders/docs/tools from a **Codex session that is still running** (`codex.exe` live; files written up to 07:15) |

### Uncommitted work by the parallel Codex session (not authored here, not yet reviewed)

- `scripts/missions/mission_02.gd`: basketball → `assets/props/phase04_realistic/basketball_recessed_channels.glb`.
- `scripts/world/env_cellblock.gd`: `_bed()` hides the old bed mesh, keeps its box collision, and adds `phase04_architecture/prison_bunk.glb`; upper-tier doors become `phase04_cellblock/tier_security_door.glb`.
- `scripts/world/{env_intake,env_workshop,prison_court}.gd`: asset swaps (dryers, ironing station, court/bus detail).
- New: `assets/{characters/phase04_realistic,props/phase04_architecture,props/phase04_cellblock,props/phase04_realistic}/`,
  `docs/phase04/{ARCHITECTURE_WORK,BUS_COURT_WORK,CHARACTER_ASSET_AUDIT,MATERIALS_AUDIT,REALISTIC_INDEPENDENT_QA,ASSET_COVERAGE_MATRIX,REALISTIC_ASSET_REQUIREMENTS}.md`,
  `tests/phase04/evidence/realistic_*`, `tools/phase04_{architecture,bus_court,cell_hardware,character_acquisition}_*`, `data/credits.txt`.
- Its own visual review (`REALISTIC_INDEPENDENT_QA.md`) verdict: **INCOMPLETE**. It confirms the new cell tier doors and dryers
  as real improvements, finds no bus or court gain, and **rejects** its Mixamo pull/door retarget trials (crossed arms).

## Phase 04 independent QA, second pass

**NOT APPROVED** (`docs/phase04/QA_REVIEW.md`, "Second review"). 656 judged rows: **540 VERIFIED, 67 FAILED, 49 BLOCKED**
(`qa_verdicts.json`). All 116 non-verified rows are listed in `_open_rows.txt`. None of them is treated as done in Phase 05.

### Open defects by area (from the second review)

| Area | Defect | Evidence |
|---|---|---|
| Characters | Adrian's hair is long (doc says short); cap-like hair shells on both leads; a hair-card shard; sweater instead of an overshirt; temple reads as blotches | `iter02/adrian_*`, CHAR-004/007/008/009 |
| Characters | Noah still wears a recoloured denim trucker jacket; the cuff hides the wrist burn | `iter02/noah_wrist.png`, CHAR-010 |
| Cinematics | M06 SH04: Noah stands on "On your knees" | `final_exe_shots/0127` |
| Cinematics | M04 SH03: shim insert too dark to read | `0079` |
| Cinematics | M05 SH02: the handset reads as a hand to the head | `0101` |
| Staging | M05 gate: hand at the lock not visible, Adrian faces the corridor | `0094/0095` |
| Staging | M02: Silas is outside both viewports | `0040` |
| Animation | Pull is a reversed Push; no climb staged; no motion review exists (most ANIM rows BLOCKED) | ANIM-014/015 |
| Dialogue | CH01_M04_DLG022 fires in no run; 12 conditional lines seen only headless | `mission_04.gd:262` |
| Failure paths | M01 wrong-interaction bark and M06 reload-during-cinematic are untested | MIS-01-009, MIS-06-009 |
| Bus | Flat white exterior, no wheel wells, driver area illegible, no material response | BUS-001/008/010 |
| Environments | Intake benches and tray are slabs; yard is bare dirt and the wall reads tan | ENV-INTAKE-008, ENV-YARD-001/002 |
| Performance | 841 ms stall in M06 (exe); spikes 106–841 ms unexplained; no GPU frame time or bottleneck analysis | `exe_perf_m06.json`, PERF-001/004/008 |
| UI | Quit, Change device, Auto-detect, graphics dropdown and toggles never pressed; Credits shows draft text | UI-004/006/011 |
| Camera | No test for camera rotation by look input | PLAY-009 |
| Co-op | No solo-configuration cutscene run | CIN-011 |
| Evidence hygiene | Stale overshirt/salt-and-pepper wording; blank BEFORE panels; mixed ui_walkthrough frames | QA-003/014, PROC-002/003 |
| Human | No two-controller playthrough and no audio listening | COOP-004/005, AUD-001..009, CIN-008 |

### Verified and holding (do not redo)

Guard AI hearing/suspicion/search/alert/chase (6/6); horizontal split; M04 snag fix; chaos failure/retry flows; bus doors,
rear bars, dimensions and CC0 licence; exe per-mission performance (88–139 fps, p99 9.0–14.2 ms); export excludes
`tests/phase025|03|04`; extended UI walkthrough; compile check (59 scripts); regressions (gameplay 14/14, system 24/24,
checkpoints 12/12); full Chapter 1 on the exported exe via the virtual-input autopilot.

## Reference

Godot 4.7.2 (Steam), Forward+/D3D12; Blender 5.1.1; RTX 2060, Ryzen 7 5700X, Windows 11.
