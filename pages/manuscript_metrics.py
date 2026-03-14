import streamlit as st
import pandas as pd

from data.repositories import (
    get_all_patients,
    get_all_visits,
    get_all_cv_events,
    get_all_oncology_impacts,
)

st.set_page_config(page_title="Manuscript Metrics", layout="wide")

st.title("Manuscript Metrics")
st.caption("Cardio-Onco HB | Resumen de cohorte listo para manuscrito")

patients = get_all_patients()
visits = get_all_visits()
cv_events = get_all_cv_events()
oncology_impacts = get_all_oncology_impacts()

patients_df = pd.DataFrame(patients) if patients else pd.DataFrame()
visits_df = pd.DataFrame(visits) if visits else pd.DataFrame()
cv_df = pd.DataFrame(cv_events) if cv_events else pd.DataFrame()
onc_df = pd.DataFrame(oncology_impacts) if oncology_impacts else pd.DataFrame()

if visits_df.empty:
    st.info("Todavía no hay visitas guardadas para generar métricas.")
else:
    st.subheader("Resumen global")

    total_patients = len(patients_df)
    total_visits = len(visits_df)
    total_cv_events = len(cv_df)
    total_oncology_impacts = len(onc_df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pacientes", total_patients)
    c2.metric("Visitas", total_visits)
    c3.metric("Eventos CV", total_cv_events)
    c4.metric("Impacto oncológico", total_oncology_impacts)

    st.divider()

    st.subheader("Métricas descriptivas de la cohorte")

    desc = {}

    # FEVI
    if "lvef_percent" in visits_df.columns:
        desc["FEVI media"] = round(visits_df["lvef_percent"].dropna().mean(), 2) if visits_df["lvef_percent"].dropna().shape[0] > 0 else None
        desc["FEVI mediana"] = round(visits_df["lvef_percent"].dropna().median(), 2) if visits_df["lvef_percent"].dropna().shape[0] > 0 else None

    # GLS
    if "gls_percent" in visits_df.columns:
        desc["GLS medio"] = round(visits_df["gls_percent"].dropna().mean(), 2) if visits_df["gls_percent"].dropna().shape[0] > 0 else None
        desc["GLS mediano"] = round(visits_df["gls_percent"].dropna().median(), 2) if visits_df["gls_percent"].dropna().shape[0] > 0 else None

    # Scores
    if "total_risk_score" in visits_df.columns:
        desc["Score total medio"] = round(visits_df["total_risk_score"].dropna().mean(), 2) if visits_df["total_risk_score"].dropna().shape[0] > 0 else None
        desc["Score total mediano"] = round(visits_df["total_risk_score"].dropna().median(), 2) if visits_df["total_risk_score"].dropna().shape[0] > 0 else None

    # Biomarcadores y CPET
    if "troponin_basal" in visits_df.columns:
        desc["Troponina basal cargada (%)"] = round((visits_df["troponin_basal"].notna().mean() * 100), 1)
    if "bnp_ntprobnp_basal" in visits_df.columns:
        desc["BNP/NT-proBNP basal cargado (%)"] = round((visits_df["bnp_ntprobnp_basal"].notna().mean() * 100), 1)
    if "cpet_performed" in visits_df.columns:
        desc["CPET realizado (%)"] = round((visits_df["cpet_performed"].fillna(0).astype(int).mean() * 100), 1)
    if "symptomatic_or_functional_limitation" in visits_df.columns:
        desc["Síntomas/limitación funcional (%)"] = round((visits_df["symptomatic_or_functional_limitation"].fillna(0).astype(int).mean() * 100), 1)

    desc_df = pd.DataFrame(
        {"Métrica": list(desc.keys()), "Valor": list(desc.values())}
    )

    st.dataframe(desc_df, use_container_width=True)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Distribución por categoría de riesgo")

        if "risk_category_es" in visits_df.columns:
            risk_counts = visits_df["risk_category_es"].fillna("Sin dato").value_counts().reset_index()
            risk_counts.columns = ["Categoría", "n"]
            st.bar_chart(risk_counts.set_index("Categoría"))
            st.dataframe(risk_counts, use_container_width=True)
        else:
            st.info("No hay categoría de riesgo disponible.")

    with right:
        st.subheader("Eventos cardiovasculares por tipo")

        if cv_df.empty:
            st.info("No hay eventos CV registrados.")
        else:
            cv_counts = cv_df["event_type"].fillna("Sin dato").value_counts().reset_index()
            cv_counts.columns = ["Tipo de evento", "n"]
            st.bar_chart(cv_counts.set_index("Tipo de evento"))
            st.dataframe(cv_counts, use_container_width=True)

    st.divider()

    left2, right2 = st.columns(2)

    with left2:
        st.subheader("Impacto oncológico por tipo")

        if onc_df.empty:
            st.info("No hay impacto oncológico registrado.")
        else:
            onc_counts = onc_df["impact_type"].fillna("Sin dato").value_counts().reset_index()
            onc_counts.columns = ["Tipo de impacto", "n"]
            st.bar_chart(onc_counts.set_index("Tipo de impacto"))
            st.dataframe(onc_counts, use_container_width=True)

    with right2:
        st.subheader("Resumen tipo tabla 1")

        table1 = {
            "Pacientes únicos": total_patients,
            "Visitas totales": total_visits,
            "Eventos CV totales": total_cv_events,
            "Impactos oncológicos totales": total_oncology_impacts,
            "FEVI media": desc.get("FEVI media"),
            "GLS medio": desc.get("GLS medio"),
            "Score total medio": desc.get("Score total medio"),
            "Troponina basal cargada (%)": desc.get("Troponina basal cargada (%)"),
            "BNP/NT-proBNP basal cargado (%)": desc.get("BNP/NT-proBNP basal cargado (%)"),
            "CPET realizado (%)": desc.get("CPET realizado (%)"),
            "Síntomas/limitación funcional (%)": desc.get("Síntomas/limitación funcional (%)"),
        }

        table1_df = pd.DataFrame(
            {"Variable": list(table1.keys()), "Valor": list(table1.values())}
        )
        st.dataframe(table1_df, use_container_width=True)

    st.divider()

    st.subheader("Tablas exportables")

    visits_csv = visits_df.to_csv(index=False).encode("utf-8")
    cv_csv = cv_df.to_csv(index=False).encode("utf-8") if not cv_df.empty else b""
    onc_csv = onc_df.to_csv(index=False).encode("utf-8") if not onc_df.empty else b""
    desc_csv = desc_df.to_csv(index=False).encode("utf-8")
    table1_csv = table1_df.to_csv(index=False).encode("utf-8")

    d1, d2, d3, d4, d5 = st.columns(5)

    with d1:
        st.download_button(
            label="Descargar visitas CSV",
            data=visits_csv,
            file_name="cardio_onco_visits.csv",
            mime="text/csv",
        )

    with d2:
        st.download_button(
            label="Descargar eventos CV CSV",
            data=cv_csv,
            file_name="cardio_onco_cv_events.csv",
            mime="text/csv",
        )

    with d3:
        st.download_button(
            label="Descargar impacto oncológico CSV",
            data=onc_csv,
            file_name="cardio_onco_oncology_impact.csv",
            mime="text/csv",
        )

    with d4:
        st.download_button(
            label="Descargar descriptivos CSV",
            data=desc_csv,
            file_name="cardio_onco_descriptives.csv",
            mime="text/csv",
        )

    with d5:
        st.download_button(
            label="Descargar tabla 1 CSV",
            data=table1_csv,
            file_name="cardio_onco_table1.csv",
            mime="text/csv",
        )

    st.divider()

    st.subheader("Datos fuente")

    with st.expander("Ver visitas"):
        st.dataframe(visits_df, use_container_width=True)

    with st.expander("Ver eventos CV"):
        if cv_df.empty:
            st.info("No hay eventos CV.")
        else:
            st.dataframe(cv_df, use_container_width=True)

    with st.expander("Ver impacto oncológico"):
        if onc_df.empty:
            st.info("No hay impacto oncológico.")
        else:
            st.dataframe(onc_df, use_container_width=True)
