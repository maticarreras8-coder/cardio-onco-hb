import json
from pathlib import Path

catalog = [
    # Alkylating Agents
    {
        "class": "Alkylating Agents",
        "drug": "Cyclophosphamide (Endoxan) - High dose",
        "label": "Alkylating Agents — Cyclophosphamide (Endoxan) - High dose",
        "incidence_ctrcd": "7-28%",
        "crs_score": 4,
        "other_manifestations": "Pericarditis; Myocarditis; Cardiac tamponade;"
    },
    {
        "class": "Alkylating Agents",
        "drug": "Cyclophosphamide (Endoxan) - Low dose",
        "label": "Alkylating Agents — Cyclophosphamide (Endoxan) - Low dose",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Alkylating Agents",
        "drug": "Ifosfamide (Ifex)",
        "label": "Alkylating Agents — Ifosfamide (Ifex)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Arrhythmias; STT-wave changes;"
    },
    {
        "class": "Alkylating Agents",
        "drug": "Bendamustine",
        "label": "Alkylating Agents — Bendamustine",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Arrhythmias (5%);"
    },
    {
        "class": "Alkylating Agents",
        "drug": "Busulfan (Busilvex)",
        "label": "Alkylating Agents — Busulfan (Busilvex)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Endomyocardial fibrosis (case report);"
    },
    {
        "class": "Alkylating Agents",
        "drug": "Carboplatin (Carbosin)",
        "label": "Alkylating Agents — Carboplatin (Carbosin)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Coronary spasm (case report);"
    },
    {
        "class": "Alkylating Agents",
        "drug": "Carmustine (BCNU)",
        "label": "Alkylating Agents — Carmustine (BCNU)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Chest pain; Hypotension; Sinus tachycardia;"
    },
    {
        "class": "Alkylating Agents",
        "drug": "Cisplatin",
        "label": "Alkylating Agents — Cisplatin",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Endothelial injury; Arterial thrombosis; Vascular fibrosis;"
    },
    {
        "class": "Alkylating Agents",
        "drug": "Melphalan (Alkeran)",
        "label": "Alkylating Agents — Melphalan (Alkeran)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Atrial fibrillation; Supraventricular tachycardia;"
    },

    # Anthracyclines
    {
        "class": "Anthracyclines",
        "drug": "Doxorubicin (Adriamycin)",
        "label": "Anthracyclines — Doxorubicin (Adriamycin)",
        "incidence_ctrcd": "3-48%",
        "crs_score": 4,
        "other_manifestations": ""
    },
    {
        "class": "Anthracyclines",
        "drug": "Epirubicin",
        "label": "Anthracyclines — Epirubicin",
        "incidence_ctrcd": "0.9-11.4%",
        "crs_score": 4,
        "other_manifestations": ""
    },
    {
        "class": "Anthracyclines",
        "drug": "Idarubicin (Zavedos)",
        "label": "Anthracyclines — Idarubicin (Zavedos)",
        "incidence_ctrcd": "5-18%",
        "crs_score": 4,
        "other_manifestations": ""
    },
    {
        "class": "Anthracyclines",
        "drug": "Daunorubicin (Cerubidine)",
        "label": "Anthracyclines — Daunorubicin (Cerubidine)",
        "incidence_ctrcd": "1.2-9.9%",
        "crs_score": 2,
        "other_manifestations": "Cardiac arrhythmias; Myocardial ischemia; ST-T wave abnormalities;"
    },
    {
        "class": "Anthracyclines",
        "drug": "Mitoxantrone",
        "label": "Anthracyclines — Mitoxantrone",
        "incidence_ctrcd": "4.1-5.3%",
        "crs_score": 2,
        "other_manifestations": ""
    },

    # Antimetabolites
    {
        "class": "Antimetabolites",
        "drug": "Clofarabine (Evolta)",
        "label": "Antimetabolites — Clofarabine (Evolta)",
        "incidence_ctrcd": "0-27%",
        "crs_score": 4,
        "other_manifestations": ""
    },
    {
        "class": "Antimetabolites",
        "drug": "5-Fluorouracil",
        "label": "Antimetabolites — 5-Fluorouracil",
        "incidence_ctrcd": "<1%",
        "crs_score": 4,
        "other_manifestations": "High incidence of angina pectoris; acute myocardial infarction; coronary vasospasm (0.55-19%)"
    },
    {
        "class": "Antimetabolites",
        "drug": "Capecitabine (Xeloda)",
        "label": "Antimetabolites — Capecitabine (Xeloda)",
        "incidence_ctrcd": "<1%",
        "crs_score": 4,
        "other_manifestations": "High incidence of angina pectoris; acute myocardial infarction; coronary vasospasm (0.55-19%)"
    },
    {
        "class": "Antimetabolites",
        "drug": "Azaciditine",
        "label": "Antimetabolites — Azaciditine",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Pericardial effusion; Myocarditis;"
    },
    {
        "class": "Antimetabolites",
        "drug": "Cladribine (Leustatin)",
        "label": "Antimetabolites — Cladribine (Leustatin)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Antimetabolites",
        "drug": "Cytarabine (AraC)",
        "label": "Antimetabolites — Cytarabine (AraC)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Pericarditis, progressing to pericardial effusion and cardiac tamponade;"
    },
    {
        "class": "Antimetabolites",
        "drug": "Fludarabine (Fludara)",
        "label": "Antimetabolites — Fludarabine (Fludara)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Hypotension; Chest pain;"
    },
    {
        "class": "Antimetabolites",
        "drug": "Gemcitabine",
        "label": "Antimetabolites — Gemcitabine",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Cardiac arrhythmias (0.7-1.4%); Exudative pericarditis (0.2%)"
    },
    {
        "class": "Antimetabolites",
        "drug": "Mercaptopurine (Xaluprine)",
        "label": "Antimetabolites — Mercaptopurine (Xaluprine)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "No reports in literature"
    },
    {
        "class": "Antimetabolites",
        "drug": "Pentostatin",
        "label": "Antimetabolites — Pentostatin",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Case reports on cardiac complications;"
    },

    # Antitumor antibiotics
    {
        "class": "Antitumor antibiotics",
        "drug": "Mitomycin C",
        "label": "Antitumor antibiotics — Mitomycin C",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Antitumor antibiotics",
        "drug": "Bleomycin",
        "label": "Antitumor antibiotics — Bleomycin",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Pericarditis; Endothelial dysfunction and accelerated atherosclerosis; Myocardial ischemia;"
    },

    # Biologic response modifiers
    {
        "class": "Biologic response modifiers",
        "drug": "Interferon-α",
        "label": "Biologic response modifiers — Interferon-α",
        "incidence_ctrcd": "4.4%",
        "crs_score": 1,
        "other_manifestations": "Arrhythmias and conduction disorders (20%);"
    },
    {
        "class": "Biologic response modifiers",
        "drug": "Interleukin-2",
        "label": "Biologic response modifiers — Interleukin-2",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Arrhythmias (5-20%); Hypotension; Ischemia (1-4%);"
    },

    # Microtubule-targeting drugs
    {
        "class": "Microtubule-targeting drugs",
        "drug": "Vinblastine",
        "label": "Microtubule-targeting drugs — Vinblastine",
        "incidence_ctrcd": "5-10%",
        "crs_score": 2,
        "other_manifestations": "Hypertension; Myocardial ischemia;"
    },
    {
        "class": "Microtubule-targeting drugs",
        "drug": "Docetaxel (Taxotere)",
        "label": "Microtubule-targeting drugs — Docetaxel (Taxotere)",
        "incidence_ctrcd": "1.6-2%",
        "crs_score": 1,
        "other_manifestations": ""
    },
    {
        "class": "Microtubule-targeting drugs",
        "drug": "Vinorelbine (Navelbine)",
        "label": "Microtubule-targeting drugs — Vinorelbine (Navelbine)",
        "incidence_ctrcd": "1.2%",
        "crs_score": 1,
        "other_manifestations": "Myocardial ischemia;"
    },
    {
        "class": "Microtubule-targeting drugs",
        "drug": "Eribuline (Halaven)",
        "label": "Microtubule-targeting drugs — Eribuline (Halaven)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "QT interval prolongation;"
    },
    {
        "class": "Microtubule-targeting drugs",
        "drug": "Ixabepilone",
        "label": "Microtubule-targeting drugs — Ixabepilone",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Microtubule-targeting drugs",
        "drug": "Paclitaxel (Abraxane)",
        "label": "Microtubule-targeting drugs — Paclitaxel (Abraxane)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Arrhythmias (4%)"
    },
    {
        "class": "Microtubule-targeting drugs",
        "drug": "Vincristine",
        "label": "Microtubule-targeting drugs — Vincristine",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Autonomic cardioneuropathy; Myocardial ischemia;"
    },

    # Monoclonal antibody-based tyrosine kinase inhibitors
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Trastuzumab (Herceptin)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Trastuzumab (Herceptin)",
        "incidence_ctrcd": "2-28%",
        "crs_score": 4,
        "other_manifestations": "Vascular thrombosis; Arrhythmia;"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Pertuzumab (Perjeta)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Pertuzumab (Perjeta)",
        "incidence_ctrcd": "3-7%",
        "crs_score": 2,
        "other_manifestations": ""
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Aflibercept (Zaltrap)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Aflibercept (Zaltrap)",
        "incidence_ctrcd": "0-1.2%",
        "crs_score": 1,
        "other_manifestations": "Hypertension (19-44%); Venous thromboembolism;"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Bevacizumab (Avastin)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Bevacizumab (Avastin)",
        "incidence_ctrcd": "0-1.6%",
        "crs_score": 1,
        "other_manifestations": "Hypertension; Arterial thromboembolism (3.8%)"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Alemtuzumab (Lemtrada)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Alemtuzumab (Lemtrada)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Hypotension;"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Brentuximab (Adcetris)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Brentuximab (Adcetris)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Cetuximab (Erbitux)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Cetuximab (Erbitux)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Panitumumab (Vectibix)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Panitumumab (Vectibix)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Ramucirumab (Cyramza)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Ramucirumab (Cyramza)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Hypertension; Arterial thromboembolism;"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Rituximab (MabThera)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Rituximab (MabThera)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Hypotension; Infusion related adverse events; Arrhythmias;"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Ipilimumab (Yervoy)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Ipilimumab (Yervoy)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Fatal myocarditis; Pericarditis"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Nivolumab (Opdivo)",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Nivolumab (Opdivo)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Fatal myocarditis;"
    },
    {
        "class": "Monoclonal antibody-based tyrosine kinase inhibitors",
        "drug": "Ipilimumab with Nivolumab",
        "label": "Monoclonal antibody-based tyrosine kinase inhibitors — Ipilimumab with Nivolumab",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Fatal myocarditis;"
    },

    # Proteasome inhibitors
    {
        "class": "Proteasome inhibitors",
        "drug": "Carfilzomib (Kyprolis)",
        "label": "Proteasome inhibitors — Carfilzomib (Kyprolis)",
        "incidence_ctrcd": "3.8-7%",
        "crs_score": 2,
        "other_manifestations": "Myocardial infarction (0.8%); Pulmonary arterial hypertension (2%)"
    },
    {
        "class": "Proteasome inhibitors",
        "drug": "Bortezomib (Velcade)",
        "label": "Proteasome inhibitors — Bortezomib (Velcade)",
        "incidence_ctrcd": "2%",
        "crs_score": 1,
        "other_manifestations": ""
    },

    # Small-molecule tyrosine kinase inhibitors
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Pazopanib (Votrient)",
        "label": "Small-molecule tyrosine kinase inhibitors — Pazopanib (Votrient)",
        "incidence_ctrcd": "7-13%",
        "crs_score": 4,
        "other_manifestations": "Hypertension; Thrombosis; Myocardial ischemia; Bradycardia; QT interval prolongation;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Sorafenib (Nexavar)",
        "label": "Small-molecule tyrosine kinase inhibitors — Sorafenib (Nexavar)",
        "incidence_ctrcd": "4-28%",
        "crs_score": 4,
        "other_manifestations": "Hypertension; Thromboembolism; Arrhythmias; QT interval prolongation;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Sunitinib (Sutent)",
        "label": "Small-molecule tyrosine kinase inhibitors — Sunitinib (Sutent)",
        "incidence_ctrcd": "3-15%",
        "crs_score": 4,
        "other_manifestations": "Hypertension; Thromboembolism; Arrhythmias; QT interval prolongation;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Binimetinib (Mektovi)",
        "label": "Small-molecule tyrosine kinase inhibitors — Binimetinib (Mektovi)",
        "incidence_ctrcd": "1-7%",
        "crs_score": 2,
        "other_manifestations": ""
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Dabrafenib",
        "label": "Small-molecule tyrosine kinase inhibitors — Dabrafenib",
        "incidence_ctrcd": "8-9%",
        "crs_score": 2,
        "other_manifestations": "When combined with trametinib; Venous thrombosis;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Lenvatinib (Lenvima)",
        "label": "Small-molecule tyrosine kinase inhibitors — Lenvatinib (Lenvima)",
        "incidence_ctrcd": "5-7%",
        "crs_score": 2,
        "other_manifestations": "Hypertension; Arterial and venous thromboembolism;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Ponatinib (Iclusig)",
        "label": "Small-molecule tyrosine kinase inhibitors — Ponatinib (Iclusig)",
        "incidence_ctrcd": "8%",
        "crs_score": 2,
        "other_manifestations": "Hypertension; Arterial and venous thromboembolism;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Trametinib (Mekinist)",
        "label": "Small-molecule tyrosine kinase inhibitors — Trametinib (Mekinist)",
        "incidence_ctrcd": "3-7%",
        "crs_score": 2,
        "other_manifestations": "Hypertension; Venous thromboembolism;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Afatinib",
        "label": "Small-molecule tyrosine kinase inhibitors — Afatinib",
        "incidence_ctrcd": "2.20%",
        "crs_score": 1,
        "other_manifestations": "Hypertension; Arterial and venous thromboembolism;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Axitinib (Inlyta)",
        "label": "Small-molecule tyrosine kinase inhibitors — Axitinib (Inlyta)",
        "incidence_ctrcd": "0-1.8%",
        "crs_score": 1,
        "other_manifestations": ""
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Imatinib (Glivec)",
        "label": "Small-molecule tyrosine kinase inhibitors — Imatinib (Glivec)",
        "incidence_ctrcd": "0.2-1.7%",
        "crs_score": 1,
        "other_manifestations": "Beneficial effects on glucose, cholesterol; Treatment for pulmonary arterial hypertension"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Lapatinib (Tyverb)",
        "label": "Small-molecule tyrosine kinase inhibitors — Lapatinib (Tyverb)",
        "incidence_ctrcd": "1.5-2.2%",
        "crs_score": 1,
        "other_manifestations": "QT interval prolongation; Myocardial ischemia;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Ceritinib (Zykadia)",
        "label": "Small-molecule tyrosine kinase inhibitors — Ceritinib (Zykadia)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "QT interval prolongation; Sinusbradycardia;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Crizotinib (Xalkori)",
        "label": "Small-molecule tyrosine kinase inhibitors — Crizotinib (Xalkori)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Sinusbradycardia;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Ibrutinib (Imbruvica)",
        "label": "Small-molecule tyrosine kinase inhibitors — Ibrutinib (Imbruvica)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Atrial fibrillation (3-6%);"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Dasatinib (Sprycel)",
        "label": "Small-molecule tyrosine kinase inhibitors — Dasatinib (Sprycel)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "QT interval prolongation; Pulmonary arterial hypertension; Pleural effusion;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Regorafenib (Stivarga)",
        "label": "Small-molecule tyrosine kinase inhibitors — Regorafenib (Stivarga)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Hypertension; Myocardial ischemia;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Vandetanib (Caprelsa)",
        "label": "Small-molecule tyrosine kinase inhibitors — Vandetanib (Caprelsa)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "QT interval prolongation; Torsades de pointes;"
    },
    {
        "class": "Small-molecule tyrosine kinase inhibitors",
        "drug": "Vemurafenib (Zelboraf)",
        "label": "Small-molecule tyrosine kinase inhibitors — Vemurafenib (Zelboraf)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "QT interval prolongation;"
    },

    # Topoisomerase inhibitors
    {
        "class": "Topoisomerase inhibitors",
        "drug": "Etoposide (Eposin/Toposin)",
        "label": "Topoisomerase inhibitors — Etoposide (Eposin/Toposin)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Hypotension (1-2%); Acute myocardial infarction; Coronary vasospasm;"
    },
    {
        "class": "Topoisomerase inhibitors",
        "drug": "Teniposide (Vumon)",
        "label": "Topoisomerase inhibitors — Teniposide (Vumon)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Hypotension (2%); Arrhythmias;"
    },

    # Immunosuppressiva
    {
        "class": "Immunosuppressiva",
        "drug": "Lenalidomide (Revlimid)",
        "label": "Immunosuppressiva — Lenalidomide (Revlimid)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Venous or arterial thromboembolic events;"
    },
    {
        "class": "Immunosuppressiva",
        "drug": "Thalidomide",
        "label": "Immunosuppressiva — Thalidomide",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Venous or arterial thromboembolic events;"
    },

    # Miscellaneous
    {
        "class": "Miscellaneous",
        "drug": "Estramustine (Estracyt)",
        "label": "Miscellaneous — Estramustine (Estracyt)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Arterial and venous thromboembolic events;"
    },
    {
        "class": "Miscellaneous",
        "drug": "Amsacrine",
        "label": "Miscellaneous — Amsacrine",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Atrial and ventricular tachyarrhythmias;"
    },
    {
        "class": "Miscellaneous",
        "drug": "Anti-thymocyte globulin (ATG)",
        "label": "Miscellaneous — Anti-thymocyte globulin (ATG)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Miscellaneous",
        "drug": "Asparaginase (Erwinase/Paronal)",
        "label": "Miscellaneous — Asparaginase (Erwinase/Paronal)",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "Thromboembolic events; Myocardial infarction (1 case report);"
    },
    {
        "class": "Miscellaneous",
        "drug": "Histone deacetylase inhibitors",
        "label": "Miscellaneous — Histone deacetylase inhibitors",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "ST-T abnormalities (15%); QT interval prolongation (4%);"
    },
    {
        "class": "Miscellaneous",
        "drug": "Irinotecan",
        "label": "Miscellaneous — Irinotecan",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": ""
    },
    {
        "class": "Miscellaneous",
        "drug": "LHRH agonist/antagonist",
        "label": "Miscellaneous — LHRH agonist/antagonist",
        "incidence_ctrcd": "<1%",
        "crs_score": 0,
        "other_manifestations": "QT interval prolongation;"
    },
]

output_path = Path("config/treatment_catalog.json")
output_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Catálogo generado con {len(catalog)} tratamientos en {output_path}")
