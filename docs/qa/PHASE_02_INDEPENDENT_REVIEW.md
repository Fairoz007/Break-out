# Phase 02 independent QA review

19 October 2026. **INCOMPLETE.** All 305 registry IDs have conservative dispositions in PHASE_02_QA_VERDICTS.json: **10 VERIFIED, 290 IMPLEMENTED_UNTESTED, 5 BLOCKED**. No human controller completion, audio approval, full visual/motion inspection, precise contact measurement or viseme validation is claimed.

## Evidence and method

Reviewed registry/status-tool schemas; technical architecture/animation requirements; screenplay shot specifications; session, completion and scene matrices; canonical dialogue/camera data; chapter/mission, dialogue/cinematic, character, NPC, device, save and HUD code; system-test assertions and automated outputs. Parent executed Godot jobs. Independent reviewer ran only read-only data checks and isolated Python bookkeeping tests, avoiding competing graphical jobs.

Independent checks:

- `python -I tools/phase02_export_data.py --check`: exit0, 145 lines,36 shots,6 missions,19 objectives, no drift. Runtime DialogueDB loads res://data/ch01 only.
- Parsed run evidence and compared every dialogue_shown text/speaker to canonical data:145 unique dialogue IDs, zero mismatches. This proves logged content, not all staging/conditional acceptance.
- Reviewed fresh system suite: **24/24 PASS**, including save overwrite/failure, escort boundary and rendered-input edge retention. Assertions and logs inspected; parent ran engine execution.
- Independently ran `python -I tests/phase02/test_completion_audit.py`:4 tests PASS. Synthetic fixtures demonstrate missing traceability/canonical mappings block completion even with synthetic VERIFIED statuses. They are not runtime evidence.
- `full_current_gfx.json`: **chapter_complete,429.675 real seconds,Windows renderer,all6 missions,19 objectives,36 shots,133 captures**. This source run used speed3 and loaded before the later HUD/camera corrections. It is accelerated staging/regression evidence, not normal-speed playback or isolated performance.
- Final all-fixes Windows headless run:31.993s chapter_complete,19 objectives,36 shots, no ERROR/leak markers. Historical16-object/3-resource shutdown leak did not reproduce. Independently recomputed binary SHA256 and all eight source hashes: match final windows_build_manifest.json. Binary1130566808bytes.
- Targeted source M02 after input fix:until_reached57.301s. Targeted source M03 HUD:59.799s. Exported Windows M03 HUD:57.847s. Source M04 insert cycle2:49.547s. All target reports/logs are under tests/phase02/evidence.

## Defects found, corrections and independent verification

1. Save replacement initially deleted the previous checkpoint before replacement rename. Parent removed that gap, added flush/error checks and focused overwrite/forced-rename-failure tests. Source and passing assertions reviewed. Directory-destination failure is tested; power loss and locking the actual previous save are not simulated.
2. Escort default6m violated required4m. Parent changed to4.0; passing helper test checks follower4.1m(wait),3.9m(no wait),ahead5m(no wait). Actual coroutine pause/resume hysteresis is not independently integrated, so REQ-NPC-002 remains pending.
3. Technical architecture still asserted no playable chapter existed. Parent updated actual runtime ownership/deviations and identified preserved design targets. Full cross-document consistency remains pending.
4. Rendered press/release could vanish before a physics consumer. Reviewed DeviceRouter fix: render rises latch, priority-100 physics distributes edge once, context-aware just_pressed selects render or simulation snapshot. Test preserves true/false/extra-render-frame edge once, without P2 leakage or next-tick repeat. It does not sample hardware transitions occurring entirely between rendered frames. Accelerated post-fix M02 completed.
5. M01 SH05 Noah was nearly hidden by thick door jamb. Independently opened newer full-current0023/0024 after0.45m staging/camera adjustment: Noah face/torso visible left, Adrian right; SH06 centers Noah through thin bars with readable receipt subtitle. Thick-jamb occlusion resolved in samples. Full moving Rusk reaction/blend remains pending.
6. Full-current0059 M03 action prompts crossed divider/overlapped. Parent added WORD_SMART wrapping,24px inset and dynamic vertical placement. Independently opened targeted source shots_m03_hud0011(screen)/0013(lamp): long prompts wrap within their halves, no center overlap; lamp prompt remains below diagram panel. Exported Windows targeted M03 completes too. Broader UI/resolution/settings criteria remain pending.
7. M04 SH03 original sample0079 was dominated by Adrian shoulder/back. First side-camera repair remained obstructed. Independently opened cycle2 shots_m04_insert_cycle2/0010: panel/lower fastener and nearby hand visible, torso no longer fills frame. Framing obstruction resolved. No visible shim grip/lift proves authored action; precise contact remains blocked. Verdict returned from TEST_FAILED to IMPLEMENTED_UNTESTED.

