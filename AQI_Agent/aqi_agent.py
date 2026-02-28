"""
Simple Reflex Agent — AQI Monitor
Reference: AIMA Chapter 2
Standard : CPCB India

PEAS:
  P: Correct AQI classification and health warnings
  E: City air with pollutants
  A: Console display of AQI and advisory
  S: CSV file with PM2.5, PM10, NO2, CO, SO2 readings

Agent Loop:
  Read CSV row -> Compute AQI -> Match rule -> Print advisory
"""

import csv
import os

BREAKPOINTS = {
    "PM2.5": [
        (0.0,   30.0,   0,   50),
        (30.1,  60.0,  51,  100),
        (60.1,  90.0, 101,  200),
        (90.1, 120.0, 201,  300),
        (120.1,250.0, 301,  400),
        (250.1,500.0, 401,  500),
    ],
    "PM10": [
        (0,    50,   0,   50),
        (51,  100,  51,  100),
        (101, 250, 101,  200),
        (251, 350, 201,  300),
        (351, 430, 301,  400),
        (431, 600, 401,  500),
    ],
    "NO2": [
        (0,    40,   0,   50),
        (41,   80,  51,  100),
        (81,  180, 101,  200),
        (181, 280, 201,  300),
        (281, 400, 301,  400),
        (401, 800, 401,  500),
    ],
    "CO": [
        (0.0,  1.0,   0,   50),
        (1.1,  2.0,  51,  100),
        (2.1, 10.0, 101,  200),
        (10.1,17.0, 201,  300),
        (17.1,34.0, 301,  400),
        (34.1,50.0, 401,  500),
    ],
    "SO2": [
        (0,    40,   0,   50),
        (41,   80,  51,  100),
        (81,  380, 101,  200),
        (381, 800, 201,  300),
        (801,1600, 301,  400),
        (1600,2100,401,  500),
    ],
}

RULES = [
    (0,    50,  "GOOD",         "Air quality is satisfactory. No health impact."),
    (51,  100,  "SATISFACTORY", "Minor discomfort for sensitive people."),
    (101, 200,  "MODERATE",     "Discomfort for people with lung or heart disease."),
    (201, 300,  "POOR",         "Breathing discomfort for most on prolonged exposure."),
    (301, 400,  "VERY POOR",    "Respiratory illness. Avoid outdoor activity."),
    (401, 500,  "SEVERE",       "Affects healthy people. Stay indoors. Wear N95."),
]


def compute_sub_index(concentration, pollutant):
    for (bp_lo, bp_hi, i_lo, i_hi) in BREAKPOINTS[pollutant]:
        if bp_lo <= concentration <= bp_hi:
            aqi = ((i_hi - i_lo) / (bp_hi - bp_lo)) * (concentration - bp_lo) + i_lo
            return round(aqi)
    return 500


def compute_aqi(pm25, pm10, no2, co, so2):
    sub = {
        "PM2.5" : compute_sub_index(pm25, "PM2.5"),
        "PM10"  : compute_sub_index(pm10, "PM10"),
        "NO2"   : compute_sub_index(no2,  "NO2"),
        "CO"    : compute_sub_index(co,   "CO"),
        "SO2"   : compute_sub_index(so2,  "SO2"),
    }
    overall  = max(sub.values())
    dominant = max(sub, key=sub.get)
    return overall, sub, dominant


def get_advisory(aqi_value):
    for (lo, hi, category, advisory) in RULES:
        if lo <= aqi_value <= hi:
            return category, advisory
    return "SEVERE", "Extremely hazardous. Stay indoors."


def read_sensor_file(filepath):
    percepts = []
    if not os.path.exists(filepath):
        print("ERROR: File not found:", filepath)
        return percepts
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                percepts.append({
                    "timestamp" : row["timestamp"],
                    "PM2.5"     : float(row["PM2.5"]),
                    "PM10"      : float(row["PM10"]),
                    "NO2"       : float(row["NO2"]),
                    "CO"        : float(row["CO"]),
                    "SO2"       : float(row["SO2"]),
                    "location"  : row["location"],
                })
            except (ValueError, KeyError) as e:
                print("Skipping row:", e)
    return percepts


def run_aqi_agent(sensor_file="sensor_data.csv"):
    print()
    print("=" * 55)
    print("  SIMPLE REFLEX AGENT — AQI MONITOR")
    print("=" * 55)
    print()

    percepts = read_sensor_file(sensor_file)
    if not percepts:
        return

    print("Loaded {} readings from {}".format(len(percepts), sensor_file))
    print()

    results = []
    for i, p in enumerate(percepts):
        aqi, sub, dominant = compute_aqi(
            p["PM2.5"], p["PM10"], p["NO2"], p["CO"], p["SO2"]
        )
        category, advisory = get_advisory(aqi)

        print("-" * 55)
        print("  Percept   :", i + 1)
        print("  Location  :", p["location"])
        print("  Time      :", p["timestamp"])
        print("  AQI       :", aqi, "[" + category + "]")
        print("  Advisory  :", advisory)
        print("  Dominant  :", dominant, "(sub-index =", sub[dominant], ")")
        print("  All subs  :", sub)
        print("-" * 55)

        results.append((p["timestamp"], p["location"], aqi, category))

    print()
    print("=" * 55)
    print("  SUMMARY")
    print("=" * 55)
    for (ts, loc, aqi, cat) in results:
        print("  {} | {} | {} | {}".format(ts, loc, aqi, cat))
    avg   = sum(r[2] for r in results) / len(results)
    worst = max(results, key=lambda x: x[2])
    print()
    print("  Average AQI :", round(avg, 1))
    print("  Worst       : AQI {} at {} ({})".format(worst[2], worst[0], worst[1]))
    print("=" * 55)
    print()


if __name__ == "__main__":
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    sensor_file = os.path.join(script_dir, "sensor_data.csv")
    run_aqi_agent(sensor_file)
