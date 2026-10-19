# Chapter 1 acquisition and readiness — 19 October 2026

Actual files are preserved in this project. This report supplements the historical Phase 01.5 reports; it does not certify AAA quality or complete acquisition.

## Inventory and evidence

Consolidated inventory: 863 records (32 session records, including rejected evaluation material and six derivatives of existing character sources). Counts are records, not production-ready assets. See [inventory.csv](../../asset_library/manifests/acquisition_20261019/inventory.csv) and [inventory.json](../../asset_library/manifests/acquisition_20261019/inventory.json).

All 22 original missing bundles were reconciled individually: [bundle reconciliation](../../asset_library/manifests/acquisition_20261019/BUNDLE_RECONCILIATION.md). Baseline check: 831 records, 984 unique runtime paths, zero missing files; one stale shelf hash is explained by the previous scale repair/newline serialization. Current hashes are recorded without erasing historical evidence.

## Session assets

| ID | Source/category | Licence | Current validation |
|---|---|---|---|
| ACQ26_SIGNAL_FLASHLIGHT | Signal Flashlight / props | CC0-1.0 | PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED |
| ACQ26_FABRIC030 | Grey woven cloth PBR / materials | CC0-1.0 | PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED |
| ACQ26_2K_CONCRETE_WALL_001 | Concrete Wall 001 / materials | CC0-1.0 | PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED |
| ACQ26_2K_CONCRETE_FLOOR_WORN_001 | Concrete Floor Worn 001 / materials | CC0-1.0 | PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED |
| ACQ26_2K_RUSTY_PAINTED_METAL | Rusty Painted Metal / materials | CC0-1.0 | PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED |
| ACQ26_2K_PAINTED_CONCRETE | Painted Concrete / materials | CC0-1.0 | PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED |
| ACQ26_2K_DENIM_FABRIC | Denim Fabric / materials | CC0-1.0 | PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED |
| ACQ26_RADIO_EVALUATION | VerzatileDev Walkie Talkie / props | CC0 claim on current creator page and dated March 2026 update; review preserved terms | NOT TESTED |
| SF_SIMPLE_HANDCUFFS | simple_handcuffs / props | CC-BY-4.0 | {'load': 'PASS', 'meshes': 2, 'null_materials': 0} |
| SF_INDUSTRIAL_DRYER_IRONING | industrial_dryer_ironing / props | CC-BY-4.0 | {'load': 'PASS', 'meshes': 11, 'null_materials': 0} |
| SF_GUARD_TOWER | guard_tower / architecture | CC-BY-4.0 | {'load': 'PASS', 'meshes': 12, 'null_materials': 0} |
| ACQ26_YAESU_RADIO | Radio Yaesu VX-8 / props | CC-BY-4.0 | PASS isolated Godot 4.7.2 load/instantiate; rendered gameplay NOT TESTED |
| MIXAMO_CLOSING | Closing / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_KNEELING_DOWN | Kneeling Down / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_KNEELING_INSPECTING | Kneeling Inspecting / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_OPEN_DOOR_OUTWARDS | Open Door Outwards / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_OPENING_DOOR_INWARDS | Opening Door Inwards / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_POINTING_FORWARD | Pointing Forward / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_PULL_HEAVY_OBJECT_START | Pull Heavy Object Start / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_PULL_HEAVY_OBJECT_STOP | Pull Heavy Object Stop / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_PULL_HEAVY_OBJECT | Pull Heavy Object / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_PULLING_LEVER | Pulling Lever / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_STANDING_ARGUING | Standing Arguing / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_TALKING | Talking / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_UNARMED_TURN_LEFT_90 | Unarmed Turn Left 90 / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| MIXAMO_UNARMED_TURN_RIGHT_90 | Unarmed Turn Right 90 / animations | Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved | Godot4.7.2 headless imported and instantiated; animation tracks present |
| FACIAL_20261019_RB_ADRIAN_CROSS | rb_adrian_cross facial derivative / characters | MIT | PASS in isolated Godot 4.7.2 project; UID fallback warnings |
| FACIAL_20261019_RB_MARA_SEN | rb_mara_sen facial derivative / characters | MIT | PASS in isolated Godot 4.7.2 project; UID fallback warnings |
| FACIAL_20261019_RB_NOAH_REYES | rb_noah_reyes facial derivative / characters | MIT | PASS in isolated Godot 4.7.2 project; UID fallback warnings |
| FACIAL_20261019_RB_PRISONER_NPC | rb_prisoner_npc facial derivative / characters | MIT | PASS in isolated Godot 4.7.2 project; UID fallback warnings |
| FACIAL_20261019_RB_SILAS_BELL | rb_silas_bell facial derivative / characters | MIT | PASS in isolated Godot 4.7.2 project; UID fallback warnings |
| FACIAL_20261019_RB_TOMAS_RUSK | rb_tomas_rusk facial derivative / characters | MIT | PASS in isolated Godot 4.7.2 project; UID fallback warnings |

