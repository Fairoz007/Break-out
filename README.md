# BREAKOUT: NO WAY BACK

Realistic cinematic 3D cooperative action/adventure stealth thriller. Godot **4.7.2 stable**, GDScript, Windows PC, third-person, two players; local vertical split-screen first, online cooperative later. **Phase 02 in progress: all six Chapter 1 missions are playable in two-player split-screen and complete automatically from a fresh save; independent QA verification is not finished, so Phase 02 is INCOMPLETE.** See [Phase 02 session state](docs/PHASE_02_SESSION_STATE.md), the [completion audit](docs/qa/PHASE_02_COMPLETION_AUDIT.md) and the [Phase 01.5 report](docs/qa/PHASE_01_5_REPORT.md). Chapter 1 targets approximately 36 minutes, subject to playtesting.

This existing `break-out` workspace is the project root corresponding to the requested `BREAKOUT-NO-WAY-BACK/` tree; it was preserved in place so the existing Godot project remains usable. No duplicate nested project was created.

## Play it

Open the project in Godot 4.7.2 and run the main scene, or run the exported `build/windows/BreakoutNoWayBack.exe` (not committed; build it with the "Windows Desktop" preset). Default devices: P1 Adrian on keyboard and mouse (WASD, E interact, Alt jog, Shift sprint, Space jump, C crouch, Esc pause), P2 Noah on the first controller, or on the right-hand keys (IJKL, O interact, U jog, H sprint, M jump, N crouch, P pause) if no controller is connected. Controller: sticks move/look, A interact, LB jog, L3/RT sprint, X jump, B crouch, Start pause. Change assignments under Controls and devices. Both players confirm ready with their own interaction key.

Phase 02.5 recovery is **INCOMPLETE**. Current evidence and remaining work: [session state](docs/qa/PHASE_02_5_SESSION_STATE.md), [reality audit](docs/qa/PHASE_02_5_REALITY_AUDIT.md), [requirements](docs/qa/PHASE_02_5_REQUIREMENTS_MATRIX.md), and [visual review](docs/qa/VISUAL_QUALITY_AUDIT.md). Added jumping, physical crouch clearance, collision-safe recovery and camera return, device-state fixes and limited environment/material improvements. Passing automated checks do not establish production art or physical-controller acceptance.

## Start here

[STORY.md](STORY.md) is the canonical narrative source. Read it before implementing any story content. [Game design](GAME_DESIGN.md), [development plan](DEVELOPMENT_PLAN.md), [asset manifest](ASSET_MANIFEST.md), [independent review](docs/qa/PREPRODUCTION_REVIEW.md), and [blockers](docs/qa/BLOCKERS.md) define the handoff and limits.

## Seven-chapter story

1. [Blackridge](docs/chapters/CHAPTER_01_BLACKRIDGE.md)
2. [Night Shift](docs/chapters/CHAPTER_02_NIGHT_SHIFT.md)
3. [Other Shore](docs/chapters/CHAPTER_03_OTHER_SHORE.md)
4. [Ghosts of the City](docs/chapters/CHAPTER_04_GHOSTS_OF_THE_CITY.md)
5. [The Shipment](docs/chapters/CHAPTER_05_THE_SHIPMENT.md)
6. [Truth Below](docs/chapters/CHAPTER_06_TRUTH_BELOW.md)
7. [No Way Back](docs/chapters/CHAPTER_07_NO_WAY_BACK.md)

## Chapter 1 screenplay and performances

- [Full production script](docs/screenplay/CH01_FULL_SCRIPT.md): six continuous mission scenes, actual dialogue, directions, triggers and end states.
- [Dialogue and subtitle register](docs/screenplay/CH01_DIALOGUE.md)
- [Cutscenes](docs/screenplay/CH01_CUTSCENES.md)
- [Camera shot list](docs/screenplay/CH01_CAMERA_SHOTS.md)
- [Character blocking](docs/screenplay/CH01_CHARACTER_BLOCKING.md)
- [Animation requirements](docs/technical/ANIMATION_REQUIREMENTS.md)

## Missions

- [M01 — New Blood](docs/missions/CH01_MISSION_01.md)
- [M02 — Trouble in the Yard](docs/missions/CH01_MISSION_02.md)
- [M03 — The Workshop](docs/missions/CH01_MISSION_03.md)
- [M04 — Lights Out](docs/missions/CH01_MISSION_04.md)
- [M05 — Behind the Walls](docs/missions/CH01_MISSION_05.md)
- [M06 — The Betrayal](docs/missions/CH01_MISSION_06.md)

