from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parents[1];a=[]
for f in ['phase15_bulk_assets.json','phase15_bulk_oga_assets.json']:a+=json.loads((R/'asset_library/manifests'/f).read_text())
print(collections.Counter(x['category'] for x in a));print(collections.Counter(x.get('priority') for x in a));print('paths',len(a),'unique',len({x['runtime_file'] for x in a}));print('audio identities',len({x['runtime_checksum'] for x in a if x['category']=='audio'}))
print('materials', [x['asset_name'] for x in a if x['category']=='material'])
