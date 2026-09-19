# EarlySignal AI

**AI-Powered Early Warning and Decision Support for Humanitarian & Development Programmes**

> **See the risk before it becomes the result.**

**Live Application:** https://earlysignalai-global.streamlit.app/

---

## Overview

EarlySignal AI is an AI-enabled early-warning and decision-support prototype designed for humanitarian and development programmes.

Programme teams routinely collect monitoring data on achievement, implementation progress, reporting delays, complaints, supply constraints, and other operational indicators. However, emerging problems can remain hidden across separate indicators until targets are missed or reporting periods have ended.

EarlySignal AI brings these signals together to answer a practical decision question:

> **Which programme activities or locations need attention now, why, and what should the team investigate next?**

The platform combines performance forecasting, risk classification, anomaly detection, explainable AI, and geographic intelligence to identify monitoring records that may require attention and prioritize them for human review.

The system supports decision-making. It does **not** replace programme managers or automatically make programme decisions.

---

## The Problem

Humanitarian and development programmes often have substantial monitoring data but limited capacity to convert that information into timely early warnings.

Important warning signals may appear across different indicators:

* declining programme achievement;
* delayed reporting;
* incomplete activities;
* supply delays;
* increasing complaints; and
* unusual operational patterns.

When these indicators are reviewed separately, emerging implementation problems may only become clear after performance has already deteriorated.

EarlySignal AI demonstrates how existing monitoring information can be transformed into an integrated early-warning workflow.

---

## The Solution

EarlySignal AI uses multiple analytical signals rather than relying on a single prediction.

The workflow is:

**Monitoring Data → Multiple AI Signals → Integrated Priority → Explanation → Recommended Human Investigation**

The prototype provides eight connected application areas:

1. **Command Center** — integrated early-warning overview and priority records.
2. **Data Upload** — monitoring-data upload and structural readiness assessment.
3. **Performance Forecast** — forecasts next-period programme achievement.
4. **Risk Intelligence** — classifies implementation risk.
5. **Anomaly Detection** — identifies unusual monitoring patterns.
6. **Explainable AI** — shows the factors contributing to model predictions.
7. **Geographic Intelligence** — examines warning patterns across programme locations.
8. **About & Responsible AI** — documents interpretation boundaries, limitations, and human oversight.

---

## Early Warning Priority Engine

The integrated Early Warning Score combines three analytical components:

| Signal               | Weight |
| -------------------- | -----: |
| Risk Intelligence    |    50% |
| Performance Forecast |    30% |
| Anomaly Detection    |    20% |

Priority thresholds are:

| Score    | Priority |
| -------- | -------- |
| 60–100   | High     |
| 30–59.99 | Medium   |
| Below 30 | Low      |

When a forecast is unavailable, the engine renormalizes the weights of the available signals rather than treating the missing forecast as zero risk.

The **Early Warning Score is a transparent prototype prioritization index. It is not a probability of programme failure.**

---

## Prototype Data

The prototype was developed and validated using a fully synthetic monitoring dataset to avoid exposing confidential organizational or beneficiary information.

The dataset contains:

* **7,680 monitoring records**
* **5 programmes**
* **8 LGAs**
* **6 communities per LGA**
* **32 reporting months**
* **22 monitoring variables**
* Reporting period from **January 2024 to August 2026**

Each record represents one programme, LGA, community, and reporting month.

Synthetic data allows the complete analytical workflow to be demonstrated safely, but performance on this dataset should not be interpreted as evidence of equivalent performance on real organizational data.

---

## AI and Machine Learning Components

### 1. Performance Forecast

A Random Forest regression model forecasts next-period achievement.

Held-out temporal test results:

* **MAE:** 0.0507
* **RMSE:** 0.0680
* **R²:** 0.3469
* **MAE improvement over naive baseline:** 13.84%
* **RMSE improvement over naive baseline:** 16.67%

The evaluation uses a time-based split rather than randomly mixing historical and future observations.

---

### 2. Risk Intelligence

A class-balanced Logistic Regression model classifies monitoring records into implementation-risk categories.

Held-out synthetic test results:

* **Accuracy:** 98.10%
* **Macro F1:** 96.49%
* **High-Risk Recall:** 99.19%
* **High-Risk Precision:** 87.14%

The unusually strong results should be interpreted carefully. The synthetic risk labels were generated using the same family of programme indicators available to the model. These results therefore demonstrate prototype pipeline validation rather than expected real-world accuracy.

---

### 3. Anomaly Detection

An Isolation Forest identifies unusual combinations of monitoring indicators.

Held-out synthetic test results:

* **Precision:** 100%
* **Recall:** 73.91%
* **F1:** 85.00%
* **False alerts:** 0

The 100% figure refers specifically to **precision on the held-out synthetic test period**. It does not mean that the anomaly model is 100% accurate.

---

### 4. Explainable AI

EarlySignal AI provides model-level explanations showing which monitoring factors contributed most strongly to a risk prediction.

For the Logistic Regression risk model:

* **77 transformed features** are represented in the explanation layer.
* Prediction reconstruction was verified for **1,680 of 1,680 test records**.
* Maximum reconstruction difference was **0**.

Frequently identified primary drivers among high-risk records included:

