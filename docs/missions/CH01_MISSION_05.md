# Mission 05 — Behind the Walls

ID CH01_M05 · Scene CH01_M05_SC01 · Cinematic CH01_M05_CS01. P1 Adrian, P2 Noah. Planning specification; no implemented gameplay or tested timing.

Time: 18 October 2028, 22:24. One continuous day; no unexplained time jump within scene.

Duration: 420s total; 65s cinematic allocation, 355s playable estimate.

## Exact playable sequence and ownership

Open gate with shim. P1 takes west catwalk, P2 east floor route. Read selector labels and brake status across wired maintenance handsets. P2 holds brake, P1 sets selector B then energizes only after clear call. Grille rises; both release controls and reunite through mechanically latched gate. Inspect transfer ledger and cached diagnostic recording at pump console. Approach spillway door together.

P1 west elevated route selector; P2 east floor brake. Use wired handsets: P2 holds brake and gives clear call, P1 selects B then energizes. Wrong A/C safely trips breaker and resets controls; no electrical injury. Grille mechanical latch holds after release. Both reunite, inspect ledger in place and cached recording, approach spillway. Ledger never enters inventory. Recorded voice uncertain, cached yesterday; no confirmed Elena survival.

Cooperative gates: Stable puzzle, no lethal electrical handling: closed labeled switchgear only. Wrong selector trips safe breaker and resets state. Handsets substitute for impossible room acoustics. Both routes have independent return access.

## Objective and cinematic triggers

OBJ001 reach relays; OBJ002 correct selector plus brake; OBJ003 both reunite; OBJ004 inspect ledger and voice; OBJ005 both approach door. CS01 plays console clue then returns control. IDs are CH01_M05_OBJ001 onward in listed order. Checkpoint CP05_A at scene entry, CP05_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

Objectives use the CH01_M05_OBJ prefix and numeric order above. Each gate checks both players alive/present and no cinematic lock. Plot lines serialize; progression waits for required dialogue, not arbitrary arrival timers. Input ownership is fixed P1/P2; no partner can operate both physically separated stations.

## Dialogue — complete authored scene lines

