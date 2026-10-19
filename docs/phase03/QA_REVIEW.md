# Phase 03 independent QA review

Reviewer: Agent 11 Independent QA. Date: 19 October 2026. I did not implement any Phase 03 work, and I launched neither Godot nor Blender.
Machine-readable verdicts are in `docs/phase03/qa_verdicts.json`. First pass: 290 rows, **229 VERIFIED / 45 FAILED / 16 BLOCKED**. Current totals after the second review are at the end of this file. Rows I could not judge are left out, including most ENV aspect rows, all animation-quality CHAR rows, and AI, AUD, PERF and A-* rows.

## Method

- I opened each matched before/after pair (`before/` against `iter05/`, and `iter07/` for bus, solitary and characters) and checked in code that the camera position, target and FOV are identical across the 10 baseline views.
- I also opened all close-up and probe images, the Blender sheets, the hem-texture sheet, and about 45 in-game screenshots. That covers every `shot_activated` frame (36), plus objective, hold and checkpoint frames from `chapter_gfx_shots`, `m06_gfx_shots`, `m05_gfx_shots` and `first_objective`.
- I parsed the event arrays of every JSON report and read every regression log.
- Limits:
  - The autopilot uses virtual inputs at time scale 3, so it proves progression logic only, not feel.
  - No human two-controller playthrough exists.
  - Animation quality cannot be judged from stills.

## Evidence integrity problems (these block sign-off by themselves)

1. **No full graphical chapter completion exists.** `tests/phase03/evidence/chapter_gfx.json` ends `reason: timeout_real` at CH01_M06_OBJ002 with 132 screenshots (`chapter_gfx_timeout_m06.json` is byte-identical). `SESSION_STATE.md` and the D03-001 entry in `DEFECT_QUEUE.md` claim "chapter_complete (134 shots)", which the file does not support. The M06 fix is shown only by a single-mission rerun (`m06_gfx.json`).
2. **The M06 rerun ran with Adrian's texture missing.** `m06_gfx.log` contains `ERROR: No loader found for resource: res://assets/characters/phase03/adrian_body_prison_p03.png`. His clothing renders flat white in `m06_gfx_shots/0004…`, `0014…`, `0018…` and in `m06_solitary_check.jpg`. The `.import` file was written at 23:56, after that run. Every gameplay run that has the texture fix loaded is still missing.
3. **Checkpoint regression exit code.** `regress_summary.txt` records `checkpoints exit=3`, yet the JSON reports 12/12. On completion the script can only exit 0 or 1; 3 is its bad-save-slot abort. This is unexplained.
4. **The performance tooling is broken.** `perf_m01.log` shows a GDScript parse error at `tests/phase03/perf_capture.gd:21`. No `perf_*.json` exists, even though `LAUNCH_AND_TEST.md` cites it.
5. **The report is out of date.** `VISUAL_QUALITY_REPORT.md` still reviews `tests/phase025` evidence and describes assets that Phase 03 has since replaced.

## Per environment and asset

Each entry separates genuine geometry or asset improvement from lighting and colour change, then lists the visible defects that remain.

### Intake (`before/intake.png` vs `iter05/intake.png`, `intake_counter.png`, `intake_lockers.png`, `probe06/holding_bay.png`)

- **Geometry:**
  - Ceiling beams and a wainscot band.
  - A rebuilt counter with split acrylic, monitor and tray.
  - Vented lockers with handles and padlocks.
  - "HOLDING" and "WAIT BEHIND THE YELLOW LINE" signs and a floor line.
- **Lighting/colour:** walls went from olive to white brick and grey, the floor is cleaner, and the fixtures read brighter.
- **Defects:**
  - Benches are slabs on sticks (`probe06/holding_bay.png`).
  - The property tray is a plain box (`chapter_gfx_shots/0011…SH03.png`, D03-015).
  - The VANTAGE badge is a block with a "V" (`0015…SH04.png`).
  - The room is large and empty, with no security hardware.
  - P1's camera collapses to a face close-up in the holding bay (`first_objective/02_objective_set.png`, D03-014).

