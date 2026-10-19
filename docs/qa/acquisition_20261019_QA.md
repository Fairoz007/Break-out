# Independent acquisition QA — 19 October 2026

Reviewer: separate research/QA worker. Checks below were rerun against actual local files. Canonical manifest was not modified. New conversion results will be appended when delivered.

## Baseline and 22-bundle reconciliation

PASS: baseline_audit.json contains 831 canonical asset records and 22 requirement bundles. Every listed child ID exists in assets.json. All 1,125 runtime file references (984 unique paths) were independently read and SHA-256 checked against the baseline snapshot: zero missing files and zero changes since that snapshot. Historical usability/import/visual labels were not independently rerun for these baseline files; file presence does not certify production quality.

The reconciliation accurately keeps every bundle PARTIAL or BLOCKED. Child counts include unusable/proxy variants, so they must not be described as counts of production-ready assets. Baseline audit compares some canonical hashes only where recorded; a null recorded_hash_match is not a verified historical checksum.

## Steel shelf hash discrepancy resolved

PH15_STEEL_FRAME_SHELVES_01 has a stale canonical hash, not unexplained geometry corruption. Independent current SHA-256 is `d1d34aef06fe254dfeafb16f9c60bc50d5ee105295b53644b47ebb67766a0b68`. The architecture repair report's after-hash `d55c1a97d92064f76139ba52530746d234a108d89e5e347330285d068efcd390` is reproduced exactly by serializing current LF text with CRLF line endings.

Parsed current glTF differs from preserved original only by node 0 scale `[0.1,0.1,0.1]` and the documented breakout_repair metadata. Removing those yields identical parsed JSON. This matches the documented 10x scale repair in PRISON_ARCHITECTURE_VALIDATION.md and architecture_repairs.json. Preserve original/repair evidence; update stale canonical checksum in a separately authorized manifest maintenance step if desired. No redownload is necessary.

## New downloads independently verified

`asset_library/manifests/acquisition_20261019/props_materials_inventory.json`:

| Asset | Actual file checks | Licence evidence | Scope |
|---|---|---|---|
| ACQ26_SIGNAL_FLASHLIGHT | Five listed source files exist; exact size and SHA-256 match; all glTF image/buffer references resolve; JPEGs decode | Local official Poly Haven licence policy HTML exists and states CC0 | Static vintage signal flashlight, not a watchtower searchlight or modern tactical torch |
| ACQ26_FABRIC030 | Twelve listed archive/extracted files exist; exact size and SHA-256 match; 11-entry ZIP CRC test returns no error; paths have no absolute/traversal entries; images decode | Local official ambientCG licence policy HTML exists and states CC0 | Realistic woven PBR maps, not linen-stack geometry |

Source originals/archives were preserved. Acquisition hashes cover real files, not website listings. No current evidence establishes skinning, animations or full mission completion for either asset. Conversion, shader scale and scene integration remain separate checks.

## Limitations and acceptance

No Chapter 1 mission is asset-complete. Realistic prison bus interior/body scanner/watchtower, bespoke press/relay interactions, hero likeness/facial performance, synchronized restraint/contact performances, final environment assembly and collision/navigation remain required according to project gaps. Sketchfab candidate metadata and login-gated downloads do not count as acquisition. Final AAA visual quality requires representative in-game lighting, character/prop contacts, LOD/performance and split-screen review.

## Facial derivative review

Independent binary parser and SHA-256 checks PASS for all six animated GLBs in `asset_library/converted/acquisition_20261019/rocketbox_facial/animated/`: Adrian, Noah, Rusk, Mara, Silas and prisoner NPC. Each matches the Blender reload report's exact size/hash, has valid GLB v2 header/length, 80 skin joints, 37 animation arrays, 175 morph targets on the body, and embedded images. Existing Microsoft MIT notice is present and was read. These are conversions of previously acquired sources, not six new downloads.

Reviewed final Godot report records six PASS loads, skin present and 175 body blendshapes each. This reviewer inspected its evidence rather than independently launching another Godot import. Conversion worker reports fallback UID warnings; no warning-free claim. Independent visual inspection of Adrian JawOpen render confirms open mouth and intact head but also visible layered hair transparency. Other poses, in-game GPU playback, synchronized actions and lip sync remain unverified. Exported facial controls improve the prior gap, but facial acting and likeness remain incomplete.

