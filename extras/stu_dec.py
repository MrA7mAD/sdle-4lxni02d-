import json,re
M={r['id']:r for r in json.load(open('/home/claude/stu/matches.json'))}
Q={q['i']:q for q in json.load(open('/home/claude/stu/rq.json'))}
B="Sturdevant's Art and Science of Operative Dentistry, 7th ed."
def ref(pg,ch): 
    n,t=re.match(r'(\d+) \((.*)\)?',ch).groups(); t=t.rstrip(')')
    return f"{B}, ch. {n} ({t}), p. {pg}"+(" (online chapter)" if str(pg).startswith('e') else "")
CH={}
for r in M.values():
    for m in r['m']: CH[str(m['pg'])]=m['ch']
P=json.load(open('/home/claude/stu/pages.json'))
for p in P:
    if p['pg'] and p['ch']: CH.setdefault(str(p['pg']),p['ch'])
OFF=re.compile(r'kennedy|clasp|\brpd\b|denture|implant|orthodon|headgear|malocclusion|skeletal|cephalo|wits|biopsy|granuloma|lymphoma|abscess|mronj|osteonecrosis|tubercul|third molar|impacted|graft|submandibular|hemophilia|addison|ibuprofen|irrigat|perforat|resorption|dens |uvula|avuls|vitality|pulpotomy|wrong tooth|lichen|nevus|recession|miller|furcation|oroantral|flap|sedation|cleft|frenum|frenectomy|diastema|stafne|drool|odontoma|mobility|periodontal instrument|angina|varix|crossbite|sna|cantilever|needlestick|flask|gypsum|titanium|scalpel|philtrum|neglect|crown fracture|root fracture|post extending|kennedy|incisors being|probing depth|endodontic retreat|root canal treatment on tooth|canal|melanotic|white sponge|parkinson|diabetic patient|glucose|blood-filled|submucous|calculus|biologic|biological width|junctional|anterior determinant|surgical guide|steroid|caliber',re.I)
OUT={}
for i,r in M.items():
    m=r['m'][0]
    if m['s']<32 or OFF.search(r['q']): continue
    OUT[i]={'ref':ref(m['pg'],m['ch'])}
# manual page overrides / additions
MAN={'R19-Resto-7':6,'R19-Resto-27':6,'SAUD-5':6,'SAUD-313':6,'SAUD-1361':6,'R19-Resto-28':10,'SAUD-1501':10,'SAUD-1502':10,'SAUD-1651':10,'SAL-142':10,'S02-Q4':10,
 'SEP-Sultan-47':116,'SAUD-2195':116,'SAUD-2310':116,'R19-Resto-14':116,'SAL-465':12,'SAUD-946':12,'SAUD-1394':75,'SAUD-314':75,'SAL-012':75,'SEP-Muath-28':75,
 'SAUD-450':325,'SEP-Muath-42':471,'S02-Q75':'e28','S02-Q72':'e41','SAUD-608':'e41','S02-Q28-A':'e23','S02-Q28-B':'e23','SAL-079':106,'S02-Q133':106,'R19-Resto-40':106,
 'S02-Q106':393,'SAUD-2359':393,'S02-Q87':396,'OCT14-84':479,'SAUD-653':319,'SAUD-624':483,'SAUD-2488':130,'SAUD-1843':315,'SAUD-1920':315,'SAL-471':315,'SAL-468':315,'S02-Q81':315,'S02-Q101':315,
 'SAUD-1102':360,'OCT14-2':360,'SAL-234':106,'S02-Q62':106,'S02-Q102':278,'SEP-Rakan-32':'e110' }
for k,pg in MAN.items():
    if k in Q: OUT[k]={'ref':ref(pg,CH[str(pg)])}
def fx(k,ans,n): OUT[k]['ans']=ans; OUT[k]['n']=n
W="⚠ Corrected per Sturdevant 7e"
fx('R19-Resto-7','Spindles',W+" p. 6: pain during preparation limited to enamel is explained by enamel spindles (odontoblastic processes crossing the DEJ), not tufts.")
for k,a in (('SAUD-313','Enamel spindle'),('SAUD-1361','Spindel')): fx(k,a,W+" p. 6: enamel spindles may act as pain receptors, explaining sensitivity during preparation confined to enamel.")
OUT['SAUD-5']['n']="⚠ Sturdevant 7e p. 6 names enamel spindles for pain limited to enamel; spindles are not among these options."
fx('R19-Resto-28','Reparative dentin',W+" p. 10: after a strong injury/pulp exposure, secondary odontoblast-like cells form reparative (tertiary) dentin — not secondary dentin.")
fx('SEP-Sultan-47',Q['SEP-Sultan-47']['o'][3],W+" p. 116: superficial marginal staining of a bonded restoration is corrected by a shallow, narrow marginal repair; deep staining → replacement. Microabrasion is for enamel surface defects.")
fx('SAL-465','4',W+" p. 12: four embrasures radiate from each contact — facial, lingual, occlusal/incisal and gingival.")
fx('SAUD-946','4',W+" p. 12: four embrasures — facial, lingual, occlusal/incisal and gingival.")
fx('SAUD-1394','open contact',W+" pp. 73–75: restorations with open contacts, open margins or overhangs are listed caries risk factors (and open contacts cause food impaction/perio problems).")
for k in ('SAUD-2195','SAUD-2310'): fx(k,Q[k]['o'][0],"Sturdevant 7e p. 116 (with p. 102): marginal ditching deeper than 0.5 mm that predisposes to caries is an indication to replace the amalgam.")
fx('SAUD-450','connect the cavities',"Sturdevant 7e p. 325: at least ~1.6 mm (premolars) or ~2 mm (molars) of tooth structure should remain between the margin and the proximal surface; with only 1.5 mm left the lesions are joined into one preparation.")
OUT['SAUD-624']['n']="⚠ Sturdevant 7e p. 483: under composite, a thin RMGI liner is placed in the deepest part of deeper preparations; calcium hydroxide is only for preparations very close to the pulp (RDT < 0.5 mm, p. 315)."
OUT['SAUD-2488']['n']="⚠ Sturdevant 7e p. 130: calcium hydroxide stimulates reparative (tertiary) dentin, not secondary dentin."
OUT['SAL-234']['n']="⚠ Sturdevant 7e p. 106: a rounded notch on facial cervical surfaces from brushing = abrasion; a wedge-shaped cervical defect from flexure = abfraction. The stem alone doesn't decide it."
for k in ('R19-Resto-46','OCT10-42','SAUD-2507','SAUD-2063'):
    if k in Q: OUT.setdefault(k,{})['n']="⚠ Recalls disagree (amalgam expansion vs undetected pulp exposure); Sturdevant 7e doesn't address this scenario directly. Deep undercuts in dentinal line angles near the pulp point most to a mechanical pulp exposure."
json.dump(OUT,open('/home/claude/sdle-4lxni02d-/extras/book_sturdevant.json','w'),ensure_ascii=False,indent=0)
print(len(OUT),sum(1 for v in OUT.values() if 'ans' in v))
for k in ('SEP-Sultan-95','SEP-Rakan-81','SEP-Rakan-83','SEP-Rakan-58','JA-Jul-240','SAL-106','SEP-Sultan-67'):
    OUT.pop(k,None)
OUT['OCT10-42'].pop('ref',None)
OUT['SAL-474']={'ref':ref(280,CH['280'])}
json.dump(OUT,open('/home/claude/sdle-4lxni02d-/extras/book_sturdevant.json','w'),ensure_ascii=False,indent=0)
print(len(OUT))