### Cell Block A (`before/cellblock.png` vs `iter05/cellblock.png`, `cell_interior.png`, `probe06/cellblock_night.png`)

- **Geometry:** a new upper tier with steel doors, walkway slab and railings; cell number plates; a beamed ceiling; red floor lines.
- **Lighting/colour:** cooler grey palette, plus a night variant.
- **Defects:**
  - **Sky is still visible top-right** in `iter05/cellblock.png`, and the same area is a black void at night. This contradicts D03-006 "FIXED".
  - Both upper banks are labelled "A-20".
  - `cell_interior.png` shows only a bed.
  - In M04 the line "Faces at the bars" plays while both prisoners face away from the bars (`chapter_gfx_shots/0073…`).

### Yard and court (`before/yard.png` vs `iter05/yard.png`, `court_layout.png`, `court_ground.png`, `hoop_detail.png`, `yard_fence.png`)

- **Geometry:** perimeter-wall pilasters, razor wire, floodlight poles, and a new chain-link fence module (good up close in `yard_fence.png`).
- **Unchanged:** the hoops, backboards and nets are identical to the baseline (`before/hoop_detail.png`).
- **Lighting/colour:** a blue sky and sun replace the white sky, and the wall changed tint. Most of the difference between the two wide shots is lighting.
- **Defects:**
  - In the wide shots the chain-link mesh disappears and the fence reads as bare poles (`iter05/yard.png`, `court_layout.png`).
  - The wall is still tan/yellow (D03-008).
  - The backboards are plain slabs.
  - The ground is uniform dirt and the crack pattern repeats.

### Laundry workshop (`before/workshop.png` vs `iter05/workshop.png`, `workshop_machines.png`, `blender_props_sheet.jpg`)

- **Geometry:** a genuine rebuild of the washer-extractors, garment presses and lint screen; ceiling beams, signage and a pipe run.
- **Lighting/colour:** the floor and walls are now neutral grey/white, and the rust overlay is gone.
- **Defects:**
  - The hall is still mostly empty.
  - Primitive grey boxes (bin, cabinet) sit in plain view (`chapter_gfx_shots/0052…SH01.png`).
  - **CH01_M03_CS01_SH03 is a blocked frame**: a blurred wall fills the screen (`chapter_gfx_shots/0065…`). D03-017 "reframed" is not evidenced.

### Maintenance (`before/maintenance.png` vs `iter05/maintenance.png`, `maintenance_pumps.png`, `probe06/maint_brake.png`, `maint_east.png`)

- **Geometry:** pump sets rebuilt with volute, coupling guard, motor, valve and gauge; ceiling beams and caged pendants.
- **Lighting/colour:** warmer local pools of light and yellow floor lines.
- **Defects:**
  - **A solid black rectangular shadow covers the east wall** in `iter05/maintenance.png` and `probe06/maint_brake.png`. The D03-007 fix was never recaptured.
  - Most of the hall is near-black.
  - The M04 chase is almost entirely black in both viewports (`chapter_gfx_shots/0082…`).
  - The M04 shim insert is unreadable (`0079…`).

### Solitary and security (`before/solitary.png` vs `iter07/solitary.png`, `m06_solitary_check.jpg`)

- **Geometry:** a mattress and pillow on the bunk, a flush fluorescent fixture and a wainscot.
- **Lighting/colour:** the cell went from near-black to evenly bright, so it now reads as a holding cell, not segregation.
- **Defects:**
  - No toilet or sink is in view.
  - A wall pipe ends mid-wall.
  - The restricted corridor has no matched capture.
  - The M06 handles shot shows black doors with only the tops of two heads (`m06_gfx_shots/0007…`, `chapter_gfx_shots/0122…`).
  - The same guard model is cloned three times in the M06 SH02 frame (`m06_gfx_shots/0009…`).

### Bus exterior and interior (`before/bus.png` vs `iter07/bus.png`, `bus_front.png`, `bus_interior.png`, `bus_work/bus_views_p03.jpg`)

