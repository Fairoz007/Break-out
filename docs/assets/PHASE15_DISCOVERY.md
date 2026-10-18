# Phase 01.5 Asset Discovery (Agent E)

Date: 2026-10-18. Machine-readable record: `asset_library/manifests/phase15/discovery_candidates.json`. That file has every candidate, every file's sha256 and local paths. None of these assets has been integrated into runtime. `assets/` was not touched and Godot was not run.

Locations:
- Raw downloads: `asset_library/original_downloads/phase15_discovery/<slug>/`
- Licence evidence: `asset_library/licenses/phase15_discovery/<slug>/`
- Extracted archives: `asset_library/extracted_sources/phase15_discovery/<slug>/`

## 1. Realistic rigged humans

| Candidate | Status | Licence | Rig | Notes |
|---|---|---|---|---|
| **Microsoft Rocketbox** (Male_Adult_01, Security_Male_01, Medical_Female_01) | **ACQUIRED** | MIT (commercial OK; ship the notice) | 3ds Max Biped `Bip01`, 80 bones (28 facial, 30 finger) | 7.4k-9.5k tris, 1.74-1.83 m. 2k TGA colour/normal/specular. `*_facial.fbx` has 176 blendshapes (visemes, FACS, ARKit). All 32 files match the GitHub blob SHA-1. |
| MPFB2 / MakeHuman | ALREADY_ACQUIRED_PREVIOUSLY | CC0 | MakeHuman | Retargeting failed earlier |
| Quaternius packs | NOT_REALISTIC | CC0 | UAL 65 | Already in use (UBC) |
| Poly Haven | NOT_FOUND | CC0 | n/a | 521 models; no humans |
| OGA YW stylized, Modular RPG, Bartender, Very Low Poly, Kenney | NOT_REALISTIC | CC0 | various | Stylised or low-poly |
| OGA thehumbug basemeshes | SKIPPED_REDUNDANT | CC-BY 3.0 / CC0 (conflicting) | MakeHuman | Same pipeline as MPFB |
| Mixamo, Sketchfab, Fab, ActorCore | ACCOUNT_REQUIRED | various | various | Not attempted |
| MetaHuman / UE Manny, SMPL | LICENSE_UNSUITABLE | UE-only EULA / non-commercial | n/a | n/a |

Rocketbox caveats:
- The FBX texture paths point to the author's machine (`D:\temp\...`). Relink them to the sibling `Textures/`.
- The textures use a specular workflow; convert them to roughness for Godot.
- Retargeting to UAL or the Godot humanoid profile needs a Biped bone map.
- The library has 115 avatars, including Police, Security and Medical, plus 471 Biped animation FBX files (about 1.46 GB, MIT). 8 avatars have been downloaded so far (3 here, 5 in the follow-up below).

Suggested mapping:
- Security_Male_01 → Rusk and the guards
- Medical_Female_01 → Mara Sen
- Male_Adult_* → Adrian, Noah, Silas and the inmates (needs a prison-uniform retexture)

### Follow-up: Rocketbox avatars for protagonists and inmates

These were picked by viewing the official preview PNGs. All are under `microsoft_rocketbox/Adults/<name>/` and include Export plain + `_facial` FBX, all Textures and the preview PNG. Every file matches its GitHub blob SHA-1. Heights were measured in Blender from the mesh bounding box. All five have the Bip01 rig (80 bones) and 176 blendshapes.

| Avatar | Role | Clothing | Skin / hair | Height | Tris |
|---|---|---|---|---|---|
| Male_Adult_02 | Adrian | Plain beige sweater, dark trousers | Light skin, short-to-medium dark hair | 1.823 m | 7,312 |
| Male_Adult_20 | Adrian alt / inmate | Plain brown hoodie, jeans | Light skin, short dark hair | 1.805 m | 7,120 |
| Male_Adult_12 | Noah | Plain white tee under plain denim jacket, jeans | Brown skin (darker than "warm"; tint if needed), short black hair | 1.807 m | 6,722 |
| Male_Adult_11 | Silas / inmate | Plain olive short-sleeve work shirt, jeans | Light skin, very short buzz cut | 1.803 m | 6,740 |
| Male_Adult_14 | Older inmate | Plain grey shirt, khaki chinos | Light skin, balding / receding | 1.796 m | 6,842 |

None of them is a perfect height match, so scale to the briefs: Adrian about 1.01x to reach 1.84 m, Noah about 0.985x for 1.78 m, Silas 1.0x for 1.80 m.

Rusk: no older heavy-build uniformed male exists in Rocketbox. All the Police, Security and Military previews were viewed. The closest is Security_Male_01 (already acquired): older, grey hair under a peaked cap, grey security shirt and tie, 1.83 m, average build. Widen the build at retarget time. Male_Adult_14's receding head is a usable reference.

## 2. Environment and props

