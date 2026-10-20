"""Read-only structural audit of the actual character runtime payloads.

Outputs only the owned character audit document; never changes canonical models.
"""
from pathlib import Path
import hashlib, json, struct

R = Path(__file__).resolve().parents[1]

def inspect(p):
    b = p.read_bytes()
    magic, version, length = struct.unpack_from('<III', b)
    assert magic == 0x46546c67 and version == 2 and length == len(b), p
    n = struct.unpack_from('<I', b, 12)[0]
    j = json.loads(b[20:20+n])
    triangles = sum(j['accessors'][q['indices']]['count']//3 for m in j.get('meshes',[]) for q in m['primitives'] if q.get('mode',4)==4 and 'indices' in q)
    return dict(path=p.relative_to(R).as_posix(), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), triangles=triangles, joints=sum(len(s['joints']) for s in j.get('skins',[])), animations=[a.get('name','') for a in j.get('animations',[])], morphs=max([len(q.get('targets',[])) for m in j.get('meshes',[]) for q in m['primitives']]+[0]), materials=len(j.get('materials',[])), normal_maps=sum('normalTexture' in m for m in j.get('materials',[])))

rows = [inspect(p) for p in sorted((R/'assets/characters/acquisition_20261019/rocketbox_facial').glob('*.glb'))]
trials = [inspect(p) for p in sorted((R/'asset_library/converted/mixamo_20261019/retarget_trials').glob('*.glb'))]
out = '''# Phase 04 character and animation audit

Date: 20 October 2026. Result: INCOMPLETE. This audit inspected actual GLB headers, mesh index counts, skins, animation names and material definitions. It also visually inspected the existing Godot captures `docs/phase04/visual_evidence/iter02/adrian_close.png` and `noah_close.png`. These are historical baseline captures, not newly rendered proof. No character replacement was integrated by this audit.

## Runtime reuse decision

`scripts/player/character_visual.gd` loads the six facial Rocketbox derivatives below. GUARD and RUSK share the same model. These are recognisable human models with believable anatomy, facial geometry, clothing folds and skinned hands. They are usable candidates for medium-distance gameplay. They do not satisfy the requested final cinematic quality: Adrian retains long swept hair and an orange sweater; Noah retains jacket seams and chest pockets; hair reads as a solid cap, faces lack modern skin response, and likeness/garment corrections are still required. Recolouring these assets again would not solve the geometry deficiencies.

No specific separate prison officer or workshop staff model is wired in the model dictionary. Do not claim dedicated coverage from the generic guard/inmate aliases.

## License and originals

Official source: https://github.com/microsoft/Microsoft-Rocketbox . Individual source families are Adult Male 02 (Adrian), Adult Male 12 (Noah), Adult Male 11 (Silas), Adult Male 14 (inmate), Security Male 01 (Rusk/guard), and Medical Female 01 (Mara). Original FBX and facial FBX files are preserved under `asset_library/original_downloads/phase15_discovery/microsoft_rocketbox/`. The repository MIT license was rechecked against https://github.com/microsoft/Microsoft-Rocketbox/blob/master/LICENSE.md ; local notice is `asset_library/licenses/phase15_discovery/microsoft_rocketbox/LICENSE.md`. Preserve the Microsoft copyright and MIT notice in distribution. The repository describes its own meshes as relatively low poly; more animation or textures do not make them an ultra-realistic replacement.

The bulk Phase 02.5 inventory is predominantly environment models/materials and is not an alternative source of protagonist humans. Earlier MPFB candidates were explicitly rejected after repeated retarget and garment deformation failures (`asset_library/manifests/phase15_characters_records.json`); do not reactivate them as quality upgrades. UBC candidates are also earlier evaluation alternatives, not approved final characters.

## Actual payload inspection

| Runtime file | Triangles | Joints | Clips | Facial targets | Materials / normal maps | Status |
|---|---:|---:|---:|---:|---:|---|
'''
for r in rows:
    out += f"| `{r['path']}` | {r['triangles']} | {r['joints']} | {len(r['animations'])} | {r['morphs']} | {r['materials']} / {r['normal_maps']} | INTEGRATED, not VERIFIED |\n"
out += '''
## Animation coverage and blockers

The runtime has locomotion, crouch, jumping, sitting, picking up, push, climb and reaction candidate clips. Presence of tracks proves data availability only. Existing independent QA (`docs/phase04/QA_REVIEW.md`, characters section) fails reversed Push used as Pull, missing visible climb proof, cooperative hands touching nothing, and dialogue staging facing a wall. Those require contact staging and actual motion review, not additional downloads.

Sixteen Mixamo animation sources were already downloaded on 19 October. They include actual door opening/closing, heavy pull start/loop/stop, lever, kneeling, pointing, arguing and turns. Originals, checksums and license records are in `asset_library/manifests/mixamo_20261019/inventory.csv` and `asset_library/licenses/mixamo_20261019/LICENSE_RECORD.md`. Official usage FAQ: https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html . These are commercial game dependencies under Adobe's terms, not CC0 or an asset pack for redistribution. Two actual skeleton retarget trial GLBs exist below; they are not wired into the game. Their rendered poses do not constitute full contact/locomotion validation. Preserve the canonical tested rig until trials are reviewed through full motion.

| Trial file | Clips | Status |
|---|---:|---|
'''
for r in trials:
    out += f"| `{r['path']}` | {len(r['animations'])} | CONVERTED, motion/contact review required |\n"
out += '''
## Replacement priority

1. Adrian and Noah: detailed garment geometry, hair and PBR skin. Preserve 80-joint Biped bone names or explicitly retarget all 37 clips and hand attachments. No suitable new licensed drop-in model was approved in this audit.
2. True pull and door clips: reuse existing acquired trials; fit hands to actual handles and replay gameplay/cinematic motion before promotion.
3. Cooperative assistance, vault and carry contacts: acquire or author task-specific motion and validate both participants and prop trajectories together.
4. Officer and workshop staff variety: explicit role-specific models remain missing; aliasing a guard does not close those requirements.

No purchase, access bypass or unverified asset was introduced. Further character work remains necessary for acceptance.

## Reproducible integrity evidence

Run `python tools/phase04_character_acquisition_audit.py` to regenerate this report. SHA-256 values and animation names are below; hashes establish payload identity, not visual or legal approval.

```json
'''
out += json.dumps({'runtime':rows,'retarget_trials':trials}, indent=2) + '\n```\n'
(R/'docs/phase04/CHARACTER_ASSET_AUDIT.md').write_text(out,encoding='utf-8')
print('Audited', len(rows), 'runtime models and', len(trials), 'retarget trials')
