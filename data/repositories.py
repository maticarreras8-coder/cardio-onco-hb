from data.db import get_connection


def save_patient(patient_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO patients (patient_id)
        VALUES (?)
        """,
        (patient_id,)
    )

    conn.commit()
    conn.close()


def save_visit(
    patient_id: str,
    visit_date: str,
    lvef_percent: float,
    gls_percent: float,
    echo_operator: str,
    anthracycline_cum_dose_mg_m2: float,
    thoracic_rt_planned: bool,
    prior_thoracic_rt: bool,
    symptomatic_or_functional_limitation: bool,
    troponin_basal,
    bnp_ntprobnp_basal,
    cpet_performed: bool,
    cpet_vo2_peak,
    cpet_percent_predicted,
    cpet_interpretation: str,
    treatment_risk_score: int,
    patient_risk_score: int,
    total_risk_score: int,
    risk_category_es: str,
    recommendation_text: str,
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO visits (
            patient_id,
            visit_date,
            lvef_percent,
            gls_percent,
            echo_operator,
            anthracycline_cum_dose_mg_m2,
            thoracic_rt_planned,
            prior_thoracic_rt,
            symptomatic_or_functional_limitation,
            troponin_basal,
            bnp_ntprobnp_basal,
            cpet_performed,
            cpet_vo2_peak,
            cpet_percent_predicted,
            cpet_interpretation,
            treatment_risk_score,
            patient_risk_score,
            total_risk_score,
            risk_category_es,
            recommendation_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            visit_date,
            lvef_percent,
            gls_percent,
            echo_operator,
            anthracycline_cum_dose_mg_m2,
            int(thoracic_rt_planned),
            int(prior_thoracic_rt),
            int(symptomatic_or_functional_limitation),
            troponin_basal,
            bnp_ntprobnp_basal,
            int(cpet_performed),
            cpet_vo2_peak,
            cpet_percent_predicted,
            cpet_interpretation,
            treatment_risk_score,
            patient_risk_score,
            total_risk_score,
            risk_category_es,
            recommendation_text,
        )
    )

    visit_id = cur.lastrowid
    conn.commit()
    conn.close()

    return visit_id


def save_visit_treatments(visit_id: int, treatment_items: list, drivers: list):
    conn = get_connection()
    cur = conn.cursor()

    for item in treatment_items:
        is_driver = 1 if item["label"] in drivers else 0

        cur.execute(
            """
            INSERT INTO visit_treatments (
                visit_id,
                class_name,
                drug_name,
                label,
                crs_score,
                incidence_ctrcd,
                other_manifestations,
                is_driver
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                visit_id,
                item.get("class", ""),
                item.get("drug", ""),
                item.get("label", ""),
                item.get("crs_score", 0),
                item.get("incidence_ctrcd", ""),
                item.get("other_manifestations", ""),
                is_driver,
            )
        )

    conn.commit()
    conn.close()


def save_visit_risk_factors(visit_id: int, risk_factors: dict):
    conn = get_connection()
    cur = conn.cursor()

    for factor_code, factor_value in risk_factors.items():
        cur.execute(
            """
            INSERT INTO visit_risk_factors (
                visit_id,
                factor_code,
                factor_value
            )
            VALUES (?, ?, ?)
            """,
            (
                visit_id,
                factor_code,
                int(bool(factor_value)),
            )
        )

    conn.commit()
    conn.close()