## Characters

[Adrian Cross](docs/characters/ADRIAN_CROSS.md) · [Noah Reyes](docs/characters/NOAH_REYES.md) · [Elena Reyes](docs/characters/ELENA_REYES.md) · [Guards and NPCs](docs/characters/GUARDS_AND_NPCS.md) · [Relationships](docs/characters/CHARACTER_RELATIONSHIPS.md).

## Environment construction

[Prison intake](docs/environments/PRISON_INTAKE.md) · [Cell block](docs/environments/CELL_BLOCK.md) · [Prison yard](docs/environments/PRISON_YARD.md) · [Laundry/workshop](docs/environments/LAUNDRY_WORKSHOP.md) · [Maintenance network](docs/environments/MAINTENANCE_NETWORK.md). These are design specifications; runtime environments are built by `scripts/world/env_*.gd`. Graphical review and camera clearance acceptance remain tracked in the Phase 02 registry.

## Asset library

The current Phase02.5 supplement contains1,000 newly downloaded CC0 assets:335 glTF models and665 complete2K PBR material sets. [Batch inventory](asset_library/manifests/phase025_bulk_20261019/inventory.json) and [license/provenance](asset_library/licenses/phase025_bulk_20261019/README.md). They are stored under `asset_library/original_downloads/phase025_bulk_20261019/` for selection and validation; they are not all integrated into the game. The Phase01.5 counts and acquisition notes below are historical scoped records. Powered by Poly Haven.

- [Requirements](docs/assets/ASSET_REQUIREMENTS.md), [source research](docs/assets/ASSET_SOURCES.md), [licenses](docs/assets/ASSET_LICENSES.md), [gaps](docs/assets/ASSET_GAPS.md), [validation report](docs/assets/ASSET_VALIDATION_REPORT.md).
- [assets.json](asset_library/manifests/assets.json) is the machine-readable source of acquisition status, source URLs, checksums, runtime paths and scene dependencies. Stable asset IDs are uppercase; downloaded provider basenames remain unchanged for provenance. Future runtime assets use lowercase snake_case.
- `asset_library/original_downloads/` preserves provider files/ZIPs; `extracted_sources/` preserves dependency trees; `converted/` is empty because the acquired models already provide glTF. `licenses/` holds source/license evidence; `manifests/` holds metadata, hashes, validation results and rendered previews; `rejected/` is reserved for actual rejected payloads, none currently.
- `assets/` contains separate importable copies, organized by category. Runtime copies are initial import candidates and are not optimized production assets. Missing folders remain intentionally empty rather than populated with fake assets.
- Find an asset ID in the manifest → follow `original_file` and `source_url` → compare checksums → read its local license evidence → check `import_status` and `validation_status` independently. Null paths mean missing, never downloaded.

Phase 01.5 inventory, from [assets.json](asset_library/manifests/assets.json):

- 831 records: 670 downloaded Phase 01.5 records, 76 original assets, 57 derived builds, and 28 Phase 01 records.
- **772 usable:** each loads in Godot and passes file, licence and checksum checks.
- 31 rejected, failed or superseded.

What the library contains:

