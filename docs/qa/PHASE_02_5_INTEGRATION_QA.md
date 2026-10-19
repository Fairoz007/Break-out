# Phase 02.5 asset integration — independent QA

19 October 2026. **INCOMPLETE. Production realism approval withheld.**

Reviewer: independent visual QA sub-agent, with no ownership of game implementation. Source inspection and direct image review are distinguished below from runtime tests. The lead runs Godot tests to avoid concurrent editor/import contention. The existence of 1,000 verified library assets is not evidence of their integration or visual acceptance.

## Evidence inspected

| Evidence | Finding | Result |
|---|---|---|
| `tests/phase025/evidence/integration/bus_converted.png` | Blender render now shows full coach shell, wheels, glazing, correctional bars, livery and seats. Markedly improved silhouette. Broad panels and detailing remain simple. | ACCEPTABLE TEMPORARY; Godot acceptance pending |
| `tests/phase025/evidence/integration/bus_interior.png` | Actual seat meshes, upholstery, central aisle and window bars are visible. Repeated seats and simple panels/fixtures remain below production target. | ACCEPTABLE TEMPORARY; not gameplay evidence |
| `tests/phase025/evidence/integration/initial/bus.png` | Only floating bars/livery visible; bus shell and wheels absent. Likely stale imported defective conversion, not a proven root cause. | FAILED; import and recapture required |
| `tests/phase025/evidence/integration/initial/yard.png` | Only dark ground and gray background; court, perimeter, equipment and lights absent. `capture_initial.log` confirms court GDScript type-inference parse errors for baseline/free_x/basket_x/arc_x/end_angle, then nonexistent build. | INVALID environment evidence; runtime error must be resolved |
| `tests/phase025/evidence/integration/initial/cellblock.png` | Full corridor visible, but repeated orange rust, noisy floor, open upper silhouette and sparse architecture remain obvious. | FAILED production realism |
| `tests/phase025/evidence/integration/initial/workshop.png` | Full room visible, but press and washers retain angular primitive silhouettes; very uniform space and distressed materials. | FAILED production realism |

These are intermediate captures while files are changing, not a controlled final comparison. The historical `after_valid/` set predates the current integration and remains the relevant earlier complete environment baseline. New final captures must record matching cameras and the source revision/hashes used.

The capture harness writes `cameras.json` with `written: true` even for the failed yard builder, because this field tests PNG saving only. It must not be interpreted as a successful scene build or visual pass. Inspect logs and the image contents as separate gates.

## Source findings and required regression tests

| ID | Finding / risk | Required evidence | Status |
|---|---|---|---|
| IQA-01 | Bus render and imported runtime asset disagree. | Reimport final GLB, fresh Godot exterior and interior captures, opening cinematic. | FAILED |
| IQA-02 | Court builder aborted in initial capture. | Error-free Godot log plus full yard image with geometry. | FAILED |
| IQA-03 | Ball rack at (31,-20) fell inside expanded 28 x 15 m court. Lead reports moved to (38,-20). | Final image and path test. | IMPLEMENTED — NOT VERIFIED |
| IQA-04 | Court surface initially resolved to tinted brushed concrete rather than requested worn asphalt. Lead reports actual downloaded asphalt being staged. | Resource path/provenance and close ground image. | IN PROGRESS |
| IQA-05 | Two nets initially created 256 individual CylinderMesh instances, adding avoidable draw overhead. Lead plans merge. | Mesh count and graphical frame cadence. | IN PROGRESS |
| IQA-06 | Bench, mediation, Silas and inmates moved north to clear expanded court; mission SH02/03 cameras changed. | Mission 2 actual movement, cooperative distraction, NPC withdrawal, both tap and exit; screenshots of SH02/03. | IMPLEMENTED — NOT VERIFIED |
| IQA-07 | East hoop post at x35.5 is close to guard lane x35. Static source spacing alone cannot prove navigation. | Guard patrol traverses z-6 to -24 without sticking; navigation path remains valid. | NOT TESTED |
| IQA-08 | New court surface collider sits 8 mm above existing floor; overlapping navigation source surfaces may bake differently. | Navigation bake log and physical player crossing all court edges. | NOT TESTED |
| IQA-09 | Acquired intake/workshop props introduce new AABB colliders. | Both players reach every mission interaction and all guards traverse intended paths. | NOT TESTED |
| IQA-10 | No complete visible Chapter 1 production review is available yet, including solitary and all cinematic angles. | Final images, full mission gameplay and defect list per environment. | NOT TESTED |

