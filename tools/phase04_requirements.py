"""Phase 04 requirements registry generator.

Sources (none silently removed):
  1. The Phase 04 master prompt clauses below (P04-<GROUP>-NNN).
  2. Every Phase 03 row (docs/phase03/requirements.json) carried forward as P04-C-<phase03 id>, keeping its Phase 03
     status and evidence for reference in `phase03_status`, but starting Phase 04 at IMPLEMENTED_UNTESTED (if it had
     runtime evidence) or its earlier state: the Phase 04 prompt forbids trusting earlier reports without fresh review.
  3. Conflicts recorded in docs/phase04/CONFLICTS.md (authoritative source named per conflict).

Status/evidence/notes persist across regenerations. Runtime evidence merges from docs/phase04/runtime_evidence.json and
independent verdicts from docs/phase04/qa_verdicts.json (reviewer must differ from the owner).

    python -I tools/phase04_requirements.py
    python -I tools/phase04_requirements.py --set ID STATUS [--evidence PATH] [--note TEXT]
"""
import json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
DOC = R / "docs/phase04"
STORE = DOC / "requirements.json"
STATUSES = ["NOT_STARTED", "IN_PROGRESS", "IMPLEMENTED_UNTESTED", "FAILED", "BLOCKED", "VERIFIED"]
OWN = {"00": "Agent 00 Orchestrator", "01": "Agent 01 Gameplay", "02": "Agent 02 Multiplayer", "03": "Agent 03 Character TA",
       "04": "Agent 04 Animation", "05": "Agent 05 Environment", "06": "Agent 06 Asset Integration", "07": "Agent 07 Rendering/Lighting",
       "08": "Agent 08 NPC/Guard AI", "09": "Agent 09 Missions", "10": "Agent 10 Cinematics", "11": "Agent 11 Audio",
       "12": "Agent 12 UI/Accessibility", "13": "Agent 13 Performance/Build", "14": "Agent 14 Independent QA"}


def row(rid, sec, text, owner, files, accept, test, pri="P1", deps=None, mandatory=True):
    return {"id": rid, "source": f"Phase 04 master prompt §{sec}", "description": text, "priority": pri, "mandatory": mandatory,
            "owner": OWN[owner], "implementation_paths": files, "dependencies": deps or [], "acceptance_criteria": accept,
            "test_method": test, "evidence": [], "status": "NOT_STARTED", "notes": ""}


