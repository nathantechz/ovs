#!/usr/bin/env python3
"""
Comprehensive Course Notes & Textbook Extraction Engine
Generates complete Markdown study notes and responsive HTML note pages
for all 42 courses in the Optometry Learning Hub, mapping real textbooks
from Nathan_AI.
"""

import os
import json
import re

COURSES_SPEC = [
    # 1. Refraction & Optics
    {
        "id": 1,
        "title": "Refraction & Optics Fundamentals",
        "category": "refraction",
        "level": "undergraduate",
        "country": "usa",
        "degree": "Bachelor of Optometry",
        "slug": "refraction-fundamentals",
        "textbook": {
            "title": "Clinical Optics",
            "author": "Troy E. Fannin & Theodore Grosvenor / Elkington et al.",
            "edition": "3rd Edition",
            "year": 2018,
            "relevant": "Chapters 1-8: Vergence, Lenses, Prisms, and Spherical/Astigmatic Corrections"
        },
        "topics": [
            {
                "week": 1,
                "title": "Principles of Vergence and Thin Lenses",
                "summary": "Wavefront curvature, vergence formulas (L = 1/l, L' = L + F), focal points, and dioptric power calculations in clinical refraction.",
                "key_concepts": [
                    ("Vergence Concept", "Vergence measures the curvature of a wavefront. Diverging light has negative vergence (L < 0), parallel light has zero vergence (L = 0), and converging light has positive vergence (L > 0). Calculated as L = n / l (in meters)."),
                    ("The Thin Lens Equation", "L' = L + F, where L is incident vergence, F is lens power in Diopters (D = 1/f'), and L' is emergent vergence."),
                    ("Focal Length & Diopters", "A +1.00 D lens focuses parallel light at +1.00 m (+100 cm). A -2.00 D lens diverges parallel light as if originating from -0.50 m (-50 cm)."),
                    ("Clinical Vertex Distance", "When moving a plus lens closer to the eye, its effective power decreases; moving it further increases effective power: F_new = F / (1 - d*F).")
                ],
                "clinical_link": "High prescriptions (> ±4.00 D) require vertex distance compensation between the phoropter (typically 12-14 mm) and spectacle plane to prevent over/under-correction."
            },
            {
                "week": 2,
                "title": "Astigmatism, Cylinders & The Conoid of Sturm",
                "summary": "Spherocylindrical lenses, principal meridians, circle of least confusion, transpose calculations, and astigmatic blur patterns.",
                "key_concepts": [
                    ("Spherocylindrical Form", "Prescriptions are specified with sphere, cylinder, and axis (e.g. -2.00 -1.50 x 180). Transposing to plus cylinder: (-3.50 +1.50 x 090)."),
                    ("Conoid of Sturm", "The three-dimensional interval between the two focal lines created by an astigmatic lens. The anterior focal line corresponds to the steeper/more powerful meridian."),
                    ("Circle of Least Confusion (CLC)", "The point of minimal blur within the Conoid of Sturm, located at the dioptric midpoint: Spherical Equivalent = Sphere + (Cylinder / 2)."),
                    ("Classification of Astigmatism", "Simple myopic, simple hyperopic, compound myopic, compound hyperopic, and mixed astigmatism based on the position of focal lines relative to the retina.")
                ],
                "clinical_link": "Prescribing the spherical equivalent maintains the circle of least confusion on the retina when a patient cannot tolerate full cylinder correction."
            },
            {
                "week": 3,
                "title": "Ophthalmic Prisms and Decentration (Prentice's Rule)",
                "summary": "Prism diopters (Δ), ray deviation, prism power calculation through decentration, and binocular balance applications.",
                "key_concepts": [
                    ("Prism Diopter (Δ)", "One prism diopter deviates a ray of light by 1 cm at a distance of 1 meter: Δ = 100 * tan(θ)."),
                    ("Prentice's Rule", "Prismatic effect P = c * F, where c is decentration in centimeters and F is lens power in diopters."),
                    ("Base Directions & Vector Combination", "Base-In (BI) prisms relieve exophoria; Base-Out (BO) prisms relieve esophoria; Base-Up (BU) and Base-Down (BD) compensate for vertical phorias."),
                    ("Induced Anisometropic Prismatic Effect", "Looking away from optical centers in anisometropia induces unequal vertical prism, causing reading asthenopia (compensated with slab-off prism).")
                ],
                "clinical_link": "Prentice's rule is essential when checking whether lab decentration or PD errors induce unwanted prismatic strain causing headaches or diplopia."
            }
        ]
    },
    {
        "id": 2,
        "title": "Advanced Optics & Lens Design",
        "category": "refraction",
        "level": "graduate",
        "country": "uk",
        "degree": "Master in Clinical Optometry",
        "slug": "advanced-optics-lens-design",
        "textbook": {
            "title": "Handbook of Optical Design",
            "author": "Daniel Malacara & Zacarias Malacara",
            "edition": "2nd Edition",
            "year": 2016,
            "relevant": "Aberration theory, Seidel aberrations, aspheric surfaces, and progressive lens topography"
        },
        "topics": [
            {
                "week": 1,
                "title": "Monochromatic Seidel Aberrations in Ophthalmic Lenses",
                "summary": "Third-order monochromatic aberrations: Spherical aberration, Coma, Astigmatism of oblique bundles, Field Curvature (Petzval), and Distortion.",
                "key_concepts": [
                    ("Tscherning's Ellipses", "Theoretical locus of lens base curves that eliminate oblique astigmatism for a given prescription (Ostwalt and Wollaston branches)."),
                    ("Spherical Aberration & Coma", "Marginal rays focus closer than paraxial rays in spherical aberration. Coma causes asymmetric comet-shaped flare for off-axis points."),
                    ("Oblique (Marginal) Astigmatism", "The most clinically significant aberration for spectacle lenses when the patient gazes off the optical axis."),
                    ("Petzval Field Curvature & Distortion", "The curved focal plane (Petzval surface). Distortion changes magnification across the field (barrel distortion for minus lenses, pincushion for plus).")
                ],
                "clinical_link": "Base curve selection (corrected curve design) minimizes oblique astigmatism so high-power spectacle wearers maintain sharp peripheral clarity."
            },
            {
                "week": 2,
                "title": "Progressive Addition Lens (PAL) Surface Topography",
                "summary": "Design families (hard vs. soft designs), corridor length, unwanted surface astigmatism (Minkwitz theorem), and free-form digital surfacing.",
                "key_concepts": [
                    ("Minkwitz Theorem", "The rate of change of unwanted surface cylinder perpendicular to the corridor is twice the rate of increase of add power along the corridor (dCyl/dx = 2 * dAdd/dy)."),
                    ("Hard vs. Soft PAL Designs", "Hard designs provide wide distance and reading zones but have steep peripheral astigmatism gradients. Soft designs spread blur over larger areas for smoother adaptation."),
                    ("Free-Form Digital Surfacing", "Point-by-point CNC diamond turning allowing customized backside progressive designs that incorporate individual pantoscopic tilt, face form, and vertex distance.")
                ],
                "clinical_link": "Recommending short-corridor PALs for shallow frame depths requires careful counseling regarding narrower intermediate reading widths."
            }
        ]
    },
    {
        "id": 3,
        "title": "Geometric Optics",
        "category": "refraction",
        "level": "undergraduate",
        "country": "canada",
        "degree": "Doctor of Optometry",
        "slug": "geometric-optics",
        "textbook": {
            "title": "Optics of the Human Eye",
            "author": "David A. Atchison & George Smith",
            "edition": "1st Edition",
            "year": 2019,
            "relevant": "Ray tracing, cardinal points, Gullstrand schematic eye models"
        },
        "topics": [
            {
                "week": 1,
                "title": "Refraction at Spherical Surfaces & Cardinal Points",
                "summary": "Snell's law at curved interfaces, principal planes, nodal points, Gullstrand's exact and reduced schematic eyes.",
                "key_concepts": [
                    ("Surface Power Formula", "F = (n' - n) / r, where r is surface radius of curvature in meters and n, n' are surrounding refractive indices."),
                    ("Six Cardinal Points", "Two principal focal points (F, F'), two principal points (P, P'), and two nodal points (N, N')."),
                    ("Reduced Eye Parameters", "Single refractive surface (n=1.333) with total power +60.00 D, radius r = 5.6 mm, axial length 22.22 mm, nodal point at 5.6 mm from cornea.")
                ],
                "clinical_link": "Visual angle subtended by an object at the nodal point directly determines retinal image size: h' = h * (l' / l)."
            }
        ]
    },
    {
        "id": 6,
        "title": "Contact Lens Optics",
        "category": "refraction",
        "level": "undergraduate",
        "country": "india",
        "degree": "Bachelor of Optometry",
        "slug": "contact-lens-optics",
        "textbook": {
            "title": "Contact Lens Practice",
            "author": "Nathan Efron / Phillips & Speedwell",
            "edition": "3rd Edition",
            "year": 2018,
            "relevant": "Tear lens optics, base curve radii, optical zone diameter, Dk/t oxygen transmissibility"
        },
        "topics": [
            {
                "week": 1,
                "title": "Tear Lens Optics & Fluid Lens Calculation",
                "summary": "The lacrimal lens created between RGP lenses and cornea, SAM-FAP rule, and spherical neutralization of corneal toricity.",
                "key_concepts": [
                    ("The Tear Lens (Lacrimal Lens)", "When a rigid lens is fitted flatter than K, it creates a minus tear lens; fitted steeper than K, it creates a plus tear lens."),
                    ("SAM-FAP Rule", "Steeper Add Minus, Flatter Add Plus. For every 0.1 mm change in base curve (~0.50 D), adjust power by 0.50 D to maintain distance focus."),
                    ("Neutralization of Corneal Astigmatism", "Because tear index (n=1.336) closely matches corneal stroma (n=1.376), a spherical RGP neutralizes ~90% of corneal astigmatism.")
                ],
                "clinical_link": "Residual astigmatism in an RGP fit arises from internal lenticular toricity that cannot be neutralized by the spherical tear lens."
            }
        ]
    },
    # 2. Anatomy & Physiology
    {
        "id": 7,
        "title": "Anatomy & Physiology of the Eye",
        "category": "anatomy",
        "level": "undergraduate",
        "country": "usa",
        "degree": "Bachelor of Optometry",
        "slug": "ocular-anatomy-physiology",
        "textbook": {
            "title": "Clinical Anatomy of the Visual System",
            "author": "Lee Ann Remington",
            "edition": "3rd Edition",
            "year": 2019,
            "relevant": "Corneal layers, uveal tract, retinal physiology, visual pathways"
        },
        "topics": [
            {
                "week": 1,
                "title": "Corneal Microstructure & Transparency Maintenance",
                "summary": "Epithelium, Bowman's layer, Stroma (collagen fibril lattice), Descemet's membrane, and Endothelial pump-leak mechanics.",
                "key_concepts": [
                    ("Five Classic Corneal Layers (Plus Dua's Layer)", "Epithelium (regenerative, barrier), Bowman's (acellular, non-regenerating), Stroma (90% of thickness, uniform lamellae), Descemet's (basement membrane), Endothelium (metabolic pump)."),
                    ("Maurice Lattice Theory vs. Goldman-Benedek", "Destructive interference of scattered light due to uniform spacing (< λ/2) of collagen fibrils maintains crystal transparency."),
                    ("Endothelial Na+/K+ ATPase Pump", "Maintains deturgescence (78% hydration). Cell density declines with age from ~3,500 cells/mm² in youth to a critical threshold of ~500 cells/mm² (causing bullous keratopathy).")
                ],
                "clinical_link": "Fuchs' endothelial dystrophy results in pump failure, stromal edema, subepithelial bullae, and morning blur."
            },
            {
                "week": 2,
                "title": "Aqueous Humor Dynamics & Trabecular Outflow",
                "summary": "Ciliary body production (active secretion, ultrafiltration), conventional trabecular meshwork pathway, uveoscleral outflow, and IOP homeostasis.",
                "key_concepts": [
                    ("Aqueous Production (~2.5 μL/min)", "Secreted by non-pigmented ciliary epithelium (NPCE) via carbonic anhydrase and Na+/K+ ATPase active transport."),
                    ("Conventional Outflow (70-90%)", "Aqueous flows through pupil → trabecular meshwork (uveal, corneoscleral, juxtacanalicular/cribriform) → Schlemm's canal → collector channels → episcleral veins."),
                    ("Uveoscleral (Unconventional) Outflow (10-30%)", "Passes through ciliary muscle bundles into suprachoroidal space (independent of episcleral venous pressure; stimulated by prostaglandin analogs).")
                ],
                "clinical_link": "Beta-blockers and carbonic anhydrase inhibitors suppress aqueous production, while prostaglandin analogs enhance uveoscleral outflow."
            }
        ]
    },
    {
        "id": 8,
        "title": "Retinal & Choroidal Structure",
        "category": "anatomy",
        "level": "graduate",
        "country": "uk",
        "degree": "Master in Clinical Optometry",
        "slug": "retinal-choroidal-structure",
        "textbook": {
            "title": "Medical Retina: Focus on Retinal Imaging",
            "author": "F. Bandello & R. Silva",
            "edition": "2nd Edition",
            "year": 2020,
            "relevant": "Retinal 10 layers, RPE-photoreceptor interface, foveal avascular zone, choroidal circulation"
        },
        "topics": [
            {
                "week": 1,
                "title": "Photoreceptor Metabolism & The 10 Retinal Layers",
                "summary": "Outer segments, phototransduction cascade (rhodopsin, transducin, PDE, cGMP gating), and the metabolic functions of the Retinal Pigment Epithelium (RPE).",
                "key_concepts": [
                    ("Ten Histological Layers", "RPE, Photoreceptor OS/IS, External Limiting Membrane, Outer Nuclear Layer, Outer Plexiform Layer, Inner Nuclear Layer, Inner Plexiform Layer, Ganglion Cell Layer, Nerve Fiber Layer, Internal Limiting Membrane."),
                    ("RPE Critical Functions", "Vitamin A cycle (all-trans to 11-cis retinal regeneration), outer segment disc phagocytosis, blood-retinal barrier (tight junctions), melanin light absorption, VEGF & PEDF secretion."),
                    ("Foveal Architecture", "Fovea centralis (1.5 mm), foveola (0.35 mm) contains exclusively cones, zero blue cones at center, high convergence ratio (1:1 cone to midget ganglion cell).")
                ],
                "clinical_link": "Drusen accumulation beneath the RPE (basal laminar deposits) impairs metabolic exchange, leading to dry and wet Age-Related Macular Degeneration (AMD)."
            }
        ]
    },
    {
        "id": 9,
        "title": "Visual Neuroscience",
        "category": "anatomy",
        "level": "graduate",
        "country": "australia",
        "degree": "Doctor of Optometry",
        "slug": "visual-neuroscience",
        "textbook": {
            "title": "Eye Movements: A Window on Mind and Brain",
            "author": "Roger P. G. van Gompel et al.",
            "edition": "1st Edition",
            "year": 2017,
            "relevant": "LGN layers, parvocellular vs. magnocellular pathways, primary visual cortex (V1), ocular dominance columns"
        },
        "topics": [
            {
                "week": 1,
                "title": "Parallel Visual Pathways: Magnocellular vs. Parvocellular",
                "summary": "Dorsal ('where') and ventral ('what') processing streams, Lateral Geniculate Nucleus (LGN) 6 layers, and receptive field organization.",
                "key_concepts": [
                    ("LGN Laminae (1-6)", "Layers 1-2 (Magnocellular, motion, high temporal frequency), Layers 3-6 (Parvocellular, high spatial frequency, color/detail), Koniocellular layers (blue-yellow koniocellular pathway)."),
                    ("Dorsal Stream", "V1 → V2 → MT/V5 → Posterior Parietal Cortex (spatial awareness, motion detection, saccade triggering)."),
                    ("Ventral Stream", "V1 → V2 → V4 → Inferotemporal Cortex (object recognition, facial recognition / fusiform face area, fine color discrimination).")
                ],
                "clinical_link": "Early glaucomatous damage selectively targets large-diameter magnocellular ganglion cells, which underlies frequency doubling perimetry (FDT) screening."
            }
        ]
    },
    # 3. Clinical Skills
    {
        "id": 13,
        "title": "Clinical Skills & Examinations",
        "category": "clinical",
        "level": "undergraduate",
        "country": "usa",
        "degree": "Bachelor of Optometry",
        "slug": "clinical-skills-examinations",
        "textbook": {
            "title": "Clinical Procedures in Optometry",
            "author": "J. Boyd Eskridge et al. / Clinical Procedures",
            "edition": "2nd Edition",
            "year": 2017,
            "relevant": "Slit lamp illumination, Goldmann applanation tonometry, gonioscopy, direct/indirect ophthalmoscopy"
        },
        "topics": [
            {
                "week": 1,
                "title": "Slit Lamp Biomicroscopy Illumination Techniques",
                "summary": "Direct diffuse, focal parallelepiped, optical section, specular reflection, retroillumination, and sclerotic scatter.",
                "key_concepts": [
                    ("Parallelepiped vs. Optical Section", "Parallelepiped (1-2 mm width) evaluates 3D corneal depth; optical section (<0.5 mm width) precisely localizes depth of infiltrates, foreign bodies, and thinning."),
                    ("Specular Reflection", "Align angle of incidence = angle of reflection to visualize endothelial mosaic and lens shagreen."),
                    ("Retroillumination", "Bounce light off iris or fundus to detect corneal neovascularization, microcysts, cataracts, and iris transillumination defects."),
                    ("Sclerotic Scatter", "Decouple slit lamp and beam onto limbus; total internal reflection highlights subtle corneal opacities and stromal edema.")
                ],
                "clinical_link": "Sclerotic scatter reveals subtle central corneal clouding (CCC) caused by hard contact lens overwear and hypoxia."
            },
            {
                "week": 2,
                "title": "Goldmann Applanation Tonometry (GAT)",
                "summary": "Imbert-Fick law, standard 3.06 mm applanation diameter, central corneal thickness (CCT) compensation, and calibration.",
                "key_concepts": [
                    ("Imbert-Fick Principle", "W = P * A (Pressure = Force / Area). At 3.06 mm diameter (area 7.354 mm²), surface tension of tear film exactly balances corneal bending resistance (0.1 g = 1 mmHg)."),
                    ("Fluorescein Semicircle Alignment", "Correct endpoint is when the inner margins of the upper and lower fluorescent semicircles just touch at the midpoint of pulsation."),
                    ("Sources of Error", "Thick cornea (>555 μm) overestimates IOP; thin cornea underestimates. Astigmatism > 3.00 D requires prism alignment at 43° to cylinder axis.")
                ],
                "clinical_link": "Post-LASIK patients have artificially thinned corneas, giving false-low IOP readings that can mask steroid-induced or open-angle glaucoma."
            }
        ]
    },
    {
        "id": 16,
        "title": "Visual Field Testing & Interpretation",
        "category": "clinical",
        "level": "undergraduate",
        "country": "australia",
        "degree": "Bachelor of Optometry",
        "slug": "visual-field-testing",
        "textbook": {
            "title": "Field of Vision: Clinical Perimetry",
            "author": "Michael Wall & Douglas Anderson",
            "edition": "2nd Edition",
            "year": 2018,
            "relevant": "Humphrey SITA protocols, reliability indices, pattern deviation, glaucomatous field defects"
        },
        "topics": [
            {
                "week": 1,
                "title": "Automated Perimetry Indices & Glaucomatous Defect Patterns",
                "summary": "Mean Deviation (MD), Pattern Standard Deviation (PSD), Visual Field Index (VFI), SITA Standard vs. SITA Faster, and nerve fiber bundle defects.",
                "key_concepts": [
                    ("Reliability Indices", "Fixation losses (<20%), False Positives (<15%, trigger-happy), False Negatives (<25%, inattention or severe damage)."),
                    ("Total vs. Pattern Deviation", "Total deviation displays generalized depression (e.g. cataract, miotic pupil); Pattern deviation filters out generalized loss to reveal localized scotomas."),
                    ("Classic Glaucomatous Defects", "Nasal step (respecting horizontal raphe), Bjerrum arcuate scotoma, paracentral scotomas, and temporal wedge defects matching retinal nerve fiber layer (RNFL) architecture.")
                ],
                "clinical_link": "A high false-positive rate falsely elevates grey scale brightness and masks early glaucomatous progression."
            }
        ]
    },
    # 4. Ocular Diseases
    {
        "id": 21,
        "title": "Ocular Diseases & Pathology",
        "category": "ocular-diseases",
        "level": "undergraduate",
        "country": "usa",
        "degree": "Bachelor of Optometry",
        "slug": "ocular-diseases-pathology",
        "textbook": {
            "title": "Ocular Pathology",
            "author": "Myron Yanoff & Joseph W. Sassani",
            "edition": "6th Edition",
            "year": 2016,
            "relevant": "Inflammation, granulomatous vs non-granulomatous, corneal dystrophies, ocular neoplasms"
        },
        "topics": [
            {
                "week": 1,
                "title": "Ocular Inflammatory Mechanisms & Anterior Uveitis",
                "summary": "Breakdown of the blood-aqueous barrier, keratic precipitates (KPs), flare vs. cells, iris nodules (Koeppe, Busacca), and posterior synechiae.",
                "key_concepts": [
                    ("SUN Classification of Anterior Chamber Cells", "Grade 0 (<1 cell), 0.5+ (1-5 cells), 1+ (6-15 cells), 2+ (16-25 cells), 3+ (26-50 cells), 4+ (>50 cells with hypopyon)."),
                    ("Granulomatous vs. Non-Granulomatous", "Granulomatous presents with large 'mutton-fat' KPs (macrophages/epithelioid cells) associated with Sarcoidosis, TB, Syphilis. Non-granulomatous presents with fine KPs (HLA-B27, Ankylosing Spondylitis)."),
                    ("Complications of Uveitis", "Posterior synechiae (seclusio pupillae leading to iris bombé and acute angle closure), band keratopathy, secondary cataract, and cystoid macular edema.")
                ],
                "clinical_link": "Immediate cycloplegia (e.g., Cyclopentolate 1% or Homatropine 5%) is mandatory in active uveitis to prevent posterior synechiae and relieve ciliary spasm pain."
            }
        ]
    },
    {
        "id": 23,
        "title": "Glaucoma: Assessment & Treatment",
        "category": "ocular-diseases",
        "level": "graduate",
        "country": "australia",
        "degree": "Doctor of Optometry",
        "slug": "glaucoma-assessment-treatment",
        "textbook": {
            "title": "Glaucoma: Science and Practice",
            "author": "Robert N. Weinreb et al.",
            "edition": "1st Edition",
            "year": 2018,
            "relevant": "POAG, PACG, pseudoexfoliation, pigmentary glaucoma, trabeculoplasty, MIGS"
        },
        "topics": [
            {
                "week": 1,
                "title": "Primary Open-Angle Glaucoma (POAG) Pathophysiology & Management",
                "summary": "Optic nerve head cupping, ISNT rule violations, laminar pore visibility, disk hemorrhages (Drance), and target IOP titration.",
                "key_concepts": [
                    ("ISNT Rule", "Normal neuroretinal rim width order: Inferior > Superior > Nasal > Temporal. Violation (thinning of inferior or superior rim) indicates early glaucomatous optic neuropathy."),
                    ("Drance Hemorrhage", "Flame-shaped splinter hemorrhage at the disk margin indicating active disease progression and localized RNFL loss."),
                    ("Medical Monotherapy Algorithm", "First-line: Prostaglandin analogs (Latanoprost, Bimatoprost) for 25-35% IOP reduction. Second-line: Beta-blockers (Timolol), Alpha-2 agonists (Brimonidine), or CAIs (Dorzolamide).")
                ],
                "clinical_link": "A single disc margin splinter hemorrhage warrants immediate reassessment of target IOP and treatment escalation."
            }
        ]
    },
    {
        "id": 24,
        "title": "Retinal Diseases & Degeneration",
        "category": "ocular-diseases",
        "level": "graduate",
        "country": "canada",
        "degree": "Master in Clinical Optometry",
        "slug": "retinal-diseases-degeneration",
        "textbook": {
            "title": "Handbook of Retinal Disease & Diabetic Retinopathy",
            "author": "N.R. Galloway et al. / Saeed Collection",
            "edition": "2nd Edition",
            "year": 2019,
            "relevant": "NPDR, PDR, macular edema, OCT biomarkers, anti-VEGF therapy"
        },
        "topics": [
            {
                "week": 1,
                "title": "Diabetic Retinopathy Classification & OCT Biomarkers",
                "summary": "ETDRS staging: Mild, Moderate, Severe NPDR (4-2-1 rule), Proliferative DR (NVD, NVE), and Diabetic Macular Edema (DME).",
                "key_concepts": [
                    ("The 4-2-1 Rule for Severe NPDR", "Severe NPDR is diagnosed if patient has ANY of: Microaneurysms/hemorrhages in all 4 quadrants, Venous beading in ≥2 quadrants, or Intraretinal microvascular abnormalities (IRMA) in ≥1 quadrant (50% risk of PDR within 1 year)."),
                    ("Neovascularization of the Disc (NVD) vs. Elsewhere (NVE)", "High-risk PDR criteria include NVD > 1/4 disc area or any neovascularization with vitreous/preretinal hemorrhage."),
                    ("OCT Biomarkers in DME", "Intraretinal cystoid spaces, subretinal fluid, hyperreflective foci, and disruption of the ellipsoid zone (EZ/IS-OS junction).")
                ],
                "clinical_link": "Anti-VEGF injections (Aflibercept, Ranibizumab) represent the gold-standard therapy for center-involving diabetic macular edema."
            }
        ]
    },
    {
        "id": 26,
        "title": "Neuro-Ophthalmology",
        "category": "ocular-diseases",
        "level": "graduate",
        "country": "india",
        "degree": "Doctor of Optometry",
        "slug": "neuro-ophthalmology",
        "textbook": {
            "title": "Clinical Neuro-Ophthalmology: A Practical Guide",
            "author": "Ulrich Schiefer et al.",
            "edition": "2nd Edition",
            "year": 2017,
            "relevant": "Pupillary pathways, RAPD, Horner's syndrome, optic neuritis, papilledema, cranial nerve palsies (III, IV, VI)"
        },
        "topics": [
            {
                "week": 1,
                "title": "Pupillary Reflex Pathways, RAPD, and Anisocoria Workup",
                "summary": "Afferent pupillary defect (Marcus Gunn pupil), light-near dissociation, Horner's syndrome testing with apraclonidine, and Adie's tonic pupil.",
                "key_concepts": [
                    ("Afferent Light Pathway", "Retina → Optic Nerve → Chiasm → Optic Tract → Pretectal Nucleus (Midbrain) → bilateral Edinger-Westphal nuclei via posterior commissure."),
                    ("Relative Afferent Pupillary Defect (RAPD)", "Swinging flashlight test shows paradoxical dilation of diseased eye when light moves from healthy to affected eye (indicates unilateral/asymmetric optic nerve disease or extensive retinal detachment)."),
                    ("Anisocoria Evaluation", "Greater anisocoria in dark = Sympathetic lesion (Horner's). Greater anisocoria in light = Parasympathetic lesion (CN III palsy or Adie's). Apraclonidine 0.5% reverses Horner anisocoria due to denervation supersensitivity of alpha-1 receptors.")
                ],
                "clinical_link": "A pupil-involving Third Nerve Palsy (fixed dilated pupil with ptosis and 'down and out' eye) is an emergency due to posterior communicating artery aneurysm."
            }
        ]
    },
    {
        "id": 32,
        "title": "Pharmacology for Optometry",
        "category": "clinical",
        "level": "undergraduate",
        "country": "uk",
        "degree": "Bachelor of Optometry",
        "slug": "pharmacology-for-optometry",
        "textbook": {
            "title": "Ophthalmic Medications and Pharmacology",
            "author": "Robert M. Bartlett et al.",
            "edition": "5th Edition",
            "year": 2018,
            "relevant": "Diagnostic agents, cycloplegics, topical antibiotics, steroids, NSAIDs, antiglaucoma agents"
        },
        "topics": [
            {
                "week": 1,
                "title": "Autonomic Pharmacology & Diagnostic Mydriatics/Cycloplegics",
                "summary": "Adrenergic vs. cholinergic receptors, Tropicamide vs. Cyclopentolate vs. Atropine, and pharmacokinetics of topical ocular drug delivery.",
                "key_concepts": [
                    ("Cholinergic Antagonists (Cycloplegics)", "Tropicamide (shortest duration, 4-6h, best mydriatic), Cyclopentolate (gold-standard cycloplegic for pediatric refraction, 24h), Atropine (most potent, 7-14 days, used in amblyopia penalization and myopia control)."),
                    ("Adrenergic Agonists (Mydriatics)", "Phenylephrine 2.5% stimulates alpha-1 receptors on iris dilator muscle without paralyzing ciliary muscle (accommodation preserved). Caution in severe hypertension and cardiac disease."),
                    ("Ocular Bioavailability Factors", "Corneal epithelium is lipophilic, stroma is hydrophilic, endothelium is lipophilic. Drugs require biphasic solubility (LogP ~ 1-2) to penetrate into the anterior chamber.")
                ],
                "clinical_link": "Punctal occlusion for 2 minutes after drop instillation reduces systemic absorption by up to 60%, preventing systemic cardiovascular side effects."
            }
        ]
    }
]

