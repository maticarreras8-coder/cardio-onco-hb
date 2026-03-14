import json
from pathlib import Path
from datetime import date

import streamlit as st

from config.settings import APP_NAME, INSTITUTION, AUTHORS, DEFAULT_ECHO_OPERATOR
from core.risk_engine import calculate_full_risk
from core.domain_engine import build_domain_profile
from core.recommendation_engine import assemble_recommendation
from core.predictor_engine import estimate_cv_event_probability
from core.advanced_triage_engine import build_advanced_triage
from data.db import init_db
from data.repositories import (
    save_patient,
    save_visit,
    save_visit_treatments,
    save_visit_risk_factors,
    save_visit_domains,
)
from export.pdf_generator import generate_cardio_onco_pdf

st.set_page_config(page_title=APP_NAME, layout="wide")
init_db()


def load_catalog():
    catalog_path = Path("config/treatment_catalog.json")
    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)


def init_session_state():
    defaults = {
        "calculated": False,
        "result": None,
        "domain_profile": None,
        "recommendation_text": "",
        "gls_normalized": None,
        "saved_visit_id": None,
        "pdf_path": None,
        "prediction_result": None,
        "advanced_triage": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


catalog = load_catalog()
treatment_labels = [item["label"] for item in catalog]

init_session_state()

st.title(INSTITUTION)
st.subheader(APP_NAME)
st.caption(AUTHORS)

st.header("Ingreso del paciente")

patient_id = st.text_input("Patient ID *")
visit_date = st.date_input("Fecha de visita", value=date.today())

col1, col2 = st.columns(2)

with col1:
    selected_treatments = st.multiselect(
        "Tratamientos oncológicos",
        options=treatment_labels
    )

    anthracycline_cum_dose = st.number_input(
        "Dosis acumulada de antraciclina (mg/m²)",
        min_value=0.0,
        value=0.0,
        step=10.0
    )

    thoracic_rt_planned = st.checkbox("RT torácica actual / planificada")
    prior_thoracic_rt = st.checkbox("RT torácica previa")
    symptomatic_or_functional_limitation = st.checkbox("Síntomas cardiovasculares o limitación funcional")

with col2:
    st.subheader("Factores del paciente")

    htn = st.checkbox("Hipertensión arterial")
    dm = st.checkbox("Diabetes mellitus")
    cad_pad = st.checkbox("Enfermedad coronaria / PAD")
    prior_hf_cardiomyopathy = st.checkbox("Insuficiencia cardíaca / cardiomiopatía previa")
    prior_anthracycline_exposure = st.checkbox("Exposición previa a antraciclinas")
    age_gt_65 = st.checkbox("Edad > 65 años")
    female_sex = st.checkbox("Sexo femenino")

st.divider()

st.header("Ecocardiografía basal")

col3, col4, col5 = st.columns(3)

with col3:
    lvef_percent = st.number_input(
        "FEVI (%)",
        min_value=0.0,
        max_value=100.0,
        value=55.0,
        step=1.0
    )

with col4:
    gls_input_abs = st.number_input(
        "GLS",
        min_value=0.0,
        max_value=50.0,
        value=20.0,
        step=0.1
    )

with col5:
    echo_operator = st.text_input("Operador", value=DEFAULT_ECHO_OPERATOR)

risk_factors = {
    "htn": htn,
    "dm": dm,
    "cad_pad": cad_pad,
    "prior_hf_cardiomyopathy": prior_hf_cardiomyopathy,
    "prior_anthracycline_exposure": prior_anthracycline_exposure,
    "prior_thoracic_rt": prior_thoracic_rt,
    "age_gt_65": age_gt_65,
    "female_sex": female_sex,
}

if st.button("Calcular riesgo"):
    if not patient_id.strip():
        st.error("Debes ingresar un Patient ID.")
        st.session_state["calculated"] = False
    elif not selected_treatments:
        st.error("Debes seleccionar al menos un tratamiento.")
        st.session_state["calculated"] = False
    else:
        result = calculate_full_risk(
            selected_labels=selected_treatments,
            catalog=catalog,
            risk_factors=risk_factors
        )

        domain_profile = build_domain_profile(
            treatment_items=result["treatment_items"],
            treatment_score=result["treatment_score"],
            anthracycline_cum_dose_mg_m2=anthracycline_cum_dose,
            prior_thoracic_rt=prior_thoracic_rt,
            thoracic_rt_planned=thoracic_rt_planned,
            patient_risk_factors=risk_factors,
        )

        recommendation_text = assemble_recommendation(
            result=result,
            domain_profile=domain_profile
        )

        gls_normalized = -abs(gls_input_abs)

        prediction_result = estimate_cv_event_probability(
            result=result,
            domain_profile=domain_profile,
            lvef_percent=lvef_percent,
            gls_percent=gls_normalized,
            anthracycline_cum_dose_mg_m2=anthracycline_cum_dose,
            risk_factors=risk_factors,
            thoracic_rt_planned=thoracic_rt_planned,
            prior_thoracic_rt=prior_thoracic_rt,
        )

        advanced_triage = build_advanced_triage(
            prediction_result=prediction_result,
            result=result,
            domain_profile=domain_profile,
            lvef_percent=lvef_percent,
            gls_percent=gls_normalized,
            anthracycline_cum_dose_mg_m2=anthracycline_cum_dose,
            thoracic_rt_planned=thoracic_rt_planned,
            prior_thoracic_rt=prior_thoracic_rt,
            symptomatic_or_functional_limitation=symptomatic_or_functional_limitation,
        )

        st.session_state["calculated"] = True
        st.session_state["result"] = result
        st.session_state["domain_profile"] = domain_profile
        st.session_state["recommendation_text"] = recommendation_text
        st.session_state["gls_normalized"] = gls_normalized
        st.session_state["saved_visit_id"] = None
        st.session_state["pdf_path"] = None
        st.session_state["prediction_result"] = prediction_result
        st.session_state["advanced_triage"] = advanced_triage

if st.session_state["calculated"] and st.session_state["result"] is not None:
    result = st.session_state["result"]
    domain_profile = st.session_state["domain_profile"]
    recommendation_text = st.session_state["recommendation_text"]
    gls_normalized = st.session_state["gls_normalized"]
    prediction_result = st.session_state["prediction_result"]
    advanced_triage = st.session_state["advanced_triage"]

    st.divider()

    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #0B3C6F 0%, #B22222 100%);
            padding: 14px 18px;
            border-radius: 12px;
            color: white;
            margin-bottom: 14px;
        ">
            <div style="font-size: 1.4rem; font-weight: 700;">Resultado</div>
            <div style="font-size: 0.95rem;">Evaluación cardio-oncológica estructurada</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Treatment Score", result["treatment_score"])
    c2.metric("Patient Score", result["patient_score"])
    c3.metric("Total Score", result["total_score"])
    c4.metric("Categoría", result["risk_category_es"])

    st.subheader("Predicción estimada de evento cardiovascular")
    p1, p2 = st.columns(2)
    p1.metric("Probabilidad estimada", f"{prediction_result['probability_percent']}%")
    p2.metric("Banda de riesgo predictiva", prediction_result["risk_band"])

    with st.expander("Drivers principales del predictor"):
        for driver in prediction_result["drivers"]:
            st.write(f"- {driver}")
        st.caption(f"Fuente del predictor: {prediction_result.get('source', 'desconocida')}")

    st.subheader("Triage avanzado HB")

    t1, t2 = st.columns(2)
    t1.metric("Biomarcadores basales", advanced_triage["baseline_biomarkers_recommendation"])
    t2.metric("CPET", advanced_triage["cpet_recommendation"])

    st.write(f"**Síntomas o limitación funcional:** {'Sí' if symptomatic_or_functional_limitation else 'No'}")

    with st.expander("Razones del triage avanzado"):
        for reason in advanced_triage["triage_reasons"]:
            st.write(f"- {reason}")

    st.subheader("Drivers principales del score")
    for driver in result["drivers"]:
        st.write(f"- {driver}")

    st.subheader("Tratamientos seleccionados")
    for item in result["treatment_items"]:
        st.write(
            f"- {item['label']} | CRS {item['crs_score']} | CTRCD {item['incidence_ctrcd']}"
        )

    st.subheader("Datos basales")
    st.write(f"**Patient ID:** {patient_id}")
    st.write(f"**Fecha de visita:** {visit_date}")
    st.write(f"**FEVI:** {lvef_percent}%")
    st.write(f"**GLS:** {gls_normalized}%")
    st.write(f"**Operador:** {echo_operator}")
    st.write(f"**Dosis acumulada antraciclina:** {anthracycline_cum_dose} mg/m²")
    st.write(f"**RT torácica actual/planificada:** {'Sí' if thoracic_rt_planned else 'No'}")
    st.write(f"**RT torácica previa:** {'Sí' if prior_thoracic_rt else 'No'}")
    st.write(f"**Síntomas o limitación funcional:** {'Sí' if symptomatic_or_functional_limitation else 'No'}")

    st.subheader("Dominios cardiovasculares detectados")

    for domain in domain_profile:
        if domain["domain_level"] != "not_relevant":
            level = domain["domain_level"]

            if level == "priority":
                color = "#B22222"
                bg = "#FFF5F5"
            elif level == "relevant":
                color = "#0B3C6F"
                bg = "#F4F8FC"
            elif level == "present":
                color = "#355C7D"
                bg = "#F8FAFC"
            else:
                color = "#6B7280"
                bg = "#F9FAFB"

            st.markdown(
                f"""
                <div style="
                    background-color: {bg};
                    border-left: 6px solid {color};
                    padding: 12px 14px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                ">
                    <div style="font-weight: 700; color: {color};">
                        {domain['domain_name_es']} → {domain['domain_level']}
                    </div>
                    <div style="font-size: 0.9rem; margin-top: 6px;">
                        {domain['domain_reason']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div style="
            background-color: #F8FAFC;
            border: 1px solid #D9E2EC;
            border-radius: 12px;
            padding: 16px;
            margin-top: 10px;
            margin-bottom: 10px;
        ">
            <div style="
                font-size: 1.1rem;
                font-weight: 700;
                color: #0B3C6F;
                margin-bottom: 8px;
            ">
                Recomendación inteligente
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(recommendation_text.replace("\n", "  \n"))

    col_save, col_pdf = st.columns(2)

    with col_save:
        if st.button("Guardar en base de datos"):
            try:
                save_patient(patient_id)

                visit_id = save_visit(
                    patient_id=patient_id,
                    visit_date=str(visit_date),
                    lvef_percent=lvef_percent,
                    gls_percent=gls_normalized,
                    echo_operator=echo_operator,
                    anthracycline_cum_dose_mg_m2=anthracycline_cum_dose,
                    thoracic_rt_planned=thoracic_rt_planned,
                    prior_thoracic_rt=prior_thoracic_rt,
                    treatment_risk_score=result["treatment_score"],
                    patient_risk_score=result["patient_score"],
                    total_risk_score=result["total_score"],
                    risk_category_es=result["risk_category_es"],
                    recommendation_text=recommendation_text,
                )

                save_visit_treatments(
                    visit_id=visit_id,
                    treatment_items=result["treatment_items"],
                    drivers=result["drivers"],
                )

                save_visit_risk_factors(
                    visit_id=visit_id,
                    risk_factors=risk_factors,
                )

                save_visit_domains(
                    visit_id=visit_id,
                    domain_profile=domain_profile,
                )

                st.session_state["saved_visit_id"] = visit_id
                st.success(f"Paciente guardado correctamente. Visit ID: {visit_id}")

            except Exception as e:
                st.error(f"Error al guardar en base de datos: {e}")

    with col_pdf:
        if st.button("Generar PDF"):
            try:
                pdf_path = generate_cardio_onco_pdf(
                    patient_id=patient_id,
                    visit_date=str(visit_date),
                    lvef_percent=lvef_percent,
                    gls_percent=gls_normalized,
                    echo_operator=echo_operator,
                    anthracycline_cum_dose_mg_m2=anthracycline_cum_dose,
                    thoracic_rt_planned=thoracic_rt_planned,
                    prior_thoracic_rt=prior_thoracic_rt,
                    symptomatic_or_functional_limitation=symptomatic_or_functional_limitation,
                    result=result,
                    domain_profile=domain_profile,
                    recommendation_text=recommendation_text,
                    prediction_result=prediction_result,
                    advanced_triage=advanced_triage,
                )

                st.session_state["pdf_path"] = pdf_path
                st.success("PDF generado correctamente.")

            except Exception as e:
                st.error(f"Error al generar PDF: {e}")

    if st.session_state["saved_visit_id"] is not None:
        st.success(f"Última visita guardada correctamente. Visit ID: {st.session_state['saved_visit_id']}")

    if st.session_state["pdf_path"]:
        with open(st.session_state["pdf_path"], "rb") as pdf_file:
            st.download_button(
                label="Descargar PDF",
                data=pdf_file,
                file_name=Path(st.session_state["pdf_path"]).name,
                mime="application/pdf"
            )
