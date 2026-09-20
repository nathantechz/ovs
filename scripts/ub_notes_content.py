#!/usr/bin/env python3
"""
Authored content for the University of Bisha diploma notes.

Every factual claim carries the book, edition and printed page it came from.
Pages were read out of the cached wiki (scripts/build-wiki.py), whose page
markers are corrected by the offset measured for each book, so a citation
points at the page a student turns to.

Where a textbook predates current practice, the claim stays cited to the book
and a separate "what is happening now" section carries the update, marked as
such. Nothing in the cited sections is sourced from anywhere but the books.

Rendered by scripts/build-ub-notes.py.
"""

# Shortened citation handles used throughout.
KANSKI = "Kanski 8e, p. {}"
KHURANA = "Khurana, Comprehensive Ophthalmology, p. {}"

KANSKI_FULL = (
    "<strong>Kanski's Clinical Ophthalmology: A Systematic Approach</strong>, "
    "Jack J. Kanski &amp; Brad Bowling, 8th Edition, Elsevier, 2016"
)
IACLE_FULL = (
    "<strong>The IACLE Contact Lens Course</strong>, International Association "
    "of Contact Lens Educators, First Edition"
)
BROOKS_FULL = (
    "<strong>System for Ophthalmic Dispensing</strong>, Clifford W. Brooks &amp; "
    "Irvin M. Borish, 3rd Edition, Butterworth-Heinemann, 2007"
)
SCHWARTZ_FULL = (
    "<strong>Visual Perception: A Clinical Orientation</strong>, Steven H. "
    "Schwartz, 4th Edition, McGraw-Hill, 2010"
)
BORISH_FULL = (
    "<strong>Borish's Clinical Refraction</strong>, William J. Benjamin (ed.), "
    "2nd Edition, Butterworth-Heinemann, 2006"
)
VON_NOORDEN_FULL = (
    "<strong>Binocular Vision and Ocular Motility: Theory and Management of "
    "Strabismus</strong>, Gunter K. von Noorden &amp; Emilio C. Campos"
)
EVANS_FULL = (
    "<strong>Pickwell's Binocular Vision Anomalies</strong>, Bruce J. W. Evans, "
    "Elsevier, 2005"
)
VOI_FULL = "<strong>Visual Optical Instruments</strong>"
CT_GOV = (
    "<strong>ClinicalTrials.gov</strong> — trial records as cited, retrieved "
    "20 September 2026."
)


# ---------------------------------------------------------------------------
# Reusable figures. Drawn rather than lifted: the textbook photographs are
# copyrighted, so notes cite the figure number instead of reproducing it.
# ---------------------------------------------------------------------------

FIG_EYELID_ANATOMY = """
<svg viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Sagittal section of the eyelid showing levator aponeurosis, Muller muscle, tarsal plate, orbital septum and the pretarsal and preseptal orbicularis">
  <path d="M120 40 Q 150 150 175 250 Q 185 290 210 300" fill="none" stroke="#9ca3af" stroke-width="2"/>
  <text x="70" y="45" font-size="12" fill="#6b7280">Orbital septum</text>

  <path d="M170 60 Q 200 140 215 210" fill="none" stroke="#0066cc" stroke-width="3"/>
  <text x="185" y="55" font-size="12" fill="#0066cc" font-weight="bold">Levator</text>
  <text x="185" y="70" font-size="11" fill="#0066cc">aponeurosis</text>

  <path d="M215 150 Q 228 185 235 215" fill="none" stroke="#7c3aed" stroke-width="3"/>
  <text x="248" y="175" font-size="12" fill="#7c3aed" font-weight="bold">Müller muscle</text>

  <rect x="212" y="215" width="26" height="85" rx="5" fill="#fca5a5" stroke="#dc2626" stroke-width="1.5"/>
  <text x="255" y="265" font-size="12" fill="#b91c1c" font-weight="bold">Tarsal plate</text>

  <circle cx="185" cy="255" r="14" fill="#fde68a" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="95" y="258" font-size="11" fill="#b45309">Pretarsal</text>
  <text x="95" y="272" font-size="11" fill="#b45309">orbicularis</text>

  <circle cx="160" cy="170" r="16" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="70" y="168" font-size="11" fill="#b45309">Preseptal</text>
  <text x="70" y="182" font-size="11" fill="#b45309">orbicularis</text>

  <path d="M300 90 Q 380 170 300 265" fill="none" stroke="#6b7280" stroke-width="2"/>
  <text x="330" y="180" font-size="12" fill="#6b7280">Globe</text>

  <text x="60" y="325" font-size="11.5" fill="#374151">Levator + Müller raise the lid · orbicularis closes it · the tarsal plate gives the lid its shape</text>
</svg>
"""

FIG_LID_MALPOSITION = """
<svg viewBox="0 0 640 260" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Comparison of normal lid position, entropion with the lid margin turned inward, and ectropion with the lid margin turned outward">
  <g>
    <text x="55" y="30" font-size="13" fill="#374151" font-weight="bold">Normal</text>
    <path d="M30 90 Q 90 70 150 90" fill="none" stroke="#6b7280" stroke-width="2.5"/>
    <ellipse cx="90" cy="120" rx="58" ry="34" fill="#e0f2fe" stroke="#6b7280" stroke-width="1.5"/>
    <path d="M30 150 Q 90 172 150 150" fill="none" stroke="#16a34a" stroke-width="3"/>
    <line x1="60" y1="152" x2="58" y2="166" stroke="#16a34a" stroke-width="1.5"/>
    <line x1="90" y1="158" x2="90" y2="173" stroke="#16a34a" stroke-width="1.5"/>
    <line x1="120" y1="152" x2="122" y2="166" stroke="#16a34a" stroke-width="1.5"/>
    <text x="42" y="200" font-size="11" fill="#15803d">lashes point away</text>
  </g>

  <g transform="translate(210,0)">
    <text x="40" y="30" font-size="13" fill="#b91c1c" font-weight="bold">Entropion</text>
    <path d="M30 90 Q 90 70 150 90" fill="none" stroke="#6b7280" stroke-width="2.5"/>
    <ellipse cx="90" cy="120" rx="58" ry="34" fill="#fee2e2" stroke="#6b7280" stroke-width="1.5"/>
    <path d="M30 150 Q 90 134 150 150" fill="none" stroke="#dc2626" stroke-width="3"/>
    <line x1="60" y1="146" x2="62" y2="132" stroke="#dc2626" stroke-width="1.5"/>
    <line x1="90" y1="140" x2="90" y2="126" stroke="#dc2626" stroke-width="1.5"/>
    <line x1="120" y1="146" x2="118" y2="132" stroke="#dc2626" stroke-width="1.5"/>
    <text x="24" y="200" font-size="11" fill="#b91c1c">margin rolls IN — lashes abrade cornea</text>
  </g>

  <g transform="translate(420,0)">
    <text x="40" y="30" font-size="13" fill="#b45309" font-weight="bold">Ectropion</text>
    <path d="M30 90 Q 90 70 150 90" fill="none" stroke="#6b7280" stroke-width="2.5"/>
    <ellipse cx="90" cy="120" rx="58" ry="34" fill="#fef3c7" stroke="#6b7280" stroke-width="1.5"/>
    <path d="M30 150 Q 90 190 150 150" fill="none" stroke="#d97706" stroke-width="3"/>
    <rect x="66" y="166" width="48" height="12" rx="4" fill="#fca5a5" stroke="#d97706" stroke-width="1"/>
    <text x="20" y="200" font-size="11" fill="#b45309">margin rolls OUT — conjunctiva exposed</text>
  </g>
</svg>
"""

