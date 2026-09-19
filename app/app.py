# ============================================================
# EarlySignal AI
# AI-Powered Early Warning and Decision Support
# ============================================================

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="EarlySignal AI | Early Warning Decision Support",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent
OUTPUT_DIR = BASE_DIR / "outputs"

PRIORITY_RESULTS_PATH = (
    OUTPUT_DIR / "early_warning_priority_results.csv"
)

FORECAST_RESULTS_PATH = (
    OUTPUT_DIR / "forecast_results.csv"
)

RISK_RESULTS_PATH = (
    OUTPUT_DIR / "risk_results.csv"
)

ANOMALY_RESULTS_PATH = (
    OUTPUT_DIR / "anomaly_results.csv"
)

EXPLAINABILITY_RESULTS_PATH = (
    OUTPUT_DIR / "explainability_results.csv"
)

MONITORING_DATA_PATH = (
    BASE_DIR
    / "data"
    / "synthetic"
    / "earlysignal_monitoring_data.csv"
)

# ------------------------------------------------------------
# EarlySignal AI monitoring-data schema
# ------------------------------------------------------------

REQUIRED_COLUMNS = [
    "record_id",
    "reporting_date",
    "programme_name",
    "sector",
    "state",
    "lga",
    "community",
    "monthly_target",
    "monthly_achievement",
    "achievement_rate",
    "activity_completion_rate",
    "budget_utilisation_rate",
    "reporting_delay_days",
    "complaints_count",
    "staff_availability_rate",
    "supply_delay_days",
    "previous_month_achievement_rate",
    "access_constraint_score",
    "data_quality_score"
]

OPTIONAL_COLUMNS = [
    "risk_label",
    "anomaly_flag",
    "recommended_action"
]

# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------

@st.cache_data
def load_priority_results():

    df = pd.read_csv(
        PRIORITY_RESULTS_PATH,
        parse_dates=["reporting_date"]
    )

    return df

@st.cache_data
def load_forecast_results():

    df = pd.read_csv(
        FORECAST_RESULTS_PATH,
        parse_dates=["reporting_date"]
    )

    return df

@st.cache_data
def load_risk_results():

    df = pd.read_csv(
        RISK_RESULTS_PATH,
        parse_dates=["reporting_date"]
    )

    return df

@st.cache_data
def load_anomaly_results():

    df = pd.read_csv(
        ANOMALY_RESULTS_PATH,
        parse_dates=["reporting_date"]
    )

    return df

@st.cache_data
def load_explainability_results():

    df = pd.read_csv(
        EXPLAINABILITY_RESULTS_PATH,
        parse_dates=["reporting_date"]
    )

    return df
    
@st.cache_data
def load_monitoring_data():

    df = pd.read_csv(
        MONITORING_DATA_PATH,
        parse_dates=["reporting_date"]
    )

    return df
    
try:
    data = load_priority_results()

except Exception as error:

    st.error(
        "EarlySignal AI could not load the "
        "priority-engine output."
    )

    st.exception(error)
    st.stop()


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def format_forecast(value):

    if pd.isna(value):
        return "Unavailable"

    return str(value)


def safe_text(value, fallback="Not available"):

    if pd.isna(value):
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    return value

def persistent_selectbox(
    container,
    label,
    options,
    state_key
):
    widget_key = f"_{state_key}"

    if state_key not in st.session_state:
        st.session_state[state_key] = options[0]

    if st.session_state[state_key] not in options:
        st.session_state[state_key] = options[0]

    st.session_state[widget_key] = (
        st.session_state[state_key]
    )

    def save_value():
        st.session_state[state_key] = (
            st.session_state[widget_key]
        )

    return container.selectbox(
        label,
        options,
        key=widget_key,
        on_change=save_value
    )
    
# ------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------

with st.sidebar:

    st.title("⚡ EarlySignal AI")

    st.caption(
        "AI-Powered Early Warning & Decision Support"
    )

    st.markdown(
        "**See the risk before it becomes the result.**"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Command Center",
            "Data Upload",
            "Performance Forecast",
            "Risk Intelligence",
            "Anomaly Detection",
            "Explainable AI",
            "Geographic Intelligence",
            "About & Responsible AI"
        ]
    )

    st.divider()

    st.markdown(
        "**Decision-Support Prototype**"
    )

    st.caption(
        "Combines forecasting, risk intelligence, anomaly "
        "detection and explainability to prioritize monitoring "
        "records for human review."
    )

    st.caption(
        "Validated using synthetic programme monitoring data. "
        "Outputs are not automated programme decisions."
    )

    st.divider()

    st.caption(
        "EarlySignal AI • Prototype V1"
    )

# ============================================================
# COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.title("Early Warning Command Center")

    st.markdown(
        "### See the risk before it becomes the result."
    )

    st.write(
        "EarlySignal AI combines risk intelligence, "
        "performance forecasting, anomaly detection and "
        "explainable AI to help programme teams identify "
        "where attention may be needed and why."
    )

    st.info(
        "Decision-support prototype: alerts identify records "
        "recommended for human review and do not automate "
        "programme decisions."
    )

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.subheader("Monitoring Filters")

    filter_col1, filter_col2, filter_col3, filter_col4 = (
        st.columns(4)
    )

    months = sorted(
        data["reporting_date"]
        .dropna()
        .dt.strftime("%Y-%m")
        .unique(),
        reverse=True
    )

    selected_month = filter_col1.selectbox(
        "Reporting Month",
        ["All Months"] + list(months)
    )

    programmes = sorted(
        data["programme_name"]
        .dropna()
        .unique()
    )

    selected_programme = filter_col2.selectbox(
        "Programme",
        ["All Programmes"] + list(programmes)
    )

    lgas = sorted(
        data["lga"]
        .dropna()
        .unique()
    )

    selected_lga = filter_col3.selectbox(
        "LGA",
        ["All LGAs"] + list(lgas)
    )

    selected_priority = filter_col4.selectbox(
        "Priority",
        [
            "All Priorities",
            "High",
            "Medium",
            "Low"
        ]
    )

    filtered_data = data.copy()

    if selected_month != "All Months":

        filtered_data = filtered_data[
            filtered_data["reporting_date"]
            .dt.strftime("%Y-%m")
            == selected_month
        ]

    if selected_programme != "All Programmes":

        filtered_data = filtered_data[
            filtered_data["programme_name"]
            == selected_programme
        ]

    if selected_lga != "All LGAs":

        filtered_data = filtered_data[
            filtered_data["lga"]
            == selected_lga
        ]

    if selected_priority != "All Priorities":

        filtered_data = filtered_data[
            filtered_data["early_warning_priority"]
            == selected_priority
        ]

    st.caption(
        f"Showing {len(filtered_data):,} of "
        f"{len(data):,} monitoring records."
    )

    # --------------------------------------------------------
    # KPI cards
    # --------------------------------------------------------

    total_records = len(filtered_data)

    high_priority = int(
        (
            filtered_data["early_warning_priority"]
            == "High"
        ).sum()
    )

    medium_priority = int(
        (
            filtered_data["early_warning_priority"]
            == "Medium"
        ).sum()
    )

    multiple_signal_alerts = int(
        filtered_data["signal_agreement"]
        .isin(
            [
                "Multiple Signals",
                "Strong Agreement"
            ]
        )
        .sum()
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Monitoring Records",
        f"{total_records:,}"
    )

    kpi2.metric(
        "High Priority",
        f"{high_priority:,}"
    )

    kpi3.metric(
        "Medium Priority",
        f"{medium_priority:,}"
    )

    kpi4.metric(
        "Multi-Signal Alerts",
        f"{multiple_signal_alerts:,}"
    )

    st.divider()

    # --------------------------------------------------------
    # Priority distribution + signal agreement
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    # --------------------------------------------------------
    # Priority distribution
    # --------------------------------------------------------

    with chart_col1:

        st.subheader("Priority Distribution")

        priority_order = [
            "High",
            "Medium",
            "Low"
        ]

        priority_counts = (
            filtered_data[
                "early_warning_priority"
            ]
            .value_counts()
            .reindex(
                priority_order,
                fill_value=0
            )
            .rename_axis("Priority")
            .reset_index(name="Records")
        )

        priority_total = priority_counts["Records"].sum()

        if priority_total > 0:

            priority_counts["Percentage"] = (
                priority_counts["Records"]
                / priority_total
                * 100
            )

        else:

            priority_counts["Percentage"] = 0.0

        priority_counts["Label"] = (
            priority_counts["Records"].map(
                lambda value: f"{value:,}"
            )
            + "  |  "
            + priority_counts["Percentage"].map(
                lambda value: f"{value:.1f}%"
            )
        )

        priority_chart = (
            alt.Chart(priority_counts)
            .mark_bar(
                cornerRadiusEnd=4
            )
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Monitoring Records"
                ),
                y=alt.Y(
                    "Priority:N",
                    sort=priority_order,
                    title=None
                ),
                color=alt.Color(
                    "Priority:N",
                    scale=alt.Scale(
                        domain=[
                            "High",
                            "Medium",
                            "Low"
                        ],
                        range=[
                            "#D62728",
                            "#F2A900",
                            "#2CA02C"
                        ]
                    ),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "Priority:N",
                        title="Priority"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share",
                        format=".1f"
                    )
                ]
            )
        )

        priority_labels = (
            alt.Chart(priority_counts)
            .mark_text(
                align="left",
                baseline="middle",
                dx=5
            )
            .encode(
                x=alt.X("Records:Q"),
                y=alt.Y(
                    "Priority:N",
                    sort=priority_order
                ),
                text="Label:N"
            )
        )

        st.altair_chart(
            priority_chart + priority_labels,
            width="stretch"
        )

        st.caption(
            "Distribution of integrated Early Warning "
            "Priority levels in the current view."
        )

    # --------------------------------------------------------
    # Signal agreement
    # --------------------------------------------------------

    with chart_col2:

        st.subheader("Signal Agreement")

        agreement_order = [
            "Strong Agreement",
            "Multiple Signals",
            "Single Signal",
            "No Warning Signal"
        ]

        agreement_counts = (
            filtered_data[
                "signal_agreement"
            ]
            .value_counts()
            .reindex(
                agreement_order,
                fill_value=0
            )
            .rename_axis("Signal Agreement")
            .reset_index(name="Records")
        )

        agreement_total = agreement_counts["Records"].sum()

        if agreement_total > 0:

            agreement_counts["Percentage"] = (
                agreement_counts["Records"]
                / agreement_total
                * 100
            )

        else:

            agreement_counts["Percentage"] = 0.0

        agreement_counts["Label"] = (
            agreement_counts["Records"].map(
                lambda value: f"{value:,}"
            )
            + "  |  "
            + agreement_counts["Percentage"].map(
                lambda value: f"{value:.1f}%"
            )
        )

        agreement_chart = (
            alt.Chart(agreement_counts)
            .mark_bar(
                cornerRadiusEnd=4
            )
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Monitoring Records"
                ),
                y=alt.Y(
                    "Signal Agreement:N",
                    sort=agreement_order,
                    title=None
                ),
                color=alt.Color(
                    "Signal Agreement:N",
                    scale=alt.Scale(
                        domain=agreement_order,
                        range=[
                            "#C62828",
                            "#EF6C00",
                            "#F9A825",
                            "#43A047"
                        ]
                    ),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "Signal Agreement:N",
                        title="Agreement"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share",
                        format=".1f"
                    )
                ]
            )
        )

        agreement_labels = (
            alt.Chart(agreement_counts)
            .mark_text(
                align="left",
                baseline="middle",
                dx=5
            )
            .encode(
                x=alt.X("Records:Q"),
                y=alt.Y(
                    "Signal Agreement:N",
                    sort=agreement_order
                ),
                text="Label:N"
            )
        )

        st.altair_chart(
            agreement_chart + agreement_labels,
            width="stretch"
        )

        st.caption(
            "Agreement across the available early-warning "
            "signals in the current view."
        )

    st.divider()

    # --------------------------------------------------------
    # Priority alerts
    # --------------------------------------------------------

    st.subheader("Priority Alert Queue")

    st.caption(
        "Alerts are ranked using the integrated "
        "Early Warning Priority Engine."
    )

    alerts = (
        filtered_data
        .sort_values(
            [
                "early_warning_score",
                "alert_rank"
            ],
            ascending=[
                False,
                True
            ]
        )
        .copy()
    )

    alert_table = alerts[
        [
            "alert_rank",
            "record_id",
            "programme_name",
            "lga",
            "community",
            "early_warning_score",
            "early_warning_priority",
            "predicted_risk",
            "signal_agreement",
            "primary_driver"
        ]
    ].copy()

    alert_table.columns = [
        "Rank",
        "Record ID",
        "Programme",
        "LGA",
        "Community",
        "Score",
        "Priority",
        "Risk",
        "Signal Agreement",
        "Main Driver"
    ]

    st.dataframe(
        alert_table.head(25),
        hide_index=True,
        width="stretch",
        column_config={
            "Rank": st.column_config.NumberColumn(
                "Rank",
                help="Integrated alert ranking",
                format="%d"
            ),
            "Record ID": st.column_config.TextColumn(
                "Record ID",
                help="Unique monitoring record identifier"
            ),
            "Programme": st.column_config.TextColumn(
                "Programme"
            ),
            "LGA": st.column_config.TextColumn(
                "LGA"
            ),
            "Community": st.column_config.TextColumn(
                "Community"
            ),
            "Score": st.column_config.ProgressColumn(
                "Early Warning Score",
                help=(
                    "Integrated prioritization score from "
                    "Risk Intelligence, Performance Forecast "
                    "and Anomaly Detection."
                ),
                format="%.0f",
                min_value=0,
                max_value=100
            ),
            "Priority": st.column_config.TextColumn(
                "Priority",
                help=(
                    "High ≥ 60 | Medium ≥ 30 and < 60 | "
                    "Low < 30"
                )
            ),
            "Risk": st.column_config.TextColumn(
                "Risk Intelligence"
            ),
            "Signal Agreement": st.column_config.TextColumn(
                "Signal Agreement",
                help=(
                    "Degree of agreement across available "
                    "early-warning signals."
                )
            ),
            "Main Driver": st.column_config.TextColumn(
                "Main Driver",
                help=(
                    "Primary operational signal contributing "
                    "to the risk explanation."
                )
            )
        }
    )

    st.caption(
        "Showing the 25 highest-ranked records "
        "for the current filter selection."
    )

    # --------------------------------------------------------
    # Alert investigation panel
    # --------------------------------------------------------

    st.divider()

    st.subheader("Alert Investigation Panel")

    st.write(
        "Select a monitoring record to understand "
        "why it was prioritized and what the programme "
        "team may investigate."
    )

    if alerts.empty:

        st.warning(
            "No monitoring records match the "
            "current filter selection."
        )

    else:

        alert_options = alerts["record_id"].tolist()

        selected_record_id = st.selectbox(
            "Select Alert",
            alert_options,
            format_func=lambda record_id: (
                f"{record_id} — "
                f"{alerts.loc[
                    alerts['record_id'] == record_id,
                    'programme_name'
                ].iloc[0]}"
            )
        )

        selected_alert = (
            alerts[
                alerts["record_id"]
                == selected_record_id
            ]
            .iloc[0]
        )

        st.markdown(
            f"### {safe_text(selected_alert['programme_name'])}"
        )

        st.write(
            f"**{safe_text(selected_alert['lga'])} — "
            f"{safe_text(selected_alert['community'])}**"
        )

        detail1, detail2, detail3, detail4 = (
            st.columns(4)
        )

        detail1.metric(
            "Early Warning Score",
            f"{selected_alert['early_warning_score']:.0f}/100"
        )

        detail2.metric(
            "Priority",
            safe_text(
                selected_alert[
                    "early_warning_priority"
                ]
            )
        )

        detail3.metric(
            "Risk Intelligence",
            safe_text(
                selected_alert["predicted_risk"]
            )
        )

        detail4.metric(
            "Signal Agreement",
            safe_text(
                selected_alert["signal_agreement"]
            )
        )

        detail5, detail6, detail7 = st.columns(3)

        detail5.metric(
            "Performance Forecast",
            format_forecast(
                selected_alert["forecast_status"]
            )
        )

        anomaly_display = (
            "Alert"
            if int(
                selected_alert[
                    "predicted_anomaly"
                ]
            ) == 1
            else "Normal"
        )

        detail6.metric(
            "Anomaly Detection",
            anomaly_display
        )

        detail7.metric(
            "Current Achievement",
            f"{selected_alert['achievement_rate']:.1%}"
        )

        st.markdown("#### Why this alert?")

        driver1, driver2, driver3 = st.columns(3)

        driver1.write(
            "**Primary Driver**"
        )

        driver1.write(
            safe_text(
                selected_alert["primary_driver"]
            )
        )

        driver2.write(
            "**Secondary Driver**"
        )

        driver2.write(
            safe_text(
                selected_alert["secondary_driver"]
            )
        )

        driver3.write(
            "**Tertiary Driver**"
        )

        driver3.write(
            safe_text(
                selected_alert["tertiary_driver"]
            )
        )

        protective_signal = safe_text(
            selected_alert[
                "strongest_protective_signal"
            ]
        )

        st.write(
            "**Strongest Protective Signal:** "
            f"{protective_signal}"
        )

        st.markdown(
            "#### Recommended Investigation"
        )

        st.warning(
            safe_text(
                selected_alert[
                    "integrated_investigation_guidance"
                ],
                fallback=(
                    "No specific investigation guidance "
                    "is available for this record."
                )
            )
        )

        st.write(
            "**Review Status:** "
            f"{safe_text(selected_alert['review_status'])}"
        )

        st.caption(
            safe_text(
                selected_alert["decision_use"]
            )
        )

    st.divider()

    st.caption(
        "Early Warning Score = Risk Intelligence (50%) + "
        "Performance Forecast (30%) + "
        "Anomaly Detection (20%). "
        "When held-out forecast evidence is unavailable, "
        "available component weights are renormalized. "
        "The score is a prioritization index, not a "
        "probability of programme failure."
    )


