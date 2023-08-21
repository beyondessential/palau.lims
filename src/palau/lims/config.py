# -*- coding: utf-8 -*-
#
# This file is part of PALAU.LIMS
#
# Copyright 2023 Beyond Essential Systems Pty Ltd

from palau.lims import messageFactory as _
from senaite.abx import messageFactory as _sa
from Products.Archetypes import DisplayList

UNKNOWN_DOCTOR_FULLNAME = "Unknown doctor"

CULTURE_INTERPRETATION_KEYWORD = "CINTER"

# Default analysis services to create on install
# Dict with keys as service keywords
SERVICES = {
    # Culture interpretation
    CULTURE_INTERPRETATION_KEYWORD: {
        "Category": "Microbiology",
        "title": "Culture interpretation",
        "ResultOptions": [
            (0, 'A fungus has been isolated', 'positive'),
            (1, 'alpha haemolytic streptococcus', 'positive'),
            (2, 'Bacillus sp.', 'positive'),
            (3, 'Beta haemolytic streptococcus NOT isolated', 'negative'),
            (4, 'Candida sp.', 'positive'),
            (5, 'Carbapenem Resistant Enterobacteriaceae ISOLATED ', 'positive'),
            (6, 'Carbapenemase Producing Enterobacterales NOT isolated', 'negative'),
            (7, 'Coagulase neg staphylococcus', 'positive'),
            (8, 'Coagulase neg staphylococcus (2 types)', 'positive'),
            (9, 'Corynebacterium species', 'positive'),
            (10, 'Culture in progress', ''),
            (11, 'Culture proceeding', 'positive'),
            (12, 'E.coli (presumptive)', 'positive'),
            (13, 'Enteric Gram Neg Rod', 'positive'),
            (14, 'Enteric Gram Neg Rods & Coagulase negative Staph', 'positive'),
            (15, 'Enteric Gram Neg Rods & Enterococcus', 'positive'),
            (16, 'Enteric Gram Neg Rods (x2)', 'positive'),
            (17, 'Enteric Gram Neg Rods (x3)', 'positive'),
            (18, 'Enteric Gram Neg Rods and Pseudomonas', 'positive'),
            (19, 'Enterococcus (presumptive)', 'positive'),
            (20, 'Environmental gram negative rod', 'positive'),
            (21, 'Extended Spectrum Beta-Lactamase bacteria ISOLATED', 'positive'),
            (22, 'Extended Spectrum Beta-Lactamase bacteria NOT isolated', 'positive'),
            (23, 'Further culture to follow', ''),
            (24, 'Further identification in process', 'positive'),
            (25, 'Gram negative diplococci', 'positive'),
            (26, 'Gram negative rods', 'positive'),
            (27, 'Gram positive rods', 'positive'),
            (28, 'Growth from blood culture bottle(s)', 'positive'),
            (29, 'Growth from enrichment broth only', 'positive'),
            (30, 'Mixed anaerobes', 'positive'),
            (31, 'Mixed enteric flora', 'positive'),
            (32, 'Mixed Enteric Gram Neg Rods and Enterococcus', 'positive'),
            (33, 'Mixed Enteric Gram Neg Rods and Pseudomonas', 'positive'),
            (34, 'Mixed Enteric Gram Negative Rods', 'positive'),
            (35, 'Mixed Gram positive organisms', 'positive'),
            (36, 'Mixed growth of organisms', 'positive'),
            (37, 'Mixed skin flora', 'positive'),
            (38, 'MRSA ISOLATED', 'positive'),
            (39, 'MRSA NOT isolated.', 'negative'),
            (40, 'Neisseria gonorrhoeae NOT isolated', 'negative'),
            (41, 'No Bacterial pathogens isolated', 'negative'),
            (42, 'No growth (<10^5/L)', 'negative'),
            (43, 'No growth (<10^6/L)', 'negative'),
            (44, 'No growth at 48 hours', 'negative'),
            (45, 'No growth at 48 hrs (Further incubation proceeding)', 'negative'),
            (46, 'No likely pathogen isolated after 48 hours', 'negative'),
            (47, 'No significant growth', 'negative'),
            (48, 'No significant growth (<10^6/L)', 'negative'),
            (49, 'Normal skin flora', 'negative'),
            (50, 'Normal uro-genital flora', 'negative'),
            (51, 'Organism identified as:', 'positive'),
            (52, 'Oropharyngeal flora', 'positive'),
            (53, 'Pneumococcus (presumptive)', 'positive'),
            (54, 'Proteus sp. (presumptive)', 'positive'),
            (55, 'Pseudomonas (presumptive)', 'positive'),
            (56, 'Result after further incubation:', 'positive'),
            (57, 'Salmonella NOT isolated', 'negative'),
            (58, 'Salmonella or Shigella spp NOT isolated', 'negative'),
            (59, 'Salmonella, Shigella or Campylobacter spp NOT isolated', 'negative'),
            (60, 'See comment below', ''),
            (61, 'Shigella and Campylobacter spp NOT isolated', 'negative'),
            (62, 'Shigella NOT isolated', 'negative'),
            (63, 'Staph aureus NOT isolated', 'negative'),
            (64, 'Staphylococcus (presumptive)', 'positive'),
            (65, 'Streptococcus/Enterococcus (presumptive)', 'positive'),
            (66, 'Vancomycin Resistant Enterococcus (VRE) isolated', 'positive'),
            (67, 'Vancomycin Resistant Enterococcus NOT isolated', 'negative'),
            (68, 'Vibrio or Yersinia sp NOT isolated', 'negative'),
            (69, 'Vibrio sp. NOT isolated', 'negative'),
        ]
    },

    # Microscopy - Generic
    "WBC": {
        "title": "White Blood Cells",
        "Category": "Microscopy",
        "Unit": "x10⁶/L",
    },
    "RBC": {
        "title": "Red Blood Cells",
        "Category": "Microscopy",
        "Unit": "x10⁶/L",
    },
    "POLY": {
        "title": "Polymorphs",
        "Category": "Microscopy",
        "Unit": "%",
    },
    "MONO": {
        "title": "Mononuclear",
        "Category": "Microscopy",
        "Unit": "%",
    },
    "EOS": {
        "title": "Eosinophils",
        "Category": "Microscopy",
        "Unit": "%",
    },
    "MIC_APPE": {
        "title": "Appearance",
        "Category": "Microscopy",
        "ResultOptions": [
            (0, "Clear", ""),
            (1, "Turbid", ""),
            (2, "Slightly blood stained", ""),
            (3, "Moderately blood stained", ""),
            (4, "Profusely blood stained", ""),
        ]
    },

    # Microscopy - Urine
    "URI_WBC": {
        "title": "Urinary White Blood Cells",
        "Category": "Microscopy",
        "Unit": "x10⁶/L",
        "ResultOptions": [
            (0, "<10", ""),
            (1, "10-100", ""),
            (2, ">100", ""),
        ]
    },
    "URI_RBC": {
        "title": "Urinary Red Blood Cells",
        "Category": "Microscopy",
        "Unit": "x10⁶/L",
        "ResultOptions": [
            (0, "<10", ""),
            (1, "10-100", ""),
            (2, ">100", ""),
        ]
    },
    "URI_SC": {
        "title": "Urinary Squamous Cells",
        "Category": "Microscopy",
        "Unit": "x10⁶/L",
        "ResultOptions": [
            (0, "<10", ""),
            (1, "10-100", ""),
            (2, ">100", ""),
        ]
    },
    "URI_ORG": {
        "title": "Microscope Organisms (Urinary)",
        "Category": "Microscopy",
        "ResultOptions": [
            (0, "Nil Seen", ""),
            (1, "Scanty", ""),
            (2, "Moderate", ""),
            (3, "Profuse", ""),
        ]
    },
    "URI_CASTS": {
        "title": "Urinary casts",
        "Category": "Microscopy",
        "ResultOptions": [
            (0, "Nil Seen", ""),
            (1, "Scanty", ""),
            (2, "Moderate", ""),
            (3, "Profuse", ""),
        ]
    },

    # Microscopy - Swabs
    "POLY_PRES": {
        "title": "Polymorphs presence",
        "Category": "Microscopy",
        "ResultOptions": [
            (0, "Nil Seen", ""),
            (1, "Scanty", ""),
            (2, "Moderate", ""),
            (3, "Profuse", ""),
        ]
    },
    "SC": {
        "title": "Squamous Cells",
        "Category": "Microscopy",
        "ResultOptions": [
            (0, "Nil Seen", ""),
            (1, "Scanty", ""),
            (2, "Moderate", ""),
            (3, "Profuse", ""),
        ]
    },
    "MIC_ORG": {
        "title": "Microscope Organisms",
        "Category": "Microscopy",
        "ResultOptionsType": "multiselect",
        "ResultOptions": [
            (0, "Gram positive cocci - Scanty", ""),
            (1, "Gram positive cocci - Moderate", ""),
            (2, "Gram positive cocci - Profuse", ""),
            (3, "Gram negative Bacilli - Scanty", ""),
            (4, "Gram negative Bacilli - Moderate", ""),
            (5, "Gram negative Bacilli - Profuse", ""),
            (6, "Gram positive Bacilli - Scanty", ""),
            (7, "Gram positive Bacilli - Moderate", ""),
            (8, "Gram positive Bacilli - Profuse", ""),
            (9, "Gram negative cocci - Scanty", ""),
            (10, "Gram negative cocci - Moderate", ""),
            (11, "Gram negative cocci - Profuse", ""),
            (12, "Yeast - Scanty", ""),
            (13, "Yeast - Moderate", ""),
            (14, "Yeast - Profuse", ""),
        ]
    },

    # Microscopy - Cerebrospinal fluid (CSF)
    "CSF_APPE": {
        "title": "CSF Appearance",
        "Category": "Microscopy",
        "ResultOptions": [
            (0, "Clear and colourless", ""),
            (1, "Slightly blood stained", ""),
            (2, "Moderate blood stained", ""),
            (3, "Grossly blood stained", ""),
            (4, "Slight Xanthochromia", ""),
            (5, "Moderate Xanthochromia", ""),
            (6, "Profuse Xanthochromia", ""),
        ]
    },

    # Biochemistry - Cerebrospinal fluid (CSF)
    "CSF_PROT": {
        "title": "CSF Protein",
        "Category": "Biochemistry",
        "Unit": "g/L",
    },
    "CSF_GLUC": {
        "title": "CSF Glucose",
        "Category": "Biochemistry",
        "Unit": "mmol/L",
    },
    "CSF_LACT": {
        "title": "CSF Lactate",
        "Category": "Biochemistry",
        "Unit": "mmol/L",
    },
}