def save_visit_domains(visit_id: int, domain_profile: list):
    conn = get_connection()
    cur = conn.cursor()

    for domain in domain_profile:
        cur.execute(
            """
            INSERT INTO visit_domains (
                visit_id,
                domain_code,
                domain_name_es,
                domain_level,
                domain_reason
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                visit_id,
                domain.get("domain_code", ""),
                domain.get("domain_name_es", ""),
                domain.get("domain_level", ""),
                domain.get("domain_reason", ""),
            )
        )

    conn.commit()
    conn.close()


def save_cv_event(
    patient_id: str,
    visit_id: int,
    event_date: str,
    event_type: str,
    event_severity: str,
    event_description: str,
    hospitalization_required: bool,
    outcome_status: str,
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO cv_events (
            patient_id,
            visit_id,
            event_date,
            event_type,
            event_severity,
            event_description,
            hospitalization_required,
            outcome_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            visit_id,
            event_date,
            event_type,
            event_severity,
            event_description,
            int(hospitalization_required),
            outcome_status,
        )
    )

    conn.commit()
    conn.close()


def save_oncology_impact(
    patient_id: str,
    visit_id: int,
    impact_date: str,
    impact_type: str,
    treatment_affected: str,
    notes: str,
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO oncology_impact (
            patient_id,
            visit_id,
            impact_date,
            impact_type,
            treatment_affected,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            visit_id,
            impact_date,
            impact_type,
            treatment_affected,
            notes,
        )
    )

    conn.commit()
    conn.close()


def get_all_visits():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            visit_id,
            patient_id,
            visit_date,
            treatment_risk_score,
            patient_risk_score,
            total_risk_score,
            risk_category_es,
            lvef_percent,
            gls_percent,
            symptomatic_or_functional_limitation,
            troponin_basal,
            bnp_ntprobnp_basal,
            cpet_performed,
            cpet_vo2_peak,
            cpet_percent_predicted
        FROM visits
        ORDER BY visit_id DESC
        """
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_patient_visits(patient_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM visits
        WHERE patient_id = ?
        ORDER BY visit_date
        """,
        (patient_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_patient_cv_events(patient_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM cv_events
        WHERE patient_id = ?
        ORDER BY event_date DESC, cv_event_id DESC
        """,
        (patient_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_patient_oncology_impacts(patient_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM oncology_impact
        WHERE patient_id = ?
        ORDER BY impact_date DESC, oncology_impact_id DESC
        """,
        (patient_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_patient_treatments(patient_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            v.patient_id,
            v.visit_id,
            v.visit_date,
            vt.class_name,
            vt.drug_name,
            vt.label,
            vt.crs_score,
            vt.incidence_ctrcd,
            vt.other_manifestations,
            vt.is_driver
        FROM visit_treatments vt
        INNER JOIN visits v ON vt.visit_id = v.visit_id
        WHERE v.patient_id = ?
        ORDER BY v.visit_date DESC, vt.crs_score DESC
        """,
        (patient_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_ml_dataset():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
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
            v.risk_category_es,

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

            MAX(CASE WHEN e.cv_event_id IS NOT NULL THEN 1 ELSE 0 END) AS had_cv_event,
            MAX(CASE WHEN o.oncology_impact_id IS NOT NULL THEN 1 ELSE 0 END) AS had_oncology_impact

        FROM visits v
        LEFT JOIN visit_risk_factors rf ON v.visit_id = rf.visit_id
        LEFT JOIN visit_domains d ON v.visit_id = d.visit_id
        LEFT JOIN cv_events e ON v.visit_id = e.visit_id
        LEFT JOIN oncology_impact o ON v.visit_id = o.visit_id
        GROUP BY v.visit_id
        ORDER BY v.visit_id DESC
        """
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_all_cv_events():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            cv_event_id,
            patient_id,
            visit_id,
            event_date,
            event_type,
            event_severity,
            event_description,
            hospitalization_required,
            outcome_status
        FROM cv_events
        ORDER BY event_date DESC, cv_event_id DESC
        """
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_all_oncology_impacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            oncology_impact_id,
            patient_id,
            visit_id,
            impact_date,
            impact_type,
            treatment_affected,
            notes
        FROM oncology_impact
        ORDER BY impact_date DESC, oncology_impact_id DESC
        """
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_all_patients():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT patient_id, created_at
        FROM patients
        ORDER BY patient_id
        """
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def delete_patient(patient_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM cv_events WHERE patient_id = ?", (patient_id,))
    cur.execute("DELETE FROM oncology_impact WHERE patient_id = ?", (patient_id,))

    cur.execute(
        """
        DELETE FROM visit_treatments
        WHERE visit_id IN (SELECT visit_id FROM visits WHERE patient_id = ?)
        """,
        (patient_id,),
    )
    cur.execute(
        """
        DELETE FROM visit_risk_factors
        WHERE visit_id IN (SELECT visit_id FROM visits WHERE patient_id = ?)
        """,
        (patient_id,),
    )
    cur.execute(
        """
        DELETE FROM visit_domains
        WHERE visit_id IN (SELECT visit_id FROM visits WHERE patient_id = ?)
        """,
        (patient_id,),
    )

    cur.execute("DELETE FROM visits WHERE patient_id = ?", (patient_id,))
    cur.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))

    conn.commit()
    conn.close()


def delete_visit(visit_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM cv_events WHERE visit_id = ?", (visit_id,))
    cur.execute("DELETE FROM oncology_impact WHERE visit_id = ?", (visit_id,))
    cur.execute("DELETE FROM visit_treatments WHERE visit_id = ?", (visit_id,))
    cur.execute("DELETE FROM visit_risk_factors WHERE visit_id = ?", (visit_id,))
    cur.execute("DELETE FROM visit_domains WHERE visit_id = ?", (visit_id,))
    cur.execute("DELETE FROM visits WHERE visit_id = ?", (visit_id,))

    conn.commit()
    conn.close()


def delete_cv_event(cv_event_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM cv_events WHERE cv_event_id = ?", (cv_event_id,))

    conn.commit()
    conn.close()


def delete_oncology_impact(oncology_impact_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM oncology_impact WHERE oncology_impact_id = ?", (oncology_impact_id,))

    conn.commit()
    conn.close()
