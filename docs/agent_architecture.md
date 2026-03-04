# Agent Architecture — AQI Monitoring Agent

## Agent Type: Simple Reflex Agent (AIMA Chapter 2)

A Simple Reflex Agent acts only on the **current percept** using
condition-action rules. It has no memory of past percepts.

## PEAS Description

| Component | Description |
|-----------|-------------|
| **Performance** | Correct AQI category and advisory for each sensor reading |
| **Environment** | City air — pollutants PM2.5, PM10, SO2, NOx, NH3, CO, O3 |
| **Actuators** | Console output (AQI value, category, health advisory) |
| **Sensors** | CSV file rows — one row = one hourly percept |

## Agent Loop
```
Sensor Data (CSV)
      ↓
Percept (one row of pollutant readings)
      ↓
Agent Function: compute sub-index per pollutant
      ↓
AQI = MAX of all sub-indices  (CPCB rule)
      ↓
Condition-Action Rule: AQI value → category
      ↓
Actuator: print advisory to console
      ↓
Next row (next percept) — no memory carried over
```

## Scalability Design

The agent is split into modules for future upgrades:

| Module | Purpose | Future Upgrade |
|--------|---------|----------------|
| agent/subindex.py | Pollutant sub-index functions | Add new pollutants here |
| agent/environment.py | Sensor data loading | Add rolling window averaging |
| agent/agent_core.py | Agent function + rules | Upgrade to Model-Based agent |
| aqi_agent.py | Entry point | No changes needed |

## Why Simple Reflex?
- No internal state — each CSV row processed independently
- No memory of past readings
- Pure condition → action mapping
- Episodic: advisory for 08:00 doesn't depend on 07:00
