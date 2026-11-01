# Adds the KMZ Collection bank to an SDLE Study Helper index.html (idempotent).
import re, sys, json
html_path, bank_path = sys.argv[1], sys.argv[2]
s = open(html_path, encoding="utf-8").read()
if 'id="bankkmz"' in s:
    print("KMZ bank already present"); sys.exit(0)
bank = json.load(open(bank_path, encoding="utf-8"))
payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
# 1. data block after the last bank data block
last = list(re.finditer(r'<script id="bank\w+" type="application/json">.*?</script>', s, re.S))[-1]
s = s[:last.end()] + '\n<script id="bankkmz" type="application/json">' + payload + '</script>' + s[last.end():]
# 2. bank definition, appended after the last entry of BANKS (just before the closing "};" of const BANKS)
m = re.search(r'const BANKS=\{.*?\n\};', s, re.S)
assert m, "BANKS not found"
entry = (',\n "kmz":{id:"kmz",tag:"KMZ",name:"KMZ Collection",'
         'blurb:"Dr KMZ\'s collections of the most important points from the Rafi\' Al-Maqam files (19–11), one section per subject, written up as multiple choice. '
         'Repeated lines were merged, and answers that looked wrong were corrected with a note.",'
         'doc:"progresskmz",ls:"sdle-kmz-progress-v1",lss:"sdle-kmz-session-v1",kindFilter:null,\n'
         '   secs:[["Implant Dentistry","Implant"],["Fixed Prosthodontics","Fixed"],["Removable Prosthodontics","Removable"],["Orthodontics","Ortho"],["Periodontics","Perio"],["Pediatric Dentistry","Pedo"]]}')
body = m.group(0)
body2 = re.sub(r'\}\s*\n\};$', '}' + entry + '\n};', body)
assert body2 != body, "could not append to BANKS"
s = s.replace(body, body2, 1)
# 3. show it last in the bank list
s, k = re.subn(r'const ORDER=\[([^\]]*)\]', lambda mm: 'const ORDER=[' + mm.group(1) + ',"kmz"]', s, count=1)
assert k == 1
# 4. note on the bank's home screen
note = ('  if(B.id==="kmz")h+=\'<p class="sub" style="font-size:.86rem;margin:-12px 0 22px">Dr KMZ\\\'s files give one answer per line, so the other options were written in. '
        'Lines repeated in a file were merged into one question, and the note says how many times it appeared. '
        'Where a file answer looked wrong it was corrected and the note gives the original; a ⚠ marks answers worth checking. '
        'The pictures in the files were textbook snippets, so the questions are text only.</p>\';\n')
anchor = '  if(B.id==="oct")h+='
assert anchor in s
s = s.replace(anchor, note + anchor, 1)
open(html_path, "w", encoding="utf-8").write(s)
print("Added KMZ bank with", len(bank["q"]), "questions")