# ============================================================
# DATA UPLOAD & READINESS
# ============================================================

elif page == "Data Upload":

    st.title("Data Upload & Readiness")

    st.markdown(
        "### Prepare monitoring data for early-warning analysis."
    )

    st.write(
        "Upload programme monitoring data and EarlySignal AI "
        "will assess whether the dataset contains the structure "
        "and information required by the prototype analytical pipeline."
    )

    st.info(
        "This module performs data-readiness validation only. "
        "Uploading a dataset does not automatically trigger operational "
        "decisions or guarantee that it is suitable for model inference."
    )

    # --------------------------------------------------------
    # File uploader
    # --------------------------------------------------------

    uploaded_file = st.file_uploader(
        "Upload monitoring data",
        type=["csv"],
        help="Upload a CSV file using the EarlySignal AI monitoring-data structure.",
        key="monitoring_data_uploader"
    )
    
    if uploaded_file is not None:
        try:
            st.session_state["uploaded_monitoring_data"] = pd.read_csv(
                uploaded_file
            )
            st.session_state["uploaded_monitoring_filename"] = (
                uploaded_file.name
            )
    
        except Exception as error:
            st.error(
                "The uploaded CSV could not be read."
            )
            st.exception(error)
            st.stop()
    
    uploaded_data = st.session_state.get(
        "uploaded_monitoring_data"
    )

    if uploaded_data is not None:
        uploaded_filename = st.session_state.get(
            "uploaded_monitoring_filename",
            "Uploaded dataset"
        )
    
        clear_col1, clear_col2 = st.columns(
            [4, 1]
        )
    
        clear_col1.caption(
            f"Active dataset: {uploaded_filename}"
        )
    
        if clear_col2.button(
            "Clear uploaded data",
            key="clear_uploaded_monitoring_data"
        ):
            st.session_state.pop(
                "uploaded_monitoring_data",
                None
            )
            st.session_state.pop(
                "uploaded_monitoring_filename",
                None
            )
            st.rerun()

    if uploaded_data is None:

        st.subheader("Expected Data Structure")

        st.write(
            "EarlySignal AI expects programme monitoring records "
            "containing identifiers, reporting periods, programme and "
            "location information, implementation indicators and "
            "operational warning signals."
        )

        schema_df = pd.DataFrame(
            {
                "Required Field": REQUIRED_COLUMNS
            }
        )

        st.dataframe(
            schema_df,
            hide_index=True,
            width="stretch"
        )

        st.caption(
            "Risk labels, anomaly labels and recommended actions are "
            "not required from uploaded organizational monitoring data."
        )

    else:

        # ----------------------------------------------------
        # Read uploaded CSV
        # ----------------------------------------------------


        st.success(
            "File uploaded successfully."
        )

        # ----------------------------------------------------
        # Basic dataset profile
        # ----------------------------------------------------

        total_rows = len(uploaded_data)
        total_columns = len(uploaded_data.columns)

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in uploaded_data.columns
        ]

        available_required = [
            column
            for column in REQUIRED_COLUMNS
            if column in uploaded_data.columns
        ]

        required_fields_present = len(
            available_required
        )

        required_fields_total = len(
            REQUIRED_COLUMNS
        )

        schema_coverage = (
            required_fields_present
            / required_fields_total
            * 100
        )

        total_missing_values = int(
            uploaded_data.isna().sum().sum()
        )

        duplicate_rows = int(
            uploaded_data.duplicated().sum()
        )

        profile1, profile2, profile3, profile4 = (
            st.columns(4)
        )

        profile1.metric(
            "Records",
            f"{total_rows:,}"
        )

        profile2.metric(
            "Variables",
            f"{total_columns:,}"
        )

        profile3.metric(
            "Required Fields",
            f"{required_fields_present}/{required_fields_total}"
        )

        profile4.metric(
            "Schema Coverage",
            f"{schema_coverage:.0f}%"
        )

        st.divider()

        # ----------------------------------------------------
        # Readiness checks
        # ----------------------------------------------------

        st.subheader("Data Readiness Assessment")

        schema_ready = len(missing_columns) == 0

        no_duplicate_rows = duplicate_rows == 0

        if available_required:

            missing_required_values = int(
                uploaded_data[
                    available_required
                ]
                .isna()
                .sum()
                .sum()
            )

        else:

            missing_required_values = 0

        required_values_complete = (
            missing_required_values == 0
        )

        record_id_unique = False

        if "record_id" in uploaded_data.columns:

            record_id_unique = (
                uploaded_data["record_id"]
                .dropna()
                .is_unique
            )

        valid_dates = False
        invalid_date_count = None

        if "reporting_date" in uploaded_data.columns:

            parsed_dates = pd.to_datetime(
                uploaded_data["reporting_date"],
                errors="coerce"
            )

            invalid_date_count = int(
                parsed_dates.isna().sum()
            )

            valid_dates = (
                invalid_date_count == 0
            )

        readiness_checks = pd.DataFrame(
            {
                "Readiness Check": [
                    "Required schema complete",
                    "Required fields contain no missing values",
                    "No exact duplicate rows",
                    "Record IDs are unique",
                    "Reporting dates are valid"
                ],
                "Status": [
                    "PASS" if schema_ready else "REVIEW",
                    (
                        "PASS"
                        if required_values_complete
                        else "REVIEW"
                    ),
                    (
                        "PASS"
                        if no_duplicate_rows
                        else "REVIEW"
                    ),
                    (
                        "PASS"
                        if record_id_unique
                        else "REVIEW"
                    ),
                    (
                        "PASS"
                        if valid_dates
                        else "REVIEW"
                    )
                ]
            }
        )

        st.dataframe(
            readiness_checks,
            hide_index=True,
            width="stretch"
        )

        # ----------------------------------------------------
        # Overall readiness
        # ----------------------------------------------------

        all_checks_passed = (
            schema_ready
            and required_values_complete
            and no_duplicate_rows
            and record_id_unique
            and valid_dates
        )

        if all_checks_passed:

            st.success(
                "READY FOR PROTOTYPE ANALYSIS — "
                "The uploaded dataset passes the core "
                "EarlySignal AI structural readiness checks."
            )

        elif schema_ready:

            st.warning(
                "REVIEW REQUIRED — The required schema is present, "
                "but one or more data-quality checks require review "
                "before analytical use."
            )

        else:

            st.error(
                "NOT YET READY — Required EarlySignal AI fields "
                "are missing from the uploaded dataset."
            )

        # ----------------------------------------------------
        # Data-quality details
        # ----------------------------------------------------

        st.subheader("Data Quality Details")

        quality1, quality2, quality3 = st.columns(3)

        quality1.metric(
            "Missing Values",
            f"{total_missing_values:,}"
        )

        quality2.metric(
            "Duplicate Rows",
            f"{duplicate_rows:,}"
        )

        quality3.metric(
            "Missing Required Fields",
            f"{len(missing_columns):,}"
        )

        if missing_columns:

            st.warning(
                "Missing required fields: "
                + ", ".join(missing_columns)
            )

        else:

            st.success(
                "All required EarlySignal AI fields are present."
            )

        # ----------------------------------------------------
        # Reporting-period coverage
        # ----------------------------------------------------

        if (
            "reporting_date" in uploaded_data.columns
            and valid_dates
            and not uploaded_data.empty
        ):

            parsed_dates = pd.to_datetime(
                uploaded_data["reporting_date"]
            )

            min_date = parsed_dates.min()
            max_date = parsed_dates.max()

            unique_months = (
                parsed_dates
                .dt.to_period("M")
                .nunique()
            )

            st.subheader("Reporting Coverage")

            coverage1, coverage2, coverage3 = (
                st.columns(3)
            )

            coverage1.metric(
                "First Reporting Period",
                min_date.strftime("%b %Y")
            )

            coverage2.metric(
                "Latest Reporting Period",
                max_date.strftime("%b %Y")
            )

            coverage3.metric(
                "Reporting Months",
                f"{unique_months:,}"
            )

        # ----------------------------------------------------
        # Panel-structure audit
        # ----------------------------------------------------

        panel_columns = [
            "programme_name",
            "state",
            "lga",
            "community",
            "reporting_date"
        ]

        if all(
            column in uploaded_data.columns
            for column in panel_columns
        ):

            panel_data = uploaded_data[
                panel_columns
            ].copy()

            panel_data["reporting_date"] = (
                pd.to_datetime(
                    panel_data["reporting_date"],
                    errors="coerce"
                )
            )

            panel_data["reporting_month"] = (
                panel_data["reporting_date"]
                .dt.to_period("M")
            )

            duplicate_panel_records = int(
                panel_data.duplicated(
                    subset=[
                        "programme_name",
                        "state",
                        "lga",
                        "community",
                        "reporting_month"
                    ]
                ).sum()
            )

            st.subheader("Panel Structure")

            if duplicate_panel_records == 0:

                st.success(
                    "No duplicate programme/location/community/month "
                    "records were detected."
                )

            else:

                st.warning(
                    f"{duplicate_panel_records:,} duplicate "
                    "programme/location/community/month records "
                    "were detected and should be reviewed."
                )

        # ----------------------------------------------------
        # Preview
        # ----------------------------------------------------

        st.subheader("Uploaded Data Preview")

        st.dataframe(
            uploaded_data.head(20),
            hide_index=True,
            width="stretch"
        )

        st.caption(
            "Previewing the first 20 records. "
            "Data remains subject to human review before "
            "operational interpretation."
        )

        # ----------------------------------------------------
        # Prototype boundary
        # ----------------------------------------------------

        st.divider()

        st.markdown("### What happens next?")

        st.write(
            "A dataset that passes these checks is structurally "
            "compatible with the EarlySignal AI prototype. "
            "Model inference requires the appropriate preprocessing, "
            "temporal history and model-validation conditions."
        )

        st.warning(
            "Prototype boundary: this upload page does not yet score "
            "arbitrary organizational datasets with the trained models. "
            "This prevents the application from presenting unsupported "
            "predictions when data definitions or operating contexts differ."
        )


# ============================================================
# PERFORMANCE FORECAST
# ============================================================

