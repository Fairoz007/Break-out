# Phase 04 independent QA review

Reviewer: Agent 14 Independent QA. Date: 20 October 2026. I did not implement any Phase 04 work.
Verdicts: `docs/phase04/qa_verdicts.json` (656 rows: **513 VERIFIED, 107 FAILED, 36 BLOCKED**). Of the 388 non-carried
P04-* rows, I judged 274 (187 VERIFIED, 55 FAILED, 32 BLOCKED). I left 114 without a verdict because no Phase 04 evidence
covers them: most ENV sub-items, LIGHT-004..013, PERF-002..005/007/008/010, CHAR-005/006, BUS-011, and QA-001/009
(QA-001/009 are this review itself).

## Method

- Read-only. I did not launch Godot, Blender or the exe.
- I opened and looked at the actual images: all 12 UI walkthrough frames; the iter01 character, bus, court and yard
  captures; all cmp_* sheets; the Blender hoop render; contact sheets of all 36 shot frames and 12 gameplay frames from
  `final_exe_shots/`, plus about 10 frames at full size; and baseline crops for comparison.
- I parsed `final_exe.json`, `final_exe_m06.json`, `baseline_exe.json`, `m04_headless.json`, `perf_m0*.json`,
  `guard_ai_tests.json` and the logs. I read `guard_ai_tests.gd`, `ui_walkthrough.gd`, `parse_check.gd` and the
  autopilot's movement code.
- I checked dialogue programmatically: every `dialogue_shown` event's speaker and text matches `data/ch01/dialogue.json`,
  and every `shot_activated` lens matches `data/ch01/shots.json`. The dialogue, shot and objective rows are batch-checked
  from these events plus sampled frames, and their reasons say "sampled".
- All runs are virtual-input autopilot runs: time scale 3 for chapter runs, real time for perf runs. Nothing that needs
  a human two-controller playthrough or an audio listening review has been VERIFIED. Those rows are BLOCKED.

## Milestones

### Playability — mostly works
- **Works:**
  - Main menu, New Game by real click, and the first objective at 28.7 s (`baseline_first_objective.json`,
    `ui_walkthrough/00`, `05`).
  - Movement, crouch, jump and collision: `regress_gameplay.log` 14/14 and system suite 24/24.
  - Checkpoints 12/12, and Continue resumes a save (`ui_walkthrough/11_continue_resumes.png`).
  - The Phase 03 BLOCKED item P03-PLAY-011 is now resolved: interactions in all six missions fire for their owning
    player in the exe run.
- **Defects:**
  - P04-PLAY-009: camera rotation by look input is never tested. The cited tests cover camera collision only.
  - P04-PLAY-016: `autopilot_stuck` in M04. Adrian was blocked for more than 6 game seconds at (52.8, 0, 0.76) despite
    the sideways nudge (`final_exe.json` t=199.3; the same event is in `baseline_exe.json`). He recovered by
    replanning, but the snag is unexplained.
  - Carried PLAY-016: there is still no evidence that a corrupt save disables Continue.

### Co-op — works in automation; physical devices untested
- **Works:**
  - Horizontal split option: the checkbox was really clicked, and New Game and Continue both open top/bottom views with
    independent cameras and prompts (`ui_walkthrough/02`, `06`, `08`, `11`).
  - Device exclusivity, simultaneous movement, mutual skip, disconnect pause and the solo gates all pass.
- **Blocked:** keyboard+controller and two-controller play (COOP-004/005). No physical devices were used.

### Characters and animation — FAILED. Texture changes only, no geometry
- **Changes:** texture only.
  - Adrian: a pale healed cut in the left brow (VERIFIED as present, `iter01/adrian_brow.png`) and a grey crew-neck in
    the sweater V.
  - Noah: the white sneakers became dark shoes.
- **Defects:**
  - Adrian's hair is still long and swept back, not "short" (`final_exe_shots/0068`).
  - Adrian's grey temple reads as two or three grey blotches above the ear in profile and is invisible from the front
    (`iter01/adrian_face_left_final.png`, `adrian_face.png`).
  - Adrian still wears a single ribbed orange sweater, not a grey shirt under an orange overshirt.
  - Noah's "plain prison chambray" is the same denim trucker jacket, lightened. The collar, button placket and flapped
    chest pockets are all intact (`iter01/noah_close.png`, `cmp_char01.jpg`). The character document specifies an
    undershirt only.
  - Noah's wrist burn is not visible in any capture.
  - Both leads have cap-like hair shells, and a translucent hair-card shard sticks up above Adrian's crown
    (`iter01/adrian_brow.png`).