The actual flashlight Blender render was independently viewed: detailed chipped green paint, leather loop and visible lettering, suitable as a vintage worn signal device candidate. It does not solve modern guard torch/searchlight requirements. Grip, branding and in-game emitter still need review.

## Radio evaluation — reject for current realistic asset gate

`radio_inventory.json`: original 411,489-byte ZIP and three extracted files independently match recorded sizes/SHA-256; ZIP CRC PASS. Contents are OBJ, MTL and creator URL only. MTL contains eight flat Phong materials and no texture-map references; there are no texture images. The acquired radio fails the requested textured realistic material gate and should remain an evaluation download, not an accepted guard-radio replacement. No actual radio render was performed by this reviewer.

Current preserved creator product page explicitly labels the asset CC0, and the March 3, 2026 update is titled Now CC0 license. Preserved general terms simultaneously require attribution and prohibit standalone redistribution. Record that tension instead of certifying unrestricted raw redistribution from a generic CC0 label. Art rejection does not require resolving these terms; preserve all three pages with evaluation files.

## Five additional 2k material sets

Independent checks PASS for all 20 files listed in materials_2k_inventory.json: concrete_wall_001, concrete_floor_worn_001, rusty_painted_metal, painted_concrete and denim_fabric, four maps each. Exact sizes and SHA-256 match; all JPEGs decode at 2048x2048. Existing lower-resolution assets remain present. The shared preserved Poly Haven policy supplies CC0 evidence. These are usable texture source candidates; physical UV scale, shader channel binding, scene appearance and Godot checks remain separate acceptance items. This reviewer has not certified new material sphere renders.

Update: independently viewed materials_actual_render_sheet.jpg. All six spheres show mapped surface detail: woven cloth, denim, concrete wall/floor, chipped paint and painted metal. Sphere preview passes basic texture appearance; it does not verify final mesh UV scale or game lighting.

## Authenticated Sketchfab acquisitions — intermediate audit

Both records in sketchfab_inventory.json independently PASS archive size/hash, ZIP CRC and safe paths; every extracted file matches its exact archive member bytes. Laundry's separately downloaded 5,318,444-byte GLB also matches its recorded SHA-256. These are actual acquired files.

Licence evidence issue found: both `*_official.html` files under licenses/acquisition_20261019/sketchfab were zero bytes at review time, despite `official_html: SAVED`. CREDITS.md provides attribution and CC-BY-4.0 links; official web research corroborates CC Attribution labels, but zero-byte evidence files are not an adequate saved source record. Root was notified to preserve actual browser/API evidence. Conversion/render/import acceptance pending.

## Resumed independent QA — official licence evidence and Sketchfab conversion

Saved public official metadata from `https://api.sketchfab.com/v3/models/fd699067fdcc41d7b0475ca575de95d4` and `https://api.sketchfab.com/v3/models/9716a3b43fa54cf282706601526b7f73` in the corresponding nonzero `*_official_api.json` files under `asset_library/licenses/acquisition_20261019/sketchfab/`. Both identify the recorded creators and CC Attribution, link CC-BY-4.0, and explicitly state commercial use is allowed with author credit. These records repair the evidence gap; the zero-byte HTML files remain unusable evidence. Preserve attribution and indicate derivative changes.

Independently viewed `simple_handcuffs_actual.png`: detailed worn silver cuffs, chain and keys appear intact. This is a static textured prop candidate. The Blender report records no actions and approximately 4.48 x 5.99 metre bounds: scale must be measured/corrected before use, and locking/restraint/contact performances remain absent. Converted file hashes must follow the final conversion report.

Independently viewed `industrial_dryer_ironing_actual.png`: model occupies a tiny central area inside a large backdrop; this image is insufficient for detailed material/geometry acceptance. Request a tighter representative view. Godot log records successful import completion for both GLBs, but this reviewer has not independently rerun the engine or certified runtime interaction.

