# Save check: warns at once if an answer can't be saved on this device, and adds a storage line in Settings.
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*SAVE-CHECK*/" in s:
    print("save check already present"); sys.exit(0)

def sub1(old, new):
    global s
    assert s.count(old) == 1, "anchor not found once: " + old[:70]
    s = s.replace(old, new, 1)

# Settings row, right after the export/import row (before the sync row if present)
row_anchor = "<button class=\"btn\" data-xfer>Export / import</button></div>'+"
sub1(row_anchor, row_anchor + "\n   (window.storeRow?storeRow():'')+")

js = r"""
/*SAVE-CHECK*/
{
let warned=0,fails=0,lastFail="";
function warn(k,e){fails++;lastFail=(e&&(e.name||e.message))||"not kept";
  if(Date.now()-warned>20000){warned=Date.now();
    let d=document.getElementById("savewarn");if(!d){d=document.createElement("div");d.id="savewarn";
      d.style.cssText="position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 12px);transform:translateX(-50%);z-index:9999;max-width:min(92vw,620px);background:#c0392b;color:#fff;padding:12px 16px;border-radius:12px;font:600 15px/1.4 system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.35);cursor:pointer";
      d.onclick=()=>d.remove();document.body.appendChild(d)}
    d.textContent="⚠ Your answers are NOT being saved on this device ("+lastFail+"). Stop here so you don't lose work, and check Settings › Storage. (Tap to close)"}
  window.__saveFails=fails;
  const r=document.getElementById("storerow");if(r)r.outerHTML=window.storeRow()}
lsSet=function(k,v){try{localStorage.setItem(k,v);if(localStorage.getItem(k)!==v)warn(k,{name:"read-back mismatch"})}catch(e){warn(k,e)}};
function used(){let n=0,big=[];try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i),v=localStorage.getItem(k)||"";n+=k.length+v.length;big.push([k,v.length])}}catch(e){}
  big.sort((a,b)=>b[1]-a[1]);return{n,big}}
function kb(c){return c<1024?c+" characters":(c/1024).toFixed(c<10240?1:0)+" K characters"}
function testWrite(){try{const v="x".repeat(2000)+Date.now();localStorage.setItem("sdle-write-test",v);const ok=localStorage.getItem("sdle-write-test")===v;localStorage.removeItem("sdle-write-test");return ok?"":"read-back mismatch"}catch(e){return e.name||e.message||"error"}}
window.storeRow=function(){const u=used(),t=testWrite();
  let cnt="";try{if(typeof B!=="undefined"&&B){const p=JSON.parse(localStorage.getItem(B.ls)||"{}");cnt=" "+B.name+": "+Object.keys(p.ans||{}).length+" answers saved here."}}catch(e){}
  const bad=t||fails;
  const msg=bad?'<span style="color:var(--bad)">Saving is failing on this device'+(t?" ("+esc(t)+")":"")+(fails?" — "+fails+" save"+(fails>1?"s":"")+" failed this session":"")+'. Don\'t start long sessions here; use another browser or device until this is fixed.</span> ':'<span style="color:var(--ok,#3fb37f)">Saving works.</span> ';
  return '<div class="set-row" id="storerow"><div><b>Storage on this device</b><p>'+msg+'The app uses about '+kb(u.n)+' (browsers allow roughly 2,500–5,000 K).'+cnt+'</p></div><button class="btn" data-store>Check again</button></div>'};
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-store]");if(!b)return;const r=document.getElementById("storerow");if(r)r.outerHTML=window.storeRow();if(typeof toast==="function")toast(testWrite()?"Saving is failing on this device":"Saving works")});
// check once on open
setTimeout(()=>{const t=testWrite();if(t)warn("",{name:t})},2000);
}
"""
anchor = "showPicker();\ndbHandles();\n"
assert s.count(anchor) == 1, "app end not found"
s = s.replace(anchor, anchor + js, 1)
open(p, "w", encoding="utf-8").write(s)
print("save check added")
