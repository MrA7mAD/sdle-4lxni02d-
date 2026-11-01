# Moves trailing "(...)" detail out of a too-long correct option into the explanation shown after answering.
import json, re
p = "/home/claude/tools/kmz/kmz.json"
d = json.load(open(p, encoding="utf-8"))
moved = 0
for q in d["q"]:
    a = q["a"][0]; cor = q["o"][a]
    others = [o for i, o in enumerate(q["o"]) if i != a]
    m = re.match(r"^(.*\S)\s*\(([^()]*)\)$", cor)
    if m and len(cor) > max(len(o) for o in others) + 4:
        short, detail = m.group(1), m.group(2)
        if short not in others and len(short) >= 2:
            q["o"][a] = short
            q["e"] = short + ": " + detail[0].upper() + detail[1:] + "."
            moved += 1
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
L = sum(1 for q in d["q"] if len(q["o"][q["a"][0]]) == max(len(o) for o in q["o"]))
print("moved", moved, "| correct is longest now:", L, "of", len(d["q"]), round(100 * L / len(d["q"])), "%")
