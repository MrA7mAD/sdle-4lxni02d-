# Per-device "Question size" setting: Normal / Large / Fit screen.
# Scales the quiz column with transform: scale() (works the same in Safari and Chrome),
# and pads the bottom so the page still scrolls to the end.
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*QUIZ-SIZE-V2*/" in s:
    print("quiz size v2 already present"); sys.exit(0)
# remove version 1 (CSS zoom) if present
s = s.replace("\n/*QUIZ-SIZE*/\n.quizmode main .wrap{zoom:var(--qz,1)}\n", "\n")
s = re.sub(r"\n/\*QUIZ-SIZE-JS\*/\n\{.*?\nfit\(\);\n\}\n", "\n", s, flags=re.S)
s = s.replace("\n   sizeRow()+", "")

css = """
/*QUIZ-SIZE-V2*/
html.qz body.quizmode main .wrap{max-width:none;width:var(--qw);margin-left:var(--qx);margin-right:0;
  transform:scale(var(--qz));transform-origin:top left;margin-bottom:var(--qb,0px)}
"""
i = s.index("</style>"); s = s[:i] + css + s[i:]
row_anchor = "<button class=\"btn\" data-xfer>Export / import</button></div>'+"
assert s.count(row_anchor) == 1, "settings anchor"
s = s.replace(row_anchor, row_anchor + "\n   sizeRow()+", 1)
js = r"""
/*QUIZ-SIZE-JS2*/
{
const K="sdle-qsize",root=document.documentElement,BASE=726;
const mode=()=>{try{return localStorage.getItem(K)||"normal"}catch(e){return"normal"}};
let ro=null,watched=null,f=1;
function setB(){const w=document.querySelector("main .wrap");if(w&&f>1)root.style.setProperty("--qb",Math.round((f-1)*w.offsetHeight)+"px")}
function fit(){const m=mode(),mn=document.querySelector("main"),quiz=document.body.classList.contains("quizmode");f=1;
  if(m!=="normal"&&mn&&quiz){const cs=getComputedStyle(mn),W=mn.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    const room=W/BASE;f=m==="large"?Math.min(1.25,room):Math.min(1.6,room);
    if(f>1.02){f=Math.floor(f*100)/100;root.style.setProperty("--qz",String(f));root.style.setProperty("--qw",BASE+"px");
      root.style.setProperty("--qx",Math.max(0,Math.floor((W-BASE*f)/2))+"px")}else f=1}
  root.classList.toggle("qz",f>1);
  const w=document.querySelector("main .wrap");
  if(w!==watched){if(ro&&watched)ro.unobserve(watched);watched=w;if(ro&&w)ro.observe(w)}
  setB()}
try{ro=new ResizeObserver(()=>setB())}catch(e){}
addEventListener("resize",fit);
new MutationObserver(fit).observe(document.body,{attributes:true,attributeFilter:["class"]});
const mn0=document.querySelector("main");if(mn0)new MutationObserver(fit).observe(mn0,{childList:true});
if(mn0)try{new ResizeObserver(()=>fit()).observe(mn0)}catch(e){}
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
print("quiz size v2 added")
