# AI Assignment 2

**Subject:** Artificial Intelligence
**Reference:** Russell & Norvig — Artificial Intelligence: A Modern Approach (AIMA)

---

## Table of Contents

1. [Turing Test & CAPTCHA](#1-turing-test--captcha)
2. [AQI Simple Reflex Agent](#2-aqi-reflex-agent)
3. [Search Algorithms](#3-search-algorithms)
4. [Performance Results](#performance-comparison-results)
5. [How to Run](#how-to-run)
6. [Domain References](#domain-references)

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
│   ├── captcha_demo.py
│   ├── captcha_image.py
│   ├── captcha_sample.png
│   └── turing_captcha_demo.py
│
├── AQI_Agent/
│   ├── aqi_agent.py
│   ├── sensor_data.csv
│   └── agent/
│       ├── __init__.py
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

## 1. Turing Test & CAPTCHA

### What is the Turing Test?
Proposed by Alan Turing in 1950, the Turing Test determines whether a machine
can exhibit intelligence equivalent to a human.

- A human judge communicates with both a human and a machine
- The judge does not know which is the machine
- If the judge cannot reliably distinguish them, the machine passes the test

### What is CAPTCHA?
**CAPTCHA** — Completely Automated Public Turing test to tell Computers and
Humans Apart.

It is a security mechanism that prevents automated bots from performing actions
like creating fake accounts, spamming forms, or brute-force login attempts.

> Key difference: Turing Test checks if a machine can imitate a human.
> CAPTCHA checks if a user is human rather than a bot.

### Architecture
```
Turing Test:
Human Interrogator
      ↓ (text questions)
Communication Interface
      ↙              ↘
AI Agent          Human Participant
      ↘              ↙
      Judge's Decision
          ↓
Human / Machine verdict

CAPTCHA:
Challenge Generator (random distorted text)
      ↓
User Interface (display CAPTCHA)
      ↓
User Response + Timing Analysis
      ↓
Response Validator
      ↓
Allow / Deny Access
```

### Implementation
Our implementation includes:
- Random CAPTCHA generation (letters + digits)
- Character distortion using noise symbols
- Bot detection via response timing (bots respond in milliseconds)
- CAPTCHA regeneration after each attempt
- Turing Test simulation — judge tries to identify human vs AI

**Files:**
- `Turing_Captcha/captcha_generator.py` — CAPTCHA engine
- `Turing_Captcha/captcha_demo.py` — full Turing Test + CAPTCHA demo
- `Turing_Captcha/architecture_design.md` — detailed architecture

---

## What is AQI?

The **Air Quality Index (AQI)** is a standardized indicator that communicates
how polluted the air currently is and the associated health risks. It unifies
multiple pollutant measurements into a single number with a colour-coded category.

> "AQI allows us to see and understand the breadth and depth of air quality
> at a location or city, as a simple coloured symbol."
> — Guttikunda, SIM-air Working Paper #46-2021

---

### PEAS Description

| Component | Description |
|-----------|-------------|
| **Performance** | Correct AQI category and advisory per reading |
| **Environment** | City air — PM2.5, PM10, SO2, NOx, NH3, CO, O3 |
| **Actuators** | Console output (AQI value, category, advisory) |
| **Sensors** | CSV file rows — one row = one hourly percept |

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

| Module | Purpose | Future Upgrade |
|--------|---------|----------------|
| `agent/subindex.py` | Sub-index functions | Add new pollutants here only |
| `agent/environment.py` | Sensor data loading | Add rolling window averaging |
| `agent/agent_core.py` | Agent function + rules | Upgrade to Model-Based agent |
| `aqi_agent.py` | Entry point | No changes needed |

**Files:**
- `AQI_Agent/aqi_agent.py` — main agent entry point
- `AQI_Agent/agent/` — modular components
- `AQI_Agent/sensor_data.csv` — sensor input data## 	Concepts Covered

### Agent Types

| Agent | Type | File |
|-------|------|------|
| AQI Monitor | Simple Reflex Agent | aqi_agent.py |
| CAPTCHA | Simple Reflex Agent | turing_captcha_demo.py |
| Turing Bot | Model-Based Agent | turing_captcha_demo.py |

---

### Search Algorithms

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

### Problems Implemented

---

#### Water Jug Problem
Move water between a 4L and 3L jug to get exactly 2L in jug A.

**State Representation:** `(a, b)` — litres in jug A and jug B

| | Value |
|--|-------|
| Initial State | `(0, 0)` |
| Goal State | `(2, _)` |
| Actions | Fill A, Fill B, Empty A, Empty B, Pour A→B, Pour B→A |

---

#### Missionaries and Cannibals
Move 3 missionaries and 3 cannibals across a river safely.

**State Representation:** `(M, C, B)` where M = missionaries on left,
C = cannibals on left, B = boat position (0=left, 1=right)

| | Value |
|--|-------|
| Initial State | `(3, 3, 0)` |
| Goal State | `(0, 0, 1)` |
| Constraint | Cannibals must never outnumber missionaries on either bank |

---

#### Eight Queens
Place 8 queens on a chessboard so none attack each other.

**State Representation:** Tuple where `state[col]` = row of queen in that column

| | Value |
|--|-------|
| Initial State | Empty board `()` |
| Goal State | 8 queens placed, none attacking |
| Valid Solutions | 92 |

---

#### Tic Tac Toe
Find a winning sequence for X on a 3×3 board.

**State Representation:** Tuple of 9 cells, each X / O / empty

| | Value |
|--|-------|
| Initial State | All cells empty |
| Goal State | 3 X's in a row/column/diagonal |

## Performance Comparison Results

| Problem | BFS Nodes | DFS Nodes | IDDFS Nodes | BFS Time | DFS Time | IDDFS Time |
|---------|-----------|-----------|-------------|----------|----------|------------|
| Water Jug | 11 | 7 | 92 | 0.109ms | 0.059ms | 0.192ms |
| Missionaries & Cannibals | 13 | 12 | 184 | 0.178ms | 0.114ms | 0.993ms |
| 6-Queens | 114 | 32 | 388 | 1.480ms | 0.237ms | 2.167ms |
| Tic Tac Toe | 56 | 6 | — | 0.666ms | 0.090ms | — |

**Key Observations:**
- BFS always finds shortest path but expands more nodes
- DFS is faster and uses less memory but not always optimal
- IDDFS is complete + optimal like BFS but memory efficient like DFS
- DLS (Depth-Limited Search) is the building block inside IDDFS

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

### Image CAPTCHA Generator
```bash
cd Turing_Captcha
python3 captcha_image.py
```

### Search Algorithms Performance Comparison
```bash
cd Search_Algorithms
python3 performance_comparison.py
python3 problems/missionaries_cannibals.py
python3 problems/water_jug.py
python3 problems/eight_queens.py
python3 problems/tic_tac_toe.py
```

### Individual Algorithm Demos
```bash
cd Search_Algorithms
python3 bfs.py
python3 dfs.py
python3 dls.py
```

---

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
