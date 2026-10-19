# Phase 01.5 independent asset review

Reviewer: independent asset QA agent. Date: 18 October 2026. Status: **IN PROGRESS — asset readiness not approved**.

This review distinguishes file/import evidence from rendered appearance, animation deformation, scene suitability, collision and navigation. None implies the others. No gameplay systems were implemented by this reviewer.

## Evidence and checks

- Independently recomputed SHA256 for all 51 entries in `asset_library/manifests/phase15/baseline_hashes.json`: no missing or modified protected files at initial review.
- Read actual architecture, bulk asset and UI manifest fragments, original licensing records and animation requirements.
- Visually inspected `asset_library/extracted_sources/phase15_architecture/qa_contact_sheet.png`: 12 representative architecture/prop samples. Authored substitutes are recognizable and textured, but repetitive rust and simple surfaces do not establish intended cinematic realism. Remaining modules were not visually inspected at this stage. Collision, snapping and navigation require separate evidence.
- Visually inspected `asset_library/manifests/phase15_characters_previews/Walk_Loop_12.png`: the current character is skin-colored with no visible uniform, in an A-like pose with seam/artifact spots near throat and torso. This render cannot establish acceptable clothing or locomotion deformation. Character build log contains armature parenting and influence truncation warnings. Repair requested.
- Bulk decode report separates waveform decoding from listening (`NOT TESTED`). A successful decode is not an audition or mission sound match.

## Review cycles and issues

| ID | Severity | Owner | Finding / acceptance evidence | State |
|---|---|---|---|---|
| QA15-001 | Major | Architecture/coordinator | Contact sheet contains Elena photo while architecture license denied portraits. Coordinator supplied original AI image provenance and corrected architecture license. Need final path/link audit. | Corrected, final recheck pending |
| QA15-002 | Critical | Character/animation engineer | Current character preview does not demonstrate clothed, deforming protagonist. Re-render actual exported GLB at clearly distinct walk/crouch extremes on both protagonists; verify material assignment, skeleton skin binding and contact/foot behavior. | Repair requested; remains blocker |
| QA15-003 | Major | Bulk/coordinator | Intermediate bulk fragment listed deleted/deduplicated audio paths. Final merged manifest must exclude nonexistent runtime records and update checksums for attenuated replacements. Initial array hash comparison was a reviewer scalar-handling limitation; arrays require per-path comparison, not a corruption finding. | Final audit pending |
| QA15-004 | Major | Architecture/pipeline | Procedural modular dimensions/export checks do not establish assembled scene snapping, collision or navigation. Retain PARTIALLY_VERIFIED and name untested criteria. | Open documented limitation |
| QA15-005 | Major | Audio/coordinator | Technical audio decoding and quantity do not supply dialogue/score or prove prison ambience, radio, weather, machinery and alarm coverage. Scene audition/mix remains required; oversized audio packs must not inflate mission readiness. | Open documented limitation |

Up to five repair cycles are allowed; this is cycle 1. No asset bundle is approved solely by record count. A library count must distinguish unique runtime assets from texture channel files, source/runtime duplicates, same-content variants and archive members. The user requested 500–1000 assets; count fulfillment does not substitute for critical mission coverage.

Final merged-manifest, Godot-import, character repair and mission matrix review is pending coordinator integration.

## Resumed independent verification

Recomputed all 51 protected baseline hashes again after continuation: zero missing or modified files. Independently checked 691 records across architecture, Poly Haven props, bulk materials/audio, OpenGameArt audio and UI fragments: 1,460 original/runtime SHA256 comparisons and recorded license paths, zero mismatches or missing paths at this snapshot. Final audio repair may change runtime hashes and requires another check. These are integrity checks, not visual or mission approval.

The photo provenance correction is accepted: architecture licensing now links the actual original AI image record. Final merged manifest, repaired character renders, Godot import report and mission coverage matrix remain pending. Status remains IN PROGRESS; critical character and animation acceptance remains open.

### Character repair review cycle 2

