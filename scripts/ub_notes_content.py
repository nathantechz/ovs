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

# --- Contact Lenses: authored topics -------------------------------------

IACLE_M2 = "IACLE M2, p. {}"
IACLE_M5 = "IACLE M5, p. {}"
IACLE_M6 = "IACLE M6, p. {}"

FIG_CL_NOMENCLATURE = """
<svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Cross-section of a contact lens labelling back optic zone radius, back optic zone diameter, back peripheral zone, total diameter, centre thickness and edge">
  <path d="M110 120 Q 320 58 530 120" fill="none" stroke="#0066cc" stroke-width="2.5"/>
  <path d="M110 138 Q 320 82 530 138" fill="none" stroke="#0066cc" stroke-width="2.5"/>
  <line x1="110" y1="120" x2="110" y2="138" stroke="#0066cc" stroke-width="2.5"/>
  <line x1="530" y1="120" x2="530" y2="138" stroke="#0066cc" stroke-width="2.5"/>

  <line x1="110" y1="180" x2="530" y2="180" stroke="#6b7280" stroke-width="1"/>
  <line x1="110" y1="174" x2="110" y2="186" stroke="#6b7280" stroke-width="1"/>
  <line x1="530" y1="174" x2="530" y2="186" stroke="#6b7280" stroke-width="1"/>
  <text x="320" y="199" font-size="12.5" fill="#374151" text-anchor="middle">
    Total Diameter (TD, &#216;<tspan font-size="9" dy="3">T</tspan>)</text>

  <line x1="230" y1="152" x2="410" y2="152" stroke="#16a34a" stroke-width="1"/>
  <line x1="230" y1="146" x2="230" y2="158" stroke="#16a34a" stroke-width="1"/>
  <line x1="410" y1="146" x2="410" y2="158" stroke="#16a34a" stroke-width="1"/>
  <text x="320" y="171" font-size="12" fill="#15803d" text-anchor="middle">
    Back Optic Zone Diameter (BOZD, &#216;<tspan font-size="9" dy="3">0</tspan>)</text>

  <path d="M320 240 L 320 95" stroke="#dc2626" stroke-width="1" stroke-dasharray="4 3"/>
  <text x="330" y="234" font-size="12" fill="#b91c1c">BOZR (r<tspan font-size="9" dy="3">0</tspan>)</text>
  <text x="330" y="252" font-size="11" fill="#6b7280">back optic zone radius</text>

  <line x1="320" y1="72" x2="320" y2="90" stroke="#7c3aed" stroke-width="2"/>
  <text x="332" y="70" font-size="12" fill="#6d28d9">t<tspan font-size="9" dy="3">c</tspan> centre thickness</text>

  <text x="60" y="118" font-size="11.5" fill="#6b7280">edge</text>
  <text x="140" y="250" font-size="11.5" fill="#374151">Peripheral zone &#216;<tspan font-size="9" dy="3">1</tspan> (BPZD) flattens toward the edge</text>
  <text x="140" y="272" font-size="11.5" fill="#374151">F<tspan font-size="9" dy="3">v</tspan>&#8242; = Back Vertex Power (BVP) &#183; F<tspan font-size="9" dy="3">v</tspan> = Front Vertex Power</text>
</svg>
"""

FIG_TEAR_LENS = """
<svg viewBox="0 0 660 260" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Three rigid lens fitting relationships: flat with apical touch, aligned or parallel, and steep with apical clearance">
  <g>
    <text x="55" y="28" font-size="13" font-weight="bold" fill="#b45309">Flatter than K</text>
    <text x="52" y="45" font-size="11" fill="#6b7280">apical touch</text>
    <path d="M25 150 Q 100 95 175 150" fill="none" stroke="#6b7280" stroke-width="2.5"/>
    <path d="M35 142 Q 100 108 165 142" fill="none" stroke="#d97706" stroke-width="2.5"/>
    <text x="45" y="185" font-size="11.5" fill="#b45309">tear lens MINUS</text>
  </g>
  <g transform="translate(240,0)">
    <text x="48" y="28" font-size="13" font-weight="bold" fill="#15803d">Aligned</text>
    <text x="40" y="45" font-size="11" fill="#6b7280">parallel / on K</text>
    <path d="M25 150 Q 100 95 175 150" fill="none" stroke="#6b7280" stroke-width="2.5"/>
    <path d="M30 145 Q 100 92 170 145" fill="none" stroke="#16a34a" stroke-width="2.5"/>
    <text x="42" y="185" font-size="11.5" fill="#15803d">tear lens PLANO</text>
  </g>
  <g transform="translate(470,0)">
    <text x="42" y="28" font-size="13" font-weight="bold" fill="#1d4ed8">Steeper than K</text>
    <text x="40" y="45" font-size="11" fill="#6b7280">apical clearance</text>
    <path d="M25 150 Q 100 95 175 150" fill="none" stroke="#6b7280" stroke-width="2.5"/>
    <path d="M28 148 Q 100 78 172 148" fill="none" stroke="#2563eb" stroke-width="2.5"/>
    <text x="40" y="185" font-size="11.5" fill="#1d4ed8">tear lens PLUS</text>
  </g>
  <text x="30" y="225" font-size="12" fill="#374151">Grey = cornea &#183; coloured = rigid lens back surface. The gap between them is the tear lens.</text>
  <text x="30" y="245" font-size="12" fill="#374151">A soft lens drapes over the cornea, so its tear lens is thin and has no power.</text>
</svg>
"""

