"""Evidence-based asset coverage, checksums and matched screenshot sheets. No auto-approval."""
from pathlib import Path
import csv, hashlib, json, re
from collections import Counter
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1]
D=R/'docs/phase04'
E='docs/phase04/visual_evidence/'
rows=[]
def sha(p):
    f=R/p
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else ''
def add(id,name,path='',scene='',shot='',source='',license='',original='',quality='Acceptable but needs improvement',notes='',status='INTEGRATED'):
    exists=(R/path).is_file() if path else False
    referenced=bool(path) and (path.endswith('.gd') or any(Path(path).name in p.read_text(encoding='utf-8-sig') for p in (R/'scripts').rglob('*.gd')))
    if exists and status=='INTEGRATED' and not referenced:
        status='IMPORTED' if (R/(path+'.import')).exists() else 'CONVERTED'
    rows.append(dict(requirement_id=id,asset_name=name,source_url=source,license=license,downloaded_file=original,
        original_sha256=sha(original),checksum=sha(path),converted_file=path,
        godot_import_result=('Imported / runtime reference present; see captures' if exists and scene and referenced else 'Per-asset import/render NOT TESTED'),
        scene_integration=scene,visual_screenshot=(E+'realistic_after/'+shot+'.png' if shot else ''),
        gameplay_regression_result='See tests/phase04/evidence/realistic_chapter.json (automated, not human acceptance)' if scene else 'NOT TESTED',
        final_status=status if exists else 'MISSING',visual_classification=quality,notes=notes,
        priority='P0' if any(k in id for k in ['CHAR-ADRIAN','CHAR-NOAH','BUS-','COURT-','CELL-BUNK']) else 'P1' if any(k in id for k in ['CELL','LAUNDRY','YARD','ANIM']) else 'P2'))
def prop(id,name,file,scene,shot,quality='Acceptable but needs improvement',notes=''):
    add(id,name,'assets/props/phase15/'+file+'.glb',scene,shot,'Original project geometry / see earlier manifest','Original project geometry',quality=quality,notes=notes)
rb='assets/characters/acquisition_20261019/rocketbox_facial/'
for key,label,model in [('ADRIAN','Adrian Cross','adrian_cross'),('NOAH','Noah Reyes','noah_reyes'),('GUARD','Guards / Rusk','tomas_rusk'),('PRISONER','Prisoners','prisoner_npc'),('SILAS','Supporting inmate Silas','silas_bell'),('MARA','Mara','mara_sen')]:
    add('P04R-CHAR-'+key,label,rb+'rb_'+model+'.glb','CharacterVisual.MODELS','','https://github.com/microsoft/Microsoft-Rocketbox','MIT source; animation rights separate',quality='Acceptable but needs improvement',notes='Existing 80-joint/37-clip derivative. Hair/wardrobe/facial realism not approved; see CHARACTER_ASSET_AUDIT.md.')
    if key in ['ADRIAN','NOAH']: rows[-1]['visual_screenshot']=E+'realistic_before/'+key.lower()+'_full.png'
for key in ['OFFICER','WORKSHOP_STAFF']:
    add('P04R-CHAR-'+key,key.replace('_',' ').title(),notes='No dedicated production-quality variant integrated.',quality='Missing')
for name in ['Idle','Walk','Run','Sprint','Crouch','Crouch walk','Jump','Landing','Turn','Stop','Sit','Stand','Door','Pick up','Carry','Push','Pull','Climb','Vault','Cooperative assistance','Combat reaction','Dialogue','Cinematic body language']:
    good=name in ['Idle','Walk','Run','Sprint','Crouch','Crouch walk','Jump','Landing','Sit','Stand','Pick up','Push','Combat reaction','Dialogue']
    add('P04R-ANIM-'+name.upper().replace(' ','_'),name,rb+'rb_adrian_cross.glb','CharacterVisual action/locomotion mapping','',
        'https://quaternius.com/packs/universalanimationlibrary.html','CC0 UAL clips; MIT body source',quality='Acceptable but needs improvement' if good else 'Missing production motion',
        notes='Runtime clip/substitution is not contact approval. Existing Mixamo pull/door trials rejected, not active. See CHARACTER_ASSET_AUDIT.md.',status='INTEGRATED' if good else 'BLOCKED')
