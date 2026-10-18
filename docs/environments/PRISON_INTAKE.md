# Prison Intake — environment build specification

ENV_INTAKE; CH01_M01_SC01. All dimensions are provisional metric blockout targets, not tested architecture. Coordinates (x,y,z) use x east, y up, z north; floor y=0. Local origin southwest corner. Connect east exit to cell block west entry through an occluded streaming vestibule; transforms must be surveyed together before art lock.

## Layout and paths

Main footprint 24 m east-west × 16 m north-south, ceiling 4 m. Transport apron x0–8,z0–8 outdoors; secure reception x8–24,z0–8; holding x8–16,z8–16; property counter x16–24,z8–16. Partitions 0.25 m thick, doors have 1.2 m clear width, corridors 2.4 m minimum. I0 bus step (4,0,4), I1 screening (10,0,4), I2 property tray (19,0,10), I3 guard desk (21,0,12), I4 Adrian holding mark (12,0,12), I5 east exit (24,0,6). Gate D1 (8,0,4), holding grille D2 (16,0,12), exit D3 (24,0,6). D1/D3 cannot be open together during escort.

Noah path I0→I1→I2→I5; Adrian I4→I5 after approved property processing and escort. Guard counter→grille→exit; queued inmates stay x9–13,z9–11. Benches and counter are static obstructions, not stealth cover. Grille view must show badge without requiring extreme zoom. I4 and I2 are separated by transparent grille so neither screen is visually isolated from the action.

## Build, audiovisual and camera constraints

Concrete walls/floor MAT_CONCRETE, painted steel doors/grille MAT_METAL, restrained cold fluorescent interior, overcast morning apron. No baked shadow may obscure the tray. AUDIO_PRISON zones: exterior engine/coastal wash, reception ventilation, sharp grille/door tails; apply room transitions over 1 m. CS01 bus establishing camera at (2,2,0), tray insert clearance above (19,1.3,10), guard reverse from (17,1.6,12). Camera radius 0.25 m proposed; walls and grille constrain third-person distance 1–3 m. Ceiling panels allow cinematic rig paths but are not physically removed in ordinary gameplay.

Collision: sealed wall boxes, no per-triangle dynamic prop collision, grille visually transparent but physically solid. Nav: 0.4 m proposed agent radius, 2 m height; exclusion inside counter and benches, door links disabled while locked. Escort waits at corner I1 until both within 4 m. Interaction markers cannot overlap guard navigation. Bus boarding animation root locked to step height 0.35 m pending rig tests.

## Asset/build list

Manifest IDs: ENV_INTAKE (bus/apron/gates/grille/counter/benches/fluorescents as required submeshes), PROP_PHOTO, PROP_VANTAGE_BADGE, CHAR_ADRIAN, CHAR_NOAH, CHAR_RUSK, CHAR_GUARD, CHAR_INMATE, MAT_CONCRETE, MAT_METAL, AUDIO_PRISON, ANIM_HUMANOID, UI_SUBTITLES. Every kit subcomponent must get a child record if acquired separately. Existing IDs describe requirements, not proof of files. Art acceptance: door clearance, sightline to badge, no near-plane clipping at tray, both escort routes traversable. [Mission 1](../missions/CH01_MISSION_01.md).

## Coordinate conversion and cinematic precedence

This document uses a drafting grid with +z north. Convert to Godot by (x,y,z_draft)→(x,y,-z_draft), then translate to the scene-local origin in the screenplay/blocking sheet. Those local cinematic relative actor positions take precedence for contact staging; environment coordinates are provisional room extents, not final actor transforms. Record the chosen origin marker in the future scene; never copy a drafting coordinate directly into Godot.

