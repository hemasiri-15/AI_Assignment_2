# AI Assignment 2

**Subject:** Artificial Intelligence
**Reference:** Russell & Norvig — Artificial Intelligence: A Modern Approach (AIMA)

---

## Folder Structure

```
AI_Assignment_2/
│
├── README.md
│
├── Turing_Captcha/
│   ├── architecture_design.md
│   └── turing_captcha_demo.py
│
├── AQI_Agent/
│   ├── aqi_agent.py
│   └── sensor_data.csv
│
└── Search_Algorithms/
    ├── bfs.py
    ├── dfs.py
    ├── performance_comparison.py
    └── problems/
        ├── missionaries_cannibals.py
        ├── water_jug.py
        ├── eight_queens.py
        └── tic_tac_toe.py
```

---

## How to Run

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

---

## Concepts Covered

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

*Based on: Russell, S. and Norvig, P. — Artificial Intelligence: A Modern Approach, 4th Edition*

---

## Domain References

1. Guttikunda, S. (2021). *10 Frequently Asked Questions on Air Quality Index.*
   SIM-air Working Paper Series #46-2021. urbanemissions.info

2. AQI Calculation Tutorial — CPCB official methodology notebook (provided by instructor)
   Formula source: https://app.cpcbccr.com/ccr_docs/How_AQI_Calculated.pdf

> Note: AQI agent uses CPCB breakpoint interpolation formula with 24-hr rolling averages
> for aerosols (PM2.5, PM10) and 8-hr max for gases (CO, O3), as per both references above.