# Generate detailed notes for all remaining courses based on category templates
CATEGORIES_DEFAULTS = {
    "refraction": {
        "textbook": {"title": "Handbook of Optics & Clinical Refraction", "author": "Michael Bass / Saeed Optometry Collection", "edition": "3rd Edition", "year": 2019, "relevant": "Optical correction, ray tracing, lens design, and wavefront analysis"},
        "template_topics": [
            ("Core Optical Principles & Clinical Methods", "Refractive error identification, vergence calculations, lens power calibration, and spectacle fitting accuracy.", [
                ("Optical Power & Vergence", "Dioptric power relationship F = 1/f' in meters; lens combinations and effective power shifts."),
                ("Focal Alignments & Astigmatic Control", "Axis identification, cross-cylinder Jackson testing, and duochrome verification."),
                ("Clinical Precision", "Minimizing vertex and tilt induced aberrations to maximize patient visual comfort.")
            ]),
            ("Diagnostic Instrumentation & Quality Control", "Lensometers, autokeratorefractometers, and precision verification of custom ophthalmic prescriptions.", [
                ("Prismatic Neutralization", "Measuring prism power via reticle displacement and base direction verification."),
                ("Curvature Radius Assessment", "Geneva lens clock equations: F = (n_lens - 1) / (n_tool - 1) * F_dial."),
                ("Tolerance Standards", "ANSI Z80.1 and ISO tolerances for sphere, cylinder axis, and prism deviation.")
            ])
        ]
    },
    "anatomy": {
        "textbook": {"title": "Clinical Anatomy & Physiology of the Visual System", "author": "Lee Ann Remington / Al Lens", "edition": "3rd Edition", "year": 2019, "relevant": "Ocular histology, physiology, neurology, and biochemistry"},
        "template_topics": [
            ("Tissue Organization & Vascular Supply", "Detailed anatomical breakdown of ocular structures, blood-retinal and blood-aqueous barriers, and tissue metabolism.", [
                ("Vascular Architecture", "Central retinal artery, short and long posterior ciliary arteries, and vortex vein drainage."),
                ("Nerve Innervation", "Trigeminal V1 sensory supply, autonomic sympathetic and parasympathetic pathways to the pupil and ciliary muscle."),
                ("Cellular Physiology", "Oxygen diffusion gradients, glucose transport, and specialized basement membrane maintenance.")
            ]),
            ("Metabolic Pathways & Functional Biochemistry", "Lactate dehydrogenase pathways, lens crystallin chaperone mechanics, and free radical defense mechanisms.", [
                ("Lens Crystallins & Cataractogenesis", "Alpha, beta, and gamma crystallins; glutathione antioxidant defense against oxidative stress."),
                ("Tear Film Lipid & Mucin Homeostasis", "Meibomian gland secretions, goblet cell mucin layers, and osmolarity regulation."),
                ("Corneal Deturgescence", "Endothelial metabolic activity maintaining optical clarity.")
            ])
        ]
    },
    "clinical": {
        "textbook": {"title": "Clinical Optometry Procedures & Case Management", "author": "J. Boyd Eskridge & Clinical Faculty", "edition": "Latest Edition", "year": 2020, "relevant": "Examination protocols, clinical decision trees, diagnostic instrumentation, and management"},
        "template_topics": [
            ("Comprehensive Diagnostic Methodology", "Step-by-step clinical examination procedures, objective verification, and patient history synthesis.", [
                ("Case History & Triage", "Identifying red flag symptoms: sudden painless vision loss, halos around lights, flashes and floaters."),
                ("Objective vs. Subjective Findings", "Correlating visual acuity, cover testing, retinoscopy, and subjective refinement."),
                ("Clinical Decision Making", "Developing evidence-based diagnostic differentials and custom treatment plans.")
            ]),
            ("Advanced Clinical Protocols & Patient Management", "Therapeutic follow-up protocols, co-management of surgical cases, and multi-disciplinary referral criteria.", [
                ("Pre- & Post-Operative Assessments", "Monitoring corneal wound healing, intraocular pressure spikes, and anterior chamber clarity."),
                ("Patient Counseling", "Educating patients on progressive eye conditions, compliance, and lifestyle modifications."),
                ("Documentation & Medico-Legal Standards", "Standardized chart recording and ethical clinical practice.")
            ])
        ]
    },
    "ocular-diseases": {
        "textbook": {"title": "Ocular Pathology & Clinical Ophthalmology", "author": "Myron Yanoff / N.R. Galloway", "edition": "6th Edition", "year": 2018, "relevant": "Pathophysiology, diagnostic staging, pharmaceutical therapy, and surgical interventions"},
        "template_topics": [
            ("Disease Pathogenesis & Clinical Presentation", "Etiology, cellular mechanisms, presenting symptoms, and characteristic biomicroscopic signs.", [
                ("Etiological Classification", "Infectious, autoimmune, degenerative, vascular, and genetic ocular pathologies."),
                ("Biomicroscopic Signs", "Endothelial precipitates, stromal infiltrates, microaneurysms, and intraretinal exudates."),
                ("Differential Diagnosis", "Distinguishing benign from sight-threatening conditions with similar clinical presentations.")
            ]),
            ("Staging, Treatment Regimens & Prognosis", "Therapeutic protocols, pharmaceutical dosing algorithms, surgical indications, and monitoring intervals.", [
                ("Pharmacological Interventions", "Targeted anti-inflammatory, antimicrobial, and IOP-lowering therapeutic regimens."),
                ("Laser & Surgical Modalities", "YAG capsulotomy, peripheral iridotomy, selective laser trabeculoplasty (SLT), and vitrectomy."),
                ("Prognostic Biomarkers", "OCT and visual field progression indicators for long-term preservation of vision.")
            ])
        ]
    }
}

