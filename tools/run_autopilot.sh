#!/usr/bin/env bash
# Run the two-player autopilot and summarise the result.
# usage: tools/run_autopilot.sh <name> [--headless] -- <game args...>
#   e.g. tools/run_autopilot.sh m01 --headless -- --mission=1 --until=1
# Writes tests/phase02/evidence/<name>.json (report) and <name>.log; prints reason, timings and error lines.
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
cd "$(dirname "$0")/.."
name="$1"; shift
mode=()
if [ "$1" == "--headless" ]; then mode=(--headless --fixed-fps 60); shift; fi
if [ "$1" == "--" ]; then shift; fi
mkdir -p tests/phase02/evidence
log="tests/phase02/evidence/$name.log"
report="tests/phase02/evidence/$name.json"
rm -f "$report"
timeout "${RUN_TIMEOUT:-3000}" "$G" "${mode[@]}" --path . -- --autopilot --save-slot="test_$name" --report="$report" "$@" > "$log" 2>&1
code=$?
echo "exit=$code"
grep -E "SCRIPT ERROR|^ERROR|USER ERROR" "$log" | sort | uniq -c | sort -rn | head -15
python -I - "$report" <<'EOF'
import json, sys, collections
try:
    r = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception as e:
    print("no report:", e); sys.exit(0)
ev = r["events"]
print("reason:", r["reason"], "real_s:", round(r["real_seconds"], 1), "renderer:", r["renderer"], "screens:", r["screenshots"])
print("missions:", r["missions"])
c = collections.Counter(e["kind"] for e in ev)
print("events:", dict(c))
print("objectives:", [e["id"] for e in ev if e["kind"] == "objective_completed"])
print("shots:", [e["id"][-9:] for e in ev if e["kind"] == "shot_activated"])
print("lines:", len({e["id"] for e in ev if e["kind"] == "dialogue_shown"}), "checkpoints:", [e["checkpoint"] for e in ev if e["kind"] == "checkpoint"])
st = [e for e in ev if e["kind"] in ("autopilot_stuck", "interact_rejected", "checkpoint_rejected", "guard_detected")]
print("problems:", st[:8])
last = [e for e in ev if e["kind"] in ("objective_set", "tx", "ready_request")][-4:]
print("last progress:", last)
EOF
exit $code
