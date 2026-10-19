# BREAKOUT: NO WAY BACK — launch and testing instructions (Phase 03)

Engine: Godot 4.7.2 (Steam build), Forward+ / Direct3D 12. Reference machine for the recorded numbers: NVIDIA GeForce
RTX 2060, Windows 11 Pro (see `tests/phase03/evidence/perf_*.json` for CPU, window size and quality).

```bash
G="/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe"
```

## Play

- Editor: open the project in Godot 4.7.2 and press Play (main scene `res://scenes/main.tscn`).
- Command line:

```bash
"$G" --path .
```

- Exported build: `build/windows/BreakoutNoWayBack.exe` (not in git; produce it with the export command below).

Controls (default ownership): P1 Adrian = keyboard + mouse (WASD, mouse look, E interact, Space jump, C crouch,
Shift sprint); P2 Noah = first controller, otherwise the right keyboard cluster (IJKL, O interact). Change devices in
Main menu → Controls and devices. Graphics quality: `Settings.graphics_quality` 0–2 (user://settings.cfg), or
`--quality=0|1|2` after `--` on the command line.

## Automated checks (run one Godot job at a time)

| Check | Command | Pass condition |
|---|---|---|
| Import (after new assets) | `bash tools/phase03_reimport.sh` | finishes; `.import` files have mipmaps/VRAM compression |
| Regression battery | `bash tools/phase03_run_regressions.sh` | gameplay 14/14, save 12 checks true, system 24/24, checkpoints 12/12 (see `tests/phase03/evidence/regress_*.log`) |
| Real menu → first objective | `"$G" --path . res://tests/phase03/first_objective.tscn -- --save-slot=p03_first_objective` | `tests/phase03/evidence/first_objective.json` `"pass": true` |
| Full chapter, graphical | `"$G" --path . --resolution 1280x720 -- --autopilot --new --speed=3 --timeout=2400 --save-slot=p03_chapter_gfx --report=res://tests/phase03/evidence/chapter_gfx.json --shots=res://tests/phase03/evidence/chapter_gfx_shots` | report `reason` = `chapter_complete` |
| Conditional dialogue | `"$G" --headless --fixed-fps 60 --path . -- --autopilot --new --speed=4 --chaos=idle` (and `--chaos=mistakes`) with `--report=` | `chapter_complete`; idle/retry lines shown |
| One mission | add `--mission=N --until=N` to the chapter command | `until_reached` |
| Environment captures | `"$G" --path . res://tests/phase03/visual_capture.tscn -- --output=res://docs/phase03/visual_evidence/<set>` | PNGs + `cameras.json` (render settings recorded) |
| Performance | `"$G" --path . --resolution 1920x1080 res://tests/phase03/perf_capture.tscn -- --autopilot --mission=1 --until=1 --save-slot=p03_perf --perf=res://tests/phase03/evidence/perf_m01.json` | frame-time summary in the JSON |
| Requirements audit | `python -I tools/phase03_collect_evidence.py && python -I tools/phase03_requirements.py && python -I tools/phase03_completion_audit.py` | exits 0 only when every mandatory requirement is independently VERIFIED |
| Windows export | `"$G" --headless --path . --export-release "Windows Desktop" build/windows/BreakoutNoWayBack.exe` | then run the exe with the autopilot arguments above and inspect its report |

The autopilot drives both players through DeviceRouter's virtual devices and real interactions (no completion
flags are set directly). It still knows interaction positions a human must discover, and runs at time scale 3, so a
human two-controller playthrough remains a separate acceptance test.

## Trailer

`tests/phase03/trailer.tscn` renders the 72 s Chapter 1 trailer from the live levels (command in the script header);
output `build/trailer/BreakoutNoWayBack_Ch1_Trailer.mp4`.
