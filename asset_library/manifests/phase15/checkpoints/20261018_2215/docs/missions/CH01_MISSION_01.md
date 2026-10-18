# Mission 01 — New Blood

ID CH01_M01 · Scene CH01_M01_SC01 · Cinematic CH01_M01_CS01. P1 Adrian, P2 Noah. Planning specification; no implemented gameplay or tested timing.

Time: 18 October 2028, 07:10. One continuous day; no unexplained time jump within scene.

Duration: 330s total; 65s cinematic allocation, 265s playable estimate.

## Exact playable sequence and ownership

Escort Noah to search mark. P1 watches through bars and selects the stamped badge for a focus interaction while P2 submits possessions. Rusk moves Noah to east cell 14; Adrian is assigned adjacent cell 13. P1 and P2 each inspect their sink and barred door to establish controls.

P1 Adrian observes badge from holding bay; P2 Noah submits photo and reads property receipt42. Photo is tagged then returned as approved paper; only other property remains locker42. Cells are13/14. Both acknowledge observations before escort proceeds. No distraction or photo retrieval occurs.

Cooperative gates: Parallel observation: neither player can see both the property receipt and badge. Both acknowledge observations before cell assignment proceeds; no dexterity gate.

## Objective and cinematic triggers

OBJ001 submit property; OBJ002 P1 inspect badge; OBJ003 both enter assigned cell marks. Trigger CS01 on both ready, never on only P2 crossing. IDs are CH01_M01_OBJ001 onward in listed order. Checkpoint CP01_A at scene entry, CP01_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

Objectives use the CH01_M01_OBJ prefix and numeric order above. Each gate checks both players alive/present and no cinematic lock. Plot lines serialize; progression waits for required dialogue, not arbitrary arrival timers. Input ownership is fixed P1/P2; no partner can operate both physically separated stations.

## Dialogue — complete authored scene lines

Source of truth: [full script](../screenplay/CH01_FULL_SCRIPT.md#ch01_m01_sc01), [dialogue register](../screenplay/CH01_DIALOGUE.md). Lines below mirror the authored version; future edits must update both documents and rerun consistency review. Context labels distinguish optional/retry from forward progress.

[CH01_M01_DLG001] RUSK (clipped, guarded; 3.3s; main sequence): "Hands where I can see them. Name."

[CH01_M01_DLG002] NOAH (intimate, tense; 3.3s; main sequence): "Noah Reyes. My property stays with me."

[CH01_M01_DLG003] RUSK (clipped, guarded; 4.1s; main sequence): "Your name does. The rest goes in the tray."

[CH01_M01_DLG004] NOAH (intimate, tense; 4.1s; main sequence): "That photograph is all I have of my sister."

[CH01_M01_DLG005] RUSK (clipped, guarded; 2.9s; main sequence): "Then remember what she looks like."

[CH01_M01_DLG006] ADRIAN (low, controlled; 2.1s; main sequence): "Ask for a receipt."

[CH01_M01_DLG007] NOAH (intimate, tense; 2.5s; main sequence): "You running the front desk?"

[CH01_M01_DLG008] ADRIAN (low, controlled; 2.9s; main sequence): "No. I know what disappears here."

[CH01_M01_DLG009] RUSK (clipped, guarded; 2.0s; main sequence): "Cross. Sit down."

[CH01_M01_DLG010] GUARD (clipped, guarded; 4.5s; main sequence): "Contract security signed the delivery. Same seal as last week."

[CH01_M01_DLG011] NOAH (intimate, tense; 3.3s; main sequence): "The triangle. Where did that come from?"

[CH01_M01_DLG012] RUSK (clipped, guarded; 2.0s; main sequence): "Eyes forward."

[CH01_M01_DLG013] ADRIAN (low, controlled; 2.1s; main sequence): "VANTAGE. You know them?"

[CH01_M01_DLG014] NOAH (intimate, tense; 4.1s; main sequence): "I know a crate I should never have opened."

[CH01_M01_DLG015] RUSK (clipped, guarded; 2.9s; main sequence): "Thirteen, Cross. Fourteen, Reyes. Welcome home."

[CH01_M01_DLG016] ADRIAN (low, controlled; 2.9s; main sequence): "Keep your voice below the pipes."

[CH01_M01_DLG017] NOAH (intimate, tense; 3.7s; main sequence): "You first. How do you know that name?"

[CH01_M01_DLG018] ADRIAN (low, controlled; 4.9s; main sequence): "Because somebody killed a man and left it in my file."

[CH01_M01_DLG019] NOAH (intimate, tense; 3.3s; main sequence): "A receipt. You said I needed one."

[CH01_M01_DLG020] RUSK (clipped, guarded; 6.5s; main sequence): "Property number forty-two. Keep the photograph. Lose the receipt and the rest was never here."

[CH01_M01_DLG021] GUARD (clipped, guarded; 3.3s; intake idle after 20s): "Step onto the painted mark. Both feet."

[CH01_M01_DLG022] ADRIAN (low, controlled; 3.3s; badge reminder): "The stamp, Reyes. Look at the stamp."

## Animation, cameras and performance

Noah protects photo, opens hands for search, changes overshirt off camera, walks escort route. Rusk checks cuffs, tags photo, then returns approved paper photograph before escort. Adrian rises from bench without approaching bars. Contacts require authored alignment markers; no assumed animation availability.

All camera transitions and shot IDs: [camera sheet](../screenplay/CH01_CAMERA_SHOTS.md). All start/end marks and contacts: [blocking](../screenplay/CH01_CHARACTER_BLOCKING.md). Full-screen CS01 locks both input contexts after shared ready; return blends both cameras0.4s. No cinematic begins while one actor is outside safe marker. Cinematic skip is mutual and commits identical state.

## NPCs, interactive objects and asset dependencies

Present: RUSK, NOAH, ADRIAN, GUARD. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_GUARD, CHAR_INMATE, PROP_PHOTO, PROP_VANTAGE_BADGE, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

Environment: [build specification](../environments/PRISON_INTAKE.md), [cell block](../environments/CELL_BLOCK.md). All interactives named in sequence are required subcomponents of its ENV record unless a PROP ID exists. Nothing listed here is assumed downloaded. Required clips map to [animation requirements](../technical/ANIMATION_REQUIREMENTS.md). [Asset manifest](../../asset_library/manifests/assets.json) governs actual availability.

## Checkpoints, failure and retry

Wrong interaction waits with authored guard bark. Escort pauses if either player behind. No combat or death. CP01_B both on cell landing after observations, before completion gate.

CP01_A scene entry restores both actors, owned inventory, doors, controls, patrol phase, dialogue consumed flags and knowledge snapshot atomically. CP01_B placement specified above is after the final reversible puzzle. Save schema includes checkpoint ID and committed transaction IDs; repeated inputs cannot duplicate pickups. Recover-stuck action returns same-route last safe mark with partner interaction paused. Boundary doors block leaving without partner; no invisible death volumes. No automatic restart during plot line playback. See [co-op specification](../technical/COOP_REQUIREMENTS.md).

## Exit state and next mission

Both confined on east landing. Photo tagged as approved paper effects and returned to Noah before cell assignment; other property stored in locker42. Adrian knows Noah recognized the mark; Noah knows Adrian noticed.

Only the shared scene-complete transaction advances to the next mission; M06 advances to CH02 title treatment. No uncommitted action survives retry. Mission durations include cinematics and total36minutes across Chapter1; narrative clock gaps are explicit transitions, not extra playable time.

