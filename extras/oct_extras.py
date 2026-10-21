# Merges Deema's 20 Oct recall into the October bank and adds a "Source exam" filter
# to the custom-set / exam setup for the October bank. Idempotent.
import re, sys, json
html_path, bank_path = sys.argv[1], sys.argv[2]
s = open(html_path, encoding="utf-8").read()
if "/*SRC-FILTER*/" in s:
    print("October extras already present"); sys.exit(0)

def sub1(old, new):
    global s
    assert s.count(old) == 1, "anchor not found once: " + old[:60]
    s = s.replace(old, new, 1)

# ---- 1. merge Deema's questions and images into the October bank data ----
deema = json.load(open(bank_path, encoding="utf-8"))
for q in deema["q"]:
    rebuilt = q.get("by", "").endswith("rebuilt")
    q["by"] = "20 Oct exam (Deema)" + (" · rebuilt" if rebuilt else "")
m = re.search(r'(<script id="bankoct" type="application/json">)(.*?)(</script>)', s, re.S)
oct_ = json.loads(m.group(2))
have = {q["i"] for q in oct_["q"]}
added = [q for q in deema["q"] if q["i"] not in have]
oct_["q"] += added
oct_["img"].update(deema["img"])
payload = json.dumps(oct_, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
s = s[:m.start(2)] + payload + s[m.end(2):]

# blurb on the bank picker
if "20 Oct (Sandra, Aseel)" in s:
    sub1("20 Oct (Sandra, Aseel)", "20 Oct (Sandra, Aseel, Deema)")

# ---- 2. move any progress saved in the old separate Deema bank into October ----
sub1('const LSB="sdle-current-bank"',
     '(function(){try{const a=localStorage.getItem("sdle-deema-progress-v1");if(!a)return;'
     'const d=JSON.parse(a),o=JSON.parse(localStorage.getItem("sdle-oct26-progress-v1")||"{}");'
     'o.ans=o.ans||{};o.bm=o.bm||{};o.hist=Array.isArray(o.hist)?o.hist:[];'
     'for(const k in (d.ans||{}))if(!o.ans[k])o.ans[k]=d.ans[k];Object.assign(o.bm,d.bm||{});'
     'if(Array.isArray(d.hist))o.hist=o.hist.concat(d.hist).sort((x,y)=>(x.t1||0)-(y.t1||0)).slice(-300);'
     'o.u=Date.now();localStorage.setItem("sdle-oct26-progress-v1",JSON.stringify(o));'
     'localStorage.setItem("sdle-deema-progress-v1-moved",a);localStorage.removeItem("sdle-deema-progress-v1");'
     'if(localStorage.getItem("sdle-current-bank")==="deema")localStorage.setItem("sdle-current-bank","oct")}catch(e){}})();\n'
     'const LSB="sdle-current-bank"')

# ---- 3. "Source exam" filter in the setup popup (October bank only) ----
helper = ('/*SRC-FILTER*/function srcOf(q){const b=(q.by||"").replace(/\\s*·\\s*rebuilt$/,"");return(!b||b==="Rebuilt question")?"Nadine\'s recalls":b}\n'
          'function srcList(){const m={};Q.forEach(q=>{const k=srcOf(q);m[k]=(m[k]||0)+1});'
          'const day=k=>{const x=k.match(/^(\\d+) Oct/);return x?+x[1]:0};'
          'return Object.keys(m).sort((a,b)=>day(a)-day(b)||a.localeCompare(b)).map(k=>[k,m[k]])}\n'
          'function openSetup(o){')
sub1("function openSetup(o){", helper)
sub1("const st={secs:new Set(o.secs),",
     "const SRCL=B.id===\"oct\"?srcList():[];const st={src:new Set(SRCL.map(x=>x[0])),secs:new Set(o.secs),")
sub1("ids=ids.filter(i=>{const q=Q[i];",
     "ids=ids.filter(i=>{const q=Q[i];if(SRCL.length&&!st.src.has(srcOf(q)))return false;")
sub1("'<div class=\"fld\"><span class=\"lb\">Questions</span>'",
     "(SRCL.length?'<div class=\"fld\"><span class=\"lb\">Source exam <button type=\"button\" class=\"btn ghost sm\" id=\"allsrc\" style=\"padding:0 6px;font-weight:500\">'+(st.src.size===SRCL.length?\"Clear\":\"Select all\")+'</button></span><div class=\"checks\">'+"
     "SRCL.map(([k,c])=>'<label><input type=\"checkbox\" data-src=\"'+esc(k)+'\"'+(st.src.has(k)?\" checked\":\"\")+'> '+esc(k)+' <span class=\"sub\" style=\"font-size:.78rem;margin-left:auto\">'+c+'</span></label>').join(\"\")+'</div></div>':'')+"
     "'<div class=\"fld\"><span class=\"lb\">Questions</span>'")
sub1('$("#all").onclick=',
     'lay.querySelectorAll("[data-src]").forEach(c=>c.onchange=()=>{c.checked?st.src.add(c.dataset.src):st.src.delete(c.dataset.src);draw()});'
     'if($("#allsrc"))$("#allsrc").onclick=()=>{if(st.src.size===SRCL.length)st.src.clear();else SRCL.forEach(x=>st.src.add(x[0]));draw()};'
     '$("#all").onclick=')
# put the chosen source in the session title when only one is picked
sub1('const one=st.secs.size===1?SECS[[...st.secs][0]][0]:st.secs.size===SECS.length?"All specialties"',
     'const one=(SRCL.length&&st.src.size===1?[...st.src][0]+" · ":"")+(st.secs.size===1?SECS[[...st.secs][0]][0]:st.secs.size===SECS.length?"All specialties"')
# close the parenthesis we opened: find the end of that expression (":...specialties";)
m = re.search(r'(\(st\.secs\.size===1\?SECS\[\[\.\.\.st\.secs\]\[0\]\]\[0\]:st\.secs\.size===SECS\.length\?"All specialties":[^;]*?)(;)', s)
assert m, "title expression end not found"
s = s[:m.end(1)] + ")" + s[m.end(1):]

open(html_path, "w", encoding="utf-8").write(s)
print("Merged", len(added), "Deema questions into October; October now", len(oct_["q"]))
