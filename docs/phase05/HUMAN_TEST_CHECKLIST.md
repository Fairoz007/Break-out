# Phase 05 human test checklist (two controllers, audio, animation, cinematics, usability, visuals)

**Status of every section below: HUMAN_TEST_PENDING.** No person has performed these tests. The automated battery
(virtual-input autopilot, headless and software-rendered runs) cannot judge feel, readability or sound, and it does
not exercise physical controllers. Nothing in this file may be reported as passed until a named tester fills in the
result columns.

## Setup

| Item | Requirement |
|---|---|
| Build | `build/windows/BreakoutNoWayBack.exe` (re-export with `"$G" --headless --path . --export-release "Windows Desktop" build/windows/BreakoutNoWayBack.exe`; SHA-256 of the Phase 05 export is in `tests/phase05/evidence/linux/export_windows.sha256`) |
| Machine | Reference: RTX 2060, Ryzen 7 5700X, Windows 11, 1920×1080 display. Record anything different. |
| Controllers | Two XInput gamepads (e.g. two Xbox controllers), both connected **before** launch; one keyboard + mouse |
| Audio | Session A: closed-back headphones. Session B: stereo desktop speakers at normal listening level |
| Save | Delete `%APPDATA%\Godot\app_userdata\BREAKOUT NO WAY BACK\` (or use a fresh Windows user) so New Game starts clean |
| Recording | Optional but preferred: OBS capture of the full session; note timestamps in the "Notes" column |

Controls (from `scripts/core/device_router.gd`): gamepad — left stick move, right stick camera, A interact, X jump,
B crouch, LB walk (slow), L3 or right trigger sprint, Y recover/unstick, Back skip cinematic, Start pause.
Keyboard (P1 default) — WASD, mouse look, E interact, Space jump, C crouch, Alt walk, Shift sprint, R recover,
X skip, Esc pause. Second keyboard layout (P2 on one keyboard) — IJKL, O interact, M jump, N crouch, U walk, H sprint,
arrows look, P pause.

Result codes: PASS / FAIL / PARTIAL. Every FAIL or PARTIAL needs a note and, ideally, a screenshot or video timestamp.

## 1. Two-controller playthrough (COOP-004/005)

| # | Step | Expected | Result | Notes |
|---|---|---|---|---|
| 1.1 | Launch the exe with both pads connected. Main menu → Settings → Controls and devices | P1 Adrian shows controller 1, P2 Noah shows controller 2 | | |
| 1.2 | Press "Change device for P1 Adrian", then press a button on the **second** pad | P1 is reassigned to that pad; P2 is not left on the same device | | |
| 1.3 | Press "Auto-detect (controllers first)" | Both pads assigned, one each, controllers before keyboard | | |
| 1.4 | Back → New Game | Split-screen, Adrian left / Noah right (vertical split default); both HUDs show the first objective | | |
| 1.5 | Move each stick in turn | Only the matching character moves; each right stick turns only its own camera | | |
| 1.6 | Pause → Quit to main menu → Settings → tick "Horizontal split-screen (top / bottom)" → Continue | Layout is top/bottom (the option applies at the next New Game or Continue); inputs still map to the correct half | | |
| 1.7 | Play M01 New Blood to the end | Objectives advance; interaction prompts appear only on the correct player's screen | | |
| 1.8 | M02 Trouble in the Yard: mediation hold | Holding A on P1 keeps Silas's attention; Silas and the group are visible on screen during the hold | | |
| 1.9 | M03 The Workshop: cooperative lever / selector | Early release or wrong selector produces the authored failure bark and lets you retry | | |
| 1.10 | M04 Lights Out: deliberately get spotted once | Detection → fade → reload at CP04_A, both players restored, no stuck input | | |
| 1.11 | M04 shim insert (SH03) | The shim is visible in Adrian's fingers at the panel seam | | |
| 1.12 | M05 Behind the Walls: handsets, brake, gate | Each player can only use their own handset; Adrian's hand is at the gate latch during the hold | | |
| 1.13 | M06 The Betrayal: both pull handles | Cinematic plays; on "On your knees. Both of you." both characters kneel with hands raised | | |
| 1.14 | M06: during the cinematic, Start → "Restart from last checkpoint" | Restarts at CP06_A, cinematic replays from SH01, no frozen camera or dead input | | |
| 1.15 | Pause on P2's pad mid-mission; Resume; Quit to main menu; Continue | Pause owns both players; Continue returns to the last checkpoint | | |
| 1.16 | Unplug P2's pad for 5 s mid-mission, reconnect | Note exactly what happens (no pass/fail rule is specified; record behaviour) | | |
| 1.17 | Finish the chapter | Chapter end reached; credits roll; no crash. Record total play time | | |

## 2. Audio listening review (AUD-*)

Do the whole section twice: headphones (A) and speakers (B).

| # | Step | Expected | A | B | Notes |
|---|---|---|---|---|---|
| 2.1 | M01 intake dialogue | Voices intelligible over ambience at default volumes; no clipping | | | |
| 2.2 | Walk Adrian across concrete, metal grate, yard dirt | Footsteps change by surface and come from the character's side of the stereo field | | | |
| 2.3 | Stand still, pan the camera around a running machine (M03 laundry) | Machine sound pans with the camera; volume falls off with distance | | | |
| 2.4 | Doors and gates (cell door, yard gate, security grille) | Each has an audible open/close sound synced to motion | | | |
| 2.5 | M04 guard radio / barks | Guard lines are positioned at the guard; radio has a band-limited texture | | | |
| 2.6 | M06 alarm | Alarm is loud but not painful; dialogue still readable over it | | | |
| 2.7 | Settings: Voice, Music, Effects volume sliders to 0 then back | Each slider controls only its own category | | | |
| 2.8 | Any pops, stutters, missing sounds, or sounds that loop forever | None | | | |

## 3. Character animation review

| # | Step | Expected | Result | Notes |
|---|---|---|---|---|
| 3.1 | Walk, run, sprint, stop, turn on the spot with both characters | No foot sliding beyond a few cm; turns do not snap; stops settle naturally | | |
| 3.2 | Crouch-walk, jump, land, stairs (M04 landing) | No popping between states; feet do not sink into steps | | |
| 3.3 | Interactions: doors, levers, handles (M06), gate latch (M05) | Hands land on the object rather than pushing air; the object reacts when the hand arrives | | |
| 3.4 | Idle for 30 s | Natural idle; no T-pose, no frozen character | | |
| 3.5 | Clothing in motion: Adrian's overshirt hem and grey undershirt, Noah's shirt and bare forearms | No skin or trousers poking through clothing; no stretched texture at shoulders or wrists | | |

## 4. Cinematic review

| # | Shot | Expected | Result | Notes |
|---|---|---|---|---|
| 4.1 | M01 bus arrival | Bus reads as a prison transport; doors open in sync | | |
| 4.2 | M02 mediation | Adrian faces Silas; Silas framed while he speaks | | |
| 4.3 | M04 SH03 shim insert | Shim legible; hand and seam lit | | |
| 4.4 | M05 SH02 handset | Phone visibly in Adrian's hand at his ear | | |
| 4.5 | M06 SH04 kneel | Both kneel on the order line, hold through "We can still run" / "We stay alive" | | |
| 4.6 | Noah's right-wrist burn | Note every shot where you can see it; say whether it reads as a burn | | |
| 4.7 | Cut back to gameplay after each cinematic | Camera returns behind each player without a jump in control | | |

## 5. Gameplay usability

| # | Step | Expected | Result | Notes |
|---|---|---|---|---|
| 5.1 | First-time player, no briefing, plays M01–M02 | Can tell what to do from objectives and prompts alone; record any confusion | | |
| 5.2 | Subtitle size setting at each value | Readable at 1080p from a sofa distance (~2.5 m) | | |
| 5.3 | Reduced flashing on, M06 alarm | Alarm light is steady | | |
| 5.4 | Credits screen | Final text (no draft markers) | | |

## 6. Visual quality

| # | Location | Look for | Result | Notes |
|---|---|---|---|---|
| 6.1 | Adrian and Noah close up (pause during a cinematic) | Hair reads as short hair, not a cap; skin and eyes natural; clothing matches the character docs | | |
| 6.2 | Prison bus | Exterior panel detail, wheel arches, driver area legibility | | |
| 6.3 | Basketball court | Surface, markings, hoops, nets, fence | | |
| 6.4 | Cell block, intake, laundry, maintenance, security areas | Scale, materials, lighting; anything that reads as a placeholder | | |
| 6.5 | Frame pacing on the reference machine | Note any visible hitch, with mission and moment | | |

## Sign-off

| Tester | Date | Machine | Sections completed | Overall verdict |
|---|---|---|---|---|
| | | | | HUMAN_TEST_PENDING |
