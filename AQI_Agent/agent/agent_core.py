"""
agent_core.py — AQI Agent core logic

Agent Type : Simple Reflex Agent (AIMA Chapter 2)
             Each percept (CSV row) → condition-action rule → advisory

Scalability note:
  - To upgrade to Model-Based Agent: add internal state tracking here
  - To add alert thresholds or notifications: add action handlers here
  - To support multiple cities: pass station_id into compute_aqi()
"""
import numpy as np
import pandas as pd
from agent.subindex import POLLUTANT_FUNCTIONS


def compute_aqi(row):
    """
    Agent Function: f(percept) → AQI

    Computes sub-index for each registered pollutant,
    then returns MAX as final AQI (CPCB rule, SIM-46-2021 FAQ#04).

    Validity: needs PM2.5 or PM10 + at least 3 pollutants total.
    """
    sub_indices = {
        pollutant: fn(row.get(pollutant, np.nan))
        for pollutant, fn in POLLUTANT_FUNCTIONS.items()
    }

    valid_count  = sum(1 for v in sub_indices.values() if v > 0)
    pm_available = (sub_indices.get("PM2.5", 0) > 0) or \
                   (sub_indices.get("PM10",  0) > 0)

    if not pm_available or valid_count < 3:
        return np.nan, sub_indices

    return max(sub_indices.values()), sub_indices


def get_AQI_category(aqi):
    """Condition-action rules: AQI value → category + health advisory."""
    if pd.isna(aqi):
        return "UNKNOWN", "Insufficient data to compute AQI."
    aqi = round(aqi)
    if aqi <= 50:
        return "GOOD",         "Air quality satisfactory. No health risk."
    elif aqi <= 100:
        return "SATISFACTORY", "Minor discomfort for sensitive groups."
    elif aqi <= 200:
        return "MODERATE",     "Lung/heart patients and elderly may feel discomfort."
    elif aqi <= 300:
        return "POOR",         "Breathing discomfort for most on prolonged exposure."
    elif aqi <= 400:
        return "VERY POOR",    "Respiratory illness risk. Avoid outdoor activity."
    else:
        return "SEVERE",       "HEALTH EMERGENCY! Stay indoors. Wear N95 mask."
