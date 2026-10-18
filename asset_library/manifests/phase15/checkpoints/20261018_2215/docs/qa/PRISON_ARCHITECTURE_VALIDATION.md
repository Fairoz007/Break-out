# Prison architecture and bespoke props — Phase 01.5

2026-10-18. **PARTIALLY_VERIFIED**. 48 original static GLB resources and 48 editable Blender sources now exist. No gameplay, complete prison scene, collision resources, navigation maps, or interaction animations were created. These assets reduce acquisition gaps; they do not establish final realistic art readiness.

## Evidence and scope

- [Manifest fragment](../../asset_library/manifests/phase15_architecture.json): exact paths, SHA-256, polygon counts, dimensions, scene dependencies, requirement parent IDs, and individual status.
- [Original source and renders](../../asset_library/extracted_sources/phase15_architecture/): Blender 5.1 sources, contact sheet, and readable diagram front view.
- [License](../../asset_library/licenses/phase15_architecture/LICENSE.md): original project meshes and procedural materials; embedded existing Poly Haven CC0 textures remain under original source licenses. Elena portrait is the coordinator-supplied original image; its provenance remains in the story texture record.
- [Build tool](../../tools/phase15_architecture.py), [portrait and diagram pass](../../tools/phase15_architecture_finish.py), [repair pass](../../tools/phase15_architecture_repair.py). Logs beside tools document actual Blender operations.

## Obtained through original modeling

16 architecture resources: 4 m concrete wall with lower paint band/skirting/expansion joints; 4 m floor and ceiling; pier; 3 m barred partition; 1 m cell door; 1.2 m security door; dual-handle spillway door; 1.1 m hatch; 2 m rail; 2×1.6 m catwalk; ten-riser stair; 2.8 m ladder; 2×5 m welded-wire fence; yard gate; barred window.

32 prop resources: intake counter/tray, table, chair, yard bench, bed, separate mattress/pillow, vented locker, sink/tap, toilet, front-loading industrial washer, idle laundry press with separate named guard and isolation lever, selector switchgear, brake station, service panel, flanged pipe, CCTV, floodlight, fluorescent fixture, radio, wired handset, spring shim, Elena photo sleeve, VANTAGE seal, transfer ledger, inspection lamp, scrap bin, linen trolley, water tap, drain, latch, separate paired handles, maintenance diagram.

## Actual validation

| Check | Result | Evidence and limits |
|---|---|---|
| Blender creation/export | VERIFIED | Successful 48 GLB outputs, named mesh parts, explicit metric dimensions, source saves |
| File integrity | PARTIALLY_VERIFIED | SHA-256 recorded for source/runtime; coordinator independent rehash pending |
| Source axis | VERIFIED | Blender Z-up source, standard glTF Y-up export; compare Godot transforms before construction |
| UV/material setup | PARTIALLY_VERIFIED | Cubic UVs for static meshes, packed 1k CC0 concrete/rust textures, original roughness/metal materials. Procedural bump does not bake into glTF; original sources retain it |
| Visual sample | PARTIALLY_VERIFIED | Actually re-imported and rendered 12 exported GLBs in contact sheet; inspected wall, bars, stair, fence, bed, washer, press, selector, toilet, handset, diagram back, portrait front. Separate diagram front render inspected and readable |
| Repairs | VERIFIED | Moved press safety guard in front of platen, laid ledger label onto paper, explicit ink shader on diagram, added named grip/look empties for selector/brake/press/door |
| Godot imports | PARTIALLY_VERIFIED | Coordinator integration owns Godot batch import/resource load evidence; do not infer from Blender |
| Modular layout | PARTIALLY_VERIFIED | Nominal 4 m concrete and 2 m rail/deck modules; barred partition outer extent 3.06 m includes frame, 1 m cell door outer extent 1.06 m. Match openings to outer extents rather than nominal labels |
| Collision/navigation | BLOCKED | No collision/nav resources. Use simple static boxes, low-cost hulls for furniture, single plane blockers for bars/fences. Validate routes with real characters in Phase 02 |
| Animation/interaction | BLOCKED | Static parts only; named grip empties are proposals. Door pivots, safety swept volumes, movable leaf separation and synchronized hand contacts require implementation/rig tests |

## Art and coverage limitations

The contact sheet shows recognizable beveled manufactured shapes and working textured materials. It also exposes heavy bright rust, uniform surfaces, simplified toilet basin and appliance shapes; these are usable original substitutes for construction, not approved photoreal final art. Do not call the entire set visually approved because 12 samples rendered. The initial contact sheet precedes the press/ledger repair, so consult updated source and repair log for corrected meshes.

The photo sleeve retains stable ID `P15_PHOTO_SLEEVE_EMPTY` and filename although it now contains Elena's original portrait. The diagram contains actual P1 selector B / P2 hold brake labels; half-screen legibility and cinematic camera scale remain untested. The transfer ledger is a labeled physical folder, not a fully authored close-up readable evidence page. VANTAGE seal needs art-direction review against all intended story markings.

Remaining architecture-specific requirements include transport bus, full pump machinery, four-metre lifting grille and drive assembly, full corridor/doorway trim variants, linen detail, ball/court markings, convincing institutional wear, proper glass translucency, authored ledger evidence text, and collision/navigation/assembly testing. These must stay visible under parent ENV requirements. No critical parent bundle is resolved solely by these child files existing.