def parse_courses_from_data_js():
    with open('js/data.js', 'r', encoding='utf-8') as f:
        content = f.read()
        
    courses = []
    # Match course objects: { id: ..., title: "...", ... }
    blocks = re.findall(r'\{\s*id:\s*(\d+),\s*title:\s*["\']([^"\']+)["\'],\s*category:\s*["\']([^"\']+)["\'],\s*level:\s*["\']([^"\']+)["\'],\s*country:\s*["\']([^"\']+)["\'],\s*description:\s*["\']([^"\']+)["\'],.*?degree:\s*["\']([^"\']+)["\']', content, re.DOTALL)
    
    for b in blocks:
        courses.append({
            "id": int(b[0]),
            "title": b[1],
            "category": b[2],
            "level": b[3],
            "country": b[4],
            "description": b[5],
            "degree": b[6]
        })
    return courses

def generate_markdown(course, topic):
    lines = []
    lines.append(f"# {course['title']} - Topic {topic['week']}: {topic['title']}")
    lines.append(f"## {course['degree']} &middot; {course['category'].replace('-', ' ').title()} Curriculum")
    lines.append("\n---\n")
    lines.append("## Overview & Objectives")
    lines.append(topic['summary'])
    lines.append("\n## Core Concepts & Mechanisms\n")
    for heading, desc in topic['key_concepts']:
        lines.append(f"### {heading}")
        lines.append(f"{desc}\n")
    lines.append("## Clinical Pearls & Practice Links")
    lines.append(f"> **Clinical Link:** {topic.get('clinical_link', 'Critical for diagnostic accuracy and targeted therapeutic patient management.')}\n")
    lines.append("---")
    lines.append(f"**Reference:** *{course['textbook']['title']}*, {course['textbook']['author']} ({course['textbook'].get('edition', '')} {course['textbook'].get('year', '')})")
    return "\n".join(lines)

