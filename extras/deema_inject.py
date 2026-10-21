# Adds the Deema bank to an SDLE Study Helper index.html (idempotent).
import re, sys, json
html_path, bank_path = sys.argv[1], sys.argv[2]
s = open(html_path, encoding="utf-8").read()
if 'id="bankdeema"' in s:
    print("Deema bank already present"); sys.exit(0)
bank = json.load(open(bank_path, encoding="utf-8"))
n = len(bank["q"])
payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

# 1. data block, placed right after the October bank's data block
m = re.search(r'<script id="bankoct" type="application/json">.*?</script>', s, re.S)
assert m, "October bank not found"
s = s[:m.end()] + '\n<script id="bankdeema" type="application/json">' + payload + '</script>' + s[m.end():]

# 2. bank definition, copied from October's specialties
m = re.search(r'"oct":\{id:"oct".*?secs:(\[\[.*?\]\])\},', s, re.S)
assert m, "October bank definition not found"
secs = m.group(1)
entry = ('\n "deema":{id:"deema",tag:"Deema",name:"Deema · 20 Oct 2026",'
         'blurb:"Deema\'s recall of the 20 October 2026 exam, written up as multiple choice and checked against Rafi\' Al-Maqam 16. '
         'Where she couldn\'t recall an answer, it was worked out from the references and flagged.",'
         'doc:"progressdeema",ls:"sdle-deema-progress-v1",lss:"sdle-deema-session-v1",kindFilter:null,\n   secs:' + secs + '},')
s = s[:m.end()] + entry + s[m.end():]

# 3. show it right after October in the bank list
s, k = re.subn(r'const ORDER=\[([^\]]*)"oct",', r'const ORDER=[\1"oct","deema",', s, count=1)
assert k == 1, "ORDER not found"

# 4. short note on the bank's home screen
note = ('  if(B.id==="deema")h+=\'<p class="sub" style="font-size:.86rem;margin:-12px 0 22px">Deema\\\'s 20 Oct 2026 recall. '
        'Where she remembered only the question, the other options were written in. Where she couldn\\\'t remember the answer, '
        'it was worked out against Rafi\\\' Al-Maqam 16 and the textbooks, and the note under each question says so. '
        'Questions tagged \\"rebuilt\\" were written around a short recall, including the two calculation cases, the tooth-36 case and the endo-perio case. '
        'A ⚠ under the answer means the references disagree, so check it. Only \\"multiple endo questions with a new picture\\" had nothing to rebuild from.</p>\';\n')
anchor = '  if(B.id==="oct")h+='
assert anchor in s
s = s.replace(anchor, note + anchor, 1)

open(html_path, "w", encoding="utf-8").write(s)
print("Added Deema bank with", n, "questions")