Court source has metric boundary/paint construction, smooth rim geometry, bracing and woven net strands; these are genuine geometry changes. They do not automatically establish credible wear, mounting detail, close-up quality or a realistic prison yard. No certification or commercial-game-equivalent claim is approved.

## Acceptance gates

Final review must include the bus in Godot, close and wide court views, each environment at matching before/after cameras, collision/navigation regression and graphical two-player mission progression. Headless checks cannot establish visible quality, camera usability or animation quality. Hardware controller routing and a human-controlled normal-speed playthrough remain separate acceptance requirements unless actually performed and evidenced.

No current finding establishes full recovery completion or Windows executable acceptance.

## Follow-up source review and intermediate bus retest

The reviewer directly opened `integration/settled/bus.png`: the Godot scene now visibly contains the complete shell, wheels, glazing, interior seats and livery. IQA-01's missing-shell defect is fixed in this intermediate runtime capture. This is an external view, not an in-game interior camera test or proof of animated doors. Blender source and runtime appearance are now consistent enough for **ACCEPTABLE TEMPORARY** classification, while production bus quality remains unapproved.

Source reinspection confirms explicit court variable types, `SurfaceTool.set_uv`, two merged net meshes rather than 256 strand nodes, ball rack moved to (38,-20), and court pavement placed outside the navigation region with collision layer zero. These repairs resolve the identified implementation patterns; final runtime evidence is still pending. The court now requests `asphalt_02`. Texture import maintenance enables mipmap generation and normal map import flags on staged runtime assets; its generated change list is evidence of configuration edits, not visual acceptance.

New geometry issue reported to lead: the rim is approximately 10 cm clear of the board and has no connecting mounting bracket in the inspected source. Add a bracket and mounting plate, then inspect close-up in Godot. A visibly floating rim would fail the detailed-hoop requirement even if court dimensions are correct.

The `settled/yard.png` capture is also intermediate: the lead reproduced the now-repaired `add_uv` call error. It must not be accepted as final court evidence. Await the final capture directory after reimport and error-free scene construction.

Direct review of the other `settled/` images found:

- Cellblock: dark painted stationary bars are a visible improvement. Some door bars still retain bright orange rust, producing inconsistent material treatment. Upper enclosure remains incomplete from this camera.
- Workshop: added hanging fixtures are visible, but primitive press/washer bodies still dominate. The room remains below the requested geometry quality.
- Maintenance: readable lighting pools and acquired hanging fixtures improve depth. Large turquoise pumps remain visibly simplified.
- Solitary: the image is almost entirely black apart from a sharply illuminated bed covering. Wall/bed details cannot be reviewed confidently, and readability fails this camera. Fixture presence does not prove useful illumination.

These are intermediate findings before the mipmap reimport, not judgments of the forthcoming final captures. They must not be silently closed by resource-import success alone.

## Final-directory visual review

The reviewer directly opened all ten PNGs in `tests/phase025/evidence/integration/final/`: bus, bus_interior, intake, cellblock, yard, court_layout, hoop_detail, workshop, maintenance and solitary. `capture_final.log` contains Godot 4.7.2 / D3D12 Forward+ startup with no error markers. This supersedes the intermediate capture failures for scene construction; it does not retroactively validate their images.