oga='https://opengameart.org/content/3d-bus'
add('P04R-BUS-001','Detailed prison coach','assets/props/phase04_realistic/blackridge_transport_bus_chassis.glb','EnvIntake.build / M01','bus',oga,'CC0-1.0 source + original project detail','asset_library/original_downloads/phase025_integration/oga_bus/BUS.blend',notes='Named wheels/doors retained. New chassis, axles, suspension, exhaust. Flat body and simplified seats still below hero quality.')
add('P04R-COURT-HOOP','Perforated board / double rim / chain net / support','assets/props/phase04_realistic/hoop_perforated_steel.glb','prison_court.hoop / M02','hoop_detail','Original project geometry','Original project geometry',quality='Acceptable but needs improvement',notes='756 real through-holes per board; bright chain finish remains. Same 3.05 m rim height and post collider.')
add('P04R-COURT-BALL','Size 7 ball with recessed channels','assets/props/phase04_realistic/basketball_recessed_channels.glb','Mission02.build / distraction','', 'Original project geometry','Original project geometry',notes='Repaired smooth seam geometry; hero pebble skin not approved; rolling regression required after final change.')
for id,name,f in [('BENCH','Yard benches','yard_bench'),('TAP','Alcove tap','water_tap'),('CCTV','Surveillance camera','cctv_camera')]:prop('P04R-YARD-'+id,name,f,'EnvYard.build / M02','yard',notes='Existing geometry, not a newly acquired replacement.')
add('P04R-YARD-TOWER','Guard tower','assets/environments/acquisition_20261019/guard_tower.glb','EnvYard.build / M02','yard',notes='Existing acquired mesh; source license in earlier acquisition records requires per-asset closure.')
add('P04R-YARD-FENCE','Woven perimeter fence','assets/environments/phase025/chain_link_fence_2x5.glb','EnvYard.build / M02','yard',notes='Existing geometry and distant alpha LOD retained; gates and navigation unchanged.')
add('P04R-YARD-LIGHTS','Twin-head floodlight columns','assets/props/phase03/floodlight_pole.glb','EnvYard.build / M02','yard','Original project geometry','Original project geometry')
for id,name,file in [('DESK','Processing counter','intake_counter'),('LOCKER','Intake lockers','locker')]:
    add('P04R-INTAKE-'+id,name,'assets/props/phase03/'+file+'.glb','EnvIntake.build / M01','intake','Original project geometry','Original project geometry')
for id,name,f in [('BENCH','Holding benches','holding_bench'),('SCANNER','Security scanner','scanner'),('BARRIER','Security barrier','security_barrier')]:
    prop('P04R-INTAKE-'+id,name,f,'EnvIntake.build / M01','intake',notes='Path existence alone is not integration proof; inspect runtime reference inventory.')
add('P04R-CELL-TIERDOOR','Upper tier welded security doors','assets/props/phase04_cellblock/tier_security_door.glb','EnvCellblock._upper_tier / M01 M04','cellblock','tools/phase04_cell_hardware.py','Original project geometry',notes='9020 triangles, hinges, lock, view grille, food pass, louvres and kickplate. Visual only; inaccessible tier wall/collision retained.')
add('P04R-CELL-BUNK','Detailed cell bedding and frame','assets/props/phase04_architecture/prison_bunk.glb','EnvCellblock.build','cell_interior','Original project geometry','Original geometry + licensed fabric maps',quality='Acceptable but needs improvement',notes='See architecture provenance; preserve old collision separately.')
for id,name,f in [('TOILET','Cell toilet','toilet'),('SINK','Cell sink','sink'),('PANEL','Service panels','service_panel')]:prop('P04R-CELL-'+id,name,f,'EnvCellblock.build / M01 M04','cell_interior','Low-poly or unrealistic',notes='Existing simplified fixture; needs detailed replacement and close-up review.')
for name,f in [('Bars','cell_bars_3m'),('Door','cell_door_1m'),('Railing','railing_2m')]:
    add('P04R-CELL-'+name.upper(),name,'assets/environments/phase15/'+f+'.glb','EnvCellblock.build','cellblock','Original project geometry','Original project geometry',notes='Existing reused module; detailed production replacement unverified.')
