# Phase 05 performance report (D05-014, D05-015)

Updated 20 October 2026. **Status: partially resolved. Real-time measurement on the reference machine is still
required** (RTX 2060 / Ryzen 7 5700X / Windows 11); this session ran in a Linux cloud container without a GPU.

## What was measured, and where

| Source | Machine | Renderer | What it can show |
|---|---|---|---|
| Phase 04 `tests/phase04/evidence/exe_perf_m0N.json` | Reference PC, exported Windows exe, 1920×1080 split-screen, speed 1 | D3D12 Forward+ | Real-time frame times (baseline below) |
| Phase 05 `tests/phase05/evidence/linux/chapter_*.json`, `exported_chapter_*.json` | Linux container, 4 vCPU, no GPU | `--headless` | **Main-thread (CPU) stalls only**: loading, instantiation, script work. No GPU, no shader compilation, no texture upload |
| Phase 05 rendered captures (`m0N_shots`) | Same container | Forward+ on llvmpipe (software Vulkan) | Image correctness only; frame times are meaningless |

Spike tracer (added this phase, `tests/phase02/autopilot.gd`): any wall-clock frame over 50 ms is recorded with
the per-frame deltas of the engine monitors (pipeline compilations by type, texture/buffer/video memory, object,
node and resource counts, draw calls, navigation polygons), the game events logged in that frame, whether a
cinematic was active, and whether a screenshot readback happened in it. Reports list them under `frame_spikes`;
`gpu_frame_ms` holds per-viewport GPU time when a GPU renderer is active.

## Baseline (Phase 04, reference PC, exported exe)

| Mission | Mean fps | p50 ms | p99 ms | Max ms |
|---|---|---|---|---|
| M01 | 88 | 11.75 | 14.23 | 183.2 |
| M02 | 123 | 7.77 | 10.64 | 105.8 |
| M03 | 109 | 9.20 | 10.69 | 123.2 |
| M04 | 136 | 7.59 | 9.01 | 127.0 |
| M05 | 136 | 7.60 | 8.99 | 133.9 |
| M06 | 139 | 6.85 | 9.93 | **841.0** |

Phase 04 recorded only the maximum, not when it happened or what caused it.

## Measured causes (headless, Phase 05)

Full Chapter 1 autopilot, `--speed=4 --fixed-fps 60`, editor binary and exported Linux binary agree:

| Spike | ms (before) | Frame contents | Cause |
|---|---|---|---|
| M06, CH01_M06_CS01_SH05 first frame (mid-cinematic) | **1,656** | +14 nodes, +9 resources, events `shot_activated:SH05`, `clip:Interact` | `attach_to_hand()` called `load()` on `simple_handcuffs.glb` (25 MB, with a 14 MB PNG texture) on the main thread, twice, on the shot's first frame |
| M04, CH01_M04_CS01_SH03 first frame (mid-cinematic) | 74 | +9 nodes, `clip:Kneel_Work` | same path: `spring_shim.glb` loaded synchronously |
| M02–M06 mission load | 1,106–5,043 | thousands of nodes/objects created and freed, nav polygons rebuilt, `mission_loaded` | scene construction + navigation bake. Happens behind the fade to black between missions |
| M04 checkpoint reload after detection | 192 | `reload_checkpoint`, `mission_loaded` | same, behind the fade |

The M06 841 ms freeze on the reference PC is consistent with the SH05 handcuff load (same mission, one-off, much
larger than any other in-mission frame). That attribution is **plausible, not proven**: the Phase 04 report has no
timestamp for it. It is confirmed only when the reference PC run below shows the spike gone.

Shader compilation was **not** assumed: the two in-mission stalls occur with no renderer at all, so they are not
pipeline compiles. Whether GPU-side compiles also cause the 105–183 ms maxima in M01–M05 cannot be measured here.

## Fixes implemented

1. **Threaded hand-prop preloading** (`scripts/player/character_visual.gd` `warm_props()` / `prop_scene()`,
   `scripts/chapter/mission_director.gd` `hand_props()`, `scripts/chapter/chapter_root.gd`): each mission declares
   the props it will attach to hands (M04 shim; M05 shim + handset; M06 handcuffs). They start loading on a worker
   thread when the mission loads; `attach_to_hand()` takes the cached `PackedScene`.
2. **First frames behind black** (`chapter_root.gd` `_fade_in()`): after a mission or checkpoint load the screen
   stays black for three drawn frames before the fade starts, so the first draw of the new scene (pipeline
   compiles, texture uploads) cannot make the fade-in jump.

## After (headless, same runs)

| Spike | Before | After |
|---|---|---|
| M06 SH05 mid-cinematic | 1,656 ms | **none over 50 ms** |
| M04 SH03 mid-cinematic | 74 ms | **none over 50 ms** |
| Mission loads (behind fade) | 1,106–5,043 ms | 1,088–3,635 ms (unchanged in kind; varies run to run) |

Exported Linux build, full chapter: `exported_chapter_none.json` has only mission-load spikes;
`exported_chapter_mistakes.json` adds the 192 ms checkpoint reload (behind the fade). No in-mission frame over 50 ms.

## Still required (cannot be done in this container)

| Test | Command (reference PC, Git Bash, repo root) | Pass criterion |
|---|---|---|
| Real-time per-mission frame times on the new exe | `for m in 1 2 3 4 5 6; do build/windows/BreakoutNoWayBack.exe --resolution 1920x1080 --log-file "$(pwd -W)/tests/phase05/evidence/exe_perf_m0$m.log" -- --autopilot --mission=$m --until=$m --timeout=900 --save-slot=p05_exe_perf_m0$m --report="$(pwd -W)/tests/phase05/evidence/exe_perf_m0$m.json"; done` | p99 ≤ 16.7 ms in every mission; every `frame_spikes` entry outside a load/fade explained |
| M06 841 ms freeze gone | inspect `frame_spikes` in `exe_perf_m06.json` | no in-mission spike at SH05 |
| GPU-side spikes in M01–M05 | same reports: `pipe_*` deltas and `gpu_frame_ms` | any remaining in-mission spike attributed to a monitor delta |

If pipeline compilation shows up there, the next step is a warm-up pass that draws each mission's materials once
behind the post-load black frames added above.
