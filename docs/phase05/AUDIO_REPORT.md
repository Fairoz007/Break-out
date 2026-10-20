# Phase 05 audio report: ElevenLabs voice-over, effects, ambience and footsteps

Updated 20 October 2026. Generated at the owner's request with two ElevenLabs free-plan API keys. At the owner's
explicit request the keys are written in the generator scripts (`KEYS` in `tools/phase05_elevenlabs_*.py`) and are
therefore public; a key file passed as the first argument overrides them.

Scope: Chapter 1 is the only chapter with a screenplay (`data/ch01/dialogue.json`, 145 lines); Chapters 2-4 exist as
40-line outlines in `docs/chapters/` with no dialogue, so there is nothing further to record until they are written.

## Status

| Item | Result | Evidence |
|---|---|---|
| Voice-over for all 145 canonical Chapter 1 lines | **Generated and integrated** (blocker P06 "no voice-over" closed for Chapter 1) | `assets/audio/voice/ch01/*.ogg`, `voice_manifest.json` |
| 25 sound effects / beds replacing synthetic placeholders and mismatched stand-ins, 2 new cues | **Generated and integrated** | `assets/audio/phase05_elevenlabs/*.ogg`, `sfx_manifest.json` |
| Footsteps by surface (none were played before) | **Generated and integrated**: concrete 9, metal grating 9, asphalt 15, tile 9 takes | `assets/audio/phase05_elevenlabs/footsteps/` |
| Runtime: every line voiced in a full chapter run | **Verified (headless)**: 156 lines shown, 156 voiced, 140 unique IDs; 0 script errors | `tests/phase05/evidence/linux/chapter_audio.json` |
| Runtime: footsteps by surface | **Verified (headless)**: concrete 1,019, metal 28, tile 6 in one chapter run (the route never crosses asphalt) | `tests/phase05/evidence/linux/chapter_audio_steps.json` |
| Regressions after integration | gameplay 14/14, system 24/24, checkpoints 12/12, save validation, guard AI 6/6, parse 72/72 | `tests/phase03/evidence/regress_*.log` |
| **Listening quality** (casting, performance, mix, pacing) | **HUMAN_TEST_PENDING**. Nothing here was listened to; only lengths, loudness, peaks and silence were measured | `docs/phase05/HUMAN_TEST_CHECKLIST.md` §2 |

Credits used: key 1 4,703 / 10,000 (voice-over); key 2 1,765 / 10,000 (effects). About 13,500 remain.

## Licence: action required before commercial release

Both keys are on the ElevenLabs **free** plan. ElevenLabs' terms for the free plan require attribution and do not
grant a commercial licence for generated audio. The game's credits now carry the attribution
(`data/credits.txt`). **Before any commercial distribution, either regenerate on a paid plan or obtain written
confirmation of the licence; check the current ElevenLabs terms at that time.** All generated files are listed
with their prompts, settings and SHA-256 in the two manifests, so they can be found and replaced.

## Voice-over

Generator: `tools/phase05_elevenlabs_voices.py [keys_file]` (resumable; `--only`, `--redo`, `--reencode` reuses
downloaded takes without new requests). Model `eleven_multilingual_v2`; neighbouring lines of the same mission are
passed as `previous_text` / `next_text` for continuous prosody.

| Speaker | Lines | ElevenLabs voice | Casting basis (docs/characters) |
|---|---|---|---|
| ADRIAN | 52 | Brian (deep, resonant, American) | 34, tired ex-investigator; delivery "low, controlled" |
| NOAH | 55 | Liam (young, confident, American) | 29, warm and quick; "intimate, tense" |
| RUSK | 20 | Adam (dominant, firm) | 41, guard officer; "clipped, guarded" |
| GUARD | 8 | Harry (rough) | shift guards |
| SILAS | 5 | Callum (husky trickster) | 38, favour broker |
| MARA | 4 | Matilda (mature, professional) | 46, clinic doctor |
| RECORDING | 1 | Daniel (British, steady) + 320–3400 Hz band-limit and compression | calibration-log recording |

