from pathlib import Path
import json, hashlib, shutil, zipfile
R=Path(__file__).resolve().parents[1]
def write(p,s):
    f=R/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s,encoding='utf-8')
records=json.loads((R/'asset_library/manifests/acquired.json').read_text())
checks=json.loads((R/'asset_library/manifests/download_checks.json').read_text())
godot=json.loads((R/'asset_library/manifests/godot_resource_validation.json').read_text())
for a in records:
    a['import_status']='PASS'
    a['validation_status']='PASS' if a['category']=='model' else 'NOT TESTED'
    if a['category']=='model':
        result=next(x for x in godot if x['path'][6:] in a['runtime_file'])
        a['polygon_count_if_known']=result['geometry']['triangles']
        a['notes']='Godot resource load and single-angle rendered visual inspection PASS; no missing active materials. Static mesh only; collision, modular fit, LOD and gameplay performance NOT TESTED. Bounds: '+result['bounds_m']
    else:a['notes']='Image verification and Godot importer artifacts PASS; PBR material assembly, tiling and rendered application NOT TESTED. 1k acquisition preview tier; upgrade after texel-density tests.'
z=R/'asset_library/original_downloads/kenney_impact-sounds.zip'
with zipfile.ZipFile(z) as archive:
    assert archive.testzip() is None
audio=sorted((R/'assets/audio').glob('*.ogg'))
records.append(dict(asset_id='AUDIO_FOLEY',asset_name='Kenney concrete footsteps and metal impacts',category='audio',source_url='https://kenney.nl/assets/impact-sounds',creator='Kenney',license='CC0-1.0',attribution_required=False,original_file=str(z.relative_to(R)).replace('\\','/'),original_checksum=hashlib.sha256(z.read_bytes()).hexdigest(),runtime_file=[str(p.relative_to(R)).replace('\\','/') for p in audio],format='OGG Vorbis',polygon_count_if_known=None,texture_resolution_if_known=None,skeleton_type_if_applicable=None,animation_compatibility='event driven',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='DOWNLOADED',import_status='PASS',validation_status='NOT TESTED',notes='Archive CRC PASS; selected audio loads and positive duration PASS. Decoded waveform PASS (max peak0.898954, zero full-scale samples); listening NOT TESTED; this is partial foley, not prison ambience.'))
missing={
'CHAR_ADRIAN':('character','Adrian 34 realistic prison uniform, facial rig, 1.84m','all'),
'CHAR_NOAH':('character','Noah 29 realistic prison uniform, facial rig, 1.78m','all'),
'CHAR_RUSK':('character','Rusk guard uniform radio holster keys','1,2,3,4,6'),
'CHAR_MARA':('character','Dr Mara Sen medical textiles inspector coat and badge','3'),
'CHAR_SILAS':('character','Silas Bell yard broker prison uniform','2'),
'CHAR_GUARD':('character','Guard variants with radio and restraints for interception','all'),
'CHAR_INMATE':('character','Seated and working inmate crowd variants','1,2,3'),
'PROP_PHOTO':('prop','Elena photo readable front and custody sleeve','1,2,6'),
'PROP_VANTAGE_BADGE':('prop','Original VANTAGE split-chevron seal on guard transfer clipboard','1,6'),
'PROP_DIAGRAM':('prop','Maintenance diagram with separate service routes and fictional selector labels','3'),
'PROP_SHIM':('prop','Rounded laundry shim cinematic close-up and confiscation','3,4,5,6'),
'PROP_RELAY':('prop','Fictional A/B/C selector console, lamp states, held brake wheel and door interlock; select B while brake held','5'),
'PROP_LEDGER':('prop','Numbered transfer evidence and later VANTAGE ledger; later chapter full ledger','1,6'),
'ENV_INTAKE':('environment','Gate, bus exterior/interior, intake corridor counter scanner cage clipboard benches property tray','1'),
'ENV_CELLBLOCK':('environment','Two-level modular cellblock, cell doors bunks mattresses sink toilet rails stairs clinic envelope patrol clock restricted door solitary','1,4,6'),
'ENV_YARD':('environment','Fence watchtower exercise bench basketball court barrier tray return cover crowd','2'),
'ENV_WORKSHOP':('environment','Laundry industrial washer drum stopped service hatch power isolator workbenches ducts diagram board shelves linens safe tool tray','3'),
'ENV_MAINTENANCE':('environment','Modular corridors crawlspace dry service trench cable trays nonenergized relay panel crank hatch final door capture bay; no real wiring instructions','4,5,6'),
'ANIM_HUMANOID':('animation','Locomotion and all interaction/cinematic takes per ANIMATION_REQUIREMENTS.md; retargeting and two-body sync required','all'),
'AUDIO_PRISON':('audio','Ocean wind bus engine gate keys scanner crowd PA machine hum patrol radio electrical ambience alarm door restraint taps original dialogue VO score','all'),
'UI_SUBTITLES':('ui','Readable subtitle font licensed for distribution, speaker labels player icons prompts pause retry UI','all'),
'VFX_ALARM':('vfx','Alarm beacon emissive pulsing, dust and vent particles, no strobe by default','4,5,6')}
for aid,(cat,name,missions) in missing.items():
    nums=range(1,7) if missions=='all' else map(int,missions.split(','))
    records.append(dict(asset_id=aid,asset_name=name,category=cat,source_url=None,creator=None,license=None,attribution_required=None,original_file=None,original_checksum=None,runtime_file=None,format=None,polygon_count_if_known=None,texture_resolution_if_known=None,skeleton_type_if_applicable='proposed Godot humanoid mapped rig' if cat in ['character','animation'] else None,animation_compatibility='NOT TESTED',required_by_scene=['CH01_M%02d_SC01'%i for i in nums],download_status='MISSING',import_status='BLOCKED',validation_status='BLOCKED',notes='Requirement bundle; all named components must be supplied, separate subasset records before integration. No approved deliverable/source selected.'))
