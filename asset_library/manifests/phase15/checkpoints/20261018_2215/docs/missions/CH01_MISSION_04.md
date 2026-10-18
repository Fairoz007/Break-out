# Mission 04 — Lights Out

ID CH01_M04 · Scene CH01_M04_SC01 · Cinematic CH01_M04_CS01. P1 Adrian, P2 Noah. Planning specification; no implemented gameplay or tested timing.

Time: 18 October 2028, 22:10. One continuous day; no unexplained time jump within scene.

Duration: 360s total; 35s cinematic allocation, 325s playable estimate.

## Exact playable sequence and ownership

P2 calls patrol turn from bars. P1 shims rear fastener and enters common service chase, unlatching cell14 service hatch from rear. P2 follows and holds hatch while P1 clears it. Alternate movement between concrete piers; reach restricted corridor manual gate.

P2 calls patrol turn; P1 uses shim on rear fastener, enters chase, unlatches cell14 rear panel. P2 follows and holds hatch while P1 clears. Both return panels flush, alternate concrete-pier shelters, reach manual gate unseen. Guard proposed loop45s with12s safe window, to be tuned. Detection always reloads CP04_A.

Cooperative gates: P1 cannot observe landing while shimming. P2 must call turn; ready prompt can wait indefinitely. Both physically clear hatch before either may close it.

## Objective and cinematic triggers

OBJ001 open two rear panels; OBJ002 both cross chase; OBJ003 reach gate unseen. CS01 at gate. Detection triggers fail overlay and reload CP04_A, never canonical capture. IDs are CH01_M04_OBJ001 onward in listed order. Checkpoint CP04_A at scene entry, CP04_B after final reversible puzzle; checkpoint restores both players, props, patrol phase and dialogue consumed flags atomically. No checkpoint inside locked cinematic.

Objectives use the CH01_M04_OBJ prefix and numeric order above. Each gate checks both players alive/present and no cinematic lock. Plot lines serialize; progression waits for required dialogue, not arbitrary arrival timers. Input ownership is fixed P1/P2; no partner can operate both physically separated stations.

## Dialogue — complete authored scene lines

Source of truth: [full script](../screenplay/CH01_FULL_SCRIPT.md#ch01_m04_sc01), [dialogue register](../screenplay/CH01_DIALOGUE.md). Lines below mirror the authored version; future edits must update both documents and rerun consistency review. Context labels distinguish optional/retry from forward progress.

[CH01_M04_DLG001] RUSK (clipped, guarded; 2.9s; main sequence): "Final count. Faces at the bars."

[CH01_M04_DLG002] NOAH (intimate, tense; 2.0s; main sequence): "Here."

[CH01_M04_DLG003] ADRIAN (low, controlled; 2.0s; main sequence): "Here."

[CH01_M04_DLG004] GUARD (clipped, guarded; 2.0s; main sequence): "East landing clear."

[CH01_M04_DLG005] NOAH (intimate, tense; 2.9s; main sequence): "He turns at the clock. Wait."

[CH01_M04_DLG006] ADRIAN (low, controlled; 2.0s; main sequence): "I am waiting."

[CH01_M04_DLG007] NOAH (intimate, tense; 2.9s; main sequence): "Now. His back is to us."

[CH01_M04_DLG008] ADRIAN (low, controlled; 3.7s; main sequence): "Panel is loose. Do not touch the edge."

[CH01_M04_DLG009] NOAH (intimate, tense; 3.3s; main sequence): "That is your idea of a door?"

[CH01_M04_DLG010] ADRIAN (low, controlled; 2.0s; main sequence): "Tonight it is."

[CH01_M04_DLG011] ADRIAN (low, controlled; 2.9s; main sequence): "Your hatch is open. Come through."

[CH01_M04_DLG012] NOAH (intimate, tense; 2.5s; main sequence): "Holding it. Move past me."

[CH01_M04_DLG013] GUARD (clipped, guarded; 2.0s; main sequence): "Who is there?"

[CH01_M04_DLG014] NOAH (intimate, tense; 2.1s; main sequence): "Stay behind the pier."

[CH01_M04_DLG015] ADRIAN (low, controlled; 3.3s; main sequence): "He heard the pipe. Let him pass."

[CH01_M04_DLG016] NOAH (intimate, tense; 2.5s; main sequence): "How far to the outside?"

[CH01_M04_DLG017] ADRIAN (low, controlled; 3.7s; main sequence): "Far enough that we keep our voices down."

[CH01_M04_DLG018] NOAH (intimate, tense; 2.9s; main sequence): "We still have the same promise?"

[CH01_M04_DLG019] ADRIAN (low, controlled; 2.5s; main sequence): "We still have two people."

[CH01_M04_DLG020] GUARD (clipped, guarded; 2.5s; detected fail only): "Stop! Hands above your head!"

[CH01_M04_DLG021] NOAH (intimate, tense; 2.9s; retry CP04_A): "Wait for his turn this time."

[CH01_M04_DLG022] ADRIAN (low, controlled; 2.5s; patrol warning): "Hold. Boots on the landing."

## Animation, cameras and performance

Shim panel, careful crouch through service opening, brace panel for partner, lean behind pier. No animation requires protagonists clipping through bars. Contacts require authored alignment markers; no assumed animation availability.

All camera transitions and shot IDs: [camera sheet](../screenplay/CH01_CAMERA_SHOTS.md). All start/end marks and contacts: [blocking](../screenplay/CH01_CHARACTER_BLOCKING.md). Full-screen CS01 locks both input contexts after shared ready; return blends both cameras0.4s. No cinematic begins while one actor is outside safe marker. Cinematic skip is mutual and commits identical state.

## NPCs, interactive objects and asset dependencies

Present: RUSK, NOAH, ADRIAN, GUARD. Recording in M05 is an unidentified cached voice, not proof of Elena's current location.

CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_GUARD, PROP_SHIM, AUDIO_PRISON, ANIM_HUMANOID, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. These are requirements, not a claim that files exist. Every performance needs the appropriate clip in ANIM_HUMANOID; missing clips are blockers for final production.

Environment: [build specification](../environments/CELL_BLOCK.md), [maintenance](../environments/MAINTENANCE_NETWORK.md). All interactives named in sequence are required subcomponents of its ENV record unless a PROP ID exists. Nothing listed here is assumed downloaded. Required clips map to [animation requirements](../technical/ANIMATION_REQUIREMENTS.md). [Asset manifest](../../asset_library/manifests/assets.json) governs actual availability.

## Checkpoints, failure and retry

Visible guard line-of-sight1.5s target with warning indicator; full detection reloads CP04_A after authored retry line. CP04_B both at restricted gate after panels restored; it is a completion recovery point, not a stealth bypass.

CP04_A scene entry restores both actors, owned inventory, doors, controls, patrol phase, dialogue consumed flags and knowledge snapshot atomically. CP04_B placement specified above is after the final reversible puzzle. Save schema includes checkpoint ID and committed transaction IDs; repeated inputs cannot duplicate pickups. Recover-stuck action returns same-route last safe mark with partner interaction paused. Boundary doors block leaving without partner; no invisible death volumes. No automatic restart during plot line playback. See [co-op specification](../technical/COOP_REQUIREMENTS.md).

## Exit state and next mission

Both beyond cell chase at locked maintenance gate. Panels returned flush; guard has not found empty cells.

Only the shared scene-complete transaction advances to the next mission; M06 advances to CH02 title treatment. No uncommitted action survives retry. Mission durations include cinematics and total36minutes across Chapter1; narrative clock gaps are explicit transitions, not extra playable time.