Independently viewed the refreshed REST_0, Walk_Loop_12 and Crouch_Idle_Loop_8 PNGs generated around 21:47–21:48 local file timestamps. Motion is now visible, but the images show skin-colored bodies without usable uniforms, severe shoulder/upper-arm collapse, and distorted torso/limbs. REST_0 is itself highly posed rather than a neutral bind-pose demonstration. Crouch has protruding geometry near the upper back. These images fail production character appearance and deformation acceptance; skeleton presence and clip counts cannot override visible defects. QA15-002 remains CRITICAL and repair feedback was sent to the responsible engineer and coordinator. These observations apply to this render snapshot; any subsequent replacement requires fresh inspection.

### Import repair and engine review cycle 3

The coordinator repaired ADPCM WAV compatibility and restored 60 corrupt extracted PNG importer derivatives from their unchanged GLB embedded image bufferViews. Independently recomputed all 60 restored PNG hashes against `asset_library/manifests/phase15/extracted_texture_repairs.json`: zero mismatches. Final import stderr is empty. Read final `asset_library/manifests/phase15/godot_validation.json`: 773 resource jobs report successful loading (68 PackedScenes, 594 audio resources, 88 textures, 20 StandardMaterial3D resources, one font, one particle material and one style). No recorded geometry null-material or resource error was found. Job count includes dependencies and is not an independent asset count.

Actually inspected Godot preview PNGs for P15_WALL_4M, P15_LAUNDRY_WASHER, P15_CCTV_CAMERA, PH15_ADJUSTABLE_WRENCH_DEP0, PH15_MODULAR_CHAINLINK_FENCE_DEP0 and MAT_P15_ANTI_SLIP_CONCRETE. These samples show working rendering and textures; original washer/CCTV remain simplified construction art. Poly Haven wrench/fence samples show the expected textured subjects. This limited visual sample does not approve all assets, cinematic realism, collisions, navigation, audio audition or scene-specific suitability.

### Additional character repair evidence

Independently viewed `cycle4_native_8.png` and `cycle4_clothes_only.png` (21:52–21:53). Upper arms remain collapsed/missing, forearms attach incorrectly, and clothing-only rendering confirms orange cloth exists but is occluded by the body in the combined render. Character readiness remains FAILED/BLOCKED. These images support no retargeting approval.

### Fifth and final character repair cycle

Viewed `cycle5_native_8.png`: intact arms and painted orange/gray body regions are an improvement, but the arms remain spread in a rigid A-like pose and painted body regions do not demonstrate fitted uniform geometry or realistic cloth. This is an original sine-walk proxy, not successful Quaternius retargeting. The experimental GLB is retained outside runtime under converted/cycle5. Five allowed character repair cycles are exhausted; QA15-002 remains a documented critical blocker. This prototype is not counted as an accepted protagonist or baseline locomotion set.

## Final independent review (resumed Phase 01.5)

Agent F, 2026-10-18. Read-only: Godot and Blender were not run, and no asset, manifest or tool was modified. The machine-readable findings (26 items) are in `asset_library/manifests/phase15/independent_qa_final.json`.

**Integrity (exhaustive).** assets.json has 831 records with no duplicate IDs. Every runtime file exists. All 962 hashed runtime files were recomputed (748 single-file records plus every path in the 44 dict checksums), with 0 mismatches. No REJECTED, FAILED or SUPERSEDED record is usable, and no record claims VERIFIED. godot_validation.json has 908/908 jobs at load VERIFIED and 0 null materials. Every usable record's runtime paths are covered, no covered file is newer than the report, and the import md5 caches are current (886 checked). godot_character_report.json: 13 characters VERIFIED, 37 clips each, all 364 shot PNGs present. All 24 architecture repairs match their before/backup and after/current hashes, the manifest checksums and the Godot triangle counts. Licences: the Rocketbox MIT text is present, the CC BY 3.0 credit for Ouren's hoop/rack/ball is in THIRD_PARTY_NOTICES.md, and the Poly Haven, Quaternius and OGA CC0 evidence pages exist. In a seeded 20-record audio sample, 20/20 passed (file, hash, Godot, licence). The audit's 25 rejected clips are exactly the manifest REJECTED set.

