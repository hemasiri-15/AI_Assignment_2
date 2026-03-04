"""
aqi_agent.py — Entry point for AQI Monitoring Agent
AI Assignment 2 | Simple Reflex Agent (AIMA Chapter 2)

Architecture (scalable, modular):
  agent/subindex.py    — pollutant sub-index functions (CPCB breakpoints)
  agent/environment.py — sensor data loading and preprocessing
  agent/agent_core.py  — agent function and condition-action rules

To add a new pollutant: edit agent/subindex.py only (POLLUTANT_FUNCTIONS dict)
To upgrade agent type:  edit agent/agent_core.py only

Domain References:
  [1] Guttikunda, S. (2021). SIM-air Working Paper #46-2021. urbanemissions.info
  [2] CPCB AQI Tutorial Notebook (provided by instructor)
      https://app.cpcbccr.com/ccr_docs/How_AQI_Calculated.pdf
"""

import numpy as np
import pandas as pd
from agent.environment import load_sensor_data
from agent.agent_core  import compute_aqi, get_AQI_category

CSV_PATH = "sensor_data.csv"

DEMO_READINGS = [
    {"Datetime": "Example 1 — Very Poor (SIM-46-2021 pg.5)",
     "PM2.5": 200, "PM10": 225, "SO2": 30, "NOx": 55, "NH3": 50, "CO": 2.0, "O3": 111},
    {"Datetime": "Example 2 — Severe (SIM-46-2021 pg.5)",
     "PM2.5": 1200, "PM10": 1400, "SO2": 45, "NOx": 80, "NH3": 60, "CO": 5.0, "O3": 80},
    {"Datetime": "Example 3 — Good",
     "PM2.5": 20, "PM10": 35, "SO2": 15, "NOx": 20, "NH3": 30, "CO": 0.5, "O3": 30},
]


def print_result(timestamp, aqi_value, sub_indices, category, advisory):
    print(f"\n  Timestamp : {timestamp}")
    print(f"  AQI       : {round(aqi_value) if not pd.isna(aqi_value) else 'N/A'}")
    print(f"  Category  : {category}")
    print(f"  Advisory  : {advisory}")
    print(f"  Sub-indices:")
    for p, v in sub_indices.items():
        print(f"    {p:6s} → {v:.1f}")
    dominant = max(sub_indices, key=sub_indices.get)
    print(f"  Dominant Pollutant: {dominant} ({sub_indices[dominant]:.1f})")
    print("-" * 65)


def run():
    print("=" * 65)
    print("  AQI MONITORING AGENT — Simple Reflex Agent")
    print("  CPCB Methodology | SIM-46-2021 Reference")
    print("=" * 65)

    df = load_sensor_data(CSV_PATH)
    rows = df.to_dict("records") if df is not None else DEMO_READINGS

    if df is None:
        print("  [INFO] No sensor_data.csv found. Running with demo values.\n")

    for row in rows:
        timestamp          = row.get("Datetime", "—")
        aqi_value, subs    = compute_aqi(row)
        category, advisory = get_AQI_category(aqi_value)
        print_result(timestamp, aqi_value, subs, category, advisory)

    print("\n  Agent loop complete.")
    print("=" * 65)


if __name__ == "__main__":
    run()
