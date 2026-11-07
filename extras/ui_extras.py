# Auto-hiding sidebar on computers (mouse/trackpad) only. iPad/touch keeps the normal sidebar.
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*AUTOHIDE-SIDE*/" in s:
    print("autohide already present"); sys.exit(0)
css0 = "\n/*CENTER-QUIZ*/\n.quizmode .wrap{max-width:72ch}\n"
css = """
/*AUTOHIDE-SIDE*/
@media (hover:hover) and (pointer:fine) and (min-width:821px){
  .app{grid-template-columns:1fr}
  .side{position:fixed;left:0;top:0;bottom:0;width:240px;z-index:40;transform:translateX(-228px);
        transition:transform .22s ease, box-shadow .22s ease;box-shadow:none}
  .side>*{opacity:0;transition:opacity .15s ease}
  .side::after{content:"";position:absolute;right:4px;top:50%;width:3px;height:44px;margin-top:-22px;
        border-radius:3px;background:var(--line);transition:opacity .15s ease}
  .side:hover,.side:focus-within{transform:translateX(0);box-shadow:0 0 28px rgba(0,0,0,.28)}
  .side:hover>*,.side:focus-within>*{opacity:1}
  .side:hover::after,.side:focus-within::after{opacity:0}
}
@media (hover:hover) and (pointer:fine) and (min-width:821px) and (prefers-reduced-motion:reduce){
  .side,.side>*{transition:none}
}
"""
i = s.index("</style>")
s = s[:i] + css0 + css + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("autohide sidebar added")
