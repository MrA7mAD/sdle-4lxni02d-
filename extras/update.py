import re,sys,json
new_path, repo = sys.argv[1], sys.argv[2]
def banks(s):
    out={}
    for m in re.finditer(r'<script id="bank(\w+)" type="application/json">(.*?)</script>',s,re.S):
        out[m.group(1)]=[q['i'] for q in json.loads(m.group(2))['q']]
    return out
old=open(repo+'/index.html',encoding='utf-8').read()
s=open(new_path,encoding='utf-8').read()
first,rest=s.split('\n',1)
if first.startswith('<!doctype html><html><head><meta charset=utf8>') and first.endswith('<body>'): s=rest
ob,nb=banks(old),banks(s)
names=dict(re.findall(r'"(\w+)":\{id:"\w+",tag:"[^"]*",name:"([^"]+)"',s))
for k in nb:
    o,n=set(ob.get(k,[])),set(nb[k])
    print(f"{names.get(k,k)}: {len(o)} -> {len(n)}  (+{len(n-o)} new, -{len(o-n)} removed)")
for k in ob:
    if k not in nb: print("BANK REMOVED:",k)
assert s.count('<title>SDLE Study Helper</title>')==1
s=s.replace('<title>SDLE Study Helper</title>','''<title>SDLE Study Helper</title>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="SDLE">
<meta name="theme-color" content="#0E161B">''',1)
if 'serviceWorker' not in s:
    s=s.replace('</head>','<script>if("serviceWorker" in navigator){addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){})})}</script>\n</head>',1)
open(repo+'/index.html','w',encoding='utf-8').write(s)
sw=open(repo+'/sw.js').read()
v=int(re.search(r'sdle-v(\d+)',sw).group(1));open(repo+'/sw.js','w').write(sw.replace(f'sdle-v{v}',f'sdle-v{v+1}'))
print('cache ->',v+1)
# Re-add our own extra banks (not in the friend's file)
import subprocess, os
if os.path.exists('/home/claude/tools/deema.json'):
    subprocess.run(['python3','/home/claude/tools/oct_extras.py',repo+'/index.html','/home/claude/tools/deema.json'],check=True)