def prompt_rows():
    rows = []
    def group(code, sec, owner, files, test, items, pri="P1", deps=None):
        for i, (t, a) in enumerate(items, 1):
            rows.append(row(f"P04-{code}-{i:03}", sec, t, owner, files, a, test, pri, deps))
    group("BASE", "2-3", "00", ["docs/phase04/BASELINE_AUDIT.md"], "Fresh launch + recorded classification",
          [("Recoverable checkpoint before major modifications", "Commit of the Phase 03 state exists"),
           ("Project imports", "Headless import completes without errors"), ("Main menu opens", "Graphical launch shows menu"),
           ("New Game works", "Real button click starts M01"), ("Both players spawn", "Two characters grounded at spawns"),
           ("Movement works", "Gameplay regressions pass"), ("Split-screen works", "Two viewports render"), ("Mission objectives work", "Objective events"),
           ("Characters animate", "Clips play in screenshots"), ("Guard AI works", "Detection tests"), ("Cutscenes play", "shot_activated events"),
           ("Save/load works", "Checkpoint regressions"), ("No crash", "Logs free of crash"), ("Windows export exists", "Executable present and run"),
           ("Baseline gameplay screenshots captured", "docs/phase04/visual_evidence/baseline/"), ("BASELINE_AUDIT classifies systems WORKING/PARTIAL/BROKEN/MISSING/NOT_TESTED", "File present")], "P0")
    group("PLAY", "6", "01", ["scripts/player/player.gd", "scripts/player/player_camera.gd", "scripts/ui/main_menu.gd", "scripts/core/save_service.gd"],
          "Regression battery + first-objective test + graphical review",
          [(t, t + " verified in the running game") for t in ["Main menu", "New Game", "Character spawning", "Third-person movement", "Running", "Sprinting",
           "Crouching", "Jumping", "Camera rotation", "Collision", "Interactions", "Mission objectives", "Checkpoints", "Save/load",
           "Players cannot fall through the environment", "Players cannot become trapped in collision", "Movement tested with actual character models",
           "Fresh game reaches and completes the first real objective"]], "P0")
    group("COOP", "7", "02", ["scripts/chapter/chapter_root.gd", "scripts/core/device_router.gd", "scripts/ui/devices_panel.gd"],
          "System suite device/split tests + cooperative mission runs (+ human two-controller test)",
          [(t, t + " works without one player controlling the other") for t in ["Horizontal split-screen option", "Two independent cameras",
           "Two independent characters", "Keyboard/mouse plus controller", "Two-controller support", "Shared world state", "Cooperative doors",
           "Timed puzzles", "Assisted traversal", "Shared mission objectives", "Cutscene skip voting", "Checkpoint synchronization",
           "No input cross-contamination", "Simultaneous two-player test", "Disconnect / reconnect behaviour"]], "P0")
    group("CHAR", "8", "03", ["scripts/player/character_visual.gd", "assets/characters/"], "In-engine captures reviewed against docs/characters/*.md",
          [(t, t) for t in ["Adrian: realistic proportions", "Noah: realistic proportions", "Detailed clothing", "Correct materials", "Correct skeletons",
           "Proper skin weights", "Believable faces and hair", "Appropriate prison outfits (per character documents)", "Adrian likeness per ADRIAN_CROSS.md (short dark hair, grey temple, eyebrow cut)",
           "Noah likeness per NOAH_REYES.md"]], "P1")
    group("ANIM", "8", "04", ["scripts/player/character_visual.gd", "scripts/player/player.gd"], "Graphical animation review (movement_visual + chapter shots)",
          [(t, t + " clip plays and looks correct") for t in ["Idle", "Walk", "Run", "Sprint", "Crouch", "Jump", "Land", "Turn", "Sit", "Stand", "Open door",
           "Pick up", "Push", "Pull", "Climb", "Cooperative assistance", "Combat reactions", "Cinematic gestures", "No T-poses", "No foot sliding",
           "No floating", "No limb deformation", "No broken clothing", "No animation snapping", "Correct character orientation"]], "P1")
    group("BUS", "9", "06", ["assets/props/phase03/blackridge_transport_bus_p03.glb", "scripts/world/env_intake.gd"], "Exterior + interior captures, collision test",
          [(t, t) for t in ["Realistic exterior", "Correct dimensions", "Wheels and tyres", "Windows", "Mirrors", "Headlights", "Doors (functional or posed)", "Driver area",
           "Interior seating", "Realistic materials", "Appropriate collision", "Correct cinematic placement", "Not a primitive box with wheels", "Licence recorded",
           "Gameplay triggers preserved", "Exterior and interior screenshots"]], "P1")
    group("COURT", "10", "05", ["scripts/world/prison_court.gd", "scripts/world/env_yard.gd"], "Player-level captures + M02 run",
          [(t, t) for t in ["Believable dimensions", "Worn asphalt or concrete", "Accurate markings", "Detailed backboards", "Realistic rims", "Net geometry",
           "Hoop supports", "Fencing", "Yard lighting", "Surrounding detail", "No low-poly placeholder hoops", "NPC navigation preserved", "Mission interactions preserved",
           "Player-level screenshots"]], "P1")
    for code, name, f in [("INTAKE", "Prison intake", "env_intake.gd"), ("CELL", "Cell Block A", "env_cellblock.gd"), ("YARD", "Prison yard", "env_yard.gd"),
                          ("WORK", "Laundry workshop", "env_workshop.gd"), ("MAINT", "Maintenance corridors", "env_maintenance.gd"), ("SEC", "Security areas", "env_solitary.gd")]:
        group(f"ENV-{code}", "11", "05", [f"scripts/world/{f}"], "Matched captures + mission run",
              [(f"{name}: {t}", f"{t} realistic, correctly scaled, collision/navigation intact") for t in ["walls", "floors", "ceilings", "doors", "railings", "stairs",
               "cells", "furniture", "industrial machinery", "security equipment", "pipes", "ventilation", "lighting fixtures", "signage", "dirt and wear",
               "no undocumented greybox"]], "P1")
    group("LIGHT", "12", "07", ["scripts/world/env_builder.gd", "project.godot"], "Before/after captures; objective visibility check",
          [(t, t) for t in ["WorldEnvironment", "Interior and exterior lighting", "Shadows", "Reflections", "Ambient occlusion", "Exposure", "Tonemapping",
           "Colour grading", "Atmospheric effects", "Texture scale", "Normal maps", "Roughness", "Metallic response", "No excessive bloom/flat light/overexposure",
           "Objectives and characters remain visible", "Consistent before/after screenshots"]], "P1")
    group("AI", "13", "08", ["scripts/npc/guard_ai.gd", "scripts/npc/npc.gd"], "AI tests in mission environments",
          [(t, t) for t in ["Patrol routes", "Suspicion", "Investigation", "Vision", "Hearing", "Alert", "Chase", "Search", "Return to patrol",
           "Mission-specific NPC behaviour", "Detection respects solid geometry", "Both players detectable independently", "NPC animation and navigation"]], "P1")
    for i, name in enumerate(["New Blood", "Trouble in the Yard", "The Workshop", "Lights Out", "Behind the Walls", "The Betrayal"], 1):
        group(f"MIS-0{i}", "14", "09", [f"scripts/missions/mission_0{i}.gd"], "Mission run (graphical) + checkpoint restore",
              [(f"M0{i} {name}: {t}", t) for t in ["correct starting state", "spawn points", "objectives", "interactions", "cooperative actions", "NPC behaviour",
               "dialogue triggers", "cutscenes", "failure and retry", "checkpoints", "save/load", "completion", "transition to next mission"]], "P0")
    group("CIN", "15", "10", ["scripts/chapter/cinematic_director.gd", "scripts/chapter/dialogue_director.gd"], "Event log + screenshot review",
          [(t, t) for t in ["Reconcile dialogue/shot counts with files", "All dialogue plays in-game", "Subtitles", "Camera shots", "Character blocking",
           "Gestures", "Scene transitions", "Audio cues", "Cutscene triggers", "Gameplay restoration", "Cutscenes tested solo-config and co-op", "No unnecessary dialogue rewrites"]], "P1")
    group("AUD", "16", "11", ["scripts/core/audio_director.gd"], "Cue log + human listening review",
          [(t, t) for t in ["Footsteps by surface", "Prison ambience", "Doors and gates", "Machinery", "Guard radios", "Yard ambience", "Alarms", "Cinematic cues", "Spatial audio"]], "P2")
    group("UI", "16", "12", ["scripts/ui/main_menu.gd", "scripts/ui/hud.gd", "scripts/ui/pause_menu.gd"], "UI walkthrough (graphical)",
          [(t, t + " works as advertised and is readable in split-screen") for t in ["Main menu", "New Game", "Continue", "Co-op setup", "Pause", "Settings",
           "Objective HUD", "Interaction prompts", "Subtitles", "Mission completion", "Every visible control performs its function"]], "P1")
    group("PT", "17", "09", ["tests/phase02/autopilot.gd"], "Full chapter run from a fresh save (graphical, exported build) + human playthrough",
          [(t, t) for t in ["Fresh save M01→M06", "Both characters used", "Cooperative puzzles", "Guard encounters", "All objectives", "Dialogue", "Cutscenes",
           "Save/load mid-chapter", "Checkpoints", "Mission transitions", "Chapter completion", "Automated agent uses real mechanics (no completion flags)"]], "P0")
    group("PERF", "18", "13", ["tests/phase03/perf_capture.gd", "project.godot"], "Real-time perf capture per mission",
          [(t, t) for t in ["Rendering optimised", "Geometry", "Textures", "Materials", "Shadows", "Split-screen viewports", "Navigation", "Collision",
           "Scene loading", "Audio memory", "Stable 60 FPS on reference hardware", "Measurements and hardware recorded"]], "P1")
    group("BUILD", "18", "13", ["export_presets.cfg"], "Export + run exported executable through gameplay",
          [("Windows executable exported", "Export completes"), ("Executable launches", "Runs to menu"), ("Actual gameplay works in the executable", "Full chapter on exe")], "P0")
    group("QA", "19-22", "14", ["docs/phase04/qa_verdicts.json", "tools/phase04_completion_audit.py"], "Independent reviewer",
          [(t, t) for t in ["Independent QA per milestone", "Up to five repair cycles before escalation", "No fabricated evidence", "Visual evidence for all listed subjects",
           "VISUAL_QUALITY_REPORT distinguishes geometry from lighting-only change", "Completion audit fails while mandatory rows unverified",
           "No self-verification", "SESSION_STATE updated after major tasks", "Final QA report", "Remaining blocker list", "Launch and test instructions",
           "Independent QA approves the release candidate"]], "P0")
    return rows