| Need | Asset | Status | Licence | Inspection |
|---|---|---|---|---|
| Gate / security door | Poly Haven `large_iron_gate` | ACQUIRED | CC0 | 38k tris, 2.95 x 2.93 m, glTF 1k |
| Power isolator / panel | Poly Haven `power_box_01` | ACQUIRED | CC0 | 21k tris, rigged lid |
| Surveillance | Poly Haven `security_camera_01` | ACQUIRED | CC0 | 13.5k tris, rigged |
| Cell bed | Poly Haven `old_bed_frame` | ACQUIRED | CC0 | 50k tris, 2.0 m |
| Cable trays | Poly Haven `modular_electric_cables` | ACQUIRED | CC0 | 49 pieces, 42k tris |
| Transport bus | Quaternius LowPoly Public Transport (OGA) | ACQUIRED | CC0 | Bus 1.5k tris, about 4 m long (scale it up), stylised, no interior |
| Watchtower | Watchtower-Wood by atze (OGA) | ACQUIRED | CC0 | 2.6k tris, 5.2 m, wooden blockout |
| Watchtower | Guard_Tower by Ivan R. (OGA) | ACQUIRED | CC0 | Medieval arrow turret; low suitability |
| Basketball | Basketball lowpoly, NephthysGameDev (OGA) | ACQUIRED | CC0 | 112 tris |
| Hoop + rack | basketball by Ouren / Wolfgang Wozniak (OGA) | ACQUIRED | **CC-BY 3.0 (credit required)** | Hoop 400 tris, rack 992 tris |
| Walk-through scanner | n/a | NOT_FOUND | n/a | Poly Haven's `metal_detector` is a handheld treasure detector (SKIPPED_UNSUITABLE) |
| Industrial washer | n/a | NOT_FOUND | n/a | itch.io listing has no licence stated |
| Razor wire | n/a | NOT_FOUND | n/a | ambientCG has 0 hits. Chain-link fence was already acquired |
| Realistic bus / washer / scanner | Sketchfab, Fab | ACCOUNT_REQUIRED | n/a | n/a |

## 3. Audio

| Need | Asset | Status | Licence |
|---|---|---|---|
| Radio static | Radio Noise 1, Kresiek (`radio_noise_loop.wav`) | ACQUIRED | CC0 |
| Alarm, machine hum, electrical noise | 30 CC0 SFX loops, rubberduck (alarm x3, machine x11, noise x3) | ACQUIRED | CC0 |
| Alarm / siren | Sirens and Alarm Noise, aquinn | ACQUIRED | CC0 |
| Crowd | Crowd Shouting/Speaking Ambience, StarNinjas (shouting, not murmur) | ACQUIRED | CC0 |
| Wind | wind whoosh loop, SketchMan3 | ACQUIRED | CC0 |
| Water | VistulaShort.mp3, RandomMind (river waves, 5 min) | ACQUIRED | CC0 |
| PA chime | bell_ding1/2, PWL | ACQUIRED | CC0 |
| Diesel bus engine | n/a | NOT_FOUND (no-login CC0) | Use the machine loops as a proxy |
| PA voice | n/a | NOT_FOUND | Record original VO |
| Walla, diesel idle, ocean | Freesound | ACCOUNT_REQUIRED | Login needed to download |

## Needs the user's account
- Freesound: walla, diesel bus idle, ocean surf.
- Sketchfab: CC-BY realistic washer, scanner, bus, watchtower.
- Mixamo: realistic characters and animations.
- Fab: free listings.

## Attribution obligations
- Rocketbox: MIT notice.
- Ouren / Wolfgang Wozniak: CC-BY 3.0 hoop.
- Credit is optional for the CC0 items, though StarNinjas and atze request it.

## Runtime integration (Agent D)

Date: 2026-10-18. Records: `asset_library/manifests/phase15_discovery_records.json` (39 records, `DISC15_*`, all `import_status: PENDING_GODOT_CHECK`, `validation_status: PARTIALLY_VERIFIED`). Godot was not run. `assets.json` was not edited. Originals were not modified: all 135 downloaded and extracted files still match their recorded sha256. Previews are in `asset_library/manifests/phase15/previews_discovery/`, and audio waveforms are in its `audio/` subfolder. Rocketbox characters are out of scope here (coordinator).

Conversion: Blender 5.1 headless, `--factory-startup`, auto-run scripts off. `.blend` objects were appended via `bpy.data.libraries.load`, so nothing from the archives was executed. Output is GLB, Y-up, front +Z, in metres, with origin at base centre (balls: centre). Every file was re-imported in a fresh scene to get dims and tris. Poly Haven sets were copied byte-identical (1k glTF + bin + JPG).

### Props (`assets/props/phase15_discovery/<slug>/`)

