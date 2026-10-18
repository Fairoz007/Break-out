# Prison architecture and bespoke props — Phase 01.5

2026-10-18. **PARTIALLY_VERIFIED; functional for level blockout, not production art.** Current totals after the resumed session: 48 original modules/props plus 2 repair-cycle additions (17-riser 3 m stair, fence end post), 3 mission-critical originals (lifting grille, pump, basketball), 20 Poly Haven sets, 38 split kit pieces and 12 discovery props. All of them load in Godot 4.7.2. The paragraph below describes the original 48 at the time they were built.

Original state: 48 original static GLB resources and 48 editable Blender sources now exist. No gameplay, complete prison scene, collision resources, navigation maps, or interaction animations were created. These assets reduce acquisition gaps; they do not establish final realistic art readiness.

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

## Agent 03 geometric validation (resumed Phase 01.5)

2026-10-18. Covers the 48 original modules and props plus the 20 Poly Haven industrial prop sets (68 in total). Per-asset results: [architecture_validation.json](../../asset_library/manifests/phase15/architecture_validation.json). Scripts: `gltfparse.py` / `validate.py` (agent scratchpad, read-only on assets).

**Method.** A pure-Python glTF 2.0/GLB parser reads the JSON chunk, buffers and accessors. It transforms every referenced vertex through the full node hierarchy to get an exact world AABB, counts triangles from the index buffers, finds zero-area triangles (< 1e-10 m²), and checks material, UV0, normal and texture references. SHA-256 was recomputed for every runtime file. The Poly Haven copies were also checked against the provider MD5s from the API file listings. Godot was **not** run and no asset or manifest record was changed. As a cross-check, the AABB sizes match the coordinator's `godot_validation.json` bounds within 2 mm for 66 of 68 assets. The two that differ, stairs and the radio transceiver, differ only because Godot reports transformed local boxes for rotated nodes.

**Limits.** Headless parsing cannot show visual correctness, shading, snapping in an assembled scene, collision behaviour or navigation. The scale ranges below are real-world references chosen by Agent 03, not art-direction requirements. Visual evidence comes only from existing previews, each viewed once in this session. No new renders were made.

### Summary counts

| Check | Result | Status |
|---|---|---|
| Overall per-asset status | 0 VERIFIED, 67 PARTIALLY_VERIFIED, 1 FAILED (`PH15_STEEL_FRAME_SHELVES_01`) | PARTIALLY_VERIFIED |
| SHA-256 runtime vs records (48 GLB + 48 .blend; 20 sets, every runtime file) | All match; Poly Haven runtime files also match the provider MD5s | VERIFIED |
| Parse / buffers / textures present / every primitive has a material | 68/68 pass; no missing images, buffers or materials | VERIFIED |
| UV0 and normals on every primitive | 68/68 | VERIFIED |
| Empty or zero-size mesh nodes | 0 | VERIFIED |
| Zero-area triangles | 21 assets (17 original, 4 Poly Haven). Worst: fence 4,080 (30 %), photo sleeve 22 %, guard radio 21 %, catwalk 18 %. Harmless for rendering; clean up before any trimesh collision | PARTIALLY_VERIFIED |
| Y-up and plausible height | 67/68 plausible; shelves are ~10x too large | FAILED for 1 |
| Over 20k triangles (LOD and collision proxy required) | Rectangular airduct kit 45k, chain-link kit 89k, road barrier 23.8k, radio transceiver 42.4k, sectioned ladder 29.1k | flag |
| 10k to 20k triangles (LOD advised) | Original fence 13.5k, circular airduct kit 14.3k, searchlight 18.8k, fluorescent kit 17.8k, pipe wrench 10.7k, tool chest 13.4k, crate 18.3k, fire escape 11.3k | flag |
| Previews viewed by Agent 03 | 68/68 Godot previews, Blender contact sheet, diagram front render | PARTIALLY_VERIFIED |
| Visual not assessable | Fire escape (preview almost black); circular and rectangular airduct kits (preview too dark) | NOT TESTED |
| Assembled-scene snapping, collision, navigation, door animation | Not exercised | NOT TESTED |

### Scale anomalies

