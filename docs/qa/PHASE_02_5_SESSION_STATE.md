# Phase 02.5 session state

19 October 2026. **IN PROGRESS / INCOMPLETE.** Existing project and all pre-existing dirty work preserved. No commits made. Read reality audit and requirements matrix before resuming.

## Current work

- Parent owns integration, runtime, new tests, reports, export and acquisition. Specialized bus, environment and independent visual QA subagents performed the latest integration. Independent production approval remains withheld; see PHASE_02_5_INTEGRATION_QA.md.
- Gameplay repairs: separate jog3.4/sprint5.2m/s; jump; clearance-aware crouch1.1m; traversal/recovery collision reset; exclusive restored device ownership; stale input cleared. Camera retracts at close walls, sphere-sweeps cinematic return candidates on physics ticks, and lowers pivot while crouched.
- Added corrupt-save validation before enabling Continue; centered pause panel. Existing atomic save replacement remains preserved.
- Workshop floor/ceiling/rails/utilities/contact lighting and cellblock surfaces improved using existing licensed assets. This is a limited visual repair, not production realism approval.
- Fresh focused movement14/14 and save validation12/12 passed. Existing system suite24/24 passed before final camera sweep/pivot changes; repeat after final source changes. Independent checkpoint test completed fresh chapter and reconstructed all12 ordinary checkpoints from disk (13 captured including ending), all passed. This tests reconstruction before mission coroutine advances, not completion from each restored save.

## Active jobs and evidence

- Earlier normal-speed source graphical full Chapter1 (process ended without final report; NOT a passing run): `tests/phase025/evidence/full_normal_gfx.log`, report `full_normal_gfx.json`, screenshots `shots_full_normal/`. Uses virtual inputs, `--save-slot=phase025_normal_gfx`; no speed multiplier. Must await report rather than infer completion from screenshots. Do not start competing Godot render/import/export jobs.
- User additionally requested1,000 free realistic assets and selected mixed models/PBR materials. Downloader: `python tools/phase025_bulk_assets.py --target 1000 --workers 8`. Progress/inventory/failures: `asset_library/manifests/phase025_bulk_20261019/`. Acquisition COMPLETE: 335 models +665 PBR sets, 4,545 payloads /8.728GB; separate verification failed0. Complete sources: `asset_library/original_downloads/phase025_bulk_20261019/`; CC0/API evidence: `asset_library/licenses/phase025_bulk_20261019/`. Eight bounded workers, API requests spaced0.3s, official MD5/size + SHA256, dependencies validated. One provider asset counts once; component maps do not inflate totals. Acquired files are not automatically integrated into gameplay.
- Actual engine executable: `C:/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe`. Steam launcher returns early: inspect real process/explicit log/JSON completion. Leave pre-existing Project Manager PID1668 untouched.

## Valid visual comparisons

`tests/phase025/evidence/before_valid/` and `after_valid/` contain five exact matched cameras. `comparison_manifest.json` records initial/repaired source hashes. Initially clean environment scripts were temporarily restored from HEAD; repaired bytes archived and restored in finally by `tools/phase025_capture_comparison.py`. Current source is repaired. No source swap remains pending.

Earlier `before/` and `after/` captures are **INVALID**: standalone SceneTree mode failed to compile GameState in Door, causing truncated environment builders. Retained only as failed harness evidence; never use them for comparison. Corrected normal scene harness has no ERROR markers.

## Next steps

1. Latest graphical six-mission regression: tests/phase025/evidence/integration/chapter_gfx.log/json and chapter_shots/. Virtual inputs at time_scale3; await explicit report. Latest system suite integration/systems.log passed24/24. Earlier normal-speed run has no passing final report. Do not count synthetic driver as hardware playthrough.
2. Run `tests/phase025/movement_visual.tscn` for graphical animation state inspection, then graphical main-menu/New Game/pause/Continue path using actual UI. Run final system and save validation regressions sequentially.
3. Export fresh Windows build, record complete relevant source+binary hashes, run exported normal gameplay and automated chain. Keep previous build available.
4. Update reality audit, all422 requirement rows, visual audit and final report from actual evidence. Do not mark recovery complete: realistic bus/scanner/machines, exact wardrobe/identity, paired contact animation, authored facial/VO and physical two-controller acceptance remain unresolved.

## Commands

```powershell
$G = 'C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe'
& $G --headless --path . --fixed-fps 60 res://tests/phase025/gameplay_regressions.tscn
& $G --headless --path . res://tests/phase025/save_validation.tscn
& $G --headless --fixed-fps 60 --path . res://tests/phase025/checkpoint_regressions.tscn -- --save-slot=phase025_checkpoint_suite
& $G --path . res://tests/phase025/movement_visual.tscn
& $G --headless --path . --fixed-fps 60 res://tests/phase02/run_tests.tscn -- --save-slot=phase025_final_suite
python tools/phase025_bulk_assets.py --target 1000 --workers 8
```

## Latest asset integration (19 October)

- Library is complete and independently verified; only selected22 Poly Haven assets are staged in runtime (14 models,8 PBR sets). Bus additionally uses original CC0 ajanhallinta coach, authored 32-seat/cockpit/guards conversion and verified CC0 fabric_leather_02. Blender source and license records retained. All1,000 are not loaded into scenes.
- New metric28x15m court, full markings, smooth braced hoops, bolted rim brackets and woven nets. Nets merged into two meshes. Original yard floor retains sole navigation/collision surface; paint/court overlay has no collision layer. Rack relocated38,-20; confrontation bench/anchors/cameras moved north to clear court. Gameplay regression required.
- New photographed concrete/asphalt surfaces,14 detailed prop packages and restrained painted steel. Mipmaps enabled for staged PBR maps after visible aliasing was reproduced. Chapter split viewports now enable TAA plus existing2xMSAA; needs graphical/performance review.
- Valid intermediate review captures: integration/final/ (before latest door/solitary/fabric fixes), integration/verified/ (latest material/readability fixes, before TAA and pending new fence). Logs must be checked independently from PNG save success. initial/ and repaired/ have known court errors and are INVALID for court acceptance.
- Independent QA reviewed actual images; bus/court ACCEPTABLE TEMPORARY, all-environment production realism FAILED. Laundry machines, maintenance pumps, incomplete architecture, exact character fidelity/acting remain blockers. Free laundry candidates require sign-in or lack game-use permission; research recorded, no bypass.
- Environment agent preparing original Blender chain-link fence geometry to replace visibly sagging old fence; not yet integrated/tested. Bus GLB final leather seat version timestamp17:02UTC, needs latest captured run before approval.