Downloads comprise six PBR material sets (one new woven fabric, five 2k upgrades), a vintage signal flashlight, and the acquired Sketchfab props/environment candidates as recorded above. The simple itch radio is rejected: no texture maps and inconsistent generic licence terms. Six Rocketbox facial GLBs are conversions of existing licensed files, not six new downloads.

Original archives remain under asset_library/original_downloads; safe extracted sources, converted candidates, licences and manifests use dated acquisition_20261019 folders. Source ZIP CRC, file hashes, image decoding, texture dependencies and scoped Blender/Godot checks are in the linked JSON and worker reports. No payment or protection bypass was used.

## Mission coverage

Every mission retains a PARTIAL functional asset verdict and NOT READY production verdict. Existing rigged characters and 37 baseline clips are historical validated candidates; this session converted facial channels on six identities (175 targets, 80 bones, 37 body actions), but did not produce facial performances or prove new contact animation.

| Mission | Required characters | Environments | Existing/new candidate props | Missing critical presentation or validation |
|---|---|---|---|---|
| M01 New Blood | Adrian, Noah, Rusk, guard, inmates | Intake, cellblock | Photo, badge, clipboard, bars, lockers, beds; cuffs candidate | Body scanner, realistic prison bus exterior/interior, hero likeness/garments, search/photo/escort contacts |
| M02 Trouble in the Yard | Adrian, Noah, Rusk, Silas, guards, inmates | Yard | Fence, ball, bench, tap; realistic tower candidate | Court/tray return, crowd variants, mediation/ball-roll contacts, tower collision/light and scene review |
| M03 The Workshop | Adrian, Noah, Rusk, Mara, guards, inmates | Laundry workshop | Diagram, shim, lamp; textured dryer/ironing candidate and linen PBR | Mission press lever/removable screen contacts, linen-stack meshes, exact uniforms/likeness, room assembly |
| M04 Lights Out | Adrian, Noah, Rusk, guards | Cellblock, maintenance | Shim, hatch, gates, pipes, ducts | Shared rear chase, brace/hatch handoff, shim finger contacts, patrol turns, assembled lighting/collision/nav |
| M05 Behind the Walls | Adrian, Noah | Maintenance | Selector, brake, wired handsets, grille, pump, ledger, dual door | Aligned selector/brake/handset/handle actions, readable ledger/indicators, mechanisms and route validation |
| M06 The Betrayal | Adrian, Noah, Rusk, two guards | Maintenance capture bay, solitary | Dual handles, grille, beacon, cuffs candidate, pipe | Articulated cuffing/kneel/escort, forearm contact, facial acting/VO, capture/solitary set and readable props |

For exact existing asset IDs, priorities, verified-versus-proxy distinction and dependencies see [historical coverage matrix](ASSET_COVERAGE_MATRIX.md). Newly acquired static props only fill their subcomponent; they do not replace an entire environment or interaction. Baseline locomotion exists; door-specific, pull, turn-in-place, restrained escort, synchronized two-person contacts and cinematic/facial takes remain incomplete. Optional combat/sprint/vault requests in the broad brief are not all canonical Chapter 1 requirements; no unrelated pack was acquired to inflate coverage.