**Rejected claims.**
- QAF-24 (MAJOR): the coverage matrix gives every mission "Functional (critical assets): FUNCTIONAL" although each mission has CRITICAL bundles with Functional=PARTIAL: ANIM_HUMANOID, every ENV_* bundle and PROP_LEDGER (M05). Row-level IDs, statuses and child counts all match assets.json.
- QAF-07 (MAJOR): the Rocketbox engine_bounds/bounds give a size of about 0.003 x 0.018 x 0.014 m (a skinned-AABB defect), which contradicts the 1.67-1.84 m heights. The scene renders show human scale, but the recorded metric is wrong.
- QAF-16 (MINOR): zoneA_origins.png is a camera-inside-wall frame and carries no origin evidence.
- QAF-21 (MINOR): AUDIO_MATERIALS_AUDIT.md is stale. Crowd and coastal wind are now covered by 27 later, unaudited DISC15 clips, and AUDIO_FOLEY is no longer NOT TESTED.

**Characters, as viewed.** I viewed the Rocketbox sheets (Adrian, Noah, Mara, Rusk), the Godot sheets, the all-clips sheet, the close-ups, the UBC Adrian/Mara sheets, the heads sheet and zone D. The Rocketbox avatars are realistic, clothed, and show no severe deformation or clipping at thumbnail scale. Hands, faces and cloth intersection cannot be judged at that size, and there are no head close-ups for the chosen Adrian, Noah, Silas or inmate meshes. The Fixing_Kneeling foot bone drops 8-12 cm (Rocketbox), so floor contact is unproven. The Noah jacket hem shows recolour bleed. The UBC characters are stylised bodysuit proxies, as disclosed. Mara's "darker cardigan" is barely distinguishable.

**Other.** Rejected, failed and superseded files remain under res://assets (export risk). 55 usable records lack a runtime_checksum, and 222 extracted textures are unmanifested. The guard tower is usable=true despite its "NOT recommended for shipping" note. Several notes still say "Godot import pending". The MIT notice is not yet in any shipped location. Inspection renders also show a floating ceiling tile, a blown-out floor, stretched rust textures, and stylised low-poly tower/bus models clashing with the realistic cast.

Verdict: the integrity and engine-load claims are CONFIRMED. Mission functional readiness is REJECTED as stated, and should read PARTIAL. Character and production readiness remain PARTIAL.

## Disposition of rejected claims (19 October 2026)

These are the author's fixes. Each still needs an independent re-check before it counts as closed.

| Finding | Fix | Evidence |
|---|---|---|
| QAF-24 | `tools/phase15_coverage.py` now caps a mission at PARTIAL when any CRITICAL bundle is PARTIAL. All six missions now read PARTIAL / NOT READY | [ASSET_COVERAGE_MATRIX.md](ASSET_COVERAGE_MATRIX.md) |
| QAF-07 | Rocketbox `engine_bounds` recomputed from the evaluated mesh in rest pose (Blender, glTF Y-up). Heights are 1.84 / 1.78 / 1.80 / 1.79 / 1.83 / 1.67 m (Adrian, Noah, Silas, inmate, Rusk, Mara). The Godot skinned AABB is kept as `godot_skinned_aabb_unreliable`. `phase15_finalize.py` and `phase15_integrate.py` no longer overwrite it | `asset_library/manifests/phase15/rocketbox_rest_bounds.json`, `tools/phase15_rocketbox_bounds.py` |
| QAF-16 | Camera moved out of the wall to (2.5, 2.4, −11.5), and RGB axis gizmos added at both test origins. The render shows both pivots at floor level on the asset's bottom edge | `asset_library/manifests/phase15/inspection/zoneA_origins.png` |
| QAF-21 | Addendum added for the 27 DISC15 clips: 27/27 pass the automated checks. Two are flagged for full-scale peaks (radio noise loop, bell ding 2). Listening is still NOT TESTED | [AUDIO_MATERIALS_AUDIT.md](AUDIO_MATERIALS_AUDIT.md#addendum-disc15-discovery-clips-qaf-21) |
| Noah jacket-hem bleed | Recolour mask fixed in two ways: a dilated region can no longer claim another region's texels, and an opt-in island-majority vote relabels triangles that cut across a garment panel. Only the embedded body PNG was swapped (`tools/phase15_rocketbox_retexture.py`); geometry and clips are unchanged. Re-rendered in Blender, and the Godot import is clean | `asset_library/manifests/phase15/noah_retexture.json`, `rocketbox_eval/rb_noah_reyes__*.png` |