# List of analysis profiles to create on install
# Tuples of (profile name, profile properties)
PROFILES = [
    ("Urinary microscopy tests", {
        "ProfileKey": "URI_MICRO",
        "Service": ["URI_WBC", "URI_RBC", "URI_SC", "URI_ORG"],
    }),
    ("Swab microscopy tests", {
        "ProfileKey": "SWA_MICRO",
        "Service": ["POLY_PRES", "SC", "MIC_ORG"],
    }),
    ("CSF Microscopy tests", {
        "ProfileKey": "CSF_MICRO",
        "Service": ["CSF_APPE", "WBC", "RBC", "MIC_ORG"],
    }),
    ("CSF Biochemistry tests", {
        "ProfileKey": "CSF_BIOCH",
        "Service": ["CSF_PROT", "CSF_GLUC", "CSF_LACT"],
    }),
    ("Body Fluid Microscopy tests", {
        "ProfileKey": "BF_MICRO",
        "Service": ["WBC", "RBC", "SC", "MIC_ORG"],
    }),
]

# List of specifications to create on install
# Tuples of (specification name, specification properties)
SPECIFICATIONS = [
    ("CSF Biochemistry", {
        "SampleType": "CSF",
        "ResultsRange": {
            "CSF_PROT": {
                "min_operator": "geq", "min": 0.2,
                "max_operator": "lt", "max": 0.7,
            },
            "CSF_GLUC": {
                "min_operator": "geq", "min": 2.8,
                "max_operator": "leq", "max": 4.5,
            },
            "CSF_LACT": {
                "min_operator": "geq", "min": 0,
                "max_operator": "lt", "max": 2.8,
            }
        }
    })
]

# Default microorganisms to create on install
# Dict with keys as microorganism title/name
MICROORGANISMS = {
    "Acinetobacter baumannii": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Acinetobacter baumannii (meropenem-resistant)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": True,
        "mro_phenotype": "MRAB",
    },
    "Acinetobacter spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Acinetobacter spp (meropenem-resistant)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": True,
        "mro_phenotype": "MRAB",
    },
    "Aeromonas spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Bacillus spp": {
        "gram_stain": "gram+",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Burkholderia cepacia complex (presumptive)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Campylobacter spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Candida albicans": {
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Candida spp": {
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Citrobacter freundii": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Citrobacter koseri (diversus)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Citrobacter spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Clostridium perfringens": {
        "gram_stain": "gram+",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Clostridium septicum": {
        "gram_stain": "gram+",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Cryptococcus spp": {
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Cutibacterium spp": {
        "gram_stain": "gram+",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Elizabethkingia meningoseptica": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Enterobacter cloacae": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Enterobacter cloacae is a clinically significant Gram-negative, "
            "facultatively-anaerobic, rod-shaped bacterium. E. cloacae is "
            "frequently grown at 30 °C on nutrient agar or broth or at 35 °C "
            "in tryptic soy broth. It is a rod-shaped, Gram-negative "
            "bacterium, is facultatively anaerobic, and bears peritrichous "
            "flagella. It is oxidase-negative and catalase-positive.",
    },
    "Enterobacter spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Enterococcus faecalis": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Enterococcus faecalis (Vancomycin-resistant - VRE)": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "multi_resistant": True,
        "mro_phenotype": "VRE",
    },
    "Enterococcus faecium": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Enterococcus faecium is a Gram-positive, alpha-hemolytic or "
            "non-hemolytic bacterium in the genus Enterococcus. It can be "
            "commensal (innocuous, coexisting organism) in the "
            "gastrointestinal tract of humans and animals, but it may also "
            "be pathogenic, causing diseases such as neonatal meningitis or "
            "endocarditis.",
    },
    "Enterococcus faecium (Vancomycin-resistant - VRE)": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": True,
        "mro_phenotype": "VRE",
        "description":
            "Enterococcus faecium is a Gram-positive, alpha-hemolytic or "
            "non-hemolytic bacterium in the genus Enterococcus. It can be "
            "commensal (innocuous, coexisting organism) in the "
            "gastrointestinal tract of humans and animals, but it may also "
            "be pathogenic, causing diseases such as neonatal meningitis or "
            "endocarditis. Vancomycin-resistant E. faecium is often referred "
            "to as VRE.",
    },
    "Enterococcus spp": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Escherichia coli": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Escherichia coli (ceftriaxone-resistant - ESBL)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": True,
        "mro_phenotype": "ESBL",
    },
    "Escherichia coli (meropenem-resistant - CRE)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": True,
        "mro_phenotype": "CRE",
    },
    "Fusobacterium spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Gram negative organism (other)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Haemophilus influenzae": {
        "gram_stain": "gram-",
        "shape": "rod.coccobacilli",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Haemophilus influenzae (formerly called Pfeiffer's bacillus or "
            "Bacillus influenzae) is a Gram-negative, coccobacillary, "
            "facultatively anaerobic capnophilic pathogenic bacterium of the "
            "family Pasteurellaceae. H. influenzae was first described in 1892 "
            "by Richard Pfeiffer during an influenza pandemic",
    },
    "Haemophilus parainfluenzae": {
        "gram_stain": "gram-",
        "shape": "rod.coccobacilli",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Klebsiella aerogenes": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Klebsiella oxytoca": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Klebsiella pneumoniae": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Klebsiella pneumoniae is a Gram-negative, non-motile, "
            "encapsulated, lactose-fermenting, facultative anaerobic, "
            "rod-shaped bacterium. It appears as a mucoid lactose fermenter on "
            "MacConkey agar. Although found in the normal flora of the mouth, "
            "skin, and intestines, it can cause destructive changes to human "
            "and animal lungs if aspirated, specifically to the alveoli "
            "resulting in bloody, brownish or yellow colored jelly like "
            "sputum. In the clinical setting, it is the most significant "
            "member of the genus Klebsiella of the Enterobacteriaceae. "
            "K. oxytoca and K. rhinoscleromatis have also been demonstrated in "
            "human clinical specimens. In recent years, Klebsiella species "
            "have become important pathogens in nosocomial infections. It "
            "naturally occurs in the soil, and about 30% of strains can fix "
            "nitrogen in anaerobic conditions. As a free-living diazotroph, "
            "its nitrogen-fixation system has been much-studied, and is of "
            "agricultural interest, as K. pneumoniae has been demonstrated to "
            "increase crop yields in agricultural conditions. It is closely "
            "related to K. oxytoca from which it is distinguished by being "
            "indole-negative and by its ability to grow on melezitose but not "
            "3-hydroxybutyrate.",
    },
    "Klebsiella pneumoniae (ceftriaxone-resistant - ESBL)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": True,
        "mro_phenotype": "ESBL",
    },
    "Klebsiella pneumoniae (meropenem-resistant - CRE)": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "CRE",
    },
    "Klebsiella spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "In recent years, Klebsiella species have become important "
            "pathogens in nosocomial infections."
    },
    "Listeria monocytogenes": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Moraxella spp": {
        "gram_stain": "gram-",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Morganella morganii": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Neisseria gonorrhoeae": {
        "gram_stain": "gram-",
        "shape": "coccus.diplococci",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Neisseria gonorrhoeae, also known as gonococcus (singular), or "
            "gonococci (plural) is a species of Gram-negative diplococci "
            "bacteria isolated by Albert Neisser in 1879. It causes the "
            "sexually transmitted genitourinary infection gonorrhea as well "
            "as other forms of gonococcal disease including disseminated "
            "gonococcemia, septic arthritis, and gonococcal ophthalmia "
            "neonatorum.",
    },
    "Neisseria meningitidis": {
        "gram_stain": "gram-",
        "shape": "coccus.diplococci",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Pantoea spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Pasteurella multocida": {
        "gram_stain": "gram-",
        "shape": "rod.coccobacilli",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Proteus mirabilis": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Proteus penneri": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Proteus vulgaris": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Providencia spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Pseudomonas aeruginosa": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Pseudomonas aeruginosa is a common encapsulated, Gram-negative, "
            "rod-shaped bacterium that can cause disease in plants and "
            "animals, including humans. A species of considerable medical "
            "importance, P. aeruginosa is a multidrug resistant pathogen "
            "recognized for its ubiquity, its intrinsically advanced "
            "antibiotic resistance mechanisms, and its association with "
            "serious illnesses – hospital-acquired infections such as "
            "ventilator-associated pneumonia and various sepsis syndromes.",
    },
    "Pseudomonas spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Raoultella spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Salmonella paratyphi A": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Salmonella spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Salmonella is a genus of rod-shaped (bacillus) Gram-negative "
            "bacteria of the family Enterobacteriaceae.",
    },
    "Salmonella typhi": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Serratia marcescens": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Shigella flexneri": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Shigella sonnei": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Shigella spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Shigella is a genus of bacteria that is Gram-negative, "
            "facultative anaerobic, non-spore-forming, nonmotile, rod-shaped "
            "and genetically closely related to E. coli. The genus is named "
            "after Kiyoshi Shiga, who first discovered it in 1897.",
    },
    "Staphylococcus (coagulase-negative)": {
        "gram_stain": "gram+",
        "shape": "coccus.staphylococci",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Staphylococcus aureus (Methicillin-resistant - MRSA)": {
        "gram_stain": "gram+",
        "shape": "coccus.staphylococci",
        "glass": True,
        "multi_resistant": True,
        "mro_phenotype": "MRSA",
        "description":
            "Staphylococcus aureus is a Gram-positive, round-shaped bacterium "
            "that is a member of the Firmicutes, and it is a usual member of "
            "the microbiota of the body, frequently found in the upper "
            "respiratory tract and on the skin. It is often positive for "
            "catalase and nitrate reduction and is a facultative anaerobe "
            "that can grow without the need for oxygen. Although S. aureus "
            "usually acts as a commensal of the human microbiota it can also "
            "become an opportunistic pathogen, being a common cause of skin "
            "infections including abscesses, respiratory infections such as "
            "sinusitis, and food poisoning. Pathogenic strains often promote "
            "infections by producing virulence factors such as potent protein "
            "toxins, and the expression of a cell-surface protein that binds "
            "and inactivates antibodies. The emergence of antibiotic-resistant "
            "strains of S. aureus such as methicillin-resistant S. aureus "
            "(MRSA) is a worldwide problem in clinical medicine.",
    },
    "Staphylococcus aureus (methicillin-susceptible - MSSA)": {
        "gram_stain": "gram+",
        "shape": "coccus.staphylococci",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Staphylococcus aureus is a Gram-positive, round-shaped bacterium "
            "that is a member of the Firmicutes, and it is a usual member of "
            "the microbiota of the body, frequently found in the upper "
            "respiratory tract and on the skin. It is often positive for "
            "catalase and nitrate reduction and is a facultative anaerobe "
            "that can grow without the need for oxygen. Although S. aureus "
            "usually acts as a commensal of the human microbiota it can also "
            "become an opportunistic pathogen, being a common cause of skin "
            "infections including abscesses, respiratory infections such as "
            "sinusitis, and food poisoning. Pathogenic strains often promote "
            "infections by producing virulence factors such as potent protein "
            "toxins, and the expression of a cell-surface protein that binds "
            "and inactivates antibodies.",
    },
    "Staphylococcus lugdenensis": {
        "gram_stain": "gram+",
        "shape": "coccus.staphylococci",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Stenotrophomonas maltophilia": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Streptococcus anginosus group (Milleri)": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Streptococcus dysgalactiae (beta-haemolytic Group C/G)": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Streptococcus agalactiae (beta-haemolytic Group B)": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Streptococcus pneumoniae": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": True,
        "multi_resistant": False,
        "mro_phenotype": "",
        "description":
            "Streptococcus pneumoniae, or pneumococcus, is a Gram-positive, "
            "spherical bacteria, alpha-hemolytic (under aerobic conditions) "
            "or beta-hemolytic (under anaerobic conditions), facultative "
            "anaerobic member of the genus Streptococcus. They are usually "
            "found in pairs (diplococci) and do not form spores and are non "
            "motile. As a significant human pathogenic bacterium "
            "S. pneumoniae was recognized as a major cause of pneumonia in the "
            "late 19th century, and is the subject of many humoral immunity "
            "studies.",
    },
    "Streptococcus pyogenes (beta-haemolytic Group A)": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Streptococcus spp (Viridans group)": {
        "gram_stain": "gram+",
        "shape": "coccus",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Streptococcus suis": {
        "gram_stain": "gram+",
        "shape": "coccus.streptococci",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },
    "Vibrio spp": {
        "gram_stain": "gram-",
        "shape": "rod",
        "glass": False,
        "multi_resistant": False,
        "mro_phenotype": "",
    },


}