- **Geometry:** rear lamp clusters and grille, front lamps, roof A/C pod, separate treaded wheels with studded hubs, external window bars, mirrors, livery and fleet number.
- **Unchanged:** the interior is the same seats as the baseline; only the lighting is different.
- **Defects:**
  - The paint is flat white and there is no glazing anywhere.
  - The doors are static, and the front door plate stands proud of the body (`bus_p03_front34.png`).
  - The wheel-arch trim is detached dashes.
  - The driver area is a wheel and a box.
  - There is no prisoner cage or partition.
  - `bus_detail.log` bounds of 12.77 x 3.24 x 7.09 m exceed the 11-12 m spec and include an unexplained 7.09 m extent.
  - "bus_front.png" actually shows the rear.

### Adrian (`iter07/adrian_*.png`, `character/adrian_hem_texture_before_after_mask.jpg`)

- **Change:** a hem texture mask. It looks clean only in the static idle close-up.
- **Defects:**
  - Jagged triangular hem intersections in gameplay (`chapter_gfx_shots/0023…`, `0044…`, `0067…`, `0087…`).
  - White triangles at the cuff (`0101…`).
  - Untextured white clothing in the M06 rerun.
  - His wardrobe and hair do not match `ADRIAN_CROSS.md`: the captures show a red sweater, jeans and dress shoes, long slicked hair, and no grey temple or scar.

### Noah (`iter07/noah_*.png`)

- **Change:** none visible this phase.
- **Defects:**
  - Cap-like smooth hair (`chapter_gfx_shots/0112…`).
  - A denim jacket and white sneakers, which contradict `NOAH_REYES.md` (prison undershirt, repaired boots).
  - In M06 SH04 Noah stays standing while the guard orders both prisoners to their knees.

### Lighting

- **Real gains:**
  - The exterior is sky-lit with readable shadows.
  - Interior light pools come from visible fittings.
  - Render settings are recorded per capture, and the before/after cameras are matched.
- **Defects:**
  - The maintenance shadow artefact.
  - Unreadable dark gameplay in M04 (LIGHT-011).
  - Several dark or blocked cinematic frames.
  - `iter07/cameras.json` records only 2 of its 9 PNGs.

## Gameplay and process (from the reports)

- **Verified as automated logic:**
  - Menu to New Game to the first objective (`first_objective.json`).
  - All 19 objectives in order, across `chapter_gfx.json`, `m06_gfx.json` and `chaos_idle.json`.
  - M01-M05 complete in the graphical run, and M06 in the single-mission rerun.
  - All 36 shots activate with their registered lens. Of those, 7 frames are defective; see the SHOT rows.
  - 132 dialogue lines are shown in completed graphical missions. The 13 conditional lines appear only headless, so they are BLOCKED.
  - Movement speeds, crouch, jump, camera collision and device isolation all pass in the regression suites.
- **Navigation:** `autopilot_stuck` at about (52.8, 0, 0.8) in M04 recurs in every chapter run.
- **Failed:**
  - PLAY-018: no blocker-free full graphical run.
  - PROC-003, PROC-005 and PROC-006: stale or incorrect documentation.
  - QA-014: unsupported completion claims.
  - QA-011: the exported exe was never run.

## Decision: **NOT APPROVED**

Blocking items:

1. Rerun the full graphical chapter after the M06 fix and the texture import, and get `chapter_complete`. Correct SESSION_STATE and DEFECT_QUEUE to match the evidence.
2. Fix Adrian's texture loading and the hem/cuff intersections, and reverify them in gameplay shots.
3. Close the cell-block roof (sky visible) and the maintenance black-rectangle shadow, then recapture. Fix the duplicate "A-20" labels.
4. Reframe or relight these broken cinematic shots: M03 SH03, M04 SH03/SH05/SH06, M05 SH02, M06 SH01/SH06. Fix the M04 chase visibility and the staging contradictions (M04 count, M06 knees).
5. Bus: glazing, door function, paint/PBR, a driver area and a cage; resolve the bounds anomaly.
6. Bring both leads into line with their character documents: wardrobe, hair, and identifying marks.
7. Fix `perf_capture.gd` and record real split-screen performance. Explain the checkpoint exit code 3. Run the exported exe.
8. A human two-controller playthrough, which cannot be substituted by the autopilot.