| Asset | Measured (glTF X×Y×Z m) | Finding |
|---|---|---|
| PH15_STEEL_FRAME_SHELVES_01 | 10.97 × 21.41 × 5.02 | **FAILED.** The proportions match a ~1.10 × 2.14 × 0.50 m shelf at 0.1 scale. Set 0.1 import/root scale or use a wrapper scene, then re-check visually. The Godot bounds confirm the size. |
| PH15_PORTABLE_SEARCHLIGHT | 0.17 × 0.19 × 0.25 | Plausible hand lantern. **Not** a guard-tower searchlight; do not use it at tower scale. |
| P15_WATER_TAP | 0.15 × 1.28 × 0.23 | A 1.2 m standpipe, not a wall tap; confirm the intent. The valve handle floats 0.0575 m above the pipe top. |
| P15_TRANSFER_LEDGER | 0.30 × 0.025 × 0.40 | Measured thickness 0.0253 m; the record says 0.0423 m (stale since the label repair). |
| P15_STEEL_CHAIR / CELL_BED / STEEL_TABLE / YARD_BENCH / RAILING | seat 0.475, bed pan 0.44, top 0.785, bench 0.485, rail 1.10 | Plausible |
| Doors: cell 2.2, security 2.2, spillway 2.5, gate 3.0 | — | Plausible. Cell-door clear opening is 0.94 × 2.04 m inside the frame. |
| P15_STAIRS_10_RISERS | rise 10 × 0.18 = 1.80, going 0.26 | Steps are comfortable, but 1.80 m does not match the 3.0 m wall storey (~17 risers needed) or any catwalk height. |

All other assets fall inside their reference height ranges (see the JSON `scale` block).

### Modular alignment

| Module | Nominal | Measured | Pivot / origin | Result |
|---|---|---|---|---|
| Wall 4 m | 4.0 × 3.0 | 4.000 × 3.000 × 0.300 | Base y=0, x centred; 0.25 m core centred on z=0 but trim only on the +z face | On grid (X, Y) |
| Floor 4 m | 4.0 × 4.0 | 4.000 × 0.200 × 4.000 | Top at y=0 (deliberate), centred | On grid |
| Ceiling 4 m | 4.0 × 4.0 | 4.000 × 0.480 × 4.000 | Slab centred on y=0; beam hangs to −0.40 | On grid. Beam soffit at 2.6 m when the slab sits at 3.0 m; check head clearance over the 2.5 m spillway door |
| Corner pier | — | 0.650 × 3.000 × 0.635 | Base y=0, x centred, z offset by the band | Height on grid |
| Cell bars 3 m | 3.0 | 3.060 outer | Base y=0, centred | Outer extent overshoots by 0.06 m; place by outer extent |
| Cell door 1 m | 1.0 | 1.060 outer | Base y=0, origin at centre, not at the hinge | Needs a hinge pivot node. Latch-side bar gap 0.178 m vs 0.106 m elsewhere |
| Security door 1.2 | 1.2 | 1.205 | Centre-bottom; hinge at x=−0.605 | No frame or jamb; needs a pivot |
| Spillway door | 2.0 | 2.005 × 2.500 | Centre-bottom | **One 2.0 m leaf** with two handles, not two separable leaves |
| Railing 2 m | 2.0 | 2.000 × 1.1025 | Base y=0, centred | Tiles at 2 m pitch with a 0.1 m gap between end posts |
| Catwalk 2 m | 2.0 × 1.6 | 2.000 × 0.134 × 1.600 | Deck top at y=0 (deliberate) | 1.6 m width is off the 0.5 m grid |
| Stairs | — | 1.600 × 1.917 × 2.600 | Origin mid first tread (z +0.13 to −2.47); stringers 0.117 m below y=0 | Off-grid pivot; rise mismatch (see above) |
| Ladder 2.8 | 2.8 | 0.56 × 2.80 | Base y=0, centred | OK |
| Fence 2×5 | 2.0 bay | 2.100 × 5.000 | Base y=0, centred | Posts at x=±1.0 coincide with neighbours at 2 m pitch (z-fighting); 72 separate mesh nodes; 8 mm wires alias in the preview |
| Yard gate 2 m | 2.0 | 2.060 × 3.000 | Base y=0, centred | Outer extent overshoots by 0.06 m |
| Pipe 2 m | 2.0 | 0.24 × 2.000 | Base y=0, vertical | OK; rotate for horizontal runs |
| Poly Haven kits (circular and rectangular airduct, chain-link, fire escape, fluorescent, rollershutter) | — | Multi-piece showcase layouts | Kit origin, not piece connection points | Split into per-piece scenes before snapping. Rectangular duct uses a 0.6 m step; circular duct a ~0.474 m step (not metric-grid); chain-link posts ~1.0/2.0 m pitch; fire escape is 9.76 m tall with its origin at mid-height |