MICROORGANISMS_OLD = {
    "Acinetobacter baumannii": {
        "description":
            "Acinetobacter baumannii is a typically short, almost "
            "round, rod-shaped (coccobacillus) Gram-negative bacterium. It is "
            "named after the bacteriologist Paul Baumann. It can be an "
            "opportunistic pathogen in humans, affecting people with "
            "compromised immune systems, and is becoming increasingly "
            "important as a hospital-derived (nosocomial) infection. While "
            "other species of the genus Acinetobacter are often found in soil "
            "samples (leading to the common misconception that A. baumannii is "
            "a soil organism, too), it is almost exclusively isolated from "
            "hospital environments. Although occasionally it has been found "
            "in environmental soil and water samples, its natural habitat "
            "is still not known.",
        "gram_stain": "gram-",
        "glass": False,
        "multi_resistant": True,
    },
    "Pseudomonas aeruginosa": {
        "description":
            "Pseudomonas aeruginosa is a common encapsulated, Gram-negative, "
            "rod-shaped bacterium that can cause disease in plants and "
            "animals, including humans. A species of considerable medical "
            "importance, P. aeruginosa is a multidrug resistant pathogen "
            "recognized for its ubiquity, its intrinsically advanced "
            "antibiotic resistance mechanisms, and its association with "
            "serious illnesses – hospital-acquired infections such as "
            "ventilator-associated pneumonia and various sepsis syndromes.",
        "gram_stain": "gram-",
        "glass": False,
        "multi_resistant": True,
    },
    "Enterococcus faecium": {
        "description":
            "Enterococcus faecium is a Gram-positive, alpha-hemolytic or "
            "non-hemolytic bacterium in the genus Enterococcus. It can be "
            "commensal (innocuous, coexisting organism) in the "
            "gastrointestinal tract of humans and animals, but it may also "
            "be pathogenic, causing diseases such as neonatal meningitis or "
            "endocarditis. Vancomycin-resistant E. faecium is often referred "
            "to as VRE.",
        "gram_stain": "gram+",
        "glass": False,
        "multi_resistant": True,
    },
    "Staphylococcus aureus": {
        "description":
            "Staphylococcus aureus is a Gram-positive, round-shaped bacterium "
            "that is a member of the Firmicutes, and it is a usual member of "
            "the microbiota of the body, frequently found in the upper "
            "respiratory tract and on the skin. It is often positive for "
            "catalase and nitrate reduction and is a facultative anaerobe "
            "that can grow without the need for oxygen. Although S. aureus "
            "usually acts as a commensal of the human microbiota it can also "
            "become an opportunistic pathogen, being a common cause of skin "
            "infections including abscesses, respiratory infections such as "
            "sinusitis, and food poisoning. Pathogenic strains often promote "
            "infections by producing virulence factors such as potent protein "
            "toxins, and the expression of a cell-surface protein that binds "
            "and inactivates antibodies. The emergence of antibiotic-resistant "
            "strains of S. aureus such as methicillin-resistant S. aureus "
            "(MRSA) is a worldwide problem in clinical medicine. Despite much "
            "research and development, no vaccine for S. aureus has been "
            "approved.",
        "gram_stain": "gram+",
        "glass": True,
        "multi_resistant": True,
    },
    "Helicobacter pylori": {
        "description":
            "Helicobacter pylori, previously known as Campylobacter pylori, is "
            "a gram-negative, microaerophilic, spiral (helical) bacterium "
            "usually found in the stomach. Its helical shape (from which "
            "the genus name, helicobacter, derives) is thought to have evolved "
            "in order to penetrate the mucoid lining of the stomach and "
            "thereby establish infection. The bacterium was first identified "
            "in 1982 by Australian doctors Barry Marshall and Robin Warren. "
            "H. pylori has been associated with the mucosa-associated lymphoid "
            "tissue in the stomach, esophagus, colon, rectum, or tissues "
            "around the eye (termed extranodal marginal zone B-cell lymphoma "
            "of the cited organ), and of lymphoid tissue in the stomach "
            "(termed diffuse large B-cell lymphoma).",
        "gram_stain": "gram-",
        "glass": False,
        "multi_resistant": False,
    },
    "Salmonella spp": {
        "description":
            "Salmonella is a genus of rod-shaped (bacillus) Gram-negative "
            "bacteria of the family Enterobacteriaceae. The two species of "
            "Salmonella are Salmonella enterica and Salmonella bongori. "
            "S. enterica is the type species and is further divided into six "
            "subspecies that include over 2,600 serotypes. Salmonella was "
            "named after Daniel Elmer Salmon (1850–1914), an American "
            "veterinary surgeon.",
        "gram_stain": "gram-",
        "glass": True,
        "multi_resistant": False,
    },
    "Neisseria gonorrhoeae": {
        "description":
            "Neisseria gonorrhoeae, also known as gonococcus (singular), or "
            "gonococci (plural) is a species of Gram-negative diplococci "
            "bacteria isolated by Albert Neisser in 1879. It causes the "
            "sexually transmitted genitourinary infection gonorrhea as well "
            "as other forms of gonococcal disease including disseminated "
            "gonococcemia, septic arthritis, and gonococcal ophthalmia "
            "neonatorum.",
        "gram_stain": "gram-",
        "glass": True,
        "multi_resistant": False,
    },
    "Streptococcus pneumoniae": {
        "description":
            "Streptococcus pneumoniae, or pneumococcus, is a Gram-positive, "
            "spherical bacteria, alpha-hemolytic (under aerobic conditions) "
            "or beta-hemolytic (under anaerobic conditions), facultative "
            "anaerobic member of the genus Streptococcus. They are usually "
            "found in pairs (diplococci) and do not form spores and are non "
            "motile. As a significant human pathogenic bacterium "
            "S. pneumoniae was recognized as a major cause of pneumonia in the "
            "late 19th century, and is the subject of many humoral immunity "
            "studies.",
        "gram_stain": "gram+",
        "glass": True,
        "multi_resistant": True,
    },
    "Haemophilus influenzae": {
        "description":
            "Haemophilus influenzae (formerly called Pfeiffer's bacillus or "
            "Bacillus influenzae) is a Gram-negative, coccobacillary, "
            "facultatively anaerobic capnophilic pathogenic bacterium of the "
            "family Pasteurellaceae. H. influenzae was first described in 1892 "
            "by Richard Pfeiffer during an influenza pandemic",
        "gram_stain": "gram-",
        "glass": False,
        "multi_resistant": False,
    },
    "Shigella spp": {
        "description":
            "Shigella is a genus of bacteria that is Gram-negative, "
            "facultative anaerobic, non-spore-forming, nonmotile, rod-shaped "
            "and genetically closely related to E. coli. The genus is named "
            "after Kiyoshi Shiga, who first discovered it in 1897.",
        "gram_stain": "gram-",
        "glass": True,
        "multi_resistant": False,
    },
    "Enterobacter cloacae": {
        "description":
            "Enterobacter cloacae is a clinically significant Gram-negative, "
            "facultatively-anaerobic, rod-shaped bacterium. E. cloacae is "
            "frequently grown at 30 °C on nutrient agar or broth or at 35 °C "
            "in tryptic soy broth. It is a rod-shaped, Gram-negative "
            "bacterium, is facultatively anaerobic, and bears peritrichous "
            "flagella. It is oxidase-negative and catalase-positive. "
            "Source: https://en.wikipedia.org/wiki/Enterobacter_cloacae",
        "gram_stain": "gram-",
        "glass": False,
        "multi_resistant": True,
    },
    "Klebsiella pneumoniae": {
        "description":
            "Klebsiella pneumoniae is a Gram-negative, non-motile, "
            "encapsulated, lactose-fermenting, facultative anaerobic, "
            "rod-shaped bacterium. It appears as a mucoid lactose fermenter on "
            "MacConkey agar. Although found in the normal flora of the mouth, "
            "skin, and intestines, it can cause destructive changes to human "
            "and animal lungs if aspirated, specifically to the alveoli "
            "resulting in bloody, brownish or yellow colored jelly like "
            "sputum. In the clinical setting, it is the most significant "
            "member of the genus Klebsiella of the Enterobacteriaceae. "
            "K. oxytoca and K. rhinoscleromatis have also been demonstrated in "
            "human clinical specimens. In recent years, Klebsiella species "
            "have become important pathogens in nosocomial infections. It "
            "naturally occurs in the soil, and about 30% of strains can fix "
            "nitrogen in anaerobic conditions. As a free-living diazotroph, "
            "its nitrogen-fixation system has been much-studied, and is of "
            "agricultural interest, as K. pneumoniae has been demonstrated to "
            "increase crop yields in agricultural conditions. It is closely "
            "related to K. oxytoca from which it is distinguished by being "
            "indole-negative and by its ability to grow on melezitose but not "
            "3-hydroxybutyrate. "
            "Source: https://en.wikipedia.org/wiki/Klebsiella_pneumoniae",
        "gram_stain": "gram-",
        "glass": True,
        "multi_resistant": True,
    }
}

