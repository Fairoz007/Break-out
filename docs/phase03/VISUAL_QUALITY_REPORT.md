# Phase 03 visual quality report

20 October 2026. Author: implementation (Agents 03–05/08). Independent review: `QA_REVIEW.md` (Agent 11) — this report
does not approve its own work. The earlier asset-pass report is preserved as `VISUAL_QUALITY_REPORT_ASSETPASS_20261019.md`.

## Method

Matched cameras: `tests/phase03/visual_capture.gd` reproduces the ten Phase 02.5 review cameras exactly
(`visual_evidence/before/` = Phase 02.5 `integration/verified/`) and adds close-ups. Latest sets: `iter05/` (all),
`iter07/` (characters, bus, solitary), `iter08/` (cell block, yard, fence, maintenance, bus front/cabin). Every
`cameras.json` records renderer, quality level and SSAO/SSIL/fog/tonemap state. In-game evidence:
`tests/phase03/evidence/exe_chapter_shots/` (exported build) and `chapter_gfx_shots/` (source, speed 3).
Comparison sheets: `visual_evidence/cmp_*.jpg`.

Distinguishing geometry from lighting: each item below says which it is.

## Lighting and rendering (all areas)

| Setting | Before | After |
|---|---|---|
| Tonemap | Filmic, exposure 1.0 | AgX, exposure ×1.6 |
| Indirect light | Flat colour ambient | SSIL (q≥1) + SSAO tuned (radius 1.1, power 1.6) |
| Fog | none / height fog | volumetric fog (q2), sky-safe height fog otherwise |
| Shadows | hard | PCSS soft (light size 0.08–0.12 m, sun 0.6°), soft filter quality 3, 4-split sun |
| Exterior | grey procedural sky, colour ambient | blue procedural sky, sky ambient + reflections |
| Interiors | omni lights below ceilings | `ceiling_light()`: downward spot from each fitting + weak uplight; fittings never shadow themselves |
| GI | — | SDFGI evaluated and rejected (darkened rooms, black leaks through 0.25 m walls: `cmp_iter02_q.jpg`) |

## Per area (geometry/material changes vs lighting-only)

| Area | Geometry / asset changes | Material changes | Lighting | Remaining problems |
|---|---|---|---|---|
| Intake | New processing counter (laminate ledge, acrylic screen with tray pass-through, monitor/keyboard/trays), louvred steel lockers, concrete beams, steel door frames, signage, floor lines | Painted CMU walls with dado and skirting; painted-epoxy floor | 11-fixture grid, 3 shadowed | Property tray is still a flat box (D03-015); no body scanner |
| Bus | Coach proportions (12 × 2.5 × 3.1 m), new 1 m wheels with tread/rims/lug nuts (separate, they turn on arrival), headlamp clusters, grille, wipers, destination sign, plates, luggage bays, marker lamps, tail clusters, engine louvres, roof A/C, prisoner cage partition, arrival roll in SH01 | Clear-coat paint, reflective security glazing, double-sided shell | Exterior sky | Doors do not open; panels still broad; driver area basic |
| Cell block | Inaccessible upper tiers with steel doors, walkway slabs and railings (closes the sky gap), ceiling over the tier zone, beams, cell numbers, red boundary lines | Painted CMU (cream / slate-blue dado), sealed floor | High-bay run, night blue safety lights, chase service lamps | Cells sparsely furnished; night shim insert dim |
| Yard + court | Precast coping, pilasters every 6 m, concertina razor wire, galvanised floodlight columns; chain-link distance stand-in | Board-formed concrete wall (cooled grey) | Sun + sky ambient | Court/hoops are the Phase 02.5 geometry (QA: same models); yard sparse |
| Laundry workshop | Industrial washer-extractors, garment presses, isolation switch (M03 lever), lint screen frame, beams, signage, aisle lines | Painted CMU, epoxy floor, grey pipework (was orange rust) | 22-fixture grid | Room still open/uniform; no linen carts beyond existing |
| Maintenance | End-suction pump sets (motor, coupling guard, volute, valves, gauges), service headers, cable tray, beams, hazard lines, signage | Painted wear band on board-formed concrete | Pendant high-bays emitting downward (no shade shadow) | Large bare wall areas |
| Solitary | Flush ceiling fittings; bunks kept clear of the pipe stances; seat marks on the bunk ends | Painted CMU with dado | Brighter cell fills | Very small set; little detail |
| Adrian / Noah | — | Adrian sweater texture repaired (hem/cuff zigzags) | — | Likeness/wardrobe do not match the character documents (D03-032) |

Process reality: several first attempts failed visibly and were caught only by captures — SDFGI darkening, dark
first lighting pass, mipmaps disabled on new textures, the fence fix hiding the posts, the hem fix rendering white
before import, invisible hand props. Each is logged in `DEFECT_QUEUE.md`.

## Not approved by this report

Production-art sign-off of the characters, a human two-controller playthrough and an audio listening review cannot be
claimed from captures. See `QA_REVIEW.md` for the independent decision.