Wall, floor, ceiling, railing, catwalk length, ladder and pipe meet the 4 m / 2 m nominal sizes within 1 cm. Bars, cell door, security door and yard gate exceed their nominal size by their frame (0.005–0.06 m). Match openings to the outer extents. None of this proves snapping in an assembled scene (NOT TESTED).

### Collision recommendations

| Class | Assets | Recommended |
|---|---|---|
| Structural boxes | wall, floor, ceiling (slab + beam), pier, catwalk deck, counter, locker, washer, scrap bin, panels, crate, radio set | BoxShape3D (trim, ribs and vents get no collision) |
| Barrier planes | cell bars, fence, chain-link panels, railing, barred window, press guard | One thin box per panel covering the whole plane (gaps up to 0.4 m); keep visibility raycasts passing through the bars |
| Moving leaves | cell door, security door, spillway door, hatch, yard gate, rollershutter, tool-chest lid | Box per leaf on an AnimatableBody3D with a hinge pivot node (none exists yet) |
| Stairs / ladders | stairs, fire-escape flights, both ladders | Ramp/convex slope proxy for stairs; box plus Area3D climb volume for ladders |
| Furniture | table, chair, bench, bed, toilet, sink, stool, trolley, press, barrier | Compound boxes or one convex hull; **never trimesh** on assets over 20k triangles |
| Pickups | radio, handset, shim, photo, badge, ledger, lamp, wrenches, searchlight | Small box/convex plus an interaction Area3D |
| None | CCTV, floodlight, fluorescent fixtures, security light, clock, fire alarm, diagram, drain, dual handles, ceiling ducts | No collider (mounted out of reach or flush); Area3D where interactive |

### Per-asset flags (most significant)

| Asset | Flag | Severity |
|---|---|---|
| PH15_STEEL_FRAME_SHELVES_01 | ~10x scale error | FAILED |
| P15_DOUBLE_SPILLWAY_DOOR | Single leaf, not a double door | Requirement risk |
| P15_STAIRS_10_RISERS | 1.80 m rise does not fit the 3.0 m storey; off-grid pivot | Assembly risk |
| P15_FENCE_2X5 | Coincident posts at 2 m pitch; 30 % zero-area triangles; 72 nodes; wire aliasing | Assembly / performance |
| P15_WATER_TAP | Valve floats 5.75 cm above the pipe | Visual defect (also seen in the preview) |
| P15_LINEN_TROLLEY | Wheels 2 cm above the floor | Minor |
| P15_CELL_DOOR_1M, P15_YARD_GATE_2M | Latch-side bar gap 0.178 / 0.138 m | Gameplay check |
| Doors and hatch | No hinge pivots; security door has no frame | Interaction blocker |
| P15_TRANSFER_LEDGER | Record dimensions stale | Record fix |
| P15_SINK, P15_SCRAP_BIN, P15_TOILET | Seen in the previews: straight-stick faucet, solid bin with no cavity, blocky toilet | Art fidelity |
| Poly Haven kits | Split into pieces; 5 assets over 20k triangles; rollershutter and fluorescent files hold several variants | Integration work |
| PH15_WALL_CLOCK, PH15_ROLLERSHUTTER_DOOR | Use KHR_materials_transmission / specular / ior; Godot support is partial, so check the glass and the look | Visual check |
| PH15_MODULAR_FIRE_ESCAPE, airduct kits | Previews too dark to judge | Visual NOT TESTED |

**Agent 03 verdict.** File integrity, parsing, materials, textures and metric scale are VERIFIED for 67 of 68 assets. The set as a whole is **PARTIALLY_VERIFIED**: one asset FAILED on scale, and assembly snapping, collision, navigation and door interaction remain NOT TESTED. Viewing 512 px previews does not amount to visual approval.

## Repair cycle 1 (FIX → RETEST, Agent 03)

2026-10-18. Blender 5.1 (`-b --factory-startup`) edited the saved `.blend` sources and re-exported each asset with the existing glTF settings (`GLB, export_yup, export_apply, export_extras`). Godot was **not** run. Before anything was overwritten, every runtime GLB, its `.blend` source and the shelves glTF were copied to [`asset_library/rejected/phase15_architecture_prerepair/`](../../asset_library/rejected/phase15_architecture_prerepair/); nothing was deleted. Before/after hashes, dimensions and change descriptions are in [architecture_repairs.json](../../asset_library/manifests/phase15/architecture_repairs.json). The pre-repair validation is kept as `architecture_validation_precycle1.json`; `architecture_validation.json` is now the post-repair retest.

### Fixes