* low achievement;
* supply delays;
* low activity completion;
* reporting delays; and
* elevated complaints.

These contributions explain model behaviour. They should **not** be interpreted as proof of causality.

---

## Integrated Early-Warning Results

The final integrated evaluation contains **1,680 monitoring records**.

Priority distribution:

| Priority | Records |  Share |
| -------- | ------: | -----: |
| High     |     141 |  8.39% |
| Medium   |     564 | 33.57% |
| Low      |     975 | 58.04% |

The system also assesses agreement between analytical signals:

* **No Warning Signal:** 628 records
* **Single Signal:** 473 records
* **Multiple Signals:** 553 records
* **Strong Agreement:** 26 records

This allows programme teams to distinguish isolated warnings from cases where several analytical methods point toward the same monitoring record.

---

## Example Early Warning

One demonstration record illustrates the full workflow:

**Record:** ES-006044
**Programme:** Nutrition Support Programme
**Location:** Gwoza — Gwoza Site 3
**Early Warning Score:** 85/100
**Priority:** High
**Risk Intelligence:** High
**Performance Forecast:** Watch
**Anomaly Detection:** Alert
**Signal Agreement:** Strong Agreement

Primary model drivers include:

* supply delay;
* reporting delay; and
* low achievement.

The system recommends that programme staff investigate areas such as supply-chain bottlenecks, reporting timeliness, and programme targets.

This is a recommendation for **human investigation**, not an automated operational decision.

---

## Responsible AI

EarlySignal AI is intentionally designed as a human-in-the-loop decision-support system.

Its responsible-use principles include:

* AI alerts support rather than replace programme managers.
* Model scores are not treated as certainty.
* The Early Warning Score is not a probability of failure.
* Explainability represents model contribution, not causality.
* Geographic patterns describe monitoring records and should not be interpreted as inherent risk associated with a community or LGA.
* Synthetic data is used for prototype validation.
* High model performance on synthetic data is not presented as proven real-world performance.
* Operational deployment would require organization-specific validation, calibration, governance, and monitoring.

Final programme decisions remain with responsible human teams.

---

## Technology Stack

The prototype was developed using:

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Streamlit**
* **Altair**
* **Matplotlib**
* **Joblib**
* **OpenPyXL**
* **Jupyter Notebook**
* **Git & GitHub**

---

## Repository Structure

```text
EarlySignal_AI/
│
├── app/
│   └── app.py
│
├── data/
│   └── synthetic/
│       └── earlysignal_monitoring_data.csv
│
├── models/
│   ├── earlysignal_anomaly_model.joblib
│   ├── earlysignal_forecast_model.joblib
│   └── earlysignal_risk_model.joblib
│
├── notebooks/
│   ├── 01_Data_Understanding_Validation.ipynb
│   ├── 02_Exploratory_Analysis_Early_Warning_Patterns.ipynb
│   ├── 03_Performance_Forecast_Model.ipynb
│   ├── 04_Risk_Intelligence_Model.ipynb
│   ├── 05_Anomaly_Detection.ipynb
│   ├── 06_Explainable_AI.ipynb
│   └── 07_Early_Warning_Priority_Engine.ipynb
│
├── outputs/
│   ├── anomaly_results.csv
│   ├── early_warning_priority_results.csv
│   ├── explainability_results.csv
│   ├── forecast_results.csv
│   └── risk_results.csv
│
├── src/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Run the Application Locally

### 1. Clone the repository

```bash
git clone https://github.com/Ezekiel008/EarlySignal_AI.git
cd EarlySignal_AI
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start EarlySignal AI

```bash
streamlit run app/app.py
```

---

## Prototype Boundary

The current version is a competition prototype.

Uploading an arbitrary organizational dataset does **not** automatically make it compatible with the trained models. Structural similarity alone is insufficient for valid model inference.

Real organizational deployment would require:

* data mapping and validation;
* organization-specific feature engineering;
* model retraining or recalibration;
* performance and bias evaluation;
* governance and access controls;
* monitoring for model drift; and
* agreed human review and escalation procedures.

---

## Future Organizational Integration

With appropriate organizational authorization and technical governance, the architecture could be extended to support:

* Google Sheets or spreadsheet-based monitoring workflows;
* monitoring information systems;
* organizational databases;
* approved APIs;
* automated data refresh;
* organization-specific model retraining;
* configurable early-warning thresholds; and
* operational alert workflows.

These are **future deployment capabilities**, not features demonstrated by the current prototype.

---

## Challenge Context

EarlySignal AI was developed as an AI-enabled real-world problem-solving project for the **3MTT × MIT Universal AI challenge**.

The project demonstrates how machine learning can support practical programme monitoring by moving from retrospective reporting toward earlier, explainable, and human-supervised decision support.

---

## Live Demo

Explore the deployed prototype:

**https://earlysignalai-global.streamlit.app/**

---

## Author

**Ezekiel Mbaya Ibrahim**

Monitoring, Evaluation & Learning (MEL) and Data Science

---

## Disclaimer

EarlySignal AI is a prototype developed using synthetic data for demonstration and learning purposes. Its outputs should not be used as the sole basis for humanitarian, development, funding, safeguarding, or operational decisions.
