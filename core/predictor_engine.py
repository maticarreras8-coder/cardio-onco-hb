from typing import Dict, List, Any
from pathlib import Path
import pickle
import pandas as pd

MODEL_PATH = Path("storage/ml_outputs/cardio_onco_model.pkl")
FEATURES_PATH = Path("storage/ml_outputs/cardio_onco_model_features.pkl")


def estimate_cv_event_probability_rule_based(
    result: Dict[str, Any],
    domain_profile: List[Dict[str, str]],
    lvef_percent: float,
    gls_percent: float,
    anthracycline_cum_dose_mg_m2: float,
) -> Dict[str, Any]:
    score = 0.0
    drivers = []

    total_score = result.get("total_score", 0)
    if total_score >= 7:
        score += 0.22
        drivers.append("CRS total muy alto")
    elif total_score >= 5:
        score += 0.16
        drivers.append("CRS total alto")
    elif total_score >= 3:
        score += 0.10
        drivers.append("CRS total intermedio")

    if lvef_percent < 50:
        score += 0.20
        drivers.append("FEVI reducida")
    elif lvef_percent < 55:
        score += 0.10
        drivers.append("FEVI limítrofe")

    if gls_percent > -16:
        score += 0.18
        drivers.append("GLS claramente alterado")
    elif gls_percent > -18:
        score += 0.10
        drivers.append("GLS limítrofe")

    if anthracycline_cum_dose_mg_m2 >= 250:
        score += 0.15
        drivers.append("Dosis acumulada de antraciclina elevada")
    elif anthracycline_cum_dose_mg_m2 > 0:
        score += 0.08
        drivers.append("Exposición acumulada a antraciclinas")

    level_weights = {
        "present": 0.04,
        "relevant": 0.08,
        "priority": 0.14,
    }

    for domain in domain_profile:
        level = domain.get("domain_level", "not_relevant")
        if level in level_weights:
            score += level_weights[level]
            drivers.append(f"{domain['domain_name_es']} ({level})")

    probability = min(score, 0.95)
    probability_percent = round(probability * 100, 1)

    if probability_percent < 15:
        risk_band = "Bajo"
    elif probability_percent < 30:
        risk_band = "Intermedio"
    elif probability_percent < 50:
        risk_band = "Alto"
    else:
        risk_band = "Muy alto"

    unique_drivers = list(dict.fromkeys(drivers))

    return {
        "probability_percent": probability_percent,
        "risk_band": risk_band,
        "drivers": unique_drivers[:8],
        "source": "rule_based",
    }


def _domain_to_binary(domain_profile: List[Dict[str, str]], domain_code: str) -> int:
    for domain in domain_profile:
        if domain.get("domain_code") == domain_code and domain.get("domain_level") != "not_relevant":
            return 1
    return 0


def estimate_cv_event_probability_ml(
    result: Dict[str, Any],
    domain_profile: List[Dict[str, str]],
    lvef_percent: float,
    gls_percent: float,
    anthracycline_cum_dose_mg_m2: float,
    risk_factors: Dict[str, bool],
    thoracic_rt_planned: bool,
    prior_thoracic_rt: bool,
) -> Dict[str, Any]:
    if not MODEL_PATH.exists() or not FEATURES_PATH.exists():
        raise FileNotFoundError("Modelo ML no disponible")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(FEATURES_PATH, "rb") as f:
        feature_cols = pickle.load(f)

    row = {
        "lvef_percent": lvef_percent,
        "gls_percent": gls_percent,
        "anthracycline_cum_dose_mg_m2": anthracycline_cum_dose_mg_m2,
        "thoracic_rt_planned": int(thoracic_rt_planned),
        "prior_thoracic_rt": int(prior_thoracic_rt),
        "treatment_risk_score": result.get("treatment_score", 0),
        "patient_risk_score": result.get("patient_score", 0),
        "total_risk_score": result.get("total_score", 0),
        "htn": int(risk_factors.get("htn", False)),
        "dm": int(risk_factors.get("dm", False)),
        "cad_pad": int(risk_factors.get("cad_pad", False)),
        "prior_hf_cardiomyopathy": int(risk_factors.get("prior_hf_cardiomyopathy", False)),
        "prior_anthracycline_exposure": int(risk_factors.get("prior_anthracycline_exposure", False)),
        "prior_thoracic_rt_factor": int(risk_factors.get("prior_thoracic_rt", False)),
        "age_gt_65": int(risk_factors.get("age_gt_65", False)),
        "female_sex": int(risk_factors.get("female_sex", False)),
        "domain_ctr_cd": _domain_to_binary(domain_profile, "ctr_cd"),
        "domain_hypertension_vascular": _domain_to_binary(domain_profile, "hypertension_vascular"),
        "domain_thrombotic": _domain_to_binary(domain_profile, "thrombotic"),
        "domain_arrhythmic_qt": _domain_to_binary(domain_profile, "arrhythmic_qt"),
        "domain_inflammatory_myocarditis": _domain_to_binary(domain_profile, "inflammatory_myocarditis"),
        "domain_rt_late_effects": _domain_to_binary(domain_profile, "rt_late_effects"),
    }

    X = pd.DataFrame([row])[feature_cols]
    prob = float(model.predict_proba(X)[0, 1])
    probability_percent = round(prob * 100, 1)

    if probability_percent < 15:
        risk_band = "Bajo"
    elif probability_percent < 30:
        risk_band = "Intermedio"
    elif probability_percent < 50:
        risk_band = "Alto"
    else:
        risk_band = "Muy alto"

    return {
        "probability_percent": probability_percent,
        "risk_band": risk_band,
        "drivers": ["Modelo entrenado con datos Cardio-Onco HB"],
        "source": "ml_model",
    }


def estimate_cv_event_probability(
    result: Dict[str, Any],
    domain_profile: List[Dict[str, str]],
    lvef_percent: float,
    gls_percent: float,
    anthracycline_cum_dose_mg_m2: float,
    risk_factors: Dict[str, bool] = None,
    thoracic_rt_planned: bool = False,
    prior_thoracic_rt: bool = False,
) -> Dict[str, Any]:
    if risk_factors is None:
        risk_factors = {}

    try:
        return estimate_cv_event_probability_ml(
            result=result,
            domain_profile=domain_profile,
            lvef_percent=lvef_percent,
            gls_percent=gls_percent,
            anthracycline_cum_dose_mg_m2=anthracycline_cum_dose_mg_m2,
            risk_factors=risk_factors,
            thoracic_rt_planned=thoracic_rt_planned,
            prior_thoracic_rt=prior_thoracic_rt,
        )
    except Exception:
        return estimate_cv_event_probability_rule_based(
            result=result,
            domain_profile=domain_profile,
            lvef_percent=lvef_percent,
            gls_percent=gls_percent,
            anthracycline_cum_dose_mg_m2=anthracycline_cum_dose_mg_m2,
        )