| Item | Root cause / change | Retest (parser) | Status |
|---|---|---|---|
| PH15_STEEL_FRAME_SHELVES_01 | **Root cause:** the Poly Haven 1k glTF vertex data itself spans 10.97 × 21.41 × 5.02 m with no node scale. The original download is byte-identical, so this is not a project conversion error. **Fix:** node `scale [0.1,0.1,0.1]` added to the runtime glTF only; bin, textures and the original download are untouched | 1.097 × 2.140 × 0.502 m | VERIFIED (geometry) |
| P15_STAIRS_17_RISERS_3M (new) | 17 risers × 0.17647 m = 3.000 m; 16 treads × 0.28125 m = 4.500 m run; 1.5 m wide; origin at bottom-front centre | 1.5 × 3.0 × 4.5 m, on the 0.5 m grid; tread tops step evenly 0.1765 → 2.8235 m | VERIFIED (geometry) |
| P15_STAIRS_10_RISERS | Kept unchanged; the record now marks it a **1.8 m half-flight** | — | — |
| Security door | Origin on the hinge axis; leaf parented to `LEAF_HINGE`; new static steel frame (outer 1.30 × 2.25 m, 5 mm clearance) | Roots: frame ×3 plus `LEAF_HINGE` with 6 children | VERIFIED (hierarchy) |
| Spillway door | Rebuilt as two 0.995 m leaves (`Leaf_L_*`, `Leaf_R_*`) under `LEAF_LEFT_HINGE` (x=−0.98) and `LEAF_RIGHT_HINGE` (x=+0.98), with a 10 mm meeting gap; grips moved to the handles | 2.01 × 2.5 m; 2 pivots with 6 and 7 children | VERIFIED (hierarchy) |
| Hatch, cell door, yard gate | Origin moved to the hinge-side axis; leaf parented to `LEAF_HINGE` | Pivot at the origin | VERIFIED (hierarchy) |
| P15_FENCE_2X5 | Post removed from the +X end; bevel-collapsed wires rebuilt (8-sided) and joined into one mesh; new P15_FENCE_END_POST_5M for the end of a run | Zero-area triangles 4,080 → 0; triangles 13,536 → 2,468; mesh nodes 72 → 4; 2.05 m wide, tiles at 2.0 m | VERIFIED |
| P15_WATER_TAP | Valve lowered from z 1.27 to 1.2125 | No gap; height 1.225 m | VERIFIED |
| P15_LINEN_TROLLEY | All parts lowered 0.02 m | Lowest point y = 0.000 | VERIFIED |
| 15 others with zero-area triangles (wall, catwalk, security door, hatch, sink, toilet, floodlight, fluorescent fixture, radio, handset, photo sleeve, badge, ledger, lamp, bin) | Merge by distance (1e-5 m) plus dissolve degenerate | All 0 zero-area triangles; dimensions unchanged | VERIFIED (geometry) |
| Ledger record | Record dimensions now 0.0253 m thick (were stale) | — | VERIFIED |
| Optional: kit split | Chain-link fence (20 pieces) and rectangular airduct (18 pieces) exported per piece to `assets/props/phase15/split/<kit>/` (glTF + bin + shared `textures/`), origin at piece base centre; 38 `PH15_SPLIT_*` records marked DERIVED | 38/38: base at y=0, centred, materials and textures present, 0 zero-area triangles. Blender re-encoded the wire diffuse as PNG | PARTIALLY_VERIFIED |

All runtime and source checksums in the affected records were re-verified against disk with no mismatches. For repaired records, `polygon_count_if_known` now holds the exported triangle count.

### Retest summary

70 assets (68 plus 2 new): 0 FAILED, 70 PARTIALLY_VERIFIED, 0 checksum mismatches. Original assets with zero-area triangles: 17 → 0; only 4 Poly Haven props keep 1–2 each (untouched). Scale anomalies: none. Still over 20k triangles: the five Poly Haven assets listed above (unchanged).

### Visual evidence of the repairs

I re-imported the exported files into a fresh Blender scene, rendered them with Cycles and looked at both images:
- [qa_repair_cycle1_architecture.png](../../asset_library/extracted_sources/phase15_architecture/qa_repair_cycle1_architecture.png): the 17-riser stair rises to a catwalk at 3.0 m that matches the 3 m wall; the 10-riser half-flight is shown for comparison. The security door leaf swings −35° about its hinge while the new frame stays in place. The spillway leaves swing open in opposite directions about their outer hinges. The hatch, cell door and gate pivots were rotated, but their swing is hard to see from this camera. Three fence modules at 2.0 m pitch plus the end post show single posts with no doubling.
- [qa_repair_cycle1_props.png](../../asset_library/extracted_sources/phase15_architecture/qa_repair_cycle1_props.png): the shelves stand about 2.1 m beside a 1.8 m red reference pole. The tap valve sits on the pipe, the trolley wheels touch the ground, the handset and radio are intact after cleanup, and the split chain-link panel, post and duct pieces stand on the ground at their origins.
- Not re-rendered: sink, toilet, floodlight, fluorescent fixture, photo sleeve, badge, ledger, lamp, bin (cleanup only). The Godot previews in `previews/` now show **pre-repair** geometry for every repaired asset.

