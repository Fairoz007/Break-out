from pathlib import Path
import hashlib,json,zipfile,shutil,urllib.request
R=Path(__file__).resolve().parents[1]
O=R/'asset_library/original_downloads/props/acquisition_20261019';O.mkdir(parents=True,exist_ok=True)
E=R/'asset_library/extracted_sources/acquisition_20261019/walkie_talkie';E.mkdir(parents=True,exist_ok=True)
L=R/'asset_library/licenses/acquisition_20261019';L.mkdir(parents=True,exist_ok=True)
src=Path('C:/Users/LUTTA/Downloads/WalkieTalkieObj.zip'); dst=O/'verzatiledev_walkie_talkie.zip'
if not dst.exists():shutil.copyfile(src,dst)
with zipfile.ZipFile(dst) as z:
 assert z.testzip() is None
 for f in z.infolist():
  p=(E/f.filename).resolve();assert p.is_relative_to(E.resolve())
 z.extractall(E)
for name,url in [('verzatiledev_radio_source.html','https://verzatiledev.itch.io/walkie-talkie'),('verzatiledev_radio_cc0_update.html','https://verzatiledev.itch.io/walkie-talkie/devlog/1447516/now-cc0-license'),('verzatiledev_terms.html','https://verzatiledev.itch.io/terms-of-use')]:
 try:(L/name).write_bytes(urllib.request.urlopen(url,timeout=30).read())
 except Exception as e:print(name,str(e))
files=[{'local_file_path':p.relative_to(R).as_posix(),'file_size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [dst,*E.rglob('*')] if p.is_file()]
rec={'asset_id':'ACQ26_RADIO_EVALUATION','asset_name':'VerzatileDev Walkie Talkie','asset_category':'props','source_website':'itch.io','source_url':'https://verzatiledev.itch.io/walkie-talkie','creator':'VerzatileDev','license':'CC0 claim on current creator page and dated March 2026 update; review preserved terms','commercial_use_status':'PENDING_LICENSE_QA','download_date':'2026-10-19','original_filename':src.name,'local_file_path':dst.relative_to(R).as_posix(),'file_size':dst.stat().st_size,'sha256':files[0]['sha256'],'files':files,'model_format':'OBJ','texture_resolution':'PENDING','rigged_status':'none','animation_status':'none','godot_import_status':'NOT TESTED','visual_inspection_status':'EVALUATION ONLY; preview appears simple, inspect geometry/materials before accepting','related_mission':['CH01_M01','CH01_M03','CH01_M06'],'remaining_issues':'Reject if stylized or untextured; do not count as realistic production asset','archive_integrity':'CRC PASS; traversal safe','license_record':'asset_library/licenses/acquisition_20261019/verzatiledev_radio_source.html'}
(R/'asset_library/manifests/acquisition_20261019/radio_inventory.json').write_text(json.dumps([rec],indent=2))
print(json.dumps(files,indent=2))
