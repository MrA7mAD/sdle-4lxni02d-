# Adds the November 2026 Recalls bank (idempotent). Placed first in the bank list.
import re, sys, json
html_path, bank_path = sys.argv[1], sys.argv[2]
s = open(html_path, encoding="utf-8").read()
if 'id="banknov"' in s:
    print("November bank already present"); sys.exit(0)
bank = json.load(open(bank_path, encoding="utf-8"))
payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
m = re.search(r'<script id="bankoct" type="application/json">.*?</script>', s, re.S); assert m
s = s[:m.start()] + '<script id="banknov" type="application/json">' + payload + '</script>\n' + s[m.start():]
m = re.search(r'"oct":\{id:"oct".*?secs:(\[\[.*?\]\])\},', s, re.S); assert m
entry = (' "nov":{id:"nov",tag:"Nov",name:"November 2026 Recalls",'
         'blurb:"Recalls from the November 2026 exams, including the 2 Nov and 4 Nov exams, written up as multiple choice and checked against Rafi\' Al-Maqam 16.",'
         'doc:"progressnov",ls:"sdle-nov26-progress-v1",lss:"sdle-nov26-session-v1",kindFilter:null,\n   secs:' + m.group(1) + '},\n')
s = s[:m.start()] + entry + s[m.start():]
s, k = re.subn(r'const ORDER=\[', 'const ORDER=["nov",', s, count=1); assert k == 1
note = ('  if(B.id==="nov")h+=\'<p class="sub" style="font-size:.86rem;margin:-12px 0 22px">Most recalls named only the topic, so the question and options were written around it (tagged \\"rebuilt\\"). '
        'Where the candidate gave an answer, it is kept and checked; the note under each question says which. '
        'From the 2 Nov exam, the 5–6 easy infection-control questions weren\\\'t recalled in detail, so they aren\\\'t included.</p>\';\n')
anchor = '  if(B.id==="oct")h+='; assert anchor in s
s = s.replace(anchor, note + anchor, 1)
open(html_path, "w", encoding="utf-8").write(s)
print("Added November bank with", len(bank["q"]), "questions")