def carried_rows():
    p3 = json.loads((R / "docs/phase03/requirements.json").read_text(encoding="utf-8"))["requirements"]
    out = []
    for r in p3:
        st = r["status"]
        # Nothing carries VERIFIED into Phase 04: a Phase 04 verdict is required (prompt §1, §21).
        start = "IMPLEMENTED_UNTESTED" if st in ("VERIFIED", "IMPLEMENTED_UNTESTED") else st
        out.append({"id": "P04-C-" + r["id"], "source": f"Carried from Phase 03 ({r['source']})", "description": r["requirement"], "priority": r["priority"],
                    "mandatory": r.get("mandatory", True), "owner": "Agent 00 Orchestrator", "implementation_paths": r.get("implementation_files", []),
                    "dependencies": [], "acceptance_criteria": r["acceptance_criteria"], "test_method": r["test_procedure"], "evidence": list(r.get("evidence", [])),
                    "status": start, "phase03_status": st, "notes": "Phase 04 requires fresh independent review (prompt §1)."})
    return out


def load(p, d):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d


def main():
    DOC.mkdir(parents=True, exist_ok=True)
    old = {r["id"]: r for r in load(STORE, {"requirements": []})["requirements"]}
    rows = prompt_rows() + carried_rows()
    runtime = load(DOC / "runtime_evidence.json", {"items": {}})["items"]
    verdicts = load(DOC / "qa_verdicts.json", {"verdicts": []})["verdicts"]
    by = {}
    for r in rows:
        if r["id"] in old:
            for k in ("status", "evidence", "notes", "qa"):
                if k in old[r["id"]]:
                    r[k] = old[r["id"]][k]
        ev = runtime.get(r["id"])
        if ev:
            for e in ev["evidence"]:
                if e not in r["evidence"]:
                    r["evidence"].append(e)
            if ev["status"] == "FAILED" and r["status"] != "VERIFIED":
                r["status"] = "FAILED"
            elif r["status"] in ("NOT_STARTED", "IN_PROGRESS"):
                r["status"] = ev["status"]
        by[r["id"]] = r
    for v in verdicts:
        r = by.get(v["id"])
        if r is None:
            continue
        r["qa"] = v
        if v.get("reviewer") == r["owner"]:
            continue
        if v["verdict"] in ("VERIFIED", "FAILED", "BLOCKED"):
            r["status"] = v["verdict"]
    if len(sys.argv) > 3 and sys.argv[1] == "--set":
        assert sys.argv[3] in STATUSES and sys.argv[3] != "VERIFIED"
        r = by[sys.argv[2]]; r["status"] = sys.argv[3]
        a = sys.argv[4:]
        while a:
            k = a.pop(0)
            if k == "--evidence": r["evidence"].append(a.pop(0))
            elif k == "--note": r["notes"] = a.pop(0)
    out = {"generated_by": "tools/phase04_requirements.py", "statuses": STATUSES, "requirements": list(by.values())}
    STORE.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    render(out)
    print("requirements:", len(by))


