"""Phase 03 requirements registry generator.

Builds docs/phase03/requirements.json from (a) the Phase 03 master prompt clauses below, (b) the canonical Chapter 1
data in data/ch01 (6 missions, 19 objectives, 145 dialogue lines, 36 camera shots) and (c) the 87 asset rows the
earlier Phase 03 asset pass recorded in docs/phase03/REQUIREMENTS_MATRIX.md (kept, re-homed under P03-A-*).

Status, evidence and notes already stored in requirements.json are preserved across regenerations. Runtime evidence
is merged from docs/phase03/runtime_evidence.json (written by tools/phase03_collect_evidence.py) and independent QA
verdicts from docs/phase03/qa_verdicts.json. A requirement can only become VERIFIED through a QA verdict whose
reviewer differs from the requirement owner. Renders docs/phase03/REQUIREMENTS_MATRIX.md.

    python -I tools/phase03_requirements.py                       # regenerate + render
    python -I tools/phase03_requirements.py --set ID STATUS [--evidence PATH ...] [--note TEXT]
"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
DOC = R / "docs/phase03"
STORE = DOC / "requirements.json"
VERDICTS = DOC / "qa_verdicts.json"
RUNTIME = DOC / "runtime_evidence.json"
STATUSES = ["NOT_STARTED", "IN_PROGRESS", "IMPLEMENTED_UNTESTED", "FAILED", "BLOCKED", "VERIFIED"]
PROMPT = "Phase 03 master prompt"

OWNERS = {"00": "Agent 00 Orchestrator", "01": "Agent 01 Gameplay", "02": "Agent 02 Character/Animation",
          "03": "Agent 03 Environment/Assets", "04": "Agent 04 Materials/Lighting", "05": "Agent 05 Bus/Vehicle",
          "06": "Agent 06 Yard/Court", "07": "Agent 07 AI/NPC", "08": "Agent 08 Cinematics", "09": "Agent 09 Audio/UI",
          "10": "Agent 10 Performance/Build", "11": "Agent 11 Independent QA"}


def req(rid, section, text, owner, files, accept, test, priority="P1", mandatory=True, **extra):
    d = {"id": rid, "source": f"{PROMPT} §{section}", "requirement": text, "priority": priority, "mandatory": mandatory,
         "owner": OWNERS[owner], "implementation_files": files, "acceptance_criteria": accept, "test_procedure": test,
         "evidence": [], "status": "NOT_STARTED", "notes": ""}
    d.update(extra)
    return d


GFX = "Graphical capture via tests/phase03/visual_capture.tscn; independent visual review of PNGs"
AUTO = "Automated autopilot / regression run with JSON report; log free of SCRIPT ERROR"


def prompt_requirements():
    rows = []
    P = "scripts/player/player.gd"; CAM = "scripts/player/player_camera.gd"; DEV = "scripts/core/device_router.gd"
    CH = "scripts/chapter/chapter_root.gd"; MENU = "scripts/ui/main_menu.gd"; SAVE = "scripts/core/save_service.gd"
    VIS = "scripts/player/character_visual.gd"; EB = "scripts/world/env_builder.gd"
    play = [
        ("001", "Godot project launches to the main menu without script errors", [MENU, "scripts/main.gd"], "Window opens, menu visible, log has no SCRIPT ERROR", "Graphical launch, screenshot of menu, log grep"),
        ("002", "Main menu New Game starts Chapter 1 through the real UI button", [MENU], "Pressing New Game loads M01 with both players", "Graphical UI test clicking New Game"),
        ("003", "Both players spawn at mission spawn points on the floor", [CH, "scripts/missions/mission_01.gd"], "Players grounded at spawn transforms", AUTO),
        ("004", "Third-person control: camera-relative movement", [P, CAM], "Input direction maps to camera space for each player", "tests/phase025/gameplay_regressions.tscn"),
        ("005", "Walking", [P], "Walk speed reached with walk modifier", "gameplay_regressions"),
        ("006", "Running (jog)", [P], "Jog 3.4 m/s default", "gameplay_regressions"),
        ("007", "Sprinting distinct from running", [P], "Sprint 5.2 m/s while sprint held", "gameplay_regressions"),
        ("008", "Crouching with clearance-aware capsule", [P], "Crouch 1.1 m capsule; cannot stand under low ceiling", "gameplay_regressions"),
        ("009", "Jumping and landing", [P, VIS], "Jump impulse, airborne state, landing returns to locomotion", "gameplay_regressions + graphical review"),
        ("010", "Cameras: per-player spring arm with collision", [CAM], "Camera never passes through walls at close range", "gameplay_regressions camera tests"),
        ("011", "Interactions: focus, press, hold and partner states", [P, "scripts/world/interactable.gd"], "Every mission interactable usable by the allowed player only", AUTO),
        ("012", "Split-screen: two viewports of one world", [CH], "Two SubViewports render the shared World3D", "System suite split_screen_world + screenshot"),
        ("013", "Independent input: one player's device cannot control the other", [DEV], "Exclusive device ownership; virtual/physical routing tests pass", "System suite device tests"),
        ("014", "Mission objectives shown and completed in order", ["scripts/chapter/mission_director.gd"], "19 objectives set and completed in canonical order", AUTO),
        ("015", "Checkpoints written at the 12 canonical checkpoints", [SAVE, "scripts/chapter/mission_director.gd"], "All 12 checkpoints reconstruct from disk", "tests/phase025/checkpoint_regressions.tscn"),
        ("016", "Save/load: Continue restores the latest checkpoint; corrupt saves rejected", [SAVE, MENU], "Continue resumes; corrupt save disables Continue", "tests/phase025/save_validation.tscn"),
        ("017", "Reproducible test: fresh game reaches the first real mission objective", ["tests/phase03/first_objective.gd"], "Fresh New Game reaches CH01_M01_OBJ001 objective_set and completes it", "tests/phase03/first_objective.tscn"),
        ("018", "Launch and progression blockers fixed before polish", ["scripts/world/interactable.gd", "tests/phase02/autopilot.gd"], "No blocker in full graphical chapter run", "Full graphical autopilot chapter run"),
    ]
    rows += [req(f"P03-PLAY-{i}", "5", t, "01", f, a, tp, "P0") for i, t, f, a, tp in play]

    char = [
        ("001", "Adrian Cross looks like a believable adult man consistent with docs/characters/ADRIAN_CROSS.md", "Face, hair, wardrobe consistent; no visible defects in close-ups"),
        ("002", "Noah Reyes looks like a believable adult man consistent with docs/characters/NOAH_REYES.md", "Face, hair, wardrobe consistent; no visible defects in close-ups"),
        ("003", "Anatomy, facial geometry and character scale are correct (~1.8 m)", "Height and proportions measured in engine"),
        ("004", "Hair and clothing materials are realistic PBR", "No flat-colour clothing; hair not cap-like at gameplay distance"),
        ("005", "Skeleton and skin weights deform without breakage", "No candy-wrapper joints, no exploded vertices in any clip"),
        ("006", "No T-pose at any time in gameplay or cinematics", "Animation state never falls back to bind pose"),
        ("007", "Characters are grounded (no floating, no sinking)", "Foot height within 3 cm of floor while standing"),
        ("008", "Foot sliding minimised: stride speed matches movement speed", "Locomotion clip speed scaled to velocity"),
        ("009", "Limb movement correct for each clip (retargeting valid)", "Graphical review of each locomotion clip"),
        ("010", "Clothing deformation: no hem/garment intersection (Adrian sweater hem)", "Close-up shows no jagged hem intersections"),
        ("011", "Smooth transitions idle/walk/run/sprint", "Blend times > 0.15 s; no pops"),
        ("012", "Crouch transitions", "Crouch enter/exit blended"),
        ("013", "Jump and landing animation", "Airborne + land clips play"),
        ("014", "Turning in place / direction changes", "Character rotates smoothly toward movement"),
        ("015", "Climbing / traversal (vent crawl, hatch) animation", "Scripted traversal uses crawl/climb clip"),
        ("016", "Interaction animations for press/hold actions", "Interact/Push clips play on use"),
        ("017", "Cinematic gestures from blocking sheet", "Gestures in CH01_CHARACTER_BLOCKING play in cutscenes"),
        ("018", "Graphical animation test exists and was reviewed", "tests/phase025/movement_visual.tscn screenshots reviewed"),
    ]
    rows += [req(f"P03-CHAR-{i}", "6", t, "02", [VIS, "scripts/player/player.gd"], a, "tests/phase025/movement_visual.tscn + " + GFX) for i, t, a in char]

    bus = ["Realistic vehicle proportions (11–12 m coach)", "Detailed exterior panels and trim", "Proper wheels and tyres", "Windows with security bars",
           "Headlights and tail lights", "Mirrors", "Doors (front entry; animated or posed open for escort)", "Interior seating where visible",
           "Driver area where visible", "PBR metal, glass, rubber and paint materials", "Prison transport details consistent with the story (livery, cage, window guards)",
           "Gameplay and cinematic interaction points preserved (CH01_M01_CS01 SH01–SH03)", "Placement and collision tested in Godot",
           "Exterior and interior screenshots captured", "Properly licensed source recorded"]
    rows += [req(f"P03-BUS-{i+1:03}", "7", t, "05", ["scripts/world/env_intake.gd", "assets/props/phase025/blackridge_transport_bus.glb"],
                 "Bus recognisable as a detailed realistic prison transport, not placeholder geometry", GFX + " (bus, bus_interior, bus_front)") for i, t in enumerate(bus)]

    court = ["Correct court proportions (28 x 15 m)", "Believable worn asphalt/concrete surface", "Proper basketball markings", "Realistic hoops",
             "Detailed backboards", "Rim geometry", "Net geometry", "Support poles", "Fencing", "Yard lighting", "Surface wear", "Environmental dirt",
             "Prison-yard details (benches, perimeter wall, razor wire, tower)", "Court remains traversable", "Mission triggers and NPC navigation preserved", "Before-and-after screenshots"]
    rows += [req(f"P03-COURT-{i+1:03}", "8", t, "06", ["scripts/world/prison_court.gd", "scripts/world/env_yard.gd"],
                 "Believable outdoor prison court; gameplay-functional", GFX + " (yard, court_layout, hoop_detail, court_ground) + M02 autopilot") for i, t in enumerate(court)]

    envs = [("INTAKE", "Intake", "scripts/world/env_intake.gd"), ("CELL", "Cell Block A", "scripts/world/env_cellblock.gd"), ("YARD", "Prison Yard", "scripts/world/env_yard.gd"),
            ("WORK", "Laundry Workshop", "scripts/world/env_workshop.gd"), ("MAINT", "Maintenance Network", "scripts/world/env_maintenance.gd"),
            ("SEC", "Mission-specific security areas (restricted corridor, solitary)", "scripts/world/env_solitary.gd")]
    aspects = ["Modular architecture", "Walls", "Floors", "Ceilings", "Doors", "Windows", "Railings", "Stairs", "Furniture", "Machinery", "Security equipment",
               "Pipes", "Cables", "Signs", "Surface wear", "Environmental detail", "PBR albedo/normal/roughness/metallic", "Correct UV scale", "Material variation",
               "No prominent placeholder geometry"]
    for code, name, f in envs:
        rows.append(req(f"P03-ENV-{code}-000", "9", f"{name}: visually coherent, believable, correctly scaled", "03", [f, EB],
                        "Independent review of matched before/after captures passes", GFX, "P0"))
        for i, a in enumerate(aspects, 1):
            rows.append(req(f"P03-ENV-{code}-{i:03}", "9", f"{name}: {a}", "03" if i < 17 else "04", [f, EB], f"{a} believable for the room's age and maintenance", GFX, "P2", False))

    light = ["WorldEnvironment configured per level", "Interior lighting from visible fixtures", "Exterior sunlight", "Shadow quality (soft, stable)",
             "Reflections (sky/probe)", "Ambient occlusion", "Exposure / tonemapping", "Colour grading", "Fog where appropriate", "Volumetric lighting where feasible",
             "Gameplay elements remain visible", "Daytime and night mission scenes tested", "Rendering settings recorded", "Consistent before/after images"]
    rows += [req(f"P03-LIGHT-{i+1:03}", "10", t, "04", [EB, "project.godot", "scripts/core/settings.gd"], t + " — reviewed in captures", GFX) for i, t in enumerate(light)]

    ai = ["Patrol routes", "Suspicion", "Investigation", "Vision detection", "Hearing detection", "Search behaviour", "Chase behaviour", "Return to patrol",
          "Mission-specific scripted behaviour", "Guards cannot see through solid walls", "NPC placement and orientation", "NPC animation (no motionless idle during active scenes)",
          "Navigation valid after environment changes"]
    rows += [req(f"P03-AI-{i+1:03}", "12", t, "07", ["scripts/npc/guard_ai.gd", "scripts/npc/npc.gd"], t + " demonstrated in a test", "System suite guard tests + mission autopilot") for i, t in enumerate(ai)]

    cin = ["Reconcile 145 dialogue lines / 36 shots against canonical files", "Camera framing", "Character blocking", "Facial orientation", "Gestures",
           "Subtitle timing", "Scene transitions", "Audio cues", "Gameplay restoration after cutscenes", "Co-operative cutscene behaviour (both ready)",
           "No invented replacement dialogue", "Complete Chapter 1 story sequence plays in-game"]
    rows += [req(f"P03-CIN-{i+1:03}", "13", t, "08", ["scripts/chapter/cinematic_director.gd", "scripts/chapter/dialogue_director.gd"], t, "Full chapter run event log + shot screenshots") for i, t in enumerate(cin)]

    aud = ["Footsteps by surface type", "Prison ambience", "Doors and gates", "Machinery", "Guard radio sounds", "Yard ambience", "Alarms", "Environmental effects",
           "Cinematic audio cues", "Positional audio where appropriate", "Balanced levels", "No repetitive/excessive effects", "Subtitle accessibility preserved"]
    rows += [req(f"P03-AUD-{i+1:03}", "14", t, "09", ["scripts/core/audio_director.gd"], t, "Audio cue log in chapter run + listening review (human)") for i, t in enumerate(aud)]

    perf = ["FPS measured in real gameplay", "Frame-time stability", "CPU usage", "GPU usage where measurable", "Memory usage", "Scene loading time",
            "Split-screen performance", "Rendering bottlenecks identified", "Mesh complexity optimised", "Texture memory", "Shadow settings", "Material count",
            "Visibility ranges / LOD", "Navigation cost", "Collision cost", "Test hardware and settings documented"]
    rows += [req(f"P03-PERF-{i+1:03}", "15", t, "10", [EB, "project.godot", "tests/phase03/perf_capture.gd"], t + " recorded", "tests/phase03/perf_capture + chapter_gfx wall_frame_cadence") for i, t in enumerate(perf)]

    qa = ["Static validation (GDScript parse of all scripts)", "Godot import checks", "Automated gameplay tests", "Graphical tests", "Mission regression",
          "Split-screen tests", "Save/load tests", "Visual inspections", "Performance tests", "Windows export succeeds", "Exported executable actually tested",
          "Independent reviewer per milestone", "Up to five repair attempts recorded before blocker", "No fabricated results"]
    rows += [req(f"P03-QA-{i+1:03}", "16-17", t, "11" if i in (7, 11, 12, 13) else "10", ["tools/phase03_run_regressions.sh", "export_presets.cfg"], t, "See docs/phase03/SESSION_STATE.md commands", "P0" if i in (9, 10) else "P1") for i, t in enumerate(qa)]

    proc = [("Requirements matrix, JSON, session state and defect queue exist", ["docs/phase03/REQUIREMENTS_MATRIX.md", "docs/phase03/requirements.json", "docs/phase03/SESSION_STATE.md", "docs/phase03/DEFECT_QUEUE.md"]),
            ("Visual evidence folder with before/after for each major improvement", ["docs/phase03/visual_evidence"]),
            ("VISUAL_QUALITY_REPORT describes actual improvements and remaining problems", ["docs/phase03/VISUAL_QUALITY_REPORT.md"]),
            ("Automated completion audit fails while mandatory requirements are unverified", ["tools/phase03_completion_audit.py"]),
            ("Session continuity: next session can resume without repeating verified work", ["docs/phase03/SESSION_STATE.md"]),
            ("Final deliverables: launch and testing instructions", ["docs/phase03/LAUNCH_AND_TEST.md"])]
    rows += [req(f"P03-PROC-{i+1:03}", "3,18-22", t, "00", f, t, "File inspection + audit run") for i, (t, f) in enumerate(proc)]
    return rows


def mission_requirements():
    rows = []
    missions = json.loads((R / "data/ch01/missions.json").read_text(encoding="utf-8"))["missions"]
    aspects = ["Correct environment", "Player spawning", "Objectives", "NPC behaviour", "Cooperative interactions", "Mission triggers", "Dialogue",
               "Cinematics", "Failure states", "Checkpoints", "Completion conditions", "Next mission transition"]
    for i, m in enumerate(missions, 1):
        f = [f"scripts/missions/mission_0{i}.gd"]
        rows.append(req(f"P03-MIS-0{i}-000", "11", f"{m['id']} {m.get('title', '')}: playable through its intended sequence", "01", f,
                        "Mission completes in graphical autopilot run with no skipped story events", AUTO, "P0", mission_id=m["id"]))
        for j, a in enumerate(aspects, 1):
            rows.append(req(f"P03-MIS-0{i}-{j:03}", "11", f"{m['id']}: {a}", "01", f, f"{a} validated", AUTO, "P1", mission_id=m["id"]))
        for o in m["objectives"]:
            rows.append(req(f"P03-OBJ-{o['id']}", "11", f"Objective {o['id']}: {o.get('text', '')}", "01", f, "objective_set and objective_completed events in order", AUTO, "P1",
                            mission_id=m["id"], objective_id=o["id"]))
    for l in json.loads((R / "data/ch01/dialogue.json").read_text(encoding="utf-8"))["lines"]:
        rows.append(req(f"P03-DLG-{l['id']}", "13", f"{l['speaker']}: {l['text'][:70]}", "08", ["data/ch01/dialogue.json", "scripts/chapter/dialogue_director.gd"],
                        "Canonical line shown in-game when its condition occurs", "Chapter run event log dialogue_shown", "P1" if l.get("main") else "P2",
                        bool(l.get("main")), dialogue_id=l["id"], condition=l.get("condition", "")))
    for s in json.loads((R / "data/ch01/shots.json").read_text(encoding="utf-8"))["shots"]:
        rows.append(req(f"P03-SHOT-{s['id']}", "13", f"{s['id']}: {s['camera']}", "08", ["data/ch01/shots.json", "scripts/chapter/cinematic_director.gd"],
                        "Shot activates in its cinematic with the registered lens", "Chapter run event log shot_activated + screenshot", "P1", shot_id=s["id"]))
    return rows


def asset_rows():
    """Re-home the earlier asset-pass rows (P03-BUS-001 etc. there) as P03-A-* so they keep their history."""
    rows = []
    legacy = DOC / "REQUIREMENTS_MATRIX_ASSETS_20261019.md"
    src = legacy if legacy.exists() else DOC / "REQUIREMENTS_MATRIX.md"
    if not src.exists():
        return rows
    text = src.read_text(encoding="utf-8", errors="replace")
    if "P03-A-" in text and src.name == "REQUIREMENTS_MATRIX.md":
        return rows
    if src.name == "REQUIREMENTS_MATRIX.md":
        legacy.write_text(text, encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"\| (P03-[A-Z]+-\d{3}) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", line)
        if not m:
            continue
        old, item, source, owner, evidence, status = m.groups()
        status = status.replace("�", "-").replace("—", "-").strip()
        st = {"IMPLEMENTED - NOT VERIFIED": "IMPLEMENTED_UNTESTED", "IN PROGRESS": "IN_PROGRESS"}.get(status, status.replace(" ", "_"))
        if st not in STATUSES:
            st = "IN_PROGRESS"
        note = f"Imported from earlier matrix row {old}; status as recorded there."
        if st == "VERIFIED":
            st = "IMPLEMENTED_UNTESTED"
            note = f"Imported from earlier matrix row {old}, which self-reported VERIFIED without an independent verdict; re-review required."
        rows.append({"id": "P03-A-" + old[4:], "source": "Phase 03 asset-acquisition request (2026-10-19, earlier session)", "requirement": item, "priority": "P1",
                     "mandatory": True, "owner": "Agent 03 Environment/Assets", "implementation_files": [], "acceptance_criteria": item,
                     "test_procedure": "Asset pipeline + graphical review", "evidence": [evidence], "status": st,
                     "notes": note})
    return rows


def load(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def main():
    old = {r["id"]: r for r in load(STORE, {"requirements": []})["requirements"]}
    rows = prompt_requirements() + mission_requirements()
    a_rows = asset_rows()
    if not a_rows:
        a_rows = [r for r in old.values() if r["id"].startswith("P03-A-")]
    rows += a_rows
    verdicts = load(VERDICTS, {"verdicts": []})["verdicts"]
    runtime = load(RUNTIME, {"items": {}})["items"]
    by_id = {}
    for r in rows:
        prev = old.get(r["id"])
        if prev:
            for k in ("status", "evidence", "notes", "qa"):
                if k in prev:
                    r[k] = prev[k]
        if r["id"] in runtime:
            ev = runtime[r["id"]]
            for e in ev.get("evidence", []):
                if e not in r["evidence"]:
                    r["evidence"].append(e)
            if r["status"] in ("NOT_STARTED", "IN_PROGRESS") and ev.get("status"):
                r["status"] = ev["status"]
            elif ev.get("status") == "FAILED" and r["status"] != "VERIFIED":
                r["status"] = "FAILED"
        by_id[r["id"]] = r
    for v in verdicts:
        r = by_id.get(v["id"])
        if not r:
            continue
        r["qa"] = v
        if v.get("reviewer", "") == r["owner"]:
            r["qa"]["rejected"] = "reviewer is the owner; self-verification not accepted"
            continue
        if v["verdict"] in ("VERIFIED", "FAILED", "BLOCKED"):
            r["status"] = v["verdict"]
    if len(sys.argv) > 2 and sys.argv[1] == "--set":
        rid, st = sys.argv[2], sys.argv[3]
        assert st in STATUSES and st != "VERIFIED", "VERIFIED only through docs/phase03/qa_verdicts.json"
        r = by_id[rid]
        r["status"] = st
        args = sys.argv[4:]
        while args:
            k = args.pop(0)
            if k == "--evidence":
                r["evidence"].append(args.pop(0))
            elif k == "--note":
                r["notes"] = args.pop(0)
    out = {"generated_by": "tools/phase03_requirements.py", "statuses": STATUSES, "requirements": list(by_id.values())}
    STORE.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    render(out)
    print(f"requirements: {len(by_id)}")


def render(out):
    from collections import Counter
    reqs = out["requirements"]
    st = Counter(r["status"] for r in reqs)
    md = ["# Phase 03 requirements matrix", "",
          "Generated by `tools/phase03_requirements.py` from the Phase 03 master prompt, the canonical Chapter 1 data in `data/ch01/` and the earlier",
          "Phase 03 asset rows (kept as `P03-A-*`; original matrix preserved in `REQUIREMENTS_MATRIX_ASSETS_20261019.md`). Machine-readable store:",
          "`requirements.json`. VERIFIED is only set from an independent QA verdict in `qa_verdicts.json` whose reviewer is not the owner.", "",
          "| Status | Count |", "|---|---|"] + [f"| {s} | {st.get(s, 0)} |" for s in STATUSES] + [f"| **Total** | **{len(reqs)}** |", ""]
    groups = {}
    for r in reqs:
        g = r["id"].split("-")[1]
        groups.setdefault(g, []).append(r)
    names = {"PLAY": "Milestone 01 — playability", "CHAR": "Milestone 02 — characters and animation", "BUS": "Milestone 03 — prison bus",
             "COURT": "Milestone 04 — basketball court", "ENV": "Milestone 05 — prison environments", "LIGHT": "Milestone 06 — lighting",
             "MIS": "Milestone 07 — missions", "OBJ": "Milestone 07 — objectives", "AI": "Milestone 08 — NPC and guard AI", "CIN": "Milestone 09 — cinematics",
             "DLG": "Milestone 09 — canonical dialogue lines", "SHOT": "Milestone 09 — canonical camera shots", "AUD": "Milestone 10 — audio",
             "PERF": "Milestone 11 — performance", "QA": "Milestone 12 — QA and Windows build", "PROC": "Process and deliverables", "A": "Earlier Phase 03 asset rows"}
    for g, items in groups.items():
        md += [f"## {names.get(g, g)}", "", "| ID | Requirement | Pri | Owner | Implementation | Acceptance | Test | Evidence | Status |", "|---|---|---|---|---|---|---|---|---|"]
        for r in items:
            ev = "<br>".join(r["evidence"][:3]) + (f" (+{len(r['evidence']) - 3})" if len(r["evidence"]) > 3 else "")
            cell = lambda x: str(x).replace("|", "/").replace("\n", " ")
            md.append(f"| {r['id']} | {cell(r['requirement'])} | {r['priority']} | {r['owner'].split(' ')[1]} | {cell(', '.join(f'`{f}`' for f in r['implementation_files'][:2]))} | "
                      f"{cell(r['acceptance_criteria'])} | {cell(r['test_procedure'])} | {cell(ev) or '—'} | {r['status']} |")
        md.append("")
    (DOC / "REQUIREMENTS_MATRIX.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