# List of default antibiotics to create on install
# Tuples of (antibiotic name, antibiotic properties)
ANTIBIOTICS = [
    ("Ampicillin", {
        "abbreviation": "Amp",
        "antibiotic_class": _sa("Penicillins"),
        "description":
            "Ampicillin is an antibiotic used to prevent and treat a number of "
            "bacterial infections, such as respiratory tract infections, "
            "urinary tract infections, meningitis, salmonellosis, and "
            "endocarditis. It may also be used to prevent group B "
            "streptococcal infection in newborns. It is used by mouth, by "
            "injection into a muscle, or intravenously. Common side effects "
            "include rash, nausea, and diarrhea. It should not be used in "
            "people who are allergic to penicillin. Serious side effects "
            "may include Clostridium difficile colitis or anaphylaxis. While "
            "usable in those with kidney problems, the dose may need to be "
            "decreased. Its use during pregnancy and breastfeeding appears "
            "to be generally safe. Source: https://en.wikipedia.org/wiki/Ampicillin",
    }),
    ("Amoxy + clavulanate", {
        "abbreviation": "Amc",
        "antibiotic_class": _sa("Penicillins"),
        "description":
            "Amoxicillin/clavulanic acid, also known as co-amoxiclav, is an "
            "antibiotic useful for the treatment of a number of bacterial "
            "infections. It is a combination consisting of amoxicillin, a "
            "β-lactam antibiotic, and potassium clavulanate, a β-lactamase "
            "inhibitor. It is specifically used for otitis media, strep "
            "throat, pneumonia, cellulitis, urinary tract infections, and "
            "animal bites. It is taken by mouth or by injection into a vein. "
            "Common side effects include diarrhea, vomiting, and allergic "
            "reactions.It also increases the risk of yeast infections, "
            "headaches, and blood clotting problems.It is not recommended in "
            "people with a history of a penicillin allergy. It is relatively "
            "safe for use during pregnancy. Source: "
            "https://en.wikipedia.org/wiki/Amoxicillin/clavulanic_acid",
    }),
    ("Ceftriaxone", {
        "abbreviation": "Cro",
        "antibiotic_class": _sa("Cephalosporins"),
        "description":
            "Ceftriaxone, sold under the brand name Rocephin, is an antibiotic "
            "used for the treatment of a number of bacterial infections. These "
            "include middle ear infections, endocarditis, meningitis, "
            "pneumonia, bone and joint infections, intra-abdominal infections, "
            "skin infections, urinary tract infections, gonorrhea, and pelvic "
            "inflammatory disease. It is also sometimes used before surgery "
            "and following a bite wound to try to prevent infection. "
            "Ceftriaxone can be given by injection into a vein or into a "
            "muscle. Common side effects include pain at the site of injection "
            "and allergic reactions. Other possible side effects include C. "
            "difficile associated diarrhea, hemolytic anemia, gall bladder "
            "disease, and seizures. It is not recommended in those who have "
            "had anaphylaxis to penicillin but may be used in those who have "
            "had milder reactions. The intravenous form should not be given "
            "with intravenous calcium. There is tentative evidence that "
            "ceftriaxone is relatively safe during pregnancy and "
            "breastfeeding. It is a third-generation cephalosporin that works "
            "by preventing bacteria from making a cell wall. Source "
            "https://en.wikipedia.org/wiki/Ceftriaxone",
    }),
    ("Gentamicin", {
        "abbreviation": "Cn",
        "antibiotic_class": _sa("Aminoglycosides"),
        "description":
            "Gentamicin, sold under brand name Garamycin among others, is an "
            "antibiotic used to treat several types of bacterial infections. "
            "This may include bone infections, endocarditis, pelvic "
            "inflammatory disease, meningitis, pneumonia, urinary tract "
            "infections, and sepsis among others. It is not effective for "
            "gonorrhea or chlamydia infections. It can be given intravenously, "
            "by injection into a muscle, or topically. Topical formulations "
            "may be used in burns or for infections of the outside of the "
            "eye. In the developed world, it is often only used for two days "
            "until bacterial cultures determine what specific antibiotics the "
            "infection is sensitive to. The dose required should be monitored "
            "by blood testing. Gentamicin can cause inner ear problems and "
            "kidney problems. The inner ear problems can include problems with "
            "balance and hearing loss. These problems may be permanent. If "
            "used during pregnancy, it can cause harm to the developing baby. "
            "However, it appears to be safe for use during breastfeeding. "
            "Gentamicin is a type of aminoglycoside. It works by disrupting "
            "the ability of the bacteria to make proteins, which typically "
            "kills the bacteria. Source: https://en.wikipedia.org/wiki/Gentamicin",
    }),
    ("Norfloxacin", {
        "abbreviation": "Nor",
        "antibiotic_class": _sa("Aminoglycosides"),
        "description":
            "Norfloxacin, sold under the brand name Noroxin among others, is "
            "an antibiotic that belongs to the class of fluoroquinolone "
            "antibiotics. It is used to treat urinary tract infections, "
            "gynecological infections, inflammation of the prostate gland, "
            "gonorrhea and bladder infection. Eye drops were approved for use "
            "in children older than one year of age. Norfloxacin is associated "
            "with a number of rare serious adverse reactions as well as "
            "spontaneous tendon ruptures and irreversible peripheral "
            "neuropathy. Tendon problems may manifest long after therapy had "
            "been completed and in severe cases may result in lifelong "
            "disabilities. Source: https://en.wikipedia.org/wiki/Norfloxacin",
    }),
    ("Ciprofloxacin", {
        "abbreviation": "Cip",
        "antibiotic_class": _sa("Fluoroquinolones"),
        "description":
            "Ciprofloxacin is an antibiotic used to treat a number of "
            "bacterial infections. This includes bone and joint infections, "
            "intra abdominal infections, certain type of infectious diarrhea, "
            "respiratory tract infections, skin infections, typhoid fever, and "
            "urinary tract infections, among others. For some infections it is "
            "used in addition to other antibiotics. It can be taken by mouth, "
            "as eye drops, as ear drops, or intravenously. Common side effects "
            "include nausea, vomiting, diarrhea and rash. Severe side effects "
            "include an increased risk of tendon rupture, hallucinations, and "
            "nerve damage. In people with myasthenia gravis, there is "
            "worsening muscle weakness. Rates of side effects appear to be "
            "higher than some groups of antibiotics such as cephalosporins but "
            "lower than others such as clindamycin. Studies in other animals "
            "raise concerns regarding use in pregnancy. No problems were "
            "identified, however, in the children of a small number of women "
            "who took the medication. It appears to be safe during "
            "breastfeeding. It is a second-generation fluoroquinolone with a "
            "broad spectrum of activity that usually results in the death of "
            "the bacteria. Source: https://en.wikipedia.org/wiki/Ciprofloxacin",
    }),
    ("Nitrofurantoin", {
        "abbreviation": "F",
        "antibiotic_class": _sa("Other"),
        "description":
            "Nitrofurantoin, sold under the brand name Macrobid among others, "
            "is an antibiotic medication used to treat bladder infections, ear "
            "infections, and minor skin infections, but is not as effective "
            "for kidney infections. It is taken by mouth. Common side "
            "effects include nausea, loss of appetite, diarrhea, and "
            "headaches. Rarely numbness, lung problems, or liver problems may "
            "occur. It should not be used in people with kidney problems. "
            "While it appears to be generally safe during pregnancy it should "
            "not be used near delivery. While it usually works by slowing "
            "bacterial growth, it may result in bacterial death at the high "
            "concentrations found in urine. "
            "Source: https://en.wikipedia.org/wiki/Nitrofurantoin",
    }),
    ("Sulph/trimethoprim", {
        "abbreviation": "Sxt",
        "antibiotic_class": _sa("Other"),
        "description":
            "Trimethoprim/sulfamethoxazole (TMP/SMX), also known as "
            "co-trimoxazole among other names, is an antibiotic used to treat "
            "a variety of bacterial infections. It consists of one part "
            "trimethoprim to five parts sulfamethoxazole. It is used for "
            "urinary tract infections, methicillin-resistant Staphylococcus "
            "aureus (MRSA) skin infections, travelers' diarrhea, respiratory "
            "tract infections, and cholera, among others. It may be used both "
            "to treat and prevent pneumocystis pneumonia and toxoplasmosis in "
            "people with HIV/AIDS and other causes of immunosuppression. It "
            "can be given by mouth or intravenously. Common side effects "
            "include nausea, vomiting, rash, and diarrhea. Severe allergic "
            "reactions and Clostridium difficile diarrhea may occasionally "
            "occur. Its use in pregnancy is not recommended. It appears to be "
            "safe for use during breastfeeding as long as the baby is healthy. "
            "TMP/SMX generally results in bacterial death. It works by "
            "blocking the making and use of folate by the microorganisms. "
            "Source: https://en.wikipedia.org/wiki/Trimethoprim/sulfamethoxazole",
    }),
    ("Meropenem", {
        "abbreviation": "Mem",
        "antibiotic_class": _sa("Carbapenems"),
        "description":
            "Meropenem, sold under the brandname Merrem among others, is a "
            "broad-spectrum antibiotic used to treat a variety of bacterial "
            "infections. Some of these include meningitis, intra-abdominal "
            "infection, pneumonia, sepsis, and anthrax. It is given by "
            "injection into a vein. Common side effects include nausea, "
            "diarrhea, constipation, headache, rash, and pain at the site of "
            "injection. Serious side effects include Clostridium difficile "
            "infection, seizures, and allergic reactions including "
            "anaphylaxis. Those who are allergic to other β-lactam antibiotics "
            "are more likely to be allergic to meropenem as well. Use in "
            "pregnancy appears to be safe. It is in the carbapenem family of "
            "medications. Meropenem usually results in bacterial death through "
            "blocking their ability to make a cell wall. It is more resistant "
            "to breakdown by β-lactamase producing bacteria. "
            "Source: https://en.wikipedia.org/wiki/Meropenem"
    }),
    ("Ceftazidime", {
        "abbreviation": "Caz",
        "antibiotic_class": _sa("Cephalosporins"),
        "description":
            "Ceftazidime, sold under the brand names Fortaz among others, is "
            "an antibiotic useful for the treatment of a number of bacterial "
            "infections. Specifically it is used for joint infections, "
            "meningitis, pneumonia, sepsis, urinary tract infections, "
            "malignant otitis externa, Pseudomonas aeruginosa infection, and "
            "vibrio infection. It is given by injection into a vein, muscle, "
            "or eye. Common side effects include nausea, allergic reactions, "
            "and pain at the site of injection. Other side effects may "
            "include Clostridium difficile diarrhea. It is not recommended in "
            "people who have had previous anaphylaxis to a penicillin. Its use "
            "is relatively safe during pregnancy and breastfeeding. It is in "
            "the third-generation cephalosporin family of medications and "
            "works by interfering with the bacteria's cell wall. "
            "Source: https://en.wikipedia.org/wiki/Ceftazidime"
    }),
    ("Piperacillin + tazobactam", {
        "abbreviation": "Tzp",
        "antibiotic_class": _sa("Penicillins"),
        "description":
            "Piperacillin/tazobactam, sold under the brand names Zosyn among "
            "others, is a combination medication containing the antibiotic "
            "piperacillin and the β-lactamase inhibitor tazobactam. The "
            "combination has activity against many Gram-positive and "
            "Gram-negative bacteria including Pseudomonas aeruginosa. It is "
            "used to treat pelvic inflammatory disease, intra-abdominal "
            "infection, pneumonia, cellulitis, and sepsis. It is given by "
            "injection into a vein. Common adverse effects include headache, "
            "trouble sleeping, rash, nausea, constipation, and diarrhea. "
            "Serious adverse effects include Clostridium difficile infection "
            "and allergic reactions including anaphylaxis. Those who are "
            "allergic to other β-lactam are more likely to be allergic to "
            "piperacillin/tazobactam. Use in pregnancy or breastfeeding "
            "appears to generally be safe. It usually results in bacterial "
            "death through blocking their ability to make a cell wall. "
            "Source: https://en.wikipedia.org/wiki/Piperacillin/tazobactam"
    }),
    ("Amikacin", {
        "abbreviation": "Ak",
        "antibiotic_class": _sa("Aminoglycosides"),
        "description":
            "Amikacin is an antibiotic medication used for a number of "
            "bacterial infections. This includes joint infections, "
            "intra-abdominal infections, meningitis, pneumonia, sepsis, and "
            "urinary tract infections. It is also used for the treatment of "
            "multidrug-resistant tuberculosis. It is used by injection into a "
            "vein using an IV or into a muscle.  Amikacin, like other "
            "aminoglycoside antibiotics, can cause hearing loss, balance "
            "problems, and kidney problems. Other side effects include "
            "paralysis, resulting in the inability to breathe. If used during "
            "pregnancy it may cause permanent deafness in the baby. Amikacin "
            "works by blocking the function of the bacteria's 30S ribosomal "
            "subunit, making it unable to produce proteins. "
            "Source: https://en.wikipedia.org/wiki/Amikacin"
    }),
    ("Chloramphenicol", {
        "abbreviation": "C",
        "antibiotic_class": _sa("Other"),
        "description":
            "Chloramphenicol is an antibiotic useful for the treatment of a "
            "number of bacterial infections. This includes use as an eye "
            "ointment to treat conjunctivitis. By mouth or by injection into a "
            "vein, it is used to treat meningitis, plague, cholera, and typhoid "
            "fever. Its use by mouth or by injection is only recommended when "
            "safer antibiotics cannot be used. Monitoring both blood levels of "
            "the medication and blood cell levels every two days is "
            "recommended during treatment. Common side effects include bone "
            "marrow suppression, nausea, and diarrhea. The bone marrow "
            "suppression may result in death. To reduce the risk of side "
            "effects treatment duration should be as short as possible. "
            "People with liver or kidney problems may need lower doses. In "
            "young children a condition known as gray baby syndrome may occur "
            "which results in a swollen stomach and low blood pressure. Its "
            "use near the end of pregnancy and during breastfeeding is "
            "typically not recommended. Chloramphenicol is a broad-spectrum "
            "antibiotic that typically stops bacterial growth by stopping the "
            "production of proteins. "
            "Source: https://en.wikipedia.org/wiki/Chloramphenicol"
    }),
    ("Tetracycline", {
        "abbreviation": "Te",
        "antibiotic_class": _sa("Tetracyclines"),
        "description":
            "Tetracycline, sold under the brand name Sumycin among others, is "
            "an antibiotic used to treat a number of infections. This includes "
            "acne, cholera, brucellosis, plague, malaria, and syphilis. It is "
            "taken by mouth. Common side effects include vomiting, diarrhea, "
            "rash, and loss of appetite. Other side effects include poor tooth "
            "development if used by children less than eight years of age, "
            "kidney problems, and sunburning easily. Use during pregnancy "
            "may harm the baby. Tetracycline is in the tetracyclines family of "
            "medications. It works by blocking the ability of bacteria to make "
            "proteins. "
            "Source: https://en.wikipedia.org/wiki/Tetracycline"
    }),
    ("Pefloxacin", {
        "abbreviation": "Pef",
        "antibiotic_class": _sa("Fluoroquinolones"),
        "description":
            "Pefloxacin is a broad-spectrum antibiotic that is active against "
            "both Gram-positive and Gram-negative bacteria. It functions by "
            "inhibiting DNA gyrase, a type II topoisomerase, and topoisomerase "
            "IV, which is an enzyme necessary to separate, replicated DNA, "
            "thereby inhibiting cell division. Tendinitis and rupture, usually "
            "of the Achilles tendon, are class-effects of the "
            "fluoroquinolones, most frequently reported with pefloxacin. "
            "Source: https://en.wikipedia.org/wiki/Pefloxacin"
    }),
    ("Cefoxitin", {
        "abbreviation": "Fox",
        "antibiotic_class": _sa("Cephalosporins"),
        "description":
            "Cefoxitin is a second-generation cephamycin antibiotic developed "
            "by Merck & Co., Inc. from Cephamycin C in the year following its "
            "discovery, 1972. It was synthesized in order to create an "
            "antibiotic with a broader spectrum. It is often grouped with "
            "the second-generation cephalosporins. Cefoxitin is a beta-lactam "
            "antibiotic which binds to penicillin binding proteins, or "
            "transpeptidases. By binding to PBPs, cefoxitin prevents the PBPs "
            "from forming the cross-linkages between the peptidoglycan layers "
            "that make up the bacterial cell wall, thereby interfering with "
            "cell wall synthesis. It is a strong beta-lactamase inducer, as "
            "are certain other antibiotics (such as imipenem). However, "
            "cefoxitin is a better substrate than imipenem for beta-lactamases."
            " Source: https://en.wikipedia.org/wiki/Cefoxitin"
    }),
    ("Erythromycin", {
        "abbreviation": "E",
        "antibiotic_class": _sa("Macrolides"),
        "description":
            "Erythromycin is an antibiotic used for the treatment of a number "
            "of bacterial infections. This includes respiratory tract "
            "infections, skin infections, chlamydia infections, pelvic "
            "inflammatory disease, and syphilis. It may also be used during "
            "pregnancy to prevent Group B streptococcal infection in the "
            "newborn, as well as to improve delayed stomach emptying. It "
            "can be given intravenously and by mouth. An eye ointment is "
            "routinely recommended after delivery to prevent eye infections in "
            "the newborn. Common side effects include abdominal cramps, "
            "vomiting, and diarrhea. More serious side effects may include "
            "Clostridium difficile colitis, liver problems, prolonged QT, and "
            "allergic reactions. It is generally safe in those who are "
            "allergic to penicillin. Erythromycin also appears to be safe to "
            "use during pregnancy. While generally regarded as safe during "
            "breastfeeding, its use by the mother during the first two weeks "
            "of life may increase the risk of pyloric stenosis in the baby. "
            "This risk also applies if taken directly by the baby during this "
            "age. It is in the macrolide family of antibiotics and works by "
            "decreasing bacterial protein production. "
            "Source: https://en.wikipedia.org/wiki/Erythromycin"
    }),
    ("Oxacillin", {
        "abbreviation": "Ox",
        "antibiotic_class": _sa("Penicillins"),
        "description":
            "Oxacillin is a penicillinase-resistant β-lactam. It is similar to "
            "methicillin, and has replaced methicillin in clinical use. Other "
            "related compounds are nafcillin, cloxacillin, dicloxacillin, and "
            "flucloxacillin. Since it is resistant to penicillinase enzymes, "
            "such as that produced by Staphylococcus aureus, it is widely used "
            "clinically in the US to treat penicillin-resistant Staphylococcus "
            "aureus. However, with the introduction and widespread use of both "
            "oxacillin and methicillin, antibiotic-resistant strains called "
            "methicillin-resistant and oxacillin-resistant Staphylococcus "
            "aureus (MRSA/ORSA) have become increasingly prevalent worldwide. "
            "MRSA/ORSA can be treated with vancomycin or other new "
            "antibiotics. The use of oxacillin is contraindicated in "
            "individuals that have experienced a hypersensitivity reaction to "
            "any medication in the penicillin family of antibiotics. "
            "Cross-allergenicity has been documented in individuals taking "
            "oxacillin that experienced a previous hypersensitivity reaction "
            "when given cephalosporins and cephamycins. Commonly reported "
            "adverse effects associated with the use of oxacillin include skin "
            "rash, diarrhea, nausea, vomiting, hematuria, agranulocytosis, "
            "eosinophilia, leukopenia, neutropenia, thrombocytopenia, "
            "hepatotoxicity, acute interstitial nephritis, and fever. High "
            "doses of oxacillin have been reported to cause renal, hepatic, "
            "and nervous system toxicity. Common to all members of the "
            "penicillin class of drugs, oxacillin may cause acute or delayed "
            "hypersensitivity reactions. As an injection, oxacillin may cause "
            "injection site reactions, which may be characterized by redness, "
            "swelling, and itching. "
            "Source: https://en.wikipedia.org/wiki/Oxacillin"
    }),
    ("Vancomycin", {
        "abbreviation": "Va",
        "antibiotic_class": _sa("Other"),
        "description":
            "Vancomycin is an antibiotic used to treat a number of bacterial "
            "infections. It is recommended intravenously as a treatment for "
            "complicated skin infections, bloodstream infections, "
            "endocarditis, bone and joint infections, and meningitis caused by "
            "methicillin-resistant Staphylococcus aureus. Blood levels may be "
            "measured to determine the correct dose. Vancomycin is also "
            "recommended by mouth as a treatment for severe Clostridium "
            "difficile colitis. When taken by mouth it is very poorly "
            "absorbed. Common side effects include pain in the area of "
            "injection and allergic reactions. Occasionally, hearing loss, "
            "low blood pressure, or bone marrow suppression occur. Safety in "
            "pregnancy is not clear, but no evidence of harm has been found, "
            "and it is likely safe for use when breastfeeding. It is a type "
            "of glycopeptide antibiotic and works by blocking the construction "
            "of a cell wall. "
            "Source: https://en.wikipedia.org/wiki/Vancomycin"
    }),
]

