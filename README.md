# AI Assignment 2

**Subject:** Artificial Intelligence
**Reference:** Russell & Norvig — Artificial Intelligence: A Modern Approach (AIMA)

---

## Folder Structure

```
AI_Assignment_2/
│
├── README.md
├── requirements.txt
│
├── docs/
│   ├── agent_architecture.md
│   ├── turing_vs_captcha.md
│   └── search_algorithm_analysis.md
│
├── Turing_Captcha/
│   ├── architecture_design.md
│   ├── captcha_generator.py
│   └── captcha_demo.py
│
├── AQI_Agent/
│   ├── aqi_agent.py
│   ├── sensor_data.csv
│   └── agent/
│       ├── subindex.py
│       ├── environment.py
│       └── agent_core.py
│
└── Search_Algorithms/
    ├── bfs.py
    ├── dfs.py
    ├── dls.py
    ├── performance_comparison.py
    └── problems/
        ├── missionaries_cannibals.py
        ├── water_jug.py
        ├── eight_queens.py
        └── tic_tac_toe.py
```

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### AQI Agent
```bash
cd AQI_Agent
python3 aqi_agent.py
```

### Turing Test and CAPTCHA Demo
```bash
cd Turing_Captcha
python3 turing_captcha_demo.py
```

### Search Algorithms
```bash
cd Search_Algorithms

python3 bfs.py
python3 dfs.py
python3 performance_comparison.py

python3 problems/missionaries_cannibals.py
python3 problems/water_jug.py
python3 problems/eight_queens.py
python3 problems/tic_tac_toe.py
```

### DLS (Depth-Limited Search) Demo
```bash
cd Search_Algorithms
python3 dls.py
```

---

## 	Concepts Covered

### Agent Types (AIMA Chapter 2)

| Agent | Type | File |
|-------|------|------|
| AQI Monitor | Simple Reflex Agent | aqi_agent.py |
| CAPTCHA | Simple Reflex Agent | turing_captcha_demo.py |
| Turing Bot | Model-Based Agent | turing_captcha_demo.py |

### Search Algorithms (AIMA Chapter 3)

| Algorithm | Queue Used | Complete | Optimal | Space |
|-----------|-----------|----------|---------|-------|
| BFS | FIFO Queue | Yes | Yes (unit cost) | O(b^d) |
| DFS | LIFO Stack | No | No | O(b*m) |
| DLS | LIFO Stack | No | No | O(b*l) |
| IDDFS | Stack (reset) | Yes | Yes | O(b*d) |

### Problems as Search

| Problem | State | Initial | Goal |
|---------|-------|---------|------|
| Water Jug | (litres_A, litres_B) | (0, 0) | (2, any) |
| Missionaries and Cannibals | (M_left, C_left, boat) | (3, 3, L) | (0, 0, R) |
| Eight Queens | Tuple of queen row positions | Empty board | 8 queens no conflict |
| Tic Tac Toe | 9-cell board tuple | All empty | X wins |

---

## What is AQI?

The **Air Quality Index (AQI)** is a standardized indicator that communicates
how polluted the air currently is and the associated health risks. It unifies
multiple pollutant measurements into a single number with a colour-coded category.

> "AQI allows us to see and understand the breadth and depth of air quality
> at a location or city, as a simple coloured symbol."
> — Guttikunda, SIM-air Working Paper #46-2021

---

## How AQI is Computed (CPCB Method)

We implemented the official **CPCB breakpoint interpolation formula**:
```
AQI = ((I_hi - I_lo) / (BP_hi - BP_lo)) × (C - BP_lo) + I_lo
```

Where:
| Symbol | Meaning |
|--------|---------|
| C | Measured concentration of the pollutant |
| BP_lo | Breakpoint concentration just below C |
| BP_hi | Breakpoint concentration just above C |
| I_lo | AQI value corresponding to BP_lo |
| I_hi | AQI value corresponding to BP_hi |

This is applied to each pollutant separately to get a **sub-index**.
The **final AQI = maximum of all sub-indices** (never an average).

---

## Pollutants Monitored

| Pollutant | Unit | Averaging Period |
|-----------|------|-----------------|
| PM2.5 | µg/m³ | 24-hour average |
| PM10 | µg/m³ | 24-hour average |
| SO2 | µg/m³ | 24-hour average |
| NOx | ppb | 24-hour average |
| NH3 | µg/m³ | 24-hour average |
| CO | mg/m³ | 8-hour maximum |
| O3 | µg/m³ | 8-hour maximum |

> PM2.5 and PM10 use 24-hour rolling averages.
> CO and O3 use 8-hour maximum values.
> (Source: CPCB methodology, Reference [2])

---

## AQI Categories (India — CPCB Standard)

| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0–50 | Good | No health risk |
| 51–100 | Satisfactory | Minor discomfort for sensitive groups |
| 101–200 | Moderate | Discomfort for lung/heart patients |
| 201–300 | Poor | Breathing discomfort for most people |
| 301–400 | Very Poor | Respiratory illness on prolonged exposure |
| 401–500 | Severe | Health emergency — stay indoors |

---

## Agent Design — Why Simple Reflex?

Our AQI agent is a **Simple Reflex Agent** (AIMA Chapter 2) because:

- It acts only on the **current percept** (one CSV row at a time)
- It uses **condition-action rules** (AQI value → health advisory)
- It has **no memory** of past readings — each row is independent
- The environment is **fully observable, episodic, static and discrete**
```
Percept (CSV row)
      ↓
Compute sub-index per pollutant using CPCB formula
      ↓
Final AQI = MAX of sub-indices
      ↓
Condition-Action Rule → Health Advisory
      ↓
Output to console (Actuator)
```

### Scalability
The agent is designed for future upgrades as the course progresses:

| Now (Assignment 2) | Future Upgrade |
|--------------------|----------------|
| Simple Reflex Agent | Model-Based Agent with memory |
| CSV file input | Live IoT sensor feed |
| Console output | Web dashboard / alerts |
| India CPCB standard | Multi-country AQI support |


## Domain References

1. Guttikunda, S. (2021). *10 Frequently Asked Questions on Air Quality Index.*
   SIM-air Working Paper Series #46-2021. urbanemissions.info

2. AQI Calculation Tutorial — CPCB official methodology notebook (provided by instructor)
   Formula source: https://app.cpcbccr.com/ccr_docs/How_AQI_Calculated.pdf

> Note: AQI agent uses CPCB breakpoint interpolation formula with 24-hr rolling averages
> for aerosols (PM2.5, PM10) and 8-hr max for gases (CO, O3), as per both references above.


---

*Based on: Russell, S. and Norvig, P. — Artificial Intelligence: A Modern Approach, 4th Edition*

---
