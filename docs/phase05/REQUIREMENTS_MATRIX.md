# Phase 05 requirements matrix

Statuses: NOT_STARTED · IN_PROGRESS · IMPLEMENTED_UNTESTED · FAILED · BLOCKED · VERIFIED. Nothing is VERIFIED without
evidence. Phase 04 rows stay in `docs/phase04/requirements.json` / `qa_verdicts.json`. The 116 non-verified Phase 04 rows
(`_open_rows.txt`) are inherited **as open**, and the Phase 05 rows below that cover them name them in "Carries".

| ID | Milestone | Requirement | Carries | Status |
|---|---|---|---|---|
| P05-BASE-001 | Audit | Verify HEAD, registry, defects, QA verdict; write baseline docs | — | VERIFIED (`BASELINE_REPORT.md`) |
| P05-CHAR-001 | M01 Characters | Real hair geometry (strands/cards), not cap shells, on both leads | CHAR-004 | NOT_STARTED |
| P05-CHAR-002 | M01 | Adrian: short dark hair, grey temple, healed left brow cut | CHAR-007/009 | NOT_STARTED |
| P05-CHAR-003 | M01 | Adrian: grey shirt + orange prison overshirt (no sweater) | CHAR-008 | NOT_STARTED |
| P05-CHAR-004 | M01 | Noah: prison uniform garment geometry replacing the denim jacket | D04-004 | NOT_STARTED |
| P05-CHAR-005 | M01 | Noah: separate blue undershirt layer | CHAR-008 | NOT_STARTED |
| P05-CHAR-006 | M01 | Noah's wrist burn visible in the intended cinematic shots | CHAR-010 | NOT_STARTED |
| P05-CHAR-007 | M01 | Skin, eye and cloth material response (roughness, SSS where supported) | — | NOT_STARTED |
| P05-CHAR-008 | M01 | Continuity: same look across all 6 missions and cinematics | — | NOT_STARTED |
| P05-ANIM-001 | M02 Movement | Acceleration/deceleration, walk/run/sprint, turn, strafe, crouch, jump/land, stairs, stops | ANIM-002..008 | NOT_STARTED |
| P05-ANIM-002 | M02 | Foot sliding/root motion investigated and measured | ANIM-020/021 | NOT_STARTED |
| P05-ANIM-003 | M02 | Foot IK / ground alignment, head look-at, idle variation (where feasible) | — | NOT_STARTED |
| P05-ANIM-004 | M02 | Motion evidence (frame sequences or video) for every locomotion state | QA-004 | NOT_STARTED |
| P05-INT-001 | M03 Interactions | Hands reach the real handle/lever/lock; character faces the object | ANIM-016/025 | NOT_STARTED |
| P05-INT-002 | M03 | A real pull animation (not a reversed push) | ANIM-014 | NOT_STARTED |
| P05-INT-003 | M03 | Object responds at the right animation moment | — | NOT_STARTED |
| P05-ENV-001 | M04 Environments | Cell block, cell interior | — | IN_PROGRESS (Codex: tier doors, bunk; unreviewed in game) |
| P05-ENV-002 | M04 | Yard ground and wall colour | ENV-YARD-001/002 | NOT_STARTED |
| P05-ENV-003 | M04 | Intake benches and property tray | ENV-INTAKE-008 | NOT_STARTED |
| P05-ENV-004 | M04 | Laundry workshop | — | IN_PROGRESS (Codex: dryers, ironing station) |
| P05-ENV-005 | M04 | Maintenance tunnels and security areas | — | NOT_STARTED |
| P05-BUS-001 | M05 Bus/court | Bus exterior panels, wheel wells, paint/rubber/metal response | BUS-001/010 | NOT_STARTED |
| P05-BUS-002 | M05 | Bus driver area legible | BUS-008 | NOT_STARTED |
| P05-COURT-001 | M05 | Court surroundings, basketball | COURT-010 | IN_PROGRESS (Codex: ball) |
| P05-CIN-001 | M06 Cinematics | M06 SH04: Noah reaches the kneel on "On your knees", frame-by-frame | CIN-005 | NOT_STARTED |
| P05-CIN-002 | M06 | M04 SH03 shim insert readable | SHOT M04 SH03 | NOT_STARTED |
| P05-CIN-003 | M06 | M05 SH02 handset readable | SHOT M05 SH02 | NOT_STARTED |
| P05-CIN-004 | M06 | M02 mediation: Silas in frame | ANIM-025 | NOT_STARTED |
| P05-CIN-005 | M06 | M05 gate: hand at the lock, facing the gate | ANIM-016 | NOT_STARTED |
| P05-CIN-006 | M06 | Burn reveal and bus introduction reviewed | — | NOT_STARTED |
| P05-CIN-007 | M06 | Solo-configuration cutscene run | CIN-011 | NOT_STARTED |
| P05-AI-001 | M07 Guards | Idle variation, natural turning, alert communication; existing 6/6 tests preserved | AI-013 | NOT_STARTED |
| P05-AUD-001 | M08 Audio | Surface footsteps, ambience, radio, machinery, doors, alarms, reverb, balance | AUD-001..009 | NOT_STARTED |
| P05-AUD-002 | M08 | Human listening test (headphones + speakers) | AUD-* | HUMAN_TEST_PENDING |
| P05-COOP-001 | M09 Co-op | Independent input/cameras, assignment, prompts, pause, cutscenes (automated) | — | NOT_STARTED |
| P05-COOP-002 | M09 | Keyboard+controller and two-controller human playthrough | COOP-004/005 | HUMAN_TEST_PENDING |
| P05-COOP-003 | M09 | Camera rotation by look input test | PLAY-009 | NOT_STARTED |
| P05-PERF-001 | M10 Performance | Measured cause of each >50 ms frame (load, shader, upload, nav, anim, audio, GC) | PERF-001/008 | NOT_STARTED |
| P05-PERF-002 | M10 | Fix implemented; before/after on the exe; no scenes excluded | D04-017 | NOT_STARTED |
| P05-PERF-003 | M10 | GPU frame time recorded | PERF-004 | NOT_STARTED |
| P05-REG-001 | M11 Regression | All 6 missions: spawn, objectives, interactions, NPCs, co-op, dialogue, cinematics, fail/retry, checkpoints, save/load, completion | — | NOT_STARTED |
| P05-REG-002 | M11 | CH01_M04_DLG022 fires; conditional lines captured on screen | PT-006, DLG rows | NOT_STARTED |
| P05-REG-003 | M11 | M01 wrong-interaction bark; M06 reload during cinematic | MIS-01-009, MIS-06-009 | NOT_STARTED |
| P05-ASSET-001 | M12 Assets | Every acquired asset: source, licence, path, checksum, import, integration, screenshot | — | IN_PROGRESS (Codex manifests; unverified) |
| P05-VIS-001 | M13 Visual | `VISUAL_QUALITY_REPORT.md` from matched-camera in-game captures | PROC-002/003 | NOT_STARTED |
| P05-HUM-001 | M14 Human | Structured human testing checklist | — | NOT_STARTED |
| P05-UI-001 | M15 Release | Untested UI controls pressed; Credits final text | UI-004/006/011 | NOT_STARTED |
| P05-REL-001 | M15 | Clean export: no test scenes or dev-only resources | D05-027 | NOT_STARTED |
| P05-REL-002 | M15 | Exported exe: menu, New Game, both players, split, M01–M06, save/load, audio events, cinematics, fail/retry | — | NOT_STARTED |
| P05-QA-001 | QA | Independent reviewer verdict on Phase 05 evidence | QA-012 | NOT_STARTED |
| P05-QA-002 | QA | `tools/phase05_completion_audit.py` | — | NOT_STARTED |