elif page == "Performance Forecast":

    st.title("Performance Forecast")

    st.markdown(
        "### Anticipate next-month programme performance."
    )

    st.write(
        "The Performance Forecast module estimates next-month "
        "achievement using recent implementation performance, "
        "operational conditions and temporal monitoring signals."
    )

    st.info(
        "Forecasts are decision-support signals validated on "
        "synthetic monitoring data. They are recommended for "
        "human review and should not be treated as guaranteed outcomes."
    )

    # --------------------------------------------------------
    # Load forecast results
    # --------------------------------------------------------

    try:

        forecast_data = load_forecast_results()

    except Exception as error:

        st.error(
            "EarlySignal AI could not load the "
            "performance-forecast results."
        )

        st.exception(error)
        st.stop()

    # --------------------------------------------------------
    # Forecast filters
    # --------------------------------------------------------

    st.subheader("Forecast Filters")

    fc1, fc2, fc3, fc4 = st.columns(4)

    forecast_months = sorted(
        forecast_data["reporting_date"]
        .dropna()
        .dt.strftime("%Y-%m")
        .unique(),
        reverse=True
    )

    forecast_month = persistent_selectbox(
        fc1,
        "Reporting Month",
        ["All Months"] + list(forecast_months),
        "forecast_month"
    )

    forecast_programmes = sorted(
        forecast_data["programme_name"]
        .dropna()
        .unique()
    )

    forecast_programme = persistent_selectbox(
        fc2,
        "Programme",
        ["All Programmes"] + list(forecast_programmes),
        "forecast_programme"
    )

    forecast_lgas = sorted(
        forecast_data["lga"]
        .dropna()
        .unique()
    )

    forecast_lga = persistent_selectbox(
        fc3,
        "LGA",
        ["All LGAs"] + list(forecast_lgas),
        "forecast_lga"
    )

    forecast_status_filter = persistent_selectbox(
        fc4,
        "Forecast Status",
        [
            "All Statuses",
            "Critical",
            "Watch",
            "On Track"
        ],
        "forecast_status_filter"
    )

    filtered_forecast = forecast_data.copy()

    if forecast_month != "All Months":

        filtered_forecast = filtered_forecast[
            filtered_forecast["reporting_date"]
            .dt.strftime("%Y-%m")
            == forecast_month
        ]

    if forecast_programme != "All Programmes":

        filtered_forecast = filtered_forecast[
            filtered_forecast["programme_name"]
            == forecast_programme
        ]

    if forecast_lga != "All LGAs":

        filtered_forecast = filtered_forecast[
            filtered_forecast["lga"]
            == forecast_lga
        ]

    if forecast_status_filter != "All Statuses":

        filtered_forecast = filtered_forecast[
            filtered_forecast["forecast_status"]
            == forecast_status_filter
        ]

    st.caption(
        f"Showing {len(filtered_forecast):,} of "
        f"{len(forecast_data):,} held-out forecast records."
    )

    # --------------------------------------------------------
    # Forecast KPIs
    # --------------------------------------------------------

    total_forecasts = len(filtered_forecast)

    critical_forecasts = int(
        (
            filtered_forecast["forecast_status"]
            == "Critical"
        ).sum()
    )

    watch_forecasts = int(
        (
            filtered_forecast["forecast_status"]
            == "Watch"
        ).sum()
    )

    on_track_forecasts = int(
        (
            filtered_forecast["forecast_status"]
            == "On Track"
        ).sum()
    )

    fk1, fk2, fk3, fk4 = st.columns(4)

    fk1.metric(
        "Forecast Records",
        f"{total_forecasts:,}"
    )

    fk2.metric(
        "Critical",
        f"{critical_forecasts:,}"
    )

    fk3.metric(
        "Watch",
        f"{watch_forecasts:,}"
    )

    fk4.metric(
        "On Track",
        f"{on_track_forecasts:,}"
    )

    st.divider()

    # --------------------------------------------------------
    # Status distribution
    # --------------------------------------------------------

    chart1, chart2 = st.columns(2)

    with chart1:

        st.subheader("Forecast Status Distribution")

        forecast_status_order = [
            "Critical",
            "Watch",
            "On Track"
        ]

        forecast_counts = (
            filtered_forecast["forecast_status"]
            .value_counts()
            .reindex(
                forecast_status_order,
                fill_value=0
            )
            .rename_axis("Forecast Status")
            .reset_index(name="Records")
        )

        forecast_total = forecast_counts["Records"].sum()

        if forecast_total > 0:

            forecast_counts["Percentage"] = (
                forecast_counts["Records"]
                / forecast_total
                * 100
            )

        else:

            forecast_counts["Percentage"] = 0.0

        forecast_counts["Label"] = (
            forecast_counts["Records"].map(
                lambda value: f"{value:,}"
            )
            + "  |  "
            + forecast_counts["Percentage"].map(
                lambda value: f"{value:.1f}%"
            )
        )

        forecast_status_chart = (
            alt.Chart(forecast_counts)
            .mark_bar(
                cornerRadiusEnd=4
            )
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Forecast Records"
                ),
                y=alt.Y(
                    "Forecast Status:N",
                    sort=forecast_status_order,
                    title=None
                ),
                color=alt.Color(
                    "Forecast Status:N",
                    scale=alt.Scale(
                        domain=[
                            "Critical",
                            "Watch",
                            "On Track"
                        ],
                        range=[
                            "#D62728",
                            "#F2A900",
                            "#2CA02C"
                        ]
                    ),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "Forecast Status:N",
                        title="Status"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share",
                        format=".1f"
                    )
                ]
            )
        )

        forecast_status_labels = (
            alt.Chart(forecast_counts)
            .mark_text(
                align="left",
                baseline="middle",
                dx=5
            )
            .encode(
                x=alt.X("Records:Q"),
                y=alt.Y(
                    "Forecast Status:N",
                    sort=forecast_status_order
                ),
                text="Label:N"
            )
        )

        st.altair_chart(
            forecast_status_chart
            + forecast_status_labels,
            width="stretch"
        )

        st.caption(
            "Distribution of predicted next-month "
            "performance statuses in the current view."
        )

    # --------------------------------------------------------
    # Programme outlook
    # --------------------------------------------------------

    with chart2:

        st.subheader("Programme Forecast Outlook")

        if filtered_forecast.empty:

            st.info(
                "No records match the current filters."
            )

        else:

            programme_outlook = (
                filtered_forecast
                .groupby(
                    "programme_name",
                    as_index=False
                )[
                    "predicted_next_achievement_rate"
                ]
                .mean()
                .rename(
                    columns={
                        "predicted_next_achievement_rate":
                        "Predicted Achievement"
                    }
                )
                .sort_values(
                    "Predicted Achievement"
                )
            )

            programme_outlook[
                "Predicted Achievement %"
            ] = (
                programme_outlook[
                    "Predicted Achievement"
                ]
                * 100
            )

            programme_outlook["Label"] = (
                programme_outlook[
                    "Predicted Achievement %"
                ]
                .map(
                    lambda value: f"{value:.1f}%"
                )
            )

            programme_chart = (
                alt.Chart(programme_outlook)
                .mark_bar(
                    cornerRadiusEnd=4
                )
                .encode(
                    x=alt.X(
                        "Predicted Achievement %:Q",
                        title=(
                            "Average Predicted "
                            "Next Achievement (%)"
                        ),
                        scale=alt.Scale(
                            domain=[0, 100]
                        )
                    ),
                    y=alt.Y(
                        "programme_name:N",
                        sort=alt.SortField(
                            field="Predicted Achievement %",
                            order="ascending"
                        ),
                        title=None
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "programme_name:N",
                            title="Programme"
                        ),
                        alt.Tooltip(
                            "Predicted Achievement %:Q",
                            title=(
                                "Predicted Next Achievement"
                            ),
                            format=".1f"
                        )
                    ]
                )
            )

            programme_labels = (
                alt.Chart(programme_outlook)
                .mark_text(
                    align="left",
                    baseline="middle",
                    dx=5
                )
                .encode(
                    x=alt.X(
                        "Predicted Achievement %:Q"
                    ),
                    y=alt.Y(
                        "programme_name:N",
                        sort=alt.SortField(
                            field="Predicted Achievement %",
                            order="ascending"
                        )
                    ),
                    text="Label:N"
                )
            )

            st.altair_chart(
                programme_chart
                + programme_labels,
                width="stretch"
            )

            st.caption(
                "Average predicted next-month achievement "
                "by programme for the current filter selection."
            )

    st.divider()

    # --------------------------------------------------------
    # Model validation evidence
    # --------------------------------------------------------

    st.subheader("Forecast Model Evidence")

    st.write(
        "The Random Forest forecast model was evaluated on a "
        "future held-out period rather than randomly splitting "
        "records across time."
    )

    mv1, mv2, mv3, mv4 = st.columns(4)

    mv1.metric(
        "MAE",
        "0.0507"
    )

    mv2.metric(
        "RMSE",
        "0.0680"
    )

    mv3.metric(
        "R²",
        "0.3469"
    )

    mv4.metric(
        "MAE vs Baseline",
        "13.84% better"
    )

    st.caption(
        "Held-out evaluation: 1,440 forecast records. "
        "The model also improved RMSE by 16.67% compared with "
        "the naive previous-performance baseline. Results reflect "
        "prototype validation on synthetic monitoring data."
    )

    # --------------------------------------------------------
    # Forecast thresholds
    # --------------------------------------------------------

    with st.expander(
        "How are forecast statuses defined?"
    ):

        st.write(
            "**Critical:** predicted next achievement below 65%."
        )

        st.write(
            "**Watch:** predicted next achievement from "
            "65% to below 75%."
        )

        st.write(
            "**On Track:** predicted next achievement "
            "of 75% or higher."
        )

        st.caption(
            "These thresholds are prototype decision-support "
            "categories and should be calibrated to organizational "
            "targets and programme context before operational use."
        )

    st.divider()

    # --------------------------------------------------------
    # Forecast watchlist
    # --------------------------------------------------------

    st.subheader("Forecast Watchlist")

    st.caption(
        "Records with the lowest predicted next-month "
        "achievement appear first."
    )

    if filtered_forecast.empty:

        st.warning(
            "No forecast records match the current filters."
        )

    else:

        forecast_watchlist = (
            filtered_forecast
            .sort_values(
                "predicted_next_achievement_rate",
                ascending=True
            )
            .copy()
        )

        forecast_table = forecast_watchlist[
            [
                "record_id",
                "programme_name",
                "lga",
                "community",
                "achievement_rate",
                "predicted_next_achievement_rate",
                "forecast_status",
                "absolute_forecast_error"
            ]
        ].copy()

        forecast_table.columns = [
            "Record ID",
            "Programme",
            "LGA",
            "Community",
            "Current Achievement",
            "Predicted Next Achievement",
            "Status",
            "Held-Out Error"
        ]

        # Convert rates to percentage points for display only.
        forecast_table["Current Achievement"] = (
            forecast_table["Current Achievement"] * 100
        )

        forecast_table["Predicted Next Achievement"] = (
            forecast_table["Predicted Next Achievement"] * 100
        )

        st.dataframe(
            forecast_table.head(25),
            hide_index=True,
            width="stretch",
            column_config={
                "Record ID": st.column_config.TextColumn(
                    "Record ID",
                    help="Unique monitoring record identifier"
                ),
                "Programme": st.column_config.TextColumn(
                    "Programme"
                ),
                "LGA": st.column_config.TextColumn(
                    "LGA"
                ),
                "Community": st.column_config.TextColumn(
                    "Community"
                ),
                "Current Achievement":
                    st.column_config.ProgressColumn(
                        "Current Achievement",
                        help=(
                            "Achievement rate in the "
                            "current reporting period."
                        ),
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    ),
                "Predicted Next Achievement":
                    st.column_config.ProgressColumn(
                        "Predicted Next Achievement",
                        help=(
                            "Random Forest prediction for "
                            "next-month achievement."
                        ),
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    ),
                "Status": st.column_config.TextColumn(
                    "Forecast Status",
                    help=(
                        "Critical < 65% | Watch 65% to < 75% | "
                        "On Track ≥ 75%"
                    )
                ),
                "Held-Out Error":
                    st.column_config.NumberColumn(
                        "Held-Out Error",
                        help=(
                            "Absolute forecast error observed "
                            "during held-out prototype evaluation."
                        ),
                        format="%.3f"
                    )
            }
        )

        st.caption(
            "Showing the 25 lowest predicted next-month "
            "achievement records for the current selection."
        )

    # --------------------------------------------------------
    # Record-level forecast explorer
    # --------------------------------------------------------

    st.divider()

    st.subheader("Forecast Explorer")

    st.write(
        "Select a record to compare current performance, "
        "the predicted next-month achievement and the actual "
        "next-month achievement observed in the synthetic "
        "held-out evaluation period."
    )

    if not filtered_forecast.empty:

        forecast_explorer = (
            filtered_forecast
            .sort_values(
                "predicted_next_achievement_rate"
            )
            .copy()
        )

        forecast_record_ids = (
            forecast_explorer["record_id"]
            .tolist()
        )

        selected_forecast_id = st.selectbox(
            "Select Forecast Record",
            forecast_record_ids,
            format_func=lambda record_id: (
                f"{record_id} — "
                f"{forecast_explorer.loc[
                    forecast_explorer['record_id']
                    == record_id,
                    'programme_name'
                ].iloc[0]}"
            ),
            key="forecast_record_selector"
        )

        selected_forecast = (
            forecast_explorer[
                forecast_explorer["record_id"]
                == selected_forecast_id
            ]
            .iloc[0]
        )

        st.markdown(
            f"### {safe_text(selected_forecast['programme_name'])}"
        )

        st.write(
            f"**{safe_text(selected_forecast['lga'])} — "
            f"{safe_text(selected_forecast['community'])}**"
        )

        fe1, fe2, fe3, fe4 = st.columns(4)

        fe1.metric(
            "Current Achievement",
            f"{selected_forecast['achievement_rate']:.1%}"
        )

        fe2.metric(
            "Predicted Next",
            (
                f"{selected_forecast[
                    'predicted_next_achievement_rate'
                ]:.1%}"
            )
        )

        fe3.metric(
            "Actual Next",
            (
                f"{selected_forecast[
                    'next_achievement_rate'
                ]:.1%}"
            )
        )

        fe4.metric(
            "Forecast Status",
            safe_text(
                selected_forecast["forecast_status"]
            )
        )

        st.write(
            "**Absolute Forecast Error:** "
            f"{selected_forecast['absolute_forecast_error']:.3f}"
        )

        forecast_gap = (
            selected_forecast[
                "predicted_next_achievement_rate"
            ]
            - selected_forecast[
                "achievement_rate"
            ]
        )

        if forecast_gap < 0:

            st.warning(
                "The model anticipates a decline of "
                f"{abs(forecast_gap):.1%} from the current "
                "achievement rate. This record may warrant "
                "closer programme review."
            )

        elif forecast_gap > 0:

            st.success(
                "The model anticipates an improvement of "
                f"{forecast_gap:.1%} from the current "
                "achievement rate."
            )

        else:

            st.info(
                "The forecast indicates little change from "
                "the current achievement rate."
            )

        st.caption(
            "Actual next-month achievement is shown here because "
            "this page displays held-out prototype evaluation data. "
            "For a live future forecast, the actual next-month value "
            "would not yet be known."
        )

    st.divider()

    st.caption(
        "Forecast outputs support programme monitoring and "
        "prioritization. They do not predict programme outcomes "
        "with certainty and should be interpreted alongside "
        "field knowledge, implementation context and human review."
    )

# ============================================================
# RISK INTELLIGENCE
# ============================================================

