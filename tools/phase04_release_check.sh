#!/usr/bin/env bash
# Phase 04 release-candidate battery on the current tree: regressions, guard AI, UI walkthrough, parse check,
# Windows export and a full graphical chapter on the exported executable. Outputs: tests/phase04/evidence/final_*.
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
E=tests/phase04/evidence
S=$E/final_summary.txt; : > $S
step() { echo "$1 exit=$2" | tee -a $S; }
bash tools/phase03_run_regressions.sh > $E/final_regressions.txt 2>&1; step regressions $?
for f in regress_gameplay.log regress_system_suite.log regress_save_validation.log regress_checkpoints.log regress_summary.txt; do cp tests/phase03/evidence/$f $E/$f; done
cp $E/regress_system_suite.log $E/system_suite.log
timeout 300 "$G" --headless --fixed-fps 60 --path . res://tests/phase04/guard_ai_tests.tscn > $E/guard_ai_tests.log 2>&1; step guard_ai $?
timeout 300 "$G" --headless --path . res://tests/phase04/parse_check.tscn > $E/parse_check.log 2>&1; step parse_check $?
timeout 500 "$G" --path . --resolution 1600x900 --log-file $E/ui_walkthrough.log res://tests/phase04/ui_walkthrough.tscn -- --save-slot=p04_ui > /dev/null 2>&1; step ui_walkthrough $?
for c in idle mistakes; do
  timeout 1500 "$G" --headless --fixed-fps 60 --path . -- --autopilot --new --speed=4 --chaos=$c --timeout=6000 --save-slot=p04_chaos_$c --report=res://$E/chaos_$c.json > $E/chaos_$c.log 2>&1; step chaos_$c $?
done
timeout 900 "$G" --path . --log-file $E/final_capture.log res://tests/phase03/visual_capture.tscn -- --output=res://docs/phase04/visual_evidence/iter02 > /dev/null 2>&1; step capture $?
timeout 2400 "$G" --headless --path . --export-release "Windows Desktop" build/windows/BreakoutNoWayBack.exe > $E/final_export.log 2>&1; step export $?
rm -rf $E/final_exe_shots; mkdir -p $E/final_exe_shots
timeout 2700 build/windows/BreakoutNoWayBack.exe --resolution 1280x720 --log-file "$(pwd -W)/$E/final_exe.log" -- --autopilot --new --speed=3 --timeout=2400 --save-slot=p04_final_exe --report="$(pwd -W)/$E/final_exe.json" --shots="$(pwd -W)/$E/final_exe_shots" > /dev/null 2>&1; step exe_chapter $?
for m in 1 2 3 4 5 6; do   # real-time cadence on the exported build (speed 1, 1920x1080 split-screen)
  timeout 900 build/windows/BreakoutNoWayBack.exe --resolution 1920x1080 --log-file "$(pwd -W)/$E/exe_perf_m0$m.log" -- --autopilot --mission=$m --until=$m --timeout=900 --save-slot=p04_exe_perf_m0$m --report="$(pwd -W)/$E/exe_perf_m0$m.json" > /dev/null 2>&1; step exe_perf_m0$m $?
done
echo done | tee -a $S