FIG_CORNEA_LAYERS = """
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="The five layers of the cornea from anterior to posterior: epithelium, Bowman layer, stroma, Descemet membrane and endothelium, with thicknesses">
  <rect x="90" y="40" width="380" height="34" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="482" y="62" font-size="12.5" fill="#1d4ed8" font-weight="bold">Epithelium</text>
  <text x="100" y="62" font-size="11" fill="#1e40af">surface / wing / basal cells — regenerates</text>

  <rect x="90" y="74" width="380" height="16" fill="#bfdbfe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="482" y="87" font-size="12.5" fill="#1d4ed8" font-weight="bold">Bowman layer</text>
  <text x="100" y="87" font-size="10.5" fill="#1e40af">does NOT regenerate — injury scars</text>

  <rect x="90" y="90" width="380" height="140" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="482" y="165" font-size="12.5" fill="#1d4ed8" font-weight="bold">Stroma</text>
  <text x="100" y="150" font-size="11" fill="#1e40af">~90% of thickness · regular collagen lamellae = transparency</text>
  <text x="100" y="170" font-size="11" fill="#1e40af">avascular — nutrition from aqueous and tears</text>

  <rect x="90" y="230" width="380" height="14" fill="#bfdbfe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="482" y="242" font-size="12.5" fill="#1d4ed8" font-weight="bold">Descemet</text>

  <rect x="90" y="244" width="380" height="20" fill="#93c5fd" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="482" y="259" font-size="12.5" fill="#1d4ed8" font-weight="bold">Endothelium</text>
  <text x="100" y="259" font-size="10.5" fill="#1e3a8a">pumps fluid out — does not divide</text>

  <text x="30" y="150" font-size="11" fill="#6b7280" transform="rotate(-90 30 150)" text-anchor="middle">tears → aqueous</text>

  <text x="90" y="292" font-size="12" fill="#374151"><tspan font-weight="bold">11.5 mm</tspan> vertical · <tspan font-weight="bold">12 mm</tspan> horizontal · <tspan font-weight="bold">540 µm</tspan> central</text>
  <text x="90" y="310" font-size="12" fill="#374151">~<tspan font-weight="bold">three-quarters</tspan> of the eye's optical power · most densely innervated tissue in the body</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Course 1 — Ocular Diseases (10 topics x 3 h = 30 h)
# ---------------------------------------------------------------------------

OCULAR_DISEASES = {
    "name": "Ocular Diseases",
    "slug": "ocular-diseases",
    "summary": (
        "Ten topics covering the eyelids, conjunctiva, cornea, lens and retina — "
        "what each condition is, what it looks like at the slit lamp, the "
        "measurements and tests that identify it, and when it must be referred."
    ),
    "wco": (
        "Primarily <strong>Category 3 — Ocular Diagnostic Services</strong>: "
        "detecting, recognising and triaging ocular disease. At diploma level "
        "the expectation is accurate recognition, correct urgency of referral "
        "and management of minor conditions within national scope — not "
        "therapeutic prescribing, which sits in WCO Category 4."
    ),
    "grounding": (
        "Every clinical claim is cited to " + KANSKI_FULL + ", with "
        "Khurana's <em>Comprehensive Ophthalmology</em> as a second source. "
        "Current-practice sections draw on ClinicalTrials.gov and named "
        "consensus reports, and are marked separately from textbook content."
    ),
    "topics": [
        # ---------------------------------------------------------------- 1
        {
            "slug": "01-introduction-to-ophthalmic-diseases",
            "title": "Introduction to Ophthalmic Diseases",
            "hours": 3,
            "summary": (
                "How to look at an eye systematically, the vocabulary used to "
                "describe what you find, and the red flags that change a routine "
                "examination into an urgent referral."
            ),
            "wco": (
                "<strong>Category 3 — Ocular Diagnostic Services.</strong> This "
                "topic establishes the examination sequence and the referral "
                "thresholds that every later topic depends on."
            ),
            "sections": [
                {
                    "heading": "1. Work front to back, every time",
                    "blocks": [
                        {"type": "prose", "text":
                            "Kanski is organised anatomically — eyelids, lacrimal system, "
                            "orbit, dry eye, conjunctiva, cornea, sclera, lens, glaucoma, "
                            "uvea, retina, then neuro-ophthalmology. That order is not "
                            "editorial convenience; it is the order in which you examine "
                            "an eye, and adopting it means you stop missing things."},
                        {"type": "table",
                         "headers": ["Structure", "Kanski chapter", "Starts at"],
                         "rows": [
                             ["Eyelids", "Chapter 1", "p. 1"],
                             ["Lacrimal drainage system", "Chapter 2", "p. 63"],
                             ["Orbit", "Chapter 3", "p. 77"],
                             ["Dry eye / tear film", "Chapter 4", "p. 119"],
                             ["Conjunctiva", "Chapter 5", "p. 131"],
                             ["Cornea", "Chapter 6", "p. 167"],
                             ["Lens", "Chapter 9", "p. 269"],
                             ["Glaucoma", "Chapter 10", "p. 305"],
                             ["Uveitis", "Chapter 11", "p. 395"],
                             ["Retinal vascular disease", "Chapter 13", "p. 519"],
                             ["Retinal detachment", "Chapter 16", "p. 681"],
                         ],
                         "source": "Chapter openings, Kanski 8e"},
                        {"type": "callout", "variant": "clinical",
                         "title": "Turn the sequence into a habit",
                         "text":
                            "Lids → lashes → lid margin → conjunctiva → cornea → anterior "
                            "chamber → iris → lens → (dilate) → vitreous → disc → macula → "
                            "periphery. Say it under your breath while you work. The "
                            "conditions you will miss are the ones in the step you skipped."},
                    ],
                },
                {
                    "heading": "2. Symptoms point to the tissue",
                    "blocks": [
                        {"type": "prose", "text":
                            "Non-specific symptoms of surface inflammation include "
                            "<strong>lacrimation, grittiness, stinging and burning</strong>. "
                            "Two symptoms are far more specific and are worth memorising.",
                         "cite": KANSKI.format(132)},
                        {"type": "list", "items": [
                            "<strong>Itching is the hallmark of allergic disease</strong>, "
                            "although it may occur to a lesser extent in blepharitis and dry eye.",
                            "<strong>Significant pain, photophobia or marked foreign body "
                            "sensation suggest corneal involvement</strong> — the cornea is "
                            "the most densely innervated tissue in the body.",
                        ], "source": "Kanski 8e, p. 132 and p. 168"},
                        {"type": "callout",
                         "title": "Reasoning from one symptom",
                         "text":
                            "A patient who itches has allergy until proved otherwise. A "
                            "patient with true photophobia has a cornea problem until proved "
                            "otherwise. Neither is a diagnosis, but each tells you which "
                            "chapter you are in."},
                    ],
                },
                {
                    "heading": "3. Red flags — refer, do not observe",
                    "blocks": [
                        {"type": "list", "intro":
                            "These findings appear throughout the topics that follow. "
                            "Whatever else you conclude, any of them ends the routine "
                            "examination:",
                         "items": [
                            "<strong>Corneal melting or thinning</strong>, or an epithelial "
                            "defect that is not closing",
                            "<strong>Perforation</strong>, with or without iris plugging",
                            "<strong>A white corneal infiltrate</strong> — treat as "
                            "microbial keratitis until proved otherwise",
                            "<strong>Sudden painless loss of vision</strong>",
                            "<strong>Sudden onset of flashes, floaters or a field defect</strong> "
                            "— retinal detachment",
                            "<strong>A fixed, mid-dilated pupil with a hazy cornea and a hard, "
                            "painful eye</strong> — angle closure",
                         ],
                         "source": "Complications sections throughout Kanski 8e; "
                                   "dry eye complications at p. 126"},
                        {"type": "callout", "variant": "clinical",
                         "title": "Your job at diploma level",
                         "text":
                            "You are not expected to treat these. You are expected to "
                            "<em>recognise</em> them and to get the patient in front of "
                            "someone who can, with the right urgency. A correct referral "
                            "made today is worth more than a diagnosis made next week."},
                    ],
                },
                {
                    "heading": "4. Describing what you see",
                    "blocks": [
                        {"type": "table",
                         "headers": ["Term", "Means"],
                         "rows": [
                             ["<strong>Papillae</strong>", "Vascular core at the centre — "
                              "non-specific, but a feature of allergic and bacterial disease"],
                             ["<strong>Follicles</strong>", "Lymphoid aggregates, vessels at "
                              "the periphery — viral and chlamydial disease"],
                             ["<strong>Punctate epithelial erosions</strong>", "Pinpoint "
                              "epithelial loss staining with fluorescein"],
                             ["<strong>Infiltrate</strong>", "White stromal opacity — cellular "
                              "collection, may be sterile or microbial"],
                             ["<strong>Hypopyon</strong>", "Layered white cells in the "
                              "anterior chamber"],
                             ["<strong>Madarosis</strong>", "Loss of lashes"],
                             ["<strong>Trichiasis</strong>", "Misdirected lashes touching the globe"],
                             ["<strong>Poliosis</strong>", "Whitening of the lashes"],
                         ],
                         "source": "Terminology used throughout Kanski 8e Chapters 1, 5 and 6"},
                        {"type": "callout",
                         "title": "Papillae or follicles?",
                         "text":
                            "It is the single most useful distinction on the tarsal "
                            "conjunctiva. Look at where the vessel is. Centre of the bump = "
                            "papilla. Vessels sweeping around the outside of a pale bump = "
                            "follicle. Papillae lean allergic or bacterial; follicles lean "
                            "viral or chlamydial."},
                    ],
                },
            ],
            "check": [
                "In what order do you examine an eye, and why does the order matter?",
                "A patient's only symptom is itching. Which group of conditions moves to the top of your list?",
                "Why does marked photophobia point to the cornea specifically?",
                "Distinguish a papilla from a follicle at the slit lamp.",
                "List four findings that end a routine examination and trigger referral.",
                "Define madarosis, trichiasis and poliosis.",
            ],
            "sources": [
                KANSKI_FULL + " — Chapter openings; conjunctival symptoms p. 132; "
                "corneal innervation p. 168; dry eye complications p. 126.",
            ],
        },

        # ---------------------------------------------------------------- 2
        {
            "slug": "02-eyelid-disorders-ptosis-blepharospasm",
            "title": "Eyelid Disorders: Ptosis and Blepharospasm",
            "hours": 3,
            "summary": (
                "The four causes of ptosis, the five measurements that classify it, "
                "and how blepharospasm differs from a lid that simply cannot lift."
            ),
            "wco": (
                "<strong>Category 3 — Ocular Diagnostic Services</strong>, with the "
                "measurement set sitting in <strong>Category 2</strong>. You are "
                "expected to measure and classify ptosis accurately and to recognise "
                "the neurogenic causes that need urgent referral."
            ),
            "sections": [
                {
                    "heading": "1. What ptosis is, and its four causes",
                    "blocks": [
                        {"type": "prose", "text":
                            "<strong>Ptosis is an abnormally low position of the upper "
                            "lid</strong>; it may be congenital or acquired.",
                         "cite": KANSKI.format(38)},
                        {"type": "list", "intro": "Kanski classifies it by mechanism:",
                         "items": [
                            "<strong>Neurogenic ptosis</strong> — an innervational defect "
                            "such as <strong>third nerve paresis</strong> or "
                            "<strong>Horner syndrome</strong>.",
                            "<strong>Myogenic ptosis</strong> — a myopathy of the levator "
                            "itself, or impaired transmission at the neuromuscular junction "
                            "(neuromyopathic). Acquired myogenic ptosis occurs in "
                            "<strong>myasthenia gravis</strong>, <strong>myotonic "
                            "dystrophy</strong> and <strong>progressive external "
                            "ophthalmoplegia</strong>.",
                            "<strong>Aponeurotic (involutional) ptosis</strong> — a defect "
                            "in the levator aponeurosis. This is the common age-related form.",
                            "<strong>Mechanical ptosis</strong> — the gravitational effect "
                            "of a mass, or scarring.",
                         ], "source": "Kanski 8e, p. 38"},
                        {"type": "figure", "svg": FIG_EYELID_ANATOMY,
                         "caption": "Eyelid anatomy in section. Compare with Kanski 8e "
                                    "Fig. 1.57 (p. 45). The levator and Müller muscle raise "
                                    "the lid; failure at different points in this diagram "
                                    "produces the four classes of ptosis."},
                    ],
                },
                {
                    "heading": "2. The measurements",
                    "blocks": [
                        {"type": "prose", "text":
                            "Ptosis is classified by numbers, not impressions. These are "
                            "the five you record, and they are examined constantly."},
                        {"type": "subheading", "text": "Margin–reflex distance (MRD)"},
                        {"type": "prose", "text":
                            "Measured to the corneal light reflex from a light held by the "
                            "examiner on which the patient fixates. The "
                            "<strong>normal measurement is 4–5 mm</strong>.",
                         "cite": KANSKI.format(40)},
                        {"type": "subheading", "text": "Palpebral fissure height"},
                        {"type": "prose", "text":
                            "The distance between the upper and lower lid margins, measured "
                            "in the pupillary plane. The upper lid margin normally rests "
                            "about <strong>2 mm below the upper limbus</strong> and the "
                            "lower <strong>1 mm above the lower limbus</strong>. The "
                            "measurement is shorter in males (<strong>7–10 mm</strong>) than "
                            "in females (<strong>8–12 mm</strong>).",
                         "cite": KANSKI.format(40)},
                        {"type": "subheading", "text": "Severity grading"},
                        {"type": "table",
                         "headers": ["Grade", "Amount"],
                         "rows": [["Mild", "up to 2 mm"], ["Moderate", "3 mm"],
                                  ["Severe", "4 mm or more"]],
                         "source": "Kanski 8e, p. 40"},
                        {"type": "subheading", "text": "Levator function (upper lid excursion)"},
                        {"type": "steps", "intro": "This is a procedure — do it exactly:",
                         "items": [
                            "Place your <strong>thumb firmly against the patient's brow</strong> "
                            "to negate the action of frontalis.",
                            "Start with the eyes in <strong>downgaze</strong>.",
                            "Ask the patient to look up <strong>as far as possible</strong>.",
                            "Measure the amount of excursion with a rule.",
                         ], "source": "Kanski 8e, p. 40, Fig. 1.51"},
                        {"type": "table",
                         "headers": ["Levator function", "Excursion"],
                         "rows": [["Normal", "15 mm or more"], ["Good", "12–14 mm"],
                                  ["Fair", "5–11 mm"], ["Poor", "4 mm or less"]],
                         "source": "Kanski 8e, p. 40"},
                        {"type": "callout", "variant": "clinical",
                         "title": "If you forget the thumb, the number is wrong",
                         "text":
                            "Frontalis will lift the brow and inflate your excursion "
                            "measurement, making poor levator function look fair. Since "
                            "levator function decides which operation the patient gets, "
                            "this is not a trivial error."},
                        {"type": "subheading", "text": "Upper lid crease"},
                        {"type": "prose", "text":
                            "The vertical distance between the lid margin and the lid crease "
                            "in downgaze — about <strong>10 mm in females</strong> and "
                            "<strong>8 mm in males</strong>. <strong>Absence of the crease "
                            "in congenital ptosis is evidence of poor levator function</strong>, "
                            "whereas <strong>a high crease suggests an aponeurotic "
                            "defect</strong> (usually involutional).",
                         "cite": KANSKI.format(40)},
                        {"type": "callout",
                         "title": "One measurement that gives you the diagnosis",
                         "text":
                            "The crease is the cheapest discriminator you have. High crease "
                            "in an elderly patient with good levator function = aponeurotic "
                            "ptosis. Absent crease in a child = poor levator function and "
                            "congenital ptosis. You have narrowed the classification before "
                            "touching anything else."},
                    ],
                },
                {
                    "heading": "3. Surgical options — know what the numbers decide",
                    "blocks": [
                        {"type": "table",
                         "headers": ["Procedure", "Indication", "Levator function needed"],
                         "rows": [
                             ["<strong>Müller muscle / conjunctival resection</strong>",
                              "Mild ptosis — maximal elevation achievable is 2–3 mm. "
                              "Includes most Horner syndrome and mild congenital ptosis",
                              "Good — at least 10 mm"],
                             ["<strong>Levator advancement (resection)</strong>",
                              "Ptosis of any cause; extent of resection set by severity "
                              "and levator function",
                              "At least 5 mm"],
                             ["<strong>Brow (frontalis) suspension</strong>",
                              "Severe ptosis (&gt;4 mm) — third nerve palsy, "
                              "blepharophimosis, failed previous levator resection",
                              "Very poor — under 4 mm"],
                         ],
                         "source": "Kanski 8e, p. 45"},
                        {"type": "callout", "variant": "clinical",
                         "title": "Why a diploma optometrist records these",
                         "text":
                            "You will not perform the surgery, but your measurements decide "
                            "which one is possible. A referral letter carrying MRD, fissure "
                            "height, levator function and crease position is immediately "
                            "actionable. One saying \"droopy lid\" is not."},
                    ],
                },
                {
                    "heading": "4. Blepharospasm",
                    "blocks": [
                        {"type": "prose", "text":
                            "Blepharospasm is involuntary forced closure of the lids by "
                            "spasm of the orbicularis. It is a <em>closing</em> problem; "
                            "ptosis is an <em>opening</em> problem. The distinction matters "
                            "because the treatments are unrelated."},
                        {"type": "prose", "text":
                            "<strong>Botulinum toxin injection to the orbicularis muscle "
                            "may help control the blepharospasm that often occurs in severe "
                            "dry eye.</strong> Injected at the medial canthus it can also "
                            "reduce tear drainage, presumably by limiting lid movement.",
                         "cite": KANSKI.format(129)},
                        {"type": "callout",
                         "title": "The link worth remembering",
                         "text":
                            "Kanski places blepharospasm treatment inside the <em>dry eye</em> "
                            "chapter. Severe ocular surface disease drives reflex spasm. If "
                            "you meet blepharospasm, examine the ocular surface before "
                            "assuming a primary neurological cause."},
                        {"type": "list", "intro": "Also consider, and exclude:", "items": [
                            "<strong>Reflex spasm</strong> from any painful ocular surface "
                            "condition — corneal foreign body, abrasion, severe dry eye",
                            "<strong>Hemifacial spasm</strong> — unilateral, involves the "
                            "lower face as well, suggests a seventh nerve cause",
                            "<strong>Benign essential blepharospasm</strong> — bilateral, "
                            "progressive, a focal dystonia, needs neurology input",
                        ]},
                    ],
                },
            ],
            "check": [
                "Name the four mechanistic classes of ptosis, with one cause of each.",
                "What is the normal MRD, and how is it measured?",
                "Give the normal palpebral fissure height for males and for females.",
                "Describe how to measure levator function, including the step most often forgotten.",
                "A patient has 14 mm levator function and a high lid crease. Which class of ptosis, and why?",
                "Which ptosis operation requires levator function of at least 5 mm?",
                "Why should you examine the ocular surface in a patient with blepharospasm?",
            ],
            "sources": [
                KANSKI_FULL + " — Ptosis classification p. 38; measurements and grading "
                "p. 40; surgical indications p. 45; botulinum toxin for blepharospasm p. 129.",
            ],
        },

        # ---------------------------------------------------------------- 3
        {
            "slug": "03-eyelid-malpositions",
            "title": "Eyelid Malpositions: Entropion, Ectropion and Dermatitis",
            "hours": 3,
            "summary": (
                "Why an ageing lid turns in or out, the bedside tests that show which "
                "mechanism has failed, and why entropion threatens the cornea while "
                "ectropion threatens the tear film."
            ),
            "wco": (
                "<strong>Category 3 — Ocular Diagnostic Services.</strong> Recognition, "
                "the lid laxity tests, and correct referral. Temporary protective "
                "measures such as lubricants and taping fall within diploma scope."
            ),
            "sections": [
                {
                    "heading": "1. The two malpositions",
                    "blocks": [
                        {"type": "figure", "svg": FIG_LID_MALPOSITION,
                         "caption": "Entropion turns the margin inward so lashes abrade the "
                                    "cornea; ectropion turns it outward and exposes the tarsal "
                                    "conjunctiva. Compare Kanski 8e Figs 1.61 and 1.67."},
                        {"type": "callout",
                         "title": "One sentence that separates them",
                         "text":
                            "<strong>Entropion is a corneal problem</strong> — inturned lashes "
                            "abrade the epithelium. <strong>Ectropion is a tear film and "
                            "surface problem</strong> — the punctum no longer reaches the tear "
                            "lake, so the eye waters while the exposed conjunctiva dries."},
                    ],
                },
                {
                    "heading": "2. Involutional ectropion",
                    "blocks": [
                        {"type": "prose", "text":
                            "Involutional (age-related) ectropion <strong>affects the lower "
                            "lid of elderly patients</strong>. It causes "
                            "<strong>epiphora</strong> (tear overflow) and may exacerbate "
                            "ocular surface disease. The red appearance of the exposed "
                            "conjunctiva is cosmetically poor. In long-standing cases the "
                            "tarsal conjunctiva may become chronically inflamed, thickened "
                            "and <strong>keratinized</strong>.",
                         "cite": KANSKI.format(45)},
                        {"type": "subheading", "text": "The horizontal lid laxity test"},
                        {"type": "steps", "intro":
                            "This is the key bedside test and it has a precise threshold:",
                         "items": [
                            "Take the <strong>central part of the lower lid</strong> between "
                            "finger and thumb.",
                            "Pull it away from the globe. <strong>Laxity is demonstrated by "
                            "pulling the lid 8 mm or more from the globe.</strong>",
                            "Release it and watch. The abnormal finding is <strong>failure "
                            "to snap back to its normal position without the patient first "
                            "blinking</strong>.",
                         ], "source": "Kanski 8e, p. 45"},
                        {"type": "callout", "variant": "clinical",
                         "title": "The detail candidates lose marks on",
                         "text":
                            "It is not enough that the lid returns slowly. The test is "
                            "positive if it needs <em>a blink</em> to reseat. Watch the lid, "
                            "not the clock, and do not let the patient blink until you have "
                            "seen the result."},
                    ],
                },
                {
                    "heading": "3. Other types of ectropion",
                    "blocks": [
                        {"type": "list", "items": [
                            "<strong>Paralytic ectropion</strong> — from facial nerve palsy. "
                            "Permanent treatment options include <strong>medial "
                            "canthoplasty</strong> and a <strong>lateral canthal sling</strong>, "
                            "in which a refashioned canthal tendon from the lower lid is "
                            "passed through a buttonhole in the tendon from the upper lid.",
                            "<strong>Mechanical ectropion</strong> — caused by tumours on or "
                            "near the lid margin dragging it outward.",
                            "<strong>Cicatricial ectropion</strong> — scarring of the skin "
                            "shortening the anterior lamella.",
                        ], "source": "Kanski 8e, pp. 45–50, Fig. 1.66"},
                        {"type": "callout", "variant": "clinical",
                         "title": "Mechanical ectropion is a referral, urgently",
                         "text":
                            "A lid pulled out of position by a mass means there is a mass. "
                            "Do not record \"ectropion\" and arrange a review — examine the "
                            "lid margin properly and refer any lesion."},
                    ],
                },
                {
                    "heading": "4. Involutional entropion — four mechanisms",
                    "blocks": [
                        {"type": "list", "intro":
                            "Kanski lists the contributing factors. Each is testable at the "
                            "slit lamp:",
                         "items": [
                            "<strong>Horizontal lid laxity</strong> — the same test as for "
                            "ectropion.",
                            "<strong>Vertical lid instability</strong> caused by attenuation, "
                            "dehiscence or disinsertion of the <strong>lower lid retractors</strong>. "
                            "Weakness is recognised by <strong>decreased excursion of the lower "
                            "lid in downgaze</strong>.",
                            "<strong>Over-riding of the pretarsal by the preseptal "
                            "orbicularis</strong> during lid closure. This moves the lower "
                            "border of the tarsal plate anteriorly, away from the globe, and "
                            "the upper border towards the globe — <strong>tipping the lid "
                            "inwards</strong>.",
                            "<strong>Orbital septum laxity</strong> with prolapse of orbital "
                            "fat into the lower lid.",
                         ], "source": "Kanski 8e, p. 50, Fig. 1.67B"},
                        {"type": "callout",
                         "title": "Test the retractors in ten seconds",
                         "text":
                            "Ask the patient to look down and watch the lower lid. A normal "
                            "lid follows the eye downward. A lid that stays put has weak "
                            "retractors — the second mechanism on the list, and one you can "
                            "document without any equipment."},
                    ],
                },
                {
                    "heading": "5. Management within your scope",
                    "blocks": [
                        {"type": "prose", "text":
                            "For entropion, <strong>temporary protection must be as "
                            "short-term as possible</strong>. Options include "
                            "<strong>lubricants, taping, soft bandage contact lenses</strong> "
                            "and <strong>orbicularis chemodenervation with botulinum "
                            "toxin</strong>.",
                         "cite": KANSKI.format(50)},
                        {"type": "callout", "variant": "clinical",
                         "title": "Read that instruction carefully",
                         "text":
                            "\"As short-term as possible\" is the textbook telling you that "
                            "taping is a bridge to surgery, not a management plan. Every day "
                            "of inturned lashes is another day of corneal abrasion. Tape the "
                            "lid <em>and</em> make the referral."},
                    ],
                },
                {
                    "heading": "6. Eyelid dermatitis",
                    "blocks": [
                        {"type": "prose", "text":
                            "Eyelid skin is the thinnest in the body and reacts readily. "
                            "Kanski associates specific skin disease with specific forms of "
                            "lid margin disease, which is the practical link for this topic."},
                        {"type": "table",
                         "headers": ["Lid condition", "Commonly associated skin disease"],
                         "rows": [
                             ["Staphylococcal anterior blepharitis", "<strong>Atopic dermatitis</strong>"],
                             ["Seborrhoeic anterior blepharitis", "<strong>Seborrhoeic dermatitis</strong>"],
                             ["Posterior blepharitis (MGD)", "<strong>Acne rosacea</strong>"],
                         ],
                         "source": "Kanski 8e, Table 1.4, p. 34"},
                        {"type": "prose", "text":
                            "<strong>Angular blepharitis</strong> is usually caused by "
                            "<strong>Moraxella lacunata</strong> or <strong>S. aureus</strong>. "
                            "Red, scaly, macerated and fissured skin is seen at the lateral "
                            "and/or medial canthi. Note that <strong>skin chafing secondary "
                            "to tear overflow</strong>, especially at the lateral canthus, can "
                            "cause a similar clinical picture and may predispose to infection. "
                            "Treatment involves topical chloramphenicol, bacitracin or "
                            "erythromycin.",
                         "cite": KANSKI.format(38)},
                        {"type": "callout",
                         "title": "The loop you must spot",
                         "text":
                            "Ectropion causes tear overflow. Tear overflow chafes the lateral "
                            "canthal skin. Chafed skin looks like — and predisposes to — "
                            "angular blepharitis. Treating the infection without correcting "
                            "the lid position guarantees recurrence."},
                    ],
                },
            ],
            "check": [
                "State the threshold distance and the release criterion for the horizontal lid laxity test.",
                "Why does ectropion cause watering, and ectropion of which lid?",
                "List the four mechanisms contributing to involutional entropion.",
                "How do you test lower lid retractor weakness without equipment?",
                "Which malposition threatens the cornea, and by what mechanism?",
                "Name the skin disease associated with posterior blepharitis.",
                "Why is taping an entropion not a management plan?",
            ],
            "sources": [
                KANSKI_FULL + " — Involutional ectropion and the laxity test p. 45; "
                "paralytic and mechanical ectropion pp. 45–50, Fig. 1.66; involutional "
                "entropion mechanisms and treatment p. 50, Fig. 1.67B; blepharitis "
                "associations Table 1.4 p. 34; angular blepharitis p. 38.",
            ],
        },
    ],
}


# --- Ocular Diseases topics 4-10 -------------------------------------------

OCULAR_DISEASES["topics"] += [
    {
        "slug": "04-eyelid-infections-and-inflammation",
        "title": "Eyelid Infections and Inflammation",
        "hours": 3,
        "summary": (
            "Chronic blepharitis in its anterior and posterior forms — why the "
            "symptoms never match the signs, the table that separates the three "
            "types, and the lid hygiene that actually works."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services.</strong> Blepharitis "
            "is the commonest lid condition you will meet and the one most often "
            "managed entirely within diploma scope through lid hygiene and "
            "ocular lubrication."
        ),
        "sections": [
            {
                "heading": "1. Why blepharitis is difficult",
                "blocks": [
                    {"type": "prose", "text":
                        "Chronic blepharitis (chronic marginal blepharitis) is a "
                        "<strong>very common cause of ocular discomfort and irritation</strong>. "
                        "Kanski is unusually frank about why it frustrates clinicians: "
                        "<strong>the poor correlation between symptoms and signs, the "
                        "uncertain aetiology and mechanisms of the disease process all "
                        "combine to make management difficult</strong>.",
                     "cite": KANSKI.format(34)},
                    {"type": "callout",
                     "title": "Set the patient's expectations on day one",
                     "text":
                        "Because symptoms and signs correlate poorly, a patient can look "
                        "better and feel no different. Tell them at the first visit that "
                        "this is a condition to be controlled rather than cured, and that "
                        "hygiene is lifelong. Patients who are not told this stop after "
                        "two weeks and conclude the treatment failed."},
                ],
            },
            {
                "heading": "2. Anterior and posterior — the division",
                "blocks": [
                    {"type": "prose", "text":
                        "Blepharitis may be subdivided into anterior and posterior, "
                        "<strong>although there is considerable overlap and both types are "
                        "often present (mixed blepharitis)</strong>.",
                     "cite": KANSKI.format(34)},
                    {"type": "subheading", "text": "Anterior blepharitis"},
                    {"type": "list", "items": [
                        "Affects the area <strong>surrounding the bases of the "
                        "eyelashes</strong>; may be <strong>staphylococcal</strong> or "
                        "<strong>seborrhoeic</strong>.",
                        "Regarded as related more to chronic infective elements and hence "
                        "<strong>more amenable to treatment and remission</strong> than the "
                        "posterior form.",
                        "In staphylococcal blepharitis an aetiological factor may be an "
                        "<strong>abnormal cell-mediated response to components of the cell "
                        "wall of S. aureus</strong>, which may also be responsible for the "
                        "red eyes and peripheral corneal infiltrates seen in some patients. "
                        "It is more common and more marked in patients with "
                        "<strong>atopic dermatitis</strong>.",
                        "Seborrhoeic blepharitis is strongly associated with generalised "
                        "<strong>seborrhoeic dermatitis</strong> involving the scalp, "
                        "nasolabial folds, skin behind the ears and the sternum.",
                    ], "source": "Kanski 8e, p. 34"},
                    {"type": "subheading", "text": "Posterior blepharitis"},
                    {"type": "list", "items": [
                        "Caused by <strong>meibomian gland dysfunction</strong> and "
                        "alterations in meibomian gland secretions.",
                        "<strong>Bacterial lipases</strong> may result in the formation of "
                        "<strong>free fatty acids</strong>. This <strong>increases the "
                        "melting point of the meibum</strong>, preventing its expression "
                        "from the glands, contributing to ocular surface irritation and "
                        "possibly enabling growth of <em>S. aureus</em>.",
                        "<strong>Loss of the tear film phospholipids that act as "
                        "surfactants results in increased tear evaporation and osmolarity, "
                        "and an unstable tear film.</strong>",
                        "Commonly a <strong>more persistent and chronic</strong> "
                        "inflammatory condition than anterior blepharitis; associated with "
                        "<strong>acne rosacea</strong>.",
                    ], "source": "Kanski 8e, p. 34"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Why warm compresses work — the mechanism, not the ritual",
                     "text":
                        "Free fatty acids raise the melting point of meibum so it will not "
                        "flow. Heat lowers the viscosity back to where expression is "
                        "possible. That is the whole rationale, and it tells you the "
                        "compress must be genuinely warm and held long enough to heat the "
                        "gland — not a brief wipe with a tepid flannel."},
                ],
            },
            {
                "heading": "3. The Demodex question",
                "blocks": [
                    {"type": "prose", "text":
                        "A reaction to the hair follicle and sebaceous gland-dwelling mite "
                        "<strong>Demodex</strong> may play a causative role in some patients "
                        "— <strong>D. folliculorum longus in anterior blepharitis</strong> "
                        "and <strong>D. folliculorum brevis in posterior blepharitis</strong>. "
                        "Kanski is careful: the mite <strong>can be found normally in a "
                        "majority of older patients, most of whom do not develop symptomatic "
                        "blepharitis</strong>. Overpopulation or hypersensitivity may lead "
                        "to symptoms.",
                     "cite": KANSKI.format(34)},
                    {"type": "callout",
                     "title": "Finding the mite is not finding the cause",
                     "text":
                        "Most older patients carry Demodex without symptoms. Cylindrical "
                        "collarettes at the lash base are the suggestive sign; the mere "
                        "presence of mites is not."},
                ],
            },
            {
                "heading": "4. The comparison table — learn this one",
                "blocks": [
                    {"type": "table",
                     "headers": ["Feature", "Staphylococcal (anterior)",
                                 "Seborrhoeic (anterior)", "Posterior (MGD)"],
                     "rows": [
                         ["Lash deposit", "Hard", "Soft", "—"],
                         ["Lash loss", "++", "+", "—"],
                         ["Distorted lashes / trichiasis", "++", "+", "—"],
                         ["Lid margin ulceration", "+", "—", "—"],
                         ["Lid margin notching", "+", "—", "++"],
                         ["Cyst", "Hordeolum ++", "—", "Meibomian ++"],
                         ["Conjunctival phlyctenule", "+", "—", "—"],
                         ["Tear film foaming", "—", "—", "++"],
                         ["Dry eye", "+", "+", "++"],
                         ["Corneal punctate erosions", "+", "+", "++"],
                         ["Corneal vascularisation", "+", "+", "++"],
                         ["Corneal infiltrates", "+", "+", "++"],
                         ["Associated skin disease", "Atopic dermatitis",
                          "Seborrhoeic dermatitis", "Acne rosacea"],
                     ],
                     "source": "Kanski 8e, Table 1.4, p. 34"},
                ],
            },
            {
                "heading": "5. Symptoms and signs",
                "blocks": [
                    {"type": "prose", "text":
                        "Involvement is <strong>usually bilateral and symmetrical</strong>. "
                        "Symptoms are caused by disruption of normal ocular surface function "
                        "and reduction in tear stability, and are similar in all forms, "
                        "though <strong>stinging may be more common in posterior "
                        "disease</strong>. <strong>Burning, grittiness, mild photophobia, "
                        "and crusting and redness of the lid margins with remissions and "
                        "exacerbations are characteristic.</strong>",
                     "cite": KANSKI.format(34)},
                    {"type": "callout",
                     "title": "The timing clue",
                     "text":
                        "Symptoms are <strong>usually worse in the mornings</strong>, "
                        "although <strong>in patients with associated dry eye they may "
                        "increase during the day</strong>. A patient who is worst on waking "
                        "points to blepharitis; one who deteriorates through the day points "
                        "to a dry eye component. <span class=\"cite\">Kanski 8e, pp. 34–35</span>"},
                    {"type": "subheading", "text": "Signs — staphylococcal"},
                    {"type": "list", "items": [
                        "<strong>Hard scales and crusting</strong> mainly located around the "
                        "bases of the lashes; <strong>collarettes</strong> are cylindrical "
                        "collections around lash bases.",
                        "Mild <strong>papillary conjunctivitis</strong> and chronic "
                        "conjunctival hyperaemia are common.",
                        "Long-standing cases may develop scarring and notching "
                        "(<strong>tylosis</strong>) of the lid margin, "
                        "<strong>madarosis, trichiasis and poliosis</strong>.",
                        "Associated <strong>tear film instability and dry eye</strong>.",
                    ], "source": "Kanski 8e, p. 35"},
                    {"type": "subheading", "text": "Signs — posterior (meibomian gland disease)"},
                    {"type": "list", "items": [
                        "<strong>Excessive and abnormal meibomian gland secretion</strong>, "
                        "manifesting as <strong>capping of meibomian gland orifices with oil "
                        "globules</strong>.",
                        "<strong>Pouting, recession, or plugging</strong> of meibomian gland "
                        "orifices.",
                        "<strong>Hyperaemia and telangiectasis</strong> of the posterior lid "
                        "margin.",
                        "<strong>Pressure on the lid margin results in expression of "
                        "meibomian fluid that may be turbid or toothpaste-like</strong>; in "
                        "severe cases secretions become so <strong>inspissated</strong> that "
                        "expression is impossible.",
                    ], "source": "Kanski 8e, p. 35"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Express the glands — it is a two-second test",
                     "text":
                        "Gentle pressure on the lid margin with a cotton bud or your "
                        "fingertip against the globe tells you the grade immediately: clear "
                        "oil is normal, turbid or toothpaste-like is MGD, nothing at all is "
                        "severe inspissation. Record what came out, not just that the "
                        "margins looked red."},
                ],
            },
            {
                "heading": "6. Related lid infections",
                "blocks": [
                    {"type": "subheading", "text": "Childhood blepharokeratoconjunctivitis"},
                    {"type": "prose", "text":
                        "A poorly defined condition that <strong>tends to be more severe in "
                        "Asian and Middle Eastern populations</strong> — directly relevant "
                        "to practice in Saudi Arabia. Presentation is usually at about "
                        "<strong>6 years of age</strong> with recurrent episodes of anterior "
                        "or posterior blepharitis, sometimes with recurrent styes or "
                        "chalazia. <strong>Constant eye rubbing and photophobia may lead to "
                        "misdiagnosis as allergic eye disease.</strong>",
                     "cite": KANSKI.format(38)},
                    {"type": "list", "intro": "Findings and management:", "items": [
                        "Conjunctival changes: diffuse hyperaemia, bulbar phlyctens, "
                        "follicular or papillary hyperplasia.",
                        "Corneal changes: superficial punctate keratopathy, marginal "
                        "keratitis, peripheral vascularisation, axial subepithelial haze.",
                        "Treatment is with <strong>lid hygiene and topical antibiotic "
                        "ointment at bedtime</strong>. Topical low-dose steroids "
                        "(prednisolone 0.1% or fluorometholone 0.1%) and erythromycin syrup "
                        "125 mg daily for 4–6 weeks may also be used.",
                    ], "source": "Kanski 8e, p. 38"},
                    {"type": "callout", "variant": "clinical",
                     "title": "A child with itchy eyes in this region",
                     "text":
                        "Kanski names this as more severe in Middle Eastern populations and "
                        "warns it is <em>misdiagnosed as allergy</em>. A six-year-old rubbing "
                        "their eyes with photophobia deserves a lid margin examination before "
                        "an antihistamine."},
                    {"type": "subheading", "text": "Tick infestation of the eyelid"},
                    {"type": "prose", "text":
                        "Ticks can attach to the eyelid and should be removed at the earliest "
                        "opportunity to minimise the risk of a tick-borne zoonosis such as "
                        "<strong>Lyme disease</strong>. It is <strong>critical that the tick "
                        "is detached as close to its skin attachment as possible</strong> in "
                        "order to remove its head and mouthparts. Lyme disease transmission "
                        "is thought to require attachment of the tick for "
                        "<strong>at least 36 hours</strong>.",
                     "cite": KANSKI.format(38)},
                ],
            },
        ],
        "check": [
            "Why does Kanski describe blepharitis management as difficult?",
            "Explain the free fatty acid mechanism in posterior blepharitis, and how it justifies warm compresses.",
            "Which form is associated with atopic dermatitis, and which with acne rosacea?",
            "A patient is worst on waking. Another is worst by evening. What does each suggest?",
            "Describe what you expect on expressing a normal gland, an MGD gland, and a severely affected gland.",
            "Why is finding Demodex not the same as finding the cause?",
            "Which lid condition is more severe in Middle Eastern children, and what is it commonly mistaken for?",
        ],
        "sources": [
            KANSKI_FULL + " — Chronic blepharitis, classification and mechanisms p. 34; "
            "Table 1.4 comparison p. 34; symptoms and signs pp. 34–35; childhood "
            "blepharokeratoconjunctivitis and tick infestation p. 38.",
        ],
    },

    {
        "slug": "05-conjunctival-and-allergic-disease",
        "title": "Conjunctival Diseases and Allergic Conjunctivitis",
        "hours": 3,
        "summary": (
            "Conjunctival anatomy and its immune tissue, the symptom that identifies "
            "allergy, and the papillae-versus-follicles distinction that sorts most "
            "red eyes at the slit lamp."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services.</strong> Differentiating "
            "the causes of a red eye and recognising which need referral is core "
            "diploma work; topical anti-allergy therapy depends on national scope."
        ),
        "sections": [
            {
                "heading": "1. Anatomy — three parts, one membrane",
                "blocks": [
                    {"type": "prose", "text":
                        "The conjunctiva is a <strong>transparent mucous membrane</strong> "
                        "that lines the inner surface of the eyelids and the anterior "
                        "surface of the globe, <strong>terminating at the corneoscleral "
                        "limbus</strong>. It is <strong>richly vascular</strong>, supplied "
                        "by the <strong>anterior ciliary and palpebral arteries</strong>. "
                        "There is a dense lymphatic network draining to the "
                        "<strong>preauricular and submandibular nodes</strong>. It has a key "
                        "protective role, mediating both passive and active immunity.",
                     "cite": KANSKI.format(132)},
                    {"type": "list", "intro": "Anatomically it divides into:", "items": [
                        "<strong>Palpebral conjunctiva</strong> — starts at the "
                        "mucocutaneous junction of the lid margins and is <strong>firmly "
                        "attached to the posterior tarsal plates</strong>. The tarsal blood "
                        "vessels are <strong>vertically orientated</strong>.",
                        "<strong>Forniceal conjunctiva</strong> — <strong>loose and "
                        "redundant</strong>.",
                        "<strong>Bulbar conjunctiva</strong> — covers the anterior sclera.",
                    ], "source": "Kanski 8e, p. 132"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Why you palpate the preauricular node",
                     "text":
                        "Conjunctival lymphatics drain to the preauricular and submandibular "
                        "nodes. A palpable, tender preauricular node in a red eye is a "
                        "strong pointer to <strong>viral</strong> conjunctivitis. It costs "
                        "five seconds and is one of the most discriminating signs available "
                        "to you."},
                ],
            },
            {
                "heading": "2. CALT — the conjunctiva's immune tissue",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>Conjunctiva-associated lymphoid tissue (CALT)</strong> is "
                        "<strong>critical in the initiation and regulation of ocular surface "
                        "immune responses</strong>. It consists of lymphocytes within the "
                        "epithelial layers, lymphatics and associated blood vessels, with a "
                        "stromal component of lymphocytes and plasma cells, "
                        "<strong>including follicular aggregates</strong>.",
                     "cite": KANSKI.format(132)},
                    {"type": "callout",
                     "title": "This explains follicles",
                     "text":
                        "Follicles are visible CALT. When the conjunctiva mounts a "
                        "lymphoid response — viral or chlamydial infection — those "
                        "aggregates enlarge and become the pale, avascular-centred bumps you "
                        "see in the fornix. Knowing what they <em>are</em> is what makes the "
                        "papillae/follicle distinction memorable rather than arbitrary."},
                ],
            },
            {
                "heading": "3. Symptoms — and the one that matters",
                "blocks": [
                    {"type": "prose", "text":
                        "Non-specific symptoms include <strong>lacrimation, grittiness, "
                        "stinging and burning</strong>. Two findings carry far more weight:",
                     "cite": KANSKI.format(132)},
                    {"type": "list", "items": [
                        "<strong>Itching is the hallmark of allergic disease</strong>, "
                        "although it may also occur to a lesser extent in blepharitis and "
                        "dry eye.",
                        "<strong>Significant pain, photophobia or a marked foreign body "
                        "sensation suggest corneal involvement</strong> — which moves the "
                        "problem out of the conjunctiva chapter entirely.",
                    ], "source": "Kanski 8e, p. 132"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Ask one question first",
                     "text":
                        "\"Does it itch, or does it hurt?\" Itch sends you toward allergy. "
                        "Pain with photophobia sends you to the cornea and raises the "
                        "urgency. Almost no other single question separates red eyes so "
                        "efficiently."},
                ],
            },
            {
                "heading": "4. Papillae versus follicles",
                "blocks": [
                    {"type": "table",
                     "headers": ["", "Papillae", "Follicles"],
                     "rows": [
                         ["Vascular pattern", "<strong>Vessel at the centre</strong>, "
                          "branching outward", "<strong>Vessels around the periphery</strong>, "
                          "pale avascular centre"],
                         ["Underlying tissue", "Vascular/inflammatory hyperplasia",
                          "<strong>Lymphoid aggregates (CALT)</strong>"],
                         ["Typical causes", "Allergic disease, bacterial infection, "
                          "chronic irritation, contact lens wear",
                          "Viral infection, chlamydial infection, drug toxicity"],
                         ["Best seen", "Upper tarsal conjunctiva (evert the lid)",
                          "Lower fornix and tarsal conjunctiva"],
                     ],
                     "source": "Conjunctival inflammation signs, Kanski 8e Chapter 5"},
                    {"type": "callout",
                     "title": "You must evert the lid",
                     "text":
                        "Giant papillae in vernal disease and contact lens papillary "
                        "conjunctivitis live on the <em>upper</em> tarsal conjunctiva. If "
                        "you do not evert, you do not see them, and you will attribute the "
                        "patient's lens intolerance to something else."},
                ],
            },
            {
                "heading": "5. Allergic conjunctivitis in practice",
                "blocks": [
                    {"type": "list", "intro":
                        "The allergic group is united by itch and by papillae, and "
                        "separated by severity and corneal involvement:",
                     "items": [
                        "<strong>Seasonal and perennial allergic conjunctivitis</strong> — "
                        "itch, watering, mild papillae. No corneal threat.",
                        "<strong>Vernal keratoconjunctivitis</strong> — young patients, "
                        "often male, <strong>giant papillae</strong> on the upper tarsus, "
                        "limbal Horner–Trantas dots, and a real risk of <strong>shield "
                        "ulcer</strong>. Corneal involvement makes this sight-threatening.",
                        "<strong>Atopic keratoconjunctivitis</strong> — older patients with "
                        "atopic dermatitis; chronic, scarring, corneal involvement common.",
                        "<strong>Contact lens papillary conjunctivitis</strong> — papillae "
                        "from mechanical and immunological response to the lens or its "
                        "deposits. Managed by changing lens, modality or care system.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The one that is not benign",
                     "text":
                        "Seasonal allergy is uncomfortable. <strong>Vernal disease with "
                        "corneal involvement is sight-threatening.</strong> A young patient "
                        "with severe itch, giant papillae and any corneal staining is a "
                        "referral, not a bottle of antihistamine."},
                ],
            },
        ],
        "check": [
            "Where does the conjunctiva terminate, and which arteries supply it?",
            "Which lymph nodes drain the conjunctiva, and why does that matter clinically?",
            "What is CALT, and which clinical sign is it responsible for?",
            "Which symptom is the hallmark of allergic disease?",
            "Distinguish a papilla from a follicle by vascular pattern and by cause.",
            "Why must the upper lid be everted in a contact lens wearer with intolerance?",
            "Which allergic condition threatens sight, and by what mechanism?",
        ],
        "sources": [
            KANSKI_FULL + " — Conjunctival anatomy, CALT and symptoms of conjunctival "
            "inflammation p. 132; signs of conjunctival inflammation, Chapter 5 (from p. 131).",
        ],
    },

    {
        "slug": "07-corneal-diseases-part-1",
        "title": "Corneal Diseases (Part 1): Structure and Bacterial Keratitis",
        "hours": 3,
        "summary": (
            "The cornea's dimensions, layers and nerve supply — then microbial "
            "keratitis, where contact lens wear is the single most important risk "
            "factor and the referral is same-day."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services</strong>, with direct "
            "relevance to <strong>Category 1</strong> contact lens practice. "
            "Recognising microbial keratitis and referring it urgently is a defining "
            "safety competency for anyone who fits lenses."
        ),
        "sections": [
            {
                "heading": "1. The cornea in numbers",
                "blocks": [
                    {"type": "prose", "text":
                        "The cornea is a complex structure which, as well as having a "
                        "protective role, is <strong>responsible for about three-quarters of "
                        "the optical power of the eye</strong>. The normal cornea is "
                        "<strong>free of blood vessels</strong>; nutrients are supplied and "
                        "metabolic products removed mainly via the <strong>aqueous humour "
                        "posteriorly and the tears anteriorly</strong>.",
                     "cite": KANSKI.format(168)},
                    {"type": "prose", "text":
                        "The cornea is the <strong>most densely innervated tissue in the "
                        "body</strong>, and conditions such as abrasions and bullous "
                        "keratopathy are associated with <strong>marked pain, photophobia "
                        "and reflex lacrimation</strong>. A subepithelial and a deeper "
                        "stromal nerve plexus are both supplied by the <strong>first "
                        "division of the trigeminal nerve</strong>.",
                     "cite": KANSKI.format(168)},
                    {"type": "prose", "text":
                        "The average corneal diameter is <strong>11.5 mm vertically and "
                        "12 mm horizontally</strong>. It is <strong>540 µm thick "
                        "centrally</strong> on average, and thicker peripherally.",
                     "cite": KANSKI.format(168)},
                    {"type": "figure", "svg": FIG_CORNEA_LAYERS,
                     "caption": "Corneal layers and dimensions. Compare with Kanski 8e "
                                "Chapter 6 (p. 168). Figures cited from the text; the "
                                "diagram is drawn for this note."},
                    {"type": "callout", "variant": "clinical",
                     "title": "Three consequences you will use every week",
                     "text":
                        "<strong>Three-quarters of the eye's power</strong> is why a small "
                        "corneal irregularity ruins vision and why topography matters. "
                        "<strong>Avascularity</strong> is why the graft survives and why new "
                        "vessels are always abnormal. <strong>Dense V1 innervation</strong> "
                        "is why corneal problems hurt out of all proportion to their size — "
                        "and why a <em>painless</em> corneal lesion should worry you, since "
                        "it implies reduced sensation."},
                ],
            },
            {
                "heading": "2. Bacterial keratitis — the risk factors",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>Contact lens wear, particularly if extended, is the most "
                        "important risk factor.</strong> Corneal epithelial compromise "
                        "secondary to <strong>hypoxia</strong> and minor trauma is thought "
                        "to be important, as is <strong>bacterial adherence to the lens "
                        "surface</strong>.",
                     "cite": KANSKI.format(175)},
                    {"type": "list", "items": [
                        "<strong>Wearers of soft lenses are at higher risk than those of "
                        "rigid gas permeable</strong> and other types.",
                        "Infection is more likely if there is poor lens hygiene, "
                        "<strong>but it can also occur even with apparently meticulous lens "
                        "care, and with daily disposable lenses</strong>.",
                        "<strong>Trauma, including refractive surgery</strong> (particularly "
                        "LASIK), has been linked to bacterial infection, including with "
                        "<strong>atypical mycobacteria</strong>.",
                    ], "source": "Kanski 8e, p. 175"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Read the second bullet again",
                     "text":
                        "Kanski explicitly says infection occurs <em>even with meticulous "
                        "care and with daily disposables</em>. Never reassure a symptomatic "
                        "lens wearer on the grounds that their hygiene is good or their "
                        "lenses are daily. The history does not exclude the diagnosis."},
                ],
            },
            {
                "heading": "3. Recognising it, and acting",
                "blocks": [
                    {"type": "list", "intro":
                        "A contact lens wearer with a red, painful eye is microbial "
                        "keratitis until proven otherwise. Look for:",
                     "items": [
                        "<strong>A white or creamy stromal infiltrate</strong>, usually with "
                        "an overlying epithelial defect that stains with fluorescein",
                        "<strong>Marked pain, photophobia and reflex lacrimation</strong> — "
                        "expected, given V1 innervation",
                        "<strong>Anterior chamber activity, possibly hypopyon</strong>",
                        "Conjunctival injection, worst circumcorneally",
                     ]},
                    {"type": "steps", "intro": "What to do, in order:", "items": [
                        "<strong>Remove the lens</strong> and do not replace it.",
                        "<strong>Do not patch</strong> the eye.",
                        "<strong>Do not start a topical steroid.</strong>",
                        "Retain the lens, case and solutions — they may be cultured.",
                        "<strong>Refer the same day</strong> for scraping and intensive "
                        "topical antibiotics.",
                    ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The distinction that decides urgency",
                     "text":
                        "A <strong>sterile peripheral infiltrate</strong> in a lens wearer "
                        "is typically small, peripheral, multiple, with an intact or minimally "
                        "stained epithelium and little pain. <strong>Microbial keratitis</strong> "
                        "is typically single, larger, more central, with a definite epithelial "
                        "defect, significant pain and anterior chamber activity. If you cannot "
                        "confidently place it in the first group, treat it as the second."},
                ],
            },
            {
                "heading": "4. Other management options Kanski lists",
                "blocks": [
                    {"type": "list", "intro":
                        "For persistent epithelial defects and threatened perforation, the "
                        "options in the surrounding text are worth knowing so your referral "
                        "letter is informed:",
                     "items": [
                        "<strong>Temporary or permanent lateral tarsorrhaphy or medial "
                        "canthoplasty</strong>, and occasionally central tarsorrhaphy.",
                        "<strong>Conjunctival (Gundersen) flap</strong> — protects and tends "
                        "to heal a corneal epithelial defect; particularly suitable for "
                        "chronic unilateral disease with poor visual prognosis. Buccal "
                        "mucous membrane is an alternative.",
                        "<strong>Amniotic membrane patch grafting</strong> for persistent "
                        "unresponsive epithelial defects.",
                        "<strong>Tissue adhesive (cyanoacrylate glue)</strong> to seal small "
                        "perforations.",
                     ], "source": "Kanski 8e, p. 175"},
                ],
            },
        ],
        "check": [
            "What proportion of the eye's optical power does the cornea provide?",
            "Give the corneal diameters and average central thickness.",
            "Which nerve supplies the cornea, and what are the clinical consequences?",
            "Why should a painless corneal lesion concern you?",
            "What is the most important risk factor for bacterial keratitis?",
            "Are soft or rigid lens wearers at higher risk, and why?",
            "A daily disposable wearer with good hygiene has a painful red eye. Does the history reassure you?",
            "List the five immediate actions on suspecting microbial keratitis.",
        ],
        "sources": [
            KANSKI_FULL + " — Corneal anatomy, physiology, innervation and dimensions "
            "p. 168; bacterial keratitis risk factors and surgical options p. 175.",
        ],
    },

    {
        "slug": "09-lens-diseases",
        "title": "Lens Diseases: Cataract Types and Assessment",
        "hours": 3,
        "summary": (
            "The three morphological types of age-related cataract, the refractive "
            "shift each produces, how to see them at the slit lamp, and why posterior "
            "subcapsular cataract wrecks vision out of proportion to its size."
        ),
        "wco": (
            "<strong>Category 2 and 3.</strong> Grading lens opacity, explaining the "
            "symptoms it produces and timing referral for surgery are core diploma "
            "competencies, as is recognising the refractive shift that precedes it."
        ),
        "sections": [
            {
                "heading": "1. Nuclear sclerotic cataract",
                "blocks": [
                    {"type": "prose", "text":
                        "Nuclear cataract is <strong>an exaggeration of normal ageing "
                        "change</strong>. It is <strong>often associated with myopia due to "
                        "an increase in the refractive index of the nucleus</strong>, "
                        "resulting in <strong>some elderly patients being able to read "
                        "without spectacles again — the 'second sight of the aged'</strong>. "
                        "In contrast, in the healthy ageing eye, and in occasional cases of "
                        "cortical and subcapsular cataract, there is a <strong>mild "
                        "hypermetropic shift</strong>.",
                     "cite": KANSKI.format(270)},
                    {"type": "prose", "text":
                        "It is characterised by a <strong>yellowish hue due to the "
                        "deposition of urochrome pigment</strong>, and is <strong>best "
                        "assessed with an oblique slit lamp beam</strong>. When advanced, "
                        "the nucleus appears <strong>brown</strong> or even "
                        "<strong>black</strong>, the latter being typical of marked "
                        "post-vitrectomy opacity.",
                     "cite": KANSKI.format(270)},
                    {"type": "callout", "variant": "clinical",
                     "title": "A myopic shift in an older patient is a finding",
                     "text":
                        "An elderly patient delighted that they can suddenly read without "
                        "glasses is describing nuclear sclerosis, not improvement. Record "
                        "the shift, examine the lens, and explain what is happening — "
                        "otherwise they will be baffled when their distance vision "
                        "deteriorates."},
                ],
            },
            {
                "heading": "2. Subcapsular cataract",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>Anterior subcapsular cataract</strong> lies directly under "
                        "the lens capsule and is associated with <strong>fibrous metaplasia "
                        "of the lens epithelium</strong>.",
                     "cite": KANSKI.format(270)},
                    {"type": "prose", "text":
                        "<strong>Posterior subcapsular opacity</strong> lies just in front of "
                        "the posterior capsule and has a <strong>granular or plaque-like "
                        "appearance on oblique slit lamp biomicroscopy</strong>, but "
                        "typically appears <strong>black and vacuolated on "
                        "retroillumination</strong>; the vacuoles are swollen migratory lens "
                        "epithelial cells (<strong>bladder or Wedl cells</strong>).",
                     "cite": KANSKI.format(270)},
                    {"type": "callout",
                     "title": "Two views of the same opacity",
                     "text":
                        "PSC looks granular on a direct oblique beam and black on "
                        "retroillumination. If you only ever use one technique you will "
                        "under-grade it. Retroillumination through a dilated pupil is the "
                        "sensitive view — use it."},
                    {"type": "prose", "text":
                        "<strong>Due to its location at the nodal point of the eye, a "
                        "posterior subcapsular opacity often has a particularly profound "
                        "effect on vision.</strong> Patients are characteristically troubled "
                        "by <strong>glare, for instance from the headlights of oncoming "
                        "cars</strong>, and <strong>symptoms are increased by miosis, such "
                        "as occurs during near visual activity and in bright "
                        "sunlight</strong>.",
                     "cite": KANSKI.format(270)},
                    {"type": "callout", "variant": "clinical",
                     "title": "The complaint that does not match the acuity",
                     "text":
                        "A patient with 6/9 Snellen who cannot drive at night and struggles "
                        "to read in sunlight very likely has PSC. Because it sits at the "
                        "nodal point and worsens with miosis, the disability is real even "
                        "though the chart looks acceptable. Measure glare or test in bright "
                        "conditions rather than dismissing the symptom."},
                ],
            },
            {
                "heading": "3. Cortical cataract",
                "blocks": [
                    {"type": "prose", "text":
                        "Cortical cataract may involve the anterior, posterior or equatorial "
                        "cortex. The opacities <strong>start as clefts and vacuoles between "
                        "lens fibres due to cortical hydration</strong>. Subsequent "
                        "opacification results in typical <strong>cuneiform (wedge-shaped) "
                        "or radial spoke-like opacities</strong>, <strong>often initially in "
                        "the inferonasal quadrant</strong>. As with posterior subcapsular "
                        "opacity, <strong>glare is a common symptom</strong>.",
                     "cite": KANSKI.format(270)},
                    {"type": "callout",
                     "title": "Where to look first",
                     "text":
                        "Cortical spokes begin <strong>inferonasally</strong>. On "
                        "retroillumination, start your scan there and you will catch early "
                        "changes that a central-only look would miss."},
                ],
            },
            {
                "heading": "4. Summary table",
                "blocks": [
                    {"type": "table",
                     "headers": ["Type", "Appearance", "Best seen with", "Refractive shift",
                                 "Characteristic symptom"],
                     "rows": [
                         ["<strong>Nuclear sclerotic</strong>",
                          "Yellowish → brown/black (urochrome)",
                          "<strong>Oblique slit lamp beam</strong>",
                          "<strong>Myopic</strong> — 'second sight'",
                          "Gradual distance blur; improved near vision"],
                         ["<strong>Posterior subcapsular</strong>",
                          "Granular/plaque; black and vacuolated on retroillumination",
                          "<strong>Retroillumination</strong>",
                          "Occasionally mild hypermetropic",
                          "<strong>Glare</strong>; worse with miosis — near work, sunlight, headlights"],
                         ["<strong>Cortical</strong>",
                          "Cuneiform / radial spokes, often inferonasal first",
                          "Retroillumination",
                          "Occasionally mild hypermetropic",
                          "Glare"],
                     ],
                     "source": "Kanski 8e, p. 270"},
                ],
            },
        ],
        "check": [
            "Which cataract type causes a myopic shift, and by what mechanism?",
            "What is 'second sight of the aged' and what is actually happening?",
            "Which pigment gives nuclear cataract its colour?",
            "Why does posterior subcapsular cataract affect vision disproportionately?",
            "Name two everyday situations that worsen PSC symptoms, and explain why.",
            "What are bladder (Wedl) cells and where are they seen?",
            "In which quadrant do cortical opacities typically begin?",
            "Which slit lamp technique best shows each of the three types?",
        ],
        "sources": [
            KANSKI_FULL + " — Age-related cataract: nuclear, subcapsular and cortical "
            "morphology, refractive shifts and symptoms, p. 270 (Chapter 9, Lens, "
            "from p. 269).",
        ],
    },
]

# Dry eye was authored as a standalone page before this module existed; it is
# listed here so the course index links it, and rendered from its own file.
OCULAR_DISEASES["topics"].append({
    "slug": "06-dry-eye-disease",
    "title": "Dry Eye Disease",
    "hours": 3,
    "external": True,
})

OCULAR_DISEASES["topics"] += [
    {
        "slug": "08-corneal-diseases-part-2",
        "title": "Corneal Diseases (Part 2): Viral Keratitis and Ectasia",
        "hours": 3,
        "summary": (
            "Herpes simplex and herpes zoster at the cornea, the stain that gives "
            "the diagnosis away, the drug that must never be given blind, and "
            "keratoconus — the ectasia a diploma optometrist is most likely to "
            "detect first."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services.</strong> Recognising "
            "dendritic ulcer and withholding steroid is a safety-critical diploma "
            "competency. Keratoconus detection links directly to "
            "<strong>Category 1</strong> contact lens practice."
        ),
        "sections": [
            {
                "heading": "1. Where these sit in the book",
                "blocks": [
                    {"type": "table",
                     "headers": ["Condition", "Kanski 8e page"],
                     "rows": [
                         ["Bacterial keratitis", "p. 175"],
                         ["Fungal keratitis", "p. 180"],
                         ["<strong>Herpes simplex keratitis</strong>", "<strong>p. 183</strong>"],
                         ["<strong>Herpes zoster ophthalmicus</strong>", "<strong>p. 189</strong>"],
                         ["Interstitial keratitis", "p. 194"],
                         ["Protozoan keratitis (incl. Acanthamoeba)", "p. 197"],
                         ["Helminthic keratitis", "p. 199"],
                         ["Rosacea", "p. 201"],
                         ["Peripheral corneal ulceration / thinning", "p. 202"],
                         ["Neurotrophic keratopathy", "p. 206"],
                         ["Exposure keratopathy", "p. 207"],
                         ["<strong>Corneal ectasias</strong>", "<strong>p. 213</strong>"],
                     ],
                     "source": "Chapter 6 contents, Kanski 8e"},
                ],
            },
            {
                "heading": "2. Herpes simplex keratitis",
                "blocks": [
                    {"type": "list", "intro":
                        "The epithelial (dendritic) form is the one you must recognise "
                        "without hesitation:",
                     "items": [
                        "A <strong>branching, linear epithelial lesion with terminal "
                        "bulbs</strong> and swollen epithelial cells at the margins.",
                        "<strong>The ulcer bed stains with fluorescein; the swollen cells "
                        "at the margins stain with rose Bengal.</strong> The two stains show "
                        "different things — use both if you can.",
                        "<strong>Corneal sensation is reduced</strong>. Test it before "
                        "instilling anything, because anaesthetic destroys the test.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The single most important rule in this topic",
                     "text":
                        "<strong>Never start a topical steroid in an undiagnosed red eye "
                        "with an epithelial defect.</strong> Steroid applied to a dendritic "
                        "ulcer converts it into a geographic ulcer and can cost the eye. If "
                        "you are not certain what you are looking at, you refer — you do not "
                        "treat."},
                    {"type": "callout",
                     "title": "Test sensation first, always",
                     "text":
                        "Corneal sensation is the one test that anaesthetic, fluorescein and "
                        "even prolonged lid manipulation will degrade. A wisp of cotton wool "
                        "to the cornea before anything else takes ten seconds and can point "
                        "straight at a herpetic or neurotrophic cause."},
                    {"type": "prose", "text":
                        "For the stromal and severe forms Kanski notes that "
                        "<strong>IOP should be monitored</strong>, that "
                        "<strong>perforation — actual or impending — is managed as for "
                        "bacterial keratitis</strong>, and that <strong>therapeutic "
                        "keratoplasty</strong> is considered when medical therapy is "
                        "ineffective or following perforation.",
                     "cite": KANSKI.format(183)},
                ],
            },
            {
                "heading": "3. Herpes zoster ophthalmicus",
                "blocks": [
                    {"type": "list", "items": [
                        "Reactivation of varicella zoster in the <strong>ophthalmic division "
                        "of the trigeminal nerve (V1)</strong> — the same division that "
                        "supplies the cornea.",
                        "<strong>Hutchinson sign</strong> — vesicles on the side or tip of "
                        "the nose, indicating nasociliary branch involvement and a higher "
                        "likelihood of ocular disease.",
                        "The rash <strong>respects the midline</strong>, which distinguishes "
                        "it from most other facial rashes.",
                        "Ocular complications are wide-ranging: keratitis, uveitis, raised "
                        "IOP, scleritis and, later, <strong>post-herpetic neuralgia</strong>.",
                     ], "source": "Herpes zoster ophthalmicus, Kanski 8e from p. 189"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Check the nose",
                     "text":
                        "Hutchinson sign is free information. A patient with a V1 rash and "
                        "vesicles on the nose tip needs ocular examination urgently, because "
                        "the nasociliary nerve supplies both the nose tip and the globe."},
                ],
            },
            {
                "heading": "4. Corneal ectasia — keratoconus",
                "blocks": [
                    {"type": "list", "intro":
                        "Kanski places corneal ectasias at <strong>p. 213</strong>. "
                        "Keratoconus matters disproportionately to you because the earliest "
                        "signs appear in a refraction, not in a clinic:",
                     "items": [
                        "<strong>Progressive irregular astigmatism</strong>, often with "
                        "frequent spectacle changes and poor best-corrected acuity.",
                        "<strong>Scissoring reflex on retinoscopy</strong> — frequently the "
                        "first objective sign, and one you will see before anyone else does.",
                        "<strong>Munson sign</strong> — V-shaped indentation of the lower lid "
                        "in downgaze, a late sign.",
                        "<strong>Vogt striae</strong> — fine vertical stromal lines that "
                        "disappear on digital pressure.",
                        "<strong>Fleischer ring</strong> — iron deposition at the base of the "
                        "cone, best seen with a cobalt blue filter.",
                        "<strong>Acute hydrops</strong> — sudden painful vision loss with "
                        "corneal oedema from a break in Descemet membrane.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "Why the scissoring reflex is your sign",
                     "text":
                        "A young patient whose astigmatism keeps changing and whose "
                        "retinoscopy reflex scissors is keratoconus until topography says "
                        "otherwise. Detecting it early matters more now than it used to, "
                        "because cross-linking can halt progression — see the next section."},
                ],
            },
            {
                "heading": "5. What is happening now",
                "blocks": [
                    {"type": "prose", "text":
                        "Kanski 8e is from <strong>2016</strong>, and keratoconus management "
                        "is the clearest example in this course of a textbook being overtaken. "
                        "The signs above are unchanged; what has changed is what happens after "
                        "the diagnosis."},
                    {"type": "list", "items": [
                        "<strong>Corneal cross-linking (CXL)</strong> has moved keratoconus "
                        "from a condition that was optically managed while it progressed, to "
                        "one where progression itself can be arrested. This makes "
                        "<em>early detection</em> — your scissoring reflex — genuinely "
                        "sight-saving rather than merely diagnostic.",
                        "<strong>Scleral lenses</strong> have substantially expanded what can "
                        "be fitted before keratoplasty is considered.",
                        "<strong>Topography and tomography</strong> now detect subclinical "
                        "disease well before slit lamp signs appear, which is why a "
                        "suspicious refraction warrants imaging rather than watchful waiting.",
                     ]},
                    {"type": "callout",
                     "title": "The practical consequence",
                     "text":
                        "In 2016 a young keratoconic was refracted and reviewed. Today they "
                        "are imaged, and if progression is documented they are referred for "
                        "cross-linking. Your threshold for topography in a young patient with "
                        "changing astigmatism should be low."},
                ],
            },
        ],
        "check": [
            "Describe the appearance of a dendritic ulcer and which stain shows which component.",
            "Why must corneal sensation be tested before instilling drops?",
            "What happens if a topical steroid is applied to a dendritic ulcer?",
            "What is Hutchinson sign and why does it predict ocular involvement?",
            "List four clinical signs of keratoconus and say which you are most likely to detect first.",
            "What is acute hydrops?",
            "Why has early keratoconus detection become more important since 2016?",
        ],
        "sources": [
            KANSKI_FULL + " — Chapter 6 contents and page map; herpes simplex keratitis "
            "management p. 183; herpes zoster ophthalmicus from p. 189; corneal ectasias "
            "from p. 213.",
            "Cross-linking and scleral lens practice are noted as current practice "
            "postdating the 8th edition and are marked as such in the text.",
        ],
    },

    {
        "slug": "10-retinal-diseases",
        "title": "Retinal Diseases: PVD, Breaks and Detachment",
        "hours": 3,
        "summary": (
            "Posterior vitreous detachment — what it is, how common it is, and why "
            "it matters — then retinal breaks and the detachment that follows, with "
            "the symptoms that make this an emergency referral."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services.</strong> Recognising "
            "the symptoms of PVD and retinal detachment, and referring with correct "
            "urgency, is among the highest-stakes decisions a diploma optometrist "
            "makes."
        ),
        "sections": [
            {
                "heading": "1. Posterior vitreous detachment",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>Posterior vitreous detachment (PVD) refers to separation of "
                        "the cortical vitreous, along with the delineating posterior hyaloid "
                        "membrane (PHM), from the neurosensory retina posterior to the "
                        "vitreous base.</strong>",
                     "cite": KANSKI.format(694)},
                    {"type": "list", "intro": "The mechanism has two named stages:", "items": [
                        "<strong>Synchysis</strong> — vitreous gel liquefaction with age, "
                        "forming fluid-filled cavities.",
                        "<strong>Syneresis</strong> — subsequent condensation, with access to "
                        "the preretinal space allowed by a dehiscence in the cortical gel "
                        "and/or the posterior hyaloid membrane.",
                    ], "source": "Kanski 8e, p. 694"},
                    {"type": "prose", "text":
                        "<strong>The prevalence of PVD increases with age, and in individuals "
                        "in their 80s is likely to be at least 60%.</strong> It is typically "
                        "spontaneous, but can be induced by events such as <strong>cataract "
                        "surgery, trauma, uveitis and panretinal photocoagulation</strong>. "
                        "The time taken for a PVD to complete after initiation is believed to "
                        "be variable, but <strong>probably occurs in stages over the course "
                        "of months</strong> in many patients.",
                     "cite": KANSKI.format(694)},
                    {"type": "callout", "variant": "clinical",
                     "title": "\"In stages over months\" is the safety message",
                     "text":
                        "A PVD that looks uncomplicated today can still tear the retina next "
                        "week, because the separation is not finished. That is precisely why "
                        "every patient you send home after a PVD assessment must be told to "
                        "return immediately if symptoms change."},
                ],
            },
            {
                "heading": "2. The symptoms that matter",
                "blocks": [
                    {"type": "table",
                     "headers": ["Symptom", "What it suggests", "Urgency"],
                     "rows": [
                         ["<strong>New floaters</strong>", "PVD; possible vitreous "
                          "haemorrhage if sudden shower", "Same-day assessment"],
                         ["<strong>Flashes (photopsia)</strong>", "Vitreoretinal traction — "
                          "the retina is being pulled", "Same-day assessment"],
                         ["<strong>A shower of dark spots</strong>", "Vitreous haemorrhage, "
                          "often from a torn vessel at a break", "<strong>Urgent</strong>"],
                         ["<strong>A curtain or shadow in the field</strong>",
                          "<strong>Retinal detachment</strong>", "<strong>Emergency</strong>"],
                         ["<strong>Central vision loss</strong>",
                          "Macula-off detachment", "<strong>Emergency</strong>"],
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The macula-on / macula-off distinction",
                     "text":
                        "If central vision is still good, the macula is probably still "
                        "attached — and surgery to reattach it before the macula detaches "
                        "gives a far better visual outcome. That is why a detachment with "
                        "intact central vision is <em>more</em> urgent, not less. Say so "
                        "explicitly when you refer."},
                ],
            },
            {
                "heading": "3. Peripheral retinal findings",
                "blocks": [
                    {"type": "list", "intro":
                        "Kanski's peripheral retina section describes appearances you will "
                        "meet on dilated examination and must be able to tell apart from "
                        "pathology:",
                     "items": [
                        "<strong>White with pressure</strong> and <strong>white without "
                        "pressure</strong> — greyish-white appearance of the peripheral "
                        "retina, seen with and without scleral indentation respectively. "
                        "Note that condensed vitreous gel can be strongly attached to an "
                        "area of white without pressure.",
                        "<strong>Lattice degeneration</strong> — the most important "
                        "predisposing lesion to retinal break formation.",
                        "In myopic eyes, <strong>retinal holes developing in atrophic retina "
                        "may occasionally lead to retinal detachment</strong>. "
                        "<strong>Because of lack of contrast, small holes may be very "
                        "difficult to visualise.</strong>",
                     ], "source": "Kanski 8e, p. 694, Fig. 16.19"},
                    {"type": "callout",
                     "title": "Myopes deserve more care",
                     "text":
                        "Kanski notes small holes in atrophic myopic retina are hard to see "
                        "for lack of contrast. Combine that with the higher baseline risk in "
                        "myopia and the message is simple: dilate myopic patients, examine "
                        "the periphery properly, and take their symptoms seriously."},
                ],
            },
            {
                "heading": "4. Types of retinal detachment",
                "blocks": [
                    {"type": "table",
                     "headers": ["Type", "Mechanism", "Kanski page"],
                     "rows": [
                         ["<strong>Rhegmatogenous</strong>",
                          "Fluid passes through a retinal break into the subretinal space",
                          "p. 701"],
                         ["<strong>Tractional</strong>",
                          "Fibrovascular membranes pull the retina off — classically "
                          "proliferative diabetic retinopathy",
                          "p. 711"],
                         ["<strong>Exudative</strong>",
                          "Fluid accumulates beneath the retina without a break — "
                          "inflammation, tumour, vascular disease",
                          "p. 712"],
                     ],
                     "source": "Chapter 16 contents, Kanski 8e"},
                    {"type": "callout",
                     "title": "Rhegma- means a break",
                     "text":
                        "The word does the work. Rhegmatogenous = there is a hole. If there "
                        "is no hole, the fluid arrived another way — pulled (tractional) or "
                        "leaked (exudative) — and the cause, and the treatment, are "
                        "different."},
                ],
            },
            {
                "heading": "5. What is happening now",
                "blocks": [
                    {"type": "list", "items": [
                        "<strong>Widefield and ultra-widefield imaging</strong> now "
                        "documents peripheral pathology that previously depended entirely on "
                        "indirect ophthalmoscopy with indentation, making findings shareable "
                        "with the referral unit.",
                        "<strong>OCT</strong> resolves vitreoretinal interface anatomy "
                        "directly, so partial PVD, vitreomacular traction and macular "
                        "involvement can be confirmed rather than inferred.",
                        "Neither replaces the clinical skills above. A curtain in the field "
                        "is still an emergency referral whether or not you have imaging.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The thing technology has not changed",
                     "text":
                        "The decisive act in retinal detachment is still recognising the "
                        "symptom and moving quickly. No instrument improves on a clinician "
                        "who asks about flashes, floaters and field loss, and who acts the "
                        "same day."},
                ],
            },
        ],
        "check": [
            "Define posterior vitreous detachment precisely.",
            "Distinguish synchysis from syneresis.",
            "What is the approximate prevalence of PVD in people in their 80s?",
            "Name four events that can induce a PVD.",
            "Why does the fact that PVD completes 'in stages over months' change your advice to the patient?",
            "Why is a detachment with preserved central vision more urgent, not less?",
            "Name the three types of retinal detachment and the mechanism of each.",
            "Why are small retinal holes harder to see in myopic eyes?",
        ],
        "sources": [
            KANSKI_FULL + " — Posterior vitreous detachment, synchysis and syneresis, "
            "prevalence and inducing events p. 694; peripheral retinal appearances p. 694, "
            "Fig. 16.19; retinal breaks p. 698; rhegmatogenous p. 701, tractional p. 711 "
            "and exudative p. 712 detachment (Chapter 16 from p. 681).",
        ],
    },
]

# Keep topics in syllabus order.
OCULAR_DISEASES["topics"].sort(key=lambda t: t["slug"])


# ---------------------------------------------------------------------------
# The remaining five courses.
#
# Topic lists are transcribed from the University of Bisha course-content
# tables. Topics without a "sections" key have not been written yet and render
# as "outline only" in the course index, so the gap between the syllabus and
# the notes stays visible instead of being quietly hidden.
# ---------------------------------------------------------------------------

def outline(slug, title, hours=None):
    entry = {"slug": slug, "title": title}
    if hours:
        entry["hours"] = hours
    return entry


CONTACT_LENSES = {
    "name": "Contact Lenses",
    "slug": "contact-lenses",
    "summary": (
        "Ten topics from the first glass shells to modern soft lens optics — "
        "materials and manufacture, the tear lens that governs rigid lens power, "
        "care systems, and the complications that bring wearers back."
    ),
    "wco": (
        "<strong>Category 1 — Optical Technology Services</strong> for fitting, "
        "verification and care, with <strong>Category 3</strong> for recognising "
        "and referring the complications of lens wear."
    ),
    "grounding": (
        "Grounded in " + IACLE_FULL + " — Module 2 (Introduction), Module 3 "
        "(Fitting), Module 5 (Care and Maintenance), Module 6 (The Cornea in "
        "Contact Lens Wear) and Module 9 (Special Topics). The modules are First "
        "Edition and predate silicone hydrogels, so soft lens materials carry "
        "clearly marked current-practice notes."
    ),
    "topics": [
        outline("01-history-of-contact-lenses", "History of Contact Lenses", 1),
        outline("02-corneal-topography-and-nomenclature",
                "Corneal Topography and Contact Lens Nomenclature", 2),
        outline("03-rigid-gas-permeable-lenses",
                "Rigid Gas Permeable Lenses: Materials, Manufacturing, Care", 2),
        outline("04-optical-properties-of-rigid-lenses",
                "Optical Properties of Rigid Lenses", 2),
        outline("05-complications-of-rigid-lenses",
                "Complications of Rigid Lenses", 1),
        outline("06-soft-contact-lenses",
                "Soft Contact Lenses: Materials, Manufacturing, Design, Use", 2),
        outline("07-care-of-soft-lenses", "Care of Soft Lenses", 1),
        outline("08-complications-of-soft-lenses",
                "Complications of Soft Lenses", 1),
        outline("09-complications-of-soft-lenses-continued",
                "Complications of Soft Lenses (continued)", 1),
        outline("10-optical-properties-of-soft-lenses",
                "Optical Properties of Soft Lenses", 2),
    ],
}

NEUROVISUAL_PERCEPTION = {
    "name": "Neurovisual Perception",
    "slug": "neurovisual-perception",
    "summary": (
        "How the retina and visual cortex turn light into sight — adaptation, "
        "acuity, contrast, colour and its deficiencies, spatial vision and depth."
    ),
    "wco": (
        "<strong>Category 2 — Visual Function Services.</strong> Measuring and "
        "interpreting visual function is the core of this course: acuity, contrast "
        "sensitivity and colour vision testing all sit squarely in diploma scope."
    ),
    "grounding": (
        "Grounded in " + SCHWARTZ_FULL + ", with the AAO Basic and Clinical "
        "Science Course Section 5 (Neuro-Ophthalmology) for the afferent pathway."
    ),
    "topics": [
        outline("01-retina-and-primary-visual-cortex",
                "Retina and Primary Visual Cortex", 2),
        outline("02-physiology-of-vision", "Physiology of Vision", 2),
        outline("03-light-and-dark-adaptation", "Light and Dark Adaptation", 2),
        outline("04-visual-acuity", "Visual Acuity", 2),
        outline("05-contrast-sensitivity", "Contrast Sensitivity", 2),
        outline("06-color-vision", "Colour Vision", 4),
        outline("07-color-vision-deficiencies", "Colour Vision Deficiencies", 2),
        outline("08-spatial-vision", "Spatial Vision", 2),
        outline("09-depth-perception", "Depth Perception", 2),
    ],
}

OPTICAL_INSTRUMENTATION = {
    "name": "Optical Instrumentation",
    "slug": "optical-instrumentation",
    "summary": (
        "The instruments on a clinic bench — what each one measures, the principle "
        "it works on, how to use it, and how to read what it produces."
    ),
    "wco": (
        "<strong>Category 2 and 3.</strong> Operating and interpreting diagnostic "
        "instruments is a defining diploma competency; the electrophysiology topics "
        "are interpretive rather than operational at this level."
    ),
    "grounding": (
        "Grounded in " + VOI_FULL + ", Kaschke et al. <em>Optical Devices in "
        "Ophthalmology and Optometry</em>, and the dedicated texts in the library "
        "for perimetry, ultrasound and optical coherence tomography."
    ),
    "topics": [
        outline("01-acuity-contrast-colour-instruments",
                "Visual Acuity, Contrast Sensitivity and Colour Vision Instruments", 2),
        outline("02-topography-and-retinoscopy-instruments",
                "Corneal Topography and Retinoscopy Instruments", 3),
        outline("03-visual-field-testing", "Visual Field Testing", 2),
        outline("04-ultrasound-imaging",
                "A-scan, B-scan and Ultrasound Imaging", 2),
        outline("05-electrophysiological-tests",
                "Electrophysiological Tests (VEP, ERG, EOG)", 2),
        outline("06-keratometry-instruments",
                "Contact Lens Curvature Measurement", 2),
        outline("07-lensmeter", "Lens Power Measurement (Lensmeter)", 2),
    ],
}

OPHTHALMIC_LENSES_DISPENSING = {
    "name": "Ophthalmic Lenses and Spectacle Dispensing",
    "slug": "ophthalmic-lenses-dispensing",
    "summary": (
        "From the optics of a spectacle lens to a finished, fitted pair — notation, "
        "prism and decentration, vertex distance, frames and lens mounting."
    ),
    "wco": (
        "<strong>Category 1 — Optical Technology Services.</strong> This is the "
        "course most fully inside diploma scope: every topic is something a "
        "dispensing optometrist performs directly."
    ),
    "grounding": (
        "Grounded in " + BROOKS_FULL + " — the page offset for this book was "
        "verified exact, so citations name the printed page a reader turns to."
    ),
    "topics": [
        outline("01-optics-of-ophthalmic-lenses", "Optics of Ophthalmic Lenses"),
        outline("02-spherical-lenses", "Spherical Lenses"),
        outline("03-cylindrical-lenses", "Cylindrical Lenses"),
        outline("04-contact-lenses", "Contact Lenses"),
        outline("05-lens-notations-and-symbols", "Lens Notations and Symbols"),
        outline("06-prism-and-spherical-equivalent",
                "Prism, Conical Sections and Spherical Equivalent"),
        outline("07-vertex-distance", "Vertex Distance"),
        outline("08-distance-and-near-vision", "Distance and Near Vision"),
        outline("09-prentices-rule-and-decentration",
                "Prentice's Rule and Decentration"),
        outline("10-frames-types-parts-measurements",
                "Frames: Types, Parts and Measurements"),
        outline("11-frame-design-and-lens-mounting",
                "Frame Design and Lens Mounting"),
    ],
}

VISUAL_OPTICS_BINOCULAR_VISION = {
    "name": "Visual Optics and Binocular Vision",
    "slug": "visual-optics-binocular-vision",
    "summary": (
        "The eye as an optical system, the optics of refractive error and its "
        "correction, accommodation, and how the two eyes work together — through "
        "to strabismus and fixation disparity."
    ),
    "wco": (
        "<strong>Category 2 — Visual Function Services</strong>, with "
        "<strong>Category 1</strong> for the optical correction of refractive "
        "error and prism prescribing."
    ),
    "grounding": (
        "Grounded in " + BORISH_FULL + ", Atchison &amp; Smith <em>Optics of the "
        "Human Eye</em>, " + VON_NOORDEN_FULL + " and " + EVANS_FULL + "."
    ),
    "topics": [
        outline("01-the-eye-as-an-optical-system",
                "Theoretical Optics: The Eye as an Optical System"),
        outline("02-refractive-errors-and-correction",
                "Optical Principles of Refractive Errors and Their Correction"),
        outline("03-corneal-measurement-and-topography",
                "Fundamentals of Corneal Measurement and Corneal Topography"),
        outline("04-retinal-imaging-principles",
                "Principles of Retinal Imaging and Their Application to the Eye"),
        outline("05-accommodation", "Accommodation of the Eye"),
        outline("06-binocular-vision-and-eye-movements",
                "Binocular Vision and Eye Movements"),
        outline("07-eye-movements-and-prisms",
                "Eye Movements and the Use of Prisms"),
        outline("08-accommodation-and-eye-movements",
                "Relationship Between Accommodation and Eye Movements"),
        outline("09-strabismus-and-its-types", "Strabismus and Its Types"),
        outline("10-fixation-disparity",
                "Measurement of Fixation Disparity and Eye Stability"),
    ],
}

COURSES = [
    OCULAR_DISEASES,
    CONTACT_LENSES,
    NEUROVISUAL_PERCEPTION,
    OPTICAL_INSTRUMENTATION,
    OPHTHALMIC_LENSES_DISPENSING,
    VISUAL_OPTICS_BINOCULAR_VISION,
]
