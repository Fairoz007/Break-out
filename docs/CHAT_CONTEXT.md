# BREAKOUT: NO WAY BACK — chat context (handoff for a new session)

Written 20 October 2026 by Claude Code. Paste or point a new chat at this file. Authoritative detail lives in the docs it
links; this is the map.

## Project

- Godot 4.7.2 (Steam build: `C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe`),
  Forward+/D3D12, GDScript; Blender 5.1.1 (`C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`).
- Two-player local split-screen co-op, third person, Chapter 1 "Blackridge": six missions (New Blood, Trouble in the
  Yard, The Workshop, Lights Out, Behind the Walls, The Betrayal); 145 canonical dialogue lines, 36 camera shots,
  19 objectives, 12 checkpoints (`data/ch01/*.json`). Story bible `STORY.md`; mission specs `docs/missions/`.
- Reference machine: RTX 2060, Ryzen 7 5700X, Windows 11.

## Git state

| Branch | Commit | Remote | Contents |
|---|---|---|---|
| `main` | `f1de48a` | origin/main is 1 behind | Phase 02 |
| `phase03` | `0fb705c` | **pushed** `origin/phase03` | Phase 02.5 (Codex) + Phase 03 |
| `phase04` | `95a69eb` | **local only, not pushed** | Phase 04 baseline → QA round 1 fixes |

Remote: `https://github.com/Fairoz007/Break-out.git` (Git LFS for glb/gltf/fbx/blend/zip). Large re-creatable sources
are git-ignored (8.2 GB bulk download, Blender working copies, old screenshot folders); manifests/checksums/licences
are committed.

**Parallel work warning (07:06–07:14, 20 Oct):** a Codex session is again editing this folder, uncommitted:
`scripts/missions/mission_02.gd`, `scripts/world/{env_cellblock,env_intake,env_workshop,prison_court}.gd`, new
`assets/{characters/phase04_realistic,props/phase04_architecture,props/phase04_cellblock,props/phase04_realistic}/`,
`docs/phase04/{ARCHITECTURE_WORK,BUS_COURT_WORK,CHARACTER_ASSET_AUDIT,MATERIALS_AUDIT,REALISTIC_INDEPENDENT_QA}.md`,
`tests/phase04/evidence/realistic_*`. Coordinate before committing or editing those files.

## Status per phase

- **Phase 03 — INCOMPLETE** (audit 258 VERIFIED / 40 FAILED / 19 BLOCKED of 646). Resume point:
  `docs/phase03/SESSION_STATE.md`; `DEFECT_QUEUE.md`, `QA_REVIEW.md`, `LAUNCH_AND_TEST.md`.
- **Phase 04 — INCOMPLETE, release candidate NOT APPROVED** by independent QA (second review: 540 VERIFIED /
  67 FAILED / 49 BLOCKED of 656 judged rows; registry has 1,034 rows incl. all Phase 03 rows carried as `P04-C-*`).
  Resume point: `docs/phase04/SESSION_STATE.md`; `BASELINE_AUDIT.md`, `CONFLICTS.md`, `DEFECT_QUEUE.md`,
  `QA_REVIEW.md` (first + second review), `VISUAL_QUALITY_REPORT.md`, `LAUNCH_AND_TEST.md`, `COMPLETION_AUDIT.md`.

## What works (evidence-backed)

- Real main-menu New Game → first objective; regressions (gameplay 14/14, system 24/24, save validation, checkpoints
  12/12); compile check of all scripts; guard AI 6/6 (hearing, suspicion→search→return, alert/chase, walls block
  sight, independent per-player detection).
- Full Chapter 1 on the **exported Windows build** (`build/windows/BreakoutNoWayBack.exe`, 1.45 GB, git-ignored)
  via the virtual-input autopilot: chapter_complete, 134 screenshots, no errors, no stuck events.
- Failure/retry paths (`--chaos=mistakes`: M04 detection → CP04_A reload, wrong selector, early lever release, missed
  distraction) and idle barks (`--chaos=idle`).
- Exe real-time performance per mission at 1920x1080 split-screen: 88–139 fps, p99 9.0–14.2 ms (one unexplained
  841 ms freeze in M06).
