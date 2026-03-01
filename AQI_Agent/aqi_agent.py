"""
AQI Agent — AI Assignment 2
Agent Type  : Simple Reflex Agent (AIMA Chapter 2)
Architecture: Condition-Action Rules

Domain References:
  [1] Guttikunda, S. (2021). 10 Frequently Asked Questions on Air Quality Index.
      SIM-air Working Paper Series #46-2021. urbanemissions.info
  [2] Kaggle Tutorial — "Calculating AQI (Air Quality Index) in India"
      CPCB official formula: https://app.cpcbccr.com/ccr_docs/How_AQI_Calculated.pdf

PEAS Description:
  Performance : Correct AQI category and advisory for each hourly reading
  Environment : City air with pollutants — PM2.5, PM10, SO2, NOx, NH3, CO, O3
  Actuators   : Console output (AQI value, category, health advisory)
  Sensors     : CSV file rows (one row = one hourly percept from monitoring stations)

AQI Formula (CPCB, from Reference [1] FAQ#03):
  sub_index = ((AQI_hi - AQI_lo) / (BP_hi - BP_lo)) * (CONC - BP_lo) + AQI_lo
  Final AQI  = MAX of all sub-indices (Reference [1] FAQ#04)

Averaging Rules (from Reference [2]):
  PM2.5, PM10, SO2, NOx, NH3  → 24-hour rolling average (min 16 data points)
  CO, O3                       → 8-hour rolling maximum

Validity Check (from Reference [2]):
  AQI is computed only if:
    - At least one of PM2.5 or PM10 is available
    - At least 3 of the 7 pollutants have valid readings
"""

import pandas as pd
import numpy as np
import os


# ─── SUB-INDEX FUNCTIONS (CPCB breakpoints, from Reference [2]) ──────────────
# Each function maps a pollutant concentration to its AQI sub-index (0–500)
# Source: Kaggle tutorial "calculating-aqi-air-quality-index-tutorial.ipynb"

def get_PM25_subindex(x):
    """PM2.5 in µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0:
        return 0
    if x <= 30:   return x * 50 / 30
    elif x <= 60:  return 50 + (x - 30) * 50 / 30
    elif x <= 90:  return 100 + (x - 60) * 100 / 30
    elif x <= 120: return 200 + (x - 90) * 100 / 30
    elif x <= 250: return 300 + (x - 120) * 100 / 130
    else:          return 400 + (x - 250) * 100 / 130


def get_PM10_subindex(x):
    """PM10 in µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0:
        return 0
    if x <= 50:    return x
    elif x <= 100: return x
    elif x <= 250: return 100 + (x - 100) * 100 / 150
    elif x <= 350: return 200 + (x - 250)
    elif x <= 430: return 300 + (x - 350) * 100 / 80
    else:          return 400 + (x - 430) * 100 / 80


def get_SO2_subindex(x):
    """SO2 in µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0:
        return 0
    if x <= 40:     return x * 50 / 40
    elif x <= 80:   return 50 + (x - 40) * 50 / 40
    elif x <= 380:  return 100 + (x - 80) * 100 / 300
    elif x <= 800:  return 200 + (x - 380) * 100 / 420
    elif x <= 1600: return 300 + (x - 800) * 100 / 800
    else:           return 400 + (x - 1600) * 100 / 800


def get_NOx_subindex(x):
    """NOx in ppb, 24-hr average"""
    if pd.isna(x) or x < 0:
        return 0
    if x <= 40:    return x * 50 / 40
    elif x <= 80:  return 50 + (x - 40) * 50 / 40
    elif x <= 180: return 100 + (x - 80) * 100 / 100
    elif x <= 280: return 200 + (x - 180) * 100 / 100
    elif x <= 400: return 300 + (x - 280) * 100 / 120
    else:          return 400 + (x - 400) * 100 / 120


def get_NH3_subindex(x):
    """NH3 in µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0:
        return 0
    if x <= 200:    return x * 50 / 200
    elif x <= 400:  return 50 + (x - 200) * 50 / 200
    elif x <= 800:  return 100 + (x - 400) * 100 / 400
    elif x <= 1200: return 200 + (x - 800) * 100 / 400
    elif x <= 1800: return 300 + (x - 1200) * 100 / 600
    else:           return 400 + (x - 1800) * 100 / 600


