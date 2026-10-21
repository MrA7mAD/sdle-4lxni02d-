# Builds the "Deema · 20 Oct 2026" bank (questions + images) as deema.json
# Format matches the app's other banks: i, s, q, o, a, k, e, c, r, by, n, pi
import json, re, random, base64, io, sys
from PIL import Image

HTML = sys.argv[1]
OUT = sys.argv[2]
IMGDIR = "/home/claude/deema"

s = open(HTML, encoding="utf-8").read()
R16 = {q["i"]: q for q in json.loads(re.search(r'<script id="bank16" type="application/json">(.*?)</script>', s, re.S).group(1))["q"]}

def ref16(i):
    return "Rafi' Al-Maqam 16 " + i + " cites: " + R16[i]["r"]
def conf(i):   return "Confirmed: Rafi' Al-Maqam 16 gives the same answer (" + i + ")"
def cons(i):   return "Consistent with a related Rafi' Al-Maqam 16 question (" + i + ")"
NOT16 = "Not covered in Rafi' Al-Maqam 16"

BY = "Deema · 20 Oct"
BYR = "Deema · 20 Oct · rebuilt"
NOANS = "The recall gave the options but no answer; the answer here was worked out from the references."

# s = specialty index: 0 Endo, 1 Resto, 2 Perio, 3 Implant, 4 Fixed, 5 Removable, 6 Ortho, 7 Pedo,
# 8 Trauma, 9 Oral Surgery & LA, 10 Oral Med & Path, 11 Radiology, 12 Materials, 13 Medical, 14 Professionalism
# For mcq, the FIRST option is the correct one; options are shuffled below.
Q = [
 dict(s=8, q="After trauma, a permanent incisor sits out of occlusion (shorter than its neighbours). Which injury is this?",
      o=["Intrusion", "Extrusion", "Lateral luxation"],
      e="An intruded tooth is driven into the alveolar bone, so its incisal edge sits short of the occlusal plane. It is usually immobile with a high metallic percussion note. An extruded tooth looks longer and hits first, and a laterally luxated tooth is usually locked in a displaced position with an occlusal interference.",
      c=cons("S01-Q48-A"), r=ref16("S01-Q48-A"), by=BY, n=NOANS),
 dict(s=5, q="When is a mandibular lingual bar major connector contraindicated?",
      o=["Shallow lingual vestibule (less than about 8 mm from the gingival margins to the floor of the mouth)", "Deep lingual vestibule", "Healthy periodontal support on all abutments", "A Kennedy Class I edentulous arch"],
      e="A lingual bar needs about 8 mm of vertical space: roughly 4 mm for the bar plus 3–4 mm of clearance below the gingival margins. With a shallow floor of mouth there is no room, so a lingual plate is used instead.",
      c=cons("S06-Q167"), r=ref16("S06-Q167"), by=BY, n="The recall gave the two vestibule options; the other two were written in. " + NOANS),
 dict(s=6, q="Which orthodontic bracket and archwire would be most suitable for a patient with a jewellery (nickel) allergy?",
      o=["Ceramic bracket with aluminum wire", "Stainless steel bracket with aluminum wire", "Nickel steel bracket with stainless steel wire", "Ceramic bracket with stainless steel wire"],
      e="Jewellery allergy is almost always nickel allergy. Ceramic brackets contain no nickel, and stainless steel contains about 8–12% nickel, so the best choice pairs a ceramic bracket with a non-stainless wire. Nickel-free titanium (TMA/beta-titanium) wires are the usual choice in practice.",
      c="Answer worked out by reasoning; " + NOT16 + ". ⚠ Check the wire option.", r="Where to read more: Proffit WR et al. Contemporary Orthodontics. Orthodontic materials and nickel hypersensitivity.",
      by=BY, n="As recalled, the wire was \"aluminum\". There is no aluminium archwire in practice, so the exam option was most likely a nickel-free titanium wire. " + NOANS),
 dict(s=13, q="A patient taking clindamycin develops severe diarrhoea. Which organism is responsible?",
      o=["Clostridioides difficile", "Candida albicans", "Staphylococcus aureus", "Escherichia coli"],
      e="Clindamycin is one of the antibiotics most strongly linked to C. difficile overgrowth and pseudomembranous colitis. Stop the drug and refer.",
      c=conf("S10-Q55"), r=ref16("S10-Q55"), by=BY),
 dict(s=2, q="Long scenario: a patient has bleeding, multiple deep periodontal pockets and bone loss. Which bacterium is most associated?",
      o=["Tannerella forsythia", "Streptococcus mutans", "Lactobacillus species", "Actinomyces naeslundii"],
      e="T. forsythia belongs to the red complex (with P. gingivalis and T. denticola), which is linked to bleeding on probing, deep pockets and attachment loss in periodontitis. S. mutans and lactobacilli are caries organisms, and Actinomyces is an early plaque coloniser.",
      c=cons("S03-Q40-C"), r=ref16("S03-Q40-C"), by=BY),
 dict(s=4, q="A patient taking lisinopril needs a gingival retraction cord. Which agent should be avoided?",
      o=["Epinephrine", "Aluminium chloride", "Ferric sulfate", "Plain (non-medicated) cord"],
      e="Lisinopril is an ACE inhibitor, so the patient is hypertensive. Epinephrine-impregnated cord is absorbed through the sulcus and can raise heart rate and blood pressure. Aluminium chloride or ferric sulfate are the safer haemostatic agents.",
      c=cons("S10-Q48"), r=ref16("S10-Q48"), by=BY, n=NOANS),
 dict(s=1, k="card", q="Which burs or instruments are used to finish and polish a Class IV composite restoration?",
      n="Deema remembered an option of \"2 carbide burs and 1 diamond\" but not the answer. In general, a Class IV composite is contoured with fine or extra-fine finishing diamonds or 12–30-fluted carbide finishing burs, then polished with graded discs, rubber points and polishing paste.",
      r="Where to read more: Ritter AV et al. Sturdevant's Art and Science of Operative Dentistry. Finishing and polishing composite restorations.",
      c="No answer recorded in the recall", by=BY),
 dict(s=2, q="A labially positioned tooth has a thin band of keratinized gingiva and is planned for periodontal (mucogingival) surgery. What should be considered first?",
      o=["Orthodontic treatment to move the tooth back into the alveolar bone", "Root canal treatment", "Extraction", "Crown"],
      e="Labial malposition thins the bone and gingiva over the root. Moving the tooth into the alveolar housing first often thickens the tissue and reduces the need for grafting, or improves the result if surgery is still needed.",
      c="Answer worked out by reasoning; " + NOT16, r="Where to read more: Newman MG et al. Newman and Carranza's Clinical Periodontology. Mucogingival therapy and orthodontic considerations.",
      by=BY, n=NOANS),
 dict(s=10, k="open", q="An irregular brown macule on the palate is an incidental finding. What is the diagnosis?",
      o=["Nevus (the first word was not recalled)", "Melanotic macule"],
      n="Deema couldn't recall the answer. The palate is the most common oral site for a nevus, while melanotic macules are more typical of the lower lip and gingiva. Either way, an irregular pigmented palatal lesion needs a biopsy to rule out melanoma, since the palate is also the most common site of oral melanoma.",
      r=ref16("S10-Q96-D"), c="No answer recorded in the recall", by=BY),
 dict(s=5, k="open", q="In a complete denture, the \"F\" sound comes out like \"V\". Where are the maxillary anterior teeth positioned?",
      o=["Too far anterior and too incisal", "Too far anterior and too cervical", "Too far palatal"],
      n="Deema couldn't recall the answer. For F and V, the incisal edges of the maxillary incisors should lightly touch the wet-dry line of the lower lip. When these sounds are distorted, the incisors are set either too short or long, or too far labial or palatal. Check this one against Zarb (phonetics in complete-denture tooth arrangement).",
      r="Where to read more: Zarb GA et al. Prosthodontic Treatment for Edentulous Patients. Phonetics and anterior tooth arrangement.",
      c="No answer recorded in the recall", by=BY),
 dict(s=2, q="Which root of the maxillary first molar is most commonly resected?",
      o=["Distobuccal", "Mesiobuccal", "Palatal", "Distobuccal and palatal"],
      e="The distobuccal root is the shortest and smallest, sits close to the furcation and is often the one with bone loss. Removing it affects the tooth's support least, so it is the root most often resected.",
      c="Answer worked out by reasoning; " + NOT16 + ". Saud's File gives the same answer.", r="Where to read more: Newman MG et al. Newman and Carranza's Clinical Periodontology. Furcation involvement and root resection.",
      by=BY, n=NOANS),
 dict(s=6, k="open", q="A patient is a mouth breather. Which appliance is used?",
      o=["Oral (vestibular) screen", "Rapid maxillary expansion", "Removable appliance with Z-spring", "Headgear"],
      n="The recall only said \"mouth breather, which appliance\"; the options were written in. An oral (vestibular) screen is the habit-breaking appliance that trains lip seal and nasal breathing once any airway obstruction is ruled out. Rapid maxillary expansion is used when there is also a narrow maxilla or crossbite, and Rafi' Al-Maqam 19 gives \"expansion\" for this topic.",
      r=ref16("S07-Q11-H"), c="No answer recorded in the recall", by=BYR),
 dict(s=13, q="What is the maximum epinephrine dose per appointment for a patient with significant cardiovascular disease?",
      o=["0.04 mg", "0.01 mg", "0.2 mg", "0.4 mg"],
      e="For cardiac patients the limit is 0.04 mg, about two 1.8-mL cartridges of 1:100,000 epinephrine. For a healthy adult the maximum is 0.2 mg.",
      c="Consistent with the October 2026 bank (OCT-65); " + NOT16, r="Where to read more: Malamed SF. Handbook of Local Anesthesia. Vasoconstrictor doses in cardiovascular disease.",
      by=BY, n="The recall gave 0.04 and 0.01; the other options were written in. " + NOANS),
 dict(s=10, q="Long scenario: a patient has brief, unilateral, electric-shock-like facial pain. What is the diagnosis?",
      o=["Trigeminal neuralgia", "Atypical facial pain", "Temporomandibular disorder", "Postherpetic neuralgia"],
      e="Paroxysms of unilateral electric-shock pain lasting seconds, often set off by light touch at a trigger zone and followed by a refractory period, are classic trigeminal neuralgia.",
      c=conf("S10-Q26"), r=ref16("S10-Q26"), by=BY),
 dict(s=5, q="Which occlusal scheme is used for a complete denture opposing a removable partial denture?",
      o=["Bilateral balanced occlusion", "Unilateral balanced occlusion", "Mutually protected occlusion", "Canine guidance"],
      e="A complete denture needs contacts on both sides during excursions to stay stable, so bilateral balanced occlusion is used. Canine guidance and mutually protected occlusion tip a complete denture.",
      c=cons("S06-Q33-A"), r=ref16("S06-Q33-A"), by=BY, n="The recall gave unilateral and bilateral occlusion; the other options were written in. " + NOANS),
 dict(s=13, k="open", q="A patient with liver cirrhosis needs local anaesthesia. Which agent should be given?",
      o=["Bupivacaine", "Xylocaine (lidocaine)", "Procaine", "Prilocaine"],
      n="Deema couldn't recall the answer, and the references disagree. Amides (lidocaine, bupivacaine, prilocaine) are broken down in the liver. Some answer keys therefore pick an ester (procaine). Others pick prilocaine, which is partly metabolised outside the liver, or articaine if it's offered. Whatever the agent, use the lowest dose and check INR and platelets first.",
      r=ref16("S10-Q33-E"), c="No answer recorded in the recall", by=BY),
 dict(s=10, q="Histology shows Reed-Sternberg cells. What is the diagnosis?",
      o=["Hodgkin lymphoma", "Burkitt lymphoma", "Multiple myeloma", "Langerhans cell histiocytosis"],
      e="Reed-Sternberg cells (large binucleate \"owl-eye\" cells) are the hallmark of Hodgkin lymphoma, which typically presents as painless cervical lymphadenopathy.",
      c="Recall answer; " + NOT16 + ". Saud's File gives the same answer.", r="Where to read more: Neville BW et al. Oral and Maxillofacial Pathology. Hodgkin lymphoma.",
      by=BY),
 dict(s=6, q="Apertognathia (skeletal open bite) is most commonly associated with which skeletal pattern?",
      o=["Vertical maxillary excess", "Short lower facial height", "Class II division 2 with deep bite", "Mandibular retrognathia with a low angle"],
      e="Apertognathia is an open bite. Skeletal open bites typically come with excess vertical growth of the posterior maxilla, a long lower face and a steep mandibular plane.",
      c="Recall answer; Salem's Prep gives the same answer (SAL-763). Rafi' Al-Maqam 19 links it to mandibular prognathism instead.", r="Where to read more: Proffit WR et al. Contemporary Orthodontics. Vertical problems and long-face pattern.",
      by=BYR, n="The recall gave only \"Apertognathia? Maxillary excess\"; the question and other options were written around that answer."),
 dict(s=5, q="Teeth 18, 17 and 16 are missing, 24 and 26 are missing, and 25 is non-restorable. What is the Kennedy classification?",
      o=["Kennedy Class II, modification 1", "Kennedy Class I, modification 1", "Kennedy Class III, modification 1", "Kennedy Class II, modification 2"],
      e="Classify after planned extractions, so 25 counts as missing. The right side is a distal-extension space (18, 17, 16), giving Class II. The left side (24–26) is one additional bounded space, so it is modification 1. This assumes 27 is present.",
      c="Applegate's rules as applied in Rafi' Al-Maqam 16 (" + "S06-Q125" + ")", r=ref16("S06-Q125"),
      by=BYR, n="No options were recalled; they were written in. The answer assumes 27 is still present."),
 dict(s=6, q="A 14-year-old with Class I malocclusion has a single anterior tooth in crossbite. What is the treatment?",
      o=["Removable appliance with a Z-spring", "Fixed appliance", "Chin cup", "Observe until growth is complete"],
      e="A single dental anterior crossbite with adequate space in a cooperative patient is corrected with a removable appliance and a Z-spring or finger spring, with posterior bite blocks to open the bite.",
      c=cons("S07-Q29"), r=ref16("S07-Q29"), by=BY, n=NOANS),
 dict(s=6, q="What is the first tissue reaction 24–48 hours after placing orthodontic force?",
      o=["Hyalinization", "Apposition", "Deposition", "Osteoblast activity"],
      e="With typical orthodontic forces, blood flow in the compressed PDL is cut off within minutes and the area becomes cell-free (hyalinized) within hours to days. Tooth movement then waits for undermining resorption from the adjacent marrow spaces.",
      c="Answer worked out by reasoning; " + NOT16 + ". Saud's File gives the same answer.", r="Where to read more: Proffit WR et al. Contemporary Orthodontics. The biologic basis of orthodontic therapy.",
      by=BY, n=NOANS),
 dict(s=11, q="A radiograph shows loss of the lamina dura and a fibrous-dysplasia-like (ground-glass) bone pattern. Which condition is most likely?",
      o=["Hyperparathyroidism", "Hypertension", "Diabetes mellitus", "Hypothyroidism"],
      e="Hyperparathyroidism causes generalized loss of lamina dura with a granular or ground-glass bone pattern, and sometimes brown tumours.",
      c=cons("S10-Q288-E"), r=ref16("S10-Q288-E"), by=BY, n=NOANS),
 dict(s=10, q="A patient has desquamative gingivitis and white striae on the buccal mucosa. What is the diagnosis?",
      o=["Erosive lichen planus", "Mucous membrane pemphigoid", "Pemphigus vulgaris", "Linear IgA disease"],
      e="Desquamative gingivitis has several causes, but bilateral reticular white (Wickham) striae on the buccal mucosa point to lichen planus. Pemphigoid and pemphigus do not produce striae.",
      c=conf("S10-Q52"), r=ref16("S10-Q52"), by=BY, n=NOANS),
 dict(s=4, k="open", q="Tooth 35 is retained with a good crown and root, and tooth 13 has a poor prognosis. What is the plan?",
      o=["Retain 35", "Crown on 35", "Extraction and implant", "Extraction and space closure"],
      n="The recall of this scenario is incomplete, so no answer is given. Work it out from the full case if you meet it again.",
      c="No answer recorded in the recall", by=BY),
 dict(s=2, q="A patient develops an ulcer in the area of 35 and 36 two days after scaling. What is the management?",
      o=["Reassurance and follow-up", "Another round of scaling", "Systemic antibiotics", "Incisional biopsy"],
      e="A small ulcer after instrumentation is a traumatic ulcer and heals on its own within 1–2 weeks. Review it, and biopsy only if it hasn't healed by about 2 weeks.",
      c=cons("S03-Q93-A"), r=ref16("S03-Q93-A"), by=BY, n=NOANS),
 dict(s=12, q="A patient reports a sulfur allergy. Which elastomeric impression material should be avoided?",
      o=["Polysulfide", "Polyvinyl siloxane (addition silicone)", "Polyether", "Condensation silicone"],
      e="Polysulfide (mercaptan rubber) is based on a sulfur-containing polymer. Addition silicone and polyether are sulfur-free alternatives.",
      c="Answer worked out by reasoning; " + NOT16, r="Where to read more: Anusavice KJ et al. Phillips' Science of Dental Materials. Elastomeric impression materials.",
      by=BYR, n="The recall only said \"patient allergy to sulfur, which impression?\"; the options were written in."),
 dict(s=10, q="After an episode of erythema multiforme treated with corticosteroids, the patient wants definitive treatment to prevent recurrence. What is given?",
      o=["Suppressive antiviral therapy (e.g., acyclovir)", "Long-term systemic corticosteroids", "Systemic antibiotics", "Topical antifungal"],
      e="Most recurrent erythema multiforme is triggered by herpes simplex, so continuous antiviral suppression reduces recurrences. Corticosteroids treat the acute episode but don't prevent the next one.",
      c=conf("S10-Q181"), r=ref16("S10-Q181"), by=BYR, n="The options were written in."),
 dict(s=14, q="Infection-control case: what is the first and most important measure to prevent cross-infection?",
      o=["Hand hygiene", "Wearing gloves", "Autoclaving instruments", "Using a rubber dam"],
      e="Hand hygiene is the single most important measure. It comes before gloving and between every patient, and gloves don't replace it.",
      c=cons("S09-Q63"), r=ref16("S09-Q63"), by=BYR, n="The recall said \"case about hand hygiene first\"; the question and options were written around that."),
 dict(s=5, q="What is the minimum number of clasp assemblies for a Kennedy Class I RPD?",
      o=["2", "1", "3", "4"],
      e="A Kennedy Class I (bilateral distal extension) RPD needs one direct retainer on each side, next to each extension, so the minimum is 2. A Class II needs 3, and a Class III needs 4 (quadrilateral).",
      c="Answer worked out by reasoning; " + NOT16 + ". Saud's File gives the same answer.", r="Where to read more: Carr AB et al. McCracken's Removable Partial Prosthodontics. Direct retainers and RPD design.",
      by=BY, n=NOANS),
 dict(s=7, q="A newborn has small keratin-filled cysts along the midpalatal raphe. What are they?",
      o=["Epstein pearls", "Bohn nodules", "Dental lamina cysts", "Natal teeth"],
      e="Epstein pearls lie along the midpalatal raphe. Bohn nodules are on the buccal and lingual alveolar ridges or the junction of hard and soft palate, and dental lamina cysts are on the alveolar crest. All resolve on their own.",
      c="Recall answer; " + NOT16 + ". Rafi' Al-Maqam 19 gives the same answer (R19-OM-120).", r="Where to read more: Neville BW et al. Oral and Maxillofacial Pathology. Developmental defects: palatal cysts of the newborn.",
      by=BYR, n="The recall said \"Midpalatal — Epstein pearl\"; the question and other options were written around that."),
 dict(s=8, k="open", q="After trauma, a tooth has a cervical root fracture with no mobility (the type of trauma wasn't specified). How long is it splinted?",
      o=["2 weeks", "4 weeks"],
      n="The recall didn't say which injury, so the answer depends on it. A root fracture is splinted for 4 weeks, and up to 4 months for a cervical-third fracture. A subluxation is splinted for up to 2 weeks only for comfort, and a concussion needs no splint.",
      r=ref16("S01-Q68"), c="No answer recorded in the recall", by=BY),
 dict(s=11, q="Bilateral small round radiolucencies are seen between the first molar and premolar regions of the mandible. What are they?",
      o=["Mental foramen", "Periapical granulomas", "Lateral periodontal cysts", "Stafne bone cavity"],
      e="The mental foramen appears as a round radiolucency near the premolar apices, bilaterally. It moves relative to the root on angled films, and the tooth tests vital.",
      c=cons("S01-Q19-D"), r=ref16("S01-Q19-D"), by=BY, n="Deema's recalled answer, marked \"not sure\"; the options were written in."),
 dict(s=4, k="card", q="Long case: a patient needs anterior crown impressions and has a thin gingival phenotype. What should be considered before the impression?",
      n="Deema couldn't recall the options, only that \"thin retraction cord\" wasn't one of them. For a thin phenotype, Rafi' Al-Maqam 16 recommends gentle displacement with a small-diameter cord, avoiding trauma and recession.",
      r=ref16("S05-Q2"), c="No answer recorded in the recall", by=BY),
 dict(s=0, q="What is the narrowest part of the root canal?",
      o=["Apical constriction", "Anatomical apex", "Radiographic apex", "Apical foramen"],
      e="The apical constriction (minor diameter) is the narrowest part of the canal, usually 0.5–1 mm short of the foramen. It is the ideal end point for preparation and obturation.",
      c=conf("S01-Q224"), r=ref16("S01-Q224"), by=BY, n=NOANS),
 dict(s=8, q="A patient had trauma 3 days ago (see photo). What is the treatment?", img="img-009.png",
      o=["Pulpotomy (partial / Cvek)", "Direct pulp capping and MTA", "Root canal treatment", "Extraction"],
      e="The photo shows a complicated crown fracture with a small pulp exposure. After a delay of days, a partial (Cvek) pulpotomy removes the superficially inflamed pulp and has a better prognosis than direct pulp capping, which is reserved for very recent, tiny exposures.",
      c=cons("S01-Q166"), r=ref16("S01-Q166"), by=BY, n=NOANS),
 dict(s=0, q="An asymptomatic dens evaginatus is found (see photo). What is the treatment?", img="img-010.png",
      o=["Grinding (careful, gradual reduction with dentin protection)", "Observe with follow-up", "Root canal treatment"],
      e="The tubercle usually contains a pulp horn and fractures or wears, which can expose the pulp. Prevention is gradual grinding with protection of the exposed dentin, or reinforcing it with sealant or composite. Root canal treatment is only for pulp disease.",
      c="Consistent with the October 2026 bank (OCT10-37, OCT14-102)", r="Where to read more: Berman LH, Hargreaves KM, eds. Cohen's Pathways of the Pulp. Dens evaginatus.",
      by=BY, n=NOANS),
 dict(s=2, q="What type of bone loss is shown in this radiograph?", img="img-011.png",
      o=["Severe horizontal bone loss", "Severe vertical bone loss", "Moderate horizontal bone loss"],
      e="The crest is level across the incisors with no angular defects, so the loss is horizontal. It reaches about half the root length or more, which counts as severe.",
      c="Answer judged from the image; " + NOT16, r="Where to read more: Newman MG et al. Newman and Carranza's Clinical Periodontology. Radiographic assessment of bone loss.",
      by=BY, n=NOANS),
 dict(s=7, q="A child needs two extractions and has a history of an unpleasant dental visit. What is the management?",
      o=["Nitrous oxide–oxygen sedation", "Treat as usual", "General anaesthesia"],
      e="A cooperative but anxious child having a short procedure is a classic indication for nitrous oxide–oxygen inhalation sedation. General anaesthesia is for children who can't cooperate or need extensive treatment.",
      c=cons("S10-Q38"), r=ref16("S10-Q38"), by=BY, n=NOANS),
 dict(s=2, q="What working angle should the curette face make with the tooth during scaling?",
      o=["45–90°", "90–110°", "0–15°", "110–130°"],
      e="The working angulation is 45–90° (ideally about 70–80°). At 0° the blade is inserted under the gingiva, and above 90° it burnishes calculus and traumatises the soft tissue.",
      c=conf("S03-Q57"), r=ref16("S03-Q57"), by=BY, n="The recall gave 45–90 and 90–110; the other options were written in. " + NOANS),
 dict(s=13, q="Which test is used to diagnose epilepsy?",
      o=["Electroencephalography (EEG)", "Electrocardiography (ECG)", "Electromyography (EMG)", "Panoramic radiograph"],
      e="An EEG records the brain's electrical activity and shows epileptiform discharges.",
      c="Recall answer; " + NOT16, r="Where to read more: Little JW et al. Dental Management of the Medically Compromised Patient. Seizure disorders.",
      by=BY, n="The options were written in."),
 dict(s=9, q="A canine space infection (shown with a photo in the exam) most commonly arises from which tooth?",
      o=["Maxillary canine", "Mandibular canine", "Maxillary second molar", "Maxillary central incisor"],
      e="The long maxillary canine root ends above the levator anguli oris, so infection spreads into the canine space. This swells the upper lip and cheek and obliterates the nasolabial fold.",
      c=cons("S10-Q111-C"), r=ref16("S10-Q111-C"), by=BYR, n="The recall only said \"canine space infection photo\"; the question and options were written in."),
]


