# Phase 06 requirements matrix

Statuses: NOT_STARTED, IN_PROGRESS, IMPLEMENTED_UNTESTED, FAILED, BLOCKED, VERIFIED. "VERIFIED" here means automated
evidence in this Linux session (headless runs, decode checks, software renders); anything needing ears, a GPU or
Windows is marked accordingly.

| ID | Requirement (prompt section) | Status | Evidence / blocker |
|---|---|---|---|
| P06-01 | Phase 05 recovery, baseline docs (§1) | VERIFIED | `BASELINE_AUDIT.md`, this file, `SESSION_STATE.md`, `DEFECT_QUEUE.md` |
| P06-02 | ElevenLabs pipeline: TTS, voice selection, SFX, download, retry, usage tracking, metadata, validation (§2) | VERIFIED | `tools/elevenlabs_client.py`, generators; usage log `build/elevenlabs_usage.jsonl` |
| P06-03 | Key from `ELEVENLABS_API_KEY` / ignored secrets file; no hardcoded keys; not in exports (§2, §19) | VERIFIED (tree) / **FAILED (history)** | audit PASS for tracked files; keys remain in commit `be68b4a` → rotate (D06-001) |
| P06-04 | Estimate before billable batches; approval (§2, §19) | VERIFIED | `phase06_elevenlabs_sfx.py --estimate`: 14 items, ~1,280 credits; awaiting approval |
| P06-05 | Models/endpoints/limits/commercial use verified against the API (§2) | VERIFIED | models list, Music API 402, free tier, licence note |
| P06-06 | Dialogue inventory + `DIALOGUE_AUDIO_MANIFEST.csv` incl. conditional lines (§3) | VERIFIED | 145 rows (130 main, 15 conditional) |
| P06-07 | Consistent character voices (§4) | VERIFIED (consistency) / HUMAN_AUDIO_REVIEW_PENDING (quality) | audit: one voice per character |
| P06-08 | Cinematic dialogue generated, validated, linked, played in Godot (§5) | VERIFIED (headless: take loaded and player started at the trigger, dummy audio driver) | 145/145 RUNTIME_VOICED; audible check on hardware pending |
| P06-09 | SFX library for prison, yard, laundry, tunnels, bus (§6) | IN_PROGRESS | 25 + 42 footsteps integrated; 14 BLOCKED on approval (D06-002) |
| P06-10 | Buses Master/Dialogue/Music/Ambience/SFX/UI/Radio; spatial; attenuation; ducking; fades; transitions (§7) | IMPLEMENTED_UNTESTED (audible) / VERIFIED (logic) | `settings.gd`, `audio_director.gd`; regressions pass |
| P06-11 | Dialogue/subtitle sync, not cut off by shot changes (§8) | VERIFIED (headless) | line holds max(screenplay, take); dialogue director independent of shots |
| P06-12 | Lip sync with available controls (§8) | IMPLEMENTED_UNTESTED | amplitude-driven JawOpen from Dialogue-bus analyser; visemes not available (D06-005) |
| P06-13 | Surface footsteps, directional voices, reverb, ambience transitions, radio processing, music transitions, tension cues (§9) | IMPLEMENTED_UNTESTED (audible) | footsteps counted per surface; music sequence logged; occlusion not done (D06-006) |
| P06-14 | Realistic 3D asset improvements (§10) | IN_PROGRESS | Phase 05 Adrian/Noah done; Phase 06 audit only (`ASSET_INTEGRATION_REPORT.md`) |
| P06-15 | Audio–animation sync: doors, footsteps, bus, ball (§11) | VERIFIED (events) | Door.set_open sounds; bus tween; footsteps by stride; ball cue at throw |
| P06-16 | Mission audio coverage M01–M06 (§12) | VERIFIED (headless) except pending files | `tests/phase06/evidence/mission_audio_coverage.txt` |
| P06-17 | `tools/phase06_audio_audit.py` + runtime dialogue test (§14) | VERIFIED | audit exit 0; three chapter runs |
| P06-18 | Human listening checklist (§15) | VERIFIED (prepared) / HUMAN_AUDIO_REVIEW_PENDING | `AUDIO_QA_REPORT.md` |
| P06-19 | Audio performance (§16) | VERIFIED (memory/load) / BLOCKED (frame time) | `audio_perf.json`; frame time needs the reference PC |
| P06-20 | Full regression (§17) | VERIFIED (headless) | gameplay 14/14, system 24/24, checkpoints 12/12, save validation, guard AI 6/6, parse 73/73, 3 chapter runs |
| P06-21 | Exported Windows executable tested (§17) | BLOCKED | exports from Linux; cannot run a Windows exe here → GPU/Windows session |
| P06-22 | Independent QA loop (§18) | VERIFIED (loop run once) | `QA_REVIEW.md`: APPROVED_WITH_CONDITIONS; S3/S4 findings fixed and retested; S1 key rotation is the owner's |
| P06-23 | Deliverable documents (§20) | VERIFIED | all files under `docs/phase06/` |
