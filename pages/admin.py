import streamlit as st
import pandas as pd

from data.repositories import (
    get_all_patients,
    get_all_visits,
    get_all_cv_events,
    get_all_oncology_impacts,
    delete_patient,
    delete_visit,
    delete_cv_event,
    delete_oncology_impact,
)

st.set_page_config(page_title="Administración", layout="wide")

st.title("Administración")
st.caption("Cardio-Onco HB | Gestión de registros")

patients = get_all_patients()
visits = get_all_visits()
cv_events = get_all_cv_events()
oncology_impacts = get_all_oncology_impacts()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Pacientes", "Visitas", "Eventos CV", "Impacto oncológico"]
)

with tab1:
    st.subheader("Eliminar paciente completo")

    if not patients:
        st.info("No hay pacientes cargados.")
    else:
        patients_df = pd.DataFrame(patients)
        st.dataframe(patients_df, use_container_width=True)

        patient_options = patients_df["patient_id"].astype(str).tolist()
        patient_to_delete = st.selectbox("Seleccionar paciente", options=patient_options, key="delete_patient")

        confirm_patient = st.checkbox("Confirmo que quiero eliminar este paciente y todo su historial", key="confirm_patient")

        if st.button("Eliminar paciente", key="btn_delete_patient"):
            if not confirm_patient:
                st.warning("Debés confirmar la eliminación.")
            else:
                delete_patient(patient_to_delete)
                st.success(f"Paciente {patient_to_delete} eliminado correctamente.")
                st.rerun()

with tab2:
    st.subheader("Eliminar visita puntual")

    if not visits:
        st.info("No hay visitas cargadas.")
    else:
        visits_df = pd.DataFrame(visits)
        visits_df["visit_label"] = (
            "Visit ID " + visits_df["visit_id"].astype(str)
            + " | Patient ID " + visits_df["patient_id"].astype(str)
            + " | Fecha " + visits_df["visit_date"].astype(str)
        )

        st.dataframe(visits_df.drop(columns=["visit_label"]), use_container_width=True)

        visit_map = dict(zip(visits_df["visit_label"], visits_df["visit_id"]))
        visit_label = st.selectbox("Seleccionar visita", options=list(visit_map.keys()), key="delete_visit")

        confirm_visit = st.checkbox("Confirmo que quiero eliminar esta visita", key="confirm_visit")

        if st.button("Eliminar visita", key="btn_delete_visit"):
            if not confirm_visit:
                st.warning("Debés confirmar la eliminación.")
            else:
                delete_visit(int(visit_map[visit_label]))
                st.success("Visita eliminada correctamente.")
                st.rerun()

with tab3:
    st.subheader("Eliminar evento cardiovascular")

    if not cv_events:
        st.info("No hay eventos cardiovasculares cargados.")
    else:
        cv_df = pd.DataFrame(cv_events)
        cv_df["event_label"] = (
            "Event ID " + cv_df["cv_event_id"].astype(str)
            + " | Patient ID " + cv_df["patient_id"].astype(str)
            + " | Tipo " + cv_df["event_type"].astype(str)
            + " | Fecha " + cv_df["event_date"].astype(str)
        )

        st.dataframe(cv_df.drop(columns=["event_label"]), use_container_width=True)

        event_map = dict(zip(cv_df["event_label"], cv_df["cv_event_id"]))
        event_label = st.selectbox("Seleccionar evento CV", options=list(event_map.keys()), key="delete_cv_event")

        confirm_cv = st.checkbox("Confirmo que quiero eliminar este evento cardiovascular", key="confirm_cv")

        if st.button("Eliminar evento CV", key="btn_delete_cv_event"):
            if not confirm_cv:
                st.warning("Debés confirmar la eliminación.")
            else:
                delete_cv_event(int(event_map[event_label]))
                st.success("Evento cardiovascular eliminado correctamente.")
                st.rerun()

with tab4:
    st.subheader("Eliminar impacto oncológico")

    if not oncology_impacts:
        st.info("No hay impactos oncológicos cargados.")
    else:
        onc_df = pd.DataFrame(oncology_impacts)
        onc_df["impact_label"] = (
            "Impact ID " + onc_df["oncology_impact_id"].astype(str)
            + " | Patient ID " + onc_df["patient_id"].astype(str)
            + " | Tipo " + onc_df["impact_type"].astype(str)
            + " | Fecha " + onc_df["impact_date"].astype(str)
        )

        st.dataframe(onc_df.drop(columns=["impact_label"]), use_container_width=True)

        impact_map = dict(zip(onc_df["impact_label"], onc_df["oncology_impact_id"]))
        impact_label = st.selectbox("Seleccionar impacto oncológico", options=list(impact_map.keys()), key="delete_impact")

        confirm_impact = st.checkbox("Confirmo que quiero eliminar este impacto oncológico", key="confirm_impact")

        if st.button("Eliminar impacto oncológico", key="btn_delete_impact"):
            if not confirm_impact:
                st.warning("Debés confirmar la eliminación.")
            else:
                delete_oncology_impact(int(impact_map[impact_label]))
                st.success("Impacto oncológico eliminado correctamente.")
                st.rerun()
