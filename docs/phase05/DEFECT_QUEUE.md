# Phase 05 defect queue

Loop: INSPECT → IMPLEMENT → TEST → CAPTURE → REVIEW → FIX → RETEST, at most 5 repair cycles before escalating as BLOCKED.
S1 = critical, S2 = high (both block approval), S3 = medium, S4 = low. Every row starts from the Phase 04 second QA review.

| ID | Sev | Area | Defect | From | Attempts | Status |
|---|---|---|---|---|---|---|
| D05-001 | S2 | Noah | Recoloured denim trucker jacket instead of a prison uniform with a separate undershirt | D04-004, CHAR-008 | 0 | OPEN |
| D05-002 | S2 | Noah | Wrist burn hidden by the cuff in all shots | CHAR-010 | 0 | OPEN |
| D05-003 | S2 | Hair | Cap-like hair shells on both leads; Adrian's is long (doc: short); hair-card shard | D04-010, CHAR-004/007 | 0 | OPEN |
| D05-004 | S2 | Adrian | Ribbed sweater instead of a grey shirt + orange overshirt; temple blotches | CHAR-008/009 | 0 | OPEN |
| D05-005 | S2 | M06 SH04 | Noah still stands on "On your knees. Both of you" | D04-013, CIN-005 | 0 | OPEN |
| D05-006 | S2 | M04 SH03 | Shim insert too dark and unreadable | SHOT, LIGHT-015 | 0 | OPEN |
| D05-007 | S2 | M05 SH02 | Handset reads as a hand to the head | SHOT, CIN-006 | 0 | OPEN |
| D05-008 | S2 | M05 gate | Hand at the lock not visible; Adrian faces away | D04-012, ANIM-016 | 0 | OPEN |
| D05-009 | S3 | M02 | Silas outside both viewports during mediation | ANIM-025 | 0 | OPEN |
| D05-010 | S2 | Dialogue | CH01_M04_DLG022 never fires (narrow trigger, `mission_04.gd` ~l.262) | PT-006, MIS-04-007 | 0 | OPEN |
| D05-011 | S3 | Dialogue | 12 conditional lines seen only in headless runs | DLG rows | 0 | OPEN |
| D05-012 | S2 | Failure path | M01 wrong-interaction bark untested | MIS-01-009 | 0 | OPEN |
| D05-013 | S2 | Failure path | M06 reload during cinematic → CP06 restart untested | MIS-06-009 | 0 | OPEN |
| D05-014 | S2 | Performance | 100–841 ms single-frame stalls (M06 841 ms) with no measured cause | D04-017, PERF-001/008 | 0 | OPEN |
| D05-015 | S3 | Performance | No GPU frame time recorded; M01 draw-call outlier unexplained | PERF-004/008 | 0 | OPEN |
| D05-016 | S2 | Animation | Pull is a reversed Push; Codex retarget trials rejected (crossed arms) | ANIM-014 | 0 | OPEN |
| D05-017 | S3 | Animation | No motion (video/frame-sequence) review exists for locomotion or interactions | ANIM-002..024 | 0 | OPEN |
| D05-018 | S2 | Bus | Flat white exterior panels, no wheel wells, no material wear | BUS-001/010 | 0 | OPEN |
| D05-019 | S3 | Bus | Driver area behind the cage illegible | BUS-008 | 0 | OPEN |
| D05-020 | S3 | Intake | Slab benches and box property tray | ENV-INTAKE-008 | 0 | OPEN |
| D05-021 | S3 | Yard | Bare uniform dirt; the wall reads tan | ENV-YARD-001/002, COURT-010 | 0 | OPEN |
| D05-022 | S3 | UI | Quit, Change device ×2, Auto-detect, graphics dropdown and toggles never pressed | UI-004/006/011 | 0 | OPEN |
| D05-023 | S3 | UI | Credits screen shows draft text | UI-011 | 0 | OPEN |
| D05-024 | S3 | Camera | No test for camera rotation by look input | PLAY-009 | 0 | OPEN |
| D05-025 | S3 | Cinematics | No solo-configuration cutscene run | CIN-011 | 0 | OPEN |
| D05-026 | S4 | Evidence | Stale overshirt/salt-and-pepper wording; blank BEFORE panels; mixed ui_walkthrough frames | QA-003/014, PROC-002/003 | 0 | OPEN |
| D05-027 | S4 | Build | tests/phase02 autopilot, `_probe_acq`, `_diag`, tests/asset_inspection still ship | QA second review | 0 | OPEN |
| D05-028 | S2 | Human | No two-controller playthrough and no audio listening | COOP-004/005, AUD-*, CIN-008 | — | HUMAN_TEST_PENDING |
| D05-029 | S3 | Integration | The Codex session's uncommitted asset swaps (bunk, tier doors, dryers, basketball) are unreviewed in gameplay and unregistered | git status | 0 | OPEN |
