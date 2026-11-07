# Optional PC <-> iPad progress sync through a private GitHub Gist. Off unless a token is entered on that device.
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*GIST-SYNC*/" in s:
    print("sync already present"); sys.exit(0)

def sub1(old, new):
    global s
    assert s.count(old) == 1, "anchor not found once: " + old[:70]
    s = s.replace(old, new, 1)

# 1. Settings row, right after the export/import row
row_anchor = "<button class=\"btn\" data-xfer>Export / import</button></div>'+"
sub1(row_anchor, row_anchor + "\n   syncRow()+")
# 2. A reset is remembered so sync doesn't bring the old answers back
sub1("P.ans={};P.bm={};S=null;", "P.ans={};P.bm={};P.rz=Date.now();S=null;")

js = r"""
/*GIST-SYNC*/
{
const TK="sdle-sync-token",GK="sdle-sync-gist",LK="sdle-sync-last",DESC="SDLE Study Helper sync (private)";
const API="https://api.github.com";
const g=k=>{try{return localStorage.getItem(k)}catch(e){return null}};
const st=(k,v)=>{try{v==null?localStorage.removeItem(k):localStorage.setItem(k,v)}catch(e){}};
let busy=false,again=false,timer=null,lastErr="";
function on(){return !!g(TK)}
function hdr(){return{"Authorization":"Bearer "+g(TK),"Accept":"application/vnd.github+json","Content-Type":"application/json"}}
async function api(path,opt){const r=await fetch(API+path,Object.assign({headers:hdr(),cache:"no-store"},opt||{}));
  if(!r.ok){const t=r.status===401?"The GitHub key was rejected (expired or wrong).":r.status===404?"Sync file not found or the key has no Gist access.":"GitHub error "+r.status;throw new Error(t)}
  return r.status===204?null:r.json()}
async function findOrCreate(){
  let id=g(GK);if(id)return id;
  for(let page=1;page<=5;page++){const list=await api("/gists?per_page=100&page="+page);
    const hit=(list||[]).find(x=>x.description===DESC);if(hit){st(GK,hit.id);return hit.id}if(!list||list.length<100)break}
  const made=await api("/gists",{method:"POST",body:JSON.stringify({description:DESC,public:false,files:{"README.md":{content:"Progress sync for SDLE Study Helper. Do not edit."}}})});
  st(GK,made.id);return made.id}
async function fileText(f){if(!f)return null;if(!f.truncated)return f.content;const r=await fetch(f.raw_url,{cache:"no-store"});return r.ok?r.text():null}
function clone(x){return JSON.parse(JSON.stringify(x||{}))}
function nrm(p){p=p&&typeof p==="object"?p:{};p.ans=p.ans||{};p.bm=p.bm||{};p.hist=Array.isArray(p.hist)?p.hist:[];p.set=p.set||{};p.u=p.u||0;p.rz=p.rz||0;return p}
function merge(a,b){a=nrm(clone(a));b=nrm(clone(b));const rz=Math.max(a.rz,b.rz);
  const o={ans:{},bm:{},hist:[],set:(a.u>=b.u?a.set:b.set),u:Math.max(a.u,b.u),rz};
  [a,b].forEach(src=>{for(const id in src.ans){const x=src.ans[id];if(!Array.isArray(x))continue;if((x[4]||0)*1000<rz)continue;const y=o.ans[id];
    if(!y||(x[4]||0)>(y[4]||0)){const z=x.slice();if(y){z[2]=Math.max(x[2]||0,y[2]||0);z[3]=Math.max(x[3]||0,y[3]||0)}o.ans[id]=z}
    else{y[2]=Math.max(x[2]||0,y[2]||0);y[3]=Math.max(x[3]||0,y[3]||0)}}});
  [a,b].forEach(src=>{if(src.rz>=rz)for(const id in src.bm)o.bm[id]=1});
  const byId={};[a,b].forEach(src=>src.hist.forEach(h=>{if(!h||!h.id||(h.t1||h.id)<rz)return;const y=byId[h.id];
    if(!y)byId[h.id]=clone(h);else{Object.assign(y.r,h.r);y.t1=Math.max(y.t1||0,h.t1||0)}}));
  o.hist=Object.values(byId).sort((p,q)=>p.id-q.id).slice(-300);
  ["m19"].forEach(k=>{if(a[k]||b[k])o[k]=Math.max(a[k]||0,b[k]||0)});
  return o}
function sig(p){p=nrm(p);return JSON.stringify([p.ans,Object.keys(p.bm).sort(),p.hist.map(h=>[h.id,h.t1]),p.rz])}
async function run(){
  if(!on())return;if(busy){again=true;return}busy=true;
  try{
    const id=await findOrCreate();const gist=await api("/gists/"+id);const files={};let curChanged=false;
    for(const bid in BANKS){const key=BANKS[bid].ls,fname="sdle-"+bid+".json";
      const locRaw=g(key);let loc=null;try{loc=locRaw?JSON.parse(locRaw):null}catch(e){}
      let rem=null;try{const t=await fileText(gist.files&&gist.files[fname]);rem=t?JSON.parse(t):null}catch(e){}
      if(!loc&&!rem)continue;
      const m=merge(loc,rem);
      if(!loc||sig(m)!==sig(loc)){st(key,JSON.stringify(m));if(typeof B!=="undefined"&&B&&B.ls===key)curChanged=true}
      if(!rem||sig(m)!==sig(rem))files[fname]={content:JSON.stringify(m)}}
    if(Object.keys(files).length)await api("/gists/"+id,{method:"PATCH",body:JSON.stringify({files})});
    st(LK,String(Date.now()));lastErr="";
    if(curChanged){try{P=normB(JSON.parse(g(B.ls)),B.id);renderSide();
      if(typeof V!=="undefined"&&V&&["home","bookmarks","mistakes","history"].includes(V.name)&&typeof go==="function")go(V.name)}catch(e){}}
  }catch(e){lastErr=e.message||String(e)}
  finally{busy=false;refreshRow();if(again){again=false;setTimeout(run,500)}}}
function soon(){if(!on())return;clearTimeout(timer);timer=setTimeout(run,4000)}
// push a few seconds after the app saves
const origSave=save;save=function(){const r=origSave.apply(this,arguments);soon();return r};
function ago(t){if(!t)return"never";const s=Math.round((Date.now()-t)/1000);return s<60?"just now":s<3600?Math.round(s/60)+" min ago":s<86400?Math.round(s/3600)+" h ago":new Date(t).toLocaleDateString()}
window.syncRow=function(){
  if(!on())return '<div class="set-row" id="syncrow"><div><b>Sync PC and iPad</b><p>Off on this device. Turn it on with your private GitHub key to keep progress the same on your own devices. Other people using this link are not affected.</p></div><button class="btn" data-sync="on">Set up</button></div>';
  return '<div class="set-row" id="syncrow"><div><b>Sync PC and iPad</b><p>'+(lastErr?'<span style="color:var(--bad)">'+esc(lastErr)+'</span> ':'On. ')+'Last synced '+(busy?'now…':ago(+g(LK)||0))+'.</p></div><div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn" data-sync="now">Sync now</button><button class="btn" data-sync="off">Turn off</button></div></div>'};
function refreshRow(){const r=document.getElementById("syncrow");if(r)r.outerHTML=window.syncRow()}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-sync]");if(!b)return;const a=b.dataset.sync;
  if(a==="on"){const t=prompt("Paste your GitHub token (Gist access only).\nIt is saved only in this browser on this device.");if(!t||!t.trim())return;
    st(TK,t.trim());st(GK,null);lastErr="";refreshRow();run().then(()=>{if(lastErr&&/rejected/.test(lastErr)){st(TK,null);refreshRow()}if(typeof toast==="function")toast(lastErr?"Sync failed: "+lastErr:"Sync is on")})}
  else if(a==="now"){run().then(()=>{if(typeof toast==="function")toast(lastErr?"Sync failed: "+lastErr:"Synced")})}
  else if(a==="off"){if(confirm("Turn off sync on this device? Your progress stays here; the key is removed from this browser.")){st(TK,null);st(GK,null);st(LK,null);lastErr="";refreshRow()}}});
// sync on open and whenever the app comes back to the foreground
if(on())setTimeout(run,1500);
document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="visible"&&on()){clearTimeout(timer);timer=setTimeout(run,800)}});
}
"""
anchor = "showPicker();\ndbHandles();\n})();"
assert s.count(anchor) == 1, "app end not found"
s = s.replace(anchor, "showPicker();\ndbHandles();\n" + js + "})();", 1)
open(p, "w", encoding="utf-8").write(s)
print("sync added")
