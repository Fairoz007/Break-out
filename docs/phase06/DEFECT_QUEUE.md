# Phase 06 defect queue

S1 critical, S2 high (both block approval), S3 medium, S4 low. Phase 05 rows still open are carried as D05-*.

| ID | Sev | Area | Defect | Status |
|---|---|---|---|---|
| D06-001 | **S1** | Security | Both ElevenLabs keys are in git history (commit `be68b4a`, owner-requested at the time) of a **public** repository | Removed from tree, moved to `.secrets/`; **owner must rotate/revoke both keys** |
| D06-002 | S2 | Audio | 14 Phase 06 cues have no file (music beds, sting, laundry, tunnel, bus arrival/engine-off, cell-block day bed) | **BLOCKED: awaiting approval** for ~1,280 credits; hooks in place |
| D06-003 | S2 | Audio | No human listening review | HUMAN_AUDIO_REVIEW_PENDING |
| D06-004 | S3 | Audio | Music API refused on the free plan; tension score is sound-effect drones | Documented; paid plan needed for composed music |
| D06-005 | S3 | Audio | Lip sync is amplitude-driven jaw only; no phoneme visemes | Documented limitation |
| D06-006 | S3 | Audio | No sound occlusion | Documented limitation |
| D06-007 | S3 | Audio | Footsteps from stride distance, not foot-contact events (retargeted clips carry none) | Documented |
| D06-008 | S2 | Licence | ElevenLabs free-plan output not licensed for commercial use | Attribution added; regenerate on a paid plan before release |
| D06-009 | S3 | UI test | Walkthrough: graphics dropdown never changes (popup not visible to the scripted click) and leaves the reduced-flash toggle unclickable after it | OPEN (fix on GPU machine; test-side) |
| D06-010 | S3 | Guards | Insignia read "SECURITY OFFICER" | OPEN |
| D06-011 | S4 | Inmates | Same shirt as Adrian's overshirt; scalp blotch | OPEN |
| D06-012 | S3 | Captures | Software-rendered capture queue for M02/M04/M05 stopped early (14 M04 frames) | Re-run on GPU |
| D06-013 | S3 | Audio | Ducking stuck after quit mid-line; music in menu; spots under pause; radio in lip-sync; double cues; phantom landing step; no asphalt steps | FIXED (QA_REVIEW.md 2–8) |
| D06-014 | S4 | Docs | CSVs imported as translations; wording beyond evidence | FIXED (QA_REVIEW.md 10–11) |
| D05-014 | S2 | Performance | Real-time spikes on the reference PC unmeasured after the prop-preload fix | Needs GPU session |
| D05-018/019 | S2/S3 | Bus | Flat exterior panels; illegible driver area | OPEN |
| D05-028 | S2 | Human | Two-controller playthrough | HUMAN_TEST_PENDING |
| — | S2 | Release | Phase 04 never approved; `phase04` branch not pushed; no fresh independent QA approval | OPEN |
