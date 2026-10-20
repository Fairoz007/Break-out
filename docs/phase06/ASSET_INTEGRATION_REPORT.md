# Phase 06 asset integration report

Updated 20 October 2026. **Status: audit done; no new 3D assets integrated in this Phase 06 session** (time went to
the audio system and pipeline). The Phase 05 character work below is the latest integrated asset work.

## Priority list and current state

| Asset | State | Evidence | Next action |
|---|---|---|---|
| Adrian hair + clothing | DONE (Phase 05): short hair shells with grey temple; Rocketbox m012 collared shirt as orange overshirt + separate grey undershirt (collar and hem); 37 clips intact | `tests/phase05/evidence/adrian_garment/*.jpg`, `tools/phase05_adrian_garment.py` | human visual review; shoulder zigzag texture mark (S4) |
| Noah hair + uniform | DONE (Phase 05): cropped curls; blue prison shirt (short sleeves, bare forearms), grey undershirt, orange trousers, healed burn on the right wrist | `tests/phase05/evidence/noah_burn_sheet.jpg` | burn is too small to read in wide cinematic shots (no shot frames it) |
| Guard uniforms | Realistic Rocketbox security uniform | `tests/phase06/evidence/npc_GUARD.jpg` | **D06-010**: sleeve patches and name bar read "SECURITY OFFICER" (private security); repaint as corrections insignia |
| Inmates | Realistic; same collared shirt as Adrian's overshirt | `npc_INMATE.jpg` | **D06-011**: give generic inmates a variant (tee or different shirt colour) so Adrian reads distinct; reddish scalp blotch |
| Silas, Mara | Realistic, match docs | `npc_SILAS.jpg`, `npc_MARA.jpg` | — |
| Prison bus | Proportions, wheels, doors, glazing, cage good; exterior still flat white panels, driver area illegible | D05-018/019 | panel seams/rivets/wear in Blender (`tools/phase04_bus_court_build.py` base) |
| Basketball court | Gooseneck hoops, perforated steel backboards, markings (Phase 04 + Codex) | `docs/phase04/BUS_COURT_WORK.md` | GPU capture review |
| Cell doors, security equipment, workshop machinery, furniture, maintenance equipment | Codex Phase 04 swaps integrated (bunks, tier doors, dryers, ball) and Phase 03 Blender props | `docs/phase04/ARCHITECTURE_WORK.md` | GPU capture review; intake benches/tray (D05-020), yard dirt (D05-021) |

No assets were downloaded or purchased in Phase 06. Licence records for existing assets remain in
`asset_library/licenses/` and `ASSET_MANIFEST.md`.