# List of default AST Panels to create on install
# Tuples of (ast panel name, panel properties)
AST_PANELS = [
    ("Gram negative panel", {
        "microorganisms": [
            "Acinetobacter baumannii",
            "Acinetobacter baumannii (meropenem-resistant)",
            "Pseudomonas aeruginosa",
            "Salmonella spp",
            "Neisseria gonorrhoeae",
            "Haemophilus influenzae",
            "Shigella spp",
            "Klebsiella pneumoniae",
            "Klebsiella pneumoniae (ceftriaxone-resistant - ESBL)",
            "Klebsiella pneumoniae (meropenem-resistant - CRE)",
            "Enterobacter cloacae",
        ],
        "antibiotics": [
            "Ampicillin",
            "Amoxy + clavulanate",
            "Ceftriaxone",
            "Gentamicin",
            "Norfloxacin",
            "Ciprofloxacin",
            "Nitrofurantoin",
            "Sulph/trimethoprim",
            "Meropenem",
            "Ceftazidime",
            "Piperacillin + tazobactam",
            "Amikacin",
            "Chloramphenicol",
            "Tetracycline",
            "Pefloxacin",
        ],
    }),
    ("Gram positive panel", {
        "microorganisms": [
            "Enterococcus faecium",
            "Enterococcus faecium (Vancomycin-resistant - VRE)",
            "Staphylococcus aureus",
            "Staphylococcus aureus (Methicillin-resistant - MRSA)",
            "Staphylococcus aureus (methicillin-susceptible - MSSA)",
            "Streptococcus pneumoniae"
        ],
        "antibiotics": [
            "Cefoxitin",
            "Chloramphenicol",
            "Erythromycin",
            "Sulph/trimethoprim",
            "Tetracycline",
            "Oxacillin",
            "Ampicillin",
            "Vancomycin",
            "Nitrofurantoin",
        ],
    }),
]

