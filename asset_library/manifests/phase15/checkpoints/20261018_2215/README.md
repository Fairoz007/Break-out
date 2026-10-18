# BREAKOUT: NO WAY BACK

Realistic cinematic 3D cooperative action/adventure stealth thriller. Godot **4.7.2 stable**, GDScript, Windows PC, third-person, two players; local vertical split-screen first, online cooperative later. **Phase 01: documentation delivered, asset readiness BLOCKED. No gameplay implemented.** Chapter 1 targets approximately 36 minutes, subject to playtesting.

This existing `break-out` workspace is the project root corresponding to the requested `BREAKOUT-NO-WAY-BACK/` tree; it was preserved in place so the existing Godot project remains usable. No duplicate nested project was created.

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

[Prison intake](docs/environments/PRISON_INTAKE.md) · [Cell block](docs/environments/CELL_BLOCK.md) · [Prison yard](docs/environments/PRISON_YARD.md) · [Laundry/workshop](docs/environments/LAUNDRY_WORKSHOP.md) · [Maintenance network](docs/environments/MAINTENANCE_NETWORK.md). Dimensions are proposed metric build specifications; no constructed level or camera clearance playtest is claimed.

## Asset library

- [Requirements](docs/assets/ASSET_REQUIREMENTS.md), [source research](docs/assets/ASSET_SOURCES.md), [licenses](docs/assets/ASSET_LICENSES.md), [gaps](docs/assets/ASSET_GAPS.md), [validation report](docs/assets/ASSET_VALIDATION_REPORT.md).
- [assets.json](asset_library/manifests/assets.json) is the machine-readable source of acquisition status, source URLs, checksums, runtime paths and scene dependencies. Stable asset IDs are uppercase; downloaded provider basenames remain unchanged for provenance. Future runtime assets use lowercase snake_case.
- `asset_library/original_downloads/` preserves provider files/ZIPs; `extracted_sources/` preserves dependency trees; `converted/` is empty because the acquired models already provide glTF. `licenses/` holds source/license evidence; `manifests/` holds metadata, hashes, validation results and rendered previews; `rejected/` is reserved for actual rejected payloads, none currently.
- `assets/` contains separate importable copies, organized by category. Runtime copies are initial import candidates and are not optimized production assets. Missing folders remain intentionally empty rather than populated with fake assets.
- Find an asset ID in the manifest → follow `original_file` and `source_url` → compare checksums → read its local license evidence → check `import_status` and `validation_status` independently. Null paths mean missing, never downloaded.

Acquired: two 1k material map sets, three static prop sets, one partial foley selection. Poly Haven provides 25 payload files; Kenney archive retained in full, 20 selected OGG files copied to runtime. **Powered by Poly Haven**; Kenney credit appreciated. Their [CC0 policy](https://polyhaven.com/license) and [Kenney license statement](https://kenney.nl/support) support commercial use; local evidence is retained. This does not license missing assets or candidate listings.

## Godot development

Installed and tested: `4.7.2.stable.steam.ed1daf0bf`. Open this directory's [project.godot](project.godot) with Godot 4.7.2 stable. Existing Forward Plus/Jolt/D3D12 settings are preserved. No main scene is assigned: pressing Play is not a Phase 01 acceptance test. Select Import on the project manager or open in the editor and allow the import scan to finish. `asset_library/.gdignore` prevents duplicate source import.

[Asset pipeline](docs/technical/GODOT_ASSET_PIPELINE.md) · [Cooperative requirements](docs/technical/COOP_REQUIREMENTS.md) · [Scene architecture](docs/technical/SCENE_ARCHITECTURE.md). Planned `scenes/`, `scripts/`, `resources/` and `tests/` directories contain no gameplay implementation. Future scene roots use stable chapter/mission IDs; authored scene wrappers refer to imported glTF rather than editing provider payloads. Keep two player contexts separate and shared mission state authoritative; exact interfaces are proposals in the architecture document.

Validation tools only:

```powershell
python tools/audit_documentation.py
# Use your installed Godot executable for these two commands:
godot --headless --path . --editor --import
godot --path . --rendering-method gl_compatibility --script tools/validate_resources.gd
```

`godot` may not be on PATH. The installed executable discovered here is `C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe`; call it with PowerShell's `&` and a quoted path. The render validation opens an engine window briefly and writes preview PNGs and resource JSON. This is a tool, not gameplay. Acquisition/build scripts require Python and Pillow; they preserve source metadata. Do not rerun documentation generators after editorial corrections without reviewing the diff.

## Progress and next gate

Completed: narrative treatments; Chapter 1 production script, dialogue, cinematics and blocking; six mission specifications; five environment specifications; inventory and license records; legal selected downloads; static Godot import/resource tests and rendered inspection. Independent findings and corrective cycles are tracked in [review](docs/qa/PREPRODUCTION_REVIEW.md). Documentation consistency audit is reproducible; it does not certify artistic quality or playability.

Pending/blocking: realistic character models/outfits/rigs, animation library and performance takes, complete prison architecture, bespoke story props, full ambience/VO/music, UI/font and VFX; geometry scale/snap, collision/nav, animation deformation, audio listening/mix review, performance and split-screen playtests. Latest validation: three model sets load and render; 20 OGG files load with positive duration and decode without full-scale samples; acquired texture files decode/import. **Phase 01 is not fully asset-ready and is not declared complete.** Exact outstanding bundles are in [asset gaps](docs/assets/ASSET_GAPS.md) and [blockers](docs/qa/BLOCKERS.md).

Next phase begins with closing asset/rig gates and a reviewed blockout, then gameplay implementation only when authorized. No full gameplay coding was started here.

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

