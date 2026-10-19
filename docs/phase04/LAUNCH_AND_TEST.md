# Phase 04 launch and testing instructions

Everything in `docs/phase03/LAUNCH_AND_TEST.md` still applies (controls, autopilot, captures, trailer). Phase 04 adds:

```bash
G="/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe"
```

| Check | Command | Pass condition |
|---|---|---|
| Baseline (fresh evidence from a commit) | `bash tools/phase04_baseline.sh` | `tests/phase04/evidence/baseline_summary.txt` all exit=0 |
| Release battery (regressions, guard AI, parse, UI, export, exe chapter) | `bash tools/phase04_release_check.sh` | `final_summary.txt` all exit=0; `final_exe.json` chapter_complete |
| Guard AI | `"$G" --headless --fixed-fps 60 --path . res://tests/phase04/guard_ai_tests.tscn` | 5/5 |
| UI walkthrough (real clicks, horizontal split, pause, Continue) | `"$G" --path . --resolution 1600x900 res://tests/phase04/ui_walkthrough.tscn -- --save-slot=p04_ui` | `ui_walkthrough.json` pass |
| Compile check (all scripts, autoloads present) | `"$G" --headless --path . res://tests/phase04/parse_check.tscn` | failed = 0 |
| Performance, every mission, real time | `bash tools/phase04_perf_all.sh` | `perf_m0N.json` summaries |
| Character texture pass | `python tools/phase04_character_textures.py` (then `bash tools/phase03_reimport.sh`) | `assets/characters/phase04/*.png` |
| Requirements + audit | `python -I tools/phase04_collect_evidence.py && python -I tools/phase04_requirements.py && python -I tools/phase04_completion_audit.py` | exit 0 only when all mandatory rows are independently VERIFIED |

Split-screen layout: Settings → "Horizontal split-screen (top / bottom)" (applies at the next New Game/Continue), or
`--split=horizontal` after `--`. Graphics quality: Settings → Graphics (low/medium/high) or `--quality=0|1|2`.

Human acceptance still required: two people with two controllers playing Chapter 1 start to finish, and an audio
listening pass.
