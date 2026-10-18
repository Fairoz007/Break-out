from pathlib import Path
import urllib.request,json,time
R=Path(__file__).resolve().parents[1]
slugs=['blue_metal_plate','metal_plate','rusty_painted_metal','rubber_tiles','denim_fabric','fabric_leather_01','dirty_tiles','asphalt_01','anti_slip_concrete','worn_corrugated_iron']
for slug in slugs:
 for kind,path in [('files',R/f'asset_library/manifests/phase15_bulk_{slug}.json'),('info',R/f'asset_library/licenses/phase15_bulk/{slug}_source.json')]:
  if path.exists():continue
  data=urllib.request.urlopen(urllib.request.Request('https://api.polyhaven.com/'+kind+'/'+slug,headers={'User-Agent':'Breakout-Preproduction/1.0'})).read();path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);time.sleep(1.1)
 print(slug,flush=True)