CONTACT_LENSES["topics"] = [
    {
        "slug": "01-history-of-contact-lenses",
        "title": "History of Contact Lenses",
        "hours": 1,
        "summary": (
            "From a sketch in 1508 to the hydrogel that made lenses a mass product — "
            "the people, the dates and, more usefully, the problems each step was "
            "trying to solve."
        ),
        "wco": (
            "<strong>Category 1 — Optical Technology Services.</strong> Context "
            "rather than competency, but the failures in this timeline are the "
            "reason modern fitting rules exist."
        ),
        "sections": [
            {
                "heading": "1. The idea before the object",
                "blocks": [
                    {"type": "prose", "text":
                        "Despite early understanding of the eye and the development of "
                        "ophthalmic optics, <strong>the concept of a correcting lens on the "
                        "eye did not emerge until Herschel's 'Dissertation on Light' was "
                        "published in 1845</strong>.",
                     "cite": IACLE_M2.format(5)},
                    {"type": "prose", "text":
                        "<strong>Leonardo da Vinci (1508)</strong> is often claimed to be "
                        "the first to describe a 'contact' lens. His sketches of a schematic "
                        "eye and of a head immersed in water have been used to illustrate a "
                        "refractive system in contact with the eye. The original manuscript "
                        "(Manuscript D, held at the Bibliothèque Mazarine) describes "
                        "<strong>the neutralisation of the cornea by water</strong> and the "
                        "mechanism of image formation at the optic nerve.",
                     "cite": IACLE_M2.format(5)},
                    {"type": "callout",
                     "title": "Read the claim carefully",
                     "text":
                        "IACLE does not say da Vinci invented the contact lens — it says he "
                        "is <em>often claimed</em> to have described one, and that his "
                        "sketches <em>have been used</em> to illustrate the concept. He "
                        "described neutralising the cornea with water. That is the honest "
                        "version, and it is the one to give in an exam."},
                ],
            },
            {
                "heading": "2. The glass era",
                "blocks": [
                    {"type": "table",
                     "headers": ["Year", "Who", "What"],
                     "rows": [
                         ["1887", "Müller brothers", "Protective shell of clear blown glass for a patient with lid disease"],
                         ["1888", "<strong>Adolf Fick</strong>", "Published his work using glass shells on <strong>rabbit corneas</strong>"],
                         ["1888", "<strong>Eugène Kalt</strong>", "Used glass shells on patients with <strong>keratoconus</strong>"],
                         ["1889", "<strong>August Müller</strong>", "Experimented on his own eyes (a <strong>−14 D myope</strong>) and described the effects of corneal oedema"],
                         ["1892", "D. E. Sulzer", "Reported the use of lathe-cut glass lenses"],
                         ["1892", "Henry Dor", "Suggested replacing the post-lens glucose solution with <strong>normal saline</strong>"],
                         ["1896", "Thomas Lohnstein", "Produced 'water spectacles' — the Hydrodiascope"],
                         ["1896", "Adolf Fick", "Lost interest in contact lenses following Elschnig's critical commentary"],
                     ],
                     "source": "IACLE M2, p. 30"},
                    {"type": "prose", "text":
                        "August Müller's account is the one worth remembering. He compared "
                        "spectacles with contact lenses which almost totally corrected his "
                        "14 D of myopia, and <strong>described the effects of corneal oedema "
                        "including progressive veiling of objects and coloured haloes around "
                        "lights</strong>. He attempted to improve lacrimal circulation by a "
                        "<strong>lens edge lift at the limbus</strong>.",
                     "cite": IACLE_M2.format(12)},
                    {"type": "callout", "variant": "clinical",
                     "title": "The first oedema symptoms ever recorded are the ones you still ask about",
                     "text":
                        "Veiling of vision and coloured haloes around lights, described in "
                        "1889 by a man wearing glass on his own eyes. When you ask a lens "
                        "wearer about haloes you are asking August Müller's question, and "
                        "his instinct — lift the edge to improve tear exchange — is still "
                        "the principle behind peripheral curves."},
                ],
            },
            {
                "heading": "3. PMMA and the corneal lens",
                "blocks": [
                    {"type": "table",
                     "headers": ["Year", "Development"],
                     "rows": [
                         ["1946", "About <strong>50,000 pairs</strong> sold in the USA; improvement in PMMA chemistry after wartime fitting of service personnel"],
                         ["1948", "<strong>Kevin Tuohy</strong> developed large-diameter (<strong>11.5–12.5 mm</strong>) corneal PMMA lenses, fitted <strong>much flatter than K</strong>. Rapid exodus from scleral PMMA lenses"],
                         ["1949", "About <strong>200,000 pairs</strong> sold in the USA"],
                         ["1950", "Tuohy's patent for corneal lenses granted"],
                         ["1950", "<strong>George Butterfield</strong> proposed fitting the corneal lens <strong>'on K'</strong> and patented the first <strong>multicurve</strong> design"],
                         ["1950s", "Increased publication on the relationship of contact lens wear to corneal physiology"],
                         ["1953", "'Micro lenses' introduced by Söhnges, Neill and Dickinson — <strong>9.5 mm</strong> diameter, fitted flatter than K"],
                     ],
                     "source": "IACLE M2, p. 31"},
                    {"type": "callout",
                     "title": "Two years, two philosophies",
                     "text":
                        "Tuohy fitted <em>much flatter than K</em> in 1948; Butterfield "
                        "proposed <em>on K</em> in 1950 and invented the multicurve to make "
                        "it work. The argument about how closely a rigid lens should follow "
                        "the cornea starts here, and the answer — align centrally, flatten "
                        "peripherally — is still what you do today."},
                ],
            },
            {
                "heading": "4. The hydrogel",
                "blocks": [
                    {"type": "prose", "text":
                        "In 1954 <strong>Professor Otto Wichterle and Dr Drahoslav Lim</strong> "
                        "of the Institute of Macromolecular Chemistry of the Czechoslovak "
                        "Academy of Sciences in Prague suggested that a plastic which more "
                        "closely simulated living tissue would be more suitable for orbital "
                        "implants than the metallic elements then being considered.",
                     "cite": IACLE_M2.format(21)},
                    {"type": "prose", "text":
                        "They discovered a stable transparent gel, "
                        "<strong>poly-hydroxyethyl-methacrylate (PHEMA)</strong>, a "
                        "water-absorbing polymer (<strong>38.6%</strong> water), "
                        "<strong>permeable to nutrients and metabolites</strong>.",
                     "cite": IACLE_M2.format(21)},
                    {"type": "callout", "variant": "clinical",
                     "title": "Why 38.6% matters",
                     "text":
                        "PHEMA's water content is the number every later soft material is "
                        "compared against. Water was how early hydrogels carried oxygen, so "
                        "water content became shorthand for physiological performance — a "
                        "shorthand that only broke down when silicone hydrogels arrived and "
                        "decoupled the two. Learn the number and you understand why the "
                        "industry talked about water for forty years."},
                ],
            },
            {
                "heading": "5. What is happening now",
                "blocks": [
                    {"type": "prose", "text":
                        "The IACLE modules are <strong>First Edition</strong> and their "
                        "timeline effectively ends before the material that now dominates "
                        "soft lens fitting. Treat what follows as signposting beyond the "
                        "textbook."},
                    {"type": "list", "items": [
                        "<strong>Silicone hydrogels</strong> broke the link between water "
                        "content and oxygen transmissibility, raising Dk/t far beyond what "
                        "PHEMA-based materials could reach and making extended wear "
                        "physiologically plausible.",
                        "<strong>Daily disposables</strong> moved the main safety lever from "
                        "disinfection compliance to simply not reusing the lens.",
                        "<strong>Myopia control</strong> lenses — orthokeratology and "
                        "dual-focus soft designs — have given contact lenses a therapeutic "
                        "purpose beyond refractive correction.",
                        "<strong>Scleral lenses</strong> have returned, now in gas-permeable "
                        "materials, for irregular corneas and ocular surface disease. The "
                        "shape Fick and Kalt used in 1888 is current practice again.",
                    ]},
                ],
            },
        ],
        "check": [
            "What did Herschel contribute, and in what year?",
            "State precisely what da Vinci described — and what he did not.",
            "Who first used glass shells on patients with keratoconus, and in what year?",
            "What symptoms of corneal oedema did August Müller describe, and how did he try to solve the problem?",
            "Give the diameter and fitting philosophy of Tuohy's 1948 corneal lens.",
            "How did Butterfield's approach differ from Tuohy's, and what did he invent to achieve it?",
            "Name the material Wichterle and Lim discovered, its water content, and why that mattered.",
        ],
        "sources": [
            IACLE_FULL + " — Module 2, Lecture 2.1 History of Contact Lenses: "
            "Herschel and da Vinci p. 5; August Müller p. 12; Wichterle and Lim "
            "p. 21; chronology of the glass era p. 30 and the PMMA era p. 31.",
        ],
    },

    {
        "slug": "02-corneal-topography-and-nomenclature",
        "title": "Corneal Topography and Contact Lens Nomenclature",
        "hours": 2,
        "summary": (
            "The vocabulary and symbols used on every lens order and verification "
            "form — and the corneal measurements those numbers have to match."
        ),
        "wco": (
            "<strong>Category 1 — Optical Technology Services.</strong> Specifying "
            "and verifying a lens correctly is the foundation of everything else in "
            "this course."
        ),
        "sections": [
            {
                "heading": "1. The parameters, and their symbols",
                "blocks": [
                    {"type": "prose", "text":
                        "Every lens is described by the same small set of parameters. "
                        "IACLE's symbols are the ones used on order forms and in the "
                        "literature, and are worth learning exactly."},
                    {"type": "table",
                     "headers": ["Symbol", "Parameter"],
                     "rows": [
                         ["<strong>r<sub>0</sub></strong>", "Back Optic Zone Radius (BOZR)"],
                         ["<strong>&Oslash;<sub>0</sub></strong>", "Back Optic Zone Diameter (BOZD)"],
                         ["<strong>&Oslash;<sub>a0</sub></strong>", "Front Optic Zone Diameter (FOZD)"],
                         ["<strong>&Oslash;<sub>1</sub></strong>", "Back Peripheral Zone Diameter (BPZD)"],
                         ["<strong>&Oslash;<sub>T</sub></strong>", "Total Diameter (TD)"],
                         ["<strong>t<sub>c</sub></strong>", "Geometric centre thickness"],
                         ["<strong>t<sub>EA</sub> / t<sub>ER</sub></strong>", "Axial and radial edge thickness"],
                         ["<strong>F<sub>v</sub>&prime;</strong>", "Back Vertex Power (BVP)"],
                         ["<strong>F<sub>v</sub></strong>", "Front Vertex Power (FVP)"],
                     ],
                     "source": "IACLE M2, p. 162"},
                    {"type": "figure", "svg": FIG_CL_NOMENCLATURE,
                     "caption": "Lens parameters in section. Compare with the labelled "
                                "diagram in IACLE M2 p. 162."},
                    {"type": "callout", "variant": "clinical",
                     "title": "BVP, not FVP",
                     "text":
                        "A contact lens is specified and verified by its <strong>back</strong> "
                        "vertex power, because that is the surface nearest the eye and "
                        "therefore what determines the correction. A lensmeter reading taken "
                        "with the lens the wrong way round gives FVP, and for a high-powered "
                        "lens the two differ enough to matter."},
                ],
            },
            {
                "heading": "2. Design factors that change on-eye performance",
                "blocks": [
                    {"type": "list", "intro":
                        "IACLE lists the soft lens design factors, noting that "
                        "<strong>each can affect 'on-eye' performance</strong>:",
                     "items": [
                        "Geometric centre thickness (t<sub>c</sub>)",
                        "Lens diameter (total diameter, TD, &Oslash;<sub>T</sub>)",
                        "Back optic zone radius (BOZR, r<sub>0</sub>)",
                        "Back surface design",
                     ], "source": "IACLE M2, p. 162"},
                    {"type": "callout",
                     "title": "Thickness is not only about comfort",
                     "text":
                        "Centre thickness sets oxygen transmissibility, because Dk/t divides "
                        "the material's permeability by the thickness. A thicker lens in the "
                        "same material delivers less oxygen. Thickness is a physiological "
                        "parameter, not just a handling one."},
                ],
            },
            {
                "heading": "3. Corneal measurement",
                "blocks": [
                    {"type": "prose", "text":
                        "The lens has to match a cornea, so the cornea has to be measured. "
                        "IACLE's optics lecture devotes a section to <strong>Corneal Radius "
                        "of Curvature</strong>, sitting immediately before "
                        "<strong>The Tear Lens</strong> and <strong>Over-Refraction</strong> "
                        "— the order tells you how the three connect.",
                     "cite": IACLE_M2.format(104)},
                    {"type": "list", "intro": "Two approaches, with different reach:", "items": [
                        "<strong>Keratometry</strong> measures the radius of curvature of a "
                        "small central zone, typically about 3 mm, in two principal "
                        "meridians. Quick, reproducible, and the basis of first trial lens "
                        "selection.",
                        "<strong>Corneal topography</strong> maps thousands of points across "
                        "the whole cornea, showing peripheral flattening, irregularity and "
                        "asymmetry that keratometry averages away.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "Why keratometry alone was rejected in 1946",
                     "text":
                        "A 1946 patent application for a corneal lens was refused, one "
                        "ground being that <em>\"many eyes present corneal surfaces of "
                        "irregular curvature; keratometer measurements alone would not "
                        "avail.\"</em> <span class=\"cite\">IACLE M2, p. 19</span> That "
                        "objection is exactly why topography exists. Keratometry gives you "
                        "a starting lens; it does not describe the cornea."},
                ],
            },
        ],
        "check": [
            "Write the symbols for back optic zone radius, total diameter and back vertex power.",
            "Why is a contact lens specified by BVP rather than FVP?",
            "List the four soft lens design factors IACLE names.",
            "Explain why centre thickness is a physiological parameter.",
            "What does keratometry measure, and over roughly what zone?",
            "Give the 1946 objection to relying on keratometry, and say what modern instrument answers it.",
        ],
        "sources": [
            IACLE_FULL + " — Module 2: lens parameters and soft lens design factors "
            "p. 162; optics lecture contents including corneal radius of curvature, "
            "the tear lens and over-refraction p. 104; the 1946 patent objection p. 19.",
        ],
    },
]

CONTACT_LENSES["topics"] += [
    {
        "slug": "03-rigid-gas-permeable-lenses",
        "title": "Rigid Gas Permeable Lenses: Materials, Manufacturing, Care",
        "hours": 2,
        "summary": (
            "What Dk and Dk/t actually mean, how they are measured, what the "
            "high-Dk materials cost you in handling, and why RGP care is a "
            "different problem from soft lens care."
        ),
        "wco": (
            "<strong>Category 1 — Optical Technology Services.</strong> Material "
            "selection, verification and care instruction are performed directly at "
            "diploma level."
        ),
        "sections": [
            {
                "heading": "1. Oxygen permeability and transmissibility",
                "blocks": [
                    {"type": "prose", "text":
                        "These two terms are constantly confused and the distinction is "
                        "simple once stated. <strong>Dk is a property of the material</strong>. "
                        "<strong>Dk/t is a property of the lens</strong>.",
                     "cite": IACLE_M2.format(41)},
                    {"type": "equation", "text": "Dk/t  =  Material Dk &divide; t",
                     "where": "t may be t<sub>c</sub> (geometric centre thickness) or "
                              "t<sub>Local</sub>, depending on the transmissibility being calculated"},
                    {"type": "list", "items": [
                        "<strong>D</strong> = diffusion coefficient of the material",
                        "<strong>k</strong> = solubility of the gas in the material",
                        "<strong>Dk</strong> is therefore <strong>not</strong> a function of "
                        "lens thickness, shape or back vertex power",
                        "<strong>Dk/t</strong> divides that permeability by the thickness, so "
                        "it describes what a particular lens delivers",
                    ], "source": "IACLE M2, p. 41"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Why a high-Dk material can still starve a cornea",
                     "text":
                        "Order a high-Dk material in a thick, high-minus design and you have "
                        "diluted the very property you paid for. When a patient shows "
                        "hypoxic signs, ask about lens <em>thickness</em> and power, not just "
                        "the material name."},
                    {"type": "prose", "text":
                        "Transmissibility is measured instrumentally. The "
                        "<strong>coulometric</strong> technique mounts the lens in an "
                        "environment-controlled cell and feeds data to a recorder or data "
                        "logger; <strong>Dk is determined indirectly from Dk/t and thickness "
                        "measurements</strong>. The <strong>polarographic</strong> technique "
                        "is the main alternative.",
                     "cite": IACLE_M2.format(41)},
                ],
            },
            {
                "heading": "2. What high-Dk materials cost you",
                "blocks": [
                    {"type": "list", "intro":
                        "IACLE is candid about the manufacturing disadvantages of "
                        "fluorosilicone acrylates and silicone acrylates:",
                     "items": [
                        "They are <strong>more susceptible to solvent damage during "
                        "manufacture</strong>, and solvents can affect the surface.",
                        "The <strong>back optic zone radius of finished lenses has been "
                        "known to change over time</strong>, especially in high minus back "
                        "vertex powers.",
                        "<strong>The more exotic materials of high Dk are often difficult to "
                        "modify</strong>, especially in contact lens practice.",
                        "<strong>Reproducibility of lenses fabricated in these materials is "
                        "lower</strong> than that of less permeable materials.",
                     ], "source": "IACLE M2, p. 61"},
                    {"type": "callout",
                     "title": "Two practical consequences",
                     "text":
                        "First, <strong>re-verify</strong> high-Dk RGPs at aftercare — the "
                        "BOZR may not be what you ordered, particularly in high minus. "
                        "Second, do not promise in-practice modification of an exotic "
                        "high-Dk lens; the textbook says it is often not feasible."},
                ],
            },
            {
                "heading": "3. Care of rigid lenses",
                "blocks": [
                    {"type": "prose", "text":
                        "Rigid lenses are not replaced frequently, which changes the care "
                        "problem. IACLE notes that protein removers are included in the care "
                        "systems for soft lenses <strong>and some RGP lenses, that are not "
                        "replaced regularly (&gt;1 month)</strong>.",
                     "cite": IACLE_M5.format(18)},
                    {"type": "list", "intro": "The regimen has distinct steps:", "items": [
                        "<strong>Surface cleaning</strong> — removes surface debris and "
                        "loosely bound deposit at the end of each wearing period.",
                        "<strong>Rinsing</strong> — removes the cleaner itself before the "
                        "lens goes near the eye.",
                        "<strong>Disinfection</strong> — kills micro-organisms during storage.",
                        "<strong>Protein removal</strong> — periodic, for lenses kept longer "
                        "than a month. <strong>Not all protein removers are enzyme-based</strong>; "
                        "those that are are usually supplied in tablet form, chemical-based "
                        "systems as ready-to-use liquids. They are effective at loosening "
                        "tightly bound protein deposits, but <strong>cannot be expected to "
                        "remove all proteins</strong>.",
                     ], "source": "IACLE M5, p. 18"},
                    {"type": "callout", "variant": "clinical",
                     "title": "The step patients skip",
                     "text":
                        "IACLE is explicit that <strong>lenses should be cleaned and rinsed "
                        "before</strong> being placed in the container with the tablet or "
                        "solution. Patients routinely drop the tablet in with a dirty lens "
                        "and wonder why deposits persist. Say the order out loud when you "
                        "teach it: clean, rinse, then protein-remove."},
                ],
            },
        ],
        "check": [
            "Define Dk and Dk/t, and say which is a property of the lens rather than the material.",
            "What do D and k stand for?",
            "Why is Dk independent of back vertex power but Dk/t is not?",
            "Name the two techniques for measuring oxygen transmissibility.",
            "Give three manufacturing disadvantages of high-Dk materials.",
            "Which lenses need periodic protein removal, and above what replacement interval?",
            "What must be done to a lens before protein removal, and why?",
        ],
        "sources": [
            IACLE_FULL + " — Module 2: oxygen permeability and transmissibility and "
            "their measurement p. 41; manufacturing disadvantages of high-Dk materials "
            "p. 61. Module 5: protein removal p. 18.",
        ],
    },

    {
        "slug": "04-optical-properties-of-rigid-lenses",
        "title": "Optical Properties of Rigid Lenses",
        "hours": 2,
        "summary": (
            "The tear lens — the single idea that makes rigid lens power make sense. "
            "Why fitting flatter or steeper than K changes the power you must order, "
            "and what decentration does to it."
        ),
        "wco": (
            "<strong>Category 1 — Optical Technology Services.</strong> Calculating "
            "the ordered power from a trial lens and over-refraction is a core "
            "dispensing competency."
        ),
        "sections": [
            {
                "heading": "1. The tear lens exists only under a rigid lens",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>When a flexible lens is placed on the cornea, the 'tear "
                        "lens' under the contact lens is very thin. It has no dioptric power "
                        "due to the conformity of the lens to the shape of the cornea.</strong>",
                     "cite": IACLE_M2.format(135)},
                    {"type": "prose", "text":
                        "<strong>If a rigid lens is used, the 'tear lens' depends on the "
                        "relationship between the curvatures of the lens back surface and "
                        "the cornea</strong> and, to a lesser extent, the material's "
                        "rigidity.",
                     "cite": IACLE_M2.format(135)},
                    {"type": "callout", "variant": "clinical",
                     "title": "This single difference drives everything",
                     "text":
                        "A soft lens drapes, so what you order is essentially the ocular "
                        "refraction adjusted for vertex distance. A rigid lens does not "
                        "drape, so it creates a liquid lens between itself and the cornea — "
                        "and that liquid lens has power you must account for."},
                ],
            },
            {
                "heading": "2. The three fitting relationships",
                "blocks": [
                    {"type": "prose", "text":
                        "IACLE names the three simplest RGP/cornea relationships as "
                        "<strong>flatter or apical touch</strong>, <strong>alignment or "
                        "parallel</strong>, and <strong>steeper or apical clearance</strong>.",
                     "cite": IACLE_M2.format(135)},
                    {"type": "figure", "svg": FIG_TEAR_LENS,
                     "caption": "The three relationships and the tear lens each creates. "
                                "Compare IACLE M2 p. 135."},
                    {"type": "table",
                     "headers": ["Fit", "Tear lens shape", "Tear lens power", "Compensate by ordering"],
                     "rows": [
                         ["<strong>Flatter than K</strong> (apical touch)",
                          "Minus meniscus", "<strong>Minus</strong>", "<strong>More plus</strong> in the lens"],
                         ["<strong>Aligned</strong> (on K, parallel)",
                          "Parallel", "<strong>Plano</strong>", "No compensation"],
                         ["<strong>Steeper than K</strong> (apical clearance)",
                          "Plus meniscus", "<strong>Plus</strong>", "<strong>More minus</strong> in the lens"],
                     ]},
                    {"type": "callout",
                     "title": "SAM–FAP",
                     "text":
                        "<strong>S</strong>teeper <strong>A</strong>dd <strong>M</strong>inus, "
                        "<strong>F</strong>latter <strong>A</strong>dd <strong>P</strong>lus. "
                        "The mnemonic is only worth using if you can also say why: a steep "
                        "fit creates a plus tear lens, so the contact lens must carry more "
                        "minus for the total to stay correct."},
                ],
            },
            {
                "heading": "3. Decentration induces prism",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>If a rigid lens decentres, the tear lens will acquire a "
                        "prismatic component</strong> in addition to the spherical or "
                        "sphero-cylindrical optics dictated by the fitting relationship.",
                     "cite": IACLE_M2.format(135)},
                    {"type": "prose", "text":
                        "When a rigid lens decentres, and is possibly tilted by upper or "
                        "lower lid pressures, a prismatic tear lens may be induced under it. "
                        "<strong>In higher powered lenses, any induced tear prismatic effect "
                        "may be insignificant when compared with the prism induced by the "
                        "decentred optics.</strong>",
                     "cite": IACLE_M2.format(135)},
                    {"type": "callout", "variant": "clinical",
                     "title": "A patient who sees well only sometimes",
                     "text":
                        "Intermittent blur or doubling in a rigid lens wearer, worse after "
                        "blinking, points at a lens moving off centre. Two prismatic effects "
                        "are in play — the tear lens and the decentred lens optics — and in "
                        "high powers the second dominates. Assess the fit, not the "
                        "prescription."},
                ],
            },
            {
                "heading": "4. Over-refraction is how you resolve it",
                "blocks": [
                    {"type": "prose", "text":
                        "IACLE places <strong>Over-Refraction</strong> immediately after the "
                        "tear lens section, and there is a practical exercise devoted to it "
                        "(Practical 2.3, Contact Lens Over-Refraction).",
                     "cite": IACLE_M2.format(104)},
                    {"type": "steps", "intro": "The logic in order:", "items": [
                        "Place a <strong>trial lens of known BOZR and BVP</strong> on the eye "
                        "and let it settle.",
                        "Assess the <strong>fitting relationship</strong> — flat, aligned or "
                        "steep — since this tells you what the tear lens is doing.",
                        "Perform an <strong>over-refraction</strong> through the trial lens.",
                        "<strong>Ordered BVP = trial lens BVP + over-refraction</strong>, "
                        "adjusted if the final lens BOZR differs from the trial lens, because "
                        "changing BOZR changes the tear lens.",
                    ]},
                    {"type": "callout",
                     "title": "The reason over-refraction beats calculation",
                     "text":
                        "Over-refraction measures the eye <em>with the tear lens already in "
                        "place</em>. It absorbs the tear lens, vertex distance and any "
                        "flexure into one reading. Calculate only when you must change the "
                        "BOZR between trial and final lens."},
                ],
            },
        ],
        "check": [
            "Why does a soft lens have no tear-lens power?",
            "Name the three RGP fitting relationships and the tear lens power each creates.",
            "A lens fitted 0.10 mm steeper than K — should the ordered power be more plus or more minus, and why?",
            "What happens to the tear lens when a rigid lens decentres?",
            "In a high-powered lens, which prismatic effect dominates?",
            "Write the relationship between trial lens BVP, over-refraction and ordered BVP.",
            "When must you calculate rather than rely on over-refraction alone?",
        ],
        "sources": [
            IACLE_FULL + " — Module 2, Lecture 2.3 Optics and Vision of Contact "
            "Lenses: the tear lens, fitting relationships and decentration-induced "
            "prism p. 135; lecture contents listing corneal radius, tear lens and "
            "over-refraction p. 104.",
        ],
    },

    {
        "slug": "05-complications-of-rigid-lenses",
        "title": "Complications of Rigid Lenses",
        "hours": 1,
        "summary": (
            "Hypoxia and its signs, mechanical effects of a lens that does not drape, "
            "and the one complication that must never be managed in the chair."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services.</strong> Recognising "
            "and grading complications, and referring microbial keratitis the same "
            "day."
        ),
        "sections": [
            {
                "heading": "1. Oxygen is the underlying variable",
                "blocks": [
                    {"type": "prose", "text":
                        "IACLE frames the whole subject around supply and demand: a lens "
                        "should be selected which <strong>allows a level of oxygen above, "
                        "and preferably well above, the 'average' minimum required</strong>. "
                        "Considerable research has established <strong>general agreement on "
                        "the oxygen levels required for safe daily and overnight wear</strong>, "
                        "and the module notes that many lenses historically marketed were "
                        "<strong>incapable of meeting</strong> those levels, especially for "
                        "overnight extended wear.",
                     "cite": IACLE_M6.format(5)},
                    {"type": "callout",
                     "title": "The historical point that still matters",
                     "text":
                        "The textbook admits the industry sold lenses that could not meet "
                        "the published oxygen requirements. That is the context for every "
                        "hypoxic complication described below — and the reason material Dk "
                        "improved so sharply afterwards."},
                ],
            },
            {
                "heading": "2. Signs of hypoxia",
                "blocks": [
                    {"type": "list", "intro":
                        "August Müller described the symptoms in 1889 — veiling of vision "
                        "and coloured haloes around lights "
                        "<span class=\"cite\">IACLE M2, p. 12</span>. The signs you look "
                        "for:",
                     "items": [
                        "<strong>Corneal oedema</strong> — the direct consequence; striae "
                        "and folds appear as it increases.",
                        "<strong>Epithelial microcysts</strong> — a marker of chronic "
                        "metabolic stress rather than acute insult, appearing weeks into the "
                        "problem and, importantly, <em>increasing</em> transiently when the "
                        "cause is removed.",
                        "<strong>Neovascularisation</strong> — vessels growing into a tissue "
                        "that Kanski reminds us is normally <strong>free of blood "
                        "vessels</strong> <span class=\"cite\">Kanski 8e, p. 168</span>.",
                        "<strong>Reduced corneal sensitivity</strong> with chronic wear.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "Any new corneal vessel is abnormal",
                     "text":
                        "The cornea is avascular by design. A vessel crossing the limbus in "
                        "a lens wearer is the eye responding to a problem you have not yet "
                        "named. Find it before the vessel gets further."},
                ],
            },
            {
                "heading": "3. Mechanical complications",
                "blocks": [
                    {"type": "list", "intro":
                        "A rigid lens does not conform to the cornea, which creates problems "
                        "a soft lens does not:",
                     "items": [
                        "<strong>3 and 9 o'clock staining</strong> — peripheral desiccation "
                        "where the lid fails to resurface the cornea beside the lens edge.",
                        "<strong>Corneal abrasion</strong> from a foreign body trapped "
                        "beneath the lens — rigid lenses trap debris that a soft lens would "
                        "not.",
                        "<strong>Lens binding / adherence</strong>, particularly after "
                        "overnight wear.",
                        "<strong>Corneal warpage and spectacle blur</strong> — the cornea "
                        "moulds to the lens, so spectacle vision is poor immediately after "
                        "removal.",
                        "<strong>Ptosis</strong> with long-term rigid wear.",
                     ]},
                    {"type": "callout",
                     "title": "Spectacle blur is a fitting signal",
                     "text":
                        "A patient who cannot see with their glasses for hours after lens "
                        "removal has a cornea being reshaped. Recheck keratometry against "
                        "the original readings before assuming the spectacle prescription "
                        "has changed."},
                ],
            },
            {
                "heading": "4. The one that cannot wait",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>Contact lens wear, particularly if extended, is the most "
                        "important risk factor</strong> for bacterial keratitis. Corneal "
                        "epithelial compromise secondary to <strong>hypoxia</strong> and "
                        "minor trauma is thought to be important, as is bacterial adherence "
                        "to the lens surface. <strong>Wearers of soft lenses are at higher "
                        "risk than those of rigid gas permeable</strong> and other types.",
                     "cite": "Kanski 8e, p. 175"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Lower risk is not no risk",
                     "text":
                        "RGP wearers are at lower risk than soft lens wearers — but a rigid "
                        "lens wearer with a red, painful eye and an infiltrate is managed "
                        "exactly the same way: remove the lens, do not patch, do not "
                        "steroid, keep the lens and case for culture, refer the same day."},
                ],
            },
        ],
        "check": [
            "What does IACLE say about the oxygen performance of lenses historically marketed?",
            "List four signs of corneal hypoxia in a lens wearer.",
            "Why is any new corneal blood vessel abnormal?",
            "Explain the mechanism of 3 and 9 o'clock staining.",
            "A patient cannot see through their spectacles after removing RGPs. What is happening and what do you check?",
            "Are RGP or soft lens wearers at higher risk of bacterial keratitis?",
            "State the five immediate actions on finding an infiltrate in a lens wearer.",
        ],
        "sources": [
            IACLE_FULL + " — Module 6, Lecture 6.1 Corneal Oxygen Requirements and "
            "the Effects of Hypoxia p. 5; Module 2 p. 12 for Müller's description of "
            "oedema symptoms.",
            KANSKI_FULL + " — corneal avascularity p. 168; bacterial keratitis risk "
            "factors p. 175.",
        ],
    },
]

