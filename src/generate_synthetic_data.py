from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


SEED = 42

OUT = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "synthetic"
    / "earlysignal_monitoring_data.csv"
)

rng = np.random.default_rng(SEED)


# ============================================================
# PROGRAMME STRUCTURE
# ============================================================

programmes = [
    "Community Resilience Programme",
    "Livelihood Recovery Initiative",
    "Education Access Project",
    "Nutrition Support Programme",
    "WASH Resilience Initiative",
]

sectors = {
    "Community Resilience Programme": "Protection/Resilience",
    "Livelihood Recovery Initiative": "Livelihoods",
    "Education Access Project": "Education",
    "Nutrition Support Programme": "Nutrition",
    "WASH Resilience Initiative": "WASH",
}

lgas = [
    "Maiduguri",
    "Jere",
    "Konduga",
    "Mafa",
    "Bama",
    "Ngala",
    "Dikwa",
    "Gwoza",
]

communities = {
    lga: [f"{lga} Site {i}" for i in range(1, 7)]
    for lga in lgas
}

months = pd.date_range(
    "2024-01-01",
    "2026-08-01",
    freq="MS"
)


# ============================================================
# PERSISTENT PROGRAMME / LOCATION EFFECTS
# ============================================================

programme_effect = {
    "Community Resilience Programme": 0.03,
    "Livelihood Recovery Initiative": 0.00,
    "Education Access Project": -0.01,
    "Nutrition Support Programme": 0.02,
    "WASH Resilience Initiative": -0.02,
}

lga_effect = {
    "Maiduguri": 0.020,
    "Jere": 0.010,
    "Konduga": 0.000,
    "Mafa": -0.010,
    "Bama": -0.015,
    "Ngala": -0.025,
    "Dikwa": -0.020,
    "Gwoza": -0.030,
}


# ============================================================
# GENERATE TRUE MONTHLY PANEL DATA
# ============================================================

rows = []

record_counter = 1

