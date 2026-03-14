from typing import Dict, List, Any


def _contains_any(text: str, keywords: List[str]) -> bool:
    """
    Devuelve True si el texto contiene cualquiera de las palabras clave.
    """
    if not text:
        return False

    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def detect_ctr_cd_domain(
    treatment_items: List[Dict[str, Any]],
    treatment_score: int,
    anthracycline_cum_dose_mg_m2: float,
    prior_thoracic_rt: bool,
    thoracic_rt_planned: bool,
    patient_risk_factors: Dict[str, bool],
) -> Dict[str, str]:
    """
    Detecta el dominio de disfunción ventricular / CTRCD.
    """
    level = "not_relevant"
    reasons = []

    high_ctr_drugs = [
        "Anthracyclines",
        "Trastuzumab",
        "Pertuzumab",
        "Carfilzomib",
        "Clofarabine",
        "Mitoxantrone",
        "Pazopanib",
        "Sorafenib",
        "Sunitinib",
    ]

    for item in treatment_items:
        class_name = item.get("class", "")
        drug_name = item.get("drug", "")

        if class_name == "Anthracyclines":
            reasons.append(f"{class_name} — {drug_name}")
            level = "priority"

        if any(name.lower() in drug_name.lower() for name in high_ctr_drugs):
            reasons.append(f"{class_name} — {drug_name}")
            if level != "priority":
                level = "relevant"

        if item.get("crs_score", 0) >= 4 and level == "not_relevant":
            reasons.append(f"CRS alto por {class_name} — {drug_name}")
            level = "relevant"

    if anthracycline_cum_dose_mg_m2 and anthracycline_cum_dose_mg_m2 > 0:
        reasons.append(f"Dosis acumulada de antraciclina: {anthracycline_cum_dose_mg_m2} mg/m²")
        if level == "not_relevant":
            level = "present"

    if prior_thoracic_rt or thoracic_rt_planned:
        reasons.append("Radioterapia torácica")
        if level == "not_relevant":
            level = "present"

    if patient_risk_factors.get("prior_hf_cardiomyopathy"):
        reasons.append("Antecedente de insuficiencia cardíaca / cardiomiopatía")
        level = "priority"

    if patient_risk_factors.get("prior_anthracycline_exposure"):
        reasons.append("Exposición previa a antraciclinas")
        if level == "not_relevant":
            level = "present"

    if treatment_score >= 4 and level == "not_relevant":
        level = "present"

    return {
        "domain_code": "ctr_cd",
        "domain_name_es": "Disfunción ventricular / CTRCD",
        "domain_name_en": "Left ventricular dysfunction / CTRCD",
        "domain_level": level,
        "domain_reason": "; ".join(dict.fromkeys(reasons))
    }


