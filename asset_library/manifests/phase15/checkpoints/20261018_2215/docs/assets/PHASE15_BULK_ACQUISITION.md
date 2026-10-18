# Phase 01.5 bulk acquisition — actual scope

This acquisition adds **606 distinct semantic assets: 587 audio clips and 19 PBR material sets**. It does not add 606 meshes or characters. Texture channels, source/runtime copies, file extensions and provider demonstration montages are not counted as separate assets. SHA256 deduplication excluded the existing 20 clips and repeated byte-identical clips. Two preview montages were excluded from runtime and the final manifests. The complete original archives remain intact.

## Provenance and storage

- [Kenney Impact Sounds](https://kenney.nl/assets/impact-sounds): remainder of the existing archive, excluding already installed clips.
- [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds) and [UI Audio](https://kenney.nl/assets/ui-audio): 151 distinct optional interface candidates after deduplication and montage exclusion. These do not resolve prison ambience.
- [Kenney RPG Audio](https://kenney.nl/assets/rpg-audio): ordinary object/door/footstep candidates; sword/bow/spell filenames excluded. Foley Sounds page returned HTTP404, so no files were invented for it.
- [100 CC0 SFX #2](https://opengameart.org/content/100-cc0-sfx-2), [75 CC0 breaking/falling/hit](https://opengameart.org/content/75-cc0-breaking-falling-hit-sfx), [100 CC0 metal/wood](https://opengameart.org/content/100-cc0-metal-and-wood-sfx): rubberduck, 275 actual clips, including doors, keys, metal movement, machinery loops, thunder, switches, object handling and impacts.
- [Electronic device loop](https://opengameart.org/content/electronic-device-loop): qubodup, archived FLAC converted losslessly to supported WAV.
- [Storm & Siren](https://opengameart.org/content/storm-siren): TinyWorlds, combined weather/flood-siren field recording. This is not an isolated prison alarm.
- [Poly Haven](https://polyhaven.com/license): 19 CC0 1k PBR sets. **Powered by Poly Haven**. Provider metadata snapshots retain author names. Diffuse, OpenGL normal, roughness and metallic where supplied are preserved; physical UV scale still needs artist review.

All downloaded sources above designate CC0. Actual provider HTML/license files and author metadata are retained under `asset_library/licenses/phase15_bulk/`. The pre-existing Poly Haven CC0 policy snapshot remains the shared policy evidence. The [CC0 legal text](https://creativecommons.org/publicdomain/zero/1.0/legalcode) applies to the asset content; provider branding is not included in the game.

Originals: `asset_library/original_downloads/phase15_bulk/` (existing Impact archive retained at its prior path). Runtime: `assets/audio/phase15/`, `assets/textures/phase15/`, `assets/materials/phase15/`. Individual provider texture downloads do not have an archive; original delivered files are retained. ZIP files are not redundantly expanded into a second full source tree: each manifest identifies its original archive member. Every source archive has CRC verification and SHA256; texture files additionally match provider MD5 and decode with Pillow.

## Machine records

- [Bulk manifest fragment](../../asset_library/manifests/phase15_bulk_assets.json): 310 audio +19 materials.
- [OGA manifest fragment](../../asset_library/manifests/phase15_bulk_oga_assets.json): 277 audio.
- [Audio validation](../../asset_library/manifests/phase15_bulk_audio_validation.json): all runtime audio, including existing20, decoded with FFmpeg; FFprobe sample rate/channels/duration; decoded peak and fullscale sample count.
- [Audio repair provenance](../../asset_library/manifests/phase15_bulk_audio_corrections.json): 112 new clips had decoded fullscale overshoot, now attenuated to peak0.5 and converted first to 24-bit WAV and then repaired to standard PCM16 WAV after actual Godot import rejected unsupported WAVE variants. Exact original decoded peaks/fullscale sample counts are retained in their records. Two montages excluded. Original archives unchanged.
- [Acquisition failures](../../asset_library/manifests/phase15_bulk_errors.json) and [OGA failures](../../asset_library/manifests/phase15_bulk_oga_errors.json): final selected acquisition batches report zero failures. Initial probe404 is documented above.

Attenuation provides runtime headroom. It cannot repair clipping already present in source waveforms. **No clips have been listened to by this agent**; realism, edit suitability, looping seams, clipping audibility, and performance in the mix remain NOT TESTED. Audio candidates therefore remain PARTIALLY_VERIFIED. Scene IDs in acquisition records indicate eligible pools, not approved final cue placement. Central integration and mission matrix determine actual accepted use.

Material set names: concrete_block_wall, concrete_floor_painted, concrete_floor_worn_001, painted_concrete, painted_concrete_02, concrete_wall_004, concrete_slab_wall, hangar_concrete_floor, smooth_concrete_floor, blue_metal_plate, metal_plate, rusty_painted_metal, rubber_tiles, denim_fabric, fabric_leather_01, dirty_tiles, asphalt_01, anti_slip_concrete, worn_corrugated_iron. Each is one asset regardless of map count. Material resources use albedo, OpenGL normals, red-channel roughness, and red-channel metalness if supplied. No invented metalness map is assigned where the provider has none.

## Remaining specialist work

Isolated prison crowd/PA, bus engine, guard radio performance, VO, ocean wind, clean isolated alarm, synchronization with interaction events, and final cinematic score remain specific gaps or audition tasks. Wet surfaces, clear glass, plastic and clean brushed steel are not claimed resolved by this set. PBR textiles are not complete character clothing. Characters, rigs, animations and architecture belong to separate specialist bundles.

Godot imports, visual material review, global licensing checks and mission coverage are integrated by the coordinator and independent reviewer. This document does not substitute machine decoding for listening or texture decoding for a visual quality approval. No gameplay implementation was added.

## Godot audio repair follow-up
Actual Godot imports rejected unsupported WAVE encodings. All 113 new WAV runtime clips were converted to standard PCM16, while preserving original downloaded archives. The multichannel electronic-device recording was downmixed to stereo and written with a standard PCM format1 RIFF header. A byte-level header audit verified format1 for every new WAV. Manifest runtime hashes were refreshed. This format repair does not remove clipping already present in source audio or replace audition requirements.

