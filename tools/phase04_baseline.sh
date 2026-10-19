#!/usr/bin/env bash
# Phase 04 baseline: fresh evidence from the committed Phase 03 state. Outputs in tests/phase04/evidence/baseline_*.
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
E=tests/phase04/evidence
mkdir -p $E
S=$E/baseline_summary.txt; : > $S
step() { echo "$1 exit=$2" | tee -a $S; }
timeout 1500 "$G" --headless --path . --import > $E/baseline_import.log 2>&1; step import $?
echo "import_errors=$(grep -cE '^ERROR|SCRIPT ERROR' $E/baseline_import.log)" | tee -a $S
bash tools/phase03_run_regressions.sh > $E/baseline_regressions.txt 2>&1; step regressions $?
cp tests/phase03/evidence/regress_*.log tests/phase03/evidence/regress_summary.txt $E/ 2>/dev/null
timeout 700 "$G" --path . --resolution 1600x900 --log-file $E/baseline_first_objective.log res://tests/phase03/first_objective.tscn -- --save-slot=p04_first_objective > /dev/null 2>&1; step first_objective $?
cp tests/phase03/evidence/first_objective.json $E/baseline_first_objective.json; cp -r tests/phase03/evidence/first_objective $E/baseline_first_objective_shots
timeout 900 "$G" --path . --log-file $E/baseline_capture.log res://tests/phase03/visual_capture.tscn -- --output=res://docs/phase04/visual_evidence/baseline > /dev/null 2>&1; step capture $?
timeout 2400 "$G" --headless --path . --export-release "Windows Desktop" build/windows/BreakoutNoWayBack.exe > $E/baseline_export.log 2>&1; step export $?
rm -rf $E/baseline_exe_shots; mkdir -p $E/baseline_exe_shots
timeout 2700 build/windows/BreakoutNoWayBack.exe --resolution 1280x720 --log-file "$(pwd -W)/$E/baseline_exe.log" -- --autopilot --new --speed=3 --timeout=2400 --save-slot=p04_baseline_exe --report="$(pwd -W)/$E/baseline_exe.json" --shots="$(pwd -W)/$E/baseline_exe_shots" > /dev/null 2>&1; step exe_chapter $?
echo done | tee -a $S