| Runtime file | Dims x / y-up / z (m) | Tris | Textured | Suitability |
|---|---|---|---|---|
| `large_iron_gate/large_iron_gate_1k.gltf` | 2.95 / 2.93 / 0.10 | 38,140 | PBR 1k | MEDIUM. Realistic, but an ornate garden/estate gate, not a prison security gate |
| `power_box_01/power_box_01_1k.gltf` | 0.46 / 0.50 / 0.40 | 21,272 | PBR 1k | HIGH. Breaker panel. Origin at the box centre, as provided (wall pivot) |
| `security_camera_01/security_camera_01_1k.gltf` | 0.17 / 0.29 / 0.55 | 13,571 | PBR 1k | HIGH. Realistic CCTV with bracket |
| `old_bed_frame/old_bed_frame_1k.gltf` | 0.91 / 1.20 / 2.00 | 49,990 | PBR 1k | MEDIUM-HIGH. Realistic, but heavy for instancing (needs LOD) |
| `modular_electric_cables/modular_electric_cables_1k.gltf` | 2.08 / 0.76 / 0.22 (kit layout) | 42,078 | PBR 1k | HIGH. 49 separate pieces |
| `quaternius_bus/quaternius_bus.glb` | 2.50 / 3.20 / 12.00 | 1,530 | flat colours | MEDIUM. Stylised low-poly, exterior only. Scaled non-uniformly from toy scale. Colours assigned by Agent D (source was all grey) |
| `oga_watchtower_wood/watchtower_wood.glb` | 2.57 / 6.54 / 2.92 | 2,640 | 1k diffuse | MEDIUM-LOW. Textured wooden scaffold tower, scaled x1.5. Blockout or distance use only |
| `oga_guard_tower/guard_tower_arrow_turret.glb` | 4.91 / 6.00 / 4.76 | 1,046 | 1k hand-painted | LOW. Medieval arrow turret, wrong era. Not recommended |
| `oga_basketball_lowpoly/basketball_lowpoly.glb` | 0.24 ball | 112 | none (flat orange) | LOW-MEDIUM. Its texture is missing from the archive |
| `oga_basketball_hoop_ouren/basketball_hoop.glb` | 0.95 / 3.79 / 1.97, rim 3.05 m | 400 | flat (pole/board/rim) | MEDIUM. Low-poly, no net. **CC-BY 3.0** |
| `oga_basketball_hoop_ouren/ball_rack.glb` | 1.70 / 1.00 / 0.79 | 992 | flat steel | MEDIUM. **CC-BY 3.0** |
| `oga_basketball_hoop_ouren/basketball_ouren.glb` | 0.24 ball | 216 | 512 px | MEDIUM-HIGH. Recommended ball. **CC-BY 3.0** |

Mixed style: the Poly Haven items are realistic PBR. The bus, towers, hoop, rack and balls are stylised low-poly.

Required credit: "Basketball hoop, ball rack and basketball by Ouren (Wolfgang Wozniak), https://opengameart.org/content/basketball, CC-BY 3.0. Modified: rescaled, materials added, converted to GLB."

### Audio (`assets/audio/phase15_discovery/<slug>/`)

**These clips were NOT listened to.** Checks were ffmpeg decode only (duration > 0, peak, full-scale count), plus sha256 dedupe against all existing `assets/audio` files. There were no duplicates.

| Pack | Runtime files | Format | Notes |
|---|---|---|---|
| StarNinjas crowd | `crowd_shouting.ogg` (27.4 s) | Vorbis, byte-identical | Shouting/protest crowd, not quiet walla |
| Kresiek radio | `radio_noise_loop.wav` (55.2 s) | PCM16 mono 8 kHz (from s32) | Scanner static |
| RandomMind Vistula | `vistula_waves_short.ogg` (300 s) | Vorbis q5, -2 dB | Gain reduced to avoid decode clipping. River waves, not ocean surf |
| SketchMan3 wind | `wind_woosh_loop.ogg` (6.0 s) | Vorbis, byte-identical | n/a |
| aquinn sirens | `siren_part1.ogg` (12.5 s), `siren_part2.ogg` (28.8 s) | Vorbis q5 | Split at the only silence gap. Each part still has several bursts |
| PWL bells | `bell_ding1.wav`, `bell_ding2.wav` | PCM16 stereo, byte-identical | PA chime. `bell_ding2` has 7 full-scale samples in the original |
| rubberduck loops | `alarm_01-03`, `machine_01-11`, `noise_01-03`, `pump_01-02` (.ogg) | Vorbis, byte-identical | 19 of 30 selected |

Not integrated:
- rubberduck `ambient_01-03`: content unknown without listening.
- rubberduck `rain`, `rolling`, `saw`, `water_boiling`, `water_flowing`, `weird_01-03`: off-brief.
- Quaternius SchoolBus, Taxi, Ambulance, Train, bicycles and traffic props: only the bus was requested.
