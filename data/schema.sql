CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS visits (
    visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    visit_date TEXT NOT NULL,
    lvef_percent REAL,
    gls_percent REAL,
    echo_operator TEXT,
    anthracycline_cum_dose_mg_m2 REAL,
    thoracic_rt_planned INTEGER,
    prior_thoracic_rt INTEGER,
    symptomatic_or_functional_limitation INTEGER DEFAULT 0,
    troponin_basal REAL,
    bnp_ntprobnp_basal REAL,
    cpet_performed INTEGER DEFAULT 0,
    cpet_vo2_peak REAL,
    cpet_percent_predicted REAL,
    cpet_interpretation TEXT,
    treatment_risk_score INTEGER,
    patient_risk_score INTEGER,
    total_risk_score INTEGER,
    risk_category_es TEXT,
    recommendation_text TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS visit_treatments (
    visit_treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id INTEGER NOT NULL,
    class_name TEXT,
    drug_name TEXT,
    label TEXT,
    crs_score INTEGER,
    incidence_ctrcd TEXT,
    other_manifestations TEXT,
    is_driver INTEGER,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);

CREATE TABLE IF NOT EXISTS visit_risk_factors (
    visit_risk_factor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id INTEGER NOT NULL,
    factor_code TEXT,
    factor_value INTEGER,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);

CREATE TABLE IF NOT EXISTS visit_domains (
    visit_domain_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id INTEGER NOT NULL,
    domain_code TEXT,
    domain_name_es TEXT,
    domain_level TEXT,
    domain_reason TEXT,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);

CREATE TABLE IF NOT EXISTS cv_events (
    cv_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    visit_id INTEGER,
    event_date TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_severity TEXT,
    event_description TEXT,
    hospitalization_required INTEGER DEFAULT 0,
    outcome_status TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);

CREATE TABLE IF NOT EXISTS oncology_impact (
    oncology_impact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    visit_id INTEGER,
    impact_date TEXT NOT NULL,
    impact_type TEXT NOT NULL,
    treatment_affected TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);