# Audio and Materials Audit (Phase 01.5, Agent 04)

Generated 2026-10-18T22:05:51. Machine-readable results: [audio_materials_audit.json](../../asset_library/manifests/phase15/audio_materials_audit.json).

**Listening was NOT performed.** All realism, loop-seam, edit and mix judgements remain NOT TESTED. Godot was NOT run by this audit; Godot evidence is read from earlier runs (`asset_library/manifests/phase15/godot_validation.json`, Phase 01 `godot_resource_validation.json`) plus `.import` sidecars and `.godot/imported/*.md5` cache hashes, which were compared with the current files.

## Summary

| Check | Result | Status |
|---|---|---|
| Audio files audited | 614 (310 bulk + 277 OGA downloaded, 7 original synthetic, 20 Phase 01 Kenney) | VERIFIED |
| Runtime files present / SHA256 match manifest | 0 missing, 0 mismatches (Phase 01 has no per-file hash; not compared) | VERIFIED |
| Unique by SHA256 / decoded PCM | 614 / 614 (0 byte or PCM duplicate groups) | VERIFIED |
| Near-identical waveform groups (xcorr>=0.95) | 7 groups flagged; 3 clips rejected at xcorr>=0.98 | PARTIALLY_VERIFIED |
| WAV header (RIFF/WAVE, tag 1, 16-bit, <=2 ch) + OGG Vorbis container | 0 failures (120 WAV, 494 OGG) | VERIFIED |
| FFmpeg decode | 0 failures; 0 silent; 0 with runtime full-scale samples | VERIFIED |
| DC offset > 0.01 | 5 clips (all short Kenney UI clicks/glitches) | PARTIALLY_VERIFIED |
| License evidence | 20 anomalies (all 20 Phase 01 clips: record has no license_file field; Kenney CC0 text exists). Downloaded 587: 0 anomalies | PARTIALLY_VERIFIED |
| Godot load evidence | 0 with no evidence; 0 stale import caches; 0 .import missing | VERIFIED (prior run) |
| Classification (all 614) | 589 usable candidates, 25 rejected | PARTIALLY_VERIFIED |
| Classification (587 downloaded) | 562 usable candidates, 25 rejected | PARTIALLY_VERIFIED |
| Listening / mix | not performed | NOT TESTED |
| Materials (19 PBR sets) | all .tres/textures present, maps wired, 1024x1024, Godot load VERIFIED; visual/UV review outstanding; import settings risk | PARTIALLY_VERIFIED |

## Serious issues

1. **Required prison audio is still missing**: no VO, PA speech, crowd/walla, bus engine, radio speech, music score or ocean/coastal wind. Downloads are generic foley/UI; alarm and machinery coverage is thin and partly synthetic (see Missing table).
2. **Source clipping**: 112 downloaded clips had decoded full-scale overshoot in source; runtime copies were attenuated to peak 0.5 but clipping is baked in. 11 with >=50 full-scale source samples are rejected (metalPot1-3, doorClose_1/_3, keys_05-07, bookPlace2/3, footstep08). 13 more (10-49 samples) need audition first.
3. **Stale provenance**: `phase15_bulk_audio_corrections.json` runtime_checksum differs from the current file for all 112 repaired clips. It most likely records the earlier 24-bit WAV state (inferred, not confirmed). The main manifests match the files, so the corrections file needs a refresh.
4. **Texture import settings**: all 58 material textures import with `compress/mode=0` (lossless), `mipmaps/generate=false` and `vram_texture=false`. They rely on Godot detect_3d reimport, so expect aliasing, shimmer and memory cost until the textures are set to VRAM-compressed with mipmaps (normal maps as normal maps).
5. Metal-named sets blue_metal_plate, rusty_painted_metal and worn_corrugated_iron have no metallic map (metallic defaults to 0). Only metal_plate has one.
6. Phase 01 AUDIO_FOLEY record (`assets.json`) has no license_file field and no per-file runtime checksums. That record still says `validation_status: NOT TESTED`.

## Duplicate groups

No byte-identical (SHA256) or decoded-PCM-identical groups exist. That includes the Phase 01 20 versus the Phase 15 impact-sounds remainder. Near-identical waveform groups (8 kHz mono, max-lag cross-correlation) are listed below. At xcorr>=0.98 the later member is rejected as a redundant variant. Groups from 0.95 to 0.98 are only flagged, because they are distinct Kenney variations.

