# Per-device "Question size" setting: Normal / Large / Fit screen (scales the quiz column to the screen width).
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*QUIZ-SIZE*/" in s:
    print("quiz size already present"); sys.exit(0)
css = "\n/*QUIZ-SIZE*/\n.quizmode main .wrap{zoom:var(--qz,1)}\n"
i = s.index("</style>"); s = s[:i] + css + s[i:]
row_anchor = "<button class=\"btn\" data-xfer>Export / import</button></div>'+"
assert s.count(row_anchor) == 1, "settings anchor"
s = s.replace(row_anchor, row_anchor + "\n   sizeRow()+", 1)
js = r"""
/*QUIZ-SIZE-JS*/
{
const K="sdle-qsize",root=document.documentElement;
const mode=()=>{try{return localStorage.getItem(K)||"normal"}catch(e){return"normal"}};
function fit(){const m=mode(),mn=document.querySelector("main");let f=1;
  if(m!=="normal"&&mn){const w=document.querySelector("main .wrap");
    const base=(w&&parseFloat(getComputedStyle(w).maxWidth))||740;
    const cs=getComputedStyle(mn),W=mn.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    const room=Math.max(1,W/base);f=m==="large"?Math.min(1.25,room):Math.min(1.6,room)}
  root.style.setProperty("--qz",String(Math.round(f*100)/100))}
addEventListener("resize",fit);
try{new ResizeObserver(fit).observe(document.body)}catch(e){}
new MutationObserver(fit).observe(document.body,{attributes:true,attributeFilter:["class"]});
window.sizeRow=function(){const m=mode(),b=(v,l)=>'<button data-qs="'+v+'" class="'+(m===v?'on':'')+'">'+l+'</button>';
  return '<div class="set-row" id="qsrow"><div><b>Question size</b><p>Fit screen enlarges the question screen to fill the width, so you don\'t need to zoom. Saved on this device only.</p></div><div class="seg" style="width:auto">'+b("normal","Normal")+b("large","Large")+b("fit","Fit screen")+'</div></div>'};
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-qs]");if(!b)return;
  try{localStorage.setItem(K,b.dataset.qs)}catch(x){}fit();const r=document.getElementById("qsrow");if(r)r.outerHTML=window.sizeRow()});
fit();
}
"""
anchor = "showPicker();\ndbHandles();\n"
assert s.count(anchor) == 1, "app end"
s = s.replace(anchor, anchor + js, 1)
open(p, "w", encoding="utf-8").write(s)
print("quiz size added")
