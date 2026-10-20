# Phase 06 audio QA report

Updated 20 October 2026. Independent review: `QA_REVIEW.md` (APPROVED_WITH_CONDITIONS; findings fixed and retested). Automated checks only establish that files exist, decode, are mapped and fire at the right
events. **They do not establish natural voice acting or sound quality**: that is the human listening review below,
currently **HUMAN_AUDIO_REVIEW_PENDING**.

## Automated audit (`python3 -I tools/phase06_audio_audit.py` → `tests/phase06/evidence/audio_audit.json`)

| Check | Result |
|---|---|
| every dialogue ID has a take (145) | PASS |
| takes decode, duration 0.2–20 s | PASS |
| no zero-length audio files | PASS |
| recorded text == subtitle == screenplay | PASS |
| one voice per character | PASS |
| every cue the code calls is defined | PASS |
| every defined cue has its file | PASS (14 Phase 06 cues PENDING billable generation) |
| every generated effect referenced by the game | PASS |
| ElevenLabs attribution + manifests | PASS |
| free-plan commercial licence | WARN (no commercial licence) |
| no API keys in tracked files | PASS |
| no API keys in git history | **WARN (S1)**: commit `be68b4a` adds both keys (`4884b8d` removes them) in a public repo → rotate |
| secrets file ignored + excluded from exports | PASS |
| runtime: every line shown with its take loaded and its player started (dummy driver) | PASS 145/145 |
| human listening review | PENDING |

## Runtime dialogue-trigger test

Three headless full-chapter runs on the virtual-input autopilot (`tests/phase06/evidence/chapter_{none,idle,mistakes}.json`):
all reach `chapter_complete` with 0 script errors; every `dialogue_shown` event records `voice: true` and its hold
time. Union: 145/145 lines voiced at their trigger, including all 15 conditional lines (idle barks, failure, retry,
wrong selector, patrol warning, optional skeptical stance). Per-mission coverage:
`tests/phase06/evidence/mission_audio_coverage.txt`.

Limits of this evidence: headless runs use Godot's dummy audio driver. They prove the take is loaded and its player
started on the Dialogue bus at the right event; they cannot prove audible output, mix balance, spatial placement or
lip sync on screen.

## Performance (`tests/phase06/audio_perf_probe.gd` → `tests/phase06/evidence/audio_perf.json`)

| Set | Files | Audio | Load mean / max |
|---|---|---|---|
| Voice takes | 145 | 294.7 s | 0.45 / 0.85 ms |
| Phase 05 effects | 25 | 112.4 s | 0.61 / 1.21 ms |
| Footsteps | 42 | 14.6 s | 0.46 / 1.12 ms |
| All loaded at once | 212 | | +8.4 MB static memory |

Ogg Vorbis streams stay compressed and decode on the mixer thread, so nothing is fully decoded into memory. Takes
load on demand at line start (< 1 ms). Playback latency, mixer CPU and split-screen frame-time impact need the
reference PC (GPU session).

## Human listening review — HUMAN_AUDIO_REVIEW_PENDING

Tester: ______ Date: ______ Headphones: ______ Speakers: ______

| # | Item | How | Expected | Headphones | Speakers | Notes |
|---|---|---|---|---|---|---|
| 1 | Character voice quality | Play M01–M02; listen to Adrian, Noah, Rusk | Each voice fits its character doc; consistent across the chapter | | | |
| 2 | Dialogue clarity | M03 laundry and M06 alarm (loudest scenes) | Every line intelligible without subtitles | | | |
| 3 | Pronunciation | Names: Reyes, Cross, Rusk, Blackridge, Silas | Correct and consistent | | | |
| 4 | Emotional delivery | M06 SH03–SH05 | Natural, not robotic, not over-acted; no cut-off endings | | | |
| 5 | Fast short lines | CH01_M03_DLG017, CH01_M02_DLG008 | Not rushed | | | |
| 6 | Sound-effect realism | Doors, gates, cuffs, bus, footsteps on metal ramp (M05) | Believable, matched to the action | | | |
| 7 | Music / tension balance | M04 stealth → get spotted → reload; M06 alarm | Tension bed audible but under dialogue; chase switch not jarring | | | |
| 8 | Spatial audio | Stand left/right of a talking NPC and a running machine | Sound comes from the source; falls off with distance; both split-screen halves sensible | | | |
| 9 | Ducking | Lines over the M03 machines | Ambience dips smoothly under speech, returns without pumping | | | |
| 10 | Reverb | M01 intake, M05 tunnels vs M02 yard | Light room sound indoors, dry outdoors; never smears speech | | | |
| 11 | Radio | M04 radio bed | Band-limited radio texture | | | |
| 12 | Lip sync | Pause-free M02 mediation close-ups | Jaw moves with speech (amplitude only; no visemes expected) | | | |

Verdict: HUMAN_AUDIO_REVIEW_PENDING
