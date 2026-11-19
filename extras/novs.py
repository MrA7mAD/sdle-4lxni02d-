# Alshams's 17 Nov recall (WhatsApp list). First option = correct.
BY, BYR = "17 Nov exam (Alshams)", "17 Nov exam (Alshams) · rebuilt"
REC = "Recalled answer"
RSN = "Answer worked out by reasoning"
WA = "From Alshams's WhatsApp recall."
OPTW = " Only the topic and some options were recalled; the rest were written around it."
TOPIC = " The recall named only the topic; the question and options were written around it."
def ref(b): return "Where to read more: " + b
STU = ref("Ritter AV et al. Sturdevant's Art and Science of Operative Dentistry.")
NEV = ref("Neville BW et al. Oral and Maxillofacial Pathology.")
PRO = ref("Proffit WR et al. Contemporary Orthodontics.")
MCD = ref("Dean JA, ed. McDonald and Avery's Dentistry for the Child and Adolescent.")
COH = ref("Berman LH, Hargreaves KM, eds. Cohen's Pathways of the Pulp.")
ZARB = ref("Zarb G et al. Prosthodontic Treatment for Edentulous Patients.")
ROS = ref("Rosenstiel SF et al. Contemporary Fixed Prosthodontics.")
HUP = ref("Hupp JR et al. Contemporary Oral and Maxillofacial Surgery.")
ETH = ref("Saudi Commission for Health Specialties. Professionalism and Ethics Handbook (CanMEDS roles).")
CDC = ref("CDC. Guidelines for Infection Control in Dental Health-Care Settings.")
OKE = ref("Okeson JP. Bell's Orofacial Pains.")