elif page == "Risk Intelligence":

    st.title("Risk Intelligence")

    st.markdown(
        "### Identify monitoring records that may require "
        "closer programme attention."
    )

    st.write(
        "Risk Intelligence evaluates operational and programme "
        "monitoring signals to classify records as Low, Medium "
        "or High Risk."
    )

    st.info(
        "Risk classifications are decision-support signals. "
        "They identify records recommended for human review "
        "and do not determine programme outcomes."
    )

    # --------------------------------------------------------
    # Load risk results
    # --------------------------------------------------------

    try:

        risk_data = load_risk_results()
        monitoring_data = load_monitoring_data()

    except Exception as error:

        st.error(
            "EarlySignal AI could not load the "
            "risk-intelligence data."
        )

        st.exception(error)
        st.stop()


    # --------------------------------------------------------
    # Add operational indicators from monitoring data
    # --------------------------------------------------------

    operational_columns = [
        "record_id",
        "activity_completion_rate",
        "reporting_delay_days",
        "supply_delay_days",
        "staff_availability_rate",
        "access_constraint_score",
        "complaints_count"
    ]

    columns_to_add = [
        column
        for column in operational_columns
        if (
            column == "record_id"
            or column not in risk_data.columns
        )
    ]

    if len(columns_to_add) > 1:

        risk_data = risk_data.merge(
            monitoring_data[columns_to_add],
            on="record_id",
            how="left",
            validate="one_to_one"
        )


    # --------------------------------------------------------
    # Risk Explorer integrity check
    # --------------------------------------------------------

    required_risk_explorer_columns = [
        "activity_completion_rate",
        "reporting_delay_days",
        "supply_delay_days",
        "staff_availability_rate",
        "access_constraint_score",
        "complaints_count"
    ]

    missing_risk_explorer_columns = [
        column
        for column in required_risk_explorer_columns
        if column not in risk_data.columns
    ]

    if missing_risk_explorer_columns:

        st.error(
            "Risk Explorer is missing required operational fields: "
            + ", ".join(missing_risk_explorer_columns)
        )

        st.stop()


    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.subheader("Risk Filters")

    rc1, rc2, rc3, rc4 = st.columns(4)

    risk_months = sorted(
        risk_data["reporting_date"]
        .dropna()
        .dt.strftime("%Y-%m")
        .unique(),
        reverse=True
    )

    selected_risk_month = persistent_selectbox(
        rc1,
        "Reporting Month",
        ["All Months"] + list(risk_months),
        "risk_month"
    )

    risk_programmes = sorted(
        risk_data["programme_name"]
        .dropna()
        .unique()
    )

    selected_risk_programme = persistent_selectbox(
        rc2,
        "Programme",
        ["All Programmes"] + list(risk_programmes),
        "risk_programme"
    )

    risk_lgas = sorted(
        risk_data["lga"]
        .dropna()
        .unique()
    )

    selected_risk_lga = persistent_selectbox(
        rc3,
        "LGA",
        ["All LGAs"] + list(risk_lgas),
        "risk_lga"
    )

    selected_risk_level = persistent_selectbox(
        rc4,
        "Predicted Risk",
        [
            "All Risk Levels",
            "High",
            "Medium",
            "Low"
        ],
        "risk_level"
    )

    filtered_risk = risk_data.copy()

    if selected_risk_month != "All Months":

        filtered_risk = filtered_risk[
            filtered_risk["reporting_date"]
            .dt.strftime("%Y-%m")
            == selected_risk_month
        ]

    if selected_risk_programme != "All Programmes":

        filtered_risk = filtered_risk[
            filtered_risk["programme_name"]
            == selected_risk_programme
        ]

    if selected_risk_lga != "All LGAs":

        filtered_risk = filtered_risk[
            filtered_risk["lga"]
            == selected_risk_lga
        ]

    if selected_risk_level != "All Risk Levels":

        filtered_risk = filtered_risk[
            filtered_risk["predicted_risk"]
            == selected_risk_level
        ]

    st.caption(
        f"Showing {len(filtered_risk):,} of "
        f"{len(risk_data):,} held-out risk records."
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    risk_records = len(filtered_risk)

    high_risk = int(
        (
            filtered_risk["predicted_risk"]
            == "High"
        ).sum()
    )

    medium_risk = int(
        (
            filtered_risk["predicted_risk"]
            == "Medium"
        ).sum()
    )

    low_risk = int(
        (
            filtered_risk["predicted_risk"]
            == "Low"
        ).sum()
    )

    rk1, rk2, rk3, rk4 = st.columns(4)

    rk1.metric(
        "Risk Records",
        f"{risk_records:,}"
    )

    rk2.metric(
        "High Risk",
        f"{high_risk:,}"
    )

    rk3.metric(
        "Medium Risk",
        f"{medium_risk:,}"
    )

    rk4.metric(
        "Low Risk",
        f"{low_risk:,}"
    )

    st.divider()

    # --------------------------------------------------------
    # Distribution + programme outlook
    # --------------------------------------------------------

    risk_chart1, risk_chart2 = st.columns(2)

    with risk_chart1:

        st.subheader("Predicted Risk Distribution")

        risk_order = [
            "High",
            "Medium",
            "Low"
        ]

        risk_counts = (
            filtered_risk["predicted_risk"]
            .value_counts()
            .reindex(
                risk_order,
                fill_value=0
            )
            .rename_axis("Predicted Risk")
            .reset_index(name="Records")
        )

        risk_total = risk_counts["Records"].sum()

        if risk_total > 0:

            risk_counts["Percentage"] = (
                risk_counts["Records"]
                / risk_total
                * 100
            )

        else:

            risk_counts["Percentage"] = 0.0

        risk_counts["Label"] = (
            risk_counts["Records"].map(
                lambda value: f"{value:,}"
            )
            + "  |  "
            + risk_counts["Percentage"].map(
                lambda value: f"{value:.1f}%"
            )
        )

        risk_distribution_chart = (
            alt.Chart(risk_counts)
            .mark_bar(
                cornerRadiusEnd=4
            )
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Monitoring Records"
                ),
                y=alt.Y(
                    "Predicted Risk:N",
                    sort=risk_order,
                    title=None
                ),
                color=alt.Color(
                    "Predicted Risk:N",
                    scale=alt.Scale(
                        domain=[
                            "High",
                            "Medium",
                            "Low"
                        ],
                        range=[
                            "#D62728",
                            "#F2A900",
                            "#2CA02C"
                        ]
                    ),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "Predicted Risk:N",
                        title="Predicted Risk"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share",
                        format=".1f"
                    )
                ]
            )
        )

        risk_distribution_labels = (
            alt.Chart(risk_counts)
            .mark_text(
                align="left",
                baseline="middle",
                dx=5
            )
            .encode(
                x=alt.X("Records:Q"),
                y=alt.Y(
                    "Predicted Risk:N",
                    sort=risk_order
                ),
                text="Label:N"
            )
        )

        st.altair_chart(
            risk_distribution_chart
            + risk_distribution_labels,
            width="stretch"
        )

        st.caption(
            "Distribution of predicted programme risk "
            "levels in the current view."
        )

    with risk_chart2:

        st.subheader("High-Risk Signals by Programme")

        if filtered_risk.empty:

            st.info(
                "No records match the current filters."
            )

        else:

            programme_risk = (
                filtered_risk
                .assign(
                    high_risk_signal=lambda df: (
                        df["predicted_risk"]
                        == "High"
                    ).astype(int)
                )
                .groupby(
                    "programme_name",
                    as_index=False
                )["high_risk_signal"]
                .mean()
            )

            programme_risk[
                "High-Risk Records (%)"
            ] = (
                programme_risk[
                    "high_risk_signal"
                ]
                * 100
            )

            programme_risk = (
                programme_risk
                .sort_values(
                    "High-Risk Records (%)",
                    ascending=False
                )
            )

            programme_risk["Label"] = (
                programme_risk[
                    "High-Risk Records (%)"
                ]
                .map(
                    lambda value: f"{value:.1f}%"
                )
            )

            programme_risk_chart = (
                alt.Chart(programme_risk)
                .mark_bar(
                    cornerRadiusEnd=4
                )
                .encode(
                    x=alt.X(
                        "High-Risk Records (%):Q",
                        title="High-Risk Records (%)",
                        scale=alt.Scale(
                            domain=[0, 100]
                        )
                    ),
                    y=alt.Y(
                        "programme_name:N",
                        sort=alt.SortField(
                            field="High-Risk Records (%)",
                            order="descending"
                        ),
                        title=None
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "programme_name:N",
                            title="Programme"
                        ),
                        alt.Tooltip(
                            "High-Risk Records (%):Q",
                            title="High-Risk Records",
                            format=".1f"
                        )
                    ]
                )
            )

            programme_risk_labels = (
                alt.Chart(programme_risk)
                .mark_text(
                    align="left",
                    baseline="middle",
                    dx=5
                )
                .encode(
                    x=alt.X(
                        "High-Risk Records (%):Q"
                    ),
                    y=alt.Y(
                        "programme_name:N",
                        sort=alt.SortField(
                            field="High-Risk Records (%)",
                            order="descending"
                        )
                    ),
                    text="Label:N"
                )
            )

            st.altair_chart(
                programme_risk_chart
                + programme_risk_labels,
                width="stretch"
            )

            st.caption(
                "Share of monitoring records predicted "
                "High Risk within each programme for the "
                "current filter selection."
            )

    st.divider()

    # --------------------------------------------------------
    # Model evidence
    # --------------------------------------------------------

    st.subheader("Risk Model Evidence")

    st.write(
        "The Logistic Regression risk model was evaluated "
        "on a future held-out monitoring period."
    )

    re1, re2, re3, re4 = st.columns(4)

    re1.metric(
        "Accuracy",
        "98.10%"
    )

    re2.metric(
        "Macro F1",
        "96.49%"
    )

    re3.metric(
        "High-Risk Recall",
        "99.19%"
    )

    re4.metric(
        "High-Risk Precision",
        "87.14%"
    )

    st.caption(
        "Held-out prototype evaluation: 1,680 records. "
        "Of 123 actual High-Risk records, the model detected "
        "122 and missed 1, with 18 false High-Risk alerts."
    )

    st.warning(
        "Important validation context: these unusually strong "
        "results come from synthetic data where the risk label "
        "was generated from the same family of operational "
        "indicators available to the model. They demonstrate "
        "prototype pipeline validity, not expected real-world "
        "generalization."
    )

    # --------------------------------------------------------
    # Risk model score explanation
    # --------------------------------------------------------

    with st.expander(
        "How should the High-Risk model score be interpreted?"
    ):

        st.write(
            "The High-Risk model score represents the model's "
            "estimated support for the High-Risk class within "
            "this prototype."
        )

        st.write(
            "Values may round to 1.0000 for some synthetic "
            "records. This should not be interpreted as "
            "100% certainty that a programme will fail."
        )

        st.caption(
            "The score supports prioritization and comparison "
            "between records. Operational decisions still "
            "require programme context and human review."
        )

    st.divider()

    # --------------------------------------------------------
    # High-risk review queue
    # --------------------------------------------------------

    st.subheader("Risk Review Queue")

    st.caption(
        "Records are ranked by the model's High-Risk score, "
        "with stronger High-Risk signals shown first."
    )

    if filtered_risk.empty:

        st.warning(
            "No risk records match the current filters."
        )

    else:

        risk_queue = (
            filtered_risk
            .sort_values(
                "probability_high",
                ascending=False
            )
            .copy()
        )

        risk_table = risk_queue[
            [
                "record_id",
                "programme_name",
                "lga",
                "community",
                "achievement_rate",
                "predicted_risk",
                "probability_high"
            ]
        ].copy()

        risk_table.columns = [
            "Record ID",
            "Programme",
            "LGA",
            "Community",
            "Achievement",
            "Predicted Risk",
            "High-Risk Model Score"
        ]

        # Convert achievement rate to percentage points
        # for display only.
        risk_table["Achievement"] = (
            risk_table["Achievement"] * 100
        )

        st.dataframe(
            risk_table.head(25),
            hide_index=True,
            width="stretch",
            column_config={
                "Record ID": st.column_config.TextColumn(
                    "Record ID",
                    help="Unique monitoring record identifier"
                ),
                "Programme": st.column_config.TextColumn(
                    "Programme"
                ),
                "LGA": st.column_config.TextColumn(
                    "LGA"
                ),
                "Community": st.column_config.TextColumn(
                    "Community"
                ),
                "Achievement":
                    st.column_config.ProgressColumn(
                        "Achievement",
                        help=(
                            "Achievement rate in the "
                            "current reporting period."
                        ),
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    ),
                "Predicted Risk":
                    st.column_config.TextColumn(
                        "Predicted Risk",
                        help=(
                            "Risk class predicted by the "
                            "Logistic Regression model."
                        )
                    ),
                "High-Risk Model Score":
                    st.column_config.NumberColumn(
                        "High-Risk Model Score",
                        help=(
                            "Model support for the High-Risk "
                            "class. This is a prioritization "
                            "signal, not certainty of "
                            "programme failure."
                        ),
                        format="%.4f"
                    )
            }
        )

        st.caption(
            "Showing the 25 strongest High-Risk model signals "
            "for the current filter selection."
        )

    # --------------------------------------------------------
    # Risk case explorer
    # --------------------------------------------------------

    st.divider()

    st.subheader("Risk Case Explorer")

    st.write(
        "Select a monitoring record to inspect its predicted "
        "risk level and the operational indicators associated "
        "with the case."
    )

    if not filtered_risk.empty:

        risk_explorer = (
            filtered_risk
            .sort_values(
                "probability_high",
                ascending=False
            )
            .copy()
        )

        risk_record_ids = (
            risk_explorer["record_id"]
            .tolist()
        )

        selected_risk_id = st.selectbox(
            "Select Risk Record",
            risk_record_ids,
            format_func=lambda record_id: (
                f"{record_id} — "
                f"{risk_explorer.loc[
                    risk_explorer['record_id']
                    == record_id,
                    'programme_name'
                ].iloc[0]}"
            ),
            key="risk_record_selector"
        )

        selected_case = (
            risk_explorer[
                risk_explorer["record_id"]
                == selected_risk_id
            ]
            .iloc[0]
        )

        st.markdown(
            f"### {safe_text(selected_case['programme_name'])}"
        )

        st.write(
            f"**{safe_text(selected_case['lga'])} — "
            f"{safe_text(selected_case['community'])}**"
        )

        case1, case2, case3 = st.columns(3)

        case1.metric(
            "Predicted Risk",
            safe_text(
                selected_case["predicted_risk"]
            )
        )

        case2.metric(
            "High-Risk Model Score",
            f"{selected_case['probability_high']:.4f}"
        )

        case3.metric(
            "Achievement",
            f"{selected_case['achievement_rate']:.1%}"
        )

        st.caption(
            "The High-Risk model score is a model output for "
            "prioritization, not a probability of programme failure."
        )

        st.markdown(
            "#### Operational Signals"
        )

        signal1, signal2, signal3 = st.columns(3)

        signal1.metric(
            "Activity Completion",
            f"{selected_case['activity_completion_rate']:.1%}"
        )

        signal2.metric(
            "Reporting Delay",
            f"{selected_case['reporting_delay_days']:.0f} days"
        )

        signal3.metric(
            "Supply Delay",
            f"{selected_case['supply_delay_days']:.0f} days"
        )

        signal4, signal5, signal6 = st.columns(3)

        signal4.metric(
            "Staff Availability",
            f"{selected_case['staff_availability_rate']:.1%}"
        )

        signal5.metric(
            "Access Constraint",
            f"{selected_case['access_constraint_score']:.2f}"
        )

        signal6.metric(
            "Complaints",
            f"{selected_case['complaints_count']:.0f}"
        )

        # ----------------------------------------------------
        # Human-review guidance
        # ----------------------------------------------------

        predicted_level = safe_text(
            selected_case["predicted_risk"]
        )

        if predicted_level == "High":

            st.warning(
                "High-Risk signal detected. This record is "
                "recommended for priority human review alongside "
                "field context and implementation information."
            )

        elif predicted_level == "Medium":

            st.info(
                "Medium-Risk signal detected. Continue monitoring "
                "and review emerging operational constraints."
            )

        else:

            st.success(
                "Low-Risk signal detected. Continue routine "
                "monitoring; this classification does not rule "
                "out emerging contextual risks."
            )

        st.caption(
            "Detailed driver attribution is presented separately "
            "in the Explainable AI module rather than inferred "
            "from these raw indicator values."
        )

    st.divider()

    st.caption(
        "Risk Intelligence contributes 50% of the integrated "
        "Early Warning Score. It is combined with Performance "
        "Forecasting and Anomaly Detection in the Command Center "
        "rather than being used as a standalone decision rule."
    )

# ============================================================
# ANOMALY DETECTION
# ============================================================