def get_CO_subindex(x):
    """CO in mg/m³, 8-hr max"""
    if pd.isna(x) or x < 0:
        return 0
    if x <= 1:    return x * 50 / 1
    elif x <= 2:  return 50 + (x - 1) * 50 / 1
    elif x <= 10: return 100 + (x - 2) * 100 / 8
    elif x <= 17: return 200 + (x - 10) * 100 / 7
    elif x <= 34: return 300 + (x - 17) * 100 / 17
    else:         return 400 + (x - 34) * 100 / 17


def get_O3_subindex(x):
    """O3 in µg/m³, 8-hr max"""
    if pd.isna(x) or x < 0:
        return 0
    if x <= 50:    return x * 50 / 50
    elif x <= 100: return 50 + (x - 50) * 50 / 50
    elif x <= 168: return 100 + (x - 100) * 100 / 68
    elif x <= 208: return 200 + (x - 168) * 100 / 40
    elif x <= 748: return 300 + (x - 208) * 100 / 539
    else:          return 400 + (x - 400) * 100 / 539


# ─── AQI CATEGORY (Reference [1] FAQ#03 breakpoint table) ───────────────────

def get_AQI_category(aqi):
    """Map a numeric AQI value to its CPCB category and health advisory."""
    if pd.isna(aqi):
        return "UNKNOWN", "Insufficient data to compute AQI."
    aqi = round(aqi)
    if aqi <= 50:
        return "GOOD", \
               "Air quality is satisfactory. No health risk. Enjoy outdoor activities."
    elif aqi <= 100:
        return "SATISFACTORY", \
               "Minor discomfort to sensitive people (asthma, heart conditions). Generally safe."
    elif aqi <= 200:
        return "MODERATE", \
               "People with lung/heart disease, children, elderly may feel discomfort. Others OK."
    elif aqi <= 300:
        return "POOR", \
               "Most people may experience breathing discomfort on prolonged exposure. Avoid long outdoor activity."
    elif aqi <= 400:
        return "VERY POOR", \
               "Respiratory illness on prolonged exposure. Avoid outdoor activity."
    else:
        return "SEVERE", \
               "HEALTH EMERGENCY! Stay indoors. Wear N95 mask if you must go outside."


# ─── AGENT: COMPUTE SUB-INDICES AND FINAL AQI ────────────────────────────────

def compute_aqi(row):
    """
    Agent Function: f(percept) → AQI

    Takes one row of pre-averaged sensor readings and returns the AQI.
    The row must contain 24-hr averages for PM2.5/PM10/SO2/NOx/NH3
    and 8-hr max values for CO/O3 (per CPCB rules, Reference [2]).

    Final AQI = MAX of sub-indices, valid only if:
      - At least one of PM2.5 or PM10 is available
      - At least 3 out of 7 pollutants have readings  (Reference [2])
    """
    sub_indices = {
        "PM2.5": get_PM25_subindex(row.get("PM2.5", np.nan)),
        "PM10":  get_PM10_subindex(row.get("PM10",  np.nan)),
        "SO2":   get_SO2_subindex(row.get("SO2",   np.nan)),
        "NOx":   get_NOx_subindex(row.get("NOx",   np.nan)),
        "NH3":   get_NH3_subindex(row.get("NH3",   np.nan)),
        "CO":    get_CO_subindex(row.get("CO",    np.nan)),
        "O3":    get_O3_subindex(row.get("O3",    np.nan)),
    }

    # Validity check (from Reference [2])
    valid_count   = sum(1 for v in sub_indices.values() if v > 0)
    pm_available  = (sub_indices["PM2.5"] > 0) or (sub_indices["PM10"] > 0)

    if not pm_available or valid_count < 3:
        return np.nan, sub_indices

    # AQI = maximum sub-index (Reference [1] FAQ#04 — never an average of all)
    aqi = max(sub_indices.values())
    return aqi, sub_indices


# ─── AGENT PROGRAM: PERCEPT → ACTION LOOP ────────────────────────────────────