write('asset_library/manifests/assets.json',json.dumps(records,indent=2))
write('ASSET_MANIFEST.md','# Asset manifest\n\n[Machine-readable authority](asset_library/manifests/assets.json). '+str(len(records))+' requirement records, '+str(sum(a['download_status']=='DOWNLOADED' for a in records))+' acquired records. A record may contain several files or an explicitly enumerated missing bundle; record count is not file count.\n\n| ID | Requirement | Acquisition | Validation |\n|---|---|---|---|\n'+'\n'.join('| '+a['asset_id']+' | '+a['asset_name']+' | '+a['download_status']+' | '+a['validation_status']+' |' for a in records)+'\n\n[Requirements](docs/assets/ASSET_REQUIREMENTS.md) · [licenses](docs/assets/ASSET_LICENSES.md) · [gaps](docs/assets/ASSET_GAPS.md) · [validation](docs/assets/ASSET_VALIDATION_REPORT.md).\n')
write('docs/assets/ASSET_REQUIREMENTS.md','# Chapter 1 asset requirements\n\nDerived from six mission beats and five environment specifications. Asset IDs are stable; do not substitute a source model for an entire room kit. P1 Adrian, P2 Noah. [Manifest](../../asset_library/manifests/assets.json) contains exact scope of each bundled requirement and required scene IDs.\n\n'+ '\n'.join('- **'+aid+'**: '+name+'. Missions '+m+'.' for aid,(c,name,m) in missing.items())+'\n\nAvailable additions: PROP_SCONCE caged lamp variants; PROP_CART laundry service cart; PROP_PIPES maintenance pipe modules; MAT_CONCRETE and MAT_METAL 1k source maps; AUDIO_FOLEY footsteps and impacts. These only partially satisfy environment/audio bundles. Facial blendshapes, uniform skinning, contact poses, six cinematic performances, accessible font, collision and navigation are required deliverables. Later chapter characters Elena/Voss/Vale and environments remain concept-only; acquire after Chapter 1 gate.\n\nBudgets are proposals: heroes 35–70k triangles LOD0, background 15–30k; 2k hero maps with 4k face only if measured; static repeated props 1–10k after LOD; 60fps split-screen target on hardware to be selected. No budget is validated by these source downloads.\n')
write('docs/assets/ASSET_SOURCES.md', '''# Source research and acquisition — 2026-10-18

| Source | Evidence / disposition |
|---|---|
| [Poly Haven](https://polyhaven.com) | Acquired 1k maps and three static props using provider file API; response snapshots, include dependencies, MD5 and local SHA-256 retained. Powered by Poly Haven. |
| [ambientCG](https://ambientcg.com/view?id=Concrete034) | Concrete candidate; not acquired because selected Poly Haven concrete covers initial material test. Not an approved substitute until inspected. |
| [Kenney Impact Sounds](https://kenney.nl/assets/impact-sounds) | Acquired official ZIP, preserved full extraction and license; selected concrete steps and metal impacts copied to runtime. |
| [Quaternius Universal Base Characters](https://quaternius.com/packs/universalbasecharacters) | Source-reviewed base character candidate, not acquired: proportions/style do not establish realistic named-character likeness or prison outfits. |
| [Mixamo](https://www.mixamo.com) | Animation candidate; account-mediated character/clip selection and commercial terms verification remain outstanding. No authenticated session used, no clips downloaded. |
| [Sketchfab Prison Cell](https://sketchfab.com/3d-models/prison-cell-441777a337154b85aefaa5740c359504) | Listing identifies CC Attribution and download availability; not acquired or license-approved, authorized download session and exact license version/package inspection outstanding. |
| [Fab](https://www.fab.com) | No exact free realistic prison package approved; entitlement and product-specific license must be checked before download. |
| [OpenGameArt](https://opengameart.org) | No exact realistic character/prison package approved. Site-wide licensing cannot authorize individual submissions. |

Do not use mirrors of Mixamo dumps. No paywall or access controls bypassed. Direct provider delivery URLs live in download_checks.json; source page per asset in assets.json. Individual Poly Haven files are originals, not fabricated archives. No conversion was necessary for native glTF assets.
''')
write('docs/assets/ASSET_LICENSES.md','''# License register

Downloaded Poly Haven assets: [CC0 policy](https://polyhaven.com/license), [CC0 legal text](https://creativecommons.org/publicdomain/zero/1.0/legalcode). Five provider source metadata snapshots in asset_library/licenses preserve authors and asset metadata; policy snapshot retained alongside them. Asset page URLs and file checksums in manifest. Attribution not required for the assets; API credit: **Powered by Poly Haven**.

Kenney Impact Sounds: official archive License.txt copied verbatim to asset_library/licenses/Kenney_Impact_Sounds_License.txt. [Provider support](https://kenney.nl/support) and [asset page](https://kenney.nl/assets/impact-sounds) identify CC0. Attribution not required; credit Kenney voluntarily. Preserve original ZIP and license when redistributing the library. Branding and linked websites are not game assets.

Only downloaded records have cleared CC0 provenance. All MISSING records have null license/source and are BLOCKED for shipping. Candidate pages are research, not proof of a downloaded license. Original story and project documents are newly authored project material; third-party rights of future fonts, faces, voices and uniforms still require individual checks.
''')
write('docs/assets/ASSET_GAPS.md','# Outstanding acquisition requirements\n\nAsset readiness gate: **BLOCKED**. Realistic named characters, skinned outfits, locomotion and contact animations, complete prison architecture, bespoke story props, ambience/voice/score, subtitle font and UI art remain missing. These cannot be replaced by the three downloaded static props.\n\n'+ '\n'.join('- **'+aid+'** — '+name+'. Owner: acquisition / character / environment team; license and actual deliverable required before import.' for aid,(c,name,m) in missing.items())+'\n\nRemediation order: lock humanoid rest pose → secure character deliverables → retarget sample locomotion → commission interactions → prison modular kit/collision → story props/readability → full ambience/VO → UI/VFX. For account-mediated providers, user-authorized login/entitlement is required; no claim that every candidate has been attempted or downloaded. Available approved selections were downloaded; discovery of all possible free assets is not exhaustive.\n')
write('docs/assets/ASSET_VALIDATION_REPORT.md', '''# Asset validation report — 2026-10-18

Scope: real downloads and Godot 4.7.2.stable.steam.ed1daf0bf on Windows. No gameplay implemented. PASS means only the named test passed. NOT TESTED is never PASS.

| Test | Result | Evidence / limits |
|---|---|---|
| Provider checksums | PASS | 25 Poly Haven files match provider MD5; SHA-256 and byte sizes in download_checks.json (read actual count there). |
| Kenney archive integrity | PASS | Python ZipFile.testzip returns no corrupt member; original ZIP SHA-256 in manifest. |
| PNG/JPEG decode | PASS | Pillow verify on downloaded maps; no image decode errors. |
| Godot imports / resource load | PASS | Three glTF scenes, external bins/textures resolved; selected OGG load and positive duration; machine output godot_resource_validation.json. Texture .import resources generated. |
| Static model visual inspection | PASS | Three rendered PNG previews inspected: cart textured, pipe modules intact, lamp variant/component atlas visible. One camera only; no exhaustive topology review. |
| Material assignment | PASS | 20 MeshInstance3D surfaces total, no null active materials; diffuse/roughness appear in previews. Does not certify physically correct calibrated values. |
| Scale / orientation | NOT TESTED | Imported AABBs recorded below; plausible human-sized props, no measured reference object or modular snap test. Godot Y-up render upright. |
| Collision / navigation / performance | NOT TESTED | No gameplay level, collision generation, navigation bake, LOD, split-screen GPU budget, or repeated-instance test. |
| Characters / skin / skeleton | BLOCKED | No character downloads; bone map, skin deformation and proportions cannot be tested. |
| Animations / root motion / sliding | BLOCKED | No animation deliverables. |
| Audio decoded waveform | PASS | FFmpeg decoded all 20 selected OGGs: maximum sample peak 0.898954, zero samples at/above full scale. audio_waveform_validation.json. This does not exclude source clipping below full scale. |
| Audio listening / mix suitability | NOT TESTED | No listening session or in-scene mix review. |
| Concrete/metal PBR assembly | NOT TESTED | Maps verified and imported, no assembled/rendered wall material. |

Geometry: lamp 26,576 triangles / 11 meshes (multiple variants and loose parts, isolate selected variant); cart 18,902 / 1 mesh (1.603 × 1.377 × 1.103 m); pipe collection 12,340 / 8 meshes. Triangle counts are Godot primitive counts, not source quads. Lamp and pipe aggregate bounds cover source layout, not an individual module. These source models need LOD/collision authoring before repeated scene use.

Evidence: [resource JSON](../../asset_library/manifests/godot_resource_validation.json), [file checks](../../asset_library/manifests/download_checks.json), [cart render](../../asset_library/manifests/industrial_storage_cart_1k_preview.png), [lamp render](../../asset_library/manifests/industrial_caged_sconce_1k_preview.png), [pipes render](../../asset_library/manifests/modular_industrial_pipes_01_1k_preview.png). Empty GUI stdout logs alone are not proof; JSON and saved framebuffer images prove this invocation executed. Reproduce: import editor first, then run tools/validate_resources.gd using a real rendering backend (GL compatibility used). Headless dummy rendering does not certify visuals.

Overall asset acceptance: BLOCKED by explicitly inventoried missing requirements. No 3D conversion performed because selected assets already provide glTF 2.0. No runtime-ready completeness claimed.
''')
print(len(records),'records',len(checks),'provider files',len(audio),'runtime audio files')

