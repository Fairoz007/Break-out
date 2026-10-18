# Mission 06 — The Betrayal

ID CH01_M06 · Scene CH01_M06_SC01 · Cinematic CH01_M06_CS01. P1 Adrian, P2 Noah. Planning specification; no implemented gameplay or tested timing.

Time: 18 October 2028, 22:36. One continuous day; no unexplained time jump within scene.

Duration: 270s total; 100s cinematic allocation, 170s playable estimate.

## Exact playable sequence and ownership

Both inspect lock and pull handles. Security grille closes behind on CS01 trigger; no false escape skill test. Players retain look during reveal but no movement. After fade, P1 then P2 independently interact with solitary pipe; three knocks and response complete chapter.

Both inspect lock and pull handles together. Rear security grille closes only after both occupy safe marks; canonical capture follows without a false escape skill test. Rusk enters east with two guards; the sealed loading gate blocks retreat. Reveal establishes betrayal but daughter coercion remains unknown to protagonists. Shim confiscated; approved photo remains Noah shirt. After fade both independently tap solitary pipe: three knocks and response. No collected evidence remains.

Cooperative gates: Final handle action requires both ready. Capture is authored canonical event, not a failure. Solitary pipe sequence gives both players an active closing response.

## Objective and cinematic triggers

OBJ001 both pull handles; CS01 alarm and capture; OBJ002 both answer pipe. End card CH02 NIGHT SHIFT only after both interactions. IDs are CH01_M06_OBJ001 onward in listed order. Checkpoint CP06_A at scene entry, CP06_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

Objectives use the CH01_M06_OBJ prefix and numeric order above. Each gate checks both players alive/present and no cinematic lock. Plot lines serialize; progression waits for required dialogue, not arbitrary arrival timers. Input ownership is fixed P1/P2; no partner can operate both physically separated stations.

## Dialogue — complete authored scene lines

