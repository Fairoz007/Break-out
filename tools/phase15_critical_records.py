"""Manifest fragment for original mission-critical assets built by tools/phase15_critical_props.py."""
import json, hashlib
from pathlib import Path
R = Path(__file__).resolve().parents[1]
rep = json.loads((R / 'asset_library/extracted_sources/phase15_architecture/critical/critical_props_report.json').read_text())
meta = {'basketball': ('P15_BASKETBALL', 'prop', 'PROP_BALL', ['CH01_M02'], 'Size-7 ball (0.238 m) for M02 roll distraction; procedural orange leather with black seam bands (blocky seams, no pebble texture).'),
        'pump_unit': ('P15_PUMP_UNIT', 'prop', 'ENV_MAINTENANCE', ['CH01_M05'], 'Horizontal centrifugal pump on skid and plinth: motor, coupling guard, volute, suction/discharge pipes with flanges, nameplate, ledger_inspect_marker empty. Static; no rotating parts.'),
        'security_grille_4m': ('P15_SECURITY_GRILLE_4M', 'environment', 'ENV_MAINTENANCE', ['CH01_M05', 'CH01_M06'], '4.0 m x 3.0 m clear lifting grille: fixed guides/header/threshold, separate grille_leaf node (pivot bottom centre, animate +Y to 2.9 m), drive_housing with motor/gearbox/sprocket, limit switch, latch_point empty.')}
lic = 'asset_library/licenses/phase15_architecture/LICENSE.md'
recs = []
for stem, (aid, cat, bundle, missions, note) in meta.items():
    v = rep[stem]
    recs.append({'asset_id': aid, 'asset_name': stem, 'category': cat, 'source_url': None, 'creator': 'Project original (Blender 5.1.1 script)',
                 'license': 'Project original', 'attribution_required': False, 'license_record': lic, 'license_file': lic,
                 'original_file': v['source'], 'original_checksum': hashlib.sha256((R / v['source']).read_bytes()).hexdigest(),
                 'runtime_file': v['runtime_file'], 'runtime_checksum': v['sha256'], 'format': 'GLB', 'polygon_count_if_known': v['triangles'],
                 'dimensions_m': v['dims_xyz_m_blender'], 'required_by_scene': missions, 'download_status': 'ORIGINAL_CREATED',
                 'import_status': 'PENDING_GODOT_CHECK', 'validation_status': 'PARTIALLY_VERIFIED', 'requirement_bundle': bundle,
                 'build': 'tools/phase15_critical_props.py', 'visual_evidence': 'asset_library/manifests/phase15/previews_critical/' + stem + '.png',
                 'notes': note + ' Construction-grade original geometry with flat procedural materials; not photoreal. Collision/nav and motion untested.'})
(R / 'asset_library/manifests/phase15_critical_records.json').write_text(json.dumps(recs, indent=2))
print(len(recs))