CONTACT_LENSES["topics"] += [
    {
        "slug": "06-soft-contact-lenses",
        "title": "Soft Contact Lenses: Materials, Manufacturing, Design, Use",
        "hours": 2,
        "summary": (
            "PHEMA and what followed, how hydration changes a finished lens, the "
            "design factors that alter on-eye behaviour — and an honest account of "
            "where this First Edition textbook stops."
        ),
        "wco": (
            "<strong>Category 1 — Optical Technology Services.</strong> Material and "
            "modality selection, and patient instruction, are performed directly."
        ),
        "sections": [
            {
                "heading": "1. The founding material",
                "blocks": [
                    {"type": "prose", "text":
                        "Wichterle and Lim's <strong>poly-hydroxyethyl-methacrylate "
                        "(PHEMA)</strong> is a water-absorbing polymer at "
                        "<strong>38.6% water</strong>, <strong>permeable to nutrients and "
                        "metabolites</strong>.",
                     "cite": IACLE_M2.format(21)},
                    {"type": "callout",
                     "title": "Water was the oxygen strategy",
                     "text":
                        "In a conventional hydrogel, oxygen crosses the lens dissolved in "
                        "its water. Raise the water content and you raise Dk — but you also "
                        "make the lens more fragile, more prone to dehydration and more "
                        "deposit-attracting. Every conventional soft lens is a compromise "
                        "along that one axis."},
                ],
            },
            {
                "heading": "2. Hydration changes the lens you made",
                "blocks": [
                    {"type": "prose", "text":
                        "A soft lens is manufactured dry and worn wet, and the two states "
                        "differ. IACLE's quality control notes on the wet state are "
                        "practical and specific:",
                     "cite": IACLE_M2.format(67)},
                    {"type": "list", "items": [
                        "<strong>BOZR is critical. It influences the lens fit and the optics "
                        "of the tear lens. The BOZR will be approximately 0.03 mm flatter "
                        "after hydration.</strong>",
                        "<strong>Image quality</strong> is reassessed to determine the "
                        "optical quality of the product; vision quality depends on the "
                        "prescription being accurate and the quality of the optics.",
                        "<strong>Workmanship</strong> is reassessed to confirm that hydration "
                        "has not revealed previously undetected defects. Defects may include "
                        "<strong>edge chips and surface scratches</strong>.",
                    ], "source": "IACLE M2, p. 67"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Verify wet, always",
                     "text":
                        "A lens measured dry is not the lens the patient wears — the BOZR "
                        "alone shifts about 0.03 mm flatter on hydration. Any verification "
                        "that matters is done in the hydrated state."},
                ],
            },
            {
                "heading": "3. Design factors",
                "blocks": [
                    {"type": "list", "intro":
                        "IACLE lists the soft lens design factors, each of which "
                        "<strong>can affect 'on-eye' performance</strong>:",
                     "items": [
                        "<strong>Geometric centre thickness (t<sub>c</sub>)</strong> — sets "
                        "Dk/t, handling and the degree to which the lens drapes.",
                        "<strong>Total diameter (TD, &Oslash;<sub>T</sub>)</strong> — governs "
                        "corneal coverage and limbal relationship.",
                        "<strong>Back optic zone radius (BOZR, r<sub>0</sub>)</strong> — with "
                        "diameter, determines sagittal height and therefore tightness.",
                        "<strong>Back surface design</strong>.",
                     ], "source": "IACLE M2, p. 162"},
                    {"type": "callout",
                     "title": "Judge a soft fit by sagittal height, not BOZR alone",
                     "text":
                        "BOZR and diameter act together: a lens can be made tighter by "
                        "steepening the radius <em>or</em> by increasing the diameter. When a "
                        "soft lens is too tight or too loose, either parameter is a lever."},
                ],
            },
            {
                "heading": "4. What is happening now",
                "blocks": [
                    {"type": "callout",
                     "title": "Where the textbook stops",
                     "text":
                        "The IACLE modules are <strong>First Edition</strong> and predate "
                        "silicone hydrogels. Searching the whole library for the term returns "
                        "a single passing line, in Evans on paediatric fitting "
                        "<span class=\"cite\">Evans, p. 82</span>. Everything in this section "
                        "is therefore flagged as current practice beyond the cited texts, "
                        "and none of it should be attributed to IACLE."},
                    {"type": "list", "intro":
                        "The four developments that changed soft lens practice after this "
                        "textbook:",
                     "items": [
                        "<strong>Silicone hydrogels.</strong> Oxygen travels through the "
                        "silicone phase rather than the water, breaking the water–Dk link "
                        "entirely. Dk/t rose several-fold, which is why overnight wear "
                        "became physiologically defensible. The trade-offs moved to modulus "
                        "(stiffer material, mechanical complications) and surface wettability.",
                        "<strong>Daily disposables.</strong> A lens used once removes the "
                        "storage case, the solution and the compliance problem — the three "
                        "places infection risk concentrates. Note Kanski's caution that "
                        "infection <em>can still occur</em> with daily disposables "
                        "<span class=\"cite\">Kanski 8e, p. 175</span>.",
                        "<strong>Myopia control designs.</strong> Dual-focus and "
                        "peripheral-defocus soft lenses give contact lenses a therapeutic "
                        "role in slowing axial elongation in children.",
                        "<strong>Modern scleral lenses.</strong> Gas-permeable sclerals for "
                        "irregular corneas and ocular surface disease — a return to the lens "
                        "shape Fick and Kalt used in 1888, now in materials that let the "
                        "cornea breathe.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The exam answer, and the clinic answer",
                     "text":
                        "If asked how water content relates to oxygen performance, the "
                        "textbook answer is that higher water carries more oxygen — true for "
                        "conventional hydrogels. Add that this no longer holds for silicone "
                        "hydrogels, where a <em>lower</em> water material can transmit far "
                        "more oxygen. Knowing which rule applies to which material is the "
                        "competency."},
                ],
            },
        ],
        "check": [
            "Name the founding soft lens material, its water content and who discovered it.",
            "In a conventional hydrogel, how does oxygen reach the cornea?",
            "By how much does BOZR change on hydration, and in which direction?",
            "Why must soft lens verification be done in the hydrated state?",
            "List the soft lens design factors and say which two together determine tightness.",
            "Explain why the water-content rule does not hold for silicone hydrogels.",
            "Does a daily disposable modality eliminate the risk of microbial keratitis?",
        ],
        "sources": [
            IACLE_FULL + " — Module 2: PHEMA and its discovery p. 21; wet-state "
            "quality control and the 0.03 mm hydration change p. 67; soft lens design "
            "factors p. 162.",
            KANSKI_FULL + " — infection with daily disposables p. 175.",
            "Silicone hydrogels, daily disposable modalities, myopia control designs "
            "and modern scleral lenses postdate the First Edition modules and are "
            "marked as current practice in the text.",
        ],
    },

    {
        "slug": "07-care-of-soft-lenses",
        "title": "Care of Soft Lenses",
        "hours": 1,
        "summary": (
            "What each bottle actually does, the disinfection families and how they "
            "differ, and why the care regimen depends on the replacement schedule."
        ),
        "wco": (
            "<strong>Category 1 — Optical Technology Services.</strong> Selecting a "
            "care system and teaching it is performed directly, and is the single "
            "biggest lever a diploma optometrist has on infection risk."
        ),
        "sections": [
            {
                "heading": "1. Regimen follows replacement schedule",
                "blocks": [
                    {"type": "table",
                     "headers": ["Modality", "Care required"],
                     "rows": [
                         ["<strong>Daily disposables</strong>",
                          "Because of its single use concept, this lens <strong>does not "
                          "require use of surfactant cleaner, disinfecting solution or weekly "
                          "enzyme</strong>. If needed, in-eye re-wetting drops or sterile "
                          "saline for rinsing prior to insertion"],
                         ["<strong>Regular disposables</strong> (weekly or bi-weekly)",
                          "<strong>Multi-purpose solutions given as a complete care "
                          "system</strong>. Lenses can be rinsed with aerosol saline prior to "
                          "insertion or a lubricating solution used to re-wet. "
                          "<strong>No weekly protein removal is needed</strong>"],
                         ["<strong>Lenses kept longer than a month</strong>",
                          "Add periodic <strong>protein removal</strong> — see below"],
                     ],
                     "source": "IACLE M5, p. 23 and p. 18"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Do not sell care a patient does not need",
                     "text":
                        "IACLE is explicit that daily disposables need no cleaner, no "
                        "disinfectant and no enzyme, and that regular disposables need no "
                        "weekly protein removal. Prescribing them anyway costs the patient "
                        "money and teaches them that your instructions are negotiable."},
                ],
            },
            {
                "heading": "2. The disinfection families",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>Chemical disinfection systems vary greatly and a wide "
                        "variety of types exist.</strong> Included in the chemical category "
                        "are <strong>hydrogen peroxide and multi-purpose solutions</strong>. "
                        "Chemical disinfection subdivides into <strong>oxidative (hydrogen "
                        "peroxide and chlorine)</strong> and <strong>conventional cold "
                        "chemical</strong>. IACLE adds, candidly, that "
                        "<strong>\"sometimes, the distinctions can seem confusing and "
                        "complicated to patient and practitioner alike\"</strong>.",
                     "cite": IACLE_M5.format(12)},
                    {"type": "list", "items": [
                        "<strong>Oxidative — hydrogen peroxide.</strong> Effective and "
                        "preservative-free, which suits sensitive patients. Requires "
                        "neutralisation, and an unneutralised lens causes a painful chemical "
                        "injury.",
                        "<strong>Oxidative — chlorine.</strong> The other oxidative route.",
                        "<strong>Conventional cold chemical / multi-purpose.</strong> One "
                        "bottle cleans, rinses, disinfects and stores. Convenience is the "
                        "point, and compliance is better for it — but the preservatives are "
                        "the source of the problem below.",
                        "<strong>Thermal.</strong> Historically standard; IACLE notes a "
                        "system for thermal disinfection <strong>in a domestic microwave "
                        "oven</strong> had recently been released at the time of writing.",
                     ], "source": "IACLE M5, p. 12"},
                    {"type": "callout",
                     "title": "The preservative problem, stated by the textbook",
                     "text":
                        "\"The use of strong disinfectants (many of which are also used in "
                        "lower concentrations as preservatives) in chemical-based "
                        "disinfection systems can cause problems for the patient.\" "
                        "<span class=\"cite\">IACLE M5, p. 12</span> A patient with chronic "
                        "low-grade redness and stinging on insertion may be reacting to "
                        "their solution, not their lens."},
                ],
            },
            {
                "heading": "3. Protein removal",
                "blocks": [
                    {"type": "prose", "text":
                        "Protein removers <strong>are included in the care systems for soft "
                        "contact lenses, and some RGP lenses, that are not replaced regularly "
                        "(&gt;1 month)</strong>. <strong>Not all protein removers are "
                        "enzyme-based</strong>; those that are are usually supplied in tablet "
                        "form, while chemical-based systems are supplied as ready-to-use "
                        "liquids.",
                     "cite": IACLE_M5.format(18)},
                    {"type": "prose", "text":
                        "They are <strong>effective in loosening tightly bound protein "
                        "deposits</strong>. However, they <strong>cannot be expected to "
                        "remove all proteins</strong>. <strong>Prior to protein removal, the "
                        "lenses should be cleaned and rinsed</strong> before being placed in "
                        "the recommended container with the tablet or solution.",
                     "cite": IACLE_M5.format(18)},
                ],
            },
            {
                "heading": "4. Teaching it",
                "blocks": [
                    {"type": "steps", "intro":
                        "IACLE devotes a practical to patient education (Practical 5.1, Use "
                        "and Care of Contact Lenses). The points that change outcomes:",
                     "items": [
                        "<strong>Wash and dry hands</strong> before handling — the step most "
                        "often skipped and the one that matters most.",
                        "<strong>Never rinse lenses or the case in tap water.</strong> This "
                        "is the <em>Acanthamoeba</em> route.",
                        "<strong>Discard and replace solution every time</strong>; never top "
                        "up a case that still has fluid in it.",
                        "<strong>Air-dry the case face down</strong> after rinsing, and "
                        "replace it regularly.",
                        "<strong>Do not swim or shower in lenses</strong> without advice.",
                        "<strong>Remove the lens and seek help</strong> for any red, painful "
                        "or photophobic eye — never 'wait and see'.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "One sentence worth rehearsing",
                     "text":
                        "\"If your eye is red, painful or light-sensitive, take the lens out "
                        "and contact us the same day — do not put it back in.\" Said at every "
                        "fitting and every aftercare, that sentence prevents more sight loss "
                        "than any solution you can sell."},
                ],
            },
        ],
        "check": [
            "What care does a daily disposable lens require, according to IACLE?",
            "Do regular disposables need weekly protein removal?",
            "Name the two oxidative disinfection agents.",
            "What does IACLE say about preservatives in chemical disinfection systems?",
            "Which lenses need protein removal, and what must happen to the lens first?",
            "Can protein removers remove all protein?",
            "Why must tap water never touch a lens or its case?",
        ],
        "sources": [
            IACLE_FULL + " — Module 5, Lecture 5.1 Overview of Care and Maintenance: "
            "disinfection systems and preservatives p. 12; protein removal p. 18; "
            "care by replacement schedule p. 23. Practical 5.1 covers patient "
            "education.",
        ],
    },
]