Source of truth: [full script](../screenplay/CH01_FULL_SCRIPT.md#ch01_m05_sc01), [dialogue register](../screenplay/CH01_DIALOGUE.md). Lines below mirror the authored version; future edits must update both documents and rerun consistency review. Context labels distinguish optional/retry from forward progress.

[CH01_M05_DLG001] ADRIAN (low, controlled; 2.9s; main sequence): "West side is a catwalk. Yours?"

[CH01_M05_DLG002] NOAH (intimate, tense; 3.7s; main sequence): "Floor route. Water below it, no way across."

[CH01_M05_DLG003] ADRIAN (low, controlled; 2.1s; main sequence): "Take the handset. Test."

[CH01_M05_DLG004] NOAH (intimate, tense; 3.7s; main sequence): "I hear you. Better than through a wall."

[CH01_M05_DLG005] ADRIAN (low, controlled; 4.1s; main sequence): "Selector has A, B, C. Which feeds the grille?"

[CH01_M05_DLG006] NOAH (intimate, tense; 4.1s; main sequence): "Diagram said B. Brake first. Give me a second."

[CH01_M05_DLG007] NOAH (intimate, tense; 4.1s; main sequence): "Brake held. My hands are clear of the chain."

[CH01_M05_DLG008] ADRIAN (low, controlled; 2.1s; main sequence): "Selecting B. Power on."

[CH01_M05_DLG009] NOAH (intimate, tense; 4.1s; main sequence): "Grille is up. Latch caught. You can let go."

[CH01_M05_DLG010] ADRIAN (low, controlled; 2.5s; main sequence): "Meet me by the pump."

[CH01_M05_DLG011] NOAH (intimate, tense; 2.0s; main sequence): "You waited."

[CH01_M05_DLG012] ADRIAN (low, controlled; 2.1s; main sequence): "I said I would."

[CH01_M05_DLG013] ADRIAN (low, controlled; 4.5s; main sequence): "Look at the dates. Transfer codes. No names. No destination."

[CH01_M05_DLG014] NOAH (intimate, tense; 3.3s; main sequence): "A boat every Thursday. No receiving prison."

[CH01_M05_DLG015] RECORDING (natural, understated; 4.9s; main sequence): "Calibration log. Channel seven. Tell N the harbor light still turns."

[CH01_M05_DLG016] NOAH (intimate, tense; 2.0s; main sequence): "Play that again."

[CH01_M05_DLG017] ADRIAN (low, controlled; 4.5s; main sequence): "It is damaged. We do not know who that is."

[CH01_M05_DLG018] NOAH (intimate, tense; 4.5s; main sequence): "Elena said that when our father was late coming home."

[CH01_M05_DLG019] ADRIAN (low, controlled; 4.1s; main sequence): "Somebody could know that. A recording could be old."

[CH01_M05_DLG020] NOAH (intimate, tense; 2.1s; main sequence): "The console says yesterday."

[CH01_M05_DLG021] ADRIAN (low, controlled; 4.9s; main sequence): "That is when it was copied. Keep the words. Keep moving."

[CH01_M05_DLG022] NOAH (intimate, tense; 5.3s; main sequence): "If there is a boat, there is a way to find her."

[CH01_M05_DLG023] NOAH (intimate, tense; 3.3s; wrong selector): "Breaker tripped. Set it back to neutral."

[CH01_M05_DLG024] ADRIAN (low, controlled; 3.3s; puzzle retry): "No rush. Brake, then B, then power."

## Animation, cameras and performance

P1 turns isolated selector; P2 holds mechanical brake; both pull separate door handles; Noah freezes at voice then deliberately lowers handset. Contacts require authored alignment markers; no assumed animation availability.

All camera transitions and shot IDs: [camera sheet](../screenplay/CH01_CAMERA_SHOTS.md). All start/end marks and contacts: [blocking](../screenplay/CH01_CHARACTER_BLOCKING.md). Full-screen CS01 locks both input contexts after shared ready; return blends both cameras0.4s. No cinematic begins while one actor is outside safe marker. Cinematic skip is mutual and commits identical state.

## NPCs, interactive objects and asset dependencies

Additional evidence asset: PROP_LEDGER (inspected in place).

Present: ADRIAN, NOAH, RECORDING. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

CHAR_ADRIAN, CHAR_NOAH, PROP_RELAY, PROP_LEDGER, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

Environment: [build specification](../environments/MAINTENANCE_NETWORK.md). All interactives named in sequence are required subcomponents of its ENV record unless a PROP ID exists. Nothing listed here is assumed downloaded. Required clips map to [animation requirements](../technical/ANIMATION_REQUIREMENTS.md). [Asset manifest](../../asset_library/manifests/assets.json) governs actual availability.

## Checkpoints, failure and retry

Wrong selector resets local puzzle only. Fall/stuck recovery restores same-route safe marker and pauses partner console. CP05_B at reunion after grille latched, before evidence inspection; inspected ledger/voice flags commit only at scene exit.

CP05_A scene entry restores both actors, owned inventory, doors, controls, patrol phase, dialogue consumed flags and knowledge snapshot atomically. CP05_B placement specified above is after the final reversible puzzle. Save schema includes checkpoint ID and committed transaction IDs; repeated inputs cannot duplicate pickups. Recover-stuck action returns same-route last safe mark with partner interaction paused. Boundary doors block leaving without partner; no invisible death volumes. No automatic restart during plot line playback. See [co-op specification](../technical/COOP_REQUIREMENTS.md).

## Exit state and next mission

Partial pump service ledger shows coded recurring offshore transfers, with no names or destination; the full rendition ledger is a distinct CH06 discovery. This ledger shows recurring offshore transfers; Noah suspects Elena survived but has no confirmation. They reach final door with incomplete evidence.

Only the shared scene-complete transaction advances to the next mission; M06 advances to CH02 title treatment. No uncommitted action survives retry. Mission durations include cinematics and total36minutes across Chapter1; narrative clock gaps are explicit transitions, not extra playable time.

