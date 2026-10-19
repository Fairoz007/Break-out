"""Build the Phase 02 master requirements registry from the canonical Chapter 1 documents.

Canonical IDs (scenes, missions, objectives, checkpoints, dialogue lines, camera shots) are parsed from the
screenplay and mission files, never typed by hand. System requirements are authored below with their source.
Re-running merges with the existing registry: status, blocking_issues, evidence and qa fields are preserved.

python -I tools/phase02_build_registry.py
Outputs docs/PHASE_02_REQUIREMENTS.json and docs/PHASE_02_REQUIREMENTS_MATRIX.md
"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
DOC = R / 'docs'
OUT_JSON = DOC / 'PHASE_02_REQUIREMENTS.json'
OUT_MD = DOC / 'PHASE_02_REQUIREMENTS_MATRIX.md'
STATUSES = ['NOT_STARTED', 'IN_PROGRESS', 'IMPLEMENTED_UNTESTED', 'TEST_FAILED', 'BLOCKED', 'VERIFIED']
PHASE02 = 'Phase 02 protocol (user prompt, 2026-10-19)'
MISSION_NAMES = {1: 'NEW BLOOD', 2: 'TROUBLE IN THE YARD', 3: 'THE WORKSHOP', 4: 'LIGHTS OUT', 5: 'BEHIND THE WALLS', 6: 'THE BETRAYAL'}

# ---------------------------------------------------------------- canonical parsing
dlg_md = (DOC / 'screenplay/CH01_DIALOGUE.md').read_text(encoding='utf-8')
DIALOGUE = []
for m in re.finditer(r'^\| (CH01_M0(\d)_DLG(\d{3})) \| ([A-Z]+) \| ([\d.]+)–([\d.]+)s \| ([^|]+) \| (.+?) \|\s*$', dlg_md, re.M):
    DIALOGUE.append(dict(id=m[1], mission=int(m[2]), speaker=m[4], start=float(m[5]), end=float(m[6]), condition=m[7].strip(), text=m[8].strip()))
script = (DOC / 'screenplay/CH01_FULL_SCRIPT.md').read_text(encoding='utf-8')
script_lines = {m[1]: (m[2], m[3]) for m in re.finditer(r'\[(CH01_M0\d_DLG\d{3})\] ([A-Z]+) \([^)]*\): "(.+)"', script)}
shots_md = (DOC / 'screenplay/CH01_CAMERA_SHOTS.md').read_text(encoding='utf-8')
SHOTS = [dict(id=m[1], mission=int(m[2]), reel=m[3], camera=m[4].strip(), direction=m[5].strip())
         for m in re.finditer(r'^\| (CH01_M0(\d)_CS01_SH\d\d) \| ([^|]+) \| ([^|]+) \| (.+?) \|\s*$', shots_md, re.M)]
MISSIONS, OBJECTIVES, CHECKPOINTS = [], [], []
for i in range(1, 7):
    md = (DOC / f'missions/CH01_MISSION_0{i}.md').read_text(encoding='utf-8')
    trig = re.search(r'## Objective and cinematic triggers\s+(.+?)\n', md).group(1)
    seq = re.search(r'## Exact playable sequence and ownership\s+(.+?)\n', md).group(1)
    gates = re.search(r'Cooperative gates: (.+?)\n', md).group(1)
    fail = re.search(r'## Checkpoints, failure and retry\s+(.+?)\n', md).group(1)
    exit_ = re.search(r'## Exit state and next mission\s+(.+?)\n', md).group(1)
    dur = re.search(r'Duration: (.+?)\n', md).group(1)
    MISSIONS.append(dict(n=i, id=f'CH01_M0{i}', scene=f'CH01_M0{i}_SC01', cine=f'CH01_M0{i}_CS01', name=MISSION_NAMES[i],
                         sequence=seq, gates=gates, triggers=trig, failure=fail, exit=exit_, duration=dur, doc=f'docs/missions/CH01_MISSION_0{i}.md'))
    objs = re.findall(r'OBJ(\d{3}) (.+?)(?=; OBJ\d{3}|\. |; CS01| CS01|\.$)', trig.split('IDs are')[0])
    for num, text in objs:
        OBJECTIVES.append(dict(id=f'CH01_M0{i}_OBJ{num}', mission=i, text=text.strip(' ;.'), doc=f'docs/missions/CH01_MISSION_0{i}.md'))
    for cp in ('A', 'B'):
        CHECKPOINTS.append(dict(id=f'CP0{i}_{cp}', mission=i, doc=f'docs/missions/CH01_MISSION_0{i}.md',
                                text=('scene entry' if cp == 'A' else re.search(rf'CP0{i}_B ([^.;]+)', fail).group(1))))  # specific placement from the failure section
STAGING = {f'CH01_M0{m[1]}_SC01': m[2] for m in re.finditer(r'## CH01_M0(\d)_SC01.*?\*\*Dialogue staging:\*\* (.+?)\n', script, re.S)}

# ---------------------------------------------------------------- implementation file map (planned / actual)
F = {
    'project': 'project.godot',
    'state': 'scripts/core/game_state.gd', 'save': 'scripts/core/save_service.gd', 'devices': 'scripts/core/device_router.gd',
    'dialogue_db': 'scripts/core/dialogue_db.gd', 'audio': 'scripts/core/audio_director.gd', 'settings': 'scripts/core/settings.gd',
    'chapter': 'scripts/chapter/chapter_root.gd', 'chapter_scene': 'scenes/chapter/chapter_root.tscn', 'main_scene': 'scenes/main.tscn',
    'director': 'scripts/chapter/mission_director.gd', 'cine': 'scripts/chapter/cinematic_director.gd', 'dlg_dir': 'scripts/chapter/dialogue_director.gd',
    'split': 'scripts/chapter/split_screen.gd', 'player': 'scripts/player/player.gd', 'pcam': 'scripts/player/player_camera.gd',
    'visual': 'scripts/player/character_visual.gd', 'npc': 'scripts/npc/npc.gd', 'guard': 'scripts/npc/guard_ai.gd',
    'interact': 'scripts/world/interactable.gd', 'builder': 'scripts/world/env_builder.gd',
    'env_intake': 'scripts/world/env_intake.gd', 'env_cell': 'scripts/world/env_cellblock.gd', 'env_yard': 'scripts/world/env_yard.gd',
    'env_work': 'scripts/world/env_workshop.gd', 'env_maint': 'scripts/world/env_maintenance.gd', 'env_solitary': 'scripts/world/env_solitary.gd',
    'hud': 'scripts/ui/hud.gd', 'subs': 'scripts/ui/subtitles.gd', 'menu': 'scripts/ui/main_menu.gd', 'pause': 'scripts/ui/pause_menu.gd',
    'dlg_data': 'data/ch01/dialogue.json', 'shot_data': 'data/ch01/shots.json', 'mission_data': 'data/ch01/missions.json',
    'tests': 'tests/phase02/run_tests.gd', 'playthrough': 'tests/phase02/playthrough.gd', 'export': 'export_presets.cfg',
}
def mfile(i): return f'scripts/missions/mission_0{i}.gd'
def env_for(i): return {1: [F['env_intake'], F['env_cell']], 2: [F['env_yard']], 3: [F['env_work']], 4: [F['env_cell'], F['env_maint']],
                        5: [F['env_maint']], 6: [F['env_maint'], F['env_solitary']]}[i]
EV = 'tests/phase02/evidence/'

# ---------------------------------------------------------------- system requirements (authored, with source)
SYS = [
 # id, category, source, section, description, priority, deps, agent, files, acceptance, test
 ('REQ-ARCH-001', 'architecture', 'docs/technical/SCENE_ARCHITECTURE.md', 'Future authored hierarchy', 'Chapter01Root owns MissionDirector, environment root, two PlayerRoot instances, NPC director, interactable registry, DialogueDirector, CinematicDirector and CheckpointService; one authoritative world simulation.', 'P0', [], 'A1-Foundation', ['chapter', 'chapter_scene', 'director', 'cine', 'dlg_dir', 'state'], 'Scene tree contains each service once; mission/NPC logic runs once regardless of viewport count.', 'Automated scene-tree inspection test; code review.'),
 ('REQ-ARCH-002', 'architecture', 'docs/technical/SCENE_ARCHITECTURE.md', 'MissionDirector', 'MissionDirector alone advances objective state; visuals never set plot flags; signals carry stable IDs; transitions are idempotent.', 'P0', ['REQ-ARCH-001'], 'A4-Story', ['director', 'state'], 'Repeated/duplicate interaction events do not double-advance objectives; only director writes objective flags.', 'Automated idempotency test (duplicate events).'),
 ('REQ-ARCH-003', 'architecture', 'docs/technical/SCENE_ARCHITECTURE.md', 'Resources proposed', 'Dialogue lines, missions and shots are data resources with stable IDs generated from canonical documents; no runtime parsing of external archives.', 'P0', [], 'A4-Story', ['dlg_data', 'shot_data', 'mission_data', 'dialogue_db'], 'data/ch01 files regenerate from docs and match exactly; runtime loads only res:// data.', 'Automated data-vs-doc comparison (tools/phase02_export_data.py --check).'),
 ('REQ-ARCH-004', 'architecture', 'docs/technical/GODOT_ASSET_PIPELINE.md', 'Pinned engine', 'Project runs on pinned Godot 4.7.2.stable; project metadata not downgraded; asset_library excluded from import (.gdignore).', 'P0', [], 'A6-Release', ['project'], 'Headless run on 4.7.2 with zero script errors; asset_library has .gdignore.', 'Automated headless boot test.'),
 ('REQ-ARCH-005', 'architecture', 'docs/technical/SCENE_ARCHITECTURE.md', 'Scene changes', 'Scene/mission changes request both-ready, pause barks, commit checkpoint, load both actors together, then resume.', 'P0', ['REQ-ARCH-001', 'REQ-SAVE-002'], 'A4-Story', ['chapter', 'director'], 'Mission transition loads both players into next mission spawns in one frame transaction; checkpoint committed first.', 'Automated mission transition test.'),
 ('REQ-CHAR-001', 'characters', 'docs/technical/ANIMATION_REQUIREMENTS.md', 'Scale target', 'Adrian (P1) and Noah (P2) use realistic Rocketbox models at canonical heights (1.84 m / 1.78 m) with prison clothing.', 'P0', [], 'A1-Foundation', ['player', 'visual'], 'Player scenes instance assets/characters/phase15/rocketbox/adrian_cross.glb and noah_reyes.glb; measured standing height within 3 cm.', 'Automated bounds test + graphical inspection.'),
 ('REQ-CHAR-002', 'characters', 'docs/missions (Present lists)', 'NPC cast', 'Rusk, guards, Silas, Mara and inmates appear as realistic characters at their marks in their missions.', 'P0', ['REQ-CHAR-001'], 'A3-NPC', ['npc', 'visual'], 'Each mission spawns its Present cast with the correct model.', 'Automated cast test per mission + screenshots.'),
 ('REQ-MOVE-001', 'movement', 'GAME_DESIGN.md', 'Player movement', 'Players walk, run (jog), crouch and interact; contextual ladders/hatches; constrained camera look. No jump puzzle or stamina.', 'P0', ['REQ-CHAR-001', 'REQ-INPUT-001'], 'A1-Foundation', ['player', 'visual'], 'Walk ~1.2-1.5 m/s, jog ~3.5 m/s, crouch ~0.7 m/s; collision prevents passing walls; gravity keeps feet on floor.', 'Automated movement test (velocity, collision) + graphical inspection.'),
 ('REQ-MOVE-002', 'movement', 'docs/environments/MAINTENANCE_NETWORK.md', 'Ladder', 'Ladders/hatches/stairs are explicit traversal links usable by players (M04 hatch crawl, M05 west ladder/stairs to catwalk).', 'P1', ['REQ-MOVE-001'], 'A1-Foundation', ['player', 'env_maint'], 'Player can reach catwalk y=2.5 and return; hatch crawl traverses into chase.', 'Automated traversal test.'),
 ('REQ-ANIM-001', 'animation', 'docs/technical/ANIMATION_REQUIREMENTS.md', 'Base set', 'Locomotion animation (idle, walk, jog, crouch idle/walk) blends from velocity on Adrian and Noah.', 'P0', ['REQ-CHAR-001'], 'A1-Foundation', ['visual'], 'Clip selected matches speed state; blend 0.15-0.25 s; no T-pose.', 'Automated clip-state test + graphical inspection of walk/run.'),
 ('REQ-ANIM-002', 'animation', 'docs/technical/ANIMATION_REQUIREMENTS.md', 'Mission sets', 'Interaction/performance clips play for mission actions (interact, kneel/fix, push/pull, climb, sit, hands-up) using the 37 available clips; missing bespoke clips use nearest substitute and are logged.', 'P1', ['REQ-ANIM-001'], 'A4-Story', ['visual', 'director'], 'Each mission action triggers a named clip; substitution table documented.', 'Automated clip trigger log + graphical inspection.'),
 ('REQ-ANIM-003', 'animation', 'docs/qa/BLOCKERS.md P02', 'Paired contacts', 'Paired, contact-aligned animations (assisted climb, hatch hold handoff, dual handle, cuffing) with alignment markers.', 'P1', ['REQ-ANIM-002'], 'A4-Story', ['visual'], 'Contact markers within 3 cm in paired actions.', 'Graphical contact inspection.'),
 ('REQ-ANIM-004', 'animation', 'docs/qa/BLOCKERS.md P01', 'Facial', 'Facial performance and lip-sync for close dialogue.', 'P2', [], 'A4-Story', [], 'Visemes drive face on authored line.', 'Graphical close-up inspection.'),
 ('REQ-CAM-001', 'camera', 'docs/screenplay/CH01_FULL_SCRIPT.md', 'Camera item 10', 'Third-person gameplay camera per player at 1.6 m height, 2.8 m trailing, collision retracts to 0.45 m.', 'P0', ['REQ-CHAR-001'], 'A1-Foundation', ['pcam'], 'SpringArm length 2.8 m, margin, collision shortens to >=0.45 m against walls.', 'Automated camera-collision test + graphical inspection.'),
 ('REQ-CAM-002', 'camera', 'docs/technical/COOP_REQUIREMENTS.md', 'Cinematics return', 'After a cinematic both gameplay cameras blend back over 0.4 s.', 'P1', ['REQ-CAM-001', 'REQ-CINE-001'], 'A4-Story', ['cine', 'pcam'], 'Blend duration 0.4 s measured.', 'Automated timing test.'),
 ('REQ-SPLIT-001', 'split-screen', 'docs/technical/COOP_REQUIREMENTS.md', 'Local split', 'Local two-player vertical split-screen: two SubViewports rendering the same World3D with independent cameras.', 'P0', ['REQ-CAM-001'], 'A1-Foundation', ['split', 'chapter'], 'Two viewports, left P1 right P2, share one World3D; each renders its own camera.', 'Automated viewport/world identity test + graphical screenshot.'),
 ('REQ-INPUT-001', 'input', 'docs/technical/COOP_REQUIREMENTS.md', 'Device ownership', 'Explicit device ownership before play: two gamepads preferred, keyboard+gamepad fallback, keyboard split fallback for testing; fixed P1/P2 ownership.', 'P0', [], 'A1-Foundation', ['devices', 'menu', 'project'], 'Device assignment screen; each player reads only its device; no cross-talk.', 'Automated input routing test (synthetic events per device).'),
 ('REQ-INPUT-002', 'input', 'docs/technical/COOP_REQUIREMENTS.md', 'Disconnect', 'Controller disconnect pauses both players and offers reassignment.', 'P1', ['REQ-INPUT-001'], 'A1-Foundation', ['devices', 'pause'], 'joy_connection_changed(false) for an owned pad pauses game with reassignment prompt.', 'Automated simulated-disconnect test.'),
 ('REQ-INPUT-003', 'input', 'GAME_DESIGN.md', 'Accessibility', 'Hold actions may be toggled; camera sensitivity and invert options.', 'P2', ['REQ-INPUT-001'], 'A5-Systems', ['settings', 'pause'], 'Settings toggles change behaviour.', 'Automated settings test.'),
 ('REQ-COOP-001', 'co-op', 'docs/technical/COOP_REQUIREMENTS.md', 'Simultaneous play', 'Two players move simultaneously and independently in split-screen.', 'P0', ['REQ-SPLIT-001', 'REQ-INPUT-001', 'REQ-MOVE-001'], 'A1-Foundation', ['player', 'split', 'devices'], 'Simultaneous inputs move both bodies in the same frame; cameras independent.', 'Automated simultaneous-movement test + graphical split capture.'),
 ('REQ-COOP-002', 'co-op', 'docs/technical/COOP_REQUIREMENTS.md', 'Interaction leases', 'Interactions use playerID+objectID leases with ready/active/release/cancel and atomic commits; no player consumes another\'s interaction; allowed actor enforced.', 'P0', ['REQ-COOP-001'], 'A1-Foundation', ['interact', 'director'], 'Wrong actor cannot use role-locked interactable; hold release cancels safely; duplicate commits ignored.', 'Automated interaction lease tests.'),
 ('REQ-COOP-003', 'co-op', 'docs/technical/COOP_REQUIREMENTS.md', 'Gates', 'Every co-op gate requires the two distinct actors; one player cannot solo a gate; partner waiting has no deadline.', 'P0', ['REQ-COOP-002'], 'A4-Story', ['director'] + [mfile(i) for i in range(1, 7)], 'For each mission gate, one-player attempt does not progress.', 'Automated solo-gate negative tests per mission.'),
 ('REQ-COOP-004', 'co-op', 'docs/technical/COOP_REQUIREMENTS.md', 'Prompts', 'Interaction prompts identify actor role and partner waiting state.', 'P1', ['REQ-COOP-002'], 'A5-Systems', ['hud', 'interact'], 'Prompt shows role-locked label and "waiting for partner" state.', 'Automated HUD state test + screenshot.'),
 ('REQ-COOP-005', 'co-op', 'docs/missions', 'Boundary', 'Boundary doors block leaving without partner; recover-stuck returns to last safe mark; no invisible death volumes.', 'P1', ['REQ-COOP-001'], 'A4-Story', ['director', 'player'], 'Recover action teleports to last safe mark; fall below floor recovers.', 'Automated recover test.'),
 ('REQ-ENV-001', 'environment', 'docs/environments/PRISON_INTAKE.md', 'ENV_INTAKE', 'Intake: transport apron, reception, holding bay behind transparent solid grille, property counter with tray, guard desk, east exit to cell block.', 'P0', [], 'A2-World', ['env_intake', 'builder'], 'Layout matches marks I0-I5; grille blocks movement but is visible; badge visible from holding bay.', 'Automated layout/collision test + screenshots.'),
 ('REQ-ENV-002', 'environment', 'docs/environments/CELL_BLOCK.md', 'ENV_CELLBLOCK', 'Cell block: central circulation, cells 13/14 with sinks/doors/beds, rear service panels into common chase, concrete pier shelters, restricted corridor and maintenance hatch.', 'P0', [], 'A2-World', ['env_cell', 'builder'], 'Cells 13/14 adjacent 3 m frontage; chase connects to C5/C6; pier gives real occlusion.', 'Automated layout/occlusion test + screenshots.'),
 ('REQ-ENV-003', 'environment', 'docs/environments/PRISON_YARD.md', 'ENV_YARD', 'Yard: fenced court, bench, tap alcove, west fence lane, gates, guard patrol lanes.', 'P0', [], 'A2-World', ['env_yard', 'builder'], 'Marks Y0-Y3, ball lane clear 1.6 m.', 'Automated layout test + screenshots.'),
 ('REQ-ENV-004', 'environment', 'docs/environments/LAUNDRY_WORKSHOP.md', 'ENV_WORKSHOP', 'Workshop: press enclosure with isolation lever and screen, diagram, scrap bin, Mara linen table, guard office, aisle.', 'P0', [], 'A2-World', ['env_work', 'builder'], 'Marks W0-W5 and office; no player enters moving equipment.', 'Automated layout test + screenshots.'),
 ('REQ-ENV-005', 'environment', 'docs/environments/MAINTENANCE_NETWORK.md', 'ENV_MAINTENANCE', 'Maintenance: manual gate, split, west catwalk (y 2.5) with ladder/stairs and selector, east floor with brake, handsets, lifting grille, pump console with ledger, spillway door with two handles, loading interception.', 'P0', [], 'A2-World', ['env_maint', 'builder'], 'Routes separated by fenced pump well; each recoverable; grille latch visible.', 'Automated route/collision test + screenshots.'),
 ('REQ-ENV-006', 'environment', 'docs/environments/CELL_BLOCK.md', 'Solitary annex', 'Solitary annex: two 3x4 m cells separated by a 0.25 m wall with shared pipe; separate occluded set.', 'P0', [], 'A2-World', ['env_solitary', 'builder'], 'Neither player sees through wall; pipe interactable in each.', 'Automated layout test + screenshots.'),
 ('REQ-ENV-007', 'environment', 'docs/environments/*', 'Collision', 'Static collision for walls/bars/machines; grilles physically solid; no falling through floors.', 'P0', ['REQ-ENV-001', 'REQ-ENV-002', 'REQ-ENV-003', 'REQ-ENV-004', 'REQ-ENV-005', 'REQ-ENV-006'], 'A2-World', ['builder'], 'Ray/shape tests confirm walls block; players stay above floor during scripted routes.', 'Automated collision probes per environment.'),
 ('REQ-ENV-008', 'environment', 'docs/environments/*', 'Navigation', 'Navigation meshes per environment for NPC movement; door links state-controlled.', 'P1', ['REQ-ENV-007'], 'A2-World', ['builder', 'npc'], 'NPCs reach their marks along navmesh without passing walls.', 'Automated NPC path test.'),
 ('REQ-ENV-009', 'environment', 'docs/screenplay/CH01_FULL_SCRIPT.md', 'Lighting', 'Per-scene lighting: M01 cool overcast, M02 hazy sun, M03 warm task vs cold strip, M04 night strips and flashlight cone, M05 amber lamps, M06 steady red alarm wash (no strobe), solitary pools.', 'P1', ['REQ-ENV-001'], 'A2-World', ['builder'] + [mfile(i) for i in range(1, 7)], 'Lighting set per mission as described; alarm is steady.', 'Graphical inspection screenshots.'),
 ('REQ-NPC-001', 'npc', 'docs/screenplay/CH01_CHARACTER_BLOCKING.md', 'Marks', 'NPCs occupy fixed listen marks during plot lines, resume patrol only after subtitle completion; walk at 1.2 m/s.', 'P0', ['REQ-ENV-008', 'REQ-CHAR-002'], 'A3-NPC', ['npc', 'director'], 'NPC movement suspended while its line plays.', 'Automated NPC state test.'),
 ('REQ-NPC-002', 'npc', 'docs/missions/CH01_MISSION_01.md', 'Escort', 'Rusk escorts Noah; escort pauses if either player is behind (within 4 m rule).', 'P0', ['REQ-NPC-001'], 'A3-NPC', ['npc', mfile(1)], 'Escort NPC waits when a player is >4 m behind.', 'Automated escort test.'),
 ('REQ-GUARD-001', 'guard-ai', 'docs/missions/CH01_MISSION_04.md', 'Patrol', 'Bounded deterministic guard patrol (C1->C2->north gallery->C5 sightline->C1, ~45 s loop with ~12 s safe window) with flashlight cone.', 'P0', ['REQ-NPC-001'], 'A3-NPC', ['guard', mfile(4)], 'Patrol is deterministic and phase is serialisable.', 'Automated patrol determinism test.'),
 ('REQ-GUARD-002', 'guard-ai', 'docs/missions/CH01_MISSION_04.md', 'Detection', 'Visible line-of-sight detection with ~1.5 s warning indicator; pier occlusion blocks sight; full detection plays DLG020 and reloads CP04_A.', 'P0', ['REQ-GUARD-001', 'REQ-ENV-002'], 'A3-NPC', ['guard', 'hud', mfile(4)], 'Player in cone with clear LOS accumulates detection; behind pier does not; full detection reloads CP04_A.', 'Automated detection/occlusion tests + graphical inspection.'),
 ('REQ-GUARD-003', 'guard-ai', 'docs/missions/CH01_MISSION_02.md', 'Attention', 'Guard attention responds to authored distractions (M02 ball rattle, M03 Rusk drawn by Mara/lamp request, M04 pipe sound investigation DLG013 not fail).', 'P1', ['REQ-NPC-001'], 'A3-NPC', ['guard', mfile(2), mfile(3), mfile(4)], 'Guard turns/moves to attention point on event.', 'Automated attention test.'),
 ('REQ-DLG-001', 'dialogue', 'docs/screenplay/CH01_DIALOGUE.md', 'Ledger', 'All 145 Chapter 1 lines are integrated with exact text, speaker, line ID and conditions; main lines play in screenplay order at their staging; optional lines only under named condition.', 'P0', ['REQ-ARCH-003'], 'A4-Story', ['dlg_data', 'dialogue_db', 'dlg_dir'] + [mfile(i) for i in range(1, 7)], 'Every main line is displayed during a full playthrough in order; every conditional line fires under its condition in tests.', 'Automated full dialogue coverage log vs ledger.'),
 ('REQ-DLG-002', 'dialogue', 'docs/screenplay/CH01_DIALOGUE.md', 'Subtitles', 'Subtitles show speaker and exact text, max two lines ~42 chars per line reflowed at word boundaries, held for line duration, never truncated; RECORDING prefix for recorded voice; readable at half 1080p width.', 'P0', ['REQ-DLG-001'], 'A5-Systems', ['subs', 'dlg_dir'], 'Wrap function never exceeds 2x42 without overflow handling; full text shown.', 'Automated wrap test + screenshot at 960 px width.'),
 ('REQ-DLG-003', 'dialogue', 'docs/screenplay/CH01_FULL_SCRIPT.md', 'Queue', 'Plot lines serialize; no overlapping intelligible speech; optional barks queue behind plot lines and never cover clues; progression waits for required dialogue.', 'P0', ['REQ-DLG-001'], 'A4-Story', ['dlg_dir'], 'Queue never shows two lines at once; bark deferred while plot line active.', 'Automated queue test.'),
 ('REQ-DLG-004', 'dialogue', 'docs/qa/BLOCKERS.md P06', 'Voice-over', 'Recorded voice-over for all lines.', 'P2', ['REQ-DLG-001'], 'A5-Systems', [], 'Each line has VO audio.', 'Listening test.'),
 ('REQ-CINE-001', 'cinematics', 'docs/technical/COOP_REQUIREMENTS.md', 'Cinematics', 'Both-ready precondition; full-screen shared letterboxed presentation; both control contexts suspended; shot cameras named CH01_Mnn_CS01_SHnn activated in order; pause stops the cinematic clock.', 'P0', ['REQ-SPLIT-001', 'REQ-DLG-001'], 'A4-Story', ['cine', 'shot_data'], 'All 36 shot cameras are activated during a playthrough with logged timing.', 'Automated shot activation log + graphical capture per shot.'),
 ('REQ-CINE-002', 'cinematics', 'docs/screenplay/CH01_CUTSCENES.md', 'Skip', 'Skip accepted only when both confirm; commits identical canonical state and shows a short written clue recap.', 'P1', ['REQ-CINE-001'], 'A4-Story', ['cine'], 'Single-player skip request does nothing; mutual skip ends cinematic with same flags as full play.', 'Automated skip test.'),
 ('REQ-OBJ-001', 'objectives', 'docs/missions', 'Objective display', 'Current objective text shown to both players with its ID order; objectives advance only through MissionDirector.', 'P0', ['REQ-ARCH-002'], 'A5-Systems', ['hud', 'director'], 'HUD shows current objective per mission in order.', 'Automated objective sequence test.'),
 ('REQ-SAVE-001', 'save-load', 'docs/technical/COOP_REQUIREMENTS.md', 'Snapshot', 'Checkpoint snapshot: mission ID, checkpoint ID, schema version, both transforms, inventory owner, prop/door/puzzle states, patrol phase, objective flags, knowledge, consumed dialogue, committed transaction IDs.', 'P0', ['REQ-ARCH-002'], 'A5-Systems', ['state', 'save'], 'Snapshot JSON contains all fields; restore reproduces them.', 'Automated save/restore round-trip test.'),
 ('REQ-SAVE-002', 'save-load', 'docs/technical/COOP_REQUIREMENTS.md', 'Stable saves', 'Save only stable states (never in cinematic, door motion or item transfer); retry restores both atomically; repeated inputs cannot duplicate pickups.', 'P0', ['REQ-SAVE-001'], 'A5-Systems', ['state', 'save', 'director'], 'Save request during cinematic is rejected; reload restores both players.', 'Automated negative save test.'),
 ('REQ-SAVE-003', 'save-load', PHASE02, 'Save/load', 'Persistent save file in user:// with Continue from main menu restoring mission and checkpoint after application restart.', 'P0', ['REQ-SAVE-001'], 'A5-Systems', ['save', 'menu'], 'Quit and relaunch, Continue resumes at last checkpoint with identical state.', 'Automated two-process save/load test.'),
 ('REQ-SAVE-004', 'save-load', 'docs/technical/COOP_REQUIREMENTS.md', 'Continuity', 'Inventory/knowledge continuity: photo approved paper with Noah; property locker42; diagram returned; ledger stays at console; shim acquired M03, used M04-M05, confiscated M06.', 'P0', ['REQ-SAVE-001'], 'A4-Story', ['state'] + [mfile(i) for i in range(1, 7)], 'Inventory state at each mission exit matches canon.', 'Automated continuity assertions in playthrough.'),
 ('REQ-UI-001', 'ui', PHASE02, 'Main menu', 'Main menu: New Game, Continue (enabled only with save), Controls/Device assignment, Settings, Quit.', 'P0', ['REQ-INPUT-001'], 'A5-Systems', ['menu', 'main_scene'], 'Each button performs its action; no dummy buttons.', 'Automated menu action test + screenshot.'),
 ('REQ-UI-002', 'ui', 'docs/technical/COOP_REQUIREMENTS.md', 'Pause', 'Pause menu (either player) with Resume, Restart checkpoint, Settings, Quit to menu; pausing stops cinematic clock.', 'P0', ['REQ-UI-001'], 'A5-Systems', ['pause'], 'Each pause action works.', 'Automated pause test.'),
 ('REQ-UI-003', 'ui', 'GAME_DESIGN.md', 'HUD', 'Per-player HUD in each half: objective, interaction prompt with role, partner waiting, hold progress, detection warning, checkpoint saved notice.', 'P0', ['REQ-SPLIT-001'], 'A5-Systems', ['hud'], 'HUD elements appear in the correct half.', 'Automated HUD test + screenshot.'),
 ('REQ-UI-004', 'ui', 'GAME_DESIGN.md', 'Settings', 'Settings: subtitle size, music/voice/sfx volumes, camera sensitivity/invert, hold-toggle, reduced flash.', 'P1', ['REQ-UI-002'], 'A5-Systems', ['settings', 'pause'], 'Settings persist to user://settings.cfg and apply.', 'Automated settings round-trip test.'),
 ('REQ-UI-005', 'ui', 'docs/missions/CH01_MISSION_06.md', 'End card', 'End card "CH02 NIGHT SHIFT" only after both pipe interactions; chapter-end save.', 'P0', ['REQ-SAVE-002'], 'A4-Story', [mfile(6), 'hud'], 'End card shown after both knocks; not before.', 'Automated end test + screenshot.'),
 ('REQ-AUDIO-001', 'audio', 'docs/screenplay/CH01_FULL_SCRIPT.md', 'Sound item 12', 'Per-scene ambience and cues from acquired assets: bus/ocean (M01), fence rattle/gulls/ball (M02), washer/belt/steam (M03), count bell/boots/radio (M04), pump pulse/handset/recording (M05), door/alarm/pipe knocks (M06); footsteps.', 'P1', [], 'A5-Systems', ['audio'] + [mfile(i) for i in range(1, 7)], 'Each mission starts its ambience and fires listed cues; audio buses for music/voice/sfx.', 'Automated audio playback log; listening test.'),
 ('REQ-AUDIO-002', 'audio', 'docs/qa/BLOCKERS.md P06', 'Listening', 'Audio mix listening pass.', 'P2', ['REQ-AUDIO-001'], 'QA-Independent', [], 'Human listening sign-off.', 'Listening test.'),
 ('REQ-PERF-001', 'performance', 'docs/technical/SCENE_ARCHITECTURE.md', 'Targets', 'Two-view 1080p 60 fps target on the development PC (RTX 2060) measured per mission.', 'P1', ['REQ-SPLIT-001'], 'A6-Release', ['playthrough'], 'Average fps >= 60 and 1% low reported per mission in split-screen.', 'Automated fps capture during graphical playthrough.'),
 ('REQ-EXPORT-001', 'windows-export', PHASE02, 'Section 13', 'Windows export preset and executable exist.', 'P0', ['REQ-ARCH-004'], 'A6-Release', ['export'], 'build/windows/BreakoutNoWayBack.exe produced by headless export.', 'Automated export command.'),
 ('REQ-EXPORT-002', 'windows-export', PHASE02, 'Section 13', 'Exported executable launches, loads resources, controls/split-screen/mission progression/save-load/audio work with no critical runtime errors.', 'P0', ['REQ-EXPORT-001', 'REQ-TEST-002'], 'A6-Release', ['export', 'playthrough'], 'Exported exe runs the autopilot playthrough to the end card with zero script errors.', 'Run exported exe with --autopilot; log check.'),
 ('REQ-TEST-001', 'testing', PHASE02, 'Sections 8, 11', 'Automated test suite (headless) for systems and per-mission sequences.', 'P0', [], 'QA-Independent', ['tests'], 'run_tests.gd exits 0 with all tests passing.', 'Headless run.'),
 ('REQ-TEST-002', 'testing', PHASE02, 'Section 12', 'Full Chapter 1 graphical playthrough from a fresh save through all six missions with both players, recorded duration and screenshots; repeated after final critical fix.', 'P0', [f'REQ-MIS-0{i}' for i in range(1, 7)], 'QA-Independent', ['playthrough'], 'Playthrough reaches end card; evidence report with duration and per-step screenshots.', 'Graphical autopilot playthrough + screenshot review.'),
 ('REQ-TEST-003', 'testing', PHASE02, 'Section 12', 'Human manual playthrough with two real controllers.', 'P1', ['REQ-TEST-002'], 'QA-Independent', [], 'A person completes Chapter 1 with two controllers.', 'Manual test.'),
 ('REQ-DOC-001', 'documentation', PHASE02, 'Section 14', 'Session state, requirements matrix, scene completeness matrix and completion audit reflect actual implementation.', 'P0', [], 'A6-Release', ['docs/PHASE_02_SESSION_STATE.md'], 'Docs regenerated after each milestone; audit passes coverage checks.', 'tools/phase02_completion_audit.py.'),
]

reqs = []
def add(rid, cat, src, sec, desc, pri, deps, agent, files, acc, test, mandatory=True, extra=None):
    files = [F.get(f, f) for f in files]
    reqs.append(dict(id=rid, category=cat, source_document=src, source_section=sec, description=desc, priority=pri, mandatory=mandatory,
                     dependencies=deps, responsible_agent=agent, implementation_files=files, acceptance_criteria=acc, test_method=test,
                     evidence_location=EV + rid + '.json', status='NOT_STARTED', blocking_issues=[], **(extra or {})))
for s in SYS:
    add(*s, mandatory=s[5] in ('P0', 'P1'))
for m in MISSIONS:
    i = m['n']
    add(f'REQ-MIS-0{i}', 'mission', m['doc'], 'whole mission', f"{m['id']} {m['name']} is playable end to end: {m['sequence']}", 'P0',
        ['REQ-COOP-003', 'REQ-DLG-001', 'REQ-CINE-001', 'REQ-SAVE-002'] + ([f'REQ-MIS-0{i-1}'] if i > 1 else []), 'A4-Story',
        [mfile(i), 'director'] + env_for(i),
        'Starts at CP0%d_A with correct spawns; objectives in order; NPC behaviour, interactions, co-op gates, dialogue, cutscene; completion, failure/retry, save/load restore, transition to next mission.' % i,
        'Automated mission test + graphical playthrough segment.', extra=dict(mission_id=m['id'], scene_id=m['scene'], cinematic_id=m['cine']))
    add(f'REQ-MIS-0{i}-GATE', 'co-op', m['doc'], 'Cooperative gates', m['gates'], 'P0', [f'REQ-MIS-0{i}'], 'A4-Story', [mfile(i), 'interact'],
        'Gate cannot be passed by one player; behaves as specified.', 'Automated solo-gate negative test + positive co-op test.')
    add(f'REQ-MIS-0{i}-FAIL', 'checkpoints', m['doc'], 'Checkpoints, failure and retry', m['failure'], 'P0', [f'REQ-MIS-0{i}', 'REQ-SAVE-002'], 'A4-Story', [mfile(i), 'state'],
        'Failure/retry behaves as specified; no death volumes; consumed lines stay consumed.', 'Automated failure/retry test.')
    add(f'REQ-MIS-0{i}-EXIT', 'story', m['doc'], 'Exit state and next mission', m['exit'], 'P0', [f'REQ-MIS-0{i}', 'REQ-SAVE-004'], 'A4-Story', [mfile(i), 'state'],
        'Exit-state flags/inventory equal canon; only shared scene-complete transaction advances.', 'Automated exit-state assertions.')
    add(f'REQ-SCENE-0{i}', 'scene', 'docs/screenplay/CH01_FULL_SCRIPT.md', m['scene'], f"Screenplay scene {m['scene']} implemented (location, cast, starting positions, assets, animations, dialogue staging, shots, audio, interactions, triggers, transitions, checkpoints, completion). Staging: {STAGING.get(m['scene'], '')}", 'P0',
        [f'REQ-MIS-0{i}'], 'A4-Story', [mfile(i)] + env_for(i), 'All 15 scene-completeness fields confirmed in docs/qa/SCENE_COMPLETENESS_MATRIX.md.', 'Scene completeness review + graphical inspection.',
        extra=dict(scene_id=m['scene']))
for o in OBJECTIVES:
    add(f'REQ-{o["id"]}', 'objective', o['doc'], 'Objective and cinematic triggers', f'{o["id"]}: {o["text"]}', 'P0', [f'REQ-MIS-0{o["mission"]}'], 'A4-Story',
        [mfile(o['mission']), 'director', 'mission_data'], 'Objective activates and completes in order only when its condition is met by the correct actor(s).', 'Automated mission sequence test.', extra=dict(objective_id=o['id']))
for c in CHECKPOINTS:
    add(f'REQ-{c["id"]}', 'checkpoints', c['doc'], 'Checkpoints', f'{c["id"]} ({c["text"]}) restores both players, props, patrol phase and dialogue consumed flags atomically.', 'P0',
        ['REQ-SAVE-001', f'REQ-MIS-0{c["mission"]}'], 'A5-Systems', [mfile(c['mission']), 'state', 'save'], 'Reload at this checkpoint restores identical snapshot.', 'Automated checkpoint round-trip test.', extra=dict(checkpoint_id=c['id']))
for d in DIALOGUE:
    sl = script_lines.get(d['id'])
    add(f'REQ-{d["id"]}', 'dialogue-line', 'docs/screenplay/CH01_DIALOGUE.md', d['id'], f'{d["speaker"]}: "{d["text"]}" ({d["condition"]})', 'P0', ['REQ-DLG-001', f'REQ-MIS-0{d["mission"]}'], 'A4-Story',
        ['dlg_data', mfile(d['mission'])], 'Line displayed with exact text and speaker at its staging or condition.', 'Dialogue coverage log in automated playthrough/condition tests.',
        extra=dict(dialogue_id=d['id'], speaker=d['speaker'], text=d['text'], condition=d['condition'], script_match=bool(sl and sl == (d['speaker'], d['text']))))
for s in SHOTS:
    add(f'REQ-{s["id"]}', 'camera-shot', 'docs/screenplay/CH01_CAMERA_SHOTS.md', s['id'], f'{s["camera"]}: {s["direction"]}', 'P0', ['REQ-CINE-001', f'REQ-MIS-0{s["mission"]}'], 'A4-Story',
        ['shot_data', 'cine', mfile(s['mission'])], 'Named shot camera activated in order during CS01 with documented framing (or recorded approved alternative).', 'Shot activation log + graphical capture.',
        extra=dict(shot_id=s['id'], reel=s['reel']))

# known blockers from Phase 01.5 (not silently dropped)
KNOWN = {'REQ-ANIM-003': ['P02: paired contact-aligned animation clips not available (docs/qa/BLOCKERS.md)'],
         'REQ-ANIM-004': ['P01: facial blendshapes/lip-sync not converted; no VO'],
         'REQ-DLG-004': ['P06: no recorded voice-over exists; requires casting/recording'],
         'REQ-AUDIO-002': ['P06: human listening session required'],
         'REQ-TEST-003': ['Requires a human with two controllers']}

old = {r['id']: r for r in json.loads(OUT_JSON.read_text(encoding='utf-8'))['requirements']} if OUT_JSON.exists() else {}
for r in reqs:
    o = old.get(r['id'])
    if o:
        for k in ('status', 'blocking_issues', 'evidence', 'qa', 'notes', 'implementation_files_actual', 'pending_checks'):
            if k in o: r[k] = o[k]
    elif r['id'] in KNOWN:
        r['status'] = 'BLOCKED'; r['blocking_issues'] = KNOWN[r['id']]
    assert r['status'] in STATUSES, r
dropped = sorted(set(old) - {r['id'] for r in reqs})
if dropped:
    sys.exit('Refusing to drop requirements present in the existing registry: ' + ', '.join(dropped))

counts = dict(missions=len(MISSIONS), scenes=len(MISSIONS), objectives=len(OBJECTIVES), checkpoints=len(CHECKPOINTS), dialogue_lines=len(DIALOGUE), camera_shots=len(SHOTS),
              dialogue_script_mismatches=[d['id'] for d in DIALOGUE if script_lines.get(d['id']) != (d['speaker'], d['text'])],
              dialogue_in_script_not_ledger=sorted(set(script_lines) - {d['id'] for d in DIALOGUE}))
reg = dict(generated_by='tools/phase02_build_registry.py', statuses=STATUSES, canonical_counts=counts, phase01_expected=dict(dialogue_lines=145, camera_shots=36, missions=6),
           requirements=reqs)
OUT_JSON.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')

# ---------------------------------------------------------------- markdown matrix
from collections import Counter
st = Counter(r['status'] for r in reqs)
md = ['# Phase 02 requirements matrix', '',
      f'Generated by `tools/phase02_build_registry.py` from the canonical documents; machine-readable copy: [PHASE_02_REQUIREMENTS.json](PHASE_02_REQUIREMENTS.json). Status values: {", ".join(STATUSES)}. Only the independent QA reviewer sets VERIFIED.', '',
      '## Canonical counts', '', '| Item | Found in source | Phase 01 expectation |', '|---|---|---|',
      f'| Missions / scenes | {len(MISSIONS)} / {len(MISSIONS)} | 6 |', f'| Objectives | {len(OBJECTIVES)} | — |', f'| Checkpoints | {len(CHECKPOINTS)} | — |',
      f'| Dialogue lines | {len(DIALOGUE)} | 145 |', f'| Camera shots | {len(SHOTS)} | 36 |',
      f'| Ledger lines that differ from FULL_SCRIPT | {len(counts["dialogue_script_mismatches"])} | 0 |', '',
      '## Status summary', '', '| Status | Count |', '|---|---|'] + [f'| {s} | {st.get(s, 0)} |' for s in STATUSES] + [f'| **Total** | **{len(reqs)}** |', '']
cats = {}
for r in reqs: cats.setdefault(r['category'], []).append(r)
for cat, rs in cats.items():
    md += [f'## {cat} ({len(rs)})', '']
    if cat in ('dialogue-line', 'camera-shot'):
        md += ['| ID | Requirement | Implementation | Status | Blocking |', '|---|---|---|---|---|']
        for r in rs:
            md.append(f'| {r["id"]} | {r["description"].replace("|", "/")} | {", ".join(f"`{f}`" for f in r["implementation_files"])} | {r["status"]} | {"; ".join(r["blocking_issues"]) or "—"} |')
    else:
        md += ['| ID | Pri | Source | Requirement | Deps | Agent | Implementation | Acceptance | Test | Status | Blocking |', '|---|---|---|---|---|---|---|---|---|---|---|']
        for r in rs:
            md.append(f'| {r["id"]} | {r["priority"]} | {r["source_document"]} § {r["source_section"]} | {r["description"].replace("|", "/")} | {", ".join(r["dependencies"]) or "—"} | {r["responsible_agent"]} | '
                      f'{"<br>".join(f"`{f}`" for f in r["implementation_files"]) or "—"} | {r["acceptance_criteria"]} | {r["test_method"]} | {r["status"]} | {"; ".join(r["blocking_issues"]) or "—"} |')
    md.append('')
OUT_MD.write_text('\n'.join(md) + '\n', encoding='utf-8')
print(json.dumps(dict(total=len(reqs), **{k: v for k, v in counts.items() if not isinstance(v, list)}, mismatches=counts['dialogue_script_mismatches'], extra_script=counts['dialogue_in_script_not_ledger'], status=dict(st)), indent=1))