- **Characters:** a realistic [Microsoft Rocketbox](https://github.com/microsoft/Microsoft-Rocketbox) cast (MIT; the notice must ship) in `assets/characters/phase15/rocketbox/`, and a CC0 Quaternius proxy cast in `assets/characters/phase15/ubc/`. Each character carries 37 Quaternius UAL clips.
- **Architecture:** 53 original modules and props, 20 Poly Haven sets, 38 split kit pieces and 12 discovery props.
- **Audio and materials:** 596 usable audio clips (not yet listened to) and 19 PBR sets.

Licences are mostly CC0, plus MIT (Rocketbox) and one CC-BY set (Ouren basketball hoop, credit recorded). **Powered by Poly Haven**; Kenney, Quaternius and OpenGameArt authors are credited in the records.

Readiness is tracked separately for each of the 22 requirement bundles: **functional** vs **production** ([manifest](ASSET_MANIFEST.md), [coverage matrix](docs/qa/ASSET_COVERAGE_MATRIX.md), [blockers](docs/qa/BLOCKERS.md)). Discovery and account-gated candidates are in [PHASE15_DISCOVERY.md](docs/assets/PHASE15_DISCOVERY.md).

QA reports:

- [Character rigs](docs/qa/CHARACTER_RIG_VALIDATION.md)
- [Animation](docs/qa/ANIMATION_VALIDATION.md)
- [Architecture](docs/qa/PRISON_ARCHITECTURE_VALIDATION.md)
- [Audio/materials audit](docs/qa/AUDIO_MATERIALS_AUDIT.md)
- [Independent review](docs/qa/PHASE15_INDEPENDENT_REVIEW.md)

## Godot development

Installed and tested: `4.7.2.stable.steam.ed1daf0bf`. Open this directory's [project.godot](project.godot) with Godot 4.7.2 stable. Existing Forward Plus/Jolt/D3D12 settings are preserved. Pressing Play starts `scenes/main.tscn`. Select Import on the project manager or open in the editor and allow the import scan to finish. `asset_library/.gdignore` prevents duplicate source import.

[Asset pipeline](docs/technical/GODOT_ASSET_PIPELINE.md) · [Cooperative requirements](docs/technical/COOP_REQUIREMENTS.md) · [Scene architecture](docs/technical/SCENE_ARCHITECTURE.md). Gameplay lives in `scripts/`, scene entry points in `scenes/`, and system/autopilot checks in `tests/phase02/`. Two player contexts share authoritative mission state. The architecture document distinguishes current runtime ownership from the original design target.

Validation tools only (the full rerun list is in the [validation report](docs/assets/ASSET_VALIDATION_REPORT.md)):

```powershell
$G = "C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe"
python -I tools/phase15_prepare.py
& $G --headless --path . --editor --import
& $G --path . --rendering-method gl_compatibility --script tools/phase15_validate.gd
& $G --path . --rendering-method gl_compatibility --script tools/phase15_character_godot.gd
& $G --path . --rendering-method gl_compatibility --script tools/phase15_inspection_scene.gd
python -I tools/phase15_finalize.py; python -I tools/phase15_coverage.py; python -I tools/phase15_manifest_docs.py
```

`godot` is not on PATH, so call the Steam executable above with PowerShell's `&`. The graphical scripts open a window briefly and write PNG/JSON evidence under `asset_library/manifests/`. They are tools, not gameplay.

The asset inspection scene `tests/asset_inspection/phase15_asset_inspection.tscn` arranges the modules, props, materials and both casts for visual review. It contains no gameplay logic.

## Progress and next gate

Phase 01 completed the narrative, the Chapter 1 screenplay, mission and environment specifications, and the first legal downloads. Phase 01.5 then recovered the interrupted asset session and completed the asset work, verified as follows:

- **Characters:** the MPFB deformation failure was resolved by replacing the base. A realistic cast and a proxy cast were validated in Blender and Godot.
- **Animation:** 37 clips are verified on every character.
- **Architecture:** repair cycle 1 left 0 of 70 assets failing. Critical originals were added: lifting grille, pump and ball.
- **Discovery:** discovery assets were integrated.
- **Godot:** 908/908 resources load, and an inspection scene was built.
- **Manifest:** integrated, with a per-mission coverage matrix.

Readiness gates ([report](docs/qa/PHASE_01_5_REPORT.md)):

| Gate | Verdict |
|---|---|
| A: Core gameplay assets | **PASS** |
| B: Realistic characters | **PARTIAL** |
| C: Level construction | **PARTIAL** |
| D: Cinematic assets | **BLOCKED** |
| E: Production quality | **BLOCKED** |

Open items are listed in [blockers](docs/qa/BLOCKERS.md): facial/VO, paired co-op animation, likeness approval, scanner and bus, collision/nav/LOD, audio listening, close-up props, split-screen UI/VFX, and licence credits.

The next milestone is Phase 02a: core co-op gameplay on graybox, started only when authorised. No gameplay coding was started in Phase 01.5.

## Documentation rules

1. Read README.md first.
2. Read STORY.md before story implementation.
3. Read the relevant mission specification.
4. Read its environment specifications.
5. Check assets.json, licenses and validation evidence.
6. Implement the authorized feature.
7. Run appropriate tests.
8. Update affected documentation and review findings.
9. Update README.md for important changes; never label untested or unfinished work complete.


# Break-out
