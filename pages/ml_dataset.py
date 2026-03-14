import streamlit as st
import pandas as pd

from data.repositories import get_ml_dataset

st.set_page_config(page_title="ML Dataset", layout="wide")

st.title("Dataset para Machine Learning")
st.caption("Cardio-Onco HB | Exportación estructurada para análisis predictivo")

rows = get_ml_dataset()

if not rows:
    st.info("Todavía no hay datos suficientes para construir el dataset.")
else:
    df = pd.DataFrame(rows)

    st.subheader("Vista previa del dataset")
    st.dataframe(df, use_container_width=True)

    st.subheader("Resumen")

    c1, c2, c3 = st.columns(3)

    c1.metric("Número de visitas", len(df))
    c2.metric("Eventos CV registrados", int(df["had_cv_event"].sum()))
    c3.metric("Impacto oncológico registrado", int(df["had_oncology_impact"].sum()))

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar dataset CSV",
        data=csv_data,
        file_name="cardio_onco_hb_ml_dataset.csv",
        mime="text/csv"
    )
