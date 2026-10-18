# Chapter 1 asset requirements

Derived from six mission beats and five environment specifications. Asset IDs are stable; do not substitute a source model for an entire room kit. P1 Adrian, P2 Noah. [Manifest](../../asset_library/manifests/assets.json) contains exact scope of each bundled requirement and required scene IDs.

- **CHAR_ADRIAN**: Adrian 34 realistic prison uniform, facial rig, 1.84m. Missions all.
- **CHAR_NOAH**: Noah 29 realistic prison uniform, facial rig, 1.78m. Missions all.
- **CHAR_RUSK**: Rusk guard uniform radio holster keys. Missions 1,2,3,4,6.
- **CHAR_MARA**: Dr Mara Sen medical textiles inspector coat and badge. Missions 3.
- **CHAR_SILAS**: Silas Bell yard broker prison uniform. Missions 2.
- **CHAR_GUARD**: Guard variants with radio and restraints for interception. Missions all.
- **CHAR_INMATE**: Seated and working inmate crowd variants. Missions 1,2,3.
- **PROP_PHOTO**: Elena photo readable front and custody sleeve. Missions 1,2,6.
- **PROP_VANTAGE_BADGE**: Original VANTAGE split-chevron seal on guard transfer clipboard. Missions 1,6.
- **PROP_DIAGRAM**: Maintenance diagram with separate service routes and fictional selector labels. Missions 3.
- **PROP_SHIM**: Rounded laundry shim cinematic close-up and confiscation. Missions 3,4,5,6.
- **PROP_RELAY**: Fictional A/B/C selector console, lamp states, held brake wheel and door interlock; select B while brake held. Missions 5.
- **PROP_LEDGER**: Numbered transfer evidence and later VANTAGE ledger; later chapter full ledger. Missions 1,6.
- **ENV_INTAKE**: Gate, bus exterior/interior, intake corridor counter scanner cage clipboard benches property tray. Missions 1.
- **ENV_CELLBLOCK**: Two-level modular cellblock, cell doors bunks mattresses sink toilet rails stairs clinic envelope patrol clock restricted door solitary. Missions 1,4,6.
- **ENV_YARD**: Fence watchtower exercise bench basketball court barrier tray return cover crowd. Missions 2.
- **ENV_WORKSHOP**: Laundry industrial washer drum stopped service hatch power isolator workbenches ducts diagram board shelves linens safe tool tray. Missions 3.
- **ENV_MAINTENANCE**: Modular corridors crawlspace dry service trench cable trays nonenergized relay panel crank hatch final door capture bay; no real wiring instructions. Missions 4,5,6.
- **ANIM_HUMANOID**: Locomotion and all interaction/cinematic takes per ANIMATION_REQUIREMENTS.md; retargeting and two-body sync required. Missions all.
- **AUDIO_PRISON**: Ocean wind bus engine gate keys scanner crowd PA machine hum patrol radio electrical ambience alarm door restraint taps original dialogue VO score. Missions all.
- **UI_SUBTITLES**: Readable subtitle font licensed for distribution, speaker labels player icons prompts pause retry UI. Missions all.
- **VFX_ALARM**: Alarm beacon emissive pulsing, dust and vent particles, no strobe by default. Missions 4,5,6.

Available additions: PROP_SCONCE caged lamp variants; PROP_CART laundry service cart; PROP_PIPES maintenance pipe modules; MAT_CONCRETE and MAT_METAL 1k source maps; AUDIO_FOLEY footsteps and impacts. These only partially satisfy environment/audio bundles. Facial blendshapes, uniform skinning, contact poses, six cinematic performances, accessible font, collision and navigation are required deliverables. Later chapter characters Elena/Voss/Vale and environments remain concept-only; acquire after Chapter 1 gate.

Budgets are proposals: heroes 35–70k triangles LOD0, background 15–30k; 2k hero maps with 4k face only if measured; static repeated props 1–10k after LOD; 60fps split-screen target on hardware to be selected. No budget is validated by these source downloads.
