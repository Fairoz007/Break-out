"""Capture clean initial environment sources and repaired sources with identical cameras.

Only the listed initially-clean environment scripts are temporarily replaced. Repaired
bytes are archived and restored in finally. Do not run alongside another engine job.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
ENGINE = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe")
FILES = ["scripts/world/env_builder.gd", "scripts/world/env_cellblock.gd",
         "scripts/world/env_intake.gd", "scripts/world/env_yard.gd",
         "scripts/world/env_workshop.gd", "scripts/world/env_maintenance.gd"]
EVIDENCE = ROOT / "tests/phase025/evidence"


def capture(label):
    output = EVIDENCE / label
    output.mkdir(parents=True, exist_ok=True)
    sentinel = output / "cameras.json"
    previous = sentinel.stat().st_mtime_ns if sentinel.exists() else 0
    log = EVIDENCE / (label + "_valid.log")
    subprocess.run([str(ENGINE), "--path", str(ROOT), "--resolution", "1280x720",
                    "--log-file", str(log), "res://tests/phase025/visual_capture.tscn",
                    "--", "--output=res://tests/phase025/evidence/" + label], cwd=ROOT, check=True)
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        if sentinel.exists() and sentinel.stat().st_mtime_ns != previous:
            rows = json.loads(sentinel.read_text())
            if len(rows) != 5 or not all(r["written"] for r in rows):
                raise RuntimeError("Incomplete captures")
            time.sleep(1)
            text = log.read_text(errors="replace") if log.exists() else ""
            if "ERROR:" in text:
                raise RuntimeError("Engine errors; inspect " + str(log))
            return rows
        time.sleep(1)
    raise TimeoutError("Capture did not finish: " + str(log))


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / ".gdignore").write_text("")
    repaired = {f: (ROOT / f).read_bytes() for f in FILES}
    initial = {f: subprocess.check_output(["git", "show", "HEAD:" + f], cwd=ROOT) for f in FILES}
    archive = EVIDENCE / "environment_sources"
    archive.mkdir(exist_ok=True)
    manifest = {}
    for f in FILES:
        manifest[f] = {}
        for label, source in [("initial", initial), ("repaired", repaired)]:
            (archive / (Path(f).name + "." + label + ".txt")).write_bytes(source[f])
            manifest[f][label] = hashlib.sha256(source[f]).hexdigest()
    try:
        for f, data in initial.items():
            (ROOT / f).write_bytes(data)
        before = capture("before_valid")
    finally:
        for f, data in repaired.items():
            (ROOT / f).write_bytes(data)
    after = capture("after_valid")
    if before != after:
        raise RuntimeError("Camera configurations differ")
    (EVIDENCE / "comparison_manifest.json").write_text(json.dumps({"source": manifest, "cameras_match": True,
        "baseline_scope": "Initially clean environment files from HEAD; current assets, renderer and capture harness held constant. Original incomplete standalone-script captures are invalid and superseded."}, indent=2))
    print("Five valid matched environment comparisons; repaired source restored.")


if __name__ == "__main__":
    main()
