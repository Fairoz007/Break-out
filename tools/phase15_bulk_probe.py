import urllib.request,json
x=json.load(urllib.request.urlopen(urllib.request.Request('https://api.polyhaven.com/assets?t=textures',headers={'User-Agent':'Breakout-Preproduction/1.0'})))
for k,v in x.items():
 if any(s in k for s in ['concrete','steel','rubber','fabric','painted_metal','metal_plate','plastic','asphalt','tiles','corrugated']):print(k)