def run_aqi_agent(csv_path):
    """
    Agent Program — main loop.

    Reads the CSV (sensor module), computes AQI for each row,
    and prints the health advisory (actuator).

    The agent is a Simple Reflex Agent:
      - Each row is one percept (no memory of past rows)
      - Condition-action rules map AQI value → advisory category
    """
    # ── Load data ────────────────────────────────────────────────────────────
    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV file not found: {csv_path}")
        print("Please provide a CSV with columns: Datetime, PM2.5, PM10, SO2, NOx, NH3, CO, O3")
        return

    df = pd.read_csv(csv_path)
    print("=" * 65)
    print("  AQI MONITORING AGENT — Simple Reflex Agent")
    print("  CPCB Methodology (India)")
    print("  References: SIM-46-2021 & CPCB official formula")
    print("=" * 65)
    print(f"  Loaded {len(df)} sensor readings from: {csv_path}")
    print()

    # ── Process each row (each percept) ──────────────────────────────────────
    for idx, row in df.iterrows():
        timestamp = row.get("Datetime", row.get("datetime", f"Row {idx+1}"))
        aqi_value, sub_indices = compute_aqi(row)
        category, advisory     = get_AQI_category(aqi_value)

        # ── Print action ──────────────────────────────────────────────────
        print(f"  Timestamp : {timestamp}")
        print(f"  AQI       : {round(aqi_value) if not pd.isna(aqi_value) else 'N/A'}")
        print(f"  Category  : {category}")
        print(f"  Advisory  : {advisory}")
        print()

        # Sub-index breakdown (useful for debugging / professor review)
        top_pollutant = max(sub_indices, key=sub_indices.get)
        top_value     = sub_indices[top_pollutant]
        if top_value > 0:
            print(f"  Dominant Pollutant: {top_pollutant} (sub-index = {top_value:.1f})")
        print("-" * 65)

    print()
    print("  Agent loop complete. All sensor readings processed.")
    print("=" * 65)


# ─── DEMO: SAMPLE DATA (runs if no CSV is provided) ─────────────────────────

def run_demo():
    """
    Run the agent with hardcoded sample values to demonstrate it works.
    These values are from the example calculations in Reference [1] FAQ#03.
    """
    print("=" * 65)
    print("  AQI AGENT DEMO — using example values from SIM-46-2021")
    print("=" * 65)

    # Example readings from the PDF (Reference [1] pg. 5)
    demo_readings = [
        {
            "Datetime": "Example 1 (PDF pg.5 — Very Poor day)",
            "PM2.5": 200, "PM10": 225, "SO2": 30,
            "NOx": 55, "NH3": 50, "CO": 2.0, "O3": 111
        },
        {
            "Datetime": "Example 2 (PDF pg.5 — Severe day)",
            "PM2.5": 1200, "PM10": 1400, "SO2": 45,
            "NOx": 80, "NH3": 60, "CO": 5.0, "O3": 80
        },
        {
            "Datetime": "Example 3 (Good air quality day)",
            "PM2.5": 20, "PM10": 35, "SO2": 15,
            "NOx": 20, "NH3": 30, "CO": 0.5, "O3": 30
        },
    ]

    for reading in demo_readings:
        timestamp = reading["Datetime"]
        aqi_value, sub_indices = compute_aqi(reading)
        category, advisory     = get_AQI_category(aqi_value)

        print(f"\n  Timestamp : {timestamp}")
        print(f"  Inputs    : PM2.5={reading['PM2.5']} PM10={reading['PM10']} "
              f"SO2={reading['SO2']} NOx={reading['NOx']} "
              f"CO={reading['CO']} O3={reading['O3']}")
        print(f"  Sub-indices:")
        for pollutant, si in sub_indices.items():
            print(f"    {pollutant:6s} → {si:.1f}")
        print(f"  AQI       : {round(aqi_value) if not pd.isna(aqi_value) else 'N/A'}")
        print(f"  Category  : {category}")
        print(f"  Advisory  : {advisory}")
        print("-" * 65)


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Try to load the real sensor CSV first
    CSV_PATH = "sensor_data.csv"

    if os.path.exists(CSV_PATH):
        run_aqi_agent(CSV_PATH)
    else:
        print(f"[INFO] '{CSV_PATH}' not found. Running demo with reference values.\n")
        run_demo()
