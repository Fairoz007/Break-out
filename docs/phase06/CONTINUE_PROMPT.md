# Continuation prompt — BREAKOUT: NO WAY BACK (after Phase 06 cloud session, 20 Oct 2026)

Paste everything below the line into a new Claude Code session on the Windows reference PC (RTX 2060 / Ryzen 7
5700X / Windows 11), opened in `C:\Users\LUTTA\OneDrive\Documents\break-out`.

---

BREAKOUT: NO WAY BACK — CONTINUE PHASE 05/06 ON THE REAL GPU (Windows reference PC)

Godot 4.7.2 (Steam: `C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe`),
Blender 5.1.1. Two-player split-screen co-op, Chapter 1 "Blackridge" (6 missions).

## 0. Get the code

```bash
git fetch origin claude/busy-gauss-cj4r2c
git checkout -B phase06 origin/claude/busy-gauss-cj4r2c
git lfs pull
G="/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe"
"$G" --headless --path . --import
```

Read first: `docs/phase06/SESSION_STATE.md`, `docs/phase06/DEFECT_QUEUE.md`, `docs/phase06/REQUIREMENTS_MATRIX.md`,
`docs/phase05/SESSION_STATE.md`, `docs/phase05/PERFORMANCE_REPORT.md`, `docs/phase05/HUMAN_TEST_CHECKLIST.md`,
`docs/phase06/AUDIO_QA_REPORT.md`.

The previous session ran in a Linux cloud container with **no GPU and no Windows**: everything there was verified
headless or with a software renderer. Your job is the part that needs real hardware. Do not redo work that the
docs list as verified; do not claim anything you have not run.

## 1. Secrets (first)

The two ElevenLabs free-plan keys were committed once (commit `be68b4a`) and are in git history. Ask the owner to
**rotate them** in the ElevenLabs dashboard. Put the new key(s) in `.secrets/elevenlabs.env` as
`ELEVENLABS_API_KEY=key1,key2` (the folder is git-ignored and excluded from exports) or set the environment
variable. Never print, commit or export a key.

## 2. Pending billable audio (ONLY with the owner's explicit approval in this session)

`python -I tools/phase06_elevenlabs_sfx.py --estimate` → 14 items, ~1,280 credits (music beds as sound-effect
drones — the Music API needs a paid plan; sting; laundry dryer/cart/tools/switch; tunnel drips/hum/pipe groan; bus
arrival/engine-off; cell-block day bed). After approval: run it without `--estimate`, then
`"$G" --headless --path . --import`, `python -I tools/phase06_audio_manifests.py`,
`python -I tools/phase06_audio_audit.py` (must exit 0 with no PENDING generation row). The hooks are already in
the game (they log `audio_missing` until the files exist).

## 3. Regressions (Windows)

```bash
GODOT="$G" bash tools/phase03_run_regressions.sh
"$G" --headless --fixed-fps 60 --path . res://tests/phase04/guard_ai_tests.tscn
"$G" --headless --path . res://tests/phase04/parse_check.tscn
```
Expected: gameplay 14/14, system 24/24, checkpoints 12/12, save validation all true, guard AI 6/6, parse 73/73.

## 4. Real-GPU work (the reason for this session)

1. **Export and run the Windows exe** (P06-21):
   `"$G" --headless --path . --export-release "Windows Desktop" build/windows/BreakoutNoWayBack.exe`, then the full
   chapter on the exe with screenshots:
   `build/windows/BreakoutNoWayBack.exe --resolution 1280x720 -- --autopilot --new --speed=3 --timeout=2400 --save-slot=p06_exe --report="$(pwd -W)/tests/phase06/evidence/exe_chapter.json" --shots="$(pwd -W)/tests/phase06/evidence/exe_shots"`
   plus `--chaos=mistakes` and `--chaos=idle` runs. Confirm every `dialogue_shown` has `voice: true`.
2. **Frame-time measurement** (D05-014): per mission at 1920×1080 split-screen, speed 1:
   `for m in 1 2 3 4 5 6; do build/windows/BreakoutNoWayBack.exe --resolution 1920x1080 -- --autopilot --mission=$m --until=$m --timeout=900 --save-slot=p06_perf_m0$m --report="$(pwd -W)/tests/phase06/evidence/exe_perf_m0$m.json"; done`
   Read `frame_spikes` (with monitor deltas), `wall_frame_cadence`, `gpu_frame_ms`. The Phase 04 M06 841 ms freeze
   should be gone (handcuffs GLB now preloaded); attribute every remaining in-mission spike. Target p99 ≤ 16.7 ms.
   Update `docs/phase05/PERFORMANCE_REPORT.md`.
3. **Cinematic captures on GPU** (D06-012): M04 SH03 shim insert burst, M05 SH02 handset burst, M05 gate hold,
   M02 mediation — `--mission=N --until=N --shots=... --burst=CH01_M04_CS01_SH03` etc. Review the frames.
4. **UI walkthrough** (D06-009): `"$G" --path . --resolution 1600x900 res://tests/phase04/ui_walkthrough.tscn -- --ui-out=res://tests/phase06/evidence/ui_walkthrough`.
   The graphics-dropdown step fails (popup not visible to the scripted click) and leaves the reduced-flash toggle
   unclickable; fix the test (e.g. wait for `popup.visible`, close the popup on failure) and get all steps + the
   Quit step passing.
5. **Audio on real hardware**: play M01–M06 with headphones; check ducking, reverb, spatial voices, radio bus,
   tension/chase/betrayal music switch, door sounds, footsteps on the M05 metal ramp, jaw motion following speech.
   Fill `docs/phase06/AUDIO_QA_REPORT.md` human section only with what a person actually heard.

## 5. Open defects to fix where possible

D06-010 guard insignia "SECURITY OFFICER" → corrections insignia (texture repaint); D06-011 inmates share Adrian's
overshirt (variant shirt) and scalp blotch; D05-018/019 bus exterior panels and driver area (Blender); D05-020/021
intake benches/tray and yard dirt; Adrian shoulder zigzag texture mark.

## 6. Human tests (never claim without people)

Two-controller playthrough and listening review: `docs/phase05/HUMAN_TEST_CHECKLIST.md` and
`docs/phase06/AUDIO_QA_REPORT.md`. Mark HUMAN_TEST_PENDING / HUMAN_AUDIO_REVIEW_PENDING until done.

## 7. Release gate

Phase 04 was never approved and `phase04` was never pushed. Run an independent QA review (sub-agent) over the GPU
evidence. Push the working branch after each verified step; push `phase04`/a release branch only after the
independent reviewer approves, then verify the remote commit.
