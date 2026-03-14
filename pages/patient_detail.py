import streamlit as st
import pandas as pd

from data.repositories import (
    get_all_patients,
    get_patient_visits,
    get_patient_cv_events,
    get_patient_oncology_impacts,
    get_patient_treatments,
)

st.set_page_config(page_title="Detalle del paciente", layout="wide")

st.title("Detalle del paciente")
st.caption("Cardio-Onco HB | Vista longitudinal individual")

patients = get_all_patients()

if not patients:
    st.info("No hay pacientes cargados todavía.")
else:
    patients_df = pd.DataFrame(patients)
    patient_options = patients_df["patient_id"].astype(str).tolist()

    selected_patient = st.selectbox(
        "Seleccionar paciente",
        options=patient_options
    )

    visits = get_patient_visits(selected_patient)
    cv_events = get_patient_cv_events(selected_patient)
    oncology_impacts = get_patient_oncology_impacts(selected_patient)
    treatments = get_patient_treatments(selected_patient)

    visits_df = pd.DataFrame(visits) if visits else pd.DataFrame()
    cv_df = pd.DataFrame(cv_events) if cv_events else pd.DataFrame()
    onc_df = pd.DataFrame(oncology_impacts) if oncology_impacts else pd.DataFrame()
    tx_df = pd.DataFrame(treatments) if treatments else pd.DataFrame()

    st.subheader(f"Resumen del paciente {selected_patient}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Visitas", len(visits_df))
    c2.metric("Eventos CV", len(cv_df))
    c3.metric("Impactos oncológicos", len(onc_df))
    c4.metric("Tratamientos registrados", len(tx_df))

    st.divider()

    if not visits_df.empty:
        visits_df = visits_df.sort_values("visit_date")

        st.subheader("Evolución FEVI")
        fevi_df = visits_df[["visit_date", "lvef_percent"]].rename(
            columns={"visit_date": "Fecha", "lvef_percent": "FEVI"}
        )
        st.line_chart(fevi_df.set_index("Fecha"))

        st.subheader("Evolución GLS")
        gls_df = visits_df[["visit_date", "gls_percent"]].rename(
            columns={"visit_date": "Fecha", "gls_percent": "GLS"}
        )
        st.line_chart(gls_df.set_index("Fecha"))

        st.subheader("Evolución score total")
        score_df = visits_df[["visit_date", "total_risk_score"]].rename(
            columns={"visit_date": "Fecha", "total_risk_score": "Score"}
        )
        st.line_chart(score_df.set_index("Fecha"))

        st.divider()

        st.subheader("Historial de visitas")
        st.dataframe(visits_df, use_container_width=True)
    else:
        st.info("No hay visitas registradas para este paciente.")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Eventos cardiovasculares")
        if cv_df.empty:
            st.info("No hay eventos cardiovasculares registrados.")
        else:
            st.dataframe(cv_df, use_container_width=True)

    with right:
        st.subheader("Impacto oncológico")
        if onc_df.empty:
            st.info("No hay impactos oncológicos registrados.")
        else:
            st.dataframe(onc_df, use_container_width=True)

    st.divider()

    st.subheader("Tratamientos registrados")
    if tx_df.empty:
        st.info("No hay tratamientos registrados para este paciente.")
    else:
        st.dataframe(tx_df, use_container_width=True)
