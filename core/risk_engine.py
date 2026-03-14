from typing import Dict, List, Any


def get_treatment_items(selected_labels: List[str], catalog: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Devuelve los tratamientos seleccionados con toda su información desde el catálogo.
    """
    selected = []
    selected_set = set(selected_labels)

    for item in catalog:
        if item["label"] in selected_set:
            selected.append(item)

    return selected


def calculate_treatment_risk_score(treatment_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    El CRS de tratamiento es el máximo score entre las drogas seleccionadas.
    """
    if not treatment_items:
        return {
            "treatment_score": 0,
            "drivers": [],
            "items": []
        }

    max_score = max(item["crs_score"] for item in treatment_items)
    drivers = [item["label"] for item in treatment_items if item["crs_score"] == max_score]

    return {
        "treatment_score": max_score,
        "drivers": drivers,
        "items": treatment_items
    }


def calculate_patient_risk_score(risk_factors: Dict[str, bool]) -> int:
    """
    Cada factor positivo suma 1 punto.
    """
    return sum(1 for value in risk_factors.values() if value)


def categorize_risk(total_score: int) -> Dict[str, str]:
    """
    Categoriza el riesgo según el score total.
    """
    if total_score == 0:
        return {"es": "Muy bajo", "en": "Very low"}
    if total_score in [1, 2]:
        return {"es": "Bajo", "en": "Low"}
    if total_score in [3, 4]:
        return {"es": "Intermedio", "en": "Intermediate"}
    if total_score in [5, 6]:
        return {"es": "Alto", "en": "High"}
    return {"es": "Muy alto", "en": "Very high"}


def calculate_full_risk(
    selected_labels: List[str],
    catalog: List[Dict[str, Any]],
    risk_factors: Dict[str, bool]
) -> Dict[str, Any]:
    """
    Calcula el resultado completo del CRS base.
    """
    treatment_items = get_treatment_items(selected_labels, catalog)
    treatment_result = calculate_treatment_risk_score(treatment_items)
    patient_score = calculate_patient_risk_score(risk_factors)
    total_score = treatment_result["treatment_score"] + patient_score
    category = categorize_risk(total_score)

    return {
        "treatment_items": treatment_result["items"],
        "treatment_score": treatment_result["treatment_score"],
        "drivers": treatment_result["drivers"],
        "patient_score": patient_score,
        "total_score": total_score,
        "risk_category_es": category["es"],
        "risk_category_en": category["en"]
    }
