# Bus and court asset work — 20 October 2026

## Reuse audit

Read `asset_library/manifests/phase025_bulk_20261019/inventory.csv`: no bus or hoop model exists in that bulk library (the two wicker baskets are unrelated). The actual game already uses the substantially more detailed Phase 03 bus and gooseneck hoop. Reviewed existing actual-game `docs/phase04/visual_evidence/iter02/bus.png` and `court_ground.png`; those images predate this work.

Imported actual bus GLB in Blender 5.1.1. `assets/props/phase04_realistic/bus_mesh_inspection.json` records true transformed vertex bounds, mesh names, triangles, materials, and SHA256. Ten mesh objects include separate four wheels and two hinged doors. Overall dimensions including mirrors/antenna are 12.123 x 3.238 x 3.571 m (Blender XYZ). Existing source is ajanhallinta, https://opengameart.org/content/3d-bus ; preserved local HTML explicitly identifies CC0 and original archive remains under `asset_library/original_downloads/phase025_integration/oga_bus/`. Existing derivative record identifies the conversion/build scripts. No new external model was downloaded, and no superior licensed replacement was established in this subtask.

Bus classification: **acceptable but needs improvement**, not ultra-realistic/VERIFIED. The screenshot shows simplistic continuous flat body finish and repetitive simplified upholstered seats. A mesh's triangle count does not establish realism. Retained rather than risk losing working animated wheel/door hierarchy or replace with low-poly bus.

## New court geometry

Produced `assets/props/phase04_realistic/hoop_perforated_steel.glb`, 75,936 triangles, plus JSON record and Blender preview. The original claimed perforated backboard was a solid 35 mm slab with dark square dots. New sheet has **756 actual circular through-holes** with modeled inner walls, 3 mm sheet thickness, and the same backboard extents. This changes actual geometry rather than surface paint. Corrected chain torus scaling so links become elongated ovals instead of thick round beads. Increased gooseneck bend subdivisions. Retains double steel rim, actual chain-link geometry, braces, base plate, four anchors and concrete foundation. Geometry is authored from existing project code; no third-party mesh added.

The original build function is imported without editing shared source. Reproduce using:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.1/blender.exe' -b --python tools/phase04_bus_court_build.py
```

## Integration instruction and acceptance boundary

Integrator: in `scripts/world/prison_court.gd` change `res://assets/props/phase03/hoop_gooseneck.glb` to `res://assets/props/phase04_realistic/hoop_perforated_steel.glb`. Same floor origin, local +X toward court, same rim 3.05 m, same overall dimensions. Leave placement/rotation and existing post collider unchanged. No script modifications made by this asset worker.

Status at handoff: **CONVERTED**, Blender preview visually inspected. Godot import, new in-game camera capture, collider/navigation and gameplay regression must be performed by integrator before INTEGRATED or VERIFIED. Preview establishes actual open perforations and a recognisable hoop; it does not certify cinematic quality or gameplay. Court's repeated severe asphalt cracks, bright uniform paint and surrounding plain walls remain visible quality limitations.

Executables found: Blender at `C:/Program Files/Blender Foundation/Blender 5.1/blender.exe`; repository launch documentation points Godot to `C:/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe`.

## Additional bus derivative delivered after audit

Built `blackridge_transport_bus_chassis.glb` with added lower-silhouette chassis frame rails, front/rear axles, suspension housings and leaf packs, differential, driveshaft, exhaust silencer and bent tailpipe. Imported/exported original bus without renaming original named nodes or changing wheel/door origins. `blackridge_transport_bus_chassis.asset_record.json` includes source license and checksum. Blender-rendered `bus_chassis_overview.png` and `bus_chassis_underside.png` were visually inspected. These additions improve exposed low-angle mechanical structure but do not resolve the simplistic body finish. Source textures were preserved by glTF export as adjacent image files.

Integrator: replace original Phase03 bus GLB path with `res://assets/props/phase04_realistic/blackridge_transport_bus_chassis.glb`, then test scripted door opening and rotating wheels. Same dimensions/pivots. New candidate status **CONVERTED** at handoff, not VERIFIED.

## Mission basketball audit and candidate

`scripts/missions/mission_02.gd` uses `res://assets/props/phase15/basketball.glb`. Existing builder makes a 48-segment sphere with broad black face-color seam bands and no pebble texture. Built `basketball_recessed_channels.glb`, 36,480 triangles, same size-7 circumference 0.749 m and floor origin; black rubber channels are physically recessed 1.1 mm, plus 0.12 mm fine geometry relief. Original project-authored geometry; checksum in adjacent JSON. Render `basketball_recessed_channels_preview.png` inspected: overall round silhouette and slimmer channels improve on old ball, but pole seam stepping and imperfect panel pattern remain. **Not close-up realism approved.** Integrator may use as gameplay-distance candidate by changing only mission_02.gd asset path; rerun roll-distraction regression. Status **CONVERTED** at handoff. No independent QA or gameplay certification performed by asset worker.

## Integration review and repaired ball revision

Root integrated bus/hoop and captured `docs/phase04/visual_evidence/realistic_after/`. Reviewed fresh `hoop_detail.png`: model sits properly on footing, support/rim/net visible, open perforated board reads correctly, shadow present. No obvious placement or missing-material failure. The chain net remains unusually shiny; gooseneck bend segmentation is visible in close view. Reviewed fresh `bus.png`: original body/wheel proportions and visible cabin remain intact; added underside geometry has only a small visual impact from this rear three-quarter gameplay camera. Flat white body and repetitive seating remain limitations. These are **INTEGRATED** visual findings, not final acceptance or gameplay certification.

Root rejected first ball preview because of pole-stepped black polygon seams. That rejection was valid. Repaired using dedicated `tools/phase04_bus_court_ball.py`: thin smooth analytic circular rubber insert meshes, seated in recessed orange shell; no black face-classification boundary. Fresh same-name GLB/record/preview replace rejected version. Visually inspected repaired render: jagged pole defect removed, rounded silhouette and continuous recessed channels intact. Eight-panel seam arrangement; lacks convincing leather pebble skin, so still not cinematic macro approved. Status remains **CONVERTED** pending root re-review and actual-game integration. Full bus/court builder now calls the repaired ball builder so reruns cannot restore rejected geometry.
