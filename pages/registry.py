import streamlit as st
import pandas as pd

from data.repositories import delete_patient
from data.repositories import get_all_visits, get_patient_visits

st.set_page_config(page_title="Registro de pacientes", layout="wide")

st.title("Registro de pacientes")
st.caption("Cardio-Onco HB | Diego Rojas & Matías Carreras")

visits = get_all_visits()

if not visits:
    st.info("No hay visitas guardadas todavía.")
else:
    df = pd.DataFrame(visits)

    st.subheader("Resumen")

    c1, c2, c3 = st.columns(3)

    c1.metric("Cantidad de visitas", len(df))
    c2.metric("Pacientes únicos", df["patient_id"].nunique())
    c3.metric("Score promedio", round(df["total_risk_score"].mean(), 2))

    st.divider()

    st.subheader("Filtros")

    col1, col2 = st.columns(2)

    with col1:
        patient_filter = st.text_input("Buscar por Patient ID")

    with col2:
        risk_filter = st.selectbox(
            "Filtrar por categoría de riesgo",
            options=["Todas"] + sorted(df["risk_category_es"].dropna().unique().tolist())
        )

    filtered_df = df.copy()

    if patient_filter.strip():
        filtered_df = filtered_df[
            filtered_df["patient_id"].astype(str).str.contains(patient_filter.strip(), case=False, na=False)
        ]

    if risk_filter != "Todas":
        filtered_df = filtered_df[filtered_df["risk_category_es"] == risk_filter]

    st.divider()

    st.subheader("Visitas registradas")

    display_df = filtered_df.rename(
        columns={
            "visit_id": "Visit ID",
            "patient_id": "Patient ID",
            "visit_date": "Fecha",
            "treatment_risk_score": "Treatment Score",
            "patient_risk_score": "Patient Score",
            "total_risk_score": "Total Score",
            "risk_category_es": "Categoría",
            "lvef_percent": "FEVI",
            "gls_percent": "GLS",
        }
    )

    st.dataframe(display_df, use_container_width=True)

    st.caption(f"Mostrando {len(display_df)} de {len(df)} visitas")

    st.divider()

    st.subheader("Detalle de paciente")

    patient_list = sorted(df["patient_id"].unique())

    selected_patient = st.selectbox(
        "Seleccionar paciente",
        options=patient_list
    )

    if selected_patient:

        patient_visits = get_patient_visits(selected_patient)

        if patient_visits:

            pdf = pd.DataFrame(patient_visits)

            pdf = pdf.sort_values("visit_date")

            st.subheader(f"Evolución del paciente {selected_patient}")

            c1, c2, c3 = st.columns(3)

            c1.metric("Visitas", len(pdf))
            c2.metric("Última FEVI", pdf.iloc[-1]["lvef_percent"])
            c3.metric("Último score", pdf.iloc[-1]["total_risk_score"])

            st.divider()

            st.subheader("Evolución FEVI")

            fevi_df = pdf[["visit_date", "lvef_percent"]].rename(
                columns={"visit_date": "Fecha", "lvef_percent": "FEVI"}
            )

            st.line_chart(fevi_df.set_index("Fecha"))

            st.subheader("Evolución GLS")

            gls_df = pdf[["visit_date", "gls_percent"]].rename(
                columns={"visit_date": "Fecha", "gls_percent": "GLS"}
            )

            st.line_chart(gls_df.set_index("Fecha"))

            st.subheader("Evolución Score total")

            score_df = pdf[["visit_date", "total_risk_score"]].rename(
                columns={"visit_date": "Fecha", "total_risk_score": "Score"}
            )

            st.line_chart(score_df.set_index("Fecha"))

            st.divider()

            st.subheader("Historial completo")

            st.dataframe(pdf, use_container_width=True)

st.divider()

st.subheader("Eliminar paciente")

patient_to_delete = st.selectbox(
    "Seleccionar paciente a eliminar",
    options=patient_list
)

if st.button("Eliminar paciente"):
    delete_patient(patient_to_delete)
    st.success(f"Paciente {patient_to_delete} eliminado correctamente.")
    st.rerun()