CONTACT_LENSES["topics"] += [
    {
        "slug": "08-complications-of-soft-lenses",
        "title": "Complications of Soft Lenses",
        "hours": 1,
        "summary": (
            "The hypoxic and metabolic consequences of covering a cornea that has no "
            "blood supply — oedema, microcysts, neovascularisation — and how to grade "
            "what you see."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services.</strong> Detection, "
            "grading and the decision to modify, suspend or refer."
        ),
        "sections": [
            {
                "heading": "1. Start from the physiology",
                "blocks": [
                    {"type": "prose", "text":
                        "The cornea is <strong>free of blood vessels</strong>; nutrients are "
                        "supplied and metabolic products removed <strong>mainly via the "
                        "aqueous humour posteriorly and the tears anteriorly</strong>.",
                     "cite": "Kanski 8e, p. 168"},
                    {"type": "callout",
                     "title": "A contact lens sits on the anterior supply route",
                     "text":
                        "Every soft lens complication in this topic follows from that single "
                        "sentence. Cover the anterior surface and you interfere with the "
                        "tear-borne supply of oxygen and the removal of metabolic products. "
                        "The lens does not injure the cornea; it starves it."},
                    {"type": "prose", "text":
                        "IACLE frames fitting as meeting a demand: select a lens which "
                        "<strong>allows a level of oxygen above, and preferably well above, "
                        "the 'average' minimum required</strong>, noting general agreement on "
                        "the levels needed for <strong>safe daily and overnight wear</strong>.",
                     "cite": IACLE_M6.format(5)},
                ],
            },
            {
                "heading": "2. Corneal oedema",
                "blocks": [
                    {"type": "list", "intro":
                        "The first and most direct consequence. Graded by what appears as it "
                        "worsens:",
                     "items": [
                        "<strong>Subtle</strong> — detectable only by pachymetry; no slit "
                        "lamp sign.",
                        "<strong>Striae</strong> — fine vertical greyish-white lines in the "
                        "posterior stroma. The first visible sign, and the one to hunt for.",
                        "<strong>Folds</strong> — in Descemet membrane, indicating greater "
                        "swelling.",
                        "<strong>Gross oedema</strong> — epithelial haze and reduced vision.",
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The symptoms are still Müller's",
                     "text":
                        "<strong>Progressive veiling of objects and coloured haloes around "
                        "lights</strong> <span class=\"cite\">IACLE M2, p. 12</span>. A "
                        "patient reporting haloes at the end of the day is describing "
                        "oedema, whatever else they say. Ask when in the day it happens — "
                        "end-of-day haloes point at the lens, on-waking haloes at overnight "
                        "wear."},
                ],
            },
            {
                "heading": "3. Epithelial microcysts",
                "blocks": [
                    {"type": "list", "items": [
                        "Small, discrete, irregular inclusions in the epithelium, seen best "
                        "on <strong>marginal retroillumination</strong>, showing "
                        "<strong>reversed illumination</strong> — the optical signature that "
                        "distinguishes them from vacuoles.",
                        "A marker of <strong>chronic</strong> metabolic disturbance, not an "
                        "acute event. They take weeks of altered epithelial turnover to "
                        "appear.",
                        "<strong>Counterintuitive behaviour on treatment:</strong> when the "
                        "hypoxic stimulus is removed, microcysts transiently "
                        "<em>increase</em> before resolving, as the backlog of affected "
                        "cells moves to the surface.",
                    ]},
                    {"type": "callout",
                     "title": "A rebound is success, not failure",
                     "text":
                        "You move a patient into a higher-Dk lens and the microcyst count "
                        "goes up at the next visit. That is the expected course. Record it, "
                        "explain it, and review again rather than reversing a correct "
                        "decision."},
                ],
            },
            {
                "heading": "4. Neovascularisation",
                "blocks": [
                    {"type": "list", "items": [
                        "New vessels growing in from the limbus into a tissue that is "
                        "normally avascular.",
                        "Driven by <strong>chronic hypoxia</strong> and by inflammation.",
                        "<strong>Vessels do not regress fully</strong> once established — "
                        "they may empty and become ghost vessels, but the structural change "
                        "persists.",
                        "Significant encroachment on the visual axis threatens vision and "
                        "prejudices any future corneal graft.",
                    ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "Measure it, do not just note it",
                     "text":
                        "Record the extent in millimetres of encroachment from the limbus "
                        "and the clock hours involved. \"Some neovascularisation\" at two "
                        "consecutive visits tells you nothing; \"1.2 mm at 3 o'clock, "
                        "previously 0.8 mm\" tells you to change the lens today."},
                ],
            },
            {
                "heading": "5. Reduced corneal sensitivity",
                "blocks": [
                    {"type": "prose", "text":
                        "The cornea is the <strong>most densely innervated tissue in the "
                        "body</strong>, supplied by the <strong>first division of the "
                        "trigeminal nerve</strong>.",
                     "cite": "Kanski 8e, p. 168"},
                    {"type": "callout", "variant": "clinical",
                     "title": "Why this is the most dangerous complication",
                     "text":
                        "Chronic lens wear reduces corneal sensitivity. A cornea that cannot "
                        "feel pain does not warn its owner about an ulcer. The long-term "
                        "wearer who says \"it doesn't really hurt\" may be the one in most "
                        "trouble — never let the absence of pain reassure you in a lens "
                        "wearer with a corneal lesion."},
                ],
            },
        ],
        "check": [
            "Why does covering the cornea with a lens cause metabolic problems?",
            "Name the visible signs of corneal oedema in order of increasing severity.",
            "How are microcysts best viewed, and what optical sign identifies them?",
            "Why do microcysts increase after you improve a patient's oxygen supply?",
            "Do corneal new vessels regress completely when the cause is removed?",
            "How should neovascularisation be recorded so that progression is detectable?",
            "Why is reduced corneal sensitivity dangerous rather than convenient?",
        ],
        "sources": [
            KANSKI_FULL + " — corneal avascularity, nutrition and innervation p. 168.",
            IACLE_FULL + " — Module 6, Lecture 6.1 Corneal Oxygen Requirements and "
            "the Effects of Hypoxia p. 5; Module 2 p. 12 for the symptoms of oedema.",
        ],
    },

    {
        "slug": "09-complications-of-soft-lenses-continued",
        "title": "Complications of Soft Lenses (continued)",
        "hours": 1,
        "summary": (
            "The inflammatory, mechanical and infective complications — and the "
            "distinction between a sterile infiltrate and microbial keratitis, which "
            "is the most consequential judgement in contact lens practice."
        ),
        "wco": (
            "<strong>Category 3 — Ocular Diagnostic Services.</strong> Same-day "
            "recognition and referral of microbial keratitis is a defining safety "
            "competency."
        ),
        "sections": [
            {
                "heading": "1. Papillary conjunctivitis",
                "blocks": [
                    {"type": "list", "items": [
                        "<strong>Papillae on the upper tarsal conjunctiva</strong> — the "
                        "reason lid eversion is not optional in a symptomatic wearer.",
                        "Caused by a combined mechanical and immunological response to the "
                        "lens edge, surface deposits or care solutions.",
                        "Symptoms: itch, mucus, increasing lens awareness, shortening "
                        "wearing time and lens mobility on blink.",
                        "Managed by changing lens, modality or care system — often moving to "
                        "daily disposable removes the deposit and the solution together.",
                    ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "Evert, or miss it",
                     "text":
                        "Kanski places giant papillae on the <em>upper</em> tarsal "
                        "conjunctiva. A wearer complaining of reducing wearing time whose "
                        "lids you have not everted has not been examined."},
                ],
            },
            {
                "heading": "2. Solution-related reactions",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>\"The use of strong disinfectants (many of which are also "
                        "used in lower concentrations as preservatives) in chemical-based "
                        "disinfection systems can cause problems for the patient.\"</strong>",
                     "cite": IACLE_M5.format(12)},
                    {"type": "list", "items": [
                        "Diffuse punctate staining, worst where the solution pools.",
                        "Stinging on insertion, redness settling through the day.",
                        "A peroxide system inserted without neutralisation causes immediate, "
                        "severe pain and a chemical injury — a genuine emergency.",
                    ]},
                    {"type": "callout",
                     "title": "Change one thing at a time",
                     "text":
                        "When lens, modality and solution are all changed at once and the "
                        "patient improves, you have learned nothing about the cause. Change "
                        "the solution first — it is the cheapest variable and often the "
                        "culprit."},
                ],
            },
            {
                "heading": "3. Mechanical complications",
                "blocks": [
                    {"type": "list", "items": [
                        "<strong>Superior epithelial arcuate lesion (SEAL)</strong> — an arc "
                        "of epithelial disruption in the superior cornea, from mechanical "
                        "interaction between a stiffer lens and the upper lid. More "
                        "associated with higher-modulus materials.",
                        "<strong>Tight lens syndrome</strong> — a dehydrated or steep lens "
                        "binds, giving pain, injection and an indentation ring after removal.",
                        "<strong>Lens dehydration staining</strong> — punctate staining in "
                        "the pattern of the lens, worse in dry environments and toward the "
                        "end of the day.",
                    ]},
                ],
            },
            {
                "heading": "4. The judgement that matters",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>Contact lens wear, particularly if extended, is the most "
                        "important risk factor</strong> for bacterial keratitis. "
                        "<strong>Wearers of soft lenses are at higher risk than those of "
                        "rigid gas permeable and other types.</strong> Infection is more "
                        "likely with poor lens hygiene, <strong>but it can also occur even "
                        "with apparently meticulous lens care, and with daily disposable "
                        "lenses</strong>.",
                     "cite": "Kanski 8e, p. 175"},
                    {"type": "table",
                     "headers": ["", "Sterile infiltrate", "Microbial keratitis"],
                     "rows": [
                         ["Pain", "Mild or absent", "<strong>Significant</strong>"],
                         ["Position", "Peripheral", "More central"],
                         ["Number", "Often multiple", "Usually single"],
                         ["Size", "Small", "Larger"],
                         ["Overlying epithelium", "Intact or minimally stained",
                          "<strong>Definite defect</strong>"],
                         ["Anterior chamber", "Quiet", "<strong>Activity, possibly hypopyon</strong>"],
                         ["Discharge", "Minimal", "Present"],
                     ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The rule when you are unsure",
                     "text":
                        "If you cannot place a lesion confidently in the left-hand column, "
                        "treat it as the right-hand one. The cost of referring a sterile "
                        "infiltrate is an unnecessary appointment. The cost of observing a "
                        "microbial keratitis is a cornea."},
                    {"type": "steps", "intro": "On suspicion, in order:", "items": [
                        "<strong>Remove the lens</strong> and do not replace it.",
                        "<strong>Do not patch</strong> the eye.",
                        "<strong>Do not start a topical steroid.</strong>",
                        "<strong>Retain the lens, case and solutions</strong> — they may be "
                        "cultured.",
                        "<strong>Refer the same day</strong> for scraping and intensive "
                        "topical antibiotics.",
                    ]},
                    {"type": "callout",
                     "title": "Acanthamoeba",
                     "text":
                        "Kanski gives protozoan keratitis its own section "
                        "<span class=\"cite\">p. 197</span>. Suspect it in a lens wearer with "
                        "<strong>pain markedly out of proportion to the signs</strong>, "
                        "particularly with any history of water exposure — tap water rinsing, "
                        "swimming or showering in lenses. It is the reason the tap-water rule "
                        "is absolute."},
                ],
            },
        ],
        "check": [
            "Where do the papillae of contact lens papillary conjunctivitis form, and what does that mean for your examination?",
            "Give three signs of a solution-related reaction.",
            "What is a SEAL and which material property is it associated with?",
            "List four features that distinguish microbial keratitis from a sterile infiltrate.",
            "Does meticulous hygiene exclude microbial keratitis?",
            "State the five immediate actions on suspicion of microbial keratitis.",
            "Which organism should you suspect when pain is out of proportion to the signs?",
        ],
        "sources": [
            KANSKI_FULL + " — bacterial keratitis risk factors p. 175; protozoan "
            "keratitis p. 197.",
            IACLE_FULL + " — Module 5: disinfectants and preservatives p. 12.",
        ],
    },

    {
        "slug": "10-optical-properties-of-soft-lenses",
        "title": "Optical Properties of Soft Lenses",
        "hours": 2,
        "summary": (
            "Why a soft lens has no tear lens, what flexure does to the correction, "
            "how vertex distance changes the power you order, and the magnification "
            "difference that makes lenses valuable in anisometropia."
        ),
        "wco": (
            "<strong>Category 1 — Optical Technology Services.</strong> Power "
            "determination, over-refraction and management of anisometropia."
        ),
        "sections": [
            {
                "heading": "1. No tear lens — the defining simplification",
                "blocks": [
                    {"type": "prose", "text":
                        "<strong>When a flexible lens is placed on the cornea, the 'tear "
                        "lens' under the contact lens is very thin. It has no dioptric power "
                        "due to the conformity of the lens to the shape of the cornea.</strong>",
                     "cite": IACLE_M2.format(135)},
                    {"type": "callout", "variant": "clinical",
                     "title": "What this buys you",
                     "text":
                        "Because there is no tear lens to compensate for, soft lens power is "
                        "the ocular refraction corrected for vertex distance — nothing more. "
                        "Changing the BOZR of a soft lens changes the <em>fit</em>, not the "
                        "power. That is the opposite of a rigid lens, and it is the single "
                        "most useful contrast in this course."},
                ],
            },
            {
                "heading": "2. Flexure — the complication that returns",
                "blocks": [
                    {"type": "prose", "text":
                        "The same conformity that removes the tear lens creates a different "
                        "problem: the lens takes on the shape of what it drapes over. IACLE "
                        "notes that the tear lens under a rigid lens depends on the fitting "
                        "relationship <strong>and, to a lesser extent, the material's "
                        "rigidity</strong> — rigidity being exactly what a soft lens lacks.",
                     "cite": IACLE_M2.format(135)},
                    {"type": "list", "intro": "The practical consequences:", "items": [
                        "<strong>Corneal astigmatism is not masked.</strong> A soft sphere "
                        "wraps onto a toric cornea and reproduces its astigmatism, so "
                        "significant cylinder needs a toric lens rather than a spherical one.",
                        "<strong>Thickness resists flexure.</strong> A thicker lens flexes "
                        "less — but thickness also lowers Dk/t, so the two requirements pull "
                        "against each other.",
                        "<strong>Toric lenses must be stabilised</strong>, since a rotating "
                        "cylinder is worse than none.",
                    ]},
                ],
            },
            {
                "heading": "3. Vertex distance",
                "blocks": [
                    {"type": "prose", "text":
                        "A spectacle lens sits roughly 12–14 mm in front of the cornea; a "
                        "contact lens sits on it. The effective power differs, and the "
                        "difference grows with the power of the correction.",
                     "cite": IACLE_M2.format(104)},
                    {"type": "equation", "text": "F<sub>c</sub>  =  F<sub>s</sub> / (1 &minus; d &middot; F<sub>s</sub>)",
                     "where": "F<sub>s</sub> = spectacle power (D) &middot; F<sub>c</sub> = "
                              "contact lens power (D) &middot; d = vertex distance in metres"},
                    {"type": "table",
                     "headers": ["Spectacle Rx", "Direction of change", "Roughly"],
                     "rows": [
                         ["Low (under about &plusmn;4 D)", "Negligible", "No change"],
                         ["<strong>High minus</strong>", "Needs <strong>less minus</strong>", "e.g. &minus;10.00 &rarr; about &minus;9.00"],
                         ["<strong>High plus</strong>", "Needs <strong>more plus</strong>", "e.g. +10.00 &rarr; about +11.00"],
                     ]},
                    {"type": "callout",
                     "title": "The threshold to remember",
                     "text":
                        "Compensate above about <strong>&plusmn;4.00 D</strong>. Below that "
                        "the change is inside your measurement error; above it, failing to "
                        "compensate is the reason a high myope complains their new lenses "
                        "are over-minused."},
                ],
            },
            {
                "heading": "4. Magnification and anisometropia",
                "blocks": [
                    {"type": "prose", "text":
                        "IACLE devotes a section to <strong>Magnification</strong> and "
                        "specifically to <strong>Spectacle and Contact Lens</strong> "
                        "magnification.",
                     "cite": IACLE_M2.format(104)},
                    {"type": "list", "items": [
                        "A <strong>minus spectacle lens minifies</strong> the retinal image; "
                        "a <strong>plus spectacle lens magnifies</strong> it. The effect grows "
                        "with power and with vertex distance.",
                        "A <strong>contact lens sits at the cornea</strong>, so the "
                        "magnification difference between the two eyes is far smaller.",
                        "In <strong>anisometropia</strong>, spectacles therefore produce "
                        "unequal retinal image sizes (<strong>aniseikonia</strong>), which "
                        "may prevent comfortable fusion. Contact lenses largely remove this.",
                    ]},
                    {"type": "callout", "variant": "clinical",
                     "title": "The strongest optical argument for contact lenses",
                     "text":
                        "For a patient with significant anisometropia, contact lenses are not "
                        "a cosmetic preference — they are the correction that makes binocular "
                        "vision possible. Evans makes the related point that anisometropic "
                        "amblyopes may not perceive an immediate benefit on insertion and so "
                        "are more likely to drop out "
                        "<span class=\"cite\">Evans, p. 82</span>: warn them, or you will "
                        "lose them in the first fortnight."},
                ],
            },
            {
                "heading": "5. Over-refraction",
                "blocks": [
                    {"type": "prose", "text":
                        "IACLE provides a dedicated practical, <strong>Practical 2.3 Contact "
                        "Lens Over-Refraction</strong>.",
                     "cite": IACLE_M2.format(104)},
                    {"type": "steps", "intro": "For a soft lens:", "items": [
                        "Insert a trial lens of known BVP and <strong>allow it to "
                        "settle</strong> — a lens refracted immediately on insertion gives a "
                        "misleading result.",
                        "Check the <strong>fit</strong> first: movement, centration, coverage. "
                        "An over-refraction through a poorly fitting lens measures the "
                        "misfit, not the eye.",
                        "Over-refract. <strong>Ordered BVP = trial BVP + over-refraction.</strong>",
                        "If the over-refraction contains unexpected cylinder, suspect "
                        "<strong>flexure over a toric cornea</strong> before assuming the "
                        "spectacle refraction was wrong.",
                    ]},
                ],
            },
        ],
        "check": [
            "Why does a soft lens have no tear-lens power, and what does changing its BOZR alter instead?",
            "Why does a spherical soft lens fail to mask corneal astigmatism?",
            "Why do flexure resistance and oxygen transmissibility pull against each other?",
            "Write the vertex distance formula and state the power threshold above which you compensate.",
            "A +10.00 D spectacle wearer — more plus or less plus in the contact lens?",
            "Explain why contact lenses help in anisometropia.",
            "Unexpected cylinder appears in a soft lens over-refraction. What do you suspect first?",
        ],
        "sources": [
            IACLE_FULL + " — Module 2, Lecture 2.3: the tear lens and material "
            "rigidity p. 135; lecture contents covering back vertex power, ametropia, "
            "magnification, spectacle and contact lens magnification and "
            "over-refraction p. 104; Practical 2.3 Contact Lens Over-Refraction.",
            EVANS_FULL + " — anisometropic amblyopes and contact lens drop-out p. 82.",
        ],
    },
]

COURSES = [
    OCULAR_DISEASES,
    CONTACT_LENSES,
    NEUROVISUAL_PERCEPTION,
    OPTICAL_INSTRUMENTATION,
    OPHTHALMIC_LENSES_DISPENSING,
    VISUAL_OPTICS_BINOCULAR_VISION,
]