## Actual visual samples and remaining production defects

Independently opened the exact samples named above, plus exported M02 wide/confrontation, source M02 SH04/SH05, full-current M03 SH02, M05 SH02 and M06 SH05/SH06. These limited stills do not approve all36 shots or motion between sampled frames.

- M02 SH02 shows Silas behind Noah while Noah faces away; blocking/shove/Adrian entrance not validated. M02 SH04/SH05 show clear conversation faces/subtitles.
- M03 SH02 Mara face and subtitle are readable. No T-pose/missing mesh seen in inspected conversation samples.
- Full-current0101 M05 SH02 shows handset near chest height while Adrian raised hand touches temple. Grip/contact is visibly wrong in sample, consistent with existing bespoke-contact blocker.
- M06 SH05/SH06 show Rusk under red alarm light and Adrian in solitary. These stills cannot establish steady alarm behavior, handcuff contact, performance or authored facial acting.
- Original exported3x run was deliberately interrupted after delayed M02 readiness; it eventually advanced toSH02, so no indefinite softlock is claimed.

## Blockers and acceptance still pending

- REQ-ANIM-003: generic substitutes (handle_pull -> Push; ball_roll -> OverhandThrow; pipe_knock -> Interact) cannot establish3cm prop/paired contact.
- REQ-ANIM-004: subtitle-driven sine jaw/funnel and random blink are not authored visemes. Blendshape availability is not facial-performance acceptance.
- REQ-DLG-004/REQ-AUDIO-002: VO and human listening approval absent.
- REQ-TEST-003: a person must complete Chapter1 with two controllers. Virtual devices do not replace this.
- Character model paths differ from exact registry Phase15 paths; current acquisition facial derivatives need accepted mapping and measured standing height within3cm. Guard/Rusk share a model.
- Every checkpoint needs exact restore evidence. Generic CP04_A and commit events do not prove all12 checkpoints.
- Objective events do not prove each correct-actor/negative condition. Solo-gate tests cover only M02/M03/M06 subsets.
- Each shot needs authored framing/motion acceptance, including contact work. Activation logs alone are insufficient.
- Original full-run harness quit before rendered end-card capture. Parent fixed harness only to stop driving, wait one real second and frame_post_draw, then capture. Independently viewed source and latest Windows chapter_end_card.png: readable Chapter1 Complete/CH02 Night Shift/Return to main menu. Latest Windows M06 completes52.144s with written=true capture event. Mission06 source gates finish behind sequential P1/P2 knocks and replies. Narrow REQ-UI-005 now VERIFIED; button activation is not claimed.
- Final binary31.993s headless run matches refreshed manifest source hashes. Full source graphical regression predates focused HUD/camera corrections; coverage is combined regression plus focused retests, not a monolithic final-build visual approval.
- Performance/normal reading speed/human pacing remain pending. Fixed-step headless FPS and speed3 graphical metrics do not establish normal1080p60. Top-level game_seconds is final mission time; use mission_game_seconds for chapter sums.

## Verdict policy

Ten narrow requirements have reviewed support: canonical runtime data, movement/collision, split-screen world, simultaneous movement, interaction leases/idempotence, NPC speaking pause, serialized dialogue, produced Windows executable, passing automated suite and correctly gated rendered end card. All other IDs retain explicit pending reasons, with five established human/asset blockers. Event coverage has not been converted into unsupported blanket scene/dialogue/objective/shot approval. Phase02 remains incomplete.