add('P04R-CELL-STAIRS','Accessible detailed staircase',notes='No new compatible staircase integrated. Existing upper tier is inaccessible by design; cannot alter traversal without level authoring.',quality='Missing')
dryer='https://sketchfab.com/3d-models/industrial-dryer-machine-ironing-9716a3b43fa54cf282706601526b7f73'
original='asset_library/original_downloads/props/acquisition_20261019/industrial_dryer_ironing/industrial-dryer-machine-ironing.zip'
for name,file in [('Industrial dryers','industrial_dryer'),('Ironing station','ironing_station')]:
    add('P04R-LAUNDRY-'+file.upper(),name,'assets/props/phase04_architecture/'+file+'.glb','EnvWorkshop.build / M03','workshop_machines',dryer,'CC-BY-4.0; karakocyunus',original,notes='Reused official source; separated, centered, metric-scaled, reduced ironing geometry. Credit updated in data/credits.txt. Baked color detail; not full source PBR.')
for id,name,f in [('CART','Laundry cart','linen_trolley'),('TABLE','Steel workbench','steel_table'),('TOOLS','Tool props','inspection_lamp')]:prop('P04R-LAUNDRY-'+id,name,f,'EnvWorkshop.build / M03','workshop')
add('P04R-LAUNDRY-PRESS','Mechanical laundry presses','assets/props/phase03/laundry_press.glb','EnvWorkshop.build / M03','workshop_machines','Original project geometry','Original project geometry',notes='Existing detailed mechanism retained; interaction anchors unchanged.')
add('P04R-LAUNDRY-WASHER','Production industrial washing machines',notes='Generic washer visuals removed in favour of acquired dryers; dryer asset does not fulfil washing-machine requirement.',quality='Missing realistic model')
for id,name,script,shot in [('INTAKE-ROOMS','Holding rooms and reinforced enclosure','env_intake','intake'),('CELL-WALLS','Cellblock wall modules and walkways','env_cellblock','cellblock'),('YARD-WALLS','Precast high prison walls','env_yard','yard'),('MAINT-TUNNELS','Service tunnel architecture','env_maintenance','maintenance')]:
    add('P04R-'+id,name,'scripts/world/'+script+'.gd',script+'.build',shot,'Original project architecture with existing licensed material sets','Original geometry + per-material source licenses',notes='Procedural architecture; believable dimensions do not establish production geometry/detail acceptance.')
for id,name,f in [('PIPE','Service pipes','pipe_straight_2m'),('VALVE','Valve wheel','valve_wheel'),('PANEL','Electrical cabinet','electrical_cabinet'),('DOOR','Industrial access door','industrial_door'),('DUCT','Ventilation duct','vent_duct')]:prop('P04R-MAINT-'+id,name,f,'EnvMaintenance.build / M05','maintenance',notes='Existing module; no new integration claimed; exact runtime references listed separately.')
add('P04R-MAINT-PUMP','Detailed pump assembly','assets/props/phase03/pump_unit.glb','EnvMaintenance.build / M05','maintenance','Original project geometry','Original project geometry')
for id,name,folder in [('CONCRETE','Concrete / painted concrete','concrete_wall_008'),('ASPHALT','Asphalt','asphalt_02'),('STEEL','Weathered and painted industrial metal','rusty_metal_02'),('FABRIC','Fabric','denim_fabric'),('LEATHER','Leather','fabric_leather_02')]:
    inv=json.loads((R/'asset_library/manifests/phase025_bulk_20261019/inventory.json').read_text())
    it=next((v for v in inv if v['provider_id']==folder),{})
    files=it.get('files',[])
    runtime=next((str(v.relative_to(R)).replace('\\','/') for v in (R/'assets/materials').rglob('*'+folder+'*.tres')), '')
    if not runtime and (R/'assets/materials/phase025'/folder/(folder+'.tres')).exists(): runtime='assets/materials/phase025/'+folder+'/'+folder+'.tres'
    add('P04R-MAT-'+id,name,runtime,'EnvBuilder material mapping',('court_ground' if id=='ASPHALT' else 'yard'),it.get('source_url','https://polyhaven.com/a/'+folder),'CC0-1.0', files[0]['path'] if files else '',notes='Per-object UV density/neutral lighting acceptance incomplete. See MATERIALS_AUDIT.md. Same-name source file existence does not certify every slot.')
