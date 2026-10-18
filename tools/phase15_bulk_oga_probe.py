import urllib.request,re
for page in ['https://opengameart.org/node/16130','https://opengameart.org/node/22231','https://opengameart.org/content/storm-siren','https://opengameart.org/content/door-open-door-close-set','https://opengameart.org/content/68-workshop-sounds']:
 try:
  h=urllib.request.urlopen(page).read().decode(); print(page);print('\n'.join(a for a in re.findall(r'href="([^"]+)"',h) if '/sites/default/files/' in a));print(re.findall(r'<span[^>]*class="username"[^>]*>(.*?)</span>',h))
 except Exception as e: print(e)
