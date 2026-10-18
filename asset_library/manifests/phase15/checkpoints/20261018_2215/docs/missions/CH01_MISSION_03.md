# Mission 03 — The Workshop

ID CH01_M03 · Scene CH01_M03_SC01 · Cinematic CH01_M03_CS01. P1 Adrian, P2 Noah. Planning specification; no implemented gameplay or tested timing.

Time: 18 October 2028, 14:05. One continuous day; no unexplained time jump within scene.

Duration: 420s total; 50s cinematic allocation, 370s playable estimate.

## Exact playable sequence and ownership

Mara asks for contaminated linen isolation. P2 deliberately starts the doctor conversation at the blue table (DLG003); Rusk turns to interrupt (DLG004), then goes to the office for the requested inspection lamp after DLG006. This is the nonviolent guard distraction. P1 locks out idle press lever while P2 clears screen, then P2 holds inspection lamp while P1 reads maintenance diagram. They restore screen before Rusk return. P2 palms discarded spring strip from scrap bin as shim.

P1 holds isolation lever while P2 clears screen. P2 holds lamp while P1 reads north-route diagram; P2 reads relay-key half. Mara uses contaminated linen inspection to occupy guard attention; Rusk leaves aisle before shared cinematic. Restore screen, memorize/return diagram, P2 acquires discarded spring-strip shim from scrap. A safe handoff at work exit assigns shim to Adrian for M04, shown in blocking.

Cooperative gates: Two-stage interlock: operator must keep isolation lever held; releasing pauses retrieval with hand withdrawn first. Diagram has north route on P1 view, relay key on P2 view, requiring spoken exchange.

## Objective and cinematic triggers

OBJ001 isolate and inspect; OBJ002 both inspect diagram halves; OBJ003 replace screen and collect shim. CS01 begins after Rusk leaves aisle. IDs are CH01_M03_OBJ001 onward in listed order. Checkpoint CP03_A at scene entry, CP03_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

Objectives use the CH01_M03_OBJ prefix and numeric order above. Each gate checks both players alive/present and no cinematic lock. Plot lines serialize; progression waits for required dialogue, not arbitrary arrival timers. Input ownership is fixed P1/P2; no partner can operate both physically separated stations.

## Dialogue — complete authored scene lines