for name in ['Rubber','Glass','Wood','Plastic','Stainless steel']:
    add('P04R-MAT-'+name.upper().replace(' ','_'),name,notes='Present as authored material slots; individual map provenance/UV-scale and visual acceptance require closure.',quality='Acceptable but needs improvement')
out=R/'asset_library/manifests/phase04_realistic_assets.csv'
with out.open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
intro='# Phase 04 realistic asset coverage\n\n20 October 2026. **INCOMPLETE**. Status records pipeline progress, not production approval. No requirement is auto-VERIFIED. Blank provenance is an unresolved field. Broad grouped requirements remain open.\n\n'
table='| Requirement | Asset | Pipeline | Visual class | Remaining issue |\n|---|---|---|---|---|\n'
for x in rows:table+='| '+ ' | '.join(str(x[k]).replace('|','/') for k in ['requirement_id','asset_name','final_status','visual_classification','notes'])+' |\n'
(D/'ASSET_COVERAGE_MATRIX.md').write_text(intro+table,encoding='utf-8')
(D/'REALISTIC_ASSET_REQUIREMENTS.md').write_text('# Realistic asset requirements — Phase 04\n\n20 October 2026. **INCOMPLETE**. This supplements the existing 1,034-row Phase04 registry; it does not replace or silently close it.\n\nAcceptance requires legal source and retained original, checksum, inspected mesh/rig/materials, compatible metric conversion, successful Godot import, actual Chapter1 scene placement, matched visual evidence and gameplay regression. INTEGRATED does not mean VERIFIED. Reject malformed anatomy, broken weights, cap-like placeholder hair, polygonal seam artefacts and incompatible contact animations.\n\nPriorities: P0 protagonists, coach exterior/cabin, court equipment, cell furniture; P1 walls, modular cell fronts, workshop machinery, staff variety; P2 support fixtures and dressing. Preserve all collision, navigation, spawn, mission and cinematic anchors.\n\nThe CSV and coverage matrix enumerate character variants, all requested motion families, intake, cellblock, yard, laundry, maintenance and material families. Remaining deliverables include production protagonist wardrobe/hair/face geometry, compatible pull/climb/vault/paired contact motion, convincing bus surface/interior detail and complete environment prop review. None may be closed by downloads or texture-only edits.\n\n'+table,encoding='utf-8')
# Runtime string references are an audit index, not proof that every branch executes.
refs=[]
for file in (R/'scripts').rglob('*.gd'):
    s=file.read_text(encoding='utf-8-sig')
    for n,line in enumerate(s.splitlines(),1):
        for v in re.findall(r'"([^"\n]+\.(?:glb|gltf))"',line):
            path=v.replace('res://','')
            refs.append({'script':str(file.relative_to(R)),'line':n,'reference':v,'literal_exists':(R/path).is_file(),'sha256':sha(path)})
(D/'runtime_model_reference_inventory.json').write_text(json.dumps(refs,indent=2))
# Matched evidence, no resynthesis. Labels explain chronology and camera provenance.
before=R/E/'realistic_before';after=R/E/'realistic_after';sheets=R/E/'realistic_comparisons';sheets.mkdir(exist_ok=True)
for name in ['cellblock','cell_interior','workshop_machines','hoop_detail','court_ground','bus']:
    if not (before/(name+'.png')).exists() or not (after/(name+'.png')).exists():continue
    sheet=Image.new('RGB',(1280,396),(20,23,27));draw=ImageDraw.Draw(sheet)
    for i,folder in enumerate([before,after]):
        im=Image.open(folder/(name+'.png')).convert('RGB');im.thumbnail((640,360));sheet.paste(im,(i*640,36))
        draw.text((i*640+10,10),('BEFORE THIS SESSION' if i==0 else 'AFTER THIS SESSION')+' / '+name,fill='white')
    sheet.save(sheets/(name+'.jpg'),quality=92)
summary={'requirements':len(rows),'statuses':dict(Counter(x['final_status'] for x in rows)),'runtime_references':len(refs),'production_complete':False}
(D/'realistic_asset_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