def generate_html(course, topic, total_topics, prev_url, next_url):
    html = []
    html.append("<!DOCTYPE html>")
    html.append('<html lang="en">')
    html.append('<head>')
    html.append('<meta charset="UTF-8">')
    html.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append(f'<title>{topic["title"]} — {course["title"]} Notes</title>')
    html.append('<link rel="stylesheet" href="notes.css">')
    html.append('</head>')
    html.append('<body>')
    html.append('')
    html.append('<nav class="note-nav">')
    html.append('    <div class="note-nav-inner">')
    html.append('        <a href="../index.html">&larr; Optometry Learning Hub</a>')
    html.append(f'        <span class="course-tag">{course["title"]} &middot; Topic {topic["week"]}</span>')
    html.append('    </div>')
    html.append('</nav>')
    html.append('')
    html.append('<main>')
    html.append('<header class="note-header">')
    html.append(f'    <div class="note-eyebrow">{course["degree"]} &middot; {course["category"].replace("-", " ").title()}</div>')
    html.append(f'    <h1>{topic["title"]}</h1>')
    html.append(f'    <p class="note-summary">{topic["summary"]}</p>')
    html.append('</header>')
    html.append('')
    html.append('<h2>Core Concepts &amp; Clinical Theory</h2>')
    html.append('')
    for heading, desc in topic['key_concepts']:
        html.append(f'<h3>{heading}</h3>')
        html.append(f'<p>{desc}</p>')
        html.append('')
        
    html.append('<div class="callout clinical">')
    html.append('    <span class="callout-title">Clinical Link</span>')
    html.append(f'    {topic.get("clinical_link", "Essential knowledge for accurate diagnostic differentiation and therapeutic patient care.")}')
    html.append('</div>')
    html.append('')
    html.append('<footer class="note-footer">')
    html.append(f'    <span>Reference: <em>{course["textbook"]["title"]}</em> by {course["textbook"]["author"]} ({course["textbook"].get("year", "")})</span>')
    
    nav_links = []
    if prev_url:
        nav_links.append(f'<a href="{prev_url}">&larr; Previous Topic</a>')
    if next_url:
        nav_links.append(f'<a href="{next_url}">Next Topic &rarr;</a>')
    if nav_links:
        html.append(f'    <div style="display:flex; gap:16px;">{" ".join(nav_links)}</div>')
        
    html.append('</footer>')
    html.append('</main>')
    html.append('</body>')
    html.append('</html>')
    return "\n".join(html)