for programme in programmes:

    for lga in lgas:

        for community in communities[lga]:

            # Persistent community-level characteristics
            community_effect = rng.normal(
                0,
                0.025
            )

            target_base = rng.integers(
                250,
                1000
            )

            # Initial historical conditions
            previous_rate = np.clip(
                0.82
                + programme_effect[programme]
                + lga_effect[lga]
                + community_effect
                + rng.normal(0, 0.05),
                0.50,
                1.10
            )

            previous_activity = np.clip(
                rng.normal(0.78, 0.07),
                0.40,
                1.00
            )

            previous_staff = np.clip(
                rng.normal(0.88, 0.05),
                0.55,
                1.00
            )

            previous_access = np.clip(
                rng.beta(2.2, 5.0),
                0,
                1
            )

            for reporting_date in months:

                # ------------------------------------------------
                # Seasonal effect
                # ------------------------------------------------

                seasonal_effect = (
                    0.03
                    * np.sin(
                        2
                        * np.pi
                        * (reporting_date.month - 1)
                        / 12
                    )
                )

                # ------------------------------------------------
                # Activity completion
                # ------------------------------------------------

                activity_completion = np.clip(
                    0.65 * previous_activity
                    + 0.35 * rng.beta(7, 2.4)
                    + rng.normal(0, 0.025),
                    0.20,
                    1.00
                )

                # ------------------------------------------------
                # Budget utilisation
                # ------------------------------------------------

                budget_utilisation = np.clip(
                    0.75 * rng.normal(0.80, 0.11)
                    + 0.25 * (
                        0.75
                        + 0.15 * activity_completion
                    )
                    + rng.normal(0, 0.03),
                    0.25,
                    1.20
                )

                # ------------------------------------------------
                # Reporting delay
                # ------------------------------------------------

                reporting_delay = int(
                    np.clip(
                        round(
                            0.50
                            * rng.gamma(2.0, 2.8)
                            + 0.50
                            * (1 - activity_completion)
                            * 18
                            + rng.normal(0, 1.2)
                        ),
                        0,
                        30
                    )
                )

                # ------------------------------------------------
                # Complaints
                # ------------------------------------------------

                complaints_lambda = (
                    2.2
                    + 4.5
                    * max(
                        0,
                        0.75 - previous_rate
                    )
                    + 2.0
                    * previous_access
                )

                complaints_count = max(
                    0,
                    int(
                        rng.poisson(
                            complaints_lambda
                        )
                    )
                )

                # ------------------------------------------------
                # Staff availability
                # ------------------------------------------------

                staff_availability = np.clip(
                    0.65 * previous_staff
                    + 0.35
                    * rng.normal(
                        0.88,
                        0.07
                    )
                    + rng.normal(0, 0.02),
                    0.45,
                    1.00
                )

                # ------------------------------------------------
                # Supply delay
                # ------------------------------------------------

                supply_delay = int(
                    np.clip(
                        round(
                            0.55
                            * rng.gamma(
                                1.8,
                                3.0
                            )
                            + 0.45
                            * previous_access
                            * 18
                            + rng.normal(
                                0,
                                1.5
                            )
                        ),
                        0,
                        35
                    )
                )

                # ------------------------------------------------
                # Access constraint
                # ------------------------------------------------

                access_constraint = np.clip(
                    0.70
                    * previous_access
                    + 0.30
                    * rng.beta(
                        2.2,
                        5.0
                    )
                    + rng.normal(
                        0,
                        0.025
                    ),
                    0,
                    1
                )

                # ------------------------------------------------
                # Data quality
                # ------------------------------------------------

                data_quality = np.clip(
                    rng.normal(
                        0.91
                        - 0.0015
                        * reporting_delay,
                        0.045
                    ),
                    0.55,
                    1.00
                )

                # ------------------------------------------------
                # Monthly target
                # ------------------------------------------------

                monthly_target = int(
                    np.clip(
                        round(
                            target_base
                            * (
                                1
                                + rng.normal(
                                    0,
                                    0.08
                                )
                            )
                        ),
                        120,
                        1200
                    )
                )

                # ------------------------------------------------
                # Achievement rate
                #
                # IMPORTANT:
                # Previous month's performance contributes directly
                # to current performance.
                # ------------------------------------------------

                noise = rng.normal(
                    0,
                    0.05
                )

                achievement_rate = (
                    0.16
                    + 0.26
                    * activity_completion
                    + 0.10
                    * min(
                        budget_utilisation,
                        1.0
                    )
                    + 0.12
                    * staff_availability
                    + 0.30
                    * previous_rate
                    + 0.06
                    * data_quality
                    - 0.0045
                    * reporting_delay
                    - 0.0035
                    * supply_delay
                    - 0.10
                    * access_constraint
                    - 0.004
                    * complaints_count
                    + programme_effect[
                        programme
                    ]
                    + lga_effect[
                        lga
                    ]
                    + community_effect
                    + seasonal_effect
                    + noise
                )

                achievement_rate = np.clip(
                    achievement_rate,
                    0.18,
                    1.30
                )

                rows.append(
                    {
                        "record_id":
                            f"ES-{record_counter:06d}",

                        "reporting_date":
                            reporting_date,

                        "programme_name":
                            programme,

                        "sector":
                            sectors[
                                programme
                            ],

                        "state":
                            "Borno",

                        "lga":
                            lga,

                        "community":
                            community,

                        "monthly_target":
                            monthly_target,

                        "achievement_rate":
                            achievement_rate,

                        "activity_completion_rate":
                            activity_completion,

                        "budget_utilisation_rate":
                            budget_utilisation,

                        "reporting_delay_days":
                            reporting_delay,

                        "complaints_count":
                            complaints_count,

                        "staff_availability_rate":
                            staff_availability,

                        "supply_delay_days":
                            supply_delay,

                        "previous_month_achievement_rate":
                            previous_rate,

                        "access_constraint_score":
                            access_constraint,

                        "data_quality_score":
                            data_quality,
                    }
                )

                # ------------------------------------------------
                # Carry current conditions into next month
                # ------------------------------------------------

                previous_rate = achievement_rate
                previous_activity = (
                    activity_completion
                )
                previous_staff = (
                    staff_availability
                )
                previous_access = (
                    access_constraint
                )

                record_counter += 1


frame = pd.DataFrame(rows)


# ============================================================
# INJECT ANOMALIES
# ============================================================

N_ROWS = len(frame)

anomaly_flag = np.zeros(
    N_ROWS,
    dtype=int
)

anomaly_indices = rng.choice(
    np.arange(N_ROWS),
    size=int(
        N_ROWS * 0.025
    ),
    replace=False
)

anomaly_flag[
    anomaly_indices
] = 1


for idx in anomaly_indices:

    anomaly_type = rng.integers(
        0,
        4
    )

    if anomaly_type == 0:

        frame.loc[
            idx,
            "reporting_delay_days"
        ] = rng.integers(
            25,
            50
        )

    elif anomaly_type == 1:

        frame.loc[
            idx,
            "achievement_rate"
        ] = np.clip(
            frame.loc[
                idx,
                "achievement_rate"
            ]
            * rng.uniform(
                0.35,
                0.60
            ),
            0.08,
            1.30
        )

    elif anomaly_type == 2:

        frame.loc[
            idx,
            "supply_delay_days"
        ] = rng.integers(
            25,
            55
        )

    else:

        frame.loc[
            idx,
            "complaints_count"
        ] = rng.integers(
            14,
            35
        )


frame[
    "anomaly_flag"
] = anomaly_flag


# ============================================================
# MONTHLY ACHIEVEMENT
# ============================================================

frame[
    "monthly_achievement"
] = np.maximum(
    1,
    np.round(
        frame[
            "monthly_target"
        ]
        * frame[
            "achievement_rate"
        ]
    )
).astype(int)


# ============================================================
# RISK SCORE
# ============================================================