elif page == "Anomaly Detection":

    st.title("Anomaly Detection")

    st.markdown(
        "### Surface unusual monitoring patterns for investigation."
    )

    st.write(
        "The Anomaly Detection module identifies monitoring records "
        "whose operational patterns differ substantially from the "
        "patterns learned from the prototype monitoring data."
    )

    st.info(
        "Anomaly alerts are investigation signals, not evidence of "
        "programme failure, data manipulation or misconduct. "
        "Flagged records are recommended for human review."
    )

    # --------------------------------------------------------
    # Load anomaly results
    # --------------------------------------------------------

    try:

        anomaly_data = load_anomaly_results()
        monitoring_data = load_monitoring_data()

    except Exception as error:

        st.error(
            "EarlySignal AI could not load the "
            "anomaly-detection data."
        )

        st.exception(error)
        st.stop()


    # --------------------------------------------------------
    # Add operational indicators when required
    # --------------------------------------------------------

    anomaly_operational_columns = [
        "record_id",
        "achievement_rate",
        "reporting_delay_days",
        "complaints_count",
        "supply_delay_days"
    ]

    anomaly_columns_to_add = [
        column
        for column in anomaly_operational_columns
        if (
            column == "record_id"
            or column not in anomaly_data.columns
        )
    ]

    if len(anomaly_columns_to_add) > 1:

        anomaly_data = anomaly_data.merge(
            monitoring_data[anomaly_columns_to_add],
            on="record_id",
            how="left",
            validate="one_to_one"
        )


    # --------------------------------------------------------
    # Anomaly Explorer integrity check
    # --------------------------------------------------------

    required_anomaly_columns = [
        "achievement_rate",
        "reporting_delay_days",
        "complaints_count",
        "supply_delay_days"
    ]

    missing_anomaly_columns = [
        column
        for column in required_anomaly_columns
        if column not in anomaly_data.columns
    ]

    if missing_anomaly_columns:

        st.error(
            "Anomaly Explorer is missing required fields: "
            + ", ".join(missing_anomaly_columns)
        )

        st.stop()


    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.subheader("Anomaly Filters")

    ac1, ac2, ac3, ac4 = st.columns(4)

    anomaly_months = sorted(
        anomaly_data["reporting_date"]
        .dropna()
        .dt.strftime("%Y-%m")
        .unique(),
        reverse=True
    )

    selected_anomaly_month = persistent_selectbox(
        ac1,
        "Reporting Month",
        ["All Months"] + list(anomaly_months),
        "anomaly_month"
    )

    anomaly_programmes = sorted(
        anomaly_data["programme_name"]
        .dropna()
        .unique()
    )

    selected_anomaly_programme = persistent_selectbox(
        ac2,
        "Programme",
        ["All Programmes"] + list(anomaly_programmes),
        "anomaly_programme"
    )

    anomaly_lgas = sorted(
        anomaly_data["lga"]
        .dropna()
        .unique()
    )

    selected_anomaly_lga = persistent_selectbox(
        ac3,
        "LGA",
        ["All LGAs"] + list(anomaly_lgas),
        "anomaly_lga"
    )

    selected_anomaly_status = persistent_selectbox(
        ac4,
        "Detection Status",
        [
            "All Records",
            "Alert",
            "Normal"
        ],
        "anomaly_status"
    )

    filtered_anomaly = anomaly_data.copy()

    if selected_anomaly_month != "All Months":

        filtered_anomaly = filtered_anomaly[
            filtered_anomaly["reporting_date"]
            .dt.strftime("%Y-%m")
            == selected_anomaly_month
        ]

    if selected_anomaly_programme != "All Programmes":

        filtered_anomaly = filtered_anomaly[
            filtered_anomaly["programme_name"]
            == selected_anomaly_programme
        ]

    if selected_anomaly_lga != "All LGAs":

        filtered_anomaly = filtered_anomaly[
            filtered_anomaly["lga"]
            == selected_anomaly_lga
        ]

    if selected_anomaly_status == "Alert":

        filtered_anomaly = filtered_anomaly[
            filtered_anomaly["predicted_anomaly"] == 1
        ]

    elif selected_anomaly_status == "Normal":

        filtered_anomaly = filtered_anomaly[
            filtered_anomaly["predicted_anomaly"] == 0
        ]

    st.caption(
        f"Showing {len(filtered_anomaly):,} of "
        f"{len(anomaly_data):,} held-out anomaly records."
    )


    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    anomaly_records = len(filtered_anomaly)

    detected_alerts = int(
        (
            filtered_anomaly["predicted_anomaly"]
            == 1
        ).sum()
    )

    normal_records = int(
        (
            filtered_anomaly["predicted_anomaly"]
            == 0
        ).sum()
    )

    alert_rate = (
        detected_alerts / anomaly_records
        if anomaly_records > 0
        else 0
    )

    ak1, ak2, ak3, ak4 = st.columns(4)

    ak1.metric(
        "Anomaly Records",
        f"{anomaly_records:,}"
    )

    ak2.metric(
        "Detected Alerts",
        f"{detected_alerts:,}"
    )

    ak3.metric(
        "Normal Records",
        f"{normal_records:,}"
    )

    ak4.metric(
        "Alert Rate",
        f"{alert_rate:.2%}"
    )

    st.divider()


    # --------------------------------------------------------
    # Detection distribution + programme signals
    # --------------------------------------------------------

    anomaly_chart1, anomaly_chart2 = st.columns(2)

    with anomaly_chart1:

        st.subheader("Detection Distribution")

        detection_order = [
            "Alert",
            "Normal"
        ]

        detection_counts = pd.DataFrame(
            {
                "Detection Status": detection_order,
                "Records": [
                    int(
                        (
                            filtered_anomaly[
                                "predicted_anomaly"
                            ] == 1
                        ).sum()
                    ),
                    int(
                        (
                            filtered_anomaly[
                                "predicted_anomaly"
                            ] == 0
                        ).sum()
                    )
                ]
            }
        )

        detection_total = (
            detection_counts["Records"].sum()
        )

        if detection_total > 0:

            detection_counts["Percentage"] = (
                detection_counts["Records"]
                / detection_total
                * 100
            )

        else:

            detection_counts["Percentage"] = 0.0

        detection_counts["Label"] = (
            detection_counts["Records"].map(
                lambda value: f"{value:,}"
            )
            + "  |  "
            + detection_counts["Percentage"].map(
                lambda value: f"{value:.1f}%"
            )
        )

        detection_distribution_chart = (
            alt.Chart(detection_counts)
            .mark_bar(
                cornerRadiusEnd=4
            )
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Monitoring Records"
                ),
                y=alt.Y(
                    "Detection Status:N",
                    sort=detection_order,
                    title=None
                ),
                color=alt.Color(
                    "Detection Status:N",
                    scale=alt.Scale(
                        domain=[
                            "Alert",
                            "Normal"
                        ],
                        range=[
                            "#D62728",
                            "#2CA02C"
                        ]
                    ),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "Detection Status:N",
                        title="Detection Status"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share",
                        format=".1f"
                    )
                ]
            )
        )

        detection_distribution_labels = (
            alt.Chart(detection_counts)
            .mark_text(
                align="left",
                baseline="middle",
                dx=5
            )
            .encode(
                x=alt.X("Records:Q"),
                y=alt.Y(
                    "Detection Status:N",
                    sort=detection_order
                ),
                text="Label:N"
            )
        )

        st.altair_chart(
            detection_distribution_chart
            + detection_distribution_labels,
            width="stretch"
        )

        st.caption(
            "Distribution of anomaly alerts and normal "
            "records in the current view."
        )


    with anomaly_chart2:

        st.subheader("Anomaly Signals by Programme")

        if filtered_anomaly.empty:

            st.info(
                "No records match the current filters."
            )

        else:

            programme_anomaly = (
                filtered_anomaly
                .groupby(
                    "programme_name",
                    as_index=False
                )["predicted_anomaly"]
                .mean()
            )

            programme_anomaly[
                "Detected Alerts (%)"
            ] = (
                programme_anomaly[
                    "predicted_anomaly"
                ]
                * 100
            )

            programme_anomaly = (
                programme_anomaly
                .sort_values(
                    "Detected Alerts (%)",
                    ascending=False
                )
            )

            programme_anomaly["Label"] = (
                programme_anomaly[
                    "Detected Alerts (%)"
                ]
                .map(
                    lambda value: f"{value:.1f}%"
                )
            )

            programme_anomaly_chart = (
                alt.Chart(programme_anomaly)
                .mark_bar(
                    cornerRadiusEnd=4
                )
                .encode(
                    x=alt.X(
                        "Detected Alerts (%):Q",
                        title="Detected Alerts (%)",
                        scale=alt.Scale(
                            domain=[0, 100]
                        )
                    ),
                    y=alt.Y(
                        "programme_name:N",
                        sort=alt.SortField(
                            field="Detected Alerts (%)",
                            order="descending"
                        ),
                        title=None
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "programme_name:N",
                            title="Programme"
                        ),
                        alt.Tooltip(
                            "Detected Alerts (%):Q",
                            title="Detected Alerts",
                            format=".1f"
                        )
                    ]
                )
            )

            programme_anomaly_labels = (
                alt.Chart(programme_anomaly)
                .mark_text(
                    align="left",
                    baseline="middle",
                    dx=5
                )
                .encode(
                    x=alt.X(
                        "Detected Alerts (%):Q"
                    ),
                    y=alt.Y(
                        "programme_name:N",
                        sort=alt.SortField(
                            field="Detected Alerts (%)",
                            order="descending"
                        )
                    ),
                    text="Label:N"
                )
            )

            st.altair_chart(
                programme_anomaly_chart
                + programme_anomaly_labels,
                width="stretch"
            )

            st.caption(
                "Share of monitoring records detected as "
                "anomaly alerts within each programme for "
                "the current filter selection."
            )

    st.divider()


    # --------------------------------------------------------
    # Model evidence
    # --------------------------------------------------------

    st.subheader("Anomaly Model Evidence")

    st.write(
        "The Isolation Forest model was evaluated on a future "
        "held-out monitoring period using known synthetic anomaly "
        "labels for prototype validation."
    )

    ae1, ae2, ae3, ae4 = st.columns(4)

    ae1.metric(
        "Precision",
        "100.00%"
    )

    ae2.metric(
        "Recall",
        "73.91%"
    )

    ae3.metric(
        "F1 Score",
        "85.00%"
    )

    ae4.metric(
        "False Alerts",
        "0"
    )

    st.caption(
        "Held-out synthetic test period: 1,680 records containing "
        "46 known anomalies. The model identified 34 anomaly alerts, "
        "all of which corresponded to known injected anomalies. "
        "This produced 100% precision, 73.91% recall and no false alerts."
    )

    st.warning(
        "The 100% result refers specifically to precision on the "
        "held-out synthetic test period. It does not mean the anomaly "
        "model is 100% accurate, nor does it establish expected "
        "performance on real organizational monitoring data."
    )


    # --------------------------------------------------------
    # What the model examines
    # --------------------------------------------------------

    with st.expander(
        "What monitoring signals does the anomaly model examine?"
    ):

        st.write(
            "The prototype Isolation Forest uses four operational "
            "monitoring indicators:"
        )

        st.write(
            "• Achievement rate\n\n"
            "• Reporting delay\n\n"
            "• Complaints count\n\n"
            "• Supply delay"
        )

        st.caption(
            "An unusual combination of these indicators can trigger "
            "an alert even when a programme record is not otherwise "
            "classified as high risk."
        )

    st.divider()


    # --------------------------------------------------------
    # Anomaly review queue
    # --------------------------------------------------------

    st.subheader("Anomaly Review Queue")

    st.caption(
        "Detected anomaly alerts are shown first for investigation."
    )

    if filtered_anomaly.empty:

        st.warning(
            "No anomaly records match the current filters."
        )

    else:

        anomaly_queue = (
            filtered_anomaly
            .sort_values(
                [
                    "predicted_anomaly",
                    "anomaly_score"
                ],
                ascending=[
                    False,
                    True
                ]
            )
            .copy()
        )

        anomaly_table = anomaly_queue[
            [
                "record_id",
                "programme_name",
                "lga",
                "community",
                "achievement_rate",
                "predicted_anomaly",
                "anomaly_score"
            ]
        ].copy()

        anomaly_table["predicted_anomaly"] = (
            anomaly_table["predicted_anomaly"]
            .map(
                {
                    1: "Alert",
                    0: "Normal"
                }
            )
        )

        anomaly_table.columns = [
            "Record ID",
            "Programme",
            "LGA",
            "Community",
            "Achievement",
            "Detection",
            "Anomaly Score"
        ]

        # Convert achievement rate to percentage points
        # for display only.
        anomaly_table["Achievement"] = (
            anomaly_table["Achievement"] * 100
        )

        st.dataframe(
            anomaly_table.head(25),
            hide_index=True,
            width="stretch",
            column_config={
                "Record ID": st.column_config.TextColumn(
                    "Record ID",
                    help="Unique monitoring record identifier"
                ),
                "Programme": st.column_config.TextColumn(
                    "Programme"
                ),
                "LGA": st.column_config.TextColumn(
                    "LGA"
                ),
                "Community": st.column_config.TextColumn(
                    "Community"
                ),
                "Achievement":
                    st.column_config.ProgressColumn(
                        "Achievement",
                        help=(
                            "Achievement rate in the "
                            "current reporting period."
                        ),
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    ),
                "Detection":
                    st.column_config.TextColumn(
                        "Detection",
                        help=(
                            "Isolation Forest detection result: "
                            "Alert or Normal."
                        )
                    ),
                "Anomaly Score":
                    st.column_config.NumberColumn(
                        "Anomaly Score",
                        help=(
                            "Isolation Forest anomaly score used "
                            "to rank unusual monitoring patterns. "
                            "More extreme values indicate stronger "
                            "anomaly signals in this prototype."
                        ),
                        format="%.4f"
                    )
            }
        )

        st.caption(
            "Showing the first 25 records for the current "
            "filter selection, with detected alerts prioritized."
        )


    # --------------------------------------------------------
    # Anomaly case explorer
    # --------------------------------------------------------

    st.divider()

    st.subheader("Anomaly Case Explorer")

    st.write(
        "Select a monitoring record to inspect the operational "
        "signals associated with its anomaly-detection result."
    )

    if not filtered_anomaly.empty:

        anomaly_explorer = (
            filtered_anomaly
            .sort_values(
                [
                    "predicted_anomaly",
                    "anomaly_score"
                ],
                ascending=[
                    False,
                    True
                ]
            )
            .copy()
        )

        anomaly_record_ids = (
            anomaly_explorer["record_id"]
            .tolist()
        )

        selected_anomaly_id = st.selectbox(
            "Select Anomaly Record",
            anomaly_record_ids,
            format_func=lambda record_id: (
                f"{record_id} — "
                f"{anomaly_explorer.loc[
                    anomaly_explorer['record_id']
                    == record_id,
                    'programme_name'
                ].iloc[0]}"
            ),
            key="anomaly_record_selector"
        )

        selected_anomaly = (
            anomaly_explorer[
                anomaly_explorer["record_id"]
                == selected_anomaly_id
            ]
            .iloc[0]
        )

        st.markdown(
            f"### {safe_text(selected_anomaly['programme_name'])}"
        )

        st.write(
            f"**{safe_text(selected_anomaly['lga'])} — "
            f"{safe_text(selected_anomaly['community'])}**"
        )

        anomaly_status_display = (
            "Alert"
            if int(
                selected_anomaly["predicted_anomaly"]
            ) == 1
            else "Normal"
        )

        ax1, ax2, ax3 = st.columns(3)

        ax1.metric(
            "Detection",
            anomaly_status_display
        )

        ax2.metric(
            "Anomaly Score",
            f"{selected_anomaly['anomaly_score']:.4f}"
        )

        ax3.metric(
            "Achievement",
            f"{selected_anomaly['achievement_rate']:.1%}"
        )

        st.caption(
            "The anomaly score is an Isolation Forest model output "
            "used to rank unusual observations. It is not a probability "
            "of programme failure or misconduct."
        )

        st.markdown("#### Operational Signals")

        as1, as2, as3 = st.columns(3)

        as1.metric(
            "Reporting Delay",
            f"{selected_anomaly['reporting_delay_days']:.0f} days"
        )

        as2.metric(
            "Supply Delay",
            f"{selected_anomaly['supply_delay_days']:.0f} days"
        )

        as3.metric(
            "Complaints",
            f"{selected_anomaly['complaints_count']:.0f}"
        )

        if anomaly_status_display == "Alert":

            st.warning(
                "Unusual monitoring pattern detected. Review the "
                "record for data-quality issues, reporting delays, "
                "supply constraints, implementation changes or other "
                "contextual explanations before taking action."
            )

        else:

            st.success(
                "No anomaly alert was generated for this record. "
                "Continue routine monitoring; a normal anomaly result "
                "does not rule out other programme risks."
            )

        st.caption(
            "Anomaly detection identifies unusual patterns rather "
            "than diagnosing their cause. Interpretation requires "
            "programme context and human review."
        )


    st.divider()

    st.caption(
        "Anomaly Detection contributes 20% of the integrated "
        "Early Warning Score. It complements Risk Intelligence "
        "and Performance Forecasting rather than acting as a "
        "standalone programme decision rule."
    )

# ============================================================
# EXPLAINABLE AI
# ============================================================

