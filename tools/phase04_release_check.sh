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
timeout 2400 "$G" --headless --path . --export-release "Windows Desktop" build/windows/BreakoutNoWayBack.exe > $E/final_export.log 2>&1; step export $?
rm -rf $E/final_exe_shots; mkdir -p $E/final_exe_shots
timeout 2700 build/windows/BreakoutNoWayBack.exe --resolution 1280x720 --log-file "$(pwd -W)/$E/final_exe.log" -- --autopilot --new --speed=3 --timeout=2400 --save-slot=p04_final_exe --report="$(pwd -W)/$E/final_exe.json" --shots="$(pwd -W)/$E/final_exe_shots" > /dev/null 2>&1; step exe_chapter $?
echo done | tee -a $S
