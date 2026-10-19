"""Supplement all 22 baseline bundles with scoped acquisition progress."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'asset_library/manifests/acquisition_20261019'
baseline=json.loads((D/'baseline_audit.json').read_text())['bundles']
progress={
 'CHAR_ADRIAN':('FACIAL_20261019_RB_ADRIAN_CROSS','175 facial targets now exported; 14 Mixamo clips have isolated retarget trials. Layered garments, likeness/scars, hair/materials, authored facial performance and contacts remain.'),
 'CHAR_NOAH':('FACIAL_20261019_RB_NOAH_REYES','175 facial targets now exported; 14 Mixamo clips have isolated retarget trials. Wavy hair/likeness/burn, undershirt, photo contact, materials and facial performance remain.'),
 'CHAR_RUSK':('FACIAL_20261019_RB_TOMAS_RUSK, ACQ26_YAESU_RADIO, SF_SIMPLE_HANDCUFFS','Facial controls and realistic radio/static cuffs candidates now exist. Body build, distinct guard identities, holster/keys/band attachment, restraint articulation and performance remain.'),
 'CHAR_MARA':('FACIAL_20261019_RB_MARA_SEN','Facial controls exported; age/hair/likeness, cardigan/badge and clinical performance remain.'),
 'CHAR_SILAS':('FACIAL_20261019_RB_SILAS_BELL','Facial controls exported; patched clothing, chipped incisor, likeness and performance remain.'),
 'CHAR_GUARD':('FACIAL_20261019_RB_TOMAS_RUSK, ACQ26_YAESU_RADIO, SF_SIMPLE_HANDCUFFS','Shared Rusk facial derivative and equipment candidates exist. More identities, uniform/equipment attachments, articulated restraints and performance remain.'),
 'CHAR_INMATE':('FACIAL_20261019_RB_PRISONER_NPC','Facial controls exported; crowd diversity, seated/working variants and performance remain.'),
 'ENV_INTAKE':('SF_SIMPLE_HANDCUFFS','Body scanner and realistic prison transport interior remain missing. Textured CC-BY transit bus candidate on BlendSwap awaits owner login and still requires a prison refit. Final route/collision/nav remain.'),
 'ENV_YARD':('SF_GUARD_TOWER','Realistic static tower candidate acquired, Blender rendered and Godot load checked, replacing need for medieval stand-in during art trials. Tower 1k maps, light/collision/clearance and court/tray return/scene work remain.'),
 'ENV_WORKSHOP':('SF_INDUSTRIAL_DRYER_IRONING, ACQ26_FABRIC030, ACQ26_SIGNAL_FLASHLIGHT','Textured laundry/ironing equipment, woven linen material and small inspection/emergency light acquired. Linen stack geometry, mission press lever/screen/hand contacts, room assembly/collision/nav remain.'),
 'ANIM_HUMANOID':('14 MIXAMO_* source records; 2 isolated hero trials','14 missing motion candidates downloaded: door opening, cabinet closing, turn L/R90, lever, heavy pull start/loop/stop, kneel/inspect, talk/argue/point. Structural retarget and selected static frames are limited evidence. Full cycles, root motion/feet, exact door/prop/paired contacts, restrained escort, help-up/assisted climb and facial performances remain.'),
}
out=['# Current reconciliation of all 22 original bundles - 19 October 2026','','This supplements the baseline reconciliation and historical canonical records. Acquired candidates and scoped checks do not establish production readiness. No bundle is promoted to production complete.','','| Bundle | Baseline functional / production | New scoped evidence | Current remaining requirement |','|---|---|---|---|']
rows=[]
for b in baseline:
 aid=b['asset_id'];e,g=progress.get(aid,('No bundle-specific closure this session',b['missing']))
 rows.append({'asset_id':aid,'baseline_functional':b['functional_status'],'production_status':b['production_status'],'new_evidence':e,'remaining_requirement':g})
 out.append(f"| {aid} | {b['functional_status']} / {b['production_status']} | {e} | {g} |")
(D/'CURRENT_BUNDLE_RECONCILIATION.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
(D/'current_bundles.json').write_text(json.dumps(rows,indent=2))
print(len(rows),'bundles updated with scoped progress')
