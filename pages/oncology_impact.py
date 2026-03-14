import streamlit as st
import pandas as pd
from datetime import date

from data.repositories import get_all_visits, save_oncology_impact

st.set_page_config(page_title="Impacto oncológico", layout="wide")

st.title("Carga de impacto oncológico")
st.caption("Cardio-Onco HB | Registro clínico de impacto del evento cardiovascular sobre el tratamiento oncológico")

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

    st.subheader("Datos del impacto oncológico")

    col1, col2 = st.columns(2)

    with col1:
        impact_date = st.date_input("Fecha del impacto", value=date.today())

        impact_type = st.selectbox(
            "Tipo de impacto",
            options=[
                "none",
                "treatment_delayed",
                "treatment_reduced",
                "treatment_interrupted",
                "treatment_discontinued",
                "cardiology_clearance_required",
                "regimen_changed",
            ]
        )

    with col2:
        treatment_affected = st.text_input(
            "Tratamiento afectado",
            placeholder="Ej: Doxorubicin + Trastuzumab"
        )

    notes = st.text_area(
        "Notas clínicas",
        placeholder="Describí cómo impactó el evento CV sobre el tratamiento oncológico."
    )

    if st.button("Guardar impacto oncológico"):
        try:
            save_oncology_impact(
                patient_id=str(selected_row["patient_id"]),
                visit_id=int(selected_row["visit_id"]),
                impact_date=str(impact_date),
                impact_type=impact_type,
                treatment_affected=treatment_affected,
                notes=notes,
            )

            st.success("Impacto oncológico guardado correctamente.")

        except Exception as e:
            st.error(f"Error al guardar el impacto oncológico: {e}")
