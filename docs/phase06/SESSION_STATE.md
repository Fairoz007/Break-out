# Phase 06 session state

Updated 20 October 2026 (Linux cloud session, no GPU). **Phase 06: IN PROGRESS. Not complete**: 14 cues await
approval for ~1,280 credits, the Windows exe has not been run, no human listening review, and asset work is audit
only. Phase 04 remains unapproved.

| Item | Value |
|---|---|
| Branch | `claude/busy-gauss-cj4r2c` (pushed after this session; see git log) |
| Tools | Godot 4.7.2 Linux `/opt/tools/Godot_v4.7.2-stable_linux.x86_64`, Blender 5.1.1 Linux, Mesa llvmpipe (software Vulkan), ffmpeg |
| Last builds | `build/windows/BreakoutNoWayBack.exe` (export only, not run; SHA-256 in `tests/phase06/evidence/export_windows.sha256`), `build/linux/BreakoutNoWayBack.x86_64` (run: full chapter, all shown lines voiced) — both git-ignored |
| ElevenLabs usage | key 1 4,703/10,000, key 2 1,765/10,000; Phase 06 spent 0 (Music API refused, no charge) |

## Done this session (evidence in `tests/phase06/evidence/`)

* Secrets: keys moved out of the scripts to `ELEVENLABS_API_KEY` / git-ignored `.secrets/elevenlabs.env`;
  `.secrets/*` excluded from exports; exe contains no key string. Keys still in git history → rotate (D06-001).
* Pipeline: `tools/elevenlabs_client.py` (retry, rotation, usage log, validation, cache keys);
  `tools/phase06_elevenlabs_sfx.py` (`--estimate`); manifests `tools/phase06_audio_manifests.py`;
  audit `tools/phase06_audio_audit.py` (exit 0).
* Dialogue: 145/145 lines (130 main + 15 conditional) voiced and runtime-verified headless.
* Audio architecture: buses Music, Dialogue, Radio, SFX, Ambience, UI with effects; ducking; scene reverb; bed
  fades; music crossfades (tension/chase/betrayal hooks); occasional scene one-shots; loop-leak bug fixed;
  missing cue files skip quietly.
* Sync: door motion sounds by door type; bus arrival/engine-off with the drive-in; detection stinger; PA chime;
  menu confirm/back; amplitude-driven jaw from the Dialogue-bus analyser.
* Perf: 212 audio files load in < 1.3 ms each; all loaded = +8.4 MB.
* Regression: gameplay 14/14, system 24/24, checkpoints 12/12, save validation, guard AI 6/6, parse 73/73;
  chapter runs none/idle/mistakes complete with 0 script errors; exported Linux build completes the chapter.
* Docs: BASELINE_AUDIT, REQUIREMENTS_MATRIX, DEFECT_QUEUE, AUDIO_PRODUCTION_REPORT, AUDIO_QA_REPORT,
  ASSET_INTEGRATION_REPORT, DIALOGUE_AUDIO_MANIFEST.csv, SFX_MANIFEST.csv, CONTINUE_PROMPT.

## Independent QA

`docs/phase06/QA_REVIEW.md`: APPROVED_WITH_CONDITIONS. Code findings 2–11 fixed and retested (regressions, parse
73/73, three chapter runs: 0 script errors, 145/145 lines, asphalt/concrete/metal/tile footsteps). Condition left for
the owner: **rotate both ElevenLabs keys** (S1, public repo history).

## Next executable action

On owner approval: `python3 -I tools/phase06_elevenlabs_sfx.py`, import, manifests, audit. Otherwise continue on the
Windows reference PC with `docs/phase06/CONTINUE_PROMPT.md`.