### Still open after cycle 1

- **Engine:** Godot re-import and load of every changed file NOT TESTED (coordinator owns this). Door swing in-engine, AnimatableBody behaviour, collision, navigation and assembled-scene snapping NOT TESTED.
- **Asset fixes not in scope this cycle:** cell-door latch-side bar gap (0.178 m); catwalk 1.6 m width off the 0.5 m grid; no handrail on the new stair.
- **Poly Haven:** circular airduct, fire escape, fluorescent and rollershutter kits not split; LOD for the five assets over 20k triangles.
- **Previews:** fire escape and airduct previews still too dark to judge.

## Mission-critical originals (coordinator, resumed session)

Built by [`tools/phase15_critical_props.py`](../../tools/phase15_critical_props.py), with Blender sources in `asset_library/extracted_sources/phase15_architecture/critical/`. Each was re-imported and rendered (`asset_library/manifests/phase15/previews_critical/`) and loads in Godot.

| ID | Size (m) | Notes |
|---|---|---|
| `P15_SECURITY_GRILLE_4M` | 4.4 × 3.6 × 0.73 | 4.0 × 3.0 m clear opening. Separate `grille_leaf` node with its pivot at the bottom centre (animate +Y by 2.9 m). Drive housing (motor, gearbox, sprocket), limit switch and `latch_point` empty. Serves M05 (grille raise) and M06 (rear grille closes). |
| `P15_PUMP_UNIT` | 2.4 × 1.96 × 1.0 | Centrifugal pump on skid and plinth, with a `ledger_inspect_marker` empty. Static. |
| `P15_BASKETBALL` | 0.238 | Size 7 ball. Seams are heavy procedural bands. |

## Godot asset inspection scene

[`tests/asset_inspection/phase15_asset_inspection.tscn`](../../tests/asset_inspection/phase15_asset_inspection.tscn) is built by [`tools/phase15_inspection_scene.gd`](../../tools/phase15_inspection_scene.gd). It is an **inspection scene only**, with no gameplay, input or mission logic. It places 129 items and records each one's origin-to-AABB offset in `asset_library/manifests/phase15/inspection/inspection_report.json`:

- **Zone A:** 4 m grid with floors, walls, pier, bars, doors, window, both stairs, catwalk, railings, ladder, hatch, fences and gate. Two raw-origin tests expose the pivot conventions.
- **Zone B:** every original prop, Poly Haven set and discovery prop.
- **Zone C:** all 19 PBR materials on 1 m cubes.
- **Zone D:** the realistic and proxy casts.

Renders (real GPU, gl_compatibility) are in `asset_library/manifests/phase15/inspection/*.png`.

What the renders show:

- Walls, floors and bars tile on the 4 m grid.
- The 17-riser stair reaches the 3 m catwalk height.
- Doors stand in their frames.
- Characters give a correct human scale beside the 1 m cell door and the counters.
- All 19 materials show distinct albedo and normal response.

Defects found and fixed in this loop:

- Characters were sunk by about 0.9 m. Godot's skinned-mesh AABB is in bind space, so characters are now placed by their foot-level origin.
- Autoplay set at build time had no effect, so idle playback is now called explicitly.

Visible art limits:

- Light concrete floors read nearly white under this lighting.
- The rust is heavy and uniform.
- The appliances are simplified.
- The watchtowers are stylised or medieval, and the bus is a stylised blockout with no interior.

Still NOT TESTED:

- Collision shapes.
- Navigation bake.
- Door swing in-engine.
- Split-screen performance.
- LOD for the five assets over 20k triangles.

## Readiness

- **Level blockout and construction (functional): PARTIAL to PASS.** Every interactive object named in the six mission sequences has an asset except the M01 body scanner and the M06 restraints (see the [coverage matrix](ASSET_COVERAGE_MATRIX.md)).
- **Production art: BLOCKED** on realistic institutional texturing, a realistic bus, watchtower and scanner, a court and markings, and collision/nav authoring.
