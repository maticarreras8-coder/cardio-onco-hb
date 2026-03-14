from typing import Dict, List, Any


def _format_domain_level(level: str) -> str:
    mapping = {
        "not_relevant": "No relevante",
        "present": "Presente",
        "relevant": "Relevante",
        "priority": "Prioritario",
    }
    return mapping.get(level, level)


def build_global_risk_text(result: Dict[str, Any]) -> str:
    return (
        f"**Riesgo global**  \n"
        f"El puntaje de riesgo cardiovascular (CRS) calculado para este paciente es "
        f"**{result['total_score']}**, correspondiente a una categoría de riesgo "
        f"**{result['risk_category_es']}**."
    )


def build_driver_text(result: Dict[str, Any]) -> str:
    if not result["drivers"]:
        return "**Drivers terapéuticos**  \nNo se identificaron terapias dominantes para el puntaje."

    drivers_text = "\n".join([f"- {driver}" for driver in result["drivers"]])

    return (
        "**Drivers terapéuticos del score**  \n"
        "El riesgo cardiovascular asociado al tratamiento está determinado "
        "principalmente por las siguientes terapias con mayor potencial cardiotóxico:  \n"
        f"{drivers_text}"
    )


def build_domains_text(domain_profile: List[Dict[str, str]]) -> str:
    active_domains = [d for d in domain_profile if d["domain_level"] != "not_relevant"]

    if not active_domains:
        return "**Dominios cardiovasculares relevantes**  \nNo se detectaron dominios cardiovasculares adicionales relevantes."

    lines = []
    for domain in active_domains:
        level_text = _format_domain_level(domain["domain_level"])
        lines.append(f"- {domain['domain_name_es']}: **{level_text}**")

    return "**Dominios cardiovasculares relevantes**  \n" + "\n".join(lines)


def build_management_plan(
    result: Dict[str, Any],
    domain_profile: List[Dict[str, str]]
) -> str:
    risk_category = result["risk_category_es"].lower()

    lines = []
    lines.append("- Realizar evaluación cardiovascular basal con ECG y ecocardiograma con FEVI y GLS.")

    if risk_category in ["muy bajo", "bajo"]:
        lines.append("- El seguimiento posterior puede individualizarse según evolución clínica.")
    elif risk_category == "intermedio":
        lines.append("- Considerar seguimiento ecocardiográfico periódico durante el tratamiento.")
    elif risk_category in ["alto", "muy alto"]:
        lines.append("- Se recomienda seguimiento ecocardiográfico seriado durante el tratamiento.")
        lines.append("- Se sugiere seguimiento cardio-oncológico estrecho.")

    domain_codes = {d["domain_code"]: d for d in domain_profile if d["domain_level"] != "not_relevant"}

    if "hypertension_vascular" in domain_codes:
        lines.append("- Reforzar control clínico y tensional durante el tratamiento.")

    if "thrombotic" in domain_codes:
        lines.append("- Mantener vigilancia clínica dirigida a eventos tromboembólicos arteriales o venosos.")

    if "arrhythmic_qt" in domain_codes:
        lines.append("- Considerar vigilancia electrocardiográfica según contexto clínico y terapias administradas.")

    if "inflammatory_myocarditis" in domain_codes:
        lines.append("- Mantener vigilancia clínica ante síntomas compatibles con miocarditis o pericarditis.")

    if "rt_late_effects" in domain_codes:
        lines.append("- Considerar el antecedente de radioterapia torácica como factor adicional de riesgo estructural a largo plazo.")

    lines.append("- La medición de troponina y BNP/NT-proBNP puede considerarse a criterio clínico.")

    return "**Plan sugerido**  \n" + "\n".join(lines)


def build_additional_manifestations_text(treatment_items: List[Dict[str, Any]]) -> str:
    manifestations = []

    for item in treatment_items:
        other = item.get("other_manifestations", "").strip()
        if other:
            manifestations.append(f"- {item['label']}: {other}")

    if not manifestations:
        return "**Otras manifestaciones cardiovasculares**  \nNo se registran otras manifestaciones cardiovasculares adicionales en las terapias seleccionadas."

    return (
        "**Otras manifestaciones cardiovasculares**  \n"
        "Manifestaciones descritas para las terapias seleccionadas:  \n"
        + "\n".join(manifestations)
    )


def assemble_recommendation(
    result: Dict[str, Any],
    domain_profile: List[Dict[str, str]]
) -> str:
    sections = [
        build_global_risk_text(result),
        "",
        build_driver_text(result),
        "",
        build_domains_text(domain_profile),
        "",
        build_management_plan(result, domain_profile),
        "",
        build_additional_manifestations_text(result["treatment_items"]),
    ]

    return "\n\n".join(sections)