# ---- Version 2: every recall item is a scored MCQ (former practice-only items replaced) ----
WARN = " ⚠ The recall had no answer and the references disagree; the best-supported answer is used."
REPL = {
 7: dict(s=1, q="Which instruments are used to finish and polish a Class IV composite restoration?",
      o=["Fine finishing diamonds or multifluted (12–30-blade) carbide burs, then polishing discs, rubber points and paste",
         "Coarse diamond burs only", "Plain steel round burs", "Pumice in a rubber cup only"],
      e="Gross contouring uses fine or extra-fine finishing diamonds or multifluted carbide finishing burs. The surface is then refined with graded discs, rubber points or cups, and polishing paste. Coarse diamonds and steel burs leave a rough surface, and pumice alone can't shape the restoration.",
      c="Answer worked out by reasoning; not covered in Rafi' Al-Maqam 16", r="Where to read more: Ritter AV et al. Sturdevant's Art and Science of Operative Dentistry. Finishing and polishing composite restorations.",
      by=BYR, n="Deema remembered an option of \"2 carbide burs and 1 diamond\" but not the answer, so the options were written in."),
 9: dict(s=10, q="An irregular brown macule on the palate is an incidental finding. What is the most likely diagnosis?",
      o=["Nevus (intramucosal)", "Melanotic macule", "Amalgam tattoo", "Physiologic pigmentation"],
      e="The hard palate is the most common oral site for a nevus, while an oral melanotic macule is most typical of the lower lip vermilion and gingiva. Because the palate is also the commonest site of oral melanoma, an irregular pigmented palatal lesion should still be biopsied.",
      c="Answer worked out by reasoning; " + NOT16 + "." + WARN, r=ref16("S10-Q96-D"),
      by=BY, n="Deema recalled \"…. nevus\" (first word missing) and melanotic macule but not the answer; two options were written in."),
 10: dict(s=5, q="In a complete denture, the \"F\" sound comes out like \"V\". How are the maxillary anterior teeth positioned?",
      o=["Too far incisally (too long)", "Too far cervically (too short)", "Too far palatally"],
      e="For F and V, the maxillary incisal edges should lightly touch the wet-dry line of the lower lip. If the incisors are too long, they press into the lip and \"F\" sounds like \"V\". If they are too short, \"V\" sounds like \"F\".",
      c="Answer worked out by reasoning; " + NOT16 + "." + WARN, r="Where to read more: Zarb GA et al. Prosthodontic Treatment for Edentulous Patients. Phonetics and anterior tooth arrangement.",
      by=BY, n="Recalled as \"anterior more incisal / anterior more cervical / anterior more palatal\". " + NOANS),
 12: dict(s=6, q="A child has a mouth-breathing habit with no nasal obstruction. Which appliance is used?",
      o=["Oral (vestibular) screen", "Rapid maxillary expansion", "Removable appliance with Z-spring", "Headgear"],
      e="The oral (vestibular) screen is the habit-breaking appliance: it blocks the oral airway and trains lip seal and nasal breathing, once any airway obstruction has been ruled out. Rapid maxillary expansion is used when there is also a narrow maxilla or posterior crossbite.",
      c="Answer worked out by reasoning; " + cons("S07-Q11-H") + ". Rafi' Al-Maqam 19 gives \"expansion\" for this topic." + WARN, r=ref16("S07-Q11-H"),
      by=BYR, n="The recall only said \"mouth breather, which appliance\"; the options were written in."),
 16: dict(s=13, q="A patient with liver cirrhosis needs local anaesthesia. Which agent is preferred?",
      o=["Prilocaine", "Bupivacaine", "Xylocaine (lidocaine)", "Procaine"],
      e="Amides are broken down in the liver, so their effect and toxicity are prolonged in cirrhosis. Prilocaine is the best choice here because part of its metabolism happens outside the liver, in the lungs and kidneys. Bupivacaine is long-acting and the most dependent on the liver. Procaine is an ester, but the plasma cholinesterase that breaks it down is made by the liver and is low in cirrhosis. If articaine is offered, choose it. Use the lowest effective dose and check INR and platelets.",
      c="Answer worked out by reasoning; " + cons("S10-Q33-E") + "." + WARN, r=ref16("S10-Q33-E"),
      by=BY, n=NOANS),
 24: dict(s=4, q="A retained primary canine has a good crown and root, and the permanent canine 13 has a poor prognosis (e.g., impacted). What is the plan?",
      o=["Retain the primary canine", "Crown the primary canine", "Extraction and implant", "Extraction and space closure"],
      e="A retained primary tooth with a good root and no successor that can be brought into place is kept as long as it stays functional and esthetic. It can last for years. An implant or prosthesis is planned only once it fails.",
      c="Answer worked out by reasoning; " + NOT16, r="Where to read more: Proffit WR et al. Contemporary Orthodontics. Impacted canines and retained primary teeth.",
      by=BYR, n="Recalled as \"retained 35 … and the 13 poor prognosis\". It most likely meant the primary canine 53 (the numbers swapped), so the question was rewritten that way. The options are as recalled."),
 31: dict(s=8, q="After trauma, a permanent tooth has a cervical root fracture and the coronal fragment shows no mobility. How long is it splinted?",
      o=["4 weeks", "2 weeks"],
      e="Root fractures are stabilised with a flexible splint for 4 weeks. Cervical-third fractures may benefit from up to 4 months. 2 weeks is the splint time for subluxation (only if needed for comfort), avulsion and extrusion.",
      c=cons("S01-Q68") + "." + WARN, r=ref16("S01-Q68"),
      by=BY, n="Deema said the type of trauma wasn't specified; the question is answered as a root fracture."),
 33: dict(s=4, q="Long case: a patient needs anterior crown impressions and has a thin gingival phenotype. What should be considered before the impression?",
      o=["Gentle gingival displacement with a small-diameter cord to avoid recession", "Electrosurgical troughing of the sulcus", "Double-cord technique with large cords", "Firmly packing an epinephrine cord"],
      e="Thin gingiva recedes easily after trauma, so displacement must be gentle: a small-diameter cord, placed lightly and for a short time. Electrosurgery, large cords and firm packing all risk permanent recession at the visible margin.",
      c=conf("S05-Q2"), r=ref16("S05-Q2"),
      by=BYR, n="Deema couldn't recall the options, only that \"thin retraction cord\" wasn't one of them; the options were written in."),
}
for k, v in REPL.items(): Q[k-1] = v
Q += [
 dict(s=13, q="Calculation case: a 20-kg child needs ibuprofen at 10 mg/kg per dose. What is the single dose?",
      o=["200 mg", "100 mg", "400 mg", "20 mg"],
      e="10 mg/kg × 20 kg = 200 mg per dose, every 6–8 hours. The usual paediatric range is 4–10 mg/kg per dose.",
      c=cons("S10-Q61"), r=ref16("S10-Q61"),
      by=BYR, n="The recall only said there were two calculation cases, one on ibuprofen; the numbers here are an example of that type."),
 dict(s=0, q="Calculation case: what is the diameter 16 mm from the tip (D16) of a size 30 file with a 0.04 taper?",
      o=["0.94 mm", "0.62 mm", "0.46 mm", "1.10 mm"],
      e="Diameter = tip size + (distance × taper) = 0.30 + (16 × 0.04) = 0.30 + 0.64 = 0.94 mm.",
      c="Consistent with Rafi' Al-Maqam 16 file-dimension questions (S01-Q67)", r=ref16("S01-Q67"),
      by=BYR, n="The recall only said the second calculation case was about a file; the numbers here are an example of that type."),
 dict(s=0, q="Long scenario: a tooth has a necrotic pulp, an apical radiolucency and a narrow isolated pocket tracking to the apex. What is the first treatment?",
      o=["Root canal treatment, then reassess the periodontal defect", "Periodontal surgery first", "Extraction", "Scaling and root planing only"],
      e="This is a primary endodontic lesion. The pocket is a sinus tract draining along the PDL and often heals after root canal treatment alone, so endodontic treatment comes first and the periodontium is re-evaluated after healing.",
      c=cons("S01-Q32-B"), r=ref16("S01-Q32-B"),
      by=BYR, n="The recall only said \"long scenario endo-perio lesion\"; the question was written around the usual version of this case."),
 dict(s=4, q="Long scenario: a single crown is planned on tooth 36 in a patient with normal anterior guidance. Which articulator is appropriate?",
      o=["Semi-adjustable articulator", "Fully adjustable articulator", "Simple hinge articulator", "No articulator is needed"],
      e="A semi-adjustable articulator with a facebow reproduces condylar guidance well enough for routine fixed work. A fully adjustable articulator with pantographic records is reserved for complex full-mouth rehabilitation.",
      c="Consistent with Rafi' Al-Maqam 16 articulator questions (S06-Q69)", r=ref16("S06-Q69"),
      by=BYR, n="The recall only said \"long scenario about 36 molar, fully adjustable / semi adjustable\"; the scenario was written in."),
]

rng = random.Random(2010)
out, img = [], {}
for n, d in enumerate(Q, 1):
    qid = "DEEMA-%d" % n
    k = d.get("k", "mcq")
    o = d.get("o", [])
    q = {"i": qid, "s": d["s"], "q": d["q"], "o": o, "a": [], "k": k}
    if k == "mcq":
        idx = list(range(len(o))); rng.shuffle(idx)
        q["o"] = [o[i] for i in idx]; q["a"] = [idx.index(0)]
        q["e"] = d["e"]
    for f in ("c", "r", "by", "n"):
        if d.get(f): q[f] = d[f]
    if d.get("img"):
        im = Image.open(IMGDIR + "/" + d["img"]).convert("RGB")
        buf = io.BytesIO(); im.save(buf, "WEBP", quality=82)
        key = qid + "_0"
        img[key] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
        q["pi"] = [key]
    out.append(q)

json.dump({"q": out, "img": img}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
from collections import Counter
print(len(out), "questions;", Counter(q["k"] for q in out), "; images", len(img))
print("by specialty:", sorted(Counter(q["s"] for q in out).items()))