# List of default Wards to create on install
# Tuples of (ward name, description)
WARDS = [
    ("Anaesthetics", {
        "description": "Anaesthetics",
    }),
    ("Ear, Nose and Throat (ENT)", {
        "description": "Ear, Nose and Throat (ENT)",
    }),
    ("Emergency", {
        "description": "Emergency",
    }),
    ("Intensive Care", {
        "description": "Intensive Care",
    }),
    ("Medicine", {
        "description": "Medicine",
    }),
    ("Neurosurgery", {
        "description": "Neurosurgery",
    }),
    ("Obstetrics & Gynaecology", {
        "description": "Obstetrics & Gynaecology",
    }),
    ("Orthopaedics", {
        "description": "Orthopaedics",
    }),
    ("Paediatrics", {
        "description": "Paediatrics",
    }),
    ("Pathology", {
        "description": "Pathology",
    }),
    ("Physiotherapy", {
        "description": "Physiotherapy",
    }),
    ("Psychiatry", {
        "description": "Psychiatry",
    }),
    ("Radiology", {
        "description": "Radiology",
    }),
    ("Surgery", {
        "description": "Surgery",
    }),
]

# List of default Sample Types to create on install
# Tuples of (Sample Type name, properties)
SAMPLE_TYPES = [
    ("Whole Blood", {
        "prefix": "WBL",
        "hazardous": True,
        "container_widget": "bottles",
        "minimum_volume": "10 mL",
        "description":
            "Thick, viscous liquid. Dark red in absence of oxygen, bright red "
            "in presence of oxygen. Blood is normally sterile but may contain "
            "infectious agents such as HIV, hepatitis B, hepatitis C and "
            "syphilis. Never freeze as this lyses the red blood cells. Usually "
            "4-8°C. Reasons for collection: To detect bacteria (bacteraemia, "
            "septicaemia), viruses (viraemia) or antibodies in the blood "
            "(serology)."
    }),
    ("Plasma", {
        "prefix": "PLA",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Watery part of blood left when red blood cells (RBCs) are spun "
            "out. Light straw yellow in colour, usually clear but may be "
            "turbid or milky after a fatty meal. Will clot, as it contains "
            "fibrin. Usually frozen or 4-8°C. Reasons for collection: To "
            "detect bacteria (bacteraemia, septicaemia), viruses (viraemia) or "
            "antibodies in the blood (serology)."
    }),
    ("Serum", {
        "prefix": "SER",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "What is left after the fibrin in plasma clots. Looks like plasma."
            "For drug analyses or legal blood alcohol, strict handling and "
            "legislative protocols may need to be followed. Usually frozen or "
            "4-8°C. Reasons for collection: To detect bacteria (bacteraemia, "
            "septicaemia), viruses (viraemia) or antibodies in the blood "
            "(serology)."
    }),
    ("Urine", {
        "prefix": "URI",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Mid-stream samples are usually clear, watery, non-viscous liquid. "
            "Colour can vary but is usually pale to dark yellow in colour. "
            "Total urine samples can be cloudy and turbid indicating the "
            "presence of cells. A mid-stream urine sample would usually be "
            "relatively free of microbes. For drug analyses, strict handling "
            "and legislative protocols may need to be followed. Usually 4-8°C."
            "Reasons for collection: To detect bacteria in the urine "
            "(bacteruria), casts in the urine (rafts of cells), red or white "
            "blood cells that may indicate infection, or crystals."
    }),
    ("Faeces", {
        "prefix": "FAE",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Highly variable in appearance, but generally the stool should be "
            "firm unless diarrhoea is present. Colour is dependent on diet and "
            "disease processes but ranges from black to brown to yellow to "
            "white. Smell is usually bad!. Usually 4-8°C. Reasons for "
            "collection: To detect specific bacterial, viral or parasites in "
            "the faeces."
    }),
    ("Cerebrospinal Fluid (CSF)", {
        "prefix": "CSF",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Usually a clear liquid. May contain blood as a result of the "
            "collection process or be cloudy if bacteria are present in the "
            "CSF. CSF is normally sterile. Usually 4-8°C. Reasons for "
            "collection: To detect bacteria (septic meningitis) or viruses "
            "(aseptic meningitis) in the CSF."
    }),
    ("Sputum", {
        "prefix": "SPU",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Viscous fluid or suspension, usually clear to milky. Infection is "
            "often denoted by a yellow or green colour. Treat mucus or sputum "
            "from a tubercular patient with special care to avoid aerosols."
            "Usually 4-8°C. Reasons for collection: Usually collected if "
            "pneumonia or a respiratory tract infection is suspected."
    }),
    ("Aspirates", {
        "prefix": "ASP",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Pleural aspirates (lung) are usually clear to milky. Gastric "
            "secretions (stomach) are yellow to greenish-brown with the "
            "possibility of suspended material. Peritoneal aspirates "
            "(abdominal cavity) come in various colours. Synovial (joint) and "
            "amniotic (foetal) fluids are clear and watery. Handle to avoid "
            "spills. Usually 4-8°C. Reasons for collection: Looking for "
            "evidence of microbial infection."
    }),
    ("Sweat", {
        "prefix": "SWE",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Clear to milky liquid but usually absorbed on paper or a swab. "
            "Sample may be very small - treat carefully. Usually 4-8°C. "
            "Reasons for collection: Not usually collected for microbiology. "
            "May be used to analyse salts (Na, K, Cl) to diagnose cystic "
            "fibrosis."
    }),
    ("Semen", {
        "prefix": "SEM",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Clear to milky viscous liquid. May be kept warm prior to "
            "immediate analysis. Long-term storage will require special "
            "diluents and storage at -196°C(liquid nitrogen). Samples stored "
            "at -196°C are a potential cold burn hazard. Reasons for "
            "collection: To detect infertile conditions and to check "
            "post-vasectomy status."
    }),
    ("Biopsy", {
        "prefix": "BIO",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Variable appearance and usually small. Removed during surgery. "
            "Samples are small, easy to contaminate and usually sent for "
            "testing in sterile saline to prevent drying out. Usually 4-8°C or "
            "frozen. Reasons for collection: Usually collected to check for "
            "malignancies but biopsies may occasionally be used for "
            "microbiology."
    }),
    ("Cell Smears", {
        "prefix": "SME",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Often presented on a glass microscope slide. Blood smears appear "
            "red whilst other smears are usually white. Slides are fragile and "
            "should not be dropped. Often dry at room temperature but may need "
            "to be stored at lower temperatures. Often dry at room temperature "
            "but may need to be stored at lower temperatures. Reasons for "
            "collection: Pap smears, blood-borne parasitic infections (eg "
            "malaria), DNA testing, tinea/ringworm (dermatophyte fungi)."
    }),
    ("Hair", {
        "prefix": "HAI",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Often presented in specimen bags or jars. Small amounts are "
            "easily lost - treat carefully. Room temperature. Reasons for "
            "collection: May be used for heavy metal analysis but in "
            "microbiology hair is most often collected to check for "
            "dermatophyte fungal infections of hair."
    }),
    ("Nail fragments", {
        "prefix": "NAI",
        "hazardous": True,
        "container_widget": "container",
        "minimum_volume": "10 mL",
        "description":
            "Often presented in specimen bags or jars. Small amounts are "
            "easily lost - treat carefully. Room temperature. Reasons for "
            "collection: Usually used to check for dermatophyte fungal "
            "infections of the nails (tinea)."
    }),
]