risk_score = (
    0.33
    * (
        1
        - np.minimum(
            frame[
                "achievement_rate"
            ],
            1.0
        )
    )
    + 0.20
    * (
        1
        - frame[
            "activity_completion_rate"
        ]
    )
    + 0.10
    * np.clip(
        frame[
            "reporting_delay_days"
        ]
        / 20,
        0,
        1
    )
    + 0.10
    * np.clip(
        frame[
            "supply_delay_days"
        ]
        / 25,
        0,
        1
    )
    + 0.08
    * frame[
        "access_constraint_score"
    ]
    + 0.07
    * (
        1
        - frame[
            "staff_availability_rate"
        ]
    )
    + 0.05
    * np.clip(
        frame[
            "complaints_count"
        ]
        / 15,
        0,
        1
    )
    + 0.04
    * (
        1
        - frame[
            "data_quality_score"
        ]
    )
    + 0.03
    * frame[
        "anomaly_flag"
    ]
)


# Target approximately:
# Low    ~55%
# Medium ~36%
# High   ~9%

frame[
    "risk_label"
] = np.where(
    risk_score >= 0.30,
    "High",
    np.where(
        risk_score >= 0.24,
        "Medium",
        "Low"
    )
)


# ============================================================
# RESPONSIBLE RECOMMENDED ACTIONS
# ============================================================

recommended_actions = []

for _, row in frame.iterrows():

    if row["risk_label"] == "High":

        if (
            row[
                "reporting_delay_days"
            ]
            >= 14
        ):

            action = (
                "Recommended for human review: "
                "investigate reporting bottlenecks "
                "and validate the latest field data."
            )

        elif (
            row[
                "supply_delay_days"
            ]
            >= 14
        ):

            action = (
                "Recommended for human review: "
                "investigate supply-chain delays "
                "and assess potential implementation impact."
            )

        elif (
            row[
                "activity_completion_rate"
            ]
            < 0.60
        ):

            action = (
                "Recommended for human review: "
                "assess implementation bottlenecks "
                "and possible recovery actions."
            )

        elif (
            row[
                "achievement_rate"
            ]
            < 0.65
        ):

            action = (
                "Recommended for human review: "
                "examine target underachievement "
                "and verify contributing factors."
            )

        else:

            action = (
                "Recommended for human review: "
                "review the combined risk indicators "
                "before deciding on corrective action."
            )

    elif row[
        "risk_label"
    ] == "Medium":

        action = (
            "Monitor closely and review contributing "
            "indicators during the next programme check-in."
        )

    else:

        action = (
            "Continue routine monitoring; "
            "no immediate escalation indicated."
        )

    recommended_actions.append(
        action
    )


frame[
    "recommended_action"
] = recommended_actions


# ============================================================
# FINAL COLUMN ORDER
# ============================================================

column_order = [
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
    "data_quality_score",
    "anomaly_flag",
    "risk_label",
    "recommended_action",
]

frame = frame[
    column_order
].copy()


# ============================================================
# ROUND NUMERIC RATES
# ============================================================

rate_columns = [
    "achievement_rate",
    "activity_completion_rate",
    "budget_utilisation_rate",
    "staff_availability_rate",
    "previous_month_achievement_rate",
    "access_constraint_score",
    "data_quality_score",
]

frame[
    rate_columns
] = frame[
    rate_columns
].round(4)


# ============================================================
# SORT AND SAVE
# ============================================================

frame = frame.sort_values(
    [
        "programme_name",
        "state",
        "lga",
        "community",
        "reporting_date",
    ]
).reset_index(
    drop=True
)


OUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

frame.to_csv(
    OUT,
    index=False
)


# ============================================================
# VALIDATION OUTPUT
# ============================================================

unit_date_duplicates = (
    frame.groupby(
        [
            "programme_name",
            "state",
            "lga",
            "community",
            "reporting_date",
        ]
    )
    .size()
    .gt(1)
    .sum()
)


temporal_correlation = (
    frame[
        "achievement_rate"
    ]
    .corr(
        frame[
            "previous_month_achievement_rate"
        ]
    )
)


print(
    f"Saved {len(frame):,} rows to:"
)
print(OUT)

print(
    "\nShape:",
    frame.shape
)

print(
    "\nDate range:",
    frame[
        "reporting_date"
    ].min().date(),
    "to",
    frame[
        "reporting_date"
    ].max().date()
)

print(
    "\nDuplicate programme/location/community/month records:",
    unit_date_duplicates
)

print(
    "\nRisk distribution:"
)

risk_distribution = (
    frame[
        "risk_label"
    ]
    .value_counts(
        normalize=True
    )
    .mul(100)
    .round(2)
)

print(
    risk_distribution
)

print(
    "\nAnomaly rate:",
    round(
        frame[
            "anomaly_flag"
        ].mean()
        * 100,
        2
    ),
    "%"
)

print(
    "\nAchievement vs previous-month achievement correlation:",
    round(
        temporal_correlation,
        3
    )
)

print(
    "\nSynthetic panel generation complete."
)