- **Animation:** only stills exist, so most ANIM rows are BLOCKED for motion review. These rows FAILED:
  - Pull is "Push played in reverse" (`anim_inventory.json`).
  - No climb is shown.
  - Cooperative assistance: at the M05 manual gate Adrian lunges mid-corridor with both hands in the air, touching
    nothing (`final_exe_shots/0094`).
  - Gestures and orientation: in M02 Adrian faces a blank wall while "holding Silas's attention" (`0040`), and M05 SH02
    shows a hand to the head (`0101`).

### Bus — one genuine geometry change
- **Genuine geometry:** two separate framed door leaves that open after the arrival stop (`iter01/bus_doors_open.png`,
  `bus_detail.log` Door_L/Door_R, `bus_doors` event). BUS-007 is VERIFIED.
- **Caveat:** SH01 frames the bus from the non-door side (`final_exe_shots/0006`), so players never see the doors open.
- **Remaining defects:**
  - The GLB still logs (12.77, 3.24, 7.09) m.
  - Panels are flat white with no wear.
  - The wheel-arch trim stands off the body (`0006`).
  - The rear window is unguarded (`iter01/bus.png`).
  - The driver area is not legible.
  - No licence is recorded.

### Court — genuine geometry improvement
- **Works:** both hoops are now Blender gooseneck units with a footing, bolted plate, perforated board with border and
  shooter's square, spring-mount rim and chain net (`iter01/hoop_detail.png`, `blender/hoop_gooseneck.png`, the
  `yard.png` far hoop zoomed against baseline). Carried COURT-005 (plain slab backboard) is resolved. Markings, asphalt,
  fencing, M02 navigation and interactions are intact.
- **Defect:** the surroundings are still sparse (COURT-010 FAILED).

### Environments — no Phase 04 geometry work
- **Yard wall:** a texture swap only. Brick-like tan became board-formed panels that still read tan and look flatter
  (`cmp_yard01.jpg`). D04-007 is correctly marked PARTIAL.
- **Yard ground:** bare uniform dirt.
- **Intake:** the slab benches and the box property tray are unchanged (`ui_walkthrough/06`, `final_exe_shots/0011`).
- **Not reviewed:** cell block, workshop, maintenance and security have no Phase 04 change or capture, so I left those
  rows without a verdict.

### Lighting — unchanged, judged on the current images
- **Works:** WorldEnvironment, interior/exterior lighting, shadows, no overexposure, and matched before/after cameras.
- **Defect:** LIGHT-015 FAILED. The M04 SH03 insert and the M05 SH02 handset are lost in darkness.
- **Evidence gap:** `iter01/cameras.json` records only 2 of its 16 captures.

### AI — genuine new behaviour, partly tested
- **Works:** `guard_ai_tests.json` 5/5 in the real M04 cell block with virtual-device movement. It shows hearing
  (sprint is heard, crouch-walk is silent), independent per-player detection, SUSPICIOUS → SEARCH → return to patrol,
  and walls blocking sight. Mission 04 still completes with the new AI active.
- **Untested:**
  - ALERT and chase (AI-006/007 FAILED).
  - "Noise halved through walls".
  - Part of the search test teleports the player out of sight.
- **Not seen in the chapter:** the chapter autopilot never triggers the new states (no guard_heard or guard_suspicious
  events in `final_exe.json`).

### Missions — completion verified; failure paths not
- **Works:** all six missions run start to finish on the exe, with 19/19 objectives, 13 checkpoints, NPC moves and
  transitions.
- **Defects:**
  - Failure and retry is untested in every mission (MIS-0N-009 FAILED). `m04_headless.json` is a normal completion
    run with no detection or fail event.
  - 12 conditional dialogue lines (two per mission) are never triggered (MIS-0N-007 FAILED, DLG rows FAILED).

### Cinematics — mostly plays; three framing/blocking defects remain
- **Works:**
  - All 17 cinematics, 36/36 shots (lenses match) and 133 main lines play, with verbatim canonical text.
  - The M03 SH06 regression from Phase 03 is fixed: Adrian is now in frame (`0068`).
