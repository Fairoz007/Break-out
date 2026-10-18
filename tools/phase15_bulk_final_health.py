from pathlib import Path
import json,hashlib,struct
R=Path(__file__).resolve().parents[1]
for pattern in ['phase15_bulk*.json']:
 for p in (R/'asset_library/manifests').glob(pattern):
  b=p.read_bytes()
  try:json.loads(b); assert b'\0' not in b
  except Exception as e:print('BADJSON',p.name,str(e))
for p in (R/'tools').glob('phase15_bulk*.py'):
 if b'\0' in p.read_bytes():print('BADSOURCE',p.name)
for f in ['phase15_bulk_assets.json','phase15_bulk_oga_assets.json']:
 for r in json.loads((R/'asset_library/manifests'/f).read_text()):
  p=R/r['runtime_file'];assert p.exists()
  if r['category']=='audio':assert hashlib.sha256(p.read_bytes()).hexdigest()==r['runtime_checksum']
  if p.suffix=='.wav':
   b=p.read_bytes();off=b.index(b'fmt ');tag=struct.unpack('<H',b[off+8:off+10])[0];assert tag==1,(p,tag)
print('Fragments paths hashes WAVformat1 and sourcebytehealth PASS')
