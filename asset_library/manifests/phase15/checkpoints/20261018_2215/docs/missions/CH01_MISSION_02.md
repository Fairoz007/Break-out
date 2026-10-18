# Mission 02 — Trouble in the Yard

ID CH01_M02 · Scene CH01_M02_SC01 · Cinematic CH01_M02_CS01. P1 Adrian, P2 Noah. Planning specification; no implemented gameplay or tested timing.

Time: 18 October 2028, 10:20. One continuous day; no unexplained time jump within scene.

Duration: 360s total; 45s cinematic allocation, 315s playable estimate.

## Exact playable sequence and ownership

P2 approaches exercise bench; Silas blocks exit. P1 walks to marked mediation space. P1 holds Silas attention in conversation while P2 rolls loose ball into empty fence section; guard looks west. Players withdraw together to tap alcove before whistle.

P1 mediates Silas at bench; P2 rolls loose ball to empty west fence lane after ready confirmation. Guard looks west; both withdraw to tap alcove. Ball never strikes an NPC. Silas retains hostile posture, two background inmates stay north; guard patrols east perimeter.

Cooperative gates: Conversation window waits for P2 ready. Distraction never injures an NPC. Missing timing resets standoff rather than forcing combat.

## Objective and cinematic triggers

OBJ001 both enter yard; OBJ002 P1 begin mediation and P2 roll ball; OBJ003 both reach tap alcove. Trigger CS01 once in alcove. IDs are CH01_M02_OBJ001 onward in listed order. Checkpoint CP02_A at scene entry, CP02_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

Objectives use the CH01_M02_OBJ prefix and numeric order above. Each gate checks both players alive/present and no cinematic lock. Plot lines serialize; progression waits for required dialogue, not arbitrary arrival timers. Input ownership is fixed P1/P2; no partner can operate both physically separated stations.

## Dialogue — complete authored scene lines

Source of truth: [full script](../screenplay/CH01_FULL_SCRIPT.md#ch01_m02_sc01), [dialogue register](../screenplay/CH01_DIALOGUE.md). Lines below mirror the authored version; future edits must update both documents and rerun consistency review. Context labels distinguish optional/retry from forward progress.

[CH01_M02_DLG001] SILAS (natural, understated; 2.5s; main sequence): "Fourteen. You borrowed my bench."

[CH01_M02_DLG002] NOAH (intimate, tense; 2.0s; main sequence): "It looked empty."

[CH01_M02_DLG003] SILAS (natural, understated; 2.9s; main sequence): "That was the invitation to ask."

[CH01_M02_DLG004] ADRIAN (low, controlled; 5.7s; main sequence): "He is on laundry. You break his hands, you wash your own sheets."

[CH01_M02_DLG005] SILAS (natural, understated; 2.5s; main sequence): "You vouching for him, Cross?"

[CH01_M02_DLG006] ADRIAN (low, controlled; 2.9s; main sequence): "I am saving you a chore."

[CH01_M02_DLG007] ADRIAN (low, controlled; 2.9s; main sequence): "Reyes. The ball. West fence. Easy."

[CH01_M02_DLG008] NOAH (intimate, tense; 2.5s; main sequence): "You want me to play?"

[CH01_M02_DLG009] ADRIAN (low, controlled; 2.9s; main sequence): "I want him looking somewhere else."

[CH01_M02_DLG010] GUARD (clipped, guarded; 3.3s; main sequence): "Away from the fence! All of you!"

[CH01_M02_DLG011] SILAS (natural, understated; 3.3s; main sequence): "This buys you a morning. Nothing else."

[CH01_M02_DLG012] NOAH (intimate, tense; 2.9s; main sequence): "You always make friends this quickly?"

[CH01_M02_DLG013] ADRIAN (low, controlled; 2.9s; main sequence): "Only when I need somebody alive."

[CH01_M02_DLG014] NOAH (intimate, tense; 5.7s; main sequence): "My sister Elena was on that run. They told me the boat burned."

[CH01_M02_DLG015] ADRIAN (low, controlled; 2.5s; main sequence): "Did you see her body?"

[CH01_M02_DLG016] NOAH (intimate, tense; 4.9s; main sequence): "I saw a bag. They would not let me open it."

[CH01_M02_DLG017] ADRIAN (low, controlled; 4.9s; main sequence): "The man I was accused of killing was investigating VANTAGE transfers."

[CH01_M02_DLG018] NOAH (intimate, tense; 4.1s; main sequence): "So we have a logo and two dead people."

[CH01_M02_DLG019] ADRIAN (low, controlled; 4.1s; main sequence): "We have people who want us to stop asking."

[CH01_M02_DLG020] NOAH (intimate, tense; 2.5s; main sequence): "Laundry. We keep asking there."

[CH01_M02_DLG021] SILAS (natural, understated; 2.0s; distraction idle after 20s): "Finished thinking?"

[CH01_M02_DLG022] ADRIAN (low, controlled; 3.3s; missed distraction reset): "Easy. We try when he turns again."

[CH01_M02_DLG023] NOAH (intimate, tense; 2.9s; optional skeptical stance; reconverges before next objective): "I do not trust you yet."

[CH01_M02_DLG024] ADRIAN (low, controlled; 3.3s; optional skeptical stance; reconverges before next objective): "Then trust what we can both see."

## Animation, cameras and performance

Silas blocks path and shoves shoulder once. Adrian places open hand between them; Noah rolls loose basketball toward west fence. Guard turns to rattle; both retreat with hands visible. Contacts require authored alignment markers; no assumed animation availability.

All camera transitions and shot IDs: [camera sheet](../screenplay/CH01_CAMERA_SHOTS.md). All start/end marks and contacts: [blocking](../screenplay/CH01_CHARACTER_BLOCKING.md). Full-screen CS01 locks both input contexts after shared ready; return blends both cameras0.4s. No cinematic begins while one actor is outside safe marker. Cinematic skip is mutual and commits identical state.

## NPCs, interactive objects and asset dependencies

Present: SILAS, NOAH, ADRIAN, GUARD. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_SILAS, CHAR_GUARD, CHAR_INMATE, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

Environment: [build specification](../environments/PRISON_YARD.md). All interactives named in sequence are required subcomponents of its ENV record unless a PROP ID exists. Nothing listed here is assumed downloaded. Required clips map to [animation requirements](../technical/ANIMATION_REQUIREMENTS.md). [Asset manifest](../../asset_library/manifests/assets.json) governs actual availability.

## Checkpoints, failure and retry

Missed distraction resets ball and standoff to safe marks; consumed story lines remain consumed. No fight or damage. CP02_B both at tap alcove before cinematic.

CP02_A scene entry restores both actors, owned inventory, doors, controls, patrol phase, dialogue consumed flags and knowledge snapshot atomically. CP02_B placement specified above is after the final reversible puzzle. Save schema includes checkpoint ID and committed transaction IDs; repeated inputs cannot duplicate pickups. Recover-stuck action returns same-route last safe mark with partner interaction paused. Boundary doors block leaving without partner; no invisible death volumes. No automatic restart during plot line playback. See [co-op specification](../technical/COOP_REQUIREMENTS.md).

## Exit state and next mission

Adrian and Noah agree to exchange information in laundry inspection detail. Silas remains hostile, neither protagonist becomes a murderer.

Only the shared scene-complete transaction advances to the next mission; M06 advances to CH02 title treatment. No uncommitted action survives retry. Mission durations include cinematics and total36minutes across Chapter1; narrative clock gaps are explicit transitions, not extra playable time.