| Kept | Other member(s) | Max xcorr | Action |
|---|---|---|---|
| footstep_concrete_000.ogg | footstep_concrete_001.ogg, footstep_concrete_002.ogg, footstep_concrete_003.ogg, footstep_concrete_004.ogg | 0.9685 | flag only |
| impactsoft_medium_002.ogg | impactsoft_medium_003.ogg, impactsoft_medium_004.ogg | 0.9711 | flag only |
| footstep_wood_002.ogg | footstep_wood_004.ogg | 0.9828 | reject |
| impactwood_medium_000.ogg | impactwood_medium_004.ogg | 0.9771 | flag only |
| impactpunch_heavy_001.ogg | impactpunch_heavy_004.ogg | 0.9970 | reject |
| impactpunch_medium_002.ogg | impactpunch_medium_004.ogg | 0.9907 | reject |
| impactsoft_heavy_001.ogg | impactsoft_heavy_002.ogg | 0.9504 | flag only |

## Rejected audio (25)

| File | Reason |
|---|---|
| phase15/impact-sounds/footstep_snow_000.ogg | setting mismatch: snow footsteps (no snow surface in prison/coastal setting) |
| phase15/impact-sounds/footstep_snow_001.ogg | setting mismatch: snow footsteps (no snow surface in prison/coastal setting) |
| phase15/impact-sounds/footstep_snow_002.ogg | setting mismatch: snow footsteps (no snow surface in prison/coastal setting) |
| phase15/impact-sounds/footstep_snow_003.ogg | setting mismatch: snow footsteps (no snow surface in prison/coastal setting) |
| phase15/impact-sounds/footstep_snow_004.ogg | setting mismatch: snow footsteps (no snow surface in prison/coastal setting) |
| phase15/impact-sounds/footstep_wood_004.ogg | duplicate (near-identical waveform (8 kHz mono xcorr>=0.98)) of assets/audio/phase15/impact-sounds/footstep_wood_002.ogg |
| phase15/impact-sounds/impactpunch_heavy_004.ogg | duplicate (near-identical waveform (8 kHz mono xcorr>=0.98)) of assets/audio/phase15/impact-sounds/impactpunch_heavy_001.ogg |
| phase15/impact-sounds/impactpunch_medium_004.ogg | duplicate (near-identical waveform (8 kHz mono xcorr>=0.98)) of assets/audio/phase15/impact-sounds/impactpunch_medium_002.ogg |
| phase15/rpg-audio/bookplace2.wav | likely source clipping: 76 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/rpg-audio/bookplace3.wav | likely source clipping: 62 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/rpg-audio/chop.wav | combat/fantasy content (axe chop, RPG pack) |
| phase15/rpg-audio/doorclose_1.wav | likely source clipping: 77 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/rpg-audio/doorclose_3.wav | likely source clipping: 249 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/rpg-audio/drawknife1.ogg | combat/weapon content (knife draw/slice) - not prison-escape foley scope |
| phase15/rpg-audio/drawknife2.ogg | combat/weapon content (knife draw/slice) - not prison-escape foley scope |
| phase15/rpg-audio/drawknife3.ogg | combat/weapon content (knife draw/slice) - not prison-escape foley scope |
| phase15/rpg-audio/footstep08.wav | likely source clipping: 77 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/rpg-audio/knifeslice.ogg | combat/weapon content (knife draw/slice) - not prison-escape foley scope |
| phase15/rpg-audio/knifeslice2.wav | combat/weapon content (knife draw/slice) - not prison-escape foley scope |
| phase15/rpg-audio/metalpot1.wav | likely source clipping: 141 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/rpg-audio/metalpot2.wav | likely source clipping: 536 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/rpg-audio/metalpot3.wav | likely source clipping: 948 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/100-cc0-metal-and-wood-sfx/keys_05.wav | likely source clipping: 66 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/100-cc0-metal-and-wood-sfx/keys_06.wav | likely source clipping: 104 decoded full-scale samples in source (threshold 50); attenuation cannot repair |
| phase15/100-cc0-metal-and-wood-sfx/keys_07.wav | likely source clipping: 74 decoded full-scale samples in source (threshold 50); attenuation cannot repair |

Audition priority (usable, but with 10 to 49 source full-scale samples): switch16, switch18, switch31, switch32, bookClose, bookPlace1, doorClose_4, doorOpen_1, doorOpen_2, footstep01, metalLatch, wood_breaking_01, wood_falling_01.

