"""Validate evidence, rejecting chapter_complete when its log contains resource/script errors."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1];E=R/'tests/phase04/evidence';checks={}
def logcheck(name):
    p=E/(name+'.log');s=p.read_text(encoding='utf-8-sig',errors='replace') if p.exists() else ''
    errors=re.findall(r'^(?:SCRIPT )?ERROR:.*',s,re.M)
    return s,errors
for name in ['realistic_chapter_final','realistic_exe_final']:
    path=E/(name+'.json');d=json.loads(path.read_text()) if path.exists() else {}
    s,errors=logcheck(name)
    checks[name]={'pass':d.get('reason')=='chapter_complete' and not errors,'reason':d.get('reason','PENDING'),'errors':errors,'events':len(d.get('events',[])),'autopilot_stuck':sum(x.get('kind')=='autopilot_stuck' for x in d.get('events',[])),'real_seconds':d.get('real_seconds')}
s,errors=logcheck('realistic_parse_final');checks['parse']={'pass':'failed=0' in s and not errors,'summary':next((x for x in s.splitlines() if 'PARSE CHECK' in x),''),'errors':errors}
s,errors=logcheck('realistic_gameplay_final');checks['movement_camera']={'pass':s.count(': PASS')==14 and ': FAIL' not in s and not errors,'passed':s.count(': PASS'),'errors':errors}
for name,folder,count in [('realistic_capture_accepted','realistic_after',16),('realistic_detail_final','realistic_details',5)]:
    p=R/'docs/phase04/visual_evidence'/folder/'cameras.json';d=json.loads(p.read_text()) if p.exists() else {};s,errors=logcheck(name)
    frames=d.get('captures',[])
    checks[name]={'pass':len(frames)==count and all(x.get('png_written') for x in frames) and not errors,'captures':len(frames),'errors':errors,'engine':d.get('godot'),'renderer':d.get('renderer')}
p=R/'assets/props/phase04_architecture/validation.json';d=json.loads(p.read_text())
checks['workshop_collision_anchors']={'pass':d.get('collision_comparison_pass',False) and d.get('mission_points_comparison_pass',False),'collision_shapes':d['collision_shapes'],'points':len(d['mission_points'])}
s,errors=logcheck('realistic_export_final');exe=R/'build/windows/phase04_realistic/BreakoutNoWayBack.exe'
checks['export']={'pass':exe.exists() and '[ DONE ] savepack' in s and not errors,'bytes':exe.stat().st_size if exe.exists() else 0,'errors':errors,'file':str(exe.relative_to(R))}
if exe.exists():checks['export']['sha256']=hashlib.sha256(exe.read_bytes()).hexdigest()
report={'validation_pass':all(c['pass'] for c in checks.values()),'production_complete':False,'checks':checks,'rejected_evidence':{'realistic_game.json':'Reached chapter_complete but contained missing bed resource errors; NOT acceptance evidence.','realistic_after_final_capture.log':'Missing-bed iteration, superseded by realistic_capture_accepted.log.','realistic_export.log':'First export detected Blender source in runtime folder; superseded by clean final export.'},'limitations':['Automation is not human controller acceptance','Static renders are not motion/contact approval','No whole environment or critical character requirement production-VERIFIED']}
(E/'realistic_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
raise SystemExit(0 if report['validation_pass'] else 1)
