from pathlib import Path
import pickle

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
from sklearn.ensemble import RandomForestClassifier

DB_PATH = "storage/cardio_onco_hb.db"
OUTPUT_DIR = Path("storage/ml_outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        v.visit_id,
        v.patient_id,
        v.visit_date,
        v.lvef_percent,
        v.gls_percent,
        v.anthracycline_cum_dose_mg_m2,
        v.thoracic_rt_planned,
        v.prior_thoracic_rt,
        v.symptomatic_or_functional_limitation,
        v.troponin_basal,
        v.bnp_ntprobnp_basal,
        v.cpet_performed,
        v.cpet_vo2_peak,
        v.cpet_percent_predicted,
        v.treatment_risk_score,
        v.patient_risk_score,
        v.total_risk_score,

        MAX(CASE WHEN rf.factor_code = 'htn' THEN rf.factor_value ELSE 0 END) AS htn,
        MAX(CASE WHEN rf.factor_code = 'dm' THEN rf.factor_value ELSE 0 END) AS dm,
        MAX(CASE WHEN rf.factor_code = 'cad_pad' THEN rf.factor_value ELSE 0 END) AS cad_pad,
        MAX(CASE WHEN rf.factor_code = 'prior_hf_cardiomyopathy' THEN rf.factor_value ELSE 0 END) AS prior_hf_cardiomyopathy,
        MAX(CASE WHEN rf.factor_code = 'prior_anthracycline_exposure' THEN rf.factor_value ELSE 0 END) AS prior_anthracycline_exposure,
        MAX(CASE WHEN rf.factor_code = 'prior_thoracic_rt' THEN rf.factor_value ELSE 0 END) AS prior_thoracic_rt_factor,
        MAX(CASE WHEN rf.factor_code = 'age_gt_65' THEN rf.factor_value ELSE 0 END) AS age_gt_65,
        MAX(CASE WHEN rf.factor_code = 'female_sex' THEN rf.factor_value ELSE 0 END) AS female_sex,

        MAX(CASE WHEN d.domain_code = 'ctr_cd' AND d.domain_level != 'not_relevant' THEN 1 ELSE 0 END) AS domain_ctr_cd,
        MAX(CASE WHEN d.domain_code = 'hypertension_vascular' AND d.domain_level != 'not_relevant' THEN 1 ELSE 0 END) AS domain_hypertension_vascular,
        MAX(CASE WHEN d.domain_code = 'thrombotic' AND d.domain_level != 'not_relevant' THEN 1 ELSE 0 END) AS domain_thrombotic,
        MAX(CASE WHEN d.domain_code = 'arrhythmic_qt' AND d.domain_level != 'not_relevant' THEN 1 ELSE 0 END) AS domain_arrhythmic_qt,
        MAX(CASE WHEN d.domain_code = 'inflammatory_myocarditis' AND d.domain_level != 'not_relevant' THEN 1 ELSE 0 END) AS domain_inflammatory_myocarditis,
        MAX(CASE WHEN d.domain_code = 'rt_late_effects' AND d.domain_level != 'not_relevant' THEN 1 ELSE 0 END) AS domain_rt_late_effects,

        MAX(CASE WHEN e.cv_event_id IS NOT NULL THEN 1 ELSE 0 END) AS had_cv_event

    FROM visits v
    LEFT JOIN visit_risk_factors rf ON v.visit_id = rf.visit_id
    LEFT JOIN visit_domains d ON v.visit_id = d.visit_id
    LEFT JOIN cv_events e ON v.visit_id = e.visit_id
    GROUP BY v.visit_id
    ORDER BY v.visit_id DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def prepare_data(df: pd.DataFrame):
    df = df.copy()

    feature_cols = [
        "lvef_percent",
        "gls_percent",
        "anthracycline_cum_dose_mg_m2",
        "thoracic_rt_planned",
        "prior_thoracic_rt",
        "symptomatic_or_functional_limitation",
        "troponin_basal",
        "bnp_ntprobnp_basal",
        "cpet_performed",
        "cpet_vo2_peak",
        "cpet_percent_predicted",
        "treatment_risk_score",
        "patient_risk_score",
        "total_risk_score",
        "htn",
        "dm",
        "cad_pad",
        "prior_hf_cardiomyopathy",
        "prior_anthracycline_exposure",
        "prior_thoracic_rt_factor",
        "age_gt_65",
        "female_sex",
        "domain_ctr_cd",
        "domain_hypertension_vascular",
        "domain_thrombotic",
        "domain_arrhythmic_qt",
        "domain_inflammatory_myocarditis",
        "domain_rt_late_effects",
    ]

    df[feature_cols] = df[feature_cols].fillna(0)
    df["had_cv_event"] = df["had_cv_event"].fillna(0).astype(int)

    X = df[feature_cols]
    y = df["had_cv_event"]

    return df, X, y, feature_cols


def train_model(X, y):
    if y.nunique() < 2:
        raise ValueError(
            "El outcome had_cv_event tiene una sola clase. Necesitás al menos un caso con evento y uno sin evento."
        )

    class_counts = y.value_counts()
    if class_counts.min() < 2:
        raise ValueError(
            "Cada clase necesita al menos 2 observaciones para usar train/test split estratificado."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "classification_report": classification_report(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    }

    return model, metrics


def save_feature_importance(model, feature_cols):
    importances = pd.DataFrame(
        {
            "feature": feature_cols,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    csv_path = OUTPUT_DIR / "feature_importance.csv"
    importances.to_csv(csv_path, index=False)

    plt.figure(figsize=(10, 7))
    plt.barh(importances["feature"], importances["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature importance - Random Forest")
    plt.tight_layout()
    fig_path = OUTPUT_DIR / "feature_importance.png"
    plt.savefig(fig_path, dpi=200)
    plt.close()

    return csv_path, fig_path, importances


def main():
    print("Cargando dataset desde SQLite...")
    df = load_dataset()

    if df.empty:
        print("No hay datos en la base.")
        return

    dataset_path = OUTPUT_DIR / "ml_dataset_snapshot.csv"
    df.to_csv(dataset_path, index=False)
    print(f"Dataset exportado a: {dataset_path}")

    df, X, y, feature_cols = prepare_data(df)

    print(f"Filas totales: {len(df)}")
    print("Distribución del outcome had_cv_event:")
    print(y.value_counts(dropna=False))

    try:
        model, metrics = train_model(X, y)
    except ValueError as e:
        print(f"No se pudo entrenar el modelo: {e}")
        return

    print("\nMétricas del modelo:")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"ROC AUC: {metrics['roc_auc']:.3f}")
    print("\nClassification report:")
    print(metrics["classification_report"])
    print("Confusion matrix:")
    print(metrics["confusion_matrix"])

    csv_path, fig_path, importances = save_feature_importance(model, feature_cols)

    model_path = OUTPUT_DIR / "cardio_onco_model.pkl"
    features_path = OUTPUT_DIR / "cardio_onco_model_features.pkl"

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    with open(features_path, "wb") as f:
        pickle.dump(feature_cols, f)

    print(f"\nModelo guardado en: {model_path}")
    print(f"Features guardadas en: {features_path}")
    print(f"Feature importance guardada en: {csv_path}")
    print(f"Gráfico guardado en: {fig_path}")
    print("\nTop 10 variables más importantes:")
    print(importances.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
