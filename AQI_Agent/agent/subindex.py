"""
subindex.py — Pollutant sub-index calculation functions
CPCB breakpoint interpolation formula (SIM-46-2021, Reference [1])

Scalability note: To add a new pollutant, simply add a new function here
following the same pattern, then register it in agent_core.py.
"""
import numpy as np
import pandas as pd


def get_PM25_subindex(x):
    """PM2.5 µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0: return 0
    if x <= 30:    return x * 50 / 30
    elif x <= 60:  return 50 + (x - 30) * 50 / 30
    elif x <= 90:  return 100 + (x - 60) * 100 / 30
    elif x <= 120: return 200 + (x - 90) * 100 / 30
    elif x <= 250: return 300 + (x - 120) * 100 / 130
    else:          return 400 + (x - 250) * 100 / 130

def get_PM10_subindex(x):
    """PM10 µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0: return 0
    if x <= 50:    return x
    elif x <= 100: return x
    elif x <= 250: return 100 + (x - 100) * 100 / 150
    elif x <= 350: return 200 + (x - 250)
    elif x <= 430: return 300 + (x - 350) * 100 / 80
    else:          return 400 + (x - 430) * 100 / 80

def get_SO2_subindex(x):
    """SO2 µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0: return 0
    if x <= 40:     return x * 50 / 40
    elif x <= 80:   return 50 + (x - 40) * 50 / 40
    elif x <= 380:  return 100 + (x - 80) * 100 / 300
    elif x <= 800:  return 200 + (x - 380) * 100 / 420
    elif x <= 1600: return 300 + (x - 800) * 100 / 800
    else:           return 400 + (x - 1600) * 100 / 800

def get_NOx_subindex(x):
    """NOx ppb, 24-hr average"""
    if pd.isna(x) or x < 0: return 0
    if x <= 40:    return x * 50 / 40
    elif x <= 80:  return 50 + (x - 40) * 50 / 40
    elif x <= 180: return 100 + (x - 80) * 100 / 100
    elif x <= 280: return 200 + (x - 180) * 100 / 100
    elif x <= 400: return 300 + (x - 280) * 100 / 120
    else:          return 400 + (x - 400) * 100 / 120

def get_NH3_subindex(x):
    """NH3 µg/m³, 24-hr average"""
    if pd.isna(x) or x < 0: return 0
    if x <= 200:    return x * 50 / 200
    elif x <= 400:  return 50 + (x - 200) * 50 / 200
    elif x <= 800:  return 100 + (x - 400) * 100 / 400
    elif x <= 1200: return 200 + (x - 800) * 100 / 400
    elif x <= 1800: return 300 + (x - 1200) * 100 / 600
    else:           return 400 + (x - 1800) * 100 / 600

def get_CO_subindex(x):
    """CO mg/m³, 8-hr max"""
    if pd.isna(x) or x < 0: return 0
    if x <= 1:    return x * 50 / 1
    elif x <= 2:  return 50 + (x - 1) * 50 / 1
    elif x <= 10: return 100 + (x - 2) * 100 / 8
    elif x <= 17: return 200 + (x - 10) * 100 / 7
    elif x <= 34: return 300 + (x - 17) * 100 / 17
    else:         return 400 + (x - 34) * 100 / 17

def get_O3_subindex(x):
    """O3 µg/m³, 8-hr max"""
    if pd.isna(x) or x < 0: return 0
    if x <= 50:    return x * 50 / 50
    elif x <= 100: return 50 + (x - 50) * 50 / 50
    elif x <= 168: return 100 + (x - 100) * 100 / 68
    elif x <= 208: return 200 + (x - 168) * 100 / 40
    elif x <= 748: return 300 + (x - 208) * 100 / 539
    else:          return 400 + (x - 400) * 100 / 539


# ── Pollutant registry — add new pollutants here only ────────────────────────
# Format: "column_name": function
# This is the ONLY place you need to edit to add a new pollutant.
POLLUTANT_FUNCTIONS = {
    "PM2.5": get_PM25_subindex,
    "PM10":  get_PM10_subindex,
    "SO2":   get_SO2_subindex,
    "NOx":   get_NOx_subindex,
    "NH3":   get_NH3_subindex,
    "CO":    get_CO_subindex,
    "O3":    get_O3_subindex,
}