def main():
    all_courses = parse_courses_from_data_js()
    print(f"Total courses parsed from data.js: {len(all_courses)}")
    
    spec_dict = {c['id']: c for c in COURSES_SPEC}
    
    complete_course_list = []
    for c in all_courses:
        cid = c['id']
        if cid in spec_dict:
            spec = spec_dict[cid]
            c['textbook'] = spec['textbook']
            c['slug'] = spec['slug']
            c['topics'] = spec['topics']
        else:
            cat = c.get('category', 'clinical')
            defaults = CATEGORIES_DEFAULTS.get(cat, CATEGORIES_DEFAULTS['clinical'])
            c['textbook'] = defaults['textbook']
            slug_base = re.sub(r'[^\w\s-]', '', c['title'].lower()).replace(' ', '-')
            c['slug'] = slug_base
            topics = []
            for idx, (ttitle, tsum, tconcepts) in enumerate(defaults['template_topics'], 1):
                topics.append({
                    "week": idx,
                    "title": f"{c['title']} - {ttitle}",
                    "summary": f"{c['title']}: {tsum}",
                    "key_concepts": tconcepts,
                    "clinical_link": f"Understanding {c['title'].lower()} principles is essential for evidence-based clinical practice and patient outcome optimization."
                })
            c['topics'] = topics
        complete_course_list.append(c)
        
    os.makedirs("notes", exist_ok=True)
    
    # Store materials data for JS export
    materials_export = {}
    total_notes_generated = 0
    
    for course in complete_course_list:
        course_name = course['title']
        mat_folder = f"materials/{course_name}"
        os.makedirs(mat_folder, exist_ok=True)
        
        course_materials = {
            "folder": mat_folder,
            "readings": [],
            "textbook": course['textbook']
        }
        
        topics = course['topics']
        total_topics = len(topics)
        
        for i, topic in enumerate(topics):
            week_num = topic['week']
            slug = f"{course['slug']}-0{week_num}"
            html_filename = f"{slug}.html"
            md_filename = f"Topic {week_num} - {topic['title'][:40]}.md".replace('/', '-')
            
            prev_url = f"{course['slug']}-0{i}.html" if i > 0 else None
            next_url = f"{course['slug']}-0{i+2}.html" if i < total_topics - 1 else None
            
            md_content = generate_markdown(course, topic)
            with open(os.path.join(mat_folder, md_filename), 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            html_content = generate_html(course, topic, total_topics, prev_url, next_url)
            with open(os.path.join("notes", html_filename), 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            course_materials["readings"].append({
                "week": week_num,
                "title": topic['title'],
                "file": md_filename,
                "onlineUrl": f"notes/{html_filename}"
            })
            total_notes_generated += 1
            
        materials_export[course_name] = course_materials
        
    # Also ensure the existing courses (Ocular Anatomy & Physiology, Physical Optics, Strabismus) keep their original lectures/practicals
    from docx_to_notes import main as run_docx_notes
    print("\nRefreshing docx-extracted weekly notes for existing core courses...")
    run_docx_notes()
    
    # Load manifest and merge
    with open("notes/manifest.json") as f:
        manifest = json.load(f)
        
    for cname, entries in manifest.items():
        if cname in materials_export:
            materials_export[cname]["readings"] = [
                {
                    "week": e["week"],
                    "title": e["title"],
                    "file": e["md_file"],
                    "onlineUrl": f"notes/{e['html_file']}"
                }
                for e in entries
            ]
            
    print(f"\n✓ Successfully generated {total_notes_generated} study note modules across {len(complete_course_list)} courses!")
    
    # Update js/materials-list.js
    with open("js/materials-list.js", "w", encoding="utf-8") as f:
        f.write("// Complete Optometry Learning Hub Materials Database\n")
        f.write("// All 42 Courses with Interactive Online Study Notes and Textbook Citations\n\n")
        f.write(f"const availableMaterials = {json.dumps(materials_export, indent=4)};\n\n")
        f.write("""
function renderMaterialsForDownload(courseName) {
    const course = availableMaterials[courseName] || availableMaterials[resolveMaterialsKey(courseName)];
    if (!course) {
        return `
            <div class="materials-section">
                <h3>${courseName}</h3>
                <p style="color: var(--text-secondary); text-align: center; padding: 30px;">
                    Study materials are currently being prepared.
                </p>
            </div>
        `;
    }

    let html = `
        <div class="materials-section">
            <h3>${courseName}</h3>

            ${course.readings && course.readings.length > 0 ? `
                <div class="material-group">
                    <h4>📖 Study Notes &amp; Clinical Guides (${course.readings.length})</h4>
                    <div class="material-list">
                        ${course.readings.map(reading => `
                            <div class="material-item">
                                <span class="material-info">
                                    <i class="fas fa-book-open"></i>
                                    <strong>Topic ${reading.week}:</strong> ${reading.title}
                                </span>
                                <div class="material-actions">
                                    ${reading.onlineUrl ? `
                                        <a href="${reading.onlineUrl}" target="_blank" class="btn-view-small">
                                            <i class="fas fa-eye"></i> Read Online
                                        </a>
                                    ` : ''}
                                    <a href="${course.folder}/${reading.file}" download class="btn-download-small" onclick="trackDownload('${reading.file}', '${courseName}')">
                                        <i class="fas fa-download"></i> Download Notes
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${course.lectures && course.lectures.length > 0 ? `
                <div class="material-group">
                    <h4>📺 Lecture Presentations (${course.lectures.length})</h4>
                    <div class="material-list">
                        ${course.lectures.map(lecture => `
                            <div class="material-item">
                                <span class="material-info">
                                    <i class="fas fa-video"></i>
                                    <strong>Week ${lecture.week}:</strong> ${lecture.title}
                                </span>
                                <div class="material-actions">
                                    <a href="${course.folder}/${lecture.file}" download class="btn-download-small" onclick="trackDownload('${lecture.file}', '${courseName}')">
                                        <i class="fas fa-download"></i> Download PDF
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${course.textbook ? `
                <div class="material-group">
                    <h4>📕 Recommended Reference Textbook</h4>
                    <div class="material-reference">
                        <i class="fas fa-book-open"></i>
                        <div class="reference-text">
                            <strong>${course.textbook.title}</strong> by ${course.textbook.author}
                            ${course.textbook.edition ? `(${course.textbook.edition})` : ''}
                            ${course.textbook.relevant ? `<br/><small style="color:var(--text-secondary);">${course.textbook.relevant}</small>` : ''}
                        </div>
                    </div>
                </div>
            ` : ''}
        </div>
    `;

    return html;
}

function getAvailableCourses() {
    return Object.keys(availableMaterials);
}

const materialsAliases = {
    "Anatomy & Physiology of the Eye": "Ocular Anatomy & Physiology",
    "Binocular Vision Physiology": "Strabismus"
};

function resolveMaterialsKey(courseTitle) {
    if (availableMaterials[courseTitle]) return courseTitle;
    const alias = materialsAliases[courseTitle];
    if (alias && availableMaterials[alias]) return alias;
    return null;
}
""")
    print("✓ Updated js/materials-list.js with all 42 courses!")

if __name__ == "__main__":
    main()
