# Phase 06 audio production report

Updated 20 October 2026.

## Pipeline (offline; the game never calls ElevenLabs)

| Piece | File | What it does |
|---|---|---|
| Client | `tools/elevenlabs_client.py` | Keys from `ELEVENLABS_API_KEY` (comma-separated allowed) or git-ignored `.secrets/elevenlabs.env`; keys never printed (logs show "key #n"). Retries with exponential backoff on 429/5xx/network, rotates keys on 401/402/403, usage snapshots before/after each batch into `build/elevenlabs_usage.jsonl` and the manifest, output validation (ffprobe duration + full ffmpeg decode), stable cache keys of (text/prompt, voice, model, settings). |
| Voice generator | `tools/phase05_elevenlabs_voices.py` | 145 lines, cast table, delivery→settings map, neighbouring lines as `previous_text`/`next_text`, silence trim, −18 LUFS; resumable, `--reencode` reuses downloaded takes for free |
| Effects (Phase 05) | `tools/phase05_elevenlabs_sfx.py` | one-shots, crossfade loops, sliced footsteps, peak cap |
| Effects (Phase 06) | `tools/phase06_elevenlabs_sfx.py` | 14 mission sounds + tension beds; `--estimate` prints the credit estimate without calling the API |
| Manifests | `tools/phase06_audio_manifests.py` | `docs/phase06/DIALOGUE_AUDIO_MANIFEST.csv`, `SFX_MANIFEST.csv` |
| Audit | `tools/phase06_audio_audit.py` | automated checks (see AUDIO_QA_REPORT.md) |

## Voice design (consistent IDs for the whole chapter)

| Character | Voice (ElevenLabs premade) | Direction applied |
|---|---|---|
| Adrian Cross | Brian `nPczCjzI2devNBz1zQrb` | adult, controlled, serious: stability 0.55, style 0.15 |
| Noah Reyes | Liam `TX3LPaxmHKxFdv7VOQHJ` | younger, expressive: stability 0.38, style 0.35 |
| Tomas Rusk (officer) | Adam `pNInz6obpgDQGcFmaJgB` | firm, clipped: 0.5 / 0.25 |
| Guards | Harry `SOYHLrjzK2X1ezoPC6cr` | commanding, rough: 0.5 / 0.25 |
| Silas Bell | Callum `N2lVS1w4EtoT3dr4eOWO` | mature, husky |
| Dr Mara Sen | Matilda `XrExE9yKIg1WjnnlVkGX` | natural, understated |
| Calibration recording | Daniel `onwK4e9ZLuTAKqWW03F9` | band-limited 320–3400 Hz + compression |

All are ElevenLabs premade library voices; no real person's voice was cloned.

## Dialogue

145 / 145 lines generated, 294.7 s total, all decoding, all runtime-verified as playing at their trigger (headless
union of normal, idle and mistakes chapter runs: `DIALOGUE_AUDIO_MANIFEST.csv` column `qa_status=RUNTIME_VOICED`).
Original screenplay text is unchanged (audit check: recorded text == subtitle text == screenplay).

## Godot audio architecture (Phase 06)

| Bus | Sends to | Contents | Effects |
|---|---|---|---|
| Music | Master | tension beds (crossfaded) | — |
| Dialogue | Master | voice takes | spectrum analyser (drives jaws); kept dry |
| Radio | Dialogue | radio chatter bed / cue | high-pass 320 Hz, low-pass 3.4 kHz, light overdrive |
| SFX | Master | one-shots, footsteps, door motion | reverb per scene (`AudioDirector.SPACES`; yard dry) |
| Ambience | SFX | scene beds (fade in 1.5 s) | ducks −8 dB under dialogue |
| UI | SFX | menu / checkpoint cues | — |

Player sliders keep their meaning (Voice → Dialogue incl. radio; Effects → SFX incl. ambience and UI; Music).
Ducking: ambience −8 dB and music −5 dB while a take plays (0.25 s in, 0.8 s out). Music: `play_music()` crossfade;
M04 tension bed by scene, chase bed on a guard alert (back to tension on the checkpoint reload), betrayal bed when
the M06 alarm starts, fade out at chapter end. Spatial: in-world lines and barks from the speaker's mouth height,
cues at their source (unit size 6 m), footsteps 3 m, guards' steps 4 dB louder. Occasional positional one-shots per
scene (`SCENE_SPOTS`: M03 carts/tools, M05 pipe groans). Occlusion is **not** implemented (documented limitation).

## Audio–animation sync

* Doors: `Door.set_open()` plays the open/close sound of its type at the door the moment it moves (cell doors latch
  and slam, yard gates rattle/latch, grilles slide, steel doors open/close); duplicate manual cues removed.
* Footsteps: one per stride from the character's real ground speed and the surface under it (a timer, not foot
  bone contact — the retargeted clips carry no contact events); landing step on touchdown.
* Bus: arrival sound starts with the drive-in tween; pneumatic doors with the door-fold tween; engine-off 1.5 s after.
* Lip sync: jaw (`*_JawOpen`) follows the measured speech level of the Dialogue bus; amplitude-driven, **not
  phoneme visemes**. Headless (no audio device) falls back to the old timed motion.

## Phase 06 generation batch: PENDING APPROVAL

14 items, 128 s requested, estimate **~1,280 credits** (key 2 has ~8,235 left): music_tension, music_chase,
music_betrayal (sound-effect drones; the Music API needs a paid plan), sting_capture, dryer, cart, tools, switch,
pipe_groan, drips, electric_hum, bus_arrive, bus_engine_off, cellblock_day. The run was stopped by the session's
permission system as a billable action; all hooks are already in the game and skip quietly (logging
`audio_missing`) until the files exist. To run after approval:
`python3 -I tools/phase06_elevenlabs_sfx.py && "$G" --headless --path . --import && python3 -I tools/phase06_audio_manifests.py && python3 -I tools/phase06_audio_audit.py`

## Credits used so far

| Key | Used / limit | Spent on |
|---|---|---|
| key 1 | 4,703 / 10,000 | 145 voice lines |
| key 2 | 1,765 / 10,000 | Phase 05 effects |
| Phase 06 | 0 | music probe refused (no charge) |

## Licence

Free-plan output: attribution required (in `data/credits.txt`), no commercial licence. Regenerate on a paid plan
or obtain written permission before any commercial release.
