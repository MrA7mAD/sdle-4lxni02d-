# Applies textbook checks to the question banks: page references, corrected answers, notes.
# Usage: python3 book_refs.py index.html extras/book_*.json   (idempotent: same result if run twice)
import json, re, sys
html, files = sys.argv[1], sys.argv[2:]
E = {}
for f in files:
    for k, v in json.load(open(f, encoding="utf-8")).items(): E.setdefault(k, {}).update(v)
s = open(html, encoding="utf-8").read()
done = set()
def patch(m):
    d = json.loads(m.group(2)); changed = False
    for q in d["q"]:
        e = E.get(q.get("i"))
        if not e: continue
        if e.get("ref"):
            book = e["ref"].split(",")[0]
            old = q.get("r", "")
            has_page = book.split("'")[0] in old and re.search(r"p\.\s?\d", old)
            if e["ref"] not in old and not has_page:
                if not old or (book.split("'")[0] in old and "p." not in old):
                    q["r"] = e["ref"]
                else:
                    q["r"] = old + " · " + e["ref"]
        if e.get("ans") is not None and q.get("o"):
            i = [str(x).strip() for x in q["o"]].index(e["ans"]); q["a"] = [i]
        if e.get("otext") and q.get("o"):
            a = q["a"][0] if isinstance(q["a"], list) else q["a"]; q["o"][a] = e["otext"]
        if e.get("c"): q["c"] = e["c"]
        if e.get("n") and e["n"] not in q.get("n", ""):
            q["n"] = (q.get("n", "") + " " + e["n"]).strip()
        done.add(q["i"]); changed = True
    if not changed: return m.group(0)
    return m.group(1) + json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + m.group(3)
s = re.sub(r'(<script id="bank\w+" type="application/json">)(.*?)(</script>)', patch, s, flags=re.S)
open(html, "w", encoding="utf-8").write(s)
missing = [k for k in E if k not in done]
print("book refs applied:", len(done), "missing:", missing[:10])
