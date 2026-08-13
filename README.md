# DWSIM Python Automation API – Candidate Screening Suite

A Python-based, headless chemical process simulation framework developed using the **DWSIM Automation API** and **pythonnet**.

This project demonstrates the programmatic construction and automation of DWSIM simulations for:

- **Part A:** Plug Flow Reactor (PFR) simulation
- **Part B:** Distillation Column simulation
- **Part C:** Multi-variable parametric sweep studies

The complete workflow is executed from Python without requiring manual interaction with the DWSIM graphical user interface.

All simulation flowsheets are created programmatically at runtime. No prebuilt DWSIM flowsheet is loaded as an input.

---

## Table of Contents

- [Overview](#overview)
- [Screening Task Coverage](#screening-task-coverage)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Environment Requirements](#environment-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Execution](#execution)
- [Part A – PFR Simulation](#part-a--pfr-simulation)
- [Part B – Distillation Column Simulation](#part-b--distillation-column-simulation)
- [Part C – Parametric Sweeps](#part-c--parametric-sweeps)
- [Static and Dynamic Data](#static-and-dynamic-data)
- [Result Logging](#result-logging)
- [Failure Handling](#failure-handling)
- [Generated Outputs](#generated-outputs)
- [Visualization](#visualization)
- [Headless Execution](#headless-execution)
- [No Prebuilt Flowsheet Design](#no-prebuilt-flowsheet-design)
- [Interactive AI Enhancement](#interactive-ai-enhancement)
- [Validation Checklist](#validation-checklist)
- [Reproducibility](#reproducibility)
- [Design Principles](#design-principles)
- [Conclusion](#conclusion)

---

# Overview

The objective of this project is to automate chemical process simulations using Python and the DWSIM Automation API.

The implementation creates the required DWSIM process models programmatically, executes the simulations, extracts the required KPIs, performs parametric studies, records every simulation case, and generates analysis plots.

The workflow consists of three parts.

### Part A – Plug Flow Reactor
Simulates the isomerization reaction:
$$\text{n-Pentane} \xrightarrow{k} \text{Isopentane}$$
using a kinetic reaction in a Plug Flow Reactor.

### Part B – Distillation Column
Simulates the binary separation of:
$$\text{n-Pentane} \ / \ \text{Isopentane}$$
using a DWSIM distillation column.

### Part C – Parametric Sweeps
Performs multi-variable studies for:
- **PFR:** Reactor Volume $\times$ Feed Temperature
- **Distillation:** Number of Stages $\times$ Reflux Ratio

Each parameter combination is executed as an independent simulation case and logged to CSV.

---

## Screening Task Coverage

The implementation maps the screening requirements to the following components:

| Requirement | Implementation |
| :--- | :--- |
| **Python automation** | Python-based execution framework |
| **DWSIM Automation API** | `pythonnet` with DWSIM .NET API |
| **Programmatic flowsheet construction** | Flowsheets created using `CreateFlowsheet()` |
| **PFR simulation** | Kinetic n-Pentane → Isopentane PFR |
| **Isothermal PFR operation** | PFR configured for isothermal operation |
| **Volume-based PFR sizing** | Reactor volume supplied programmatically |
| **PFR KPIs** | Conversion, outlet flows, temperature, heat duty |
| **Distillation simulation** | Binary n-Pentane / Isopentane separation |
| **Column configuration** | Stages, feed stage, reflux ratio and distillate specification |
| **Column KPIs** | Distillate purity, bottoms purity, condenser and reboiler duties |
| **PFR parametric sweep** | Reactor volume × feed temperature |
| **Column parametric sweep** | Number of stages × reflux ratio |
| **Case logging** | Unique Case ID and timestamp |
| **Success tracking** | `Success` field |
| **Failure tracking** | `Error_Message` field |
| **Unified results** | `outputs/results.csv` |
| **Sweep-specific results** | PFR and column sweep CSV files |
| **Visualization** | Automated Matplotlib plots |
| **Headless execution** | Python/DWSIM Automation API workflow |
| **No prebuilt flowsheets** | All simulation flowsheets created at runtime |

---

## Key Features

- Programmatic DWSIM flowsheet creation
- DWSIM Automation API integration
- Python/.NET interoperability using `pythonnet`
- Kinetic PFR simulation
- Isothermal PFR operation
- Binary distillation simulation
- Multi-variable parametric sweeps
- Independent simulation case execution
- Case-level success/failure tracking
- Timestamped result logging
- Unified CSV result generation
- PFR-specific sweep logging
- Distillation-specific sweep logging
- Automated trend plot generation
- Optional DWSIM flowsheet export
- Centralized simulation configuration
- Modular source code structure
- Headless execution
- Optional interactive AI simulation workflow

---

# Architecture

The overall execution architecture is:

```text
                    ┌──────────────────────┐
                    │        Python        │
                    │   run_screening.py   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ DWSIM Automation API │
                    │      pythonnet       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Create Empty         │
                    │ DWSIM Flowsheet      │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
              Part A        Part B        Part C
                PFR       Distillation     Sweeps
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   DWSIM Calculation  │
                    │        Engine        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Result Extraction  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Case Logger       │
                    │ Timestamp + KPIs     │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
             results.csv   Sweep CSVs      Plots
```

---

# Project Structure

The committed repository contains the source code, configuration, documentation, and tests:

```text
DWSIM/
│
├── config/
│   ├── __init__.py
│   └── simulation_config.py
│
├── src/
│   ├── __init__.py
│   ├── dwsim_automation.py
│   ├── pfr.py
│   ├── distillation.py
│   ├── sweeps.py
│   ├── results.py
│   └── plotting.py
│
├── tests/
│   └── test_configuration.py
│
├── run_screening.py
├── run_part_a.py
├── run_part_b.py
├── run_part_c.py
│
├── requirements.txt
├── README.md
├── PROMPT.prompt.md
└── .gitignore
```

### Runtime-Generated Outputs
The following directory is generated when the application is executed:

```text
outputs/
│
├── results.csv
├── pfr_sweep_results.csv
├── column_sweep_results.csv
│
├── flowsheets/
│   ├── pfr_flowsheet.dwxmz
│   └── distillation_flowsheet.dwxmz
│
└── plots/
    ├── pfr_conversion_vs_volume.png
    └── column_purity_vs_reflux.png
```

*Note: The `outputs/` directory is intentionally excluded from version control via `.gitignore` because these files are dynamically generated during execution.*

---

# Module Responsibilities

### `run_screening.py`
Main entry point for the complete screening workflow. It coordinates:
- Part A – PFR baseline
- Part B – Distillation baseline
- Part C – PFR sweep
- Part C – Distillation sweep
- Result aggregation and unified output generation
- Plot generation

### `run_part_a.py`
Thin standalone wrapper for executing the PFR baseline simulation directly.
```bash
python run_part_a.py
```

### `run_part_b.py`
Thin standalone wrapper for executing the distillation baseline simulation directly.
```bash
python run_part_b.py
```

### `run_part_c.py`
Thin standalone wrapper for executing the parametric sweep studies directly.
```bash
python run_part_c.py
```

### `src/dwsim_automation.py`
Responsible for initializing the DWSIM Automation environment and providing the required DWSIM API access through pythonnet.

### `src/pfr.py`
Implements Part A. Responsibilities include:
- Creating an empty DWSIM flowsheet
- Adding chemical compounds
- Adding the property package
- Creating material streams and energy streams
- Creating the kinetic reaction and reaction set
- Creating the PFR and connecting flowsheet objects
- Running calculations and extracting PFR KPIs

### `src/distillation.py`
Implements Part B. Responsibilities include:
- Creating an empty DWSIM flowsheet
- Adding chemical compounds
- Adding the property package
- Creating feed, product, and condenser/reboiler energy streams
- Creating the distillation column
- Configuring stages, feed stage, reflux ratio, and distillate specifications
- Running calculations and extracting column KPIs

### `src/sweeps.py`
Implements Part C. Responsible for:
- Generating parameter combinations for reactor and column studies
- Executing PFR and distillation simulation runs
- Logging run outcomes and returning sweep results

### `src/results.py`
Responsible for result management. Responsibilities include:
- Generating Case IDs and recording run timestamps
- Normalizing result dictionaries
- Combining all cases into a single DataFrame and writing the unified CSV

### `src/plotting.py`
Responsible for creating parametric sweep plots using Matplotlib.

### `config/simulation_config.py`
Central configuration location for:
- Chemical compounds and property packages
- Reaction kinetic parameters
- Baseline process values and dynamic sweep ranges
- DWSIM paths and output file locations

---

## Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.12+** | Automation and simulation orchestration |
| **DWSIM** | Chemical process simulation |
| **DWSIM Automation API** | Programmatic DWSIM control |
| **pythonnet** | Python/.NET interoperability |
| **Pandas** | Result processing and CSV handling |
| **Matplotlib** | Parametric plots |
| **Tabulate** | Console result formatting |

---

## Environment Requirements

- **Operating System:** Windows (64-bit)
- **Python Version:** 3.12+ 64-bit
- **DWSIM:** Must be installed on the machine with exposed .NET Assemblies.

---

## Installation

### 1. Verify Python Version
```bash
python --version
```

### 2. Install DWSIM
Install DWSIM on the Windows machine. Ensure the installation path contains DWSIM DLL assemblies.

### 3. Clone and Setup Environment
```bash
git clone <repository-url>
cd DWSIM
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

All primary simulation configuration is maintained in:
`config/simulation_config.py`

### DWSIM Path Configuration
The DWSIM installation path should be configured in `config/simulation_config.py` to match the local machine installation (e.g. `C:\Users\<username>\AppData\Local\DWSIM`). Alternatively, configure the path using the environment variable:
```text
DWSIM_PATH=<DWSIM installation directory>
```

---

## Execution

### Complete Screening Workflow
To execute the complete screening workflow, run:
```bash
python run_screening.py
```

### Individual Part Execution
- **Part A (PFR):** `python run_part_a.py`
- **Part B (Column):** `python run_part_b.py`
- **Part C (Sweeps):** `python run_part_c.py`

---

# Part A – PFR Simulation

### Objective
Part A simulates the isomerization reaction:
$$\text{n-Pentane} \rightarrow \text{Isopentane}$$
using a kinetic reaction in a Plug Flow Reactor. The PFR flowsheet is constructed entirely at runtime.

### Reaction Model
The reaction uses a first-order kinetic expression:
$$r = k C_{n\text{-Pentane}}$$
where the reaction rate is temperature-dependent through the Arrhenius equation:
$$k = A \exp\left(-\frac{E_a}{RT}\right)$$

### PFR Operation
The reactor is configured for:
- Isothermal operation
- Vapor-phase reaction
- Volume-based sizing

### PFR Inputs
| Parameter | Unit | Description |
| :--- | :---: | :--- |
| **Reactor Volume** | $m^3$ | PFR reactor volume |
| **Feed Temperature** | $K$ | Feed and isothermal reactor temperature |
| **Feed Pressure** | $Pa$ | Feed pressure |
| **Feed Molar Flow** | $mol/s$ | Feed molar flow rate (100% n-pentane) |

### PFR Outputs
- Outlet temperature ($K$ and $^\circ C$)
- n-Pentane conversion (%)
- Outlet n-Pentane flow ($mol/s$)
- Outlet Isopentane flow ($mol/s$)
- Heat duty ($kW$)

---

# Part B – Distillation Column Simulation

### Objective
Part B simulates the binary separation of n-Pentane and Isopentane using a rigorous distillation column.

### Feed Conditions
- **Flow rate:** 100 mol/s
- **Composition:** Equimolar (50% n-pentane, 50% isopentane)
- **Temperature/Pressure:** 330 K, 2 atm

### Column Configuration
The column is configured using two specs:
- **Reflux Ratio** (Spec 1)
- **Distillate Flow Rate** (Spec 2)

Default baseline parameters:
- **Stages:** 20
- **Feed Stage:** 10 (middle)
- **Reflux Ratio:** 2.5
- **Distillate Flow:** 50 mol/s

### Column Outputs
- Distillate Isopentane purity (%)
- Bottoms n-Pentane purity (%)
- Condenser duty ($kW$)
- Reboiler duty ($kW$)

---

# Part C – Parametric Sweeps

Evaluates the process KPIs across a wide range of operating parameters. Every case is treated as an independent simulation run.

### PFR Parametric Sweep
- **Reactor Volume ($m^3$):** 1.0, 2.5, 5.0, 7.5, 10.0
- **Feed Temperature ($K$):** 350.15, 373.15, 393.15, 413.15
- **Total Cases:** 20 cases

### Distillation Parametric Sweep
- **Number of Stages:** 12, 16, 20, 24
- **Reflux Ratio:** 1.5, 2.0, 2.5, 3.5, 5.0
- **Total Cases:** 20 cases

### Complete Suite Case Count
- PFR Baseline: 1 case
- Distillation Baseline: 1 case
- Sweeps: 40 cases
- **Total Simulation Cases:** 42 cases

---

# Static and Dynamic Data

The project separates model configuration from variables that change between simulation cases.

### Static Data
Static data defines the process model and remains unchanged:
- Chemical compounds and property packages
- Reaction stoichiometry and kinetics
- Feed composition
- Baseline process operating mode

### Dynamic Data
Dynamic data represents values changed between simulation cases:
- **PFR:** Reactor Volume, Feed Temperature
- **Distillation:** Number of Stages, Reflux Ratio

### Calculated Data
Calculated data is produced by DWSIM:
- **PFR:** Conversion, outlet flows, heat duty
- **Distillation:** Product purities, condenser/reboiler duties

---

# Result Logging

All results are logged to `outputs/results.csv`. Each row contains metadata, input parameters, calculated KPIs, and convergence indicators.

### Timestamped Case Logging
Each simulation case receives a timestamp for execution traceability:
```csv
Timestamp,Case_ID,Case_Name,Simulation_Type,Success
2026-08-12 13:12:10,CASE-001,Part_A_PFR_Baseline,PFR,True
```

### Case Identification
Every simulation case has a unique Case ID (e.g., `CASE-001` to `CASE-042`) and descriptive Case Name (e.g., `Part_C_Col_N20_RR2.5`).

### Schema Fields
1. **Case Metadata:** `Timestamp`, `Case_ID`, `Case_Name`, `Simulation_Type`, `Success`, `Error_Message`
2. **PFR Variables & KPIs:** `PFR_Volume_m3`, `PFR_Temperature_K`, `PFR_Outlet_Temp_K`, `PFR_Outlet_Temp_C`, `PFR_Conversion_pct`, `PFR_NPentane_Outlet_mols`, `PFR_Isopentane_Outlet_mols`, `PFR_Heat_Duty_kW`
3. **Column Variables & KPIs:** `Column_Stages`, `Column_Feed_Stage`, `Column_Reflux_Ratio`, `Column_Distillate_Purity_pct`, `Column_Bottoms_Purity_pct`, `Column_Condenser_Duty_kW`, `Column_Reboiler_Duty_kW`

---

# Failure Handling

Each simulation case runs independently inside exception handling blocks.
- **Successful Run:** `Success = True`, `Error_Message = ""`
- **Failed Run:** `Success = False`, `Error_Message = <captured exception>`

This structure prevents a single failed case from crashing the entire sweep. All errors are documented directly in the output CSV.

---

# Generated Outputs

A complete execution of `run_screening.py` generates the following files:

- **CSV Results:**
  - `outputs/results.csv` – Unified case results
  - `outputs/pfr_sweep_results.csv` – PFR-specific sweep
  - `outputs/column_sweep_results.csv` – Column-specific sweep
- **Plots:**
  - `outputs/plots/pfr_conversion_vs_volume.png` – PFR sweep plot
  - `outputs/plots/column_purity_vs_reflux.png` – Column sweep plot
- **Flowsheets:**
  - `outputs/flowsheets/pfr_flowsheet.dwxmz` – Saved PFR flowsheet
  - `outputs/flowsheets/distillation_flowsheet.dwxmz` – Saved column flowsheet

---

# Visualization

Parametric plots are automatically updated post-execution:
- **PFR Plot:** Conversion (%) vs. Reactor Volume ($m^3$) grouped by feed temperatures.
- **Distillation Plot:** Distillate Isopentane Purity (%) vs. Reflux Ratio grouped by stage counts.

---

# Headless Execution

The workflow does not use GUI automation or opening of flowsheets. It integrates via the DWSIM .NET assemblies using `pythonnet` to directly call:
```text
Python → pythonnet → DWSIM Automation API → Calculation Engine
```

---

# No Prebuilt Flowsheet Design

All flowsheets are built programmatically from an empty flowsheet at runtime:
```python
sim = auto.CreateFlowsheet()
```
Chemical compounds, thermodynamic equations of state, material/energy streams, reaction sets, and unit operations are connected and calculated on-the-fly.

---

# Interactive AI Enhancement

An optional interactive AI prompt is included in `PROMPT.prompt.md`. When imported to an AI agent, it configures a wizard that guides the user through simulation selection, parameter customization, data validation, execution, and engineering explanation.

---

## Validation Checklist

Before submission, verify the following:

### Environment
- [x] Python 3.12+ 64-bit installed
- [x] DWSIM installed
- [x] Required Python packages installed
- [x] DWSIM path configured correctly

### Part A – PFR
- [x] n-Pentane added programmatically
- [x] Isopentane added programmatically
- [x] Property package added programmatically
- [x] Kinetic reaction created programmatically
- [x] Reaction set created programmatically
- [x] PFR created programmatically
- [x] Reactor configured for isothermal operation
- [x] Reactor volume configured programmatically
- [x] Conversion calculated
- [x] Outlet flows calculated
- [x] Outlet temperature calculated
- [x] Heat duty extracted

### Part B – Distillation
- [x] Binary feed created programmatically
- [x] Distillation column created programmatically
- [x] Number of stages configurable
- [x] Feed stage configurable
- [x] Reflux ratio configurable
- [x] Distillate flow specification configured
- [x] Distillate purity calculated
- [x] Bottoms purity calculated
- [x] Condenser duty extracted
- [x] Reboiler duty extracted

### Part C – Parametric Sweep
- [x] PFR volume varied
- [x] PFR temperature varied
- [x] Column stages varied
- [x] Column reflux ratio varied
- [x] Every parameter combination executed
- [x] Every case logged

### Logging
- [x] Case ID generated
- [x] Timestamp recorded
- [x] Case name recorded
- [x] Simulation type recorded
- [x] Success status recorded
- [x] Error message recorded when required
- [x] Required KPIs recorded
- [x] Unified CSV generated

### Outputs
- [x] PFR sweep CSV generated
- [x] Column sweep CSV generated
- [x] Unified results CSV generated
- [x] PFR plot generated
- [x] Column plot generated
- [x] Optional flowsheets generated

### Automation
- [x] No prebuilt flowsheet used as an input
- [x] Flowsheets created at runtime
- [x] No manual DWSIM GUI workflow required
- [x] Complete screening executable from Python

---

# Design Principles

1. **Separation of Concerns:** Configuration (`config/`), automation logic (`src/`), and scripts (`run_*.py`) are strictly modular.
2. **Programmatic Construction:** Builds models dynamically from source instead of loading template files.
3. **Headless Automation:** Executes simulations through the DWSIM Automation API without requiring manual GUI interaction.
4. **Traceability:** Unique Case IDs and timestamps identify every run.
5. **Fault Tolerance:** Catches and logs individual failures without stopping sweeps.
6. **Extensibility:** Easily scale to add more unit operations or sweep variables.

---

# Conclusion

This project demonstrates a robust, modular, and reproducible automated
process simulation suite. By combining Python, the DWSIM Automation API,
and chemical engineering thermodynamics, the suite provides a structured
workflow for headless simulation, parametric analysis, result logging,
and visualization suitable for candidate screening and engineering design studies.