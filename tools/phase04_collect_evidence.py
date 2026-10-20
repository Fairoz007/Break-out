"""Collect Phase 04 runtime evidence into docs/phase04/runtime_evidence.json (never VERIFIED; at most
IMPLEMENTED_UNTESTED, or FAILED when a test output shows failure). Only Phase 04 outputs are used.

    python -I tools/phase04_collect_evidence.py
"""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parents[1]
E = R / "tests/phase04/evidence"
items = {}


def add(rid, ev, ok=True):
    it = items.setdefault(rid, {"evidence": [], "status": "IMPLEMENTED_UNTESTED"})
    if ev not in it["evidence"]:
        it["evidence"].append(ev)
    if not ok:
        it["status"] = "FAILED"


def j(name):
    p = E / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def txt(name):
    p = E / name
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


rel = lambda n: f"tests/phase04/evidence/{n}"

# --- baseline
summ = txt("baseline_summary.txt")
steps = dict(re.findall(r"(\w+) exit=(\d+)", summ))
if steps:
    add("P04-BASE-001", "git commit 0fb705c (origin/phase03)")
    add("P04-BASE-002", rel("baseline_import.log"), steps.get("import") == "0" and "import_errors=0" in summ)
    add("P04-BASE-016", "docs/phase04/BASELINE_AUDIT.md")
    add("P04-BASE-015", "docs/phase04/visual_evidence/baseline/cameras.json", steps.get("capture") == "0")
fo = j("baseline_first_objective.json")
if fo:
    for rid in ("P04-BASE-003", "P04-BASE-004", "P04-PLAY-001", "P04-PLAY-002", "P04-PLAY-012", "P04-PLAY-018", "P04-UI-001", "P04-UI-002"):
        add(rid, rel("baseline_first_objective.json"), fo.get("pass"))
for name in ("baseline_exe.json", "final_exe.json"):
    rep = j(name)
    if not rep:
        continue
    ok = rep.get("reason") == "chapter_complete"
    tag = rel(name)
    for rid in ("P04-BASE-005", "P04-BASE-007", "P04-BASE-008", "P04-BASE-009", "P04-BASE-011", "P04-BASE-013", "P04-BASE-014",
                "P04-BUILD-001", "P04-BUILD-002", "P04-BUILD-003", "P04-PT-001", "P04-PT-002", "P04-PT-003", "P04-PT-004", "P04-PT-005",
                "P04-PT-006", "P04-PT-007", "P04-PT-009", "P04-PT-010", "P04-PT-011", "P04-PT-012", "P04-CIN-002", "P04-CIN-004", "P04-CIN-009", "P04-CIN-010",
                "P04-UI-007", "P04-UI-008", "P04-UI-009", "P04-UI-010", "P04-COOP-006", "P04-COOP-007", "P04-COOP-008", "P04-COOP-009", "P04-COOP-010"):
        add(rid, f"{tag}#reason={rep.get('reason')}", ok)
    for e in rep.get("events", []):
        k = e.get("kind")
        if k == "dialogue_shown":
            add(f"P04-C-P03-DLG-{e['id']}", f"{tag}#dialogue_shown")
        elif k == "shot_activated":
            add(f"P04-C-P03-SHOT-{e['id']}", f"{tag}#shot_activated")
        elif k == "objective_completed":
            add(f"P04-C-P03-OBJ-{e['id']}", f"{tag}#objective_completed")
        elif k == "mission_complete":
            n = int(e["mission"])
            for a in (1, 2, 3, 4, 5, 6, 7, 8, 12, 13):
                add(f"P04-MIS-0{n}-{a:03}", f"{tag}#mission_complete:{n}")
        elif k == "checkpoint":
            add("P04-PLAY-013", f"{tag}#checkpoint")
        elif k == "bus_doors":
            add("P04-BUS-007", f"{tag}#bus_doors")
        elif k == "bus_arrival":
            add("P04-BUS-012", f"{tag}#bus_arrival")
# --- failure / retry / conditional-dialogue runs (headless chaos modes)
for name in ("chaos_idle.json", "chaos_mistakes.json"):
    rep = j(name)
    if not rep:
        continue
    tag = rel(name)
    ok = rep.get("reason") == "chapter_complete"
    kinds = [e.get("kind") for e in rep.get("events", [])]
    for e in rep.get("events", []):
        if e.get("kind") == "dialogue_shown":
            add(f"P04-C-P03-DLG-{e['id']}", f"{tag}#dialogue_shown")
    if "mistakes" in name:
        for n in range(1, 7):
            add(f"P04-MIS-0{n}-009", f"{tag}#failure/retry paths, reason={rep.get('reason')}", ok)
        if "detected_fail" in kinds:
            add("P04-AI-007", f"{tag}#detected_fail")
            add("P04-PT-004", f"{tag}#detected_fail+retry")
# --- regressions
gp = {m.group(1): m.group(2) == "PASS" for m in re.finditer(r"(?m)^(\w+): (PASS|FAIL)", txt("regress_gameplay.log"))}
gmap = {"floor_detected": ["P04-PLAY-003", "P04-PLAY-015"], "crouch_capsule_reduced": ["P04-PLAY-007"], "clear_headroom_stands": ["P04-PLAY-007", "P04-PLAY-016"],
        "jump_leaves_floor": ["P04-PLAY-008"], "jump_lands": ["P04-PLAY-008"], "camera_respects_near_wall": ["P04-PLAY-009"], "recovery_restores_collision": ["P04-PLAY-016", "P04-PLAY-010"],
        "jump_input_isolated": ["P04-COOP-013"], "virtual_owner_restored": ["P04-COOP-013"]}
for t, ok in gp.items():
    for rid in gmap.get(t, []):
        add(rid, rel("regress_gameplay.log") + "#" + t, ok)
st = {m.group(1): m.group(2) == "PASS" for m in re.finditer(r"(?m)^TEST (\w+) (PASS|FAIL)", txt("system_suite.log") or txt("regress_system_suite.log"))}
smap = {"split_screen_world": ["P04-COOP-002", "P04-BASE-007"], "device_exclusive": ["P04-COOP-003", "P04-COOP-013", "P04-COOP-004"], "simultaneous_movement": ["P04-COOP-014"],
        "movement_speeds": ["P04-PLAY-004", "P04-PLAY-005", "P04-PLAY-006"], "wall_collision": ["P04-PLAY-010"], "interaction_leases": ["P04-PLAY-011"],
        "mutual_skip": ["P04-COOP-011"], "checkpoint_reload": ["P04-COOP-012", "P04-PLAY-014"], "save_file": ["P04-PLAY-014", "P04-BASE-012"],
        "device_disconnect_pause": ["P04-COOP-015"], "guard_detection_and_cover": ["P04-AI-004", "P04-AI-011"], "solo_gate_m02": ["P04-COOP-007"],
        "solo_gate_m03": ["P04-COOP-008"], "solo_gate_m06": ["P04-COOP-007"], "escort_gap": ["P04-MIS-01-005"], "subtitle_wrap": ["P04-CIN-003", "P04-UI-009"],
        "data_integrity": ["P04-CIN-001", "P04-CIN-012"], "settings_roundtrip": ["P04-UI-006"]}
for t, ok in st.items():
    for rid in smap.get(t, []):
        add(rid, rel("system_suite.log") + "#" + t, ok)
cp = re.search(r"CHECKPOINT REGRESSIONS (\d+)/(\d+)", txt("regress_checkpoints.log"))
if cp:
    for n in range(1, 7):
        add(f"P04-MIS-0{n}-010", rel("regress_checkpoints.log"), cp.group(1) == cp.group(2))
        add(f"P04-MIS-0{n}-011", rel("regress_checkpoints.log"), cp.group(1) == cp.group(2))
    add("P04-PT-008", rel("regress_checkpoints.log"), cp.group(1) == cp.group(2))
# --- Phase 04 tests
g = j("guard_ai_tests.json")
if g:
    res = {r["test"]: r["pass"] for r in g["results"]}
    for t, rids in {"hearing_sprint_behind": ["P04-AI-005", "P04-AI-002"], "crouch_walk_silent": ["P04-AI-005"], "independent_detection": ["P04-AI-012", "P04-AI-004"],
                    "search_then_return": ["P04-AI-002", "P04-AI-003", "P04-AI-008", "P04-AI-009"], "wall_blocks_sight": ["P04-AI-011"]}.items():
        for rid in rids:
            add(rid, rel("guard_ai_tests.json") + "#" + t, res.get(t, False))
