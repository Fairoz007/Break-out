#!/usr/bin/env bash
# Phase 03 headless regression battery (one Godot job at a time). Results: tests/phase03/evidence/regress_<name>.log
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
E=tests/phase03/evidence
mkdir -p $E
run() { local name=$1; shift; timeout ${T:-1500} "$G" "$@" > $E/regress_$name.log 2>&1; echo "$name exit=$?" | tee -a $E/regress_summary.txt; }
: > $E/regress_summary.txt
run gameplay --headless --path . --fixed-fps 60 res://tests/phase025/gameplay_regressions.tscn
run save_validation --headless --path . res://tests/phase025/save_validation.tscn
run system_suite --headless --path . --fixed-fps 60 res://tests/phase02/run_tests.tscn -- --save-slot=p03_system_suite
run checkpoints --headless --fixed-fps 60 --path . res://tests/phase025/checkpoint_regressions.tscn -- --save-slot=phase025_p03_checkpoint_suite
echo all-done | tee -a $E/regress_summary.txt
