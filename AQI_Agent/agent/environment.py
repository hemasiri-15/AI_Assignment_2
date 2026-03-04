"""
environment.py — Environment module (sensor reading + preprocessing)

Scalability note:
  - Currently reads pre-averaged CSV rows (Assignment 2 — Simple Reflex)
  - Future upgrade: add rolling window computation here for real hourly data
  - Future upgrade: add multi-station aggregation here
"""
import pandas as pd
import os


def load_sensor_data(csv_path):
    """Load sensor CSV. Returns DataFrame or None."""
    if not os.path.exists(csv_path):
        print(f"[ERROR] Sensor file not found: {csv_path}")
        print("Expected columns: Datetime, PM2.5, PM10, SO2, NOx, NH3, CO, O3")
        return None
    return pd.read_csv(csv_path)


# ── FUTURE COMPLEXITY HOOK ────────────────────────────────────────────────────
# When upgrading to Model-Based Agent (future assignment), add rolling window
# averaging here:
#
# def apply_rolling_averages(df):
#     """24-hr avg for aerosols, 8-hr max for gases (CPCB rule)"""
#     df["PM2.5"] = df["PM2.5"].rolling(window=24, min_periods=16).mean()
#     df["CO"]    = df["CO"].rolling(window=8,  min_periods=1).max()
#     return df
