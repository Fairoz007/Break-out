# Asset manifest — Phase 01.5

[Machine-readable authority](asset_library/manifests/assets.json): **831 records**. That is 28 Phase 01 records (6 acquired, 22 requirement bundles) plus 803 Phase 01.5 catalogue records. **772 are usable**: they load in Godot 4.7.2 and pass file, licence and checksum checks. 25 audio candidates are REJECTED, 4 MPFB characters FAILED and 2 diagnostic proxies are SUPERSEDED. Godot: 908/908 resource jobs load (the job count includes texture and bin dependencies). A material set counts as one asset; texture channels, source/runtime copies and the 37 clips embedded per character are not counted separately.

| Category | Records | Usable |
|---|---:|---:|
| animations | 4 | 4 |
| audio | 621 | 596 |
| character_prototypes | 2 | 0 |
| characters | 17 | 13 |
| environment | 20 | 20 |
| material | 19 | 19 |
| prop | 103 | 103 |
| texture | 1 | 1 |
| ui | 14 | 14 |
| vfx | 2 | 2 |

## The 22 original requirement bundles

**Functional** = a usable asset covers the need now (realistic, construction-grade or proxy). **Production** = the intended realistic/cinematic standard. A functional proxy never closes a production requirement.

| Bundle | Priority | Functional | Production | Children (usable/total) | Godot | Licence | Missions | Remaining |
|---|---|---|---|---|---|---|---|---|
| `CHAR_ADRIAN` | CRITICAL | FUNCTIONAL | PARTIAL | 2/4 | VERIFIED | VERIFIED | M01, M02, M03, M04, M05, M06 | Facial blendshapes not exported; art-direction likeness approval; overshirt is a recoloured sweater (no layered garment); grey temple/eyebrow cut not authored; calibrated roughness from specular; close-up lighting review. |
| `CHAR_NOAH` | CRITICAL | FUNCTIONAL | PARTIAL | 2/4 | VERIFIED | VERIFIED | M01, M02, M03, M04, M05, M06 | Facial blendshapes not exported; likeness approval (skin darker than brief, hair not wavy); wrist burn not authored; recoloured jacket stands in for undershirt; photo-in-shirt contact. |
| `CHAR_RUSK` | CRITICAL | FUNCTIONAL | PARTIAL | 2/2 | VERIFIED | VERIFIED | M01, M02, M03, M04, M06 | Average (not heavy) build; radio/keys/wedding band props; shares the only realistic guard identity with CHAR_GUARD. |
| `CHAR_MARA` | CRITICAL | FUNCTIONAL | PARTIAL | 2/2 | VERIFIED | VERIFIED | M03 | Likeness mismatch: avatar is younger with dark hair (brief: 46, silver-streaked); cardigan and inspector badge missing. |
| `CHAR_SILAS` | CRITICAL | FUNCTIONAL | PARTIAL | 2/2 | VERIFIED | VERIFIED | M02 | Uniform patches and chipped incisor not authored; facial performance. |
| `CHAR_GUARD` | CRITICAL | FUNCTIONAL | PARTIAL | 2/2 | VERIFIED | VERIFIED | M01, M02, M03, M04, M05, M06 | Only one realistic guard identity (shared with Rusk); radio/restraints props; more variants needed for crowds. |
| `CHAR_INMATE` | CRITICAL | FUNCTIONAL | PARTIAL | 3/3 | VERIFIED | VERIFIED | M01, M02, M03 | Two realistic inmate identities; crowd variation and seated/working variants beyond shared clips. |
| `PROP_PHOTO` | IMPORTANT | FUNCTIONAL_PROXY | PARTIAL | 2/2 | VERIFIED | VERIFIED | M01, M02, M06 | Hand contact and close-up art direction. |
| `PROP_VANTAGE_BADGE` | IMPORTANT | FUNCTIONAL_PROXY | PARTIAL | 1/1 | VERIFIED | VERIFIED | M01, M06 | Close-up legibility/art direction. |
| `PROP_DIAGRAM` | IMPORTANT | FUNCTIONAL_PROXY | PARTIAL | 1/1 | VERIFIED | VERIFIED | M03 | Half-screen readability at authored camera. |
| `PROP_SHIM` | IMPORTANT | FUNCTIONAL_PROXY | PARTIAL | 1/1 | VERIFIED | VERIFIED | M03, M04, M05, M06 | Grip/contact and cinematic silhouette. |
| `PROP_RELAY` | IMPORTANT | FUNCTIONAL_PROXY | PARTIAL | 5/5 | VERIFIED | VERIFIED | M05 | Selector lamp states, brake wheel pivot and interlock motion; grille drive animation untested. |
| `PROP_LEDGER` | IMPORTANT | PARTIAL | BLOCKED | 1/1 | VERIFIED | VERIFIED | M01, M06 | Readable close-up evidence page and later full VANTAGE ledger. |
| `ENV_INTAKE` | CRITICAL | PARTIAL | BLOCKED | 10/10 | VERIFIED | VERIFIED | M01 | Bus is a stylised exterior blockout (no interior); body scanner missing; realistic prison gate; assembled route and collision/nav. |
| `ENV_CELLBLOCK` | CRITICAL | PARTIAL | BLOCKED | 21/21 | VERIFIED | VERIFIED | M01, M04, M06 | Two-level assembled gallery, solitary annex, clinic envelope, hinge-pivot door motion, collision/nav. |
| `ENV_YARD` | CRITICAL | PARTIAL | BLOCKED | 10/10 | VERIFIED | VERIFIED | M02 | Watchtowers are stylised/medieval (blockout only); court markings and tray return missing; searchlight asset is a hand lantern; CC-BY hoop needs credit. |
| `ENV_WORKSHOP` | CRITICAL | PARTIAL | PARTIAL | 12/12 | VERIFIED | VERIFIED | M03 | Linen stacks/detail, ducts placement, assembled room and collision/nav; machines are simplified originals. |
| `ENV_MAINTENANCE` | CRITICAL | PARTIAL | BLOCKED | 15/15 | VERIFIED | VERIFIED | M04, M05, M06 | Crawlspace/service trench modules, cable trays, capture bay assembly, collision/nav; grille drive motion untested. |
| `ANIM_HUMANOID` | CRITICAL | PARTIAL | BLOCKED | 8/8 | VERIFIED | VERIFIED | M01, M02, M03, M04, M05, M06 | 37 clips render correctly on realistic Rocketbox and UBC rigs (Blender + Godot); baseline locomotion/crouch/jump/interact/push/climb/pick-up/repair verified. Missing: turn-in-place, pull, door-specific, paired assisted climb/help-up, synchronized two-body contacts, restrained walk, facial/dialogue performance, cinematic takes; foot sliding/root motion untested. |
| `AUDIO_PRISON` | IMPORTANT | PARTIAL | BLOCKED | 596/596 | VERIFIED | VERIFIED | M01, M02, M03, M04, M05, M06 | Original VO, PA speech, crowd walla (only shouting crowd), diesel bus engine, radio speech and score missing; nothing has been listened to; mix review outstanding. |
| `UI_SUBTITLES` | IMPORTANT | PARTIAL | PARTIAL | 14/14 | VERIFIED | VERIFIED | M01, M02, M03, M04, M05, M06 | Half-screen/localized layout, accessibility and prompt composition untested. |
| `VFX_ALARM` | IMPORTANT | PARTIAL | BLOCKED | 2/2 | VERIFIED | VERIFIED | M04, M05, M06 | Beacon light rig and particle emitter appearance in scene untested. |

Totals: functional {'FUNCTIONAL': 7, 'FUNCTIONAL_PROXY': 5, 'PARTIAL': 10}; production {'PARTIAL': 14, 'BLOCKED': 8}.

Exact child IDs, paths, checksums and scoped evidence are in each bundle record (`child_asset_ids`). See also: [coverage matrix](docs/qa/ASSET_COVERAGE_MATRIX.md) · [Phase 01.5 report](docs/qa/PHASE_01_5_REPORT.md) · [validation](docs/assets/ASSET_VALIDATION_REPORT.md) · [licences](docs/assets/ASSET_LICENSES.md) · [discovery](docs/assets/PHASE15_DISCOVERY.md).