---

## Second review (20 October 2026)

Same reviewer and rules: I edited only these two files, launched neither Godot nor Blender, and opened every image cited below myself. I re-judged all FAILED and BLOCKED rows, and all 36 SHOT rows, against the new evidence. I did this because the `chapter_gfx_shots/` frames cited in the first pass were overwritten by the rerun, so the first-pass SHOT citations now point at different images.

**Totals: 295 rows, 258 VERIFIED / 20 FAILED / 17 BLOCKED.** That is 25 rows raised to VERIFIED, 5 newly judged rows VERIFIED, 3 FAILED rows moved to BLOCKED, and 1 VERIFIED row moved to FAILED (a regression).

### Evidence checked

- **`exe_chapter.json` / `.log`:** the log banner reads "v4.7.2.stable.official", so this is the export template rather than the Steam editor. The run reaches `chapter_complete` with 19/19 objectives, 6 mission completes, 36 shots, 133 dialogue lines and 134 screenshots, and logs no error lines. I opened about 40 of its frames, including every `shot_activated` frame and `chapter_end_card.png`.
- **`export.log`:** ends with savepack `[ DONE ]`. The exe is timestamped 00:40.
- **Source run:** `chapter_gfx.json` also reaches `chapter_complete` with 134 shots, so the first-pass objection (`timeout_real`) is resolved.
- **Regressions:** `regress_summary.txt` now shows all four suites at exit=0, and checkpoints at 12/12.
- **Performance:** `perf_m01.json` is a real-time M01 run in a 1920x1080 window with two 958x1080 viewports. It records 91 fps mean, p99 13.6 ms, a 142 ms maximum spike, 2.5 GB VRAM and a 6.7 s load. Only M01 was measured.
- **New captures:** all of `iter08/`, plus `zoom_m04sh01_m05sh02.jpg`, `grip_sweep.png`, `m03_gfx_shots/0017` and `/0020`, and `m06_gfx_shots/0007`.

### Fixes confirmed

| Defect | Evidence | Verdict |
|---|---|---|
| Full graphical chapter (D03-019) | `exe_chapter.json`, `chapter_gfx.json` | PLAY-018 and CIN-012 VERIFIED |
| Exported build (QA-010/011) | `export.log`, `exe_chapter.log` | VERIFIED |
| Checkpoint exit code | `regress_summary.txt` | PLAY-015 VERIFIED |
| Performance capture | `perf_m01.json` | PERF-001/002/005/006/007/016 and QA-009 VERIFIED |
| Cell-block sky gap, duplicate "A-20" (D03-022/023) | `iter08/cellblock.png`, `cellblock_night.png` | CELL-000/004/009/014 VERIFIED |
| Maintenance black rectangle (D03-007) | `iter08/maintenance.png`, `maint_brake.png` | MAINT-000 VERIFIED |
| Black M04 chase (D03-025, chase part) | `exe_chapter_shots/0082` | LIGHT-011 VERIFIED |
| Fence vanishing at distance (D03-030) | `iter08/yard.png`, `yard_far_fence.png`, exe `0040` | COURT-009 VERIFIED |
| Hem/cuff zigzags, white Adrian (D03-009/020) | exe `0044` (zoomed), `0087`, `0023`, `0101`, `0129` | CHAR-010 VERIFIED |
| M03 SH03 blocked insert (D03-024) | exe `0065` | VERIFIED. The `m03_gfx` frame `0017` renders the plate text mirrored ("NO / FFO"); the exported build reads correctly. |
| M04 SH01/SH05/SH06 staging (D03-026/027) | exe `0073`, `0088`, `0089` | VERIFIED |
| M06 SH01 heads only, SH06 crop (D03-028) | exe `0122`, `0129` | VERIFIED. SH01 is still dark and the heads are buried against the doors. |
| Bus glazing, cage, true front view (D03-031) | `iter08/bus_front_true.png`, `bus_cabin_fwd.png` | BUS-011/014 VERIFIED |
| Stale documentation | `SESSION_STATE.md`, `VISUAL_QUALITY_REPORT.md`, `LAUNCH_AND_TEST.md` | PROC-003/005/006 VERIFIED (see QA-014 for caveats) |

