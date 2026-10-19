#!/usr/bin/env bash
# Real-time (speed 1) performance capture of every mission at 1920x1080 split-screen, quality from settings.
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
E=tests/phase04/evidence
for m in ${MISSIONS:-1 2 3 4 5 6}; do
  timeout 900 "$G" --path . --resolution 1920x1080 --log-file $E/perf_m0$m.log res://tests/phase03/perf_capture.tscn -- --autopilot --mission=$m --until=$m --timeout=900 --save-slot=p04_perf_m0$m --report=res://$E/perf_m0${m}_autopilot.json --perf=res://$E/perf_m0$m.json > /dev/null 2>&1
  echo "m0$m exit=$?"
done
