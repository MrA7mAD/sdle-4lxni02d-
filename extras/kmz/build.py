# Builds kmz.json (KMZ Collection bank) from the six section files.
import json, random, importlib.util, sys
D = "/home/claude/tools/kmz/"
SECS = [("implant", "Implant Dentistry", "Implant", "IMP"), ("fixed", "Fixed Prosthodontics", "Fixed", "FIX"),
        ("removable", "Removable Prosthodontics", "Removable", "REM"), ("ortho", "Orthodontics", "Ortho", "ORT"),
        ("perio", "Periodontics", "Perio", "PER"), ("pedo", "Pediatric Dentistry", "Pedo", "PED")]
C = {None: "Answer from the KMZ file", "fix": "Corrected after checking (see note)",
     "warn": "Answer from the KMZ file ⚠ check this one", "rebuilt": "Question rebuilt around a short recall in the file"}
rng = random.Random(1911)
spec0 = importlib.util.spec_from_file_location("ovr", D + "overrides.py"); ovr = importlib.util.module_from_spec(spec0); spec0.loader.exec_module(ovr)
out, problems = [], []
for s, (mod, full, short, code) in enumerate(SECS):
    spec = importlib.util.spec_from_file_location(mod, D + mod + ".py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for n, (q, cor, dis, times, note, flag) in enumerate(m.Q, 1):
        qid = "KMZ-%s-%d" % (code, n)
        if qid in ovr.D: dis = ovr.D[qid]
        if len(dis) != 3 or cor in dis or len(set(dis)) != 3 or not q.strip() or flag not in C:
            problems.append((qid, q))
        opts = [cor] + dis; idx = list(range(4)); rng.shuffle(idx)
        notes = []
        if note: notes.append(note)
        if times > 1: notes.append("Appears %d× in the file." % times)
        e = {"i": qid, "s": s, "q": q, "o": [opts[i] for i in idx], "a": [idx.index(0)], "k": "mcq",
             "by": "KMZ · " + short + (" · rebuilt" if flag == "rebuilt" else ""), "c": C[flag]}
        if notes: e["n"] = " ".join(notes)
        out.append(e)
json.dump({"q": out, "img": {}}, open(D + "kmz.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
from collections import Counter
print("total", len(out), dict(Counter(SECS[q["s"]][2] for q in out)))
print("flags", Counter(q["c"][:22] for q in out))
print("merged duplicates:", sum(1 for q in out if "Appears" in q.get("n","")))
print("PROBLEMS:", problems)