QS = [
 dict(s=12, q="What is the minimum light intensity a halogen curing light should deliver?",
      o=["300 mW/cm²", "100 mW/cm²", "800 mW/cm²", "1000 mW/cm²"],
      e="A halogen unit below about 300 mW/cm² (many sources say 400) under-cures composite, so its output should be checked regularly with a radiometer.",
      c=RSN, r=STU, by=BY, n=WA + " The options were recalled; the answer wasn't."),
 dict(s=10, q="Enamel extends apically from the cemento-enamel junction toward the furcation as a flat extension. What is it?",
      o=["Cervical enamel projection", "Enamel pearl"],
      e="A cervical enamel projection is a flat, tongue-like extension of enamel from the CEJ into the furcation. An enamel pearl is a separate round droplet of enamel on the root.",
      c=RSN, r=NEV, by=BY, n=WA),
 dict(s=14, q="A nurse pricked herself with a needle. What type of error is this?",
      o=["Active failure", "Latent failure"],
      e="Active failures are unsafe acts by the person at the sharp end, with immediate effect. Latent failures are hidden system conditions (staffing, design, policies) that allow errors to happen.",
      c=RSN, r=ref("Reason J. Human error: models and management. BMJ 2000."), by=BY, n=WA),
 dict(s=6, q="A 12-year-old has a unilateral posterior crossbite with mandibular displacement. What is the treatment?",
      o=["Rapid palatal expansion", "Slow palatal expansion"],
      e="A unilateral crossbite with a shift usually comes from a bilaterally narrow maxilla. At 12, near the end of growth, rapid expansion opens the midpalatal suture for a skeletal effect; slow expansion suits younger children in the mixed dentition.",
      c=RSN + ". ⚠ The recall didn't give the answer; some keys pick slow expansion for a mild constriction.", r=PRO, by=BY, n=WA + " The other options were forgotten."),
 dict(s=6, q="A child has a pseudo-Class III anterior crossbite with a functional shift. What is the treatment?",
      o=["Remove the occlusal interference", "Palatal expansion"],
      e="In pseudo-Class III, an incisor interference makes the mandible slide forward. Removing it (by tipping the incisors or adjusting the contact) lets the mandible close in its true position.",
      c=RSN, r=PRO, by=BY, n=WA),
 dict(s=7, q="A 6-year-old has proximal caries that have let the neighboring teeth drift. What is the treatment?",
      o=["Stainless steel crown", "Extraction and space maintainer"],
      e="A restorable primary molar is kept: an SSC rebuilds its full mesiodistal width and contact, which stops further drifting and holds the space. Extraction with a space maintainer is for non-restorable teeth.",
      c=RSN + ". ⚠ The recall didn't give the answer or say whether the tooth was restorable.", r=MCD, by=BY, n=WA),
 dict(s=0, q="A child has pain in the lower jaw from #44. The radiograph shows an open apex with a periapical radiolucency. What is the treatment?",
      o=["Revascularization (regenerative endodontics)", "Direct pulp capping", "Pulpotomy", "Conventional RCT"],
      e="A necrotic immature tooth with apical pathology is treated by revascularization (or apexification), so the root can continue to develop. Pulp capping and pulpotomy need vital pulp; conventional RCT can't seal an open apex.",
      c=RSN, r=COH, by=BY, n=WA + " The type of pain wasn't recalled."),
 dict(s=14, q="Which CanMEDS role describes a dentist who builds rapport, listens to the patient and explains treatment so the patient can share decisions?",
      o=["Communicator", "Health advocate", "Leader", "Scholar"],
      e="The Communicator role covers the patient relationship: gathering and sharing information, empathy and shared decision-making.",
      c=RSN, r=ETH, by=BYR, n=WA + TOPIC),
 dict(s=14, q="A dentist runs oral-health awareness campaigns in local schools to improve the community's health. Which CanMEDS role is this?",
      o=["Health advocate", "Communicator", "Collaborator", "Professional"],
      e="The Health Advocate role uses expertise to improve the health of patients, communities and populations, for example through prevention and awareness.",
      c=RSN, r=ETH, by=BYR, n=WA + TOPIC),
 dict(s=0, q="A tooth has buccal bone resorption, and a gutta-percha tracing through the defect reaches the apex. No other information is given. What is the diagnosis?",
      o=["Primary endodontic lesion with secondary periodontal involvement", "Primary endodontic lesion", "True combined endo-perio lesion", "Primary periodontal lesion with secondary endodontic involvement"],
      e="A narrow tract that traces to the apex points to an endodontic source. With established buccal bone loss along the root as well, it's classed as primary endo with secondary perio involvement.",
      c=RSN + ". ⚠ The recall didn't give the answer, and it gave no caries or vitality information; with a vital-pulp test missing, the key may differ.", r=COH, by=BY, n=WA),
 dict(s=6, q="After placing orthodontic appliances, the patient feels mild pain and the teeth move slightly at first; a few weeks later there's much more movement. What causes the first, slight movement?",
      o=["Compression of the PDL", "Osteoclast activity"],
      e="The first 1–2 days of movement is the tooth shifting within the PDL space as the ligament compresses. The later, larger movement needs bone remodeling by osteoclasts after the hyalinized tissue is removed.",
      c=RSN, r=PRO, by=BY, n=WA, rep=["NOV4-84"]),
 dict(s=5, q="How many hours should a patient leave the old dentures out before impressions for a new denture?",
      o=["72 hours", "12 hours", "24 hours", "48 hours"],
      e="Abused, distorted tissues under old dentures need rest to recover their normal shape, which takes about 48–72 hours. Tissue conditioners are an alternative when the patient can't go without dentures.",
      c=RSN + ". ⚠ The recall didn't give the answer; some keys say 24 or 48 hours.", r=ZARB, by=BY, n=WA + " Came twice (on 17 and 18 Nov), once asked as when to take the impression."),
 dict(s=10, q="What is another name for hypercementosis?",
      o=["Cementum hyperplasia", "Cementoblastoma", "Concrescence", "Cemento-osseous dysplasia"],
      e="Hypercementosis (cementum hyperplasia) is excessive deposition of normal cementum on the root, giving a bulbous root.",
      c=RSN, r=NEV, by=BYR, n=WA + TOPIC),
 dict(s=4, q="Which finish line is the most hygienic?",
      o=["Supragingival", "Equigingival", "Subgingival 0.5 mm", "Subgingival 1 mm"],
      e="Supragingival margins are easiest to prepare, record, finish and clean, and they don't irritate the gingiva.",
      c=RSN, r=ROS, by=BYR, n=WA + TOPIC),
 dict(s=4, q="Two crown preparations are shown: one has a finish line that runs straight across the proximal under the papilla, the other rises interproximally to follow the gingival scallop. Which is better?",
      o=["The finish line that rises interproximally, following the gingival scallop", "The straight finish line under the papilla"],
      e="The margin should follow the scalloped CEJ and gingiva. A straight margin goes too deep interproximally under the papilla, invading the supracrestal attached tissues (biologic width).",
      c=RSN, r=ROS, by=BYR, n=WA + " The question had a picture of two crowns; it was rebuilt from the description."),
 dict(s=9, q="A patient returns the day after a surgical extraction with persistent bleeding. The site has sutures in place, and no medical history is given. What is the most appropriate management?",
      o=["Tranexamic acid", "Exploration surgery", "Fresh frozen plasma (FFP)", "Blood transfusion"],
      e="Post-extraction bleeding in a healthy patient is managed locally first: pressure, local hemostatic agents and tranexamic acid. FFP and transfusion are for coagulopathy or major blood loss.",
      c=RSN + ". ⚠ The recall didn't give the answer; some keys pick re-exploring the site.", r=HUP, by=BY, n=WA + " Recalled word for word."),
 dict(s=13, q="A dentist has a percutaneous needlestick injury from a needle contaminated with blood from an HIV-positive patient. What is the risk of HIV transmission?",
      o=["Low", "Very high", "High", "Moderate"],
      e="The risk after a percutaneous exposure to HIV-infected blood is about 0.3% (hepatitis C about 1.8%, hepatitis B up to 30% in the unvaccinated). Post-exposure prophylaxis is still started as soon as possible.",
      c=RSN, r=CDC, by=BY, n=WA + " Recalled word for word."),
 dict(s=13, q="A woman has one-sided headaches that come in episodes over months, with nausea and vomiting. What is the diagnosis?",
      o=["Migraine", "Paroxysmal hemicrania"],
      e="Migraine: unilateral throbbing headache lasting hours, with nausea, vomiting and light sensitivity. Paroxysmal hemicrania gives many short (2–30 min) orbital attacks a day with tearing, and responds to indomethacin.",
      c=RSN, r=OKE, by=BY, n=WA),
 dict(s=6, q="A space analysis shows a required space of 25 mm and an available space of 26 mm. What is the result?",
      o=["Spacing", "Normal", "Crowding"],
      e="Available space minus required space: +1 mm, so there is spacing. A negative result means crowding.",
      c=RSN, r=PRO, by=BY, n=WA),
 dict(s=1, q="You are placing an amalgam restoration, and 0.5 mm of dentin remains over the pulp. What do you place?",
      o=["GIC", "Calcium hydroxide", "Zinc oxide eugenol"],
      e="With about 0.5 mm of remaining dentin and no exposure, a glass ionomer (RMGI) base protects the pulp. Calcium hydroxide is reserved for less than 0.5 mm or a near-exposure, then covered with GIC.",
      c=RSN + "; confirmed by Rafi' Al-Maqam 16 (S02-Q82). ⚠ Some keys say calcium hydroxide.", r=STU, by=BY, n=WA),
]
