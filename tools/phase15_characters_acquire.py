import requests,re,json,zipfile,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records=[]
for slug in ['universal-base-characters','universal-animation-library','universal-animation-library-2']:
 s=requests.Session();u='https://quaternius.itch.io/'+slug
 t=s.get(u+'/purchase').text;c=re.search(r'name="csrf_token" value="([^"]+)',t).group(1)
 j=s.post(u+'/download_url',data={'csrf_token':c}).json();t=s.get(j['url']).text
 lid=root/'asset_library/licenses/phase15_characters';lid.mkdir(parents=True,exist_ok=True)
 (lid/(slug+'.html')).write_text(s.get(u).text,encoding='utf-8')
 for uid,name in re.findall(r'data-upload_id="(\d+)".*?title="([^"]+\.zip)"',t):
  if 'standard' not in name.lower():continue
  out=root/'asset_library/original_downloads/phase15_characters'/name;out.parent.mkdir(parents=True,exist_ok=True)
  if not out.exists():
   url=s.post(u+'/file/'+uid,data={'csrf_token':c}).json()['url']
   r=s.get(url);r.raise_for_status();out.write_bytes(r.content)
  ex=root/'asset_library/extracted_sources/phase15_characters'/slug;ex.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(out) as z:
   assert z.testzip() is None
   for n in z.namelist():
    assert (ex/n).resolve().is_relative_to(ex.resolve())
   z.extractall(ex)
  records.append(dict(slug=slug,source_url=u,license='CC0-1.0',original_file=str(out.relative_to(root)),original_checksum=hashlib.sha256(out.read_bytes()).hexdigest()))
  print(name,out.stat().st_size,flush=True)
(root/'asset_library/manifests/phase15_characters_downloads.json').write_text(json.dumps(records,indent=2))
