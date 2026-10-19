# Phase 04 defect queue

Carried forward: every open Phase 03 defect (`docs/phase03/DEFECT_QUEUE.md`) remains tracked; rows below record Phase 04
work. Loop: IMPLEMENT → RUN → INSPECT → TEST → REVIEW → FIX → RETEST, ≤5 repair cycles before escalation.

| ID | Sev | Area | Defect | Root cause | Fix | Attempts | Retest evidence | Status |
|---|---|---|---|---|---|---|---|---|
| D04-001 | S2 | Guard AI | No hearing, no autonomous suspicion/search/alert loop (patrol + authored attention only). | Not implemented in Phase 02/03. | `GuardAI` alert state machine: PATROL→SUSPICIOUS→SEARCH→PATROL, ALERT chase on detection; noise radius by speed, halved through walls; crouch/walk silent. | 1 | `tests/phase04/evidence/guard_ai_tests.json` 5/5; `system_suite.log` 24/24; `m04_headless.json` until_reached | FIXED — pending review |
| D04-002 | S2 | Co-op | Only vertical split-screen (Phase 04 §7 asks for horizontal). | Conflict with canonical docs (CONFLICTS.md C1). | `Settings.split_mode` + Settings checkbox; vertical stays default. | 1 | `ui_walkthrough/06_horizontal_layout_in_game.png` | FIXED — pending review |
| D04-003 | S2 | Adrian | No grey temple / healed brow cut; sweater instead of grey shirt + orange overshirt (D03-032). | Stand-in avatar textures. | `tools/phase04_character_textures.py`: grey salt-and-pepper temple, pale healed cut through left brow, grey crew-neck shirt in the V-neck. Hair length unchanged (geometry). | 4 (temple invisible at first: cards barely visible → diagnosed with P04_DEBUG_RED, scalp-only strong grey) | `visual_evidence/character/adrian_temple_brow_zoom.jpg`, `iter01/adrian_*` | FIXED (texture) — hair length OPEN |
| D04-004 | S2 | Noah | Fashion denim jacket and white sneakers vs "blue prison undershirt … repaired boots"; no wrist burn. | Stand-in textures. | Flattened chambray work shirt, dark leather boots, small burn on the right wrist. | 2 | `iter01/noah_close.png`, `noah_full.png` | FIXED — pending review |
| D04-005 | S2 | Bus | Doors static. | Coach shell had no door geometry on the kerb side. | Folding two-leaf front entry door (separate `Door_L/R` nodes) opening after the SH01 stop (`EnvIntake.open_doors`). | 1 | `iter01/bus_doors_open.png` | FIXED — pending review |
| D04-006 | S2 | Court | Plain slab backboards, primitive post/arm (QA). | Code-built primitives. | Blender `hoop_gooseneck.glb`: footing + bolted plate, square post, gooseneck, perforated steel board, spring double rim, chain net. | 1 | `iter01/hoop_detail.png`, `cmp_court01.jpg` | FIXED — pending review |
| D04-007 | S3 | Yard wall | Reads tan (QA). | Warm sun on concrete; earlier texture tan. | Grey board-formed `concrete_wall_008`. Residual warmth is lighting. | 2 | `cmp_yard01.jpg` | PARTIAL |
| D04-008 | S3 | Tooling | `--check-only` reported 53 false compile failures. | No autoloads in `--script` mode. | In-project compile check `tests/phase04/parse_check.tscn` → 60/60 compile. | 1 | `parse_check.json` | FIXED |
| D04-009 | S2 | Acceptance | Human two-controller playthrough, audio listening review. | Needs people. | — | 0 | — | BLOCKED (human) |
| D04-010 | S3 | Hair | Adrian hair length (short per doc) and cap-like hair shells on both leads. | Skinned hair geometry in the Rocketbox derivative; editing risks rig/blendshape breakage. | — | 0 | — | OPEN (art) |