def render(out):
    from collections import Counter
    reqs = out["requirements"]
    st = Counter(r["status"] for r in reqs)
    md = ["# Phase 04 requirements matrix", "", "Generated by `tools/phase04_requirements.py`. Store: `requirements.json`. Phase 03 rows are carried forward as",
          "`P04-C-*` (none removed) and must be re-verified. Conflicts and their authoritative sources: `CONFLICTS.md`.", "",
          "| Status | Count |", "|---|---|"] + [f"| {s} | {st.get(s, 0)} |" for s in STATUSES] + [f"| **Total** | **{len(reqs)}** |", ""]
    groups = {}
    for r in reqs:
        key = "C" if r["id"].startswith("P04-C-") else r["id"].split("-")[1]
        groups.setdefault(key, []).append(r)
    for g, items in groups.items():
        md += [f"## {g}", "", "| ID | Description | Pri | Owner | Paths | Deps | Acceptance | Test | Evidence | Status |", "|---|---|---|---|---|---|---|---|---|---|"]
        c = lambda x: str(x).replace("|", "/").replace("\n", " ")
        for r in items:
            ev = "<br>".join(r["evidence"][:2]) + (f" (+{len(r['evidence']) - 2})" if len(r["evidence"]) > 2 else "")
            md.append(f"| {r['id']} | {c(r['description'])} | {r['priority']} | {r['owner'].split(' ')[1]} | {c(', '.join(r['implementation_paths'][:2]))} | "
                      f"{c(', '.join(r['dependencies'])) or '—'} | {c(r['acceptance_criteria'])} | {c(r['test_method'])} | {c(ev) or '—'} | {r['status']} |")
        md.append("")
    (DOC / "REQUIREMENTS_MATRIX.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