Source of truth: [full script](../screenplay/CH01_FULL_SCRIPT.md#ch01_m06_sc01), [dialogue register](../screenplay/CH01_DIALOGUE.md). Lines below mirror the authored version; future edits must update both documents and rerun consistency review. Context labels distinguish optional/retry from forward progress.

[CH01_M06_DLG001] NOAH (intimate, tense; 2.1s; main sequence): "Two handles. One promise."

[CH01_M06_DLG002] ADRIAN (low, controlled; 2.5s; main sequence): "On three. One. Two. Three."

[CH01_M06_DLG003] RUSK (clipped, guarded; 2.9s; main sequence): "Let go of the door. Slowly."

[CH01_M06_DLG004] NOAH (intimate, tense; 2.0s; main sequence): "You followed us."

[CH01_M06_DLG005] RUSK (clipped, guarded; 2.9s; main sequence): "I was told where to wait."

[CH01_M06_DLG006] ADRIAN (low, controlled; 4.1s; main sequence): "You left the diagram where we could find it."

[CH01_M06_DLG007] RUSK (clipped, guarded; 5.3s; main sequence): "I left you a route. I thought that was all they wanted."

[CH01_M06_DLG008] NOAH (intimate, tense; 2.0s; main sequence): "Who are they?"

[CH01_M06_DLG009] RUSK (clipped, guarded; 2.1s; main sequence): "Hands on your heads."

[CH01_M06_DLG010] NOAH (intimate, tense; 2.5s; main sequence): "That voice. Was it her?"

[CH01_M06_DLG011] RUSK (clipped, guarded; 2.1s; main sequence): "I do not know."

[CH01_M06_DLG012] ADRIAN (low, controlled; 3.7s; main sequence): "Then look at him when you say it."

[CH01_M06_DLG013] RUSK (clipped, guarded; 2.1s; main sequence): "I do not know."

[CH01_M06_DLG014] GUARD (clipped, guarded; 2.9s; main sequence): "On your knees. Both of you."

[CH01_M06_DLG015] NOAH (intimate, tense; 2.1s; main sequence): "We can still run."

[CH01_M06_DLG016] ADRIAN (low, controlled; 3.3s; main sequence): "No. Look at me. We stay alive."

[CH01_M06_DLG017] NOAH (intimate, tense; 2.5s; main sequence): "You knew this could happen."

[CH01_M06_DLG018] ADRIAN (low, controlled; 5.3s; main sequence): "I knew nothing was free. I did not know it was him."

[CH01_M06_DLG019] RUSK (clipped, guarded; 3.7s; main sequence): "Separate cells. No hospital transfer. They stay here."

[CH01_M06_DLG020] GUARD (clipped, guarded; 2.5s; main sequence): "That is not your decision."

[CH01_M06_DLG021] RUSK (clipped, guarded; 2.5s; main sequence): "Write my name on it."

[CH01_M06_DLG022] NOAH (intimate, tense; 2.0s; main sequence): "Cross?"

[CH01_M06_DLG023] ADRIAN (low, controlled; 2.0s; main sequence): "Still here."

[CH01_M06_DLG024] NOAH (intimate, tense; 2.0s; main sequence): "The harbor light."

[CH01_M06_DLG025] ADRIAN (low, controlled; 2.0s; main sequence): "Still turns."

[CH01_M06_DLG026] NOAH (intimate, tense; 2.5s; main sequence): "Then we try another way."

[CH01_M06_DLG027] ADRIAN (low, controlled; 3.3s; handle idle): "Together. I am ready when you are."

[CH01_M06_DLG028] NOAH (intimate, tense; 3.3s; pipe idle): "Three knocks. If you can hear me."

## Animation, cameras and performance

Both pull handles; Rusk raises palm, guards aim low ready then restrain after protagonists surrender. Noah attempts step forward, Adrian stops him with forearm. Controlled cuff and kneel animations; no player struggle QTE. Contacts require authored alignment markers; no assumed animation availability.

All camera transitions and shot IDs: [camera sheet](../screenplay/CH01_CAMERA_SHOTS.md). All start/end marks and contacts: [blocking](../screenplay/CH01_CHARACTER_BLOCKING.md). Full-screen CS01 locks both input contexts after shared ready; return blends both cameras0.4s. No cinematic begins while one actor is outside safe marker. Cinematic skip is mutual and commits identical state.

## NPCs, interactive objects and asset dependencies

Present: NOAH, ADRIAN, RUSK, GUARD. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_GUARD, PROP_SHIM, PROP_LEDGER, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES, VFX_ALARM. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

Environment: [build specification](../environments/MAINTENANCE_NETWORK.md), [solitary](../environments/CELL_BLOCK.md). All interactives named in sequence are required subcomponents of its ENV record unless a PROP ID exists. Nothing listed here is assumed downloaded. Required clips map to [animation requirements](../technical/ANIMATION_REQUIREMENTS.md). [Asset manifest](../../asset_library/manifests/assets.json) governs actual availability.

## Checkpoints, failure and retry

Capture is success. CP06_B after capture in solitary before pipe responses. Reload during cinematic restarts CP06_A; no save inside capture. Chapter-end save commits solitary responses and confiscation once.

CP06_A scene entry restores both actors, owned inventory, doors, controls, patrol phase, dialogue consumed flags and knowledge snapshot atomically. CP06_B placement specified above is after the final reversible puzzle. Save schema includes checkpoint ID and committed transaction IDs; repeated inputs cannot duplicate pickups. Recover-stuck action returns same-route last safe mark with partner interaction paused. Boundary doors block leaving without partner; no invisible death volumes. No automatic restart during plot line playback. See [co-op specification](../technical/COOP_REQUIREMENTS.md).

## Exit state and next mission

Both alive, separately confined; shim confiscated; approved photograph remains in Noah's shirt after routine restraint search, other intake property remains locker42; ledger remains at pump console. No carried evidence. Noah retains phrase and transfer schedule in memory. Rusk betrayal known, daughter coercion not yet confirmed.

Only the shared scene-complete transaction advances to the next mission; M06 advances to CH02 title treatment. No uncommitted action survives retry. Mission durations include cinematics and total36minutes across Chapter1; narrative clock gaps are explicit transitions, not extra playable time.