# List of default Sample Points to create on install
# Tuples of (Sample Point name, properties)
SAMPLE_POINTS = [
    ('Abdomen', {}), 
    ('Anal', {}), 
    ('Ankle', {}), 
    ('Anterior', {}), 
    ('Anterior chamber', {}), 
    ('Aorta', {}), 
    ('Arm', {}), 
    ('Arterial cannula tip', {}), 
    ('Aspirate', {}), 
    ('Axilla', {}), 
    ('Back', {}), 
    ('Bartholins', {}), 
    ('Bile', {}), 
    ('Bile-duct', {}), 
    ('Biopsy', {}), 
    ('Bladder', {}), 
    ('Bone', {}), 
    ('Bowel', {}), 
    ('Brain', {}), 
    ('Breast', {}), 
    ('Bronchial', {}), 
    ('Bursa', {}), 
    ('Buttock', {}), 
    ('Calf', {}), 
    ('Carotid', {}), 
    ('Carpel', {}), 
    ('Central line (implanted) tip', {}), 
    ('Central line (non-tunnelled) tip', {}), 
    ('Central line (tunnelled) tip', {}), 
    ('Cervical (genital)', {}), 
    ('Chest', {}), 
    ('Chin', {}), 
    ('Conjunctiva', {}), 
    ('Cornea', {}), 
    ('Cubital fossa', {}), 
    ('Cyst', {}), 
    ('Ear', {}), 
    ('Elbow', {}), 
    ('Empyema', {}), 
    ('Endometrium', {}), 
    ('Episiotomy', {}), 
    ('Eqa sample', {}), 
    ('Extradural', {}), 
    ('Eye', {}), 
    ('Eye lid', {}), 
    ('Face', {}), 
    ('Fallopian tube', {}), 
    ('Feet', {}), 
    ('Finger', {}), 
    ('Fistula', {}), 
    ('Foot', {}), 
    ('Forearm', {}), 
    ('Gastric', {}), 
    ('Groin', {}), 
    ('Gum', {}), 
    ('Hand', {}), 
    ('Head/neck', {}), 
    ('Heart', {}), 
    ('Heel', {}), 
    ('Hip', {}), 
    ('Ileal', {}), 
    ('In-out catheter sample', {}), 
    ('Indwelling catheter', {}), 
    ('Inferior', {}), 
    ('Infra-lateral', {}), 
    ('Inguinal', {}), 
    ('Inner', {}), 
    ('Intercostal', {}), 
    ('Intra operative', {}), 
    ('Ischiorectal', {}), 
    ('Jugular', {}), 
    ('Kidney', {}), 
    ('Knee', {}), 
    ('Labia', {}), 
    ('Lateral', {}), 
    ('Left', {}), 
    ('Left 1st finger', {}), 
    ('Left 2nd finger', {}), 
    ('Left 2nd toe', {}), 
    ('Left 3rd finger', {}), 
    ('Left 3rd toe', {}), 
    ('Left 4th finger', {}), 
    ('Left 4th toe', {}), 
    ('Left 5th toe', {}), 
    ('Left ankle', {}), 
    ('Left arm', {}), 
    ('Left axilla', {}), 
    ('Left back', {}), 
    ('Left breast', {}), 
    ('Left buttock', {}), 
    ('Left calf', {}), 
    ('Left cheek', {}), 
    ('Left conjunctiva', {}), 
    ('Left cubital fossa', {}), 
    ('Left ear lobe', {}), 
    ('Left eye lash', {}), 
    ('Left eyebrow', {}), 
    ('Left foot', {}), 
    ('Left foot (sole)', {}), 
    ('Left great toe', {}), 
    ('Left hand', {}), 
    ('Left iliac fossa', {}), 
    ('Left index finger', {}), 
    ('Left lower back', {}), 
    ('Left lung', {}), 
    ('Left malleolus', {}), 
    ('Left orbit', {}), 
    ('Left upper back', {}), 
    ('Left wrist', {}), 
    ('Leg', {}), 
    ('Lip', {}), 
    ('Liver', {}), 
    ('Lower', {}), 
    ('Lower left arm', {}), 
    ('Lower left leg', {}), 
    ('Lower leg', {}), 
    ('Lower lip', {}), 
    ('Lower right arm', {}), 
    ('Lower right leg', {}), 
    ('Lumbar', {}), 
    ('Lung', {}), 
    ('Malleolus', {}), 
    ('Mastoid', {}), 
    ('Maxillary', {}), 
    ('Meninges', {}), 
    ('Metatarsal', {}), 
    ('Midline', {}), 
    ('Mouth', {}), 
    ('Nail', {}), 
    ('Nasal', {}), 
    ('Nasopharyngeal', {}), 
    ('Natal cleft', {}), 
    ('Neck', {}), 
    ('Nephrostomy', {}), 
    ('Nipple', {}), 
    ('Nose/groin/perineal', {}), 
    ('Ocular', {}), 
    ('Oesophagus', {}), 
    ('Olecranon', {}), 
    ('Orbit', {}), 
    ('Palm', {}), 
    ('Pancreas', {}), 
    ('Parotid', {}), 
    ('Patellar', {}), 
    ('Peg tube', {}), 
    ('Pelvic', {}), 
    ('Penile', {}), 
    ('Perianal', {}), 
    ('Pericardial', {}), 
    ('Perineal', {}), 
    ('Periorbital', {}), 
    ('Peripheral', {}), 
    ('Peripheral cannula tip', {}), 
    ('Peritoneal', {}), 
    ('Peritoneal dialysis', {}), 
    ('Pharyngeal', {}), 
    ('Pilonidal', {}), 
    ('Pin site (orthopaedic)', {}), 
    ('Placenta', {}), 
    ('Pleural', {}), 
    ('Pressure sore', {}), 
    ('Prostate', {}), 
    ('Proximal', {}), 
    ('Psoas', {}), 
    ('Quinsy', {}), 
    ('Rash', {}), 
    ('Rectal', {}), 
    ('Right 1st finger', {}), 
    ('Right 2nd finger', {}), 
    ('Right 2nd toe', {}), 
    ('Right 3rd finger', {}), 
    ('Right 3rd toe', {}), 
    ('Right 4th finger', {}), 
    ('Right 4th toe', {}), 
    ('Right 5th toe', {}), 
    ('Right arm', {}), 
    ('Right cubital fossa', {}), 
    ('Right ear lobe', {}), 
    ('Right foot', {}), 
    ('Right foot (sole)', {}), 
    ('Right front', {}), 
    ('Right great toe', {}), 
    ('Right hand', {}), 
    ('Right iliac fossa', {}), 
    ('Right index finger', {}), 
    ('Right lower back', {}), 
    ('Right malleolus', {}), 
    ('Right middle ear', {}), 
    ('Right orbit', {}), 
    ('Right upper back', {}), 
    ('Right wrist', {}), 
    ('Sacral', {}), 
    ('Salivary', {}), 
    ('Scalp', {}), 
    ('Screw', {}), 
    ('Scrotal', {}), 
    ('Sebaceous', {}), 
    ('Shin', {}), 
    ('Shoulder', {}), 
    ('Sinus', {}), 
    ('Skin', {}), 
    ('Sputum 1', {}), 
    ('Sputum 2', {}), 
    ('Sputum 3', {}), 
    ('Sternum', {}), 
    ('Stump', {}), 
    ('Subclavian', {}), 
    ('Subdural', {}), 
    ('Submandibular', {}), 
    ('Subphrenic', {}), 
    ('Superior', {}), 
    ('Suprapatellar', {}), 
    ('Suprapubic', {}), 
    ('Synovium', {}), 
    ('Tendon', {}), 
    ('Testis', {}), 
    ('Thigh', {}), 
    ('Throat', {}), 
    ('Thyroid', {}), 
    ('Tibia', {}), 
    ('Toe', {}), 
    ('Tooth socket', {}), 
    ('Tracheostomy', {}), 
    ('Umbilical', {}), 
    ('Upper', {}), 
    ('Upper arm', {}), 
    ('Upper left arm', {}), 
    ('Upper left leg', {}), 
    ('Upper leg', {}), 
    ('Upper right arm', {}), 
    ('Upper right leg', {}), 
    ('Urethra', {}), 
    ('Uterus', {}), 
    ('Vaginal (high)', {}), 
    ('Vascular access (exit) site', {}), 
    ('Ventricular', {}), 
    ('Vertebra', {}), 
    ('Vitreous', {}), 
    ('Vp shunt', {}), 
    ('Vulval', {}), 
    ('Wound', {'description': ''})
]

