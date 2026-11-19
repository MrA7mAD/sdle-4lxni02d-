# Centered quiz column + auto-hiding side menu.
# Side menu: "Auto" hides it while a mouse or trackpad is in use (PC, or iPad with Magic Keyboard)
# and shows it normally after a touch. "Always hide" / "Never hide" can be chosen per device in Settings.
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*AUTOHIDE-V2*/" in s:
    print("autohide v2 already present"); sys.exit(0)

# remove the first version (media-query only) if present
s = re.sub(r"\n/\*AUTOHIDE-SIDE\*/\n@media \(hover:hover\).*?\.side,\.side>\*\{transition:none\}\n\}\n", "\n", s, flags=re.S)

css = """
/*AUTOHIDE-V2*/
@media (min-width:821px){
  html.ah .app{grid-template-columns:1fr}
  html.ah .side{position:fixed;left:0;top:0;bottom:0;width:240px;z-index:40;transform:translateX(-228px);
        transition:transform .22s ease, box-shadow .22s ease;box-shadow:none}
  html.ah .side>*{opacity:0;transition:opacity .15s ease}
  html.ah .side::after{content:"";position:absolute;right:4px;top:50%;width:3px;height:44px;margin-top:-22px;
        border-radius:3px;background:var(--line);transition:opacity .15s ease}
  html.ah .side:hover,html.ah .side:focus-within,html.ah .side.open{transform:translateX(0);box-shadow:0 0 28px rgba(0,0,0,.28)}
  html.ah .side:hover>*,html.ah .side:focus-within>*,html.ah .side.open>*{opacity:1}
  html.ah .side:hover::after,html.ah .side:focus-within::after,html.ah .side.open::after{opacity:0}
}
@media (min-width:821px) and (prefers-reduced-motion:reduce){
  html.ah .side,html.ah .side>*{transition:none}
}
"""
if "/*CENTER-QUIZ*/" not in s:
    css = "\n/*CENTER-QUIZ*/\n.quizmode .wrap{max-width:72ch}\n" + css
i = s.index("</style>")
s = s[:i] + css + s[i:]

# Settings row, after the export/import row
row_anchor = "<button class=\"btn\" data-xfer>Export / import</button></div>'+"
assert s.count(row_anchor) == 1, "settings anchor"
s = s.replace(row_anchor, row_anchor + "\n   sideRow()+", 1)

js = r"""
/*AUTOHIDE-JS*/
{
const K="sdle-autohide";
const mode=()=>{try{return localStorage.getItem(K)||"auto"}catch(e){return"auto"}};
let last=matchMedia("(hover:hover) and (pointer:fine)").matches?"mouse":"touch";
const root=document.documentElement,sd=()=>document.querySelector(".side");
function apply(){const m=mode(),on=m==="on"||(m==="auto"&&last==="mouse");root.classList.toggle("ah",on);if(!on&&sd())sd().classList.remove("open")}
addEventListener("pointermove",e=>{if(e.pointerType==="mouse"&&last!=="mouse"){last="mouse";apply()}},{passive:true});
addEventListener("pointerdown",e=>{
  if(e.pointerType!=="mouse"&&last!=="touch"){last="touch";apply()}
  const el=sd();if(!el||!root.classList.contains("ah"))return;
  if(el.contains(e.target)){if(e.pointerType!=="mouse")el.classList.add("open")}else el.classList.remove("open")},{passive:true,capture:true});
window.sideRow=function(){const m=mode(),b=(v,l)=>'<button data-ah="'+v+'" class="'+(m===v?'on':'')+'">'+l+'</button>';
  return '<div class="set-row" id="ahrow"><div><b>Side menu</b><p>Auto hides it while you use a mouse or trackpad (also an iPad with a Magic Keyboard) and shows it again when you touch the screen. When hidden, point at the left edge to open it. Saved on this device only.</p></div><div class="seg" style="width:auto">'+b("auto","Auto")+b("on","Hide")+b("off","Show")+'</div></div>'};
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-ah]");if(!b)return;
  try{localStorage.setItem(K,b.dataset.ah)}catch(x){}apply();const r=document.getElementById("ahrow");if(r)r.outerHTML=window.sideRow()});
apply();
}
"""
anchor = "showPicker();\ndbHandles();\n"
assert s.count(anchor) == 1, "app end"
s = s.replace(anchor, anchor + js, 1)
open(p, "w", encoding="utf-8").write(s)
print("autohide v2 added")
