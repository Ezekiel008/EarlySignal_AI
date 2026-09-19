# EarlySignal AI — Synthetic Dataset Specification

The prototype dataset represents monthly monitoring observations from humanitarian and development programmes across multiple LGAs and sectors.

| Field | Meaning |
|---|---|
| record_id | Unique observation identifier |
| reporting_date | Monthly reporting period |
| programme_name | Programme name |
| sector | Programme sector |
| state | State |
| lga | Local Government Area |
| community | Community/site |
| monthly_target | Planned monthly target |
| monthly_achievement | Actual monthly achievement |
| achievement_rate | Achievement / target |
| activity_completion_rate | Proportion of planned activities completed |
| budget_utilisation_rate | Proportion of planned monthly budget utilized |
| reporting_delay_days | Days report was submitted late |
| complaints_count | Number of complaints/issues logged |
| staff_availability_rate | Proportion of required field staff available |
| supply_delay_days | Days of supply/procurement delay |
| previous_month_achievement_rate | Prior month's achievement rate proxy |
| access_constraint_score | 0–1 operational access constraint severity |
| data_quality_score | 0–1 data completeness/consistency proxy |
| anomaly_flag | Synthetic ground-truth anomaly marker |
| risk_label | Low / Medium / High implementation risk |
| recommended_action | Human-review-oriented next-step recommendation |

## Intended AI tasks
- Regression: forecast next-period achievement rate
- Classification: identify implementation risk level
- Anomaly detection: flag unusual records
- Explainability: identify major factors behind a risk prediction
- Geographic intelligence: map risk and performance by LGA/community
- Early-warning priority: combine signals into a human-readable action queue