Consolidated inventory script at review time omitted `materials_2k_inventory.json` and `sketchfab_inventory.json`; root was notified to include these records and subsequent tower/radio acquisitions before delivery. Separate manifests remain the acquisition authority until rebuilt. No complete or AAA production-ready claim is supported.

## Guard tower and replacement radio — actual-file QA

Official metadata snapshots for model `963071f5fe404970a40b166bcee430b8` by Lex713 and `aff7fc139e114b96ab81834c1ad04670` by Origamix are preserved as `guard_tower_official_api.json` and `radio_yaesu_vx8_official_api.json`. Both explicitly allow commercial use under CC-BY-4.0 with creator credit. Brand/trademark appearance in the Yaesu radio is not itself licensed by a CC copyright grant; review product branding for the intended game presentation.

Independent file checks: tower source ZIP in Downloads is 4,604,274 bytes, nine entries, CRC PASS and no absolute/traversal paths. Tower official GLB is 4,214,148 bytes, SHA-256 `96b4ac7dabe976c9f4af634054a955898b97743bdc38d11d2220e3dde924394a`; Yaesu official GLB is 55,817,224 bytes, SHA-256 `719788e88ddea03b1b3b5006c6b746f087fe0ac2ebea22d488a4f3e8882c39ad`. Both have valid GLB v2 header/declared length and embedded images (four and seven respectively), with no external image URIs.

Tower converted GLB independently checked at 4,137,664 bytes, SHA-256 `5c836137f2eb27962275a58688549473b1d4a8845c8448d05502e77ac750c9f8`, valid GLB v2, four embedded images. Viewed `guard_tower_actual.png`: coherent realistic industrial tower, stairs/railings, worn concrete supports, booth, metal platform and light. Basic static appearance passes; player clearance, collision, navigation, LODs, real-world dimensions and spotlight operation are not established by this render.

## Final radio derivative review

Independently checked the original Yaesu GLB, all seven extracted texture PNGs and the single-radio metric derivative: every byte size and SHA-256 matches `yaesu_inventory.json` / `yaesu_blender_validation.json`. The derivative is 54,449,788 bytes, SHA-256 `0475a1053391dcb54395817f3701c11298929e69b8bbfaf74c311ef191c93a98`. Original authoring archive was not acquired; the record accurately states provider-converted GLB only. Nonzero official metadata, CC-BY-4.0 licence page and attribution text are preserved in the radio licence folder.

Independently viewed `yaesu_actual_front.png`: coherent realistic handheld radio, textured controls, worn edges, visible screen and branding. Basic static appearance passes. Blender records zero armatures/actions; grip/holster attachment, operation, performance/LOD and final game lighting remain unverified. This visual acceptance applies to Yaesu only; the earlier untextured CC0 radio remains rejected for the realistic asset gate.

## Final consolidated inventory and engine evidence

Final `inventory.json` contains 849 records (831 baseline plus 18 session records, including six facial derivatives and one rejected evaluation). Independent schema inspection found all 21 requested inventory field keys present in every record. Historical unknown values remain explicitly unknown; field presence is not historical provenance verification. The rejected untextured radio is explicitly NOT CLEARED and REJECTED in the inventory/checkpoint, and is not staged for runtime.

Independently rehashed all 88 paths listed in `final_file_checks.json`: zero missing files and zero SHA-256 mismatches. Independently checked all four entries in `runtime_staging.json`: runtime size and SHA-256 match their listed source derivative for handcuffs, laundry equipment, guard tower and Yaesu radio. These are static candidates; staging does not certify main-scene integration.

Read final isolated Godot 4.7.2 `material_validation/godot_report.json`: `failed: false`, eight loaded resources, six 2k PBR materials with albedo/normal/roughness/AO, and flashlight/radio with zero null material assignments. This reviewer inspected the engine evidence without launching another engine. Fabric is correctly nonmetallic; packed metallic bindings on the other sets do not establish physical surface correctness by themselves. Final rendered game scenes, physical texture scale, actor contacts, collision/navigation, LODs and split-screen performance remain open. No mission-complete or AAA production-ready claim is supported by these checks.