## Usable candidates by requirement category (name-based, unauditioned)

| Category | Usable | Examples |
|---|---|---|
| impacts_general | 248 | impactgeneric_light_000.ogg, impactgeneric_light_001.ogg, impactgeneric_light_002.ogg, impactgeneric_light_003.ogg, impactgeneric_light_004.ogg, impactglass_heavy_000.ogg ... |
| ui | 151 | back_001.ogg, back_002.ogg, back_003.ogg, back_004.ogg, bong_001.ogg, click_001.ogg ... |
| metal_impacts | 74 | impactbell_heavy_000.ogg, impactbell_heavy_001.ogg, impactbell_heavy_002.ogg, impactbell_heavy_003.ogg, impactbell_heavy_004.ogg, impactplate_heavy_000.ogg ... |
| footsteps | 35 | footstep_carpet_000.ogg, footstep_carpet_001.ogg, footstep_carpet_003.ogg, footstep_grass_000.ogg, footstep_grass_001.ogg, footstep_grass_002.ogg ... |
| doors_locks | 27 | creak1.ogg, creak2.ogg, creak3.ogg, doorclose_2.ogg, doorclose_4.wav, dooropen_1.wav ... |
| cloth_objects_handling | 21 | belthandle1.ogg, belthandle2.ogg, bookclose.wav, bookflip1.wav, bookflip2.ogg, bookflip3.ogg ... |
| ambience_generic | 8 | sfx100v2_air_01.ogg, sfx100v2_air_02.ogg, sfx100v2_air_03.ogg, sfx100v2_loop_ambient_01.ogg, sfx100v2_loop_ambient_02.ogg, sfx100v2_loop_ambient_03.ogg ... |
| machinery_hum | 8 | sfx100v2_loop_construction_site.ogg, sfx100v2_loop_machine_01.ogg, sfx100v2_loop_machine_02.ogg, sfx100v2_loop_machine_03.ogg, sfx100v2_loop_machine_04.ogg, qubodup_edev.wav ... |
| electrical_switch | 4 | metalclick.ogg, sfx100v2_switch_01.ogg, sfx100v2_switch_02.ogg, relay_click.wav |
| weather_water | 4 | sfx100v2_loop_water_01.ogg, sfx100v2_loop_water_02.ogg, sfx100v2_loop_water_03.ogg, sfx100v2_thunder_01.ogg |
| keys | 4 | keys_01.ogg, keys_02.wav, keys_03.ogg, keys_04.wav |
| alarm | 2 | alarm_siren.wav, alert_double.wav |
| alarm+weather (combined field recording) | 1 | storm_3_siren.ogg |
| radio_static (no speech) | 1 | radio_static.wav |
| pa_chime (no speech) | 1 | pa_chime.wav |

## Required but missing / partial

| Requirement | Status | Note |
|---|---|---|
| voice-over / original dialogue (VO) | MISSING | no VO in any pack; originals deliberately contain no voice |
| PA announcements (speech) | MISSING | only synthetic pa_chime (tone) exists |
| crowd / inmate walla | MISSING | no crowd clips |
| bus engine / transport | MISSING | loop_highway is generic traffic ambience, not a bus engine interior/exterior |
| patrol radio speech / chatter | MISSING | only synthetic radio_static (noise, no speech) |
| music score | MISSING | no music |
| ocean / coastal wind ambience | MISSING | air_* and loop_ambient_* unauditioned generics; storm_3_siren is storm+siren combined, not isolated ocean wind |
| gate / cell-door mechanism (heavy sliding bars) | PARTIALLY_VERIFIED (partial) | metal doors/slams exist; no authentic prison sliding-gate recording |
| scanner / metal-detector beep | PARTIALLY_VERIFIED (partial) | UI beeps only (interface-sounds), not identified as scanner |
| restraints / handcuffs | MISSING | no cuff/chain clips identified by name (metal/keys may substitute after audition) |
| isolated prison alarm (field recording) | PARTIALLY_VERIFIED (partial) | synthetic alarm_siren/alert_double and combined storm siren only |

## Per-pack audio results

