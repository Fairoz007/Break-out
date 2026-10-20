# Phase 04 visual quality report

## Realistic asset replacement session — 20 October 2026

**INCOMPLETE.** The newer ASSET_ACQUISITION_REPORT.md and REALISTIC_INDEPENDENT_QA.md cover this session.
Fresh same-camera baseline: `visual_evidence/realistic_before/`; updated captures: `realistic_after/`;
detail views: `realistic_details/`; labelled comparisons: `realistic_comparisons/`.

New geometry: coach underside/suspension/exhaust; actual perforated basketball board and refined chain links;
smooth recessed-seam basketball; detailed welded upper-tier doors; acquired textured dryer and ironing units;
tubular single beds with actual pillow, mattress and draped blanket geometry. Court texture scale adjusted.
Existing bus folding doors, cage divider, curved hoop support and previous texture edits predate this session.
Do not attribute those earlier features to this pass.

Visible benefits are strongest in cell hardware/bedding and machine fronts. Bus undercarriage is mostly hidden
in existing cinematics. Whole-scene realism is not achieved: protagonist hair/wardrobe, contact animation,
bus body finish/cabin, true bunks, washing machines, repeated architecture and sparse dressing remain open.
The following report is retained historical context and its iter01 images are not the new-session baseline.

Final evidence gate:16 matched environment captures plus5 detail captures passed; seven runtime GLBs passed
binary/dependency integrity checks. Source and exported Windows chapter autopilots completed without
resource/script errors or stuck events. See `tests/phase04/evidence/realistic_validation.json`.
The intermediate `realistic_game.json` and missing-bed capture log are explicitly rejected despite reporting
chapter_complete. These automated results establish technical regression evidence, not production visual approval.

## Earlier visual pass (retained)

20 October 2026. Author: implementation. Not self-approving — see `QA_REVIEW.md` (Agent 14) for the independent decision.
Baseline images: `visual_evidence/baseline/` (fresh capture of the committed Phase 03 state, same cameras as
`tests/phase03/visual_capture.gd`). Phase 04 images: `visual_evidence/iter01/`. Sheets: `visual_evidence/cmp_*.jpg`.

## Genuine geometry / asset changes (not lighting)

| Subject | Change | Evidence |
|---|---|---|
| Basketball hoops | Primitive post/arm/slab board replaced by a Blender gooseneck unit: concrete footing, bolted base plate with anchor nuts, square post, bent gooseneck, braces, perforated steel backboard with painted border and shooter's square, spring-mount double rim, 12-chain steel net. Same metric layout and post collider. | `cmp_court01.jpg`, `iter01/hoop_detail.png`, `blender/hoop_gooseneck.png` |
| Bus | Functional folding two-leaf front entry door (framed glass, grab rail), opens after the SH01 arrival stop (kerb side, facing the intake; SH01 films the other side). Rear window security bars; wheel-arch flares now seated on the panel. True vertex bounds 12.12 x 3.24 (incl. mirrors; body 2.52) x 3.57 m (incl. antenna); Godot scales the coach to 12.0 m. Licence/provenance: `assets/props/phase03/blackridge_transport_bus_p03.asset_record.json` (OpenGameArt "3D Bus", CC0). | `cmp_bus01.jpg`, `iter01/bus_doors_open.png` |

## Texture / material changes (not geometry)

| Subject | Change | Evidence |
|---|---|---|
| Adrian | Salt-and-pepper grey at the left temple, pale healed cut through the left brow, faded grey crew-neck shirt in the V-neck so the orange layer reads as an overshirt (ADRIAN_CROSS.md). | `character/adrian_temple_brow_zoom.jpg`, `iter01/adrian_face.png`, `adrian_brow.png` |
| Noah | Denim jacket recoloured to a flatter prison blue — it is still the denim-jacket garment (collar, buttons, chest pockets: geometry unchanged), so "blue prison undershirt" is only approximated; white sneakers to dark leather boots; burn on the right wrist enlarged after QA (`iter02/noah_wrist.png`). | `cmp_char01.jpg`, `iter01/noah_close.png`, `noah_full.png` |
| Yard wall | Grey board-formed precast set (`concrete_wall_008`). Still reads warm under the morning sun — lighting, not texture. | `cmp_yard01.jpg` |

## Layout

Horizontal (top/bottom) split-screen option: `tests/phase04/evidence/ui_walkthrough/06_horizontal_layout_in_game.png`.

## Remaining visual problems

- Hair: Adrian's hair is longer than "short" in the character document; both leads have cap-like hair shells. Needs
  hair-geometry art; not attempted to avoid breaking the skinned/blendshape derivatives.
- Faces are Rocketbox identities, not authored likenesses; no facial performance/VO.
- Paired-contact animation (shove, cuffing, help-up) still uses single-actor clips.
- See Phase 03 QA FAILED rows still open for intake/workshop/solitary detail.
