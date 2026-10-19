# Final isolated engine validation — 19 October 2026

Godot 4.7.2 stable Steam loaded all eight resources in the isolated `asset_library/converted/acquisition_20261019/material_validation` project. Import and validation each exited 0. The final JSON has `failed: false`: six new StandardMaterial3D resources have 2048-square albedo/normal maps and assigned roughness/AO; five use packed metallic maps, while woven fabric is nonmetallic. Flashlight and single-radio GLBs instantiate with six and sixteen mesh instances respectively and zero null material assignments.

Evidence: `material_validation/godot_report.json`, `import_fixed_stdout.log`, `import_fixed_stderr.log`, `validate_fixed_stdout.log`, `validate_fixed_stderr.log` under the converted dated folder. Runtime copies are separate candidate resources; no existing game actor or scene was replaced.

The first attempt failed because copying the provider's Blender authoring file into the staged runtime triggered Godot's unconfigured Blender importer and prevented other resources importing. The final isolated project disables automatic Blender import; duplicate provider authoring files were removed from the new runtime fabric folder only after exact hash comparison with their preserved extracted-source copies. Source ZIP, Blender file, MaterialX and provider material remain preserved in extracted_sources. The custom Godot material and texture maps remain in assets/materials. Failed attempt logs are retained.

Three additional Sketchfab static derivatives passed isolated Godot instantiation with zero null material assignments; see sketchfab_godot_validation.json and SKETCHFAB_CONVERSION_REPORT.md. Six facial character derivatives passed their separate structural engine checks; see the facial conversion report. Headless loading does not certify rendered gameplay, contacts, collisions, navigation, light emitters, LODs or split-screen performance.

Blender actual renders were reviewed for all new static prop candidates and six material spheres. Radio rear view and final game-scene rendering remain NOT TESTED. Character hair transparency artefacts and cinematic performances remain open.