Delivery note → voice settings: low/controlled stability 0.55, style 0.15; intimate/tense 0.38 / 0.35;
clipped/guarded 0.5 / 0.25; natural/understated 0.6 / 0.1. Post-processing: leading/trailing silence trimmed
(60 ms kept), loudness −18 LUFS (recording −20), true peak −2 dB, mono 44.1 kHz Vorbis q5.

Timing: total 294 s of speech. 140 takes fit inside their screenplay subtitle duration. 5 run longer
(CH01_M05_DLG015 6.2 s vs 4.8; CH01_M01_DLG015 4.0 vs 2.9; CH01_M03_DLG004 3.3 vs 2.2; CH01_M03_DLG006 3.8 vs 3.4;
CH01_M06_DLG019 4.2 vs 3.7). The dialogue director holds those lines for the take's length, so nothing is cut.
Several short lines are delivered fast (for example CH01_M03_DLG017 "He looks frightened." in 0.74 s); a listener
must judge whether they sound rushed.

Runtime (`scripts/chapter/dialogue_director.gd`): a line holds for max(screenplay duration, take length); cinematic
lines play flat on the Voice bus, in-world lines and barks play positionally from the speaker (mouth height,
unit size 8 m); skipping or clearing dialogue stops the take. Each `dialogue_shown` event now records `voice` and
`hold`.

## Effects and ambience

Generator: `tools/phase05_elevenlabs_sfx.py [keys_file]` (text-to-sound-effects, prompt influence 0.55).
One-shots: silence-trimmed, −16 LUFS, peak-capped. Beds: seamless loops (the last 1.5 s crossfades into the first),
−20 LUFS, stereo. Footsteps: one recording per surface sliced at the silences into single steps.

| Cue | Was | Now |
|---|---|---|
| alarm | synthetic siren | facility klaxon loop |
| whistle, breaker_trip, detect_warn | all the same synthetic double beep | guard whistle; breaker clunk and hum dying; suspense stinger |
| relay_click, pa_chime, fluorescent, ventilation | synthetic tones/loops | relay contactor; PA two-tone chime; tube buzz loop; duct drone loop |
| cuffs | key jingle | handcuff ratchet |
| ball_bounce | light metal impact | basketball on concrete |
| handset, lever, panel | generic clicks | wall-phone handset lift; heavy lever; panel prised open |
| pipe_knock / pipe_reply | metal impacts | knuckle on pipe / muffled knock through wall |
| grille, cell_slam, door_open, door_close | spring, sheet slam, wooden RPG doors | sliding barred gate; cell door slam; steel security door open/close |
| count_bell | small bell ding | institutional headcount bell |
| bus_diesel, crowd, radio | generic machine loop, crowd shouting, radio noise | idling bus diesel; yard murmur; security radio chatter |
| bus_doors (new) | steel-door sound on the bus | pneumatic folding door hiss, at the bus |
| cellblock_night (new) | — | M04 cell block at night bed (−20 dB) |
| footsteps (new) | not played at all | per-surface takes, random choice and ±6 % pitch |

Footsteps (`CharacterVisual._footsteps`, `AudioDirector.footstep`): one step per stride (walk 0.72 m, run 0.95 m,
crouch 0.62 m and 8 dB quieter, sprint +3 dB), a heavier step on landing; surface from a downward ray to the floor
body's material (EnvBuilder tags each material with its source name). Guards' steps are 4 dB louder than the
players' so a patrol can be heard approaching.

## Not done / still required

* Human listening on headphones and speakers (checklist §2), including casting fit and mix balance.
* Guard alert/search barks beyond the 145 canonical lines were **not** added; that would add dialogue to the
  screenplay and needs the writer's approval.
* Music was not generated.