Source of truth: [full script](../screenplay/CH01_FULL_SCRIPT.md#ch01_m03_sc01), [dialogue register](../screenplay/CH01_DIALOGUE.md). Lines below mirror the authored version; future edits must update both documents and rerun consistency review. Context labels distinguish optional/retry from forward progress.

[CH01_M03_DLG001] MARA (natural, understated; 5.7s; main sequence): "Medical linen on the blue table. Keep it clear of the general wash."

[CH01_M03_DLG002] NOAH (intimate, tense; 4.1s; main sequence): "You are the doctor. Why are you counting sheets?"

[CH01_M03_DLG003] MARA (natural, understated; 4.9s; main sequence): "Because blood does not stop being evidence when somebody washes it."

[CH01_M03_DLG004] RUSK (clipped, guarded; 2.1s; main sequence): "Inspection, Doctor. Not conversation."

[CH01_M03_DLG005] ADRIAN (low, controlled; 4.1s; main sequence): "This press is catching. We need the inspection lamp."

[CH01_M03_DLG006] RUSK (clipped, guarded; 3.3s; main sequence): "You have one cycle. Then it works."

[CH01_M03_DLG007] ADRIAN (low, controlled; 4.1s; main sequence): "Lever down. Tell me when your hands are clear."

[CH01_M03_DLG008] NOAH (intimate, tense; 2.1s; main sequence): "Clear. Hold it there."

[CH01_M03_DLG009] NOAH (intimate, tense; 3.3s; main sequence): "There is a plan behind the screen."

[CH01_M03_DLG010] ADRIAN (low, controlled; 3.7s; main sequence): "Service corridor E. It runs behind our landing."

[CH01_M03_DLG011] NOAH (intimate, tense; 4.5s; main sequence): "Two relays. One opens the grille, one feeds the lock."

[CH01_M03_DLG012] ADRIAN (low, controlled; 2.0s; main sequence): "Same time?"

[CH01_M03_DLG013] NOAH (intimate, tense; 2.1s; main sequence): "Same circuit. Different rooms."

[CH01_M03_DLG014] MARA (natural, understated; 3.7s; main sequence): "Put the screen back before you restart it."

[CH01_M03_DLG015] RUSK (clipped, guarded; 2.1s; main sequence): "Doctor. The clinic called?"

[CH01_M03_DLG016] MARA (natural, understated; 4.1s; main sequence): "The envelope is sealed, Officer. Read it somewhere private."

[CH01_M03_DLG017] NOAH (intimate, tense; 2.0s; main sequence): "He looks frightened."

[CH01_M03_DLG018] ADRIAN (low, controlled; 3.7s; main sequence): "Remember that. Do not mistake it for kindness."

[CH01_M03_DLG019] ADRIAN (low, controlled; 4.5s; main sequence): "After count, I open my panel. You watch the landing."

[CH01_M03_DLG020] NOAH (intimate, tense; 4.5s; main sequence): "We leave together. No doors shut behind the other man."

[CH01_M03_DLG021] ADRIAN (low, controlled; 2.0s; main sequence): "Agreed."

[CH01_M03_DLG022] NOAH (intimate, tense; 2.0s; main sequence): "That sounded rehearsed."

[CH01_M03_DLG023] ADRIAN (low, controlled; 3.3s; main sequence): "It is a promise. Those need practice."

[CH01_M03_DLG024] NOAH (intimate, tense; 2.9s; lever released early): "Hands back. Lock it down again."

[CH01_M03_DLG025] RUSK (clipped, guarded; 2.1s; idle bark): "Less talking. More linen."

## Animation, cameras and performance

Adrian isolates press with lever, Noah removes loose lint screen and retrieves paper; hands stop before moving machinery. Mara inspects medical linen; Rusk folds clinic envelope into shirt. Contacts require authored alignment markers; no assumed animation availability.

All camera transitions and shot IDs: [camera sheet](../screenplay/CH01_CAMERA_SHOTS.md). All start/end marks and contacts: [blocking](../screenplay/CH01_CHARACTER_BLOCKING.md). Full-screen CS01 locks both input contexts after shared ready; return blends both cameras0.4s. No cinematic begins while one actor is outside safe marker. Cinematic skip is mutual and commits identical state.

## NPCs, interactive objects and asset dependencies

Present: MARA, NOAH, RUSK, ADRIAN. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_MARA, CHAR_GUARD, PROP_DIAGRAM, PROP_SHIM, PROP_RELAY, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

Environment: [build specification](../environments/LAUNDRY_WORKSHOP.md). All interactives named in sequence are required subcomponents of its ENV record unless a PROP ID exists. Nothing listed here is assumed downloaded. Required clips map to [animation requirements](../technical/ANIMATION_REQUIREMENTS.md). [Asset manifest](../../asset_library/manifests/assets.json) governs actual availability.

## Checkpoints, failure and retry

Releasing lever withdraws hands before any state change; pauses progress. Guard attention expires safely, re-offer linen inspection. CP03_B after screen restored and shim collected, before closing cinematic.

CP03_A scene entry restores both actors, owned inventory, doors, controls, patrol phase, dialogue consumed flags and knowledge snapshot atomically. CP03_B placement specified above is after the final reversible puzzle. Save schema includes checkpoint ID and committed transaction IDs; repeated inputs cannot duplicate pickups. Recover-stuck action returns same-route last safe mark with partner interaction paused. Boundary doors block leaving without partner; no invisible death volumes. No automatic restart during plot line playback. See [co-op specification](../technical/COOP_REQUIREMENTS.md).

## Exit state and next mission

Diagram memorized, original returned to prevent suspicion. Shim concealed. Plan: cell service panel, restricted corridor, maintenance spillway door.

Only the shared scene-complete transaction advances to the next mission; M06 advances to CH02 title treatment. No uncommitted action survives retry. Mission durations include cinematics and total36minutes across Chapter1; narrative clock gaps are explicit transitions, not extra playable time.

