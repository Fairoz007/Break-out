"""Write ASSET_MANIFEST.md and docs/assets/ASSET_GAPS.md from assets.json + integration_summary.json (run after phase15_finalize.py)."""
import json, collections
from pathlib import Path
R = Path(__file__).resolve().parents[1]
A = json.loads((R / 'asset_library/manifests/assets.json').read_text(encoding='utf-8'))
S = json.loads((R / 'asset_library/manifests/phase15/integration_summary.json').read_text())
B = S['bundles']; new = [a for a in A if a.get('asset_role') not in ('requirement_bundle', 'acquired_phase01')]
cat = collections.Counter(a['category'] for a in new); use = collections.Counter(a['category'] for a in new if a.get('usable'))
L = ['# Asset manifest — Phase 01.5', '',
     f"[Machine-readable authority](asset_library/manifests/assets.json): **{S['records_total']} records**. That is 28 Phase 01 records (6 acquired, 22 requirement bundles) plus {S['phase15_records']} Phase 01.5 catalogue records. "
     f"**{S['usable']} are usable**: they load in Godot 4.7.2 and pass file, licence and checksum checks. 25 audio candidates are REJECTED, 4 MPFB characters FAILED and 2 diagnostic proxies are SUPERSEDED. "
     f"Godot: {S['godot_load_verified']}/{S['godot_jobs']} resource jobs load (the job count includes texture and bin dependencies). A material set counts as one asset; texture channels, source/runtime copies and the 37 clips embedded per character are not counted separately.", '',
     '| Category | Records | Usable |', '|---|---:|---:|'] + [f'| {k} | {v} | {use.get(k, 0)} |' for k, v in sorted(cat.items())] + ['',
     '## The 22 original requirement bundles', '',
     '**Functional** = a usable asset covers the need now (realistic, construction-grade or proxy). **Production** = the intended realistic/cinematic standard. A functional proxy never closes a production requirement.', '',
     '| Bundle | Priority | Functional | Production | Children (usable/total) | Godot | Licence | Missions | Remaining |', '|---|---|---|---|---|---|---|---|---|']
for k, e in B.items():
    L.append(f"| `{k}` | {e['priority']} | {e['functional_status']} | {e['production_status']} | {e['verified_usable']}/{e['available']} | {e['godot_import']} | {e['license']} | {', '.join(m.split('_SC')[0].replace('CH01_', '') for m in e['missions'])} | {e['missing']} |")
L += ['', f"Totals: functional {S['bundle_functional']}; production {S['bundle_production']}.", '',
      'Exact child IDs, paths, checksums and scoped evidence are in each bundle record (`child_asset_ids`). See also: [coverage matrix](docs/qa/ASSET_COVERAGE_MATRIX.md) · [Phase 01.5 report](docs/qa/PHASE_01_5_REPORT.md) · [validation](docs/assets/ASSET_VALIDATION_REPORT.md) · [licences](docs/assets/ASSET_LICENSES.md) · [discovery](docs/assets/PHASE15_DISCOVERY.md).', '']
(R / 'ASSET_MANIFEST.md').write_text('\n'.join(L), encoding='utf-8')
G = ['# Remaining asset gaps — Phase 01.5', '',
     'Generated from `asset_library/manifests/phase15/integration_summary.json`. Quantity is not readiness. Optional dressing never blocks implementation.', '',
     '| Bundle | Production | Gap |', '|---|---|---|'] + [f"| `{k}` | {e['production_status']} | {e['missing']} |" for k, e in B.items() if e['production_status'] != 'PASS'] + ['',
     'Account-gated sources (Freesound, Sketchfab, Mixamo, Fab) were not accessed. Candidates found there are listed in [PHASE15_DISCOVERY.md](PHASE15_DISCOVERY.md) and need the owner\'s own login and licence acceptance.', '']
(R / 'docs/assets/ASSET_GAPS.md').write_text('\n'.join(G), encoding='utf-8'); print('ok', S['bundle_functional'], S['bundle_production'])