elif page == "Explainable AI":

    st.title("Explainable AI")

    st.markdown(
        "### Understand why a monitoring record received "
        "its risk classification."
    )

    st.write(
        "Explainable AI translates the Risk Intelligence model "
        "into manager-facing operational explanations. It highlights "
        "the signals that increased or reduced model support for "
        "a risk classification."
    )

    st.info(
        "Model explanations describe how the prototype model used "
        "available monitoring information. They do not prove that "
        "an indicator caused a programme outcome."
    )

    # --------------------------------------------------------
    # Load explainability results
    # --------------------------------------------------------

    try:

        explain_data = load_explainability_results()
        monitoring_data = load_monitoring_data()

    except Exception as error:

        st.error(
            "EarlySignal AI could not load the "
            "explainability results."
        )

        st.exception(error)
        st.stop()

    # --------------------------------------------------------
    # Add supporting fields required by Explainable AI
    # --------------------------------------------------------

    try:

        risk_support_data = load_risk_results()

    except Exception as error:

        st.error(
            "EarlySignal AI could not load supporting "
            "Risk Intelligence data."
        )

        st.exception(error)
        st.stop()


    # --------------------------------------------------------
    # Add achievement rate from monitoring data
    # --------------------------------------------------------

    if "achievement_rate" not in explain_data.columns:

        explain_data = explain_data.merge(
            monitoring_data[
                [
                    "record_id",
                    "achievement_rate"
                ]
            ],
            on="record_id",
            how="left",
            validate="one_to_one"
        )


    # --------------------------------------------------------
    # Add High-Risk model score from Risk Intelligence
    # --------------------------------------------------------

    if "probability_high" not in explain_data.columns:

        explain_data = explain_data.merge(
            risk_support_data[
                [
                    "record_id",
                    "probability_high"
                ]
            ],
            on="record_id",
            how="left",
            validate="one_to_one"
        )


    # --------------------------------------------------------
    # Required-column integrity check
    # --------------------------------------------------------

    required_explain_columns = [
        "record_id",
        "reporting_date",
        "programme_name",
        "lga",
        "community",
        "achievement_rate",
        "predicted_risk",
        "probability_high",
        "primary_driver",
        "secondary_driver",
        "tertiary_driver",
        "strongest_protective_signal"
    ]

    missing_explain_columns = [
        column
        for column in required_explain_columns
        if column not in explain_data.columns
    ]

    if missing_explain_columns:

        st.error(
            "Explainable AI is missing required fields: "
            + ", ".join(missing_explain_columns)
        )

        st.stop()


    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.subheader("Explanation Filters")

    ec1, ec2, ec3, ec4 = st.columns(4)

    explain_months = sorted(
        explain_data["reporting_date"]
        .dropna()
        .dt.strftime("%Y-%m")
        .unique(),
        reverse=True
    )

    selected_explain_month = persistent_selectbox(
        ec1,
        "Reporting Month",
        ["All Months"] + list(explain_months),
        "explain_month"
    )
    explain_programmes = sorted(
        explain_data["programme_name"]
        .dropna()
        .unique()
    )

    selected_explain_programme = persistent_selectbox(
        ec2,
        "Programme",
        ["All Programmes"] + list(explain_programmes),
        "explain_programme"
    )

    explain_lgas = sorted(
        explain_data["lga"]
        .dropna()
        .unique()
    )

    selected_explain_lga = persistent_selectbox(
        ec3,
        "LGA",
        ["All LGAs"] + list(explain_lgas),
        "explain_lga"
    )

    selected_explain_risk = persistent_selectbox(
        ec4,
        "Predicted Risk",
        [
            "All Risk Levels",
            "High",
            "Medium",
            "Low"
        ],
        "explain_risk"
    )

    filtered_explain = explain_data.copy()

    if selected_explain_month != "All Months":

        filtered_explain = filtered_explain[
            filtered_explain["reporting_date"]
            .dt.strftime("%Y-%m")
            == selected_explain_month
        ]

    if selected_explain_programme != "All Programmes":

        filtered_explain = filtered_explain[
            filtered_explain["programme_name"]
            == selected_explain_programme
        ]

    if selected_explain_lga != "All LGAs":

        filtered_explain = filtered_explain[
            filtered_explain["lga"]
            == selected_explain_lga
        ]

    if selected_explain_risk != "All Risk Levels":

        filtered_explain = filtered_explain[
            filtered_explain["predicted_risk"]
            == selected_explain_risk
        ]

    st.caption(
        f"Showing {len(filtered_explain):,} of "
        f"{len(explain_data):,} held-out explanation records."
    )


    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    explanation_records = len(filtered_explain)

    high_explanations = int(
        (
            filtered_explain["predicted_risk"]
            == "High"
        ).sum()
    )

    medium_explanations = int(
        (
            filtered_explain["predicted_risk"]
            == "Medium"
        ).sum()
    )

    low_explanations = int(
        (
            filtered_explain["predicted_risk"]
            == "Low"
        ).sum()
    )

    ek1, ek2, ek3, ek4 = st.columns(4)

    ek1.metric(
        "Explanation Records",
        f"{explanation_records:,}"
    )

    ek2.metric(
        "High Risk",
        f"{high_explanations:,}"
    )

    ek3.metric(
        "Medium Risk",
        f"{medium_explanations:,}"
    )

    ek4.metric(
        "Low Risk",
        f"{low_explanations:,}"
    )

    st.divider()


    # --------------------------------------------------------
    # Primary driver patterns
    # --------------------------------------------------------

    st.subheader("Primary Risk-Increasing Drivers")

    st.write(
        "This view summarizes the operational indicator most strongly "
        "increasing model support for each selected record."
    )

    if filtered_explain.empty:

        st.info(
            "No explanation records match the current filters."
        )

    else:

        primary_driver_counts = (
            filtered_explain["primary_driver"]
            .fillna(
                "No strong risk-increasing signal"
            )
            .value_counts()
            .rename_axis("Primary Driver")
            .reset_index(name="Records")
        )

        driver_total = (
            primary_driver_counts["Records"].sum()
        )

        if driver_total > 0:

            primary_driver_counts["Percentage"] = (
                primary_driver_counts["Records"]
                / driver_total
                * 100
            )

        else:

            primary_driver_counts["Percentage"] = 0.0

        primary_driver_counts["Label"] = (
            primary_driver_counts["Records"].map(
                lambda value: f"{value:,}"
            )
            + "  |  "
            + primary_driver_counts["Percentage"].map(
                lambda value: f"{value:.1f}%"
            )
        )

        primary_driver_chart = (
            alt.Chart(primary_driver_counts)
            .mark_bar(
                cornerRadiusEnd=4
            )
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Explanation Records"
                ),
                y=alt.Y(
                    "Primary Driver:N",
                    sort=alt.SortField(
                        field="Records",
                        order="descending"
                    ),
                    title=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "Primary Driver:N",
                        title="Primary Driver"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share",
                        format=".1f"
                    )
                ]
            )
        )

        primary_driver_labels = (
            alt.Chart(primary_driver_counts)
            .mark_text(
                align="left",
                baseline="middle",
                dx=5
            )
            .encode(
                x=alt.X("Records:Q"),
                y=alt.Y(
                    "Primary Driver:N",
                    sort=alt.SortField(
                        field="Records",
                        order="descending"
                    )
                ),
                text="Label:N"
            )
        )

        st.altair_chart(
            primary_driver_chart
            + primary_driver_labels,
            width="stretch"
        )

    st.caption(
        "Driver patterns describe model contribution, not causal "
        "relationships between an indicator and programme performance."
    )

    st.divider()


    # --------------------------------------------------------
    # Explanation validation
    # --------------------------------------------------------

    st.subheader("Explanation Validation")

    st.write(
        "The explanation layer was validated against the underlying "
        "Logistic Regression risk model to confirm that the displayed "
        "feature contributions reproduce the model decision function."
    )

    ev1, ev2, ev3 = st.columns(3)

    ev1.metric(
        "Transformed Features",
        "77"
    )

    ev2.metric(
        "Predictions Reproduced",
        "1,680 / 1,680"
    )

    ev3.metric(
        "Reproduction Rate",
        "100%"
    )

    st.caption(
        "Contribution reconstruction matched the model decision "
        "function for all 1,680 held-out records, with a maximum "
        "reconstruction difference of 0 in the prototype validation."
    )

    st.success(
        "Explanation integrity check passed: displayed model "
        "contributions are derived directly from the fitted "
        "Logistic Regression model rather than generated as "
        "unsupported narrative explanations."
    )

    st.warning(
        "This validates explanation fidelity to the prototype model. "
        "It does not establish that the model itself is causally "
        "correct or that the same performance will generalize to "
        "real organizational data."
    )

    st.divider()

    # --------------------------------------------------------
    # Explanation review queue
    # --------------------------------------------------------

    st.subheader("Explanation Review Queue")

    st.caption(
        "Records with stronger High-Risk model support are shown first."
    )

    if filtered_explain.empty:

        st.warning(
            "No explanation records match the current filters."
        )

    else:

        explanation_queue = (
            filtered_explain
            .sort_values(
                "probability_high",
                ascending=False
            )
            .copy()
        )

        explanation_table = explanation_queue[
            [
                "record_id",
                "programme_name",
                "lga",
                "community",
                "predicted_risk",
                "probability_high",
                "primary_driver"
            ]
        ].copy()

        explanation_table.columns = [
            "Record ID",
            "Programme",
            "LGA",
            "Community",
            "Predicted Risk",
            "High-Risk Model Score",
            "Primary Driver"
        ]

        st.dataframe(
            explanation_table.head(25),
            hide_index=True,
            width="stretch",
            column_config={
                "Record ID": st.column_config.TextColumn(
                    "Record ID",
                    help="Unique monitoring record identifier"
                ),
                "Programme": st.column_config.TextColumn(
                    "Programme"
                ),
                "LGA": st.column_config.TextColumn(
                    "LGA"
                ),
                "Community": st.column_config.TextColumn(
                    "Community"
                ),
                "Predicted Risk":
                    st.column_config.TextColumn(
                        "Predicted Risk",
                        help=(
                            "Risk class predicted by the "
                            "Logistic Regression model."
                        )
                    ),
                "High-Risk Model Score":
                    st.column_config.NumberColumn(
                        "High-Risk Model Score",
                        help=(
                            "Model support for the High-Risk "
                            "class. This is not certainty of "
                            "programme failure."
                        ),
                        format="%.4f"
                    ),
                "Primary Driver":
                    st.column_config.TextColumn(
                        "Primary Driver",
                        help=(
                            "Operational indicator with the "
                            "strongest risk-increasing model "
                            "contribution for this record."
                        )
                    )
            }
        )

        st.caption(
            "Showing the 25 strongest High-Risk model signals "
            "for the current filter selection."
        )

    # --------------------------------------------------------
    # Case explanation
    # --------------------------------------------------------

    st.divider()

    st.subheader("Individual Case Explanation")

    st.write(
        "Select a monitoring record to see the operational signals "
        "that most strongly increased or reduced model support for "
        "its risk classification."
    )

    if not filtered_explain.empty:

        explanation_explorer = (
            filtered_explain
            .sort_values(
                "probability_high",
                ascending=False
            )
            .copy()
        )

        explanation_record_ids = (
            explanation_explorer["record_id"]
            .tolist()
        )

        selected_explanation_id = st.selectbox(
            "Select Explanation Record",
            explanation_record_ids,
            format_func=lambda record_id: (
                f"{record_id} — "
                f"{explanation_explorer.loc[
                    explanation_explorer['record_id']
                    == record_id,
                    'programme_name'
                ].iloc[0]}"
            ),
            key="explanation_record_selector"
        )

        selected_explanation = (
            explanation_explorer[
                explanation_explorer["record_id"]
                == selected_explanation_id
            ]
            .iloc[0]
        )

        st.markdown(
            f"### {selected_explanation['programme_name']}"
        )

        st.write(
            f"**{selected_explanation['lga']} — "
            f"{selected_explanation['community']}**"
        )

        ex1, ex2, ex3 = st.columns(3)

        ex1.metric(
            "Predicted Risk",
            str(selected_explanation["predicted_risk"])
        )

        ex2.metric(
            "High-Risk Model Score",
            f"{selected_explanation['probability_high']:.4f}"
        )

        ex3.metric(
            "Achievement",
            f"{selected_explanation['achievement_rate']:.1%}"
        )

        st.caption(
            "The High-Risk model score supports prioritization. "
            "A value displayed as 1.0000 should not be interpreted "
            "as literal certainty of programme failure."
        )


        # ----------------------------------------------------
        # Risk-increasing drivers
        # ----------------------------------------------------

        st.markdown("#### Risk-Increasing Drivers")

        driver_col1, driver_col2, driver_col3 = (
            st.columns(3)
        )

        primary_driver = selected_explanation["primary_driver"]
        secondary_driver = selected_explanation["secondary_driver"]
        tertiary_driver = selected_explanation["tertiary_driver"]

        primary_driver = (
            "No strong signal"
            if pd.isna(primary_driver) or str(primary_driver).strip() == ""
            else str(primary_driver).strip()
        )

        secondary_driver = (
            "No strong signal"
            if pd.isna(secondary_driver) or str(secondary_driver).strip() == ""
            else str(secondary_driver).strip()
        )

        tertiary_driver = (
            "No strong signal"
            if pd.isna(tertiary_driver) or str(tertiary_driver).strip() == ""
            else str(tertiary_driver).strip()
        )

        driver_col1.write(
            "**Primary Driver**"
        )

        driver_col1.write(
            primary_driver
        )

        driver_col2.write(
            "**Secondary Driver**"
        )

        driver_col2.write(
            secondary_driver
        )

        driver_col3.write(
            "**Tertiary Driver**"
        )

        driver_col3.write(
            tertiary_driver
        )


        # ----------------------------------------------------
        # Protective signal
        # ----------------------------------------------------

        st.markdown("#### Protective Signal")

        protective_signal = selected_explanation[
            "strongest_protective_signal"
        ]

        protective_signal = (
            "No strong protective signal identified"
            if (
                pd.isna(protective_signal)
                or str(protective_signal).strip() == ""
            )
            else str(protective_signal).strip()
        )

        st.success(
            protective_signal
        )


        # ----------------------------------------------------
        # Recommended investigation
        # ----------------------------------------------------

        st.markdown("#### Recommended Investigation")

        primary_driver_text = (
            ""
            if primary_driver == "No strong signal"
            else primary_driver.lower()
        )

        secondary_driver_text = (
            ""
            if secondary_driver == "No strong signal"
            else secondary_driver.lower()
        )

        tertiary_driver_text = (
            ""
            if tertiary_driver == "No strong signal"
            else tertiary_driver.lower()
        )

        combined_driver_text = " ".join(
            [
                primary_driver_text,
                secondary_driver_text,
                tertiary_driver_text
            ]
        )

        investigation_items = []

        if "supply" in combined_driver_text:

            investigation_items.append(
                "review supply-chain delays, commodity availability "
                "and implementation dependencies"
            )

        if "report" in combined_driver_text:

            investigation_items.append(
                "review reporting timeliness, data flow and field "
                "reporting bottlenecks"
            )

        if "achievement" in combined_driver_text:

            investigation_items.append(
                "review progress against targets and implementation "
                "constraints affecting achievement"
            )

        if "activity" in combined_driver_text:

            investigation_items.append(
                "review activity completion, implementation pace "
                "and outstanding field actions"
            )

        if "complaint" in combined_driver_text:

            investigation_items.append(
                "review complaint trends and relevant community "
                "feedback mechanisms"
            )

        if "access" in combined_driver_text:

            investigation_items.append(
                "review access constraints and their operational "
                "implications"
            )

        if "staff" in combined_driver_text:

            investigation_items.append(
                "review staffing availability and operational "
                "capacity"
            )

        if investigation_items:

            investigation_guidance = (
                "Recommended for human review: "
                + "; ".join(investigation_items)
                + "."
            )

        else:

            investigation_guidance = (
                "Recommended for human review alongside programme "
                "context, recent implementation information and "
                "field-level evidence."
            )

        st.warning(
            investigation_guidance
        )


        # ----------------------------------------------------
        # Interpretation boundary
        # ----------------------------------------------------

        st.markdown("#### Interpretation")

        st.write(
            "These explanations show how operational indicators "
            "contributed to the model's classification. They should "
            "be used to guide questions for programme review rather "
            "than treated as proof that a particular factor caused "
            "the observed risk."
        )

        st.caption(
            "Location and categorical model coefficients are not "
            "presented as causal explanations. The manager-facing "
            "view prioritizes actionable operational monitoring "
            "signals."
        )


    st.divider()

    st.caption(
        "Explainable AI strengthens the EarlySignal AI decision-support "
        "workflow by connecting model outputs to understandable "
        "operational signals and recommended areas for human review."
    )

# ============================================================
# GEOGRAPHIC INTELLIGENCE
# ============================================================