- **Still failing:**
  - M04 SH03 shim insert unreadable (`0079`).
  - M05 SH02 handset unreadable (`0101`).
  - M06 SH04: Noah stands while ordered to kneel (`0127`).
  - M02: Adrian faces a blank wall (`0040`).
- **Not covered:** there is no solo-configuration cutscene run.

### Audio / UI
- **Audio:** all P04-AUD rows are BLOCKED. Nothing has been listened to.
- **UI that works:** menu, New Game, Continue, pause/resume/quit, HUD, prompts and subtitles. All are readable in split
  views.
- **UI defects:**
  - Change device / Auto-detect were never pressed (UI-004).
  - The sliders, graphics, invert and flashing settings were never exercised (UI-006).
  - Credits, Quit and Restart-from-checkpoint were never pressed (UI-011).
  - No per-mission completion UI was captured (UI-010).

### Full playthrough
- **Works:** the automated exe run completes M01→M06 with real mechanics. The autopilot makes no place() or commit()
  calls.
- **Blocked:** the human two-controller playthrough has not happened.

### Performance / build
- **Performance:** all six missions run in real time at 1920x1080 split-screen, at 91–139 fps mean, p99 ≤ 13.6 ms
  (PERF-011 VERIFIED). Caveats:
  - These runs are from the project, not the exe.
  - max_ms is clamped at about 150 ms in every mission while M06 process_ms_max is 903 ms, so the hitch statistics
    understate the worst frames.
  - M01 runs 3,944 draw calls p50 (14,192 max) with no analysis. PERF-001 "optimised" and carried PERF-008
    bottlenecks FAILED.
  - No GPU usage is recorded (carried PERF-004 FAILED).
- **Build:** export [DONE]. The full chapter on the exe reaches chapter_complete. The re-export (`final_export2.log`)
  differs only by adding the `tests/phase04/anim_inventory` files, and no game source changed afterwards, so the
  chapter evidence stands. Note: test scenes ship inside the release pack.

### Evidence integrity
I found no fabricated result files. These claims are unsupported (QA-003 and carried QA-014/PROC-002/PROC-003 FAILED):

- DEFECT_QUEUE says "60/60 compile", but `parse_check.json` reports checked 59.
- "Plain prison chambray" is not what the captures show.
- `cmp_char01b`/`c` label an intermediate iteration as BEFORE: the grey V-neck is already present, and baseline has no
  adrian_face capture.
- `cmp_char01e`/`f` have blank BEFORE panels.

## Release-candidate decision: **NOT APPROVED**

The Phase 04 completion conditions are not met: every mandatory row independently VERIFIED, plus the human playthrough
and audio review (`SESSION_STATE.md`, `COMPLETION_AUDIT.md`). Blocking items:

1. **Human acceptance missing.** There has been no two-controller playthrough and no audio listening review
   (COOP-004/005, all AUD rows, CIN-008).
2. **Lead characters do not match their documents.** Adrian has long hair, blotchy temple grey and a sweater instead of
   an overshirt. Noah still wears the denim jacket and his burn is not visible. Both have cap-like hair and Adrian has a
   hair-shard artefact. Evidence: `iter01/adrian_*`, `iter01/noah_*`, `cmp_char01.jpg`.
3. **Animation is not reviewed in motion,** and the stills show contact and orientation failures: Pull is a reversed
   Push, and the M05 gate (`final_exe_shots/0094`) and M02 hold (`0040`) are wrong.
4. **Cinematic defects remain:** M04 SH03 (`0079`), M05 SH02 (`0101`) and M06 SH04 (`0127`).
5. **Failure/retry paths and the 12 conditional dialogue lines are untested** in Phase 04.
6. **Guard ALERT/chase is untested.**
7. **The bus still fails** on dimensions (`bus_detail.log`), materials, trim, the rear window guard, the driver area and
   its licence. Environments other than the court have no Phase 04 improvement, and the yard wall still reads tan.
8. **There is an unexplained M04 navigation snag** (`final_exe.json` autopilot_stuck, t=199.3).

What genuinely improved in Phase 04, and holds up: the guard AI hearing/suspicion/search loop, the horizontal split
option, the UI walkthrough with real clicks, the compile check, real-time performance for all six missions, the real
gooseneck hoops, the functional bus doors, the fixed M03 SH06 framing, and Adrian's brow cut.
