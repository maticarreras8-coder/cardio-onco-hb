import streamlit as st
import pandas as pd
from datetime import date

from data.repositories import get_all_visits, save_cv_event

st.set_page_config(page_title="Eventos cardiovasculares", layout="wide")

st.title("Carga de eventos cardiovasculares")
st.caption("Cardio-Onco HB | Registro clínico de outcomes cardiovasculares")

visits = get_all_visits()

if not visits:
    st.info("No hay visitas guardadas todavía. Primero guardá al menos una visita desde la calculadora.")
else:
    df = pd.DataFrame(visits)

    st.subheader("Seleccionar visita asociada")

    df["visit_label"] = (
        "Visit ID " + df["visit_id"].astype(str)
        + " | Patient ID " + df["patient_id"].astype(str)
        + " | Fecha " + df["visit_date"].astype(str)
    )

    selected_label = st.selectbox(
        "Visita",
        options=df["visit_label"].tolist()
    )

    selected_row = df[df["visit_label"] == selected_label].iloc[0]

    st.markdown(
        f"""
        **Patient ID:** {selected_row['patient_id']}  
        **Visit ID:** {selected_row['visit_id']}  
        **Fecha visita:** {selected_row['visit_date']}  
        **Score total:** {selected_row['total_risk_score']}  
        **Categoría:** {selected_row['risk_category_es']}
        """
    )

    st.divider()

    st.subheader("Datos del evento cardiovascular")

    col1, col2 = st.columns(2)

    with col1:
        event_date = st.date_input("Fecha del evento", value=date.today())

        event_type = st.selectbox(
            "Tipo de evento",
            options=[
                "heart_failure",
                "ctrcd",
                "arrhythmia",
                "qt_prolongation",
                "myocarditis",
                "pericarditis",
                "hypertension_crisis",
                "thromboembolism_venous",
                "thromboembolism_arterial",
                "ischemia",
                "other",
            ]
        )

        event_severity = st.selectbox(
            "Severidad",
            options=["mild", "moderate", "severe", "critical"]
        )

    with col2:
        hospitalization_required = st.checkbox("Requirió internación")

        outcome_status = st.selectbox(
            "Estado actual",
            options=["ongoing", "resolved", "improved", "worsened", "unknown"]
        )

    event_description = st.text_area(
        "Descripción clínica del evento",
        placeholder="Describí el evento cardiovascular, contexto, hallazgos, tratamiento y evolución."
    )

    if st.button("Guardar evento cardiovascular"):
        try:
            save_cv_event(
                patient_id=str(selected_row["patient_id"]),
                visit_id=int(selected_row["visit_id"]),
                event_date=str(event_date),
                event_type=event_type,
                event_severity=event_severity,
                event_description=event_description,
                hospitalization_required=hospitalization_required,
                outcome_status=outcome_status,
            )

            st.success("Evento cardiovascular guardado correctamente.")

        except Exception as e:
            st.error(f"Error al guardar el evento cardiovascular: {e}")
