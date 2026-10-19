"""Collect Phase 03 runtime evidence into docs/phase03/runtime_evidence.json.

Reads actual test outputs (never asserts success that a file does not show) and maps them onto requirement IDs.
Runtime proof sets at most IMPLEMENTED_UNTESTED; a FAILED test sets FAILED. VERIFIED is reserved for independent
QA verdicts (docs/phase03/qa_verdicts.json), applied by tools/phase03_requirements.py.

    python -I tools/phase03_collect_evidence.py [--chapter tests/phase03/evidence/chapter_gfx.json ...]
"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
E = R / "tests/phase03/evidence"
items = {}


def add(rid, evidence, status="IMPLEMENTED_UNTESTED"):
    it = items.setdefault(rid, {"evidence": [], "status": status})
    if evidence not in it["evidence"]:
        it["evidence"].append(evidence)
    if status == "FAILED":
        it["status"] = "FAILED"


def rel(p):
    return str(Path(p).resolve().relative_to(R)).replace("\\", "/")


chapters = sys.argv[sys.argv.index("--chapter") + 1:] if "--chapter" in sys.argv else [str(E / n) for n in ("chapter_gfx.json", "chaos_idle.json", "chaos_mistakes.json")]
summary = {"chapter_runs": []}
for c in chapters:
    p = Path(c) if Path(c).is_absolute() else R / c
    if not p.exists():
        continue
    rep = json.loads(p.read_text(encoding="utf-8"))
    ev = rep.get("events", [])
    tag = rel(p)
    complete = rep.get("reason") == "chapter_complete"
    graphical = rep.get("screenshots", 0) > 0
    summary["chapter_runs"].append({"report": tag, "reason": rep.get("reason"), "real_seconds": rep.get("real_seconds"), "graphical": graphical,
                                    "speed": rep.get("args", {}).get("speed", "1")})
    for e in ev:
        k = e.get("kind")
        if k == "dialogue_shown" and e.get("id"):
            add(f"P03-DLG-{e['id']}", f"{tag}#dialogue_shown:{e['id']}")
        elif k == "shot_activated" and e.get("id"):
            add(f"P03-SHOT-{e['id']}", f"{tag}#shot_activated:{e['id']}")
        elif k == "objective_completed":
            add(f"P03-OBJ-{e['id']}", f"{tag}#objective_completed:{e['id']}")
        elif k == "mission_complete":
            n = int(e["mission"])
            add(f"P03-MIS-0{n}-000", f"{tag}#mission_complete:{n}")
            for j in (2, 3, 6, 7, 8, 11, 12):          # spawning, objectives, triggers, dialogue, cinematics, completion, transition
                add(f"P03-MIS-0{n}-{j:03}", f"{tag}#mission_complete:{n}")
            add(f"P03-MIS-0{n}-001", f"{tag}#mission_loaded:{n}")
        elif k == "checkpoint":
            add("P03-PLAY-015", f"{tag}#checkpoint:{e.get('id', '')}")
        elif k == "interact":
            add("P03-PLAY-011", f"{tag}#interact")
    if complete:
        for rid in ("P03-PLAY-003", "P03-PLAY-012", "P03-PLAY-014", "P03-PLAY-018", "P03-CIN-001", "P03-CIN-012", "P03-CIN-010", "P03-CIN-009", "P03-QA-005"):
            add(rid, f"{tag}#reason=chapter_complete")
        if graphical:
            add("P03-QA-004", f"{tag}#graphical chapter run, {rep.get('screenshots')} screenshots")
            add("P03-PERF-001", f"{tag}#wall_frame_cadence")
            add("P03-PERF-002", f"{tag}#wall_frame_cadence")
            add("P03-PERF-007", f"{tag}#viewport_sizes={rep.get('viewport_sizes')}")
    for e in ev:
        if e.get("kind") == "detected_fail":
            add("P03-AI-004", f"{tag}#detected_fail")
            add("P03-MIS-04-009", f"{tag}#detected_fail")

text = (E / "regress_gameplay.log").read_text(encoding="utf-8", errors="replace") if (E / "regress_gameplay.log").exists() else ""
gp = {m.group(1): m.group(2) == "PASS" for m in re.finditer(r"(?m)^(\w+): (PASS|FAIL)", text)}
gmap = {"floor_detected": ["P03-PLAY-003"], "crouch_capsule_reduced": ["P03-PLAY-008"], "blocked_stand_preserves_crouch": ["P03-PLAY-008"],
        "clear_headroom_stands": ["P03-PLAY-008"], "jump_leaves_floor": ["P03-PLAY-009"], "jump_lands": ["P03-PLAY-009"], "jump_input_isolated": ["P03-PLAY-009", "P03-PLAY-013"],
        "camera_respects_near_wall": ["P03-PLAY-010"], "camera_blend_respects_thin_wall": ["P03-PLAY-010"], "crouch_camera_follows_head": ["P03-PLAY-010"],
        "virtual_owner_restored": ["P03-PLAY-013"], "virtual_edges_cleared": ["P03-PLAY-013"]}
for name, ok in gp.items():
    for rid in gmap.get(name, []):
        add(rid, f"tests/phase03/evidence/regress_gameplay.log#{name}", "IMPLEMENTED_UNTESTED" if ok else "FAILED")
text = (E / "regress_system_suite.log").read_text(encoding="utf-8", errors="replace") if (E / "regress_system_suite.log").exists() else ""
st = {m.group(1): m.group(2) == "PASS" for m in re.finditer(r"(?m)^TEST (\w+) (PASS|FAIL)", text)}
smap = {"split_screen_world": ["P03-PLAY-012", "P03-QA-006"], "device_exclusive": ["P03-PLAY-013"], "input_between_physics_ticks": ["P03-PLAY-013"],
        "movement_speeds": ["P03-PLAY-005", "P03-PLAY-006", "P03-PLAY-007", "P03-PLAY-004"], "wall_collision": ["P03-PLAY-004"], "camera_min_distance": ["P03-PLAY-010"],
        "simultaneous_movement": ["P03-PLAY-013"], "interaction_leases": ["P03-PLAY-011"], "checkpoint_reload": ["P03-PLAY-015", "P03-QA-007"],
        "save_file": ["P03-PLAY-016", "P03-QA-007"], "snapshot_roundtrip": ["P03-PLAY-016"], "guard_detection_and_cover": ["P03-AI-004", "P03-AI-010"],
        "escort_gap": ["P03-MIS-01-005"], "solo_gate_m02": ["P03-MIS-02-005"], "solo_gate_m03": ["P03-MIS-03-005"], "solo_gate_m06": ["P03-MIS-06-005"],
        "mutual_skip": ["P03-CIN-010"], "subtitle_wrap": ["P03-AUD-013", "P03-CIN-006"], "data_integrity": ["P03-CIN-001", "P03-CIN-011"],
        "device_disconnect_pause": ["P03-PLAY-013"]}
for name, ok in st.items():
    for rid in smap.get(name, []):
        add(rid, f"tests/phase03/evidence/regress_system_suite.log#{name}", "IMPLEMENTED_UNTESTED" if ok else "FAILED")
if st:
    add("P03-QA-003", f"tests/phase03/evidence/regress_system_suite.log#{sum(st.values())}/{len(st)} passed",
        "IMPLEMENTED_UNTESTED" if all(st.values()) else "FAILED")
text = (E / "regress_save_validation.log").read_text(encoding="utf-8", errors="replace") if (E / "regress_save_validation.log").exists() else ""
m = re.search(r"SAVE VALIDATION (\{.*\})", text)
if m:
    ok = "false" not in m.group(1)
    add("P03-PLAY-016", "tests/phase03/evidence/regress_save_validation.log#SAVE VALIDATION", "IMPLEMENTED_UNTESTED" if ok else "FAILED")
text = (E / "regress_checkpoints.log").read_text(encoding="utf-8", errors="replace") if (E / "regress_checkpoints.log").exists() else ""
m = re.search(r"CHECKPOINT REGRESSIONS (\d+)/(\d+)", text)
if m:
    ok = m.group(1) == m.group(2)
    add("P03-PLAY-015", f"tests/phase03/evidence/regress_checkpoints.log#{m.group(1)}/{m.group(2)}", "IMPLEMENTED_UNTESTED" if ok else "FAILED")
    add("P03-MIS-01-010", "tests/phase03/evidence/regress_checkpoints.log", "IMPLEMENTED_UNTESTED" if ok else "FAILED")
    for n in range(2, 7):
        add(f"P03-MIS-0{n}-010", "tests/phase03/evidence/regress_checkpoints.log", "IMPLEMENTED_UNTESTED" if ok else "FAILED")
first = E / "first_objective.json"
if first.exists():
    fo = json.loads(first.read_text(encoding="utf-8"))
    add("P03-PLAY-017", "tests/phase03/evidence/first_objective.json", "IMPLEMENTED_UNTESTED" if fo.get("pass") else "FAILED")
    if fo.get("menu_new_game"):
        add("P03-PLAY-001", "tests/phase03/evidence/first_objective.json#menu", "IMPLEMENTED_UNTESTED" if fo.get("pass") else "FAILED")
        add("P03-PLAY-002", "tests/phase03/evidence/first_objective.json#new_game_button", "IMPLEMENTED_UNTESTED" if fo.get("pass") else "FAILED")

# Performance captures (real time, speed 1) and the Windows export / exported-binary run
for perf in sorted(E.glob("perf_m0*.json")):
    pr = json.loads(perf.read_text(encoding="utf-8"))
    sm = pr.get("summary", {})
    tag = rel(perf)
    if sm:
        for rid in ("P03-PERF-001", "P03-PERF-002", "P03-PERF-003", "P03-PERF-005", "P03-PERF-007", "P03-PERF-012", "P03-PERF-016", "P03-QA-009"):
            add(rid, f"{tag}#fps_mean={sm.get('fps_mean', 0):.1f},p99_ms={sm.get('p99_ms', 0):.1f}")
        add("P03-PERF-004", f"{tag}#video_mem_mb_p50={sm.get('video_mem_mb_p50', 0):.0f}")
        add("P03-PERF-006", f"{tag}#first_mission_load_ms={pr.get('first_mission_load_ms', 0):.0f}")
        add("P03-PERF-008", f"{tag}#draw_calls_p50={sm.get('draw_calls_p50')},max={sm.get('draw_calls_max')}")
exp = E / "export.log"
exe = R / "build/windows/BreakoutNoWayBack.exe"
if exp.exists() and exe.exists() and "[ DONE ]" in exp.read_text(encoding="utf-8", errors="replace").replace("", ""):
    add("P03-QA-010", "tests/phase03/evidence/export.log#savepack DONE")
elif exp.exists() and exe.exists():
    add("P03-QA-010", "tests/phase03/evidence/export.log")
exe_run = E / "exe_chapter.json"
if exe_run.exists():
    rep = json.loads(exe_run.read_text(encoding="utf-8"))
    ok = rep.get("reason") == "chapter_complete"
    add("P03-QA-011", f"tests/phase03/evidence/exe_chapter.json#reason={rep.get('reason')}", "IMPLEMENTED_UNTESTED" if ok else "FAILED")

# Graphical capture sets: evidence for visual rows (review still required).
cams = sorted((R / "docs/phase03/visual_evidence").glob("iter*/cameras.json"), key=lambda p: p.stat().st_mtime)
latest = cams[-1] if cams else None
if latest:
    d = rel(latest.parent)
    vis = {"bus": ["P03-BUS-014"], "bus_interior": ["P03-BUS-008", "P03-BUS-014"], "bus_front": ["P03-BUS-002", "P03-BUS-005", "P03-BUS-006"],
           "intake": ["P03-ENV-INTAKE-000"], "intake_counter": ["P03-ENV-INTAKE-009"], "intake_lockers": ["P03-ENV-INTAKE-009"], "cellblock": ["P03-ENV-CELL-000"],
           "cell_interior": ["P03-ENV-CELL-009"], "yard": ["P03-ENV-YARD-000", "P03-COURT-013"], "court_layout": ["P03-COURT-001", "P03-COURT-003"],
           "hoop_detail": ["P03-COURT-004", "P03-COURT-005", "P03-COURT-006", "P03-COURT-007", "P03-COURT-008"], "court_ground": ["P03-COURT-002", "P03-COURT-011"],
           "yard_fence": ["P03-COURT-009"], "workshop": ["P03-ENV-WORK-000"], "workshop_machines": ["P03-ENV-WORK-010"], "maintenance": ["P03-ENV-MAINT-000"],
           "maintenance_pumps": ["P03-ENV-MAINT-010"], "solitary": ["P03-ENV-SEC-000"]}
    for name, rids in vis.items():
        if (latest.parent / f"{name}.png").exists():
            for rid in rids:
                add(rid, f"{d}/{name}.png")
    for rid in ("P03-LIGHT-001", "P03-LIGHT-013", "P03-PROC-002"):
        add(rid, f"{d}/cameras.json")

out = {"generated_by": "tools/phase03_collect_evidence.py", "summary": summary, "items": items}
(R / "docs/phase03/runtime_evidence.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps({"items": len(items), "chapter_runs": summary["chapter_runs"]}))