# List of default Container types to create on install
# Tuples of (Container Type name, properties)
CONTAINER_TYPES = [
    ("Bottle", {
        "bactec": True,
    }),
    ("Tube", {}),
    ("Jar", {}),
    ("Screw capped container", {}),
]

# List of default Containers to create on install
# Tuples of (Container name, properties)
CONTAINERS = [
    ("Aerobic Blood Bottle", {
        "container_type": "Bottle",
        "capacity": "20 mL",
        "dry_weight": "60.5 g",
        "description":
            "Uses: Bacterial/Yeast Culture, Blood"

    }),
    ("Anaerobic Blood Bottle", {
        "container_type": "Bottle",
        "capacity": "20 mL",
        "dry_weight": "65.5 g",
        "description":
            "Uses: Bacterial/Yeast Culture, Blood"

    }),
    ("Pediatric Blood Bottle", {
        "container_type": "Bottle",
        "capacity": "20 mL",
        "dry_weight": "69.5 g",
        "description":
            "Uses: Bacterial/Yeast Culture, Blood"
    }),
    ("Mycolytic (AFB) Blood Bottle", {
        "container_type": "Bottle",
        "capacity": "20 mL",
        "description":
            "Uses: Mycobacterial Culture, Blood/Bone Marrow. Minimum volume of "
            "10 mL"
    }),
    ("Isolator", {
        "container_type": "Tube",
        "capacity": "10 mL",
        "description":
            "Uses: Fungal Culture, Blood, Filamentous"
    }),
    ("Mini Isolator", {
        "container_type": "Tube",
        "capacity": "10 mL",
        "description":
            "Uses: Fungal Culture, Blood, Filamentous"
    }),
    ("Sterile Specimen container", {
        "container_type": "Screw capped container",
        "capacity": "10 mL",
        "description":
            "Uses: Fluid specimens (Aerobic culture, AFB, mycology, virology). "
            "Tissue (Aerobic culture, AFB, Mycology, Virology). Hardware. "
            "Stool - C. difficile toxin B Gene Nucleic Acid Test. Stool - "
            "H.pylori Antigen, EIA, Stool. Stool - Norovirus Nucleic Acid Test"
    }),
    ("Carey Blair Stool container", {
        "container_type": "Screw capped container",
        "capacity": "10 mL",
        "description":
            "Uses: Bacterial Stool Nucleic Acid Test"
    }),
    ("TotalFix Stool Parasite container", {
        "container_type": "Screw capped container",
        "capacity": "10 mL",
        "description":
            "Uses: Stool Enteric Protozoan Panel. Microsporidumstain - "
            "Microsporidia"
    }),
    ("TotalFix Stool Parasite container", {
        "container_type": "Screw capped container",
        "capacity": "10 mL",
        "description":
            "Uses: Stool Enteric Protozoan Panel. Microsporidumstain - "
            "Microsporidia"
    }),
]

# List of default Containers to create on install
# Tuples of (Preservation name, properties)
PRESERVATIONS = [
    ("4-8 Celsius", {}),
    ("Room temperature", {}),
    ("Frozen", {}),
    ("Liquid nitrogen", {}),
]

# Display order of Sample fields
SAMPLE_FIELDS_ORDER = [
    "PrimaryAnalysisRequest",
    "Client",
    "Contact",
    "MedicalRecordNumber",
    "PatientFullName",
    "PatientAddress",
    "DateOfBirth",
    "Sex",
    "Gender",
    "Age",
    "DateSampled",
    "DateOfAdmission",
    "Ward",
    "WardDepartment",
    "Location",
    "ClinicalInformation",
    "CurrentAntibiotics",
    "Template",
    "Profiles",
    "SampleType",
    "Container",
    "Bottles",
    "Volume",
    "SamplePoint",
    "EnvironmentalConditions",
    "Preservation",
    "SampleCondition",
    "Priority",
    "Attachment",
]

LOCATIONS = DisplayList((
    ("int", _("Inpatient")),
    ("out", _("Outpatient")),
    ("", _("Not specified")),
))