def detect_hypertension_vascular_domain(
    treatment_items: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Detecta el dominio hipertensivo / vascular.
    Excluye pulmonary arterial hypertension para no mezclarla con HTA sistémica.
    """
    level = "not_relevant"
    reasons = []

    keywords = [
        "hypertension",
        "vascular",
        "endothelial injury",
        "arterial thrombosis",
        "arterial thromboembolism",
    ]

    for item in treatment_items:
        other = item.get("other_manifestations", "")
        other_lower = other.lower()

        # Excluir pulmonary arterial hypertension de este dominio
        cleaned_text = other_lower.replace("pulmonary arterial hypertension", "")

        if any(keyword.lower() in cleaned_text for keyword in keywords):
            reasons.append(f"{item['label']}: {other}")
            if item.get("crs_score", 0) >= 2:
                level = "priority"
            elif level == "not_relevant":
                level = "present"
            elif level == "present":
                level = "relevant"

    return {
        "domain_code": "hypertension_vascular",
        "domain_name_es": "Hipertensión / toxicidad vascular",
        "domain_name_en": "Hypertension / vascular toxicity",
        "domain_level": level,
        "domain_reason": "; ".join(dict.fromkeys(reasons))
    }

    for item in treatment_items:
        other = item.get("other_manifestations", "")
        if _contains_any(other, keywords):
            reasons.append(f"{item['label']}: {other}")
            if item.get("crs_score", 0) >= 2:
                level = "priority"
            elif level in ["not_relevant", "present"]:
                level = "relevant"
            else:
                level = "present"

    return {
        "domain_code": "hypertension_vascular",
        "domain_name_es": "Hipertensión / toxicidad vascular",
        "domain_name_en": "Hypertension / vascular toxicity",
        "domain_level": level,
        "domain_reason": "; ".join(dict.fromkeys(reasons))
    }


def detect_thrombotic_domain(
    treatment_items: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Detecta riesgo tromboembólico.
    """
    level = "not_relevant"
    reasons = []

    keywords = [
        "thromboembolism",
        "thrombosis",
        "thromboembolic",
        "venous thromboembolism",
        "arterial thromboembolism",
        "arterial and venous thromboembolic",
    ]

    for item in treatment_items:
        other = item.get("other_manifestations", "")
        if _contains_any(other, keywords):
            reasons.append(f"{item['label']}: {other}")
            if level == "not_relevant":
                level = "present"
            elif level == "present":
                level = "relevant"

    return {
        "domain_code": "thrombotic",
        "domain_name_es": "Riesgo trombótico",
        "domain_name_en": "Thrombotic risk",
        "domain_level": level,
        "domain_reason": "; ".join(dict.fromkeys(reasons))
    }


def detect_arrhythmic_qt_domain(
    treatment_items: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Detecta riesgo arrítmico / QT.
    """
    level = "not_relevant"
    reasons = []

    keywords = [
        "arrhythmia",
        "arrhythmias",
        "qt interval prolongation",
        "torsades",
        "bradycardia",
        "sinusbradycardia",
        "conduction",
        "tachyarrhythmias",
        "st-t wave",
        "stt-wave",
    ]

    for item in treatment_items:
        other = item.get("other_manifestations", "")
        if _contains_any(other, keywords):
            reasons.append(f"{item['label']}: {other}")
            if item.get("crs_score", 0) >= 2:
                level = "relevant"
            elif level == "not_relevant":
                level = "present"

    return {
        "domain_code": "arrhythmic_qt",
        "domain_name_es": "Arritmias / QT",
        "domain_name_en": "Arrhythmias / QT",
        "domain_level": level,
        "domain_reason": "; ".join(dict.fromkeys(reasons))
    }


def detect_inflammatory_domain(
    treatment_items: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Detecta dominio inflamatorio / miocarditis / pericardio.
    """
    level = "not_relevant"
    reasons = []

    keywords = [
        "myocarditis",
        "pericarditis",
        "pericardial effusion",
        "tamponade",
        "cardiac tamponade",
    ]

    for item in treatment_items:
        other = item.get("other_manifestations", "")
        if _contains_any(other, keywords):
            reasons.append(f"{item['label']}: {other}")

            if "fatal myocarditis" in other.lower():
                level = "priority"
            elif level == "not_relevant":
                level = "present"
            elif level == "present":
                level = "relevant"

    return {
        "domain_code": "inflammatory_myocarditis",
        "domain_name_es": "Inflamatorio / miocarditis / pericardio",
        "domain_name_en": "Inflammatory / myocarditis / pericardium",
        "domain_level": level,
        "domain_reason": "; ".join(dict.fromkeys(reasons))
    }


def detect_rt_late_effects_domain(
    prior_thoracic_rt: bool,
    thoracic_rt_planned: bool
) -> Dict[str, str]:
    """
    Detecta riesgo tardío relacionado con radioterapia torácica.
    """
    level = "not_relevant"
    reasons = []

    if prior_thoracic_rt:
        level = "relevant"
        reasons.append("Radioterapia torácica previa")

    if thoracic_rt_planned:
        if level == "not_relevant":
            level = "present"
        reasons.append("Radioterapia torácica actual / planificada")

    return {
        "domain_code": "rt_late_effects",
        "domain_name_es": "Radioterapia torácica / efectos tardíos",
        "domain_name_en": "Thoracic radiotherapy / late effects",
        "domain_level": level,
        "domain_reason": "; ".join(dict.fromkeys(reasons))
    }


def build_domain_profile(
    treatment_items: List[Dict[str, Any]],
    treatment_score: int,
    anthracycline_cum_dose_mg_m2: float,
    prior_thoracic_rt: bool,
    thoracic_rt_planned: bool,
    patient_risk_factors: Dict[str, bool],
) -> List[Dict[str, str]]:
    """
    Construye el perfil completo de dominios cardiovasculares.
    """
    domains = [
        detect_ctr_cd_domain(
            treatment_items=treatment_items,
            treatment_score=treatment_score,
            anthracycline_cum_dose_mg_m2=anthracycline_cum_dose_mg_m2,
            prior_thoracic_rt=prior_thoracic_rt,
            thoracic_rt_planned=thoracic_rt_planned,
            patient_risk_factors=patient_risk_factors,
        ),
        detect_hypertension_vascular_domain(treatment_items),
        detect_thrombotic_domain(treatment_items),
        detect_arrhythmic_qt_domain(treatment_items),
        detect_inflammatory_domain(treatment_items),
        detect_rt_late_effects_domain(prior_thoracic_rt, thoracic_rt_planned),
    ]

    return domains