| Pack | Clips | Header PASS | Decode PASS | Godot VERIFIED | License | Usable | Rejected |
|---|---|---|---|---|---|---|---|
| impact-sounds | 108 | 108 | 108 | 108 | VERIFIED 108 | 100 | 8 |
| interface-sounds | 100 | 100 | 100 | 100 | VERIFIED 100 | 100 | 0 |
| ui-audio | 51 | 51 | 51 | 51 | VERIFIED 51 | 51 | 0 |
| rpg-audio | 51 | 51 | 51 | 51 | VERIFIED 51 | 37 | 14 |
| 100-cc0-sfx-2 | 100 | 100 | 100 | 100 | VERIFIED 100 | 100 | 0 |
| 75-cc0-breaking-falling-hit-sfx | 75 | 75 | 75 | 75 | VERIFIED 75 | 75 | 0 |
| 100-cc0-metal-and-wood-sfx | 100 | 100 | 100 | 100 | VERIFIED 100 | 97 | 3 |
| electronic-device-loop | 1 | 1 | 1 | 1 | VERIFIED 1 | 1 | 0 |
| ambience | 1 | 1 | 1 | 1 | VERIFIED 1 | 1 | 0 |
| phase15_original | 7 | 7 | 7 | 7 | DOCUMENTED 7 | 7 | 0 |
| phase01_foley | 20 | 20 | 20 | 20 | PARTIALLY_VERIFIED 20 | 20 | 0 |

Format profile: WAV is all PCM16 format tag 1 (112 stereo 44.1/48 kHz, 7 mono 48 kHz originals, 1 stereo 96 kHz qubodup_edev). OGG is all Vorbis with 1 or 2 channels. The minimum duration is 0.007 s (UI clicks). The maximum is 85.65 s (storm_3_siren). No runtime file reaches full scale.

## Materials (19 Poly Haven sets)

| Material | .tres | Maps | Resolution | Textures exist / match original | Godot load | License | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| concrete_block_wall | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| concrete_floor_painted | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| concrete_floor_worn_001 | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| painted_concrete | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| painted_concrete_02 | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| concrete_wall_004 | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| concrete_slab_wall | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| hangar_concrete_floor | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| smooth_concrete_floor | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| blue_metal_plate | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED | no metallic map (metal-named) |
| metal_plate | OK | alb/nor/rough/metal | 1024x1024 | 4/4, 4/4 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| rusty_painted_metal | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED | no metallic map (metal-named) |
| rubber_tiles | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| denim_fabric | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| fabric_leather_01 | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| dirty_tiles | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| asphalt_01 | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| anti_slip_concrete | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED |  |
| worn_corrugated_iron | OK | alb/nor/rough | 1024x1024 | 3/3, 3/3 | VERIFIED | CC0 OK | PARTIALLY_VERIFIED | no metallic map (metal-named) |

Material notes. Every .tres is a StandardMaterial3D whose ext_resources match the manifest dependencies, with normal_enabled=true and roughness from the red channel. Every texture is a 1024x1024 PNG, byte-identical to the original download, and has a `.import` sidecar with a current cache md5. Godot load evidence covers the .tres (preview sphere, 0 null materials). The individual texture paths have no separate godot_validation entries. Licensing: each record is CC0-1.0 with a Poly Haven asset URL, and provider metadata JSON shows authors that match `creator`. The shared CC0 policy snapshot is `asset_library/licenses/PolyHaven_license_policy.html`. "Powered by Poly Haven" appears in every record note and in PHASE15_BULK_ACQUISITION.md. Visual review and physical UV scale are NOT TESTED.

## Method

- **decode**: ffmpeg -> f32le native rate/channels (peak, full-scale |x|>=0.9999, DC per channel, flat-top runs); s16le PCM sha256; mono 8 kHz 20 ms RMS envelope for near-duplicate correlation
- **wav_header**: byte-level RIFF parse: RIFF/WAVE, fmt tag 1, 16-bit, channels<=2, byte_rate/block_align consistent, RIFF size, data chunk
- **godot**: read-only cross-check of asset_library/manifests/phase15/godot_validation.json (earlier run) + .import sidecars + .godot/imported/*.md5 source_md5 vs current file md5. Godot NOT run.
- **classification**: reject: failed checks, duplicate (keep priority phase01>original>bulk>oga), combat/fantasy or setting-mismatch names, source decoded full-scale samples >= 50, license anomaly. Name-based categories; listening NOT performed.
- Scripts (scratchpad, run with `python -I`): agent04/collect.py, audit.py, report.py. No project asset, manifest or original download was modified.