## Conversion and compatibility

Blender 5.1.1 and Godot 4.7.2 are installed and were used. [Facial conversion](../../asset_library/converted/acquisition_20261019/rocketbox_facial/CONVERSION_REPORT.md) and [Sketchfab conversion](../../asset_library/manifests/acquisition_20261019/SKETCHFAB_CONVERSION_REPORT.md) describe actual checks and defects. New facial GLBs retain hair transparency artefacts and need body motion replay/visemes in the game. Static props have no functional rigs or interactions. Scale adjustments are provisional. Godot resource import does not prove collisions, navigation, LODs, split-screen performance or final appearance.

Materials include real albedo, normal and roughness maps; packed ARM is documented. Most new material maps are 2048 square; cuffs use 4096 maps, tower converted textures are 1024 despite the source page advertising 2048. UV scale, close-up density, hardware memory and final lighting are not calibrated. No texture-resolution label establishes AAA quality.

## Remaining acquisition blockers

- Realistic prison transport bus with usable interior and commercial provenance. Existing stylized bus is rejected for final art.
- Present-day body/security scanner. Researched noncommercial assets were rejected; paid option requires owner purchase approval.
- Additional believable guard/inmate identities, exact named-character likeness, layered prison clothing and authored scar/age/hair details.
- Story-specific synchronized body and hand contacts, restrained walking/cuffing, gestures, facial acting and VO. Mixamo is a separate Adobe login gate; generic clips still require retargeting and contact tests.
- Mission-specific press/interlock, selector/brake/grille mechanisms, readable evidence graphics and environmental assembly. These require asset authoring and integration.
- Original VO/PA/radio speech, score, listening review, UI/VFX accessibility and runtime performance remain tracked in prior blockers.

## Phase 02 recommendation

| Use | Verdict |
|---|---|
| Core gameplay programming with existing candidate cast/modules | PASS to continue prototyping; asset-critical presentation is incomplete |
| New static prop/material placement trials | PARTIAL; use validated derivatives with attribution and scale review |
| Realistic character gameplay | PARTIAL; likeness, hair/materials and contact actions unfinished |
| Chapter 1 final level art | PARTIAL; major intake pieces and assembly missing |
| Cinematic production | BLOCKED by authored contacts, facial acting and voice |
| Final AAA visual polish / mission asset-complete claim | BLOCKED |

Independent review: [QA report](acquisition_20261019_QA.md). Research: [legal candidates and rejections](../assets/acquisition_20261019_RESEARCH.md). Resume using [checkpoint](../../asset_library/manifests/acquisition_20261019/checkpoint.json), not a fresh download pass.

## Authenticated animation follow-up

14 targeted Mixamo FBX motions are now downloaded and preserved, replacing the previous Adobe-login acquisition blocker. These include inward/outward door opening, cabinet closing, left/right 90-degree turns, lever pull, heavy pull start/loop/stop, kneeling/inspection, conversation, arguing and pointing. Cabinet closing is not a validated prison-door contact clip. Generic kneeling is not synchronized arrest/restraint choreography.

[Animation acquisition/conversion report](MIXAMO_20261019_REPORT.md) and [independent animation QA](MIXAMO_20261019_QA.md) govern current compatibility. Raw Mixamo source files are internal commercial-game dependencies, not CC0 assets for public redistribution. Source downloads and structural import do not establish contact choreography or production-ready hero motion.

A more detailed textured transit-bus interior candidate was found on BlendSwap: [architecture follow-up](../assets/followup_20261019_ARCHITECTURE_RESEARCH.md). Owner sign-in is required before its files can be acquired. It would still require prison conversion; no bus model from that source has been downloaded.

Final static material/resource evidence: [engine validation](../../asset_library/manifests/acquisition_20261019/ENGINE_VALIDATION_REPORT.md). New static-asset credits: [attributions](../../asset_library/licenses/acquisition_20261019/ATTRIBUTIONS.md).
