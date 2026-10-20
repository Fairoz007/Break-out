# Phase 06 baseline audit

Written 20 October 2026 at the start of Phase 06, in the Linux cloud session (no GPU; Godot 4.7.2 Linux, Blender
5.1.1 Linux, Mesa llvmpipe for software rendering). Branch `claude/busy-gauss-cj4r2c`, HEAD `be68b4a`, clean tree.

## Inherited state

| Area | State at start of Phase 06 | Source |
|---|---|---|
| Phase 04 | **Not approved** by independent QA (second review 540 VERIFIED / 67 FAILED / 49 BLOCKED); `phase04` branch never pushed | `docs/phase04/QA_REVIEW.md` |
| Phase 05 | In progress; garments, hair, kneel timing, staging fixes, M06 stall fix, voice-over and SFX done; real-GPU performance, captures of M02/M04/M05, UI dropdown test and independent QA outstanding | `docs/phase05/*` |
| Regressions | gameplay 14/14, system 24/24, checkpoints 12/12, save validation, guard AI 6/6, parse 72/72 | `tests/phase03/evidence/regress_*` |
| Windows export | Exports from Linux; **cannot be run here**; last export predates the audio | `tests/phase05/evidence/linux/export_windows.*` |

## Screenplay and dialogue (verified counts)

`data/ch01/dialogue.json`: **145 lines** — 130 main-sequence, **15 conditional** (earlier reports said 12):
intake idle, badge reminder, distraction idle, missed distraction reset, two optional skeptical-stance lines,
lever released early, idle bark, detected fail, retry CP04_A, patrol warning, wrong selector, puzzle retry,
handle idle, pipe idle. Speakers: ADRIAN 52, NOAH 55, RUSK 20, GUARD 8, SILAS 5, MARA 4, RECORDING 1.
No separate "prisoner" or radio-dispatcher lines exist in the screenplay; Chapters 2–7 are outlines without dialogue.

## Audio that already existed (reused, not regenerated)

| Content | Files | Status at baseline |
|---|---|---|
| Voice-over, all 145 lines | `assets/audio/voice/ch01/*.ogg` + `voice_manifest.json` (Phase 05, ElevenLabs `eleven_multilingual_v2`) | generated, integrated, runtime-verified headless |
| 25 effects/beds + 42 footsteps | `assets/audio/phase05_elevenlabs/` + `sfx_manifest.json` | generated, integrated |
| Licensed library audio | `assets/audio/phase15*`, Kenney impact/footstep sets (washer, belt, pump, water, wind, ocean, keys, latch, fence, paper, UI) | integrated; licences in `asset_library/licenses/` |

Gaps found: no bus layout beyond Music/Voice/SFX; no ducking; no reverb; no music; doors silent when they move;
`detect_warn`, `pa_chime`, `door_close`, `ui_confirm` defined but never triggered; no bus engine/brake or
engine-off; no dryer/cart/tools in the laundry; no drips/electrical hum in the tunnels; jaw motion was a sine wave
during subtitles; a bed's loop flag leaked into one-shots of the same cue (radio).

## ElevenLabs account (checked through the API, never assumed)

| Item | Finding |
|---|---|
| Keys | 2, both **free** tier, 10,000 credits each |
| Used before Phase 06 | key 1 4,703 (voices), key 2 1,765 (effects) |
| TTS models | eleven_v4, v4_turbo, v3, v3_conversational, multilingual_v2, flash v2/v2.5, turbo v2/v2.5 |
| Sound effects | available (`/v1/sound-generation`) |
| Music API | **refused**: HTTP 402 `paid_plan_required` (probe cost 0 credits) |
| Commercial use | free plan: attribution required, no commercial licence |
| Key exposure | both keys were committed in `be68b4a` at the owner's earlier request; removed from the tree in Phase 06 and moved to `.secrets/` (git-ignored, export-excluded). They remain in git history: **rotate them**. |

## 3D assets (summary; details in ASSET_INTEGRATION_REPORT.md)

Adrian (overshirt + undershirt, short hair) and Noah (prison shirt, bare forearms, burn, cropped hair) were rebuilt
in Phase 05. Guards, Silas, inmates and Mara render as realistic Rocketbox characters
(`tests/phase06/evidence/npc_*.jpg`). Open: guard insignia read "SECURITY OFFICER"; bus exterior panels (D05-018);
intake benches/tray, yard dirt (D05-020/021).
