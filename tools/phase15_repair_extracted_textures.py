"""Restore invalid importer-derived images from intact embedded GLB images."""
from pathlib import Path
import struct,json,hashlib,io
from PIL import Image
R=Path(__file__).resolve().parents[1];report=[]
for folder in ['assets/environments/phase15','assets/props/phase15']:
    for glb in (R/folder).glob('*.glb'):
        raw=glb.read_bytes();offset=12;document=None;binary=None
        while offset<len(raw):
            length,kind=struct.unpack_from('<II',raw,offset);payload=raw[offset+8:offset+8+length];offset+=8+length
            if kind==0x4e4f534a:document=json.loads(payload)
            elif kind==0x004e4942:binary=payload
        for image in document.get('images',[]):
            if 'bufferView' not in image:continue
            name=image.get('name','')
            dest=glb.parent/(glb.stem+'_'+name+'.png')
            if not dest.exists():continue
            try:
                with Image.open(dest) as im:im.verify()
                continue
            except Exception:pass
            view=document['bufferViews'][image['bufferView']];start=view.get('byteOffset',0)
            data=binary[start:start+view['byteLength']]
            with Image.open(io.BytesIO(data)) as im:im.verify()
            tmp=dest.with_suffix('.png.restore');tmp.write_bytes(data);tmp.replace(dest)
            report.append({'path':dest.relative_to(R).as_posix(),'source_glb':glb.relative_to(R).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'repair':'Restore corrupt importer derivative from verified embedded GLB bufferView'})
(R/'asset_library/manifests/phase15/extracted_texture_repairs.json').write_text(json.dumps(report,indent=2))
print('Restored',len(report),'derived images; GLB source bytes unchanged')