### New and remaining defects

1. **Regression in M03 SH06 ("Adrian close then two-shot").** The frame shows an empty shelf, rail and cart while Adrian's line plays; Adrian is not in frame. This happens in both the exported build (`exe_chapter_shots/0068_shot_activated_CH01_M03_CS01_SH06.png`) and the post-reframe `m03_gfx_shots/0020_shot_activated_CH01_M03_CS01_SH06.png`. The pre-reframe source run (`chapter_gfx_shots/0068…`) framed him correctly. The last M03 reframe broke this shot, and no document mentions it.
2. **The M04 shim insert is still black,** with no shim readable (`exe_chapter_shots/0079…`). The D03-025 entry itself says PARTIAL.
3. **The M05 handset is unreadable.** The prop now exists, but it is hidden behind Adrian's open, splayed hand at his neck (`exe_chapter_shots/0101…`, `zoom_m04sh01_m05sh02.jpg`, `iter08/handset_grip.png`).
4. **Staging still contradicts the lines.** In M06 SH04 Noah stays standing during "On your knees. Both of you" (`exe_chapter_shots/0127…`). In M02 Adrian "holds Silas's attention" facing a blank wall with Silas out of his view (`exe_chapter_shots/0040…`).
5. **Character likeness and wardrobe still contradict the character documents (D03-032 OPEN),** and the hair is still a cap-like shell (`iter07/adrian_close.png`, `noah_close.png`, `exe_chapter_shots/0112…`).
6. **Bus:**
   - The doors are static.
   - The paint is flat white with no wear.
   - The wheel-arch trim renders as detached arcs (`exe_chapter_shots/0006…`).
   - The rear window has no guard (`iter08/bus.png`).
   - The driver area is not visible in any capture.
   - `bus_detail.log` bounds are still 12.77 x 3.24 x 7.09 m, while `VISUAL_QUALITY_REPORT.md` states 12 x 2.5 x 3.1 m. That is an unsupported claim (QA-014 BLOCKED).
7. **Yard:**
   - The wall is still tan (D03-008).
   - The backboards are plain slabs, and the hoop geometry is unchanged from Phase 02.5.
   - The ground is bare.
8. **Intake, workshop and solitary have no new captures,** so their first-pass FAILED verdicts stand: sparse rooms, the box property tray, and a solitary cell with no toilet in view.
9. **Navigation snag:** `autopilot_stuck` at (52.8, 0, 0.77) in M04 recurs in every chapter run, including the exe run. It recovers, but it is a likely snag for human players.
10. **Still BLOCKED, for lack of evidence:**
    - PLAY-011: there are no M01/M04/M05 interactable-ownership tests.
    - PLAY-016: there is no evidence of Continue after a corrupt save.
    - LIGHT-004: shadow stability needs a motion capture.
    - QA-001: no static parse check across all scripts has been reported.
    - 12 conditional DLG lines appear only in the headless runs.
11. **Not testable here:** a human two-controller playthrough and an audio listening review (D03-034).

### Decision (second review): **NOT APPROVED**

Playability, the exported build, regressions and performance are now evidenced, and most first-pass visual blockers are genuinely fixed. Approval is still blocked by:

1. The new M03 SH06 regression, plus the M04 SH03 and M05 SH02 cinematic defects.
2. The lead characters not matching the character documents (D03-032).
3. The bus scope: doors, paint and PBR, the rear window guard, the driver area and the bounds anomaly.
4. The remaining environment FAILs: intake, workshop, solitary and the yard.
5. Staging contradictions in M02 and M06.
6. No human two-controller playthrough.
