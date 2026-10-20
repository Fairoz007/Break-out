# Handoff for local continuation (Windows GPU) — 20 Oct 2026, end of cloud session

Branch `claude/busy-gauss-cj4r2c` (pushed). Cloud container had no GPU/Windows/controllers/speakers: everything below
was verified headless or with the Mesa software renderer. Continue with `docs/phase06/CONTINUE_PROMPT.md`.

## Done in this last cloud stretch (Phase 06 completion prompt)

| Item | Result | Evidence |
|---|---|---|
| Security audit | Tree clean (ElevenLabs, OpenAI-style, GitHub, AWS, Google, Slack, private-key patterns: 0). History: only the two ElevenLabs keys (`be68b4a` adds, `4884b8d` removes). One generic match is Adobe's public analytics client key inside a saved Mixamo FAQ page (licence evidence, not ours). Keys read from `ELEVENLABS_API_KEY` / git-ignored `.secrets/`, excluded from exports; no key string in the built exe. **Keys must be rotated by the owner; no ElevenLabs calls were made.** | `tools/elevenlabs_client.py`, `.gitignore`, `export_presets.cfg` |
| Missing sounds: reuse first | 6 of 14 now use licensed CC0 library audio: `tools`, `switch`, `electric_hum`, `dryer` (provisional), `drips` (provisional water loop), `music_tension` (low drone — tension ambience, **not** a composed score). Remaining 8 need generation after key rotation + approval: `cart`, `pipe_groan`, `bus_arrive`, `bus_engine_off`, `cellblock_day`, `sting_capture`, `music_chase`, `music_betrayal` (~710 credits, `python -I tools/phase06_elevenlabs_sfx.py --estimate`). Game skips missing ones quietly. | `scripts/core/audio_director.gd` (comments "Phase 06 reuse") |
| Guard insignia (D06-010) | Sleeve patches now "BLACKRIDGE ★ CORRECTIONS", name bar "CORRECTIONS" (texture copy, original untouched) for GUARD and RUSK | `tools/phase06_guard_insignia.py`, `assets/characters/phase06/guard_body_corrections.png`, `tests/phase06/evidence/npc_lineup_after.jpg` |
| Inmate variants (D06-011) | 3 issue shirts (orange / rust / grey work-detail) over orange trousers, stable per NPC name | `tools/phase06_inmate_variants.py`, `CharacterVisual.INMATE_SHIRTS`, same lineup image |
| Bus exterior (D05-018) | Flat white paint replaced by world-triplanar painted-steel panels (seams, rivets, sill grime, streaks) on `P3_BusPaint` only | `tools/phase06_bus_panels.py`, `EnvIntake._panel_bus`, `tests/phase06/evidence/bus_after.jpg` |
| UI dropdown test (D06-009) | Fixed: OptionButton opens on press, so the test presses, checks the popup, clicks the item row, always closes the popup. `graphics_dropdown` and the toggles PASS (menu section). In-game section (pause/restart/quit/continue/Quit) not finished under software rendering — **run on GPU** | `tests/phase04/ui_walkthrough.gd`, `tests/phase06/evidence/ui_walkthrough.log` |
| Regressions | gameplay 14/14, system 24/24, checkpoints 12/12, save validation, guard AI 6/6, parse 73/73; chapter none/idle complete, 0 script errors, all shown lines voiced; audio audit exit 0 | `tests/phase03/evidence/regress_*`, `tests/phase06/evidence/chapter_*.json`, `audio_audit.txt` |

## NEW defect found — investigate first on Windows

**D06-015 (S2, intermittent crash):** one headless `--chaos=mistakes` chapter run aborted with signal 11 during a
mission transition (`load_mission` → nav bake), preceded by
`ERROR: /root: The caller thread can't call the function propagate_notification()` — i.e. something touched the
scene tree from a non-main thread. 4 immediate re-runs passed (0 crashes). Prime suspect: the Phase 05 threaded
hand-prop preload (`CharacterVisual.warm_props` → `ResourceLoader.load_threaded_request` of GLB PackedScenes,
started in `chapter_root.load_mission` right before `build()`/`bake()`). Log: `tests/phase06/evidence/chapter_mistakes.log`
(the matching JSON is from an earlier run). Suggested fix to try: start `warm_props` after `m.b.bake()` (or defer it a
frame), or set `use_sub_threads=false` / load with `load_threaded_request(path, "", false)`; then run 10+ mistakes
runs on Windows and the exe.

## Still open (unchanged)

Windows exe never run; GPU frame times (M06 841 ms check); GPU re-captures M02/M04/M05; full UI walkthrough incl.
Quit; bus driver area (D05-019); intake benches/tray, yard dirt; Adrian shoulder texture mark; human listening and
two-controller tests (pending); ElevenLabs free-plan commercial licence; Phase 04 release approval.