| Area | Verified visible result | Unresolved production gap | Decision |
|---|---|---|---|
| Bus exterior/interior | Complete coach geometry, wheels, window guards, upholstery, repeated seats and aisle are visibly integrated in Godot. | Flat exterior panels, simple interior fixtures, no verified opening-door animation or functional cabin traversal. | ACCEPTABLE TEMPORARY |
| Court layout | Complete marked court, both hoops and cracked asphalt visible. Ball rack outside playing rectangle. | Crack pattern repeats conspicuously as parallel tiled seams; distant lines break into dotted pixels. | ACCEPTABLE TEMPORARY |
| Hoop close-up | Rim, connecting bracket/mounting plate, target rectangle, braces and woven net visibly present. Previously reported floating-rim gap is fixed. | Pole/base and backboard remain plain manufactured forms; mounting/foundation detail sparse. | ACCEPTABLE TEMPORARY |
| Yard surroundings | Walls, fence, tower and court visible with readable directional shadows. | Fence has strongly repeated gold/rust pattern and cloth-like sagging silhouette; yard remains sparse. | FAILED production realism |
| Intake | Less aliasing, readable floor/walls, darker bars. | Primitive counter/lockers, inconsistent rusty dynamic gate material, sparse processing equipment. | FAILED production realism |
| Cellblock | Floor and walls visibly calmer after mipmaps; painted bars improve silhouette. | Open upper structure, sparse cells, orange door-bar material inconsistent with stationary bars. | FAILED production realism |
| Workshop | Lower texture grain; practical lights and rails readable. | Primitive press/washer silhouettes remain, widespread decorative rust, sparse industrial equipment. | FAILED production realism |
| Maintenance | Useful local light pools, clear stairs and gate, restrained wall appearance. | Simplified large pumps dominate foreground; large ceiling fixture shadow lacks plausible mounting detail. | FAILED production realism |
| Solitary | Light reaches part of bed/floor. | Almost black room and unlit fixture prevent adequate architectural/detail inspection; readability fails this camera. | FAILED visual readability |

IQA-01 and IQA-02 are now **VERIFIED** for missing-body / aborted-builder repairs. IQA-03 is **VERIFIED** visually for rack placement. IQA-04 is **VERIFIED** for actual asphalt integration, while realism defects remain. IQA-05 is **VERIFIED** by source inspection for two merged nets; performance acceptance remains untested by this reviewer. IQA-08 is **VERIFIED** by source inspection for removing the overlay from collision/navigation; physical gameplay still needs regression. IQA-06/07/09 remain **NOT TESTED** until mission movement and patrol evidence is supplied. IQA-10 now has complete static environment coverage for this harness, but **FAILED** production quality and gameplay coverage is incomplete.

The line discontinuity is a visible observation; its cause is not independently isolated. Possible subpixel aliasing or insufficient depth separation must be tested rather than assumed. Mipmap changes visibly reduce material grain across the interiors, a defensible improvement. These screenshots do not support claiming the entire game now looks realistic or production ready.

## Revised verified-directory review

All ten images under `tests/phase025/evidence/integration/verified/` were directly opened by this reviewer. `tests/phase025/evidence/integration/capture_verified.log` contains renderer startup and no error markers. These observations supersede the corresponding earlier material/readability findings:

- `verified/bus_interior.png` and `verified/bus.png`: brown leather seating now has credible upholstery grain instead of the earlier conspicuous denim clothing pattern. Complete cabin geometry remains visibly integrated. ACCEPTABLE TEMPORARY; door animation and functional interior traversal remain unverified.
- `verified/intake.png` and `verified/cellblock.png`: dynamic doors now visually match the dark stationary steel bars. The inconsistent rusty door-bar defect is closed for these views. Countertop and locker-detail rust remains conspicuous, with simple counter/locker geometry and sparse furnishings.
- `verified/yard.png`, `verified/court_layout.png` and `verified/hoop_detail.png`: gray steel fence treatment removes the implausible gold finish. The fence's original sagging/wavy geometry remains below the intended secure chain-link reference; a replacement is reportedly under construction and is NOT verified here. Complete court, asphalt and detailed hoops remain visible. Repeated asphalt cracks and distant dotted lines remain visible. These captures use the pre-TAA review configuration; a later split-screen TAA edit is not verified by these stills.
- `verified/solitary.png`: added fill makes bars, walls and floor sufficiently visible to inspect. The almost-entirely-black readability defect is improved. The bed covering still appears covered in a bright orange rust texture, inconsistent with bedding; the wall fixture appears unlit despite scene fill. Production visual acceptance remains FAILED.
- `verified/workshop.png` and `verified/maintenance.png`: no change closes the prominent simplified machine/pump geometry issue. Production visual acceptance remains FAILED.

The source Chapter 1 graphical run (`integration/chapter_gfx.log` / prospective `chapter_gfx.json`, `chapter_shots/`) was still active at this review. Startup and a navigation voxel rounding warning are not proof of completed gameplay. It uses virtual inputs at time scale 3, so even a successful completion would establish automated graphical progression rather than a normal-speed human-controlled playthrough.