elif page == "Geographic Intelligence":

    st.title("Geographic Intelligence")

    st.markdown(
        "### See where programme warning signals are concentrated."
    )

    st.write(
        "Geographic Intelligence translates the integrated Early Warning "
        "Engine into location-level decision support. It helps programme "
        "teams identify LGAs with higher concentrations of priority alerts, "
        "multiple warning signals and records recommended for human review."
    )

    st.info(
        "Geographic patterns support prioritization and investigation. "
        "They should not be interpreted as evidence that a location itself "
        "caused programme risk or underperformance."
    )


    # --------------------------------------------------------
    # Required-column integrity check
    # --------------------------------------------------------

    required_geo_columns = [
        "record_id",
        "reporting_date",
        "programme_name",
        "state",
        "lga",
        "community",
        "achievement_rate",
        "early_warning_score",
        "early_warning_priority",
        "warning_signal_count",
        "signal_agreement",
        "review_status"
    ]

    missing_geo_columns = [
        column
        for column in required_geo_columns
        if column not in data.columns
    ]

    if missing_geo_columns:

        st.error(
            "Geographic Intelligence is missing required fields: "
            + ", ".join(missing_geo_columns)
        )

        st.stop()


    # --------------------------------------------------------
    # Geographic filters
    # --------------------------------------------------------

    st.subheader("Geographic Filters")

    gc1, gc2, gc3 = st.columns(3)

    geo_months = sorted(
        data["reporting_date"]
        .dropna()
        .dt.strftime("%Y-%m")
        .unique(),
        reverse=True
    )

    selected_geo_month = persistent_selectbox(
        gc1,
        "Reporting Month",
        ["All Months"] + list(geo_months),
        "geo_month"
    )

    geo_programmes = sorted(
        data["programme_name"]
        .dropna()
        .unique()
    )

    selected_geo_programme = persistent_selectbox(
        gc2,
        "Programme",
        ["All Programmes"] + list(geo_programmes),
        "geo_programme"
    )

    geo_priorities = [
        "All Priorities",
        "High",
        "Medium",
        "Low"
    ]

    selected_geo_priority = persistent_selectbox(
        gc3,
        "Priority",
        geo_priorities,
        "geo_priority"
    )


    # --------------------------------------------------------
    # Apply filters
    # --------------------------------------------------------

    filtered_geo = data.copy()

    if selected_geo_month != "All Months":

        filtered_geo = filtered_geo[
            filtered_geo["reporting_date"]
            .dt.strftime("%Y-%m")
            == selected_geo_month
        ]

    if selected_geo_programme != "All Programmes":

        filtered_geo = filtered_geo[
            filtered_geo["programme_name"]
            == selected_geo_programme
        ]

    if selected_geo_priority != "All Priorities":

        filtered_geo = filtered_geo[
            filtered_geo["early_warning_priority"]
            == selected_geo_priority
        ]

    st.caption(
        f"Showing {len(filtered_geo):,} of "
        f"{len(data):,} integrated early-warning records."
    )


    # --------------------------------------------------------
    # Geographic KPIs
    # --------------------------------------------------------

    lgas_monitored = filtered_geo["lga"].nunique()

    communities_monitored = (
        filtered_geo["community"].nunique()
    )

    high_priority_geo = int(
        (
            filtered_geo["early_warning_priority"]
            == "High"
        ).sum()
    )

    multi_signal_geo = int(
        (
            filtered_geo["warning_signal_count"]
            >= 2
        ).sum()
    )

    gk1, gk2, gk3, gk4 = st.columns(4)

    gk1.metric(
        "LGAs Monitored",
        f"{lgas_monitored:,}"
    )

    gk2.metric(
        "Communities Monitored",
        f"{communities_monitored:,}"
    )

    gk3.metric(
        "High-Priority Alerts",
        f"{high_priority_geo:,}"
    )

    gk4.metric(
        "Multi-Signal Records",
        f"{multi_signal_geo:,}"
    )

    st.divider()

    # --------------------------------------------------------
    # LGA priority profile
    # --------------------------------------------------------

    st.subheader("LGA Priority Profile")

    st.write(
        "This profile compares High, Medium and Low priority "
        "records across monitored LGAs and highlights the share "
        "recommended for High-Priority review."
    )

    if filtered_geo.empty:

        st.info(
            "No geographic records match the current filters."
        )

    else:

        # Count records by LGA and priority
        lga_priority = (
            filtered_geo
            .groupby(
                [
                    "lga",
                    "early_warning_priority"
                ]
            )
            .size()
            .reset_index(name="Records")
        )

        # Calculate total records within each LGA
        lga_priority["LGA Total"] = (
            lga_priority
            .groupby("lga")["Records"]
            .transform("sum")
        )

        # Calculate within-LGA percentage
        lga_priority["Percentage"] = (
            lga_priority["Records"]
            / lga_priority["LGA Total"]
            * 100
        )

        # Explicit priority order for stacked bars
        lga_priority["Priority Order"] = (
            lga_priority[
                "early_warning_priority"
            ]
            .map(
                {
                    "High": 1,
                    "Medium": 2,
                    "Low": 3
                }
            )
        )

        # ----------------------------------------------------
        # Stacked LGA priority chart
        # ----------------------------------------------------

        lga_priority_chart = (
            alt.Chart(lga_priority)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Monitoring Records",
                    stack="zero"
                ),
                y=alt.Y(
                    "lga:N",
                    title=None,
                    sort=alt.SortField(
                        field="LGA Total",
                        order="descending"
                    )
                ),
                color=alt.Color(
                    "early_warning_priority:N",
                    title="Priority",
                    scale=alt.Scale(
                        domain=[
                            "High",
                            "Medium",
                            "Low"
                        ],
                        range=[
                            "#D62728",
                            "#F2B134",
                            "#2CA02C"
                        ]
                    ),
                    legend=alt.Legend(
                        orient="top"
                    )
                ),
                order=alt.Order(
                    "Priority Order:Q",
                    sort="ascending"
                ),
                tooltip=[
                    alt.Tooltip(
                        "lga:N",
                        title="LGA"
                    ),
                    alt.Tooltip(
                        "early_warning_priority:N",
                        title="Priority"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share within LGA",
                        format=".1f"
                    ),
                    alt.Tooltip(
                        "LGA Total:Q",
                        title="Total LGA Records",
                        format=","
                    )
                ]
            )
            .properties(
                height=360
            )
        )

        st.altair_chart(
            lga_priority_chart,
            width="stretch"
        )

        # ----------------------------------------------------
        # Exact-value summary
        # ----------------------------------------------------

        lga_priority_summary = (
            lga_priority
            .pivot(
                index="lga",
                columns="early_warning_priority",
                values="Records"
            )
            .fillna(0)
            .astype(int)
        )

        for priority in [
            "High",
            "Medium",
            "Low"
        ]:
            if priority not in lga_priority_summary.columns:
                lga_priority_summary[priority] = 0

        lga_priority_summary = (
            lga_priority_summary[
                [
                    "High",
                    "Medium",
                    "Low"
                ]
            ]
            .reset_index()
        )

        lga_priority_summary["Total Records"] = (
            lga_priority_summary[
                [
                    "High",
                    "Medium",
                    "Low"
                ]
            ]
            .sum(axis=1)
        )

        lga_priority_summary[
            "High Priority Share"
        ] = (
            lga_priority_summary["High"]
            / lga_priority_summary["Total Records"]
            * 100
        )

        lga_priority_summary = (
            lga_priority_summary
            .sort_values(
                [
                    "High Priority Share",
                    "High"
                ],
                ascending=False
            )
        )

        lga_priority_summary.columns = [
            "LGA",
            "High",
            "Medium",
            "Low",
            "Total Records",
            "High Priority Share"
        ]

        st.dataframe(
            lga_priority_summary,
            hide_index=True,
            width="stretch",
            column_config={
                "LGA":
                    st.column_config.TextColumn(
                        "LGA"
                    ),
                "High":
                    st.column_config.NumberColumn(
                        "High",
                        format="%d"
                    ),
                "Medium":
                    st.column_config.NumberColumn(
                        "Medium",
                        format="%d"
                    ),
                "Low":
                    st.column_config.NumberColumn(
                        "Low",
                        format="%d"
                    ),
                "Total Records":
                    st.column_config.NumberColumn(
                        "Total Records",
                        format="%d"
                    ),
                "High Priority Share":
                    st.column_config.ProgressColumn(
                        "High Priority Share",
                        help=(
                            "Percentage of monitoring records "
                            "classified as High Priority "
                            "within the LGA."
                        ),
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    )
            }
        )

    st.caption(
        "The stacked chart shows monitoring-record volume by "
        "priority within each LGA. The table provides exact counts "
        "and High Priority share. Differences should be interpreted "
        "alongside the number of monitoring records observed in "
        "each LGA."
    )

    st.divider()

    # --------------------------------------------------------
    # LGA early-warning ranking
    # --------------------------------------------------------

    st.subheader("LGA Early-Warning Ranking")

    st.write(
        "LGAs are ranked using the average integrated Early Warning "
        "Score, while alert counts and signal patterns provide "
        "additional operational context."
    )

    if filtered_geo.empty:

        st.info(
            "No geographic records match the current filters."
        )

    else:

        lga_summary = (
            filtered_geo
            .groupby("lga")
            .agg(
                Monitoring_Records=(
                    "record_id",
                    "count"
                ),
                Average_Early_Warning_Score=(
                    "early_warning_score",
                    "mean"
                ),
                High_Priority_Alerts=(
                    "early_warning_priority",
                    lambda x: (x == "High").sum()
                ),
                Medium_Priority_Alerts=(
                    "early_warning_priority",
                    lambda x: (x == "Medium").sum()
                ),
                Multi_Signal_Records=(
                    "warning_signal_count",
                    lambda x: (x >= 2).sum()
                ),
                Average_Achievement=(
                    "achievement_rate",
                    "mean"
                )
            )
            .reset_index()
        )

        # Rank LGAs using the existing management logic
        lga_summary = (
            lga_summary
            .sort_values(
                [
                    "Average_Early_Warning_Score",
                    "High_Priority_Alerts"
                ],
                ascending=[
                    False,
                    False
                ]
            )
            .reset_index(drop=True)
        )

        # ----------------------------------------------------
        # LGA ranking chart
        # ----------------------------------------------------

        lga_ranking_chart = (
            alt.Chart(lga_summary)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Average_Early_Warning_Score:Q",
                    title="Average Early Warning Score",
                    scale=alt.Scale(
                        domain=[0, 100]
                    )
                ),
                y=alt.Y(
                    "lga:N",
                    title=None,
                    sort="-x"
                ),
                tooltip=[
                    alt.Tooltip(
                        "lga:N",
                        title="LGA"
                    ),
                    alt.Tooltip(
                        "Average_Early_Warning_Score:Q",
                        title="Average Warning Score",
                        format=".1f"
                    ),
                    alt.Tooltip(
                        "Monitoring_Records:Q",
                        title="Monitoring Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "High_Priority_Alerts:Q",
                        title="High-Priority Alerts",
                        format=","
                    ),
                    alt.Tooltip(
                        "Medium_Priority_Alerts:Q",
                        title="Medium-Priority Alerts",
                        format=","
                    ),
                    alt.Tooltip(
                        "Multi_Signal_Records:Q",
                        title="Multi-Signal Records",
                        format=","
                    )
                ]
            )
            .properties(
                height=360
            )
        )

        lga_ranking_labels = (
            alt.Chart(lga_summary)
            .mark_text(
                align="left",
                baseline="middle",
                dx=5
            )
            .encode(
                x=alt.X(
                    "Average_Early_Warning_Score:Q"
                ),
                y=alt.Y(
                    "lga:N",
                    sort="-x"
                ),
                text=alt.Text(
                    "Average_Early_Warning_Score:Q",
                    format=".1f"
                )
            )
        )

        st.altair_chart(
            lga_ranking_chart
            + lga_ranking_labels,
            width="stretch"
        )

        # ----------------------------------------------------
        # Exact-value ranking table
        # ----------------------------------------------------

        lga_summary_display = (
            lga_summary.copy()
        )

        lga_summary_display[
            "Average_Early_Warning_Score"
        ] = (
            lga_summary_display[
                "Average_Early_Warning_Score"
            ]
            .round(1)
        )

        # Convert achievement rate to 0–100 display scale
        lga_summary_display[
            "Average_Achievement"
        ] = (
            lga_summary_display[
                "Average_Achievement"
            ]
            * 100
        )

        lga_summary_display.columns = [
            "LGA",
            "Monitoring Records",
            "Average Early Warning Score",
            "High-Priority Alerts",
            "Medium-Priority Alerts",
            "Multi-Signal Records",
            "Average Achievement"
        ]

        st.dataframe(
            lga_summary_display,
            hide_index=True,
            width="stretch",
            column_config={
                "LGA":
                    st.column_config.TextColumn(
                        "LGA"
                    ),
                "Monitoring Records":
                    st.column_config.NumberColumn(
                        "Monitoring Records",
                        format="%d"
                    ),
                "Average Early Warning Score":
                    st.column_config.ProgressColumn(
                        "Average Early Warning Score",
                        help=(
                            "Mean integrated Early Warning Score "
                            "across monitoring records in the LGA."
                        ),
                        format="%.1f",
                        min_value=0,
                        max_value=100
                    ),
                "High-Priority Alerts":
                    st.column_config.NumberColumn(
                        "High-Priority Alerts",
                        format="%d"
                    ),
                "Medium-Priority Alerts":
                    st.column_config.NumberColumn(
                        "Medium-Priority Alerts",
                        format="%d"
                    ),
                "Multi-Signal Records":
                    st.column_config.NumberColumn(
                        "Multi-Signal Records",
                        format="%d"
                    ),
                "Average Achievement":
                    st.column_config.ProgressColumn(
                        "Average Achievement",
                        help=(
                            "Average achievement rate across "
                            "monitoring records in the LGA."
                        ),
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    )
            }
        )

    st.caption(
        "The ranking is a management prioritization view based on "
        "monitoring records, not a ranking of communities or "
        "populations by inherent risk."
    )

    st.divider()

    # --------------------------------------------------------
    # Priority concentration by programme and LGA
    # --------------------------------------------------------

    st.subheader(
        "Programme × LGA Warning Concentration"
    )

    st.write(
        "This view shows where integrated warning scores are "
        "concentrated across programmes and LGAs."
    )

    if filtered_geo.empty:

        st.info(
            "No programme-location records match the current "
            "filters."
        )

    else:

        # ----------------------------------------------------
        # Programme × LGA average warning scores
        # ----------------------------------------------------

        programme_lga_summary = (
            filtered_geo
            .groupby(
                [
                    "programme_name",
                    "lga"
                ]
            )
            .agg(
                Average_Early_Warning_Score=(
                    "early_warning_score",
                    "mean"
                ),
                Monitoring_Records=(
                    "record_id",
                    "count"
                ),
                High_Priority_Alerts=(
                    "early_warning_priority",
                    lambda x: (x == "High").sum()
                )
            )
            .reset_index()
        )

        programme_lga_summary[
            "Average_Early_Warning_Score"
        ] = (
            programme_lga_summary[
                "Average_Early_Warning_Score"
            ]
            .round(1)
        )

        # ----------------------------------------------------
        # Heatmap
        # ----------------------------------------------------

        programme_lga_heatmap = (
            alt.Chart(
                programme_lga_summary
            )
            .mark_rect()
            .encode(
                x=alt.X(
                    "lga:N",
                    title="LGA"
                ),
                y=alt.Y(
                    "programme_name:N",
                    title="Programme"
                ),
                color=alt.Color(
                    "Average_Early_Warning_Score:Q",
                    title="Average Warning Score",
                    scale=alt.Scale(
                        domain=[
                            0,
                            100
                        ],
                        scheme="yelloworangered"
                    )
                ),
                tooltip=[
                    alt.Tooltip(
                        "programme_name:N",
                        title="Programme"
                    ),
                    alt.Tooltip(
                        "lga:N",
                        title="LGA"
                    ),
                    alt.Tooltip(
                        "Average_Early_Warning_Score:Q",
                        title="Average Warning Score",
                        format=".1f"
                    ),
                    alt.Tooltip(
                        "Monitoring_Records:Q",
                        title="Monitoring Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "High_Priority_Alerts:Q",
                        title="High-Priority Alerts",
                        format=","
                    )
                ]
            )
            .properties(
                height=300
            )
        )

        programme_lga_labels = (
            alt.Chart(
                programme_lga_summary
            )
            .mark_text(
                baseline="middle",
                fontSize=12
            )
            .encode(
                x=alt.X(
                    "lga:N"
                ),
                y=alt.Y(
                    "programme_name:N"
                ),
                text=alt.Text(
                    "Average_Early_Warning_Score:Q",
                    format=".1f"
                ),
                color=alt.condition(
                    "datum.Average_Early_Warning_Score >= 50",
                    alt.value("white"),
                    alt.value("black")
                )
            )
        )

        st.altair_chart(
            programme_lga_heatmap
            + programme_lga_labels,
            width="stretch"
        )

        # ----------------------------------------------------
        # Exact-value matrix
        # ----------------------------------------------------

        programme_lga_matrix = (
            programme_lga_summary
            .pivot(
                index="programme_name",
                columns="lga",
                values="Average_Early_Warning_Score"
            )
            .round(1)
        )

        st.dataframe(
            programme_lga_matrix,
            width="stretch",
            column_config={
                column:
                    st.column_config.NumberColumn(
                        column,
                        format="%.1f"
                    )
                for column
                in programme_lga_matrix.columns
            }
        )

    st.caption(
        "Values represent the average integrated Early Warning "
        "Score for each selected programme-location combination. "
        "Higher scores indicate stronger monitoring signals for "
        "management review, not inherent geographic risk."
    )

    st.divider()

    # --------------------------------------------------------
    # Geographic review queue
    # --------------------------------------------------------

    st.subheader("Geographic Review Queue")

    st.caption(
        "Higher-priority records are shown first to support "
        "location-focused programme review."
    )

    if filtered_geo.empty:

        st.warning(
            "No geographic records match the current filters."
        )

    else:

        # Preserve integrated priority ordering
        geo_priority_order = {
            "High": 3,
            "Medium": 2,
            "Low": 1
        }

        geo_queue = filtered_geo.copy()

        geo_queue["_priority_order"] = (
            geo_queue[
                "early_warning_priority"
            ]
            .map(geo_priority_order)
            .fillna(0)
        )

        # Priority first, then Early Warning Score,
        # then number of warning signals
        geo_queue = geo_queue.sort_values(
            [
                "_priority_order",
                "early_warning_score",
                "warning_signal_count"
            ],
            ascending=[
                False,
                False,
                False
            ]
        )

        geo_queue_table = geo_queue[
            [
                "record_id",
                "programme_name",
                "lga",
                "community",
                "early_warning_score",
                "early_warning_priority",
                "warning_signal_count",
                "signal_agreement",
                "review_status"
            ]
        ].copy()

        geo_queue_table.columns = [
            "Record ID",
            "Programme",
            "LGA",
            "Community",
            "Early Warning Score",
            "Priority",
            "Warning Signals",
            "Signal Agreement",
            "Review Status"
        ]

        st.dataframe(
            geo_queue_table.head(25),
            hide_index=True,
            width="stretch",
            column_config={
                "Record ID":
                    st.column_config.TextColumn(
                        "Record ID",
                        help=(
                            "Unique monitoring record "
                            "identifier."
                        )
                    ),
                "Programme":
                    st.column_config.TextColumn(
                        "Programme"
                    ),
                "LGA":
                    st.column_config.TextColumn(
                        "LGA"
                    ),
                "Community":
                    st.column_config.TextColumn(
                        "Community"
                    ),
                "Early Warning Score":
                    st.column_config.ProgressColumn(
                        "Early Warning Score",
                        help=(
                            "Integrated prototype prioritization "
                            "score combining Risk Intelligence, "
                            "Performance Forecast and Anomaly "
                            "Detection. This is not a probability "
                            "of programme failure."
                        ),
                        format="%.1f",
                        min_value=0,
                        max_value=100
                    ),
                "Priority":
                    st.column_config.TextColumn(
                        "Priority",
                        help=(
                            "Integrated priority classification: "
                            "High, Medium or Low."
                        )
                    ),
                "Warning Signals":
                    st.column_config.NumberColumn(
                        "Warning Signals",
                        help=(
                            "Number of available analytical "
                            "components currently producing a "
                            "warning signal."
                        ),
                        format="%d"
                    ),
                "Signal Agreement":
                    st.column_config.TextColumn(
                        "Signal Agreement",
                        help=(
                            "Degree of agreement across available "
                            "warning components."
                        )
                    ),
                "Review Status":
                    st.column_config.TextColumn(
                        "Review Status",
                        help=(
                            "Recommended level of human "
                            "monitoring review."
                        )
                    )
            }
        )

        st.caption(
            "Showing the first 25 records for the current filter "
            "selection. Records are ordered by integrated priority, "
            "Early Warning Score and warning-signal count."
        )

    st.divider()

    # --------------------------------------------------------
    # LGA investigation explorer
    # --------------------------------------------------------

    st.subheader("LGA Investigation Explorer")

    st.write(
        "Select an LGA to review its current warning profile "
        "and identify records that may warrant programme follow-up."
    )

    if filtered_geo.empty:

        st.info(
            "No geographic records match the current filters."
        )

    else:

        available_lgas = sorted(
            filtered_geo["lga"]
            .dropna()
            .unique()
        )

        selected_investigation_lga = st.selectbox(
            "Select LGA",
            available_lgas,
            key="geo_investigation_lga"
        )

        selected_lga_data = filtered_geo[
            filtered_geo["lga"]
            == selected_investigation_lga
        ].copy()

        lga_records = len(selected_lga_data)

        lga_high = int(
            (
                selected_lga_data[
                    "early_warning_priority"
                ]
                == "High"
            ).sum()
        )

        lga_multi_signal = int(
            (
                selected_lga_data[
                    "warning_signal_count"
                ]
                >= 2
            ).sum()
        )

        lga_average_score = (
            selected_lga_data[
                "early_warning_score"
            ]
            .mean()
        )

        gi1, gi2, gi3, gi4 = st.columns(4)

        gi1.metric(
            "Monitoring Records",
            f"{lga_records:,}"
        )

        gi2.metric(
            "Average Warning Score",
            f"{lga_average_score:.1f}"
        )

        gi3.metric(
            "High-Priority Alerts",
            f"{lga_high:,}"
        )

        gi4.metric(
            "Multi-Signal Records",
            f"{lga_multi_signal:,}"
        )

        # ----------------------------------------------------
        # LGA priority breakdown
        # ----------------------------------------------------

        lga_priority_breakdown = (
            selected_lga_data[
                "early_warning_priority"
            ]
            .value_counts()
            .reindex(
                [
                    "High",
                    "Medium",
                    "Low"
                ],
                fill_value=0
            )
            .rename_axis("Priority")
            .reset_index(name="Records")
        )

        lga_priority_breakdown["Percentage"] = (
            lga_priority_breakdown["Records"]
            / lga_records
            * 100
        )

        lga_priority_breakdown["Label"] = (
            lga_priority_breakdown["Records"].map(
                lambda value: f"{value:,}"
            )
            + " | "
            + lga_priority_breakdown["Percentage"].map(
                lambda value: f"{value:.1f}%"
            )
        )

        st.markdown(
            f"#### {selected_investigation_lga} Priority Profile"
        )

        lga_profile_chart = (
            alt.Chart(
                lga_priority_breakdown
            )
            .mark_bar()
            .encode(
                x=alt.X(
                    "Records:Q",
                    title="Monitoring Records"
                ),
                y=alt.Y(
                    "Priority:N",
                    title=None,
                    sort=[
                        "High",
                        "Medium",
                        "Low"
                    ]
                ),
                color=alt.Color(
                    "Priority:N",
                    title="Priority",
                    scale=alt.Scale(
                        domain=[
                            "High",
                            "Medium",
                            "Low"
                        ],
                        range=[
                            "#D62728",
                            "#F2B134",
                            "#2CA02C"
                        ]
                    ),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "Priority:N",
                        title="Priority"
                    ),
                    alt.Tooltip(
                        "Records:Q",
                        title="Records",
                        format=","
                    ),
                    alt.Tooltip(
                        "Percentage:Q",
                        title="Share",
                        format=".1f"
                    )
                ]
            )
            .properties(
                height=210
            )
        )

        lga_profile_labels = (
            alt.Chart(
                lga_priority_breakdown
            )
            .mark_text(
                align="left",
                baseline="middle",
                dx=6
            )
            .encode(
                x=alt.X(
                    "Records:Q"
                ),
                y=alt.Y(
                    "Priority:N",
                    sort=[
                        "High",
                        "Medium",
                        "Low"
                    ]
                ),
                text=alt.Text(
                    "Label:N"
                )
            )
        )

        st.altair_chart(
            lga_profile_chart
            + lga_profile_labels,
            width="stretch"
        )

        # ----------------------------------------------------
        # Priority records for selected LGA
        # ----------------------------------------------------

        lga_review_records = (
            selected_lga_data[
                selected_lga_data[
                    "early_warning_priority"
                ].isin(
                    [
                        "High",
                        "Medium"
                    ]
                )
            ]
            .sort_values(
                [
                    "early_warning_score",
                    "warning_signal_count"
                ],
                ascending=[
                    False,
                    False
                ]
            )
        )

        st.markdown(
            "#### Records Recommended for Review"
        )

        if lga_review_records.empty:

            st.success(
                "No High- or Medium-priority records are present "
                "for this LGA under the current filters."
            )

        else:

            lga_review_table = lga_review_records[
                [
                    "record_id",
                    "programme_name",
                    "community",
                    "early_warning_score",
                    "early_warning_priority",
                    "signal_agreement",
                    "review_status"
                ]
            ].copy()

            lga_review_table.columns = [
                "Record ID",
                "Programme",
                "Community",
                "Early Warning Score",
                "Priority",
                "Signal Agreement",
                "Review Status"
            ]

            st.dataframe(
                lga_review_table.head(20),
                hide_index=True,
                width="stretch",
                column_config={
                    "Record ID":
                        st.column_config.TextColumn(
                            "Record ID"
                        ),
                    "Programme":
                        st.column_config.TextColumn(
                            "Programme"
                        ),
                    "Community":
                        st.column_config.TextColumn(
                            "Community"
                        ),
                    "Early Warning Score":
                        st.column_config.ProgressColumn(
                            "Early Warning Score",
                            help=(
                                "Integrated prototype "
                                "prioritization score. This is "
                                "not a probability of programme "
                                "failure."
                            ),
                            format="%.1f",
                            min_value=0,
                            max_value=100
                        ),
                    "Priority":
                        st.column_config.TextColumn(
                            "Priority"
                        ),
                    "Signal Agreement":
                        st.column_config.TextColumn(
                            "Signal Agreement"
                        ),
                    "Review Status":
                        st.column_config.TextColumn(
                            "Review Status"
                        )
                }
            )

            st.caption(
                "Showing up to 20 High- and Medium-priority "
                "records for the selected LGA, ordered by Early "
                "Warning Score and warning-signal count."
            )

        # ----------------------------------------------------
        # Human-review guidance
        # ----------------------------------------------------

        if lga_high > 0:

            st.warning(
                f"{selected_investigation_lga} contains "
                f"{lga_high:,} High-Priority record(s) in the "
                "current view. These records are recommended for "
                "human review alongside field context, programme "
                "implementation information and recent monitoring "
                "evidence."
            )

        elif lga_multi_signal > 0:

            st.info(
                f"{selected_investigation_lga} contains "
                "multiple-signal records that may warrant closer "
                "monitoring even where the integrated priority "
                "threshold is not High."
            )

        else:

            st.success(
                f"No High-Priority concentration is visible for "
                f"{selected_investigation_lga} under the current "
                "filters. Continue routine monitoring."
            )

    st.divider()

    st.caption(
        "Geographic Intelligence summarizes the spatial distribution "
        "of EarlySignal AI warning signals. Geographic patterns are "
        "recommended for human review and should be interpreted "
        "alongside programme context, data quality, access conditions "
        "and field-level evidence."
    )