- UI walkthrough through real clicks: settings (horizontal split, slider), devices, credits, New Game, pause,
  resume, Restart, quit, Continue. Horizontal (top/bottom) split option; vertical stays default (CONFLICTS C1).
- Visual work: Blender hard-surface props (washer, press, pumps, counter, lockers, isolation switch, lint screen,
  razor wire, floodlights, gooseneck hoops); bus (proportions, rotating wheels, lamps, glazing, cage, folding door,
  rear bars, CC0 licence record); lighting (AgX, SSAO+SSIL, volumetric fog, soft shadows); environment finishes;
  character texture pass (Adrian temple/brow/V-neck shirt, Noah recolour/boots/burn).
- 72 s trailer: `build/trailer/BreakoutNoWayBack_Ch1_Trailer.mp4` (`tests/phase03/trailer.tscn`).

## Open blockers (from QA second review)

1. Human two-controller playthrough and audio listening review (people required).
2. Characters vs documents: Adrian's hair long (doc: short), sweater not overshirt; Noah still a denim jacket, burn hidden
   by the cuff; cap-like hair on both — needs garment/hair geometry.
3. Cinematics: M06 SH04 Noah still standing on "On your knees" (`final_exe_shots/0127`); M04 SH03 shim unreadable
   (`0079`); M05 SH02 handset hidden by the hand (`0101`).
4. Staging: M05 gate — hand at lock not visible (`0094/0095`); M02 — Silas out of both views (`0040`).
5. Dialogue: CH01_M04_DLG022 now fires in no run (narrow trigger, `mission_04.gd` ~l.262); the 12 conditional lines
   only appear in headless runs (no on-screen evidence).
6. Untested: M01 wrong-interaction bark, M06 reload-during-cutscene rule, some UI controls (Quit, Change device,
   Auto-detect, graphics dropdown).
7. Bus exterior still flat white panels; driver area illegible. Environments outside the court unchanged in Phase 04.
8. Docs to correct: VISUAL_QUALITY_REPORT overshirt/"salt-and-pepper" wording; `cmp_char01b/c/e/f` BEFORE panels;
   credits screen shows draft text; `ui_walkthrough/` has stale first-run frames.

## Key tools and commands

```bash
G="/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe"
bash tools/phase03_reimport.sh                 # after adding textures/models (mipmaps, VRAM, normal maps)
bash tools/phase04_release_check.sh            # regressions, guard AI, parse, UI, chaos runs, captures, export, exe chapter, exe perf
bash tools/phase04_baseline.sh                 # fresh baseline evidence
python -I tools/phase04_collect_evidence.py && python -I tools/phase04_requirements.py && python -I tools/phase04_completion_audit.py
"$G" --path . res://tests/phase03/visual_capture.tscn -- --output=res://docs/phase04/visual_evidence/<set>
"$G" --path . --resolution 1280x720 -- --autopilot --new --speed=3 --timeout=2400 --save-slot=x --report=res://tests/phase04/evidence/x.json --shots=res://tests/phase04/evidence/x_shots
```

Blender builders: `tools/phase03_props_build.py` (props, hoop), `tools/phase03_bus_detail.py` (bus),
`tools/phase04_uv_raycast.py` + `tools/phase04_character_textures.py` (character textures),
`tools/phase03_adrian_hem_fix.py`.

## Working conventions used so far

- Run one Godot job at a time (GPU contention); wrap Godot runs in `timeout` (a compile error otherwise hangs the harness).
- New textures need `tools/phase03_reimport.sh` (Godot imports them without mipmaps by default).
- VERIFIED is set only from an independent QA verdict file (`docs/phase0N/qa_verdicts.json`) whose reviewer is not the
  owner; the collectors set at most IMPLEMENTED_UNTESTED.
- Autopilot = real movement/interactions through virtual devices (no completion flags), but it knows target
  positions and chapter runs use time scale 3 — not a substitute for the human playtest.
- Commit on a feature branch, not `main`; user asked to push finished phases to `origin`.

## Next steps

1. Coordinate with the Codex session's uncommitted `phase04_realistic` work (review/merge before further edits).
2. Fix QA blockers 3–8, rerun `tools/phase04_release_check.sh`, request a third QA pass.
3. Push `phase04` to origin; open a PR into `main` when the user wants.
4. Arrange the human two-controller playthrough + audio listening review.
