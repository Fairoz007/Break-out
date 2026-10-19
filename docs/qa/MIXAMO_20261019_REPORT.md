# Mixamo acquisition and compatibility — 19 October 2026

14 actual FBX Binary downloads were acquired through the authenticated official Mixamo UI. Every original is preserved in `asset_library/original_downloads/animations/mixamo_20261019`; no purchase was required. `inventory.json` and CSV in `asset_library/manifests/mixamo_20261019` record original and converted SHA256, size, source, license and scoped statuses. The first opening-door clip includes the default reference character; the other 13 deliberately contain animation skeletons without skins. This character is not an approved protagonist asset.

Adobe's official Mixamo FAQ permits royalty-free use in commercial video games. Local HTML and license record are preserved in `asset_library/licenses/mixamo_20261019`. These dependencies are retained internally; no independent asset-library redistribution permission is inferred. The official page URL is https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html . UI_ACQUISITION_RECORD.md records exact observed descriptions/settings. Query URLs identify searches, not permanent item IDs.

## Actual acquired coverage

Door inward/outward, cabinet closure, turn left/right90, lever pulling, heavy-object pull start/loop/stop, kneel transition, kneeling inspection, general conversation, standing argument and forward pointing. Cabinet closure is not validated prison-gate closure. Kneeling is not an arrest performance. Dialogue gestures do not supply facial acting or synchronized lines. Pulling is a single actor reference, not validated cooperative choreography.

## Conversion and engine evidence

Blender5.1.1 imported all14 FBX files and exported14 GLBs. Each has one armature and one source action with65 Mixamo bones. Converted GLBs are in `asset_library/converted/mixamo_20261019`. Original WithSkin reference mesh material is retained; no-skin clips have no texture requirement. Blender structural details are in blender_validation.json.

Two isolated facial-rest Rocketbox trials, rb_adrian_cross and rb_noah_reyes, contain all14 transferred actions. Retargeting maps body/finger names, applies rest-relative world quaternion rotation with bone-direction swing, and scales pelvis displacement by hip height and source parent scale. Existing canonical actor resources were not replaced. The output hashes and per-action frame counts are in retarget_trial.json.

Godot4.7.2 stable Steam imported and instantiated all16 resources (14 source GLBs plus2 hero trials); each source has1 action and each hero trial14 actions. Final headless import and validation each exited0. `asset_library/converted/mixamo_20261019/godot_validation/godot_report.json` has failed:false. This validates engine structure and animation-track presence, not gameplay contacts or rendered performance.

Six selected static frames were rendered on CPU Cycles: opening-door midpoint, heavy pull midpoint and left-turn70percent for each hero. Reviewed frames show coherent full-body anatomy and materials without obvious catastrophic deformation. Other clips and full animation playback remain NOT TESTED. These renders contain no staged doors, partners or props; physical contacts remain unverified.

## Failures and correction

Eevee rendering crashed with a WGL access violation; log retained. CPU Cycles succeeded. An initial trial inherited a preexisting UAL-transfer assumption that ignored Mixamo's0.01 parent scale in animated source translations. This displaced the pelvis and produced unusable tiny-subject renders. The isolated Mixamo wrapper now applies source parent scale, regenerated the two trials and six static pose renders, and reran final Godot checks. Shared canonical scripts/resources were not altered. Logs preserve the failed attempts. Initial male_adult_01 trial is exploratory only and is superseded by the two named hero trials.

## Readiness and remaining work

The14 source actions and two hero evaluations are candidates for Phase02 animation integration. They are not final cinematic performances. Required work includes full-motion visual review, root-motion policy, foot sliding/locking, hand contacts, exact door dimensions, prop sockets, collision/navigation, clip blending, split-screen budget, and authored timing. Paired assisted climb/help-up/dual-handle actions, cuff placement/cuffed walking, controlled capture, final facial performances and other uncovered requirements remain open. No mission is declared asset-complete by these additions.