# ============================================================
# ABOUT & RESPONSIBLE AI
# ============================================================

else:

    st.title("About & Responsible AI")

    st.markdown(
        "### See the risk before it becomes the result."
    )

    st.write(
        "EarlySignal AI is an AI-powered early warning and "
        "decision-support prototype for humanitarian and development "
        "programmes. It helps programme and monitoring teams identify "
        "activities and locations that may need attention before "
        "performance problems become visible only at the end of a "
        "reporting period."
    )

    st.info(
        "Core decision question: Which programme activities or "
        "locations need attention now, why, and what should the "
        "team investigate next?"
    )

    st.divider()


    # --------------------------------------------------------
    # Problem
    # --------------------------------------------------------

    st.subheader("The Problem")

    st.write(
        "Programme teams routinely collect monitoring information on "
        "targets, achievements, activity completion, reporting delays, "
        "supply constraints, staffing, access and community feedback. "
        "However, these signals are often reviewed separately or after "
        "a reporting period has already ended."
    )

    st.write(
        "This can make it difficult to recognize emerging implementation "
        "problems early enough for programme teams to investigate them. "
        "EarlySignal AI demonstrates how multiple monitoring signals can "
        "be combined into an explainable early-warning workflow."
    )

    st.divider()


    # --------------------------------------------------------
    # Solution
    # --------------------------------------------------------

    st.subheader("The EarlySignal AI Solution")

    st.write(
        "The prototype brings forecasting, risk classification, anomaly "
        "detection and model explanation into one integrated "
        "decision-support workflow."
    )

    st.markdown(
        """
**Monitoring Data → Data Readiness → Performance Forecast → Risk Intelligence → Anomaly Detection → Explainable AI → Geographic Intelligence → Early Warning Priority → Human Review**
        """
    )

    st.write(
        "Instead of asking programme managers to interpret several "
        "independent model outputs, EarlySignal AI combines the warning "
        "signals into a transparent priority score and provides "
        "manager-facing investigation guidance."
    )

    st.divider()


    # --------------------------------------------------------
    # AI components
    # --------------------------------------------------------

    st.subheader("AI & Analytical Components")

    ac1, ac2 = st.columns(2)

    with ac1:

        st.markdown("#### Performance Forecast")

        st.write(
            "A Random Forest regression pipeline estimates next-period "
            "achievement performance using historical and operational "
            "monitoring signals."
        )

        st.markdown("#### Risk Intelligence")

        st.write(
            "A Logistic Regression classification pipeline identifies "
            "Low, Medium and High programme risk using operational "
            "monitoring indicators."
        )

    with ac2:

        st.markdown("#### Anomaly Detection")

        st.write(
            "An Isolation Forest identifies unusual combinations of "
            "achievement, reporting delay, supply delay and complaints "
            "that may warrant investigation."
        )

        st.markdown("#### Explainable AI")

        st.write(
            "Exact Logistic Regression feature contributions translate "
            "the risk model into understandable operational signals and "
            "recommended areas for human review."
        )

    st.markdown("#### Geographic Intelligence")

    st.write(
        "Integrated warning signals are summarized across LGAs and "
        "communities to help programme teams identify where priority "
        "records and multiple warning signals are concentrated."
    )

    st.divider()


    # --------------------------------------------------------
    # Integrated early-warning engine
    # --------------------------------------------------------

    st.subheader("Integrated Early Warning Engine")

    st.write(
        "The Early Warning Engine combines three complementary signals "
        "into one transparent prototype prioritization index."
    )

    ew1, ew2, ew3 = st.columns(3)

    ew1.metric(
        "Risk Intelligence",
        "50%"
    )

    ew2.metric(
        "Performance Forecast",
        "30%"
    )

    ew3.metric(
        "Anomaly Detection",
        "20%"
    )

    st.markdown(
        """
**Priority thresholds**

- **High Priority:** Early Warning Score ≥ 60
- **Medium Priority:** Early Warning Score ≥ 30 and < 60
- **Low Priority:** Early Warning Score < 30
        """
    )

    st.info(
        "If a forecast is unavailable, the available component weights "
        "are renormalized. Missing forecast information is never treated "
        "as zero risk."
    )

    st.warning(
        "The Early Warning Score is a transparent prototype "
        "prioritization index. It is not a probability of programme "
        "failure."
    )

    st.divider()


    # --------------------------------------------------------
    # Prototype evidence
    # --------------------------------------------------------

    st.subheader("Prototype Validation Evidence")

    st.write(
        "EarlySignal AI was evaluated on a synthetic monthly monitoring "
        "panel designed to support reproducible prototype development "
        "without exposing confidential programme or participant data."
    )

    pv1, pv2, pv3, pv4 = st.columns(4)

    pv1.metric(
        "Monitoring Records",
        "7,680"
    )

    pv2.metric(
        "Programme / Location Units",
        "240"
    )

    pv3.metric(
        "Reporting Months",
        "32"
    )

    pv4.metric(
        "Integrated Test Records",
        "1,680"
    )


    st.markdown("#### Performance Forecast")

    st.write(
        "**MAE 0.0507 | RMSE 0.0680 | R² 0.3469**"
    )

    st.caption(
        "The Random Forest improved MAE by 13.84% and RMSE by "
        "16.67% compared with the held-out naive baseline."
    )


    st.markdown("#### Risk Intelligence")

    st.write(
        "**Accuracy 98.10% | Macro F1 96.49% | "
        "High-Risk Recall 99.19% | High-Risk Precision 87.14%**"
    )

    st.caption(
        "These unusually strong classification results reflect "
        "prototype validation on synthetic data whose risk labels were "
        "generated from the same family of operational indicators. They "
        "should not be presented as expected real-world performance."
    )


    st.markdown("#### Anomaly Detection")

    st.write(
        "**Precision 100.00% | Recall 73.91% | F1 85.00%**"
    )

    st.caption(
        "The Isolation Forest achieved 100% precision on the held-out "
        "synthetic test period, with zero false alerts in that evaluation. "
        "This does not mean the model is 100% accurate."
    )


    st.markdown("#### Explainability Validation")

    st.write(
        "**1,680 / 1,680 predictions reproduced | "
        "Maximum reconstruction difference: 0**"
    )

    st.caption(
        "The explanation layer reconstructs the fitted Logistic "
        "Regression decision function using exact transformed-feature "
        "contributions."
    )

    st.divider()


    # --------------------------------------------------------
    # Responsible AI
    # --------------------------------------------------------

    st.subheader("Responsible AI Principles")

    st.write(
        "EarlySignal AI is designed as decision support for programme "
        "and monitoring teams, not as an autonomous operational "
        "decision-maker."
    )

    st.markdown(
        """
- **Human oversight:** Alerts are recommended for human review before action.
- **Explainability:** Priority records are accompanied by operational signals that help users understand what the models identified.
- **No causal claims:** Model contributions and geographic patterns do not prove that an indicator or location caused an outcome.
- **Data minimization:** The prototype uses synthetic monitoring data and does not require personally identifiable participant information.
- **Transparent scoring:** The integrated 50/30/20 weighting and priority thresholds are visible to users.
- **Missing-data awareness:** Unavailable forecast information is not interpreted as evidence of low risk.
- **Context matters:** Field evidence, programme knowledge, access conditions, data quality and community feedback remain essential to interpretation.
        """
    )

    st.success(
        "EarlySignal AI supports professional judgement. "
        "It does not replace programme managers, MEL specialists, "
        "field teams or community-informed decision-making."
    )

    st.divider()


    # --------------------------------------------------------
    # Limitations
    # --------------------------------------------------------

    st.subheader("Prototype Limitations")

    st.write(
        "The current version is a demonstration prototype and should "
        "not be deployed for consequential programme decisions without "
        "additional validation."
    )

    st.markdown(
        """
- The current models were developed and evaluated using synthetic data.
- Model performance may change substantially with real organizational data.
- Risk thresholds and integrated component weights require contextual validation before operational deployment.
- Geographic Intelligence currently summarizes administrative locations and does not infer causal geographic risk.
- Anomalies indicate unusual patterns, not confirmed data-quality or implementation failures.
- Forecasts and classifications depend on the quality, completeness and timeliness of monitoring data.
- Real deployment would require governance, access controls, security, monitoring, retraining and periodic performance review.
        """
    )

    st.divider()


    # --------------------------------------------------------
    # Future organizational deployment
    # --------------------------------------------------------

    st.subheader("Path to Organizational Deployment")

    st.write(
        "The prototype architecture is designed so the synthetic data "
        "layer can later be replaced by validated organizational data "
        "once appropriate access, governance and technical integration "
        "are established."
    )

    st.markdown(
        """
Potential integrations include:

- Google Sheets or structured reporting workbooks
- Organizational monitoring databases and MIS platforms
- Approved programme APIs
- Secure data warehouses
- Scheduled reporting pipelines
        """
    )

    st.write(
        "Before deployment, the models would be retrained and validated "
        "against the organization's own historical monitoring data, "
        "indicators, programme definitions and operational context."
    )

    st.divider()


    # --------------------------------------------------------
    # Project identity
    # --------------------------------------------------------

    st.subheader("Project")

    st.markdown(
        "**EarlySignal AI — AI-Powered Early Warning and "
        "Decision Support for Humanitarian & Development Programmes**"
    )

    st.write(
        "Built as an applied AI prototype demonstrating how machine "
        "learning, anomaly detection, explainability and integrated "
        "decision support can strengthen proactive programme monitoring."
    )

    st.caption(
        "Prototype outputs are intended for demonstration, learning "
        "and human-reviewed decision support."
    )