# Per-device "Question size" setting: Normal / Large / Fit screen.
# Scales the quiz column with transform: scale() (works the same in Safari and Chrome),
# and pads the bottom so the page still scrolls to the end.
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*QUIZ-SIZE-V3*/" in s:
    print("quiz size v3 already present"); sys.exit(0)
# remove version 2 (transform) if present
s = re.sub(r"\n/\*QUIZ-SIZE-V2\*/\n.*?margin-bottom:var\(--qb,0px\)\}\n", "\n", s, flags=re.S)
s = re.sub(r"\n/\*QUIZ-SIZE-JS2\*/\n\{.*?\nfit\(\);\n\}\n", "\n", s, flags=re.S)
# remove version 1 (CSS zoom) if present
s = s.replace("\n/*QUIZ-SIZE*/\n.quizmode main .wrap{zoom:var(--qz,1)}\n", "\n")
s = re.sub(r"\n/\*QUIZ-SIZE-JS\*/\n\{.*?\nfit\(\);\n\}\n", "\n", s, flags=re.S)
s = s.replace("\n   sizeRow()+", "")

css = """
/*QUIZ-SIZE-V3*/
html.qz body.quizmode main .wrap{max-width:none;width:var(--qw);margin-left:var(--qx);margin-right:0;zoom:var(--qz);font-size:16px}
html.qz.qzr{font-size:var(--qf)}
"""
i = s.index("</style>"); s = s[:i] + css + s[i:]
row_anchor = "<button class=\"btn\" data-xfer>Export / import</button></div>'+"
assert s.count(row_anchor) == 1, "settings anchor"
s = s.replace(row_anchor, row_anchor + "\n   sizeRow()+", 1)
js = r"""
/*QUIZ-SIZE-JS3*/
{
// Sharp scaling with CSS zoom. Safari's zoom does not enlarge rem-based text, so there the root font size is raised too.
const K="sdle-qsize",root=document.documentElement,BASE=726;
const mode=()=>{try{return localStorage.getItem(K)||"normal"}catch(e){return"normal"}};
let zoomRem=true;try{const mk=z=>{const t=document.createElement("span");t.textContent="MMMMMMMMMM";t.style.cssText="position:absolute;visibility:hidden;white-space:nowrap;font-size:1rem;"+(z?"zoom:2":"");document.body.appendChild(t);const w=t.getBoundingClientRect().width;t.remove();return w};const a=mk(0),b=mk(1);zoomRem=a>0&&b/a>1.5}catch(e){}
let busy=false;
function fit(){if(busy)return;busy=true;try{
  const m=mode(),mn=document.querySelector("main"),quiz=document.body.classList.contains("quizmode");let f=1;
  if(m!=="normal"&&mn&&quiz){const cs=getComputedStyle(mn),W=mn.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    const room=W/BASE;f=m==="large"?Math.min(1.25,room):Math.min(1.6,room);f=Math.floor(f*20)/20;
    if(f>1){root.style.setProperty("--qz",String(f));root.style.setProperty("--qw",BASE+"px");
      root.style.setProperty("--qx",Math.max(0,Math.floor((W-BASE*f)/2/f))+"px");root.style.setProperty("--qf",(16*f)+"px")}}
  root.classList.toggle("qz",f>1);root.classList.remove("qzr");if(f>1){const w=document.querySelector("main .wrap");if(w)try{const mk=par=>{const t=document.createElement("span");t.textContent="MMMMMMMMMM";t.style.cssText="position:absolute;visibility:hidden;white-space:nowrap;font-size:1rem";par.appendChild(t);const x=t.getBoundingClientRect().width;t.remove();return x};const a=mk(document.body),b=mk(w);zoomRem=a>0&&b/a>f*0.8}catch(e){}root.classList.toggle("qzr",!zoomRem)}
}finally{busy=false}}
addEventListener("resize",fit);
new MutationObserver(fit).observe(document.body,{attributes:true,attributeFilter:["class"]});
const side=document.querySelector(".side");if(side)try{new ResizeObserver(()=>fit()).observe(side)}catch(e){}
document.addEventListener("transitionend",e=>{if(e.target&&e.target.classList&&e.target.classList.contains("side"))fit()});
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
print("quiz size v3 added")
