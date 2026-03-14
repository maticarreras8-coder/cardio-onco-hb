from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from config.settings import INSTITUTION, APP_NAME, AUTHORS, REPORTS_DIR


def _draw_wrapped_text(c, text, x, y, max_width, line_height=14, font_name="Helvetica", font_size=10):
    c.setFont(font_name, font_size)
    words = text.split()
    line = ""
    current_y = y

    for word in words:
        test_line = f"{line} {word}".strip()
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            line = test_line
        else:
            c.drawString(x, current_y, line)
            current_y -= line_height
            line = word

    if line:
        c.drawString(x, current_y, line)
        current_y -= line_height

    return current_y


def _draw_section_title(c, title, x, y):
    c.setFillColorRGB(0.04, 0.24, 0.44)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, title)
    c.setFillColorRGB(0, 0, 0)
    return y - 16


def generate_cardio_onco_pdf(
    patient_id,
    visit_date,
    lvef_percent,
    gls_percent,
    echo_operator,
    anthracycline_cum_dose_mg_m2,
    thoracic_rt_planned,
    prior_thoracic_rt,
    symptomatic_or_functional_limitation,
    result,
    domain_profile,
    recommendation_text,
    prediction_result=None,
    advanced_triage=None,
):
    reports_dir = Path(REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_patient_id = str(patient_id).replace(" ", "_").replace("/", "_")
    filename = f"cardio_onco_{safe_patient_id}_{timestamp}.pdf"
    file_path = reports_dir / filename

    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    left = 2 * cm
    right = width - 2 * cm
    y = height - 2 * cm

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.04, 0.24, 0.44)
    c.drawString(left, y, INSTITUTION)

    y -= 18
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left, y, APP_NAME)

    y -= 16
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.70, 0.13, 0.13)
    c.drawString(left, y, AUTHORS)

    c.setFillColorRGB(0, 0, 0)
    y -= 24

    # Identificación
    y = _draw_section_title(c, "Identificación", left, y)
    c.setFont("Helvetica", 10)
    c.drawString(left, y, f"Patient ID: {patient_id}")
    y -= 14
    c.drawString(left, y, f"Fecha de visita: {visit_date}")
    y -= 20

    # Scores
    y = _draw_section_title(c, "Resultado del score", left, y)
    c.drawString(left, y, f"Treatment Score: {result['treatment_score']}")
    y -= 14
    c.drawString(left, y, f"Patient Score: {result['patient_score']}")
    y -= 14
    c.drawString(left, y, f"Total Score: {result['total_score']}")
    y -= 14
    c.drawString(left, y, f"Categoría: {result['risk_category_es']}")
    y -= 20

    # Predicción
    if prediction_result is not None:
        y = _draw_section_title(c, "Predicción estimada", left, y)
        c.drawString(left, y, f"Probabilidad estimada de evento CV: {prediction_result['probability_percent']}%")
        y -= 14
        c.drawString(left, y, f"Banda de riesgo predictiva: {prediction_result['risk_band']}")
        y -= 16

        if prediction_result.get("drivers"):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(left, y, "Drivers principales del predictor:")
            y -= 14
            c.setFont("Helvetica", 10)
            for driver in prediction_result["drivers"]:
                y = _draw_wrapped_text(c, f"- {driver}", left, y, max_width=right - left)
                if y < 4 * cm:
                    c.showPage()
                    y = height - 2 * cm
            y -= 6

    # Triage avanzado
    if advanced_triage is not None:
        y = _draw_section_title(c, "Triage avanzado HB", left, y)
        y = _draw_wrapped_text(
            c,
            f"Síntomas o limitación funcional: {'Sí' if symptomatic_or_functional_limitation else 'No'}",
            left,
            y,
            max_width=right - left,
        )
        y = _draw_wrapped_text(
            c,
            f"Biomarcadores basales (troponina / BNP-NT-proBNP): {advanced_triage['baseline_biomarkers_recommendation']}",
            left,
            y,
            max_width=right - left,
        )
        y = _draw_wrapped_text(
            c,
            f"CPET: {advanced_triage['cpet_recommendation']}",
            left,
            y,
            max_width=right - left,
        )
        y -= 6

        if advanced_triage.get("triage_reasons"):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(left, y, "Razones del triage:")
            y -= 14
            c.setFont("Helvetica", 10)
            for reason in advanced_triage["triage_reasons"]:
                y = _draw_wrapped_text(c, f"- {reason}", left, y, max_width=right - left)
                if y < 4 * cm:
                    c.showPage()
                    y = height - 2 * cm
            y -= 6

    # Tratamientos
    y = _draw_section_title(c, "Tratamientos seleccionados", left, y)
    for item in result["treatment_items"]:
        line = f"- {item['label']} | CRS {item['crs_score']} | CTRCD {item['incidence_ctrcd']}"
        y = _draw_wrapped_text(c, line, left, y, max_width=right - left)
        if y < 4 * cm:
            c.showPage()
            y = height - 2 * cm

    y -= 6

    # Drivers
    y = _draw_section_title(c, "Drivers principales del score", left, y)
    for driver in result["drivers"]:
        y = _draw_wrapped_text(c, f"- {driver}", left, y, max_width=right - left)
        if y < 4 * cm:
            c.showPage()
            y = height - 2 * cm

    y -= 6

    # Basal
    y = _draw_section_title(c, "Datos basales", left, y)
    basal_lines = [
        f"FEVI: {lvef_percent}%",
        f"GLS: {gls_percent}%",
        f"Operador: {echo_operator}",
        f"Dosis acumulada de antraciclina: {anthracycline_cum_dose_mg_m2} mg/m²",
        f"RT torácica actual/planificada: {'Sí' if thoracic_rt_planned else 'No'}",
        f"RT torácica previa: {'Sí' if prior_thoracic_rt else 'No'}",
        f"Síntomas o limitación funcional: {'Sí' if symptomatic_or_functional_limitation else 'No'}",
    ]
    for line in basal_lines:
        c.drawString(left, y, line)
        y -= 14

    y -= 6

    # Dominios
    y = _draw_section_title(c, "Dominios cardiovasculares detectados", left, y)
    for domain in domain_profile:
        if domain["domain_level"] != "not_relevant":
            line1 = f"- {domain['domain_name_es']} → {domain['domain_level']}"
            y = _draw_wrapped_text(c, line1, left, y, max_width=right - left, font_name="Helvetica-Bold")
            if domain["domain_reason"]:
                y = _draw_wrapped_text(c, domain["domain_reason"], left + 12, y, max_width=(right - left - 12))
            y -= 4

            if y < 4 * cm:
                c.showPage()
                y = height - 2 * cm

    y -= 6

    # Recomendación
    y = _draw_section_title(c, "Recomendación inteligente", left, y)
    for paragraph in recommendation_text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y -= 6
            continue
        y = _draw_wrapped_text(c, paragraph, left, y, max_width=right - left)
        if y < 4 * cm:
            c.showPage()
            y = height - 2 * cm

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(left, 1.2 * cm, f"Generado por {APP_NAME} | {INSTITUTION}")

    c.save()
    return str(file_path)
