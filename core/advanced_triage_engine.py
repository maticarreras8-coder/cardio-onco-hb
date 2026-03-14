from typing import Dict, List, Any


def _get_domain_level(domain_profile: List[Dict[str, str]], domain_code: str) -> str:
    for domain in domain_profile:
        if domain.get("domain_code") == domain_code:
            return domain.get("domain_level", "not_relevant")
    return "not_relevant"


def _level_rank(level: str) -> int:
    mapping = {
        "not_relevant": 0,
        "present": 1,
        "relevant": 2,
        "priority": 3,
    }
    return mapping.get(level, 0)


def build_advanced_triage(
    prediction_result: Dict[str, Any],
    result: Dict[str, Any],
    domain_profile: List[Dict[str, str]],
    lvef_percent: float,
    gls_percent: float,
    anthracycline_cum_dose_mg_m2: float,
    thoracic_rt_planned: bool,
    prior_thoracic_rt: bool,
    symptomatic_or_functional_limitation: bool,
) -> Dict[str, Any]:
    """
    Capa HB de triage avanzado.
    Devuelve recomendación sobre:
    - biomarcadores basales
    - CPET
    - razones explicativas
    """

    probability = prediction_result.get("probability_percent", 0.0)

    ctr_cd_level = _get_domain_level(domain_profile, "ctr_cd")
    rt_level = _get_domain_level(domain_profile, "rt_late_effects")

    reasons = []

    # Señales clínicas/estructurales
    if probability >= 50:
        reasons.append("Probabilidad estimada de evento CV muy alta")
    elif probability >= 30:
        reasons.append("Probabilidad estimada de evento CV alta")
    elif probability >= 15:
        reasons.append("Probabilidad estimada de evento CV intermedia")

    if result.get("total_score", 0) >= 7:
        reasons.append("CRS global muy alto")
    elif result.get("total_score", 0) >= 5:
        reasons.append("CRS global alto")

    if lvef_percent < 50:
        reasons.append("FEVI reducida")
    elif lvef_percent < 55:
        reasons.append("FEVI limítrofe")

    if gls_percent > -16:
        reasons.append("GLS claramente alterado")
    elif gls_percent > -18:
        reasons.append("GLS limítrofe")

    if anthracycline_cum_dose_mg_m2 >= 250:
        reasons.append("Dosis acumulada de antraciclina elevada")
    elif anthracycline_cum_dose_mg_m2 > 0:
        reasons.append("Exposición acumulada a antraciclinas")

    if thoracic_rt_planned or prior_thoracic_rt or _level_rank(rt_level) >= 1:
        reasons.append("Radioterapia torácica actual o previa")

    if _level_rank(ctr_cd_level) >= 2:
        reasons.append("Dominio CTRCD relevante o prioritario")

    if symptomatic_or_functional_limitation:
        reasons.append("Síntomas cardiovasculares o limitación funcional")

    # Biomarcadores basales
    biomarker_recommendation = "No de rutina"
    biomarker_intensity = "low"

    if probability >= 50:
        biomarker_recommendation = "Recomendados"
        biomarker_intensity = "high"
    elif probability >= 30:
        biomarker_recommendation = "Recomendados"
        biomarker_intensity = "high"
    elif probability >= 15:
        if (
            anthracycline_cum_dose_mg_m2 > 0
            or thoracic_rt_planned
            or prior_thoracic_rt
            or lvef_percent < 55
            or gls_percent > -18
            or _level_rank(ctr_cd_level) >= 2
        ):
            biomarker_recommendation = "Considerar"
            biomarker_intensity = "medium"

    # CPET refinado por síntomas
    cpet_recommendation = "No indicado de rutina"
    cpet_intensity = "low"

    if symptomatic_or_functional_limitation:
        if probability >= 50:
            cpet_recommendation = "Recomendado"
            cpet_intensity = "high"
        elif probability >= 30:
            cpet_recommendation = "Recomendado"
            cpet_intensity = "high"
        elif (
            lvef_percent < 55
            or gls_percent > -18
            or anthracycline_cum_dose_mg_m2 >= 250
            or thoracic_rt_planned
            or prior_thoracic_rt
            or _level_rank(ctr_cd_level) >= 3
        ):
            cpet_recommendation = "Considerar"
            cpet_intensity = "medium"
    else:
        if probability >= 50:
            cpet_recommendation = "Considerar fuertemente si aparecen síntomas o duda funcional"
            cpet_intensity = "medium"
        elif probability >= 30:
            if (
                lvef_percent < 55
                or gls_percent > -18
                or anthracycline_cum_dose_mg_m2 >= 250
                or thoracic_rt_planned
                or prior_thoracic_rt
                or _level_rank(ctr_cd_level) >= 3
            ):
                cpet_recommendation = "Considerar si aparecen síntomas, desacondicionamiento o duda funcional"
                cpet_intensity = "medium"

    unique_reasons = list(dict.fromkeys(reasons))

    return {
        "baseline_biomarkers_recommendation": biomarker_recommendation,
        "baseline_biomarkers_intensity": biomarker_intensity,
        "cpet_recommendation": cpet_recommendation,
        "cpet_intensity": cpet_intensity,
        "triage_reasons": unique_reasons,
    }
