# Cell Block — environment build specification

ENV_CELLBLOCK; CH01_M01_SC01, CH01_M04_SC01, CH01_M06_SC01. Provisional metric targets; untested. x east, y up, z north, origin southwest floor.

## Coordinate layout

Main hall 32×18 m, height 7 m; playable ground gallery only. Central circulation x0–32,z6–12, clear width 6 m. Six south cells occupy x2–26,z0–6, six north cells x2–26,z12–18; ordinary cells 4×6 m gross; hero cells13/14 have3m frontage, ceiling 3 m. C13 Adrian x10–13,z0–6, C14 Noah x13–16,z0–6. Doors centered (11.5,0,6) and (14.5,0,6), 1 m clear. Rear service panels in cells13/14 connect to a common1.6m-wide chase south of cell bank; the chase exits at C5. Damaged rear panels are a bespoke requirement, not implied by every prison kit. West entry C0 (0,0,9); guard start C1 (4,0,9); patrol north turn C2 (26,0,12); shelter C5 (27,0,7); service door (30,0,9); restricted corridor x30–38,z8–11; maintenance hatch C6 (38,0,9.5), 1.1×1.1 m with crawl transition.

Solitary annex is a separate occluded set, not directly walkable from hall: two 3×4 m cells separated by 0.25 m wall, corridor 2 m wide. Wall taps carry through shared wall; neither player sees through it. Captured actors start seated at mirrored (1.5,0,2)/(4.75,0,2) in annex-local space.

## Paths, doors and camera

Intake escort west entry→central lane→C13/C14. Night player path rear cell panels→common chase→concrete pier shelters→C5→restricted manual gate C6. Patrol C1→C2→north gallery→C5 sightline→C1, proposed 45 s loop/12 s safe opportunity. No stairs or upper-floor navigation needed in Chapter 1; inaccessible gallery uses visible locked gates. Door handoff needs two 0.8 m interaction marks on opposite sides with 1.6 m passing clearance. Pillar at (27,0,6.5) provides genuine visual occlusion; no invisible cover.

Third-person camera compresses to 1 m in cells, 3 m in hall. CS01 ceiling track at y4.5 follows lights; no shot goes through cell bars. Solitary medium close-ups remain within 3 m cell walls. Test two bodies and cameras through every doorway before art lock.

## Rendering, sound, physics and navigation

Day: diffuse skylight, neutral concrete and chipped painted steel. Night: warm guard desk, low blue safety lights; lit lanes communicate patrol risk without pitch black areas. MAT_CONCRETE/MAT_METAL; AUDIO_PRISON cells use short reverb, corridor longer slap, solitary muted ventilation and taps. Steady red wash for capture annex transition; no strobe by default.

Static box collision for walls/bars, convex door collision; disable door movement until both actors out of sweep volume. Agent radius 0.4 m proposed; dynamic links on service door and hatch. Hatch traversal is an explicit animation link, never a general navmesh hole. Sound detection is scripted authored zone behavior in Phase 2; do not assume propagation simulation.

## Required assets

ENV_CELLBLOCK includes cells, beds, toilets, bars, gallery, pillars, spring service door, release box, hatch, solitary annex and light fixtures. Other IDs: CHAR_ADRIAN, CHAR_NOAH, CHAR_GUARD, PROP_PHOTO, PROP_SHIM, ANIM_HUMANOID, AUDIO_PRISON, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. [M01](../missions/CH01_MISSION_01.md), [M04](../missions/CH01_MISSION_04.md), [M06](../missions/CH01_MISSION_06.md). All custom geometry remains an acquisition/build gap until manifest says otherwise.


## Coordinate conversion and cinematic precedence

This document uses a drafting grid with +z north. Convert to Godot by (x,y,z_draft)→(x,y,-z_draft), then translate to the scene-local origin in the screenplay/blocking sheet. Those local cinematic relative actor positions take precedence for contact staging; environment coordinates are provisional room extents, not final actor transforms. Record the chosen origin marker in the future scene; never copy a drafting coordinate directly into Godot.

