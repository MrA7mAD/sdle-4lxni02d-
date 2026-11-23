# Appends Dr. Fhd's Nov quiz (NOVF-*) to the November bank: updates extras/nov.json and the banknov block in index.html.
import json, re, sys, random, base64, io, importlib.util, os
from PIL import Image
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = sys.argv[1] if len(sys.argv) > 1 else repo + "/index.html"
sp = importlib.util.spec_from_file_location("novf", repo + "/extras/novf.py"); nf = importlib.util.module_from_spec(sp); sp.loader.exec_module(nf)
bank = json.load(open(repo + "/extras/nov.json", encoding="utf-8"))
bank["q"] = [q for q in bank["q"] if not q["i"].startswith("NOVF-")]
bank["img"] = {k: v for k, v in bank["img"].items() if not k.startswith("NOVF-")}
rng = random.Random(1123)
for d in nf.QF:
    o = d["o"]; idx = list(range(len(o))); rng.shuffle(idx); qid = "NOVF-" + str(d["k"])
    q = {"i": qid, "s": d["s"], "q": d["q"], "o": [o[i] for i in idx], "a": [idx.index(0)], "k": "mcq", "e": d["e"]}
    for f in ("c", "r", "by", "n", "rep"):
        if d.get(f): q[f] = d[f]
    if d.get("img"):
        im = Image.open(d["img"]).convert("RGB"); im.thumbnail((900, 900)); buf = io.BytesIO(); im.save(buf, "WEBP", quality=80)
        bank["img"][qid + "_0"] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(); q["pi"] = [qid + "_0"]
    bank["q"].append(q)
json.dump(bank, open(repo + "/extras/nov.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
s = open(html, encoding="utf-8").read()
payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
s, k = re.subn(r'(<script id="banknov" type="application/json">).*?(</script>)', lambda m: m.group(1) + payload + m.group(2), s, count=1, flags=re.S); assert k == 1
for q_ in ("\\'", "'"):
    old = "including the 2, 4 and 17 Nov exams and Alotaibi" + q_ + "s recall,"
    if old in s: s = s.replace(old, "including the 2, 4 and 17 Nov exams, Alotaibi" + q_ + "s recall and Dr. Fhd" + q_ + "s November quiz,", 1)
open(html, "w", encoding="utf-8").write(s)
print(len(bank["q"]), "November questions;", sum(1 for q in bank["q"] if q["i"].startswith("NOVF-")), "from Dr. Fhd")