mh = j("m04_headless.json")
if mh:
    add("P04-AI-010", rel("m04_headless.json"), mh.get("reason") == "until_reached")
    add("P04-MIS-04-009", rel("m04_headless.json"))
ui = j("ui_walkthrough.json")
if ui:
    res = {s["step"]: s["pass"] for s in ui["steps"]}
    for step, rids in {"horizontal_layout_in_game": ["P04-COOP-001"], "pause_opens": ["P04-UI-005"], "resume": ["P04-UI-005"], "open_settings": ["P04-UI-006"],
                       "controls_and_devices": ["P04-UI-004"], "continue_resumes": ["P04-UI-003", "P04-PLAY-014"], "quit_to_menu": ["P04-UI-011"], "main_menu": ["P04-UI-001", "P04-BASE-003"]}.items():
        for rid in rids:
            add(rid, rel("ui_walkthrough.json") + "#" + step, res.get(step, False))
pc = j("parse_check.json")
if pc:
    add("P04-QA-003", rel("parse_check.json"), not pc["failed"])
for perf in sorted(E.glob("perf_m0?.json")):
    pr = json.loads(perf.read_text(encoding="utf-8"))
    sm = pr.get("summary", {})
    if sm:
        tag = rel(perf.name) + f"#fps={sm.get('fps_mean', 0):.0f},p99={sm.get('p99_ms', 0):.1f}ms"
        for rid in ("P04-PERF-001", "P04-PERF-006", "P04-PERF-009", "P04-PERF-012"):
            add(rid, tag)
        add("P04-PERF-011", tag, sm.get("frames_over_16_7ms_pct", 100) < 1.0)
for perf in sorted(E.glob("exe_perf_m0?.json")):
    rep = json.loads(perf.read_text(encoding="utf-8"))
    cad = rep.get("wall_frame_cadence", {})
    for k, v in cad.items():
        tag = rel(perf.name) + f"#exe m{k}: {v['fps_from_elapsed']:.0f} fps, p99 {v['p99_ms']:.1f} ms, max {v['max_ms']:.0f} ms"
        for rid in ("P04-PERF-001", "P04-PERF-002", "P04-PERF-006", "P04-PERF-012", "P04-BUILD-003"):
            add(rid, tag)
        add("P04-PERF-011", tag, v["p99_ms"] < 16.7)
ct = j("character_textures.json")
if ct:
    for rid in ("P04-CHAR-008", "P04-CHAR-009", "P04-CHAR-010"):
        add(rid, "docs/phase04/visual_evidence/character/texture_edits.jpg")
vis = R / "docs/phase04/visual_evidence/iter02"
if not vis.exists():
    vis = R / "docs/phase04/visual_evidence/iter01"
for name, rids in {"bus_doors_open.png": ["P04-BUS-007", "P04-BUS-001"], "hoop_detail.png": ["P04-COURT-004", "P04-COURT-005", "P04-COURT-006", "P04-COURT-007", "P04-COURT-008", "P04-COURT-011"],
                   "yard.png": ["P04-COURT-014", "P04-COURT-010"], "adrian_face.png": ["P04-CHAR-009"], "noah_close.png": ["P04-CHAR-010"], "noah_wrist.png": ["P04-CHAR-010"],
                   "bus_rear.png": ["P04-BUS-001", "P04-BUS-004"], "bus_cabin_fwd.png": ["P04-BUS-008", "P04-BUS-009"]}.items():
    if (vis / name).exists():
        for rid in rids:
            add(rid, f"docs/phase04/visual_evidence/{vis.name}/{name}")
(R / "docs/phase04/runtime_evidence.json").write_text(json.dumps({"generated_by": "tools/phase04_collect_evidence.py", "items": items}, indent=1), encoding="utf-8")
print("items", len(items), "failed", sum(1 for v in items.values() if v["status"] == "FAILED"))
