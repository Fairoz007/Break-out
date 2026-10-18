# Prison Yard — environment build specification

ENV_YARD; CH01_M02_SC01. Proposed 40×30 m fenced yard; not playtested. x east, y up, z north, origin southwest floor. Fence height 5 m, surrounding wall 8 m. Surface falls 0.1 m toward south drains; walkable grade under 2%.

Y0 gate (2,0,15), Y1 court center (18,0,15), Y2 confrontation bench (24,0,12), Y3 tap alcove (9,0,24), loose ball start (22,0,12), empty west fence target (3,0,12), work-call gate (38,0,24). D1 west gate 2 m clear; D2 northeast gate 2 m. Court x10–30,z6–22; benches x7–10,z23–26 and x23–27,z11–13. Maintain1.6m withdrawal lane west of Silas; no box or collision volume may block it. Yard perimeter patrol lane 2.4 m wide.

Noah enters Y0→Y2; Adrian Y3→Y2. Silas at (25,0,13), two inmates at (27,0,14)/(27,0,16), withdrawing to north fence after guard response. East guard patrols (35,0,6)→(35,0,24), second guard north fence (12,0,28)→(28,0,28). P1 mediates Silas; P2 rolls ball into empty west fence section to draw guard attention. Both finish Y3→D2.

Overcast 10:20 morning haze lighting, wet concrete roughness with limited puddles; grass only inaccessible verge. MAT_CONCRETE/MAT_METAL, AUDIO_PRISON distant voices and fenced wind, dialogue ducking 6 dB proposed. Benches are cover-sized visual objects but no stealth occurs here. Fence and wall have full static collision; avoid detailed wire collision. Ball follows safe constrained path with no impact damage; no NPC occupies target lane.

Camera orbit range 2–4 m, keep fence outside dialogue reverses. Establishing shot (5,5,4), confrontation two-shot camera west of bench (21,1.6,12), conversation reverse toward blank wall rather than crowded background. NPC nav excludes ball lane while rolling; all gate links state-controlled. Accessibility route avoids steps. Acceptance: both player cameras retain silhouettes during intervention, distraction can be read without sound, ball route is clear, gate silhouette visible from tap alcove.

Assets: ENV_YARD (fence, walls, gates, court, benches, water tap, ball, drains, guard fixtures), CHAR_ADRIAN, CHAR_NOAH, CHAR_SILAS, CHAR_GUARD, CHAR_INMATE, PROP_PHOTO, ANIM_HUMANOID, AUDIO_PRISON, MAT_CONCRETE, MAT_METAL, UI_SUBTITLES. [Mission](../missions/CH01_MISSION_02.md). Subcomponents require separate manifest records if sourced separately; no yard kit currently presumed complete.


## Coordinate conversion and cinematic precedence

This document uses a drafting grid with +z north. Convert to Godot by (x,y,z_draft)→(x,y,-z_draft), then translate to the scene-local origin in the screenplay/blocking sheet. Those local cinematic relative actor positions take precedence for contact staging; environment coordinates are provisional room extents, not final actor transforms. Record the chosen origin marker in the future scene; never copy a drafting coordinate directly into Godot.

