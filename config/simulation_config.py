"""
config/simulation_config.py
===========================
Central configuration for all static simulation parameters and sweep ranges.
Edit this file to change kinetic constants, base operating conditions, or sweep ranges.
"""

import os

# ---------------------------------------------------------------------------
# DWSIM Installation
# ---------------------------------------------------------------------------

# Primary lookup: environment variable DWSIM_PATH (portable, avoids hard-coding).
# Fallback: per-machine default under AppData.
DWSIM_PATH: str = os.environ.get(
    "DWSIM_PATH",
    r"C:\Users\ramya\AppData\Local\DWSIM"
)

THERMOCS_PATH: str = os.path.join(DWSIM_PATH, "ThermoCS")

# ---------------------------------------------------------------------------
# Output Directories
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
OUTPUTS_DIR: str = os.path.join(_HERE, "outputs")
FLOWSHEETS_DIR: str = os.path.join(OUTPUTS_DIR, "flowsheets")
PLOTS_DIR: str = os.path.join(OUTPUTS_DIR, "plots")

# CSV output paths
RESULTS_CSV: str = os.path.join(OUTPUTS_DIR, "results.csv")
PFR_SWEEP_CSV: str = os.path.join(OUTPUTS_DIR, "pfr_sweep_results.csv")
COLUMN_SWEEP_CSV: str = os.path.join(OUTPUTS_DIR, "column_sweep_results.csv")

# Flowsheet save paths
PFR_FLOWSHEET: str = os.path.join(FLOWSHEETS_DIR, "pfr_flowsheet.dwxmz")
DISTILLATION_FLOWSHEET: str = os.path.join(FLOWSHEETS_DIR, "distillation_flowsheet.dwxmz")

# Plot save paths
PFR_PLOT: str = os.path.join(PLOTS_DIR, "pfr_conversion_vs_volume.png")
COLUMN_PLOT: str = os.path.join(PLOTS_DIR, "column_purity_vs_reflux.png")

# ---------------------------------------------------------------------------
# Chemical System
# ---------------------------------------------------------------------------

COMPOUNDS: list[str] = ["n-Pentane", "Isopentane"]
PROPERTY_PACKAGE: str = "Peng-Robinson (PR)"

# ---------------------------------------------------------------------------
# Kinetic Parameters  (n-Pentane → Isopentane, first-order Arrhenius)
# ---------------------------------------------------------------------------

KINETIC_PRE_EXP: float = 1.0e5      # A  [s^-1]
KINETIC_ACTIVATION_ENERGY: float = 50_000.0  # Ea [J/mol]
KINETIC_REACTION_ORDER: float = 1.0

# ---------------------------------------------------------------------------
# Part A – PFR Base Operating Conditions
# ---------------------------------------------------------------------------

PFR_BASE: dict = {
    "v_reactor": 7.5,       # m³
    "t_feed": 393.15,        # K  (120 °C)
    "p_feed": 202_650.0,     # Pa (2 atm)
    "flow_feed": 100.0,      # mol/s  (100% n-pentane)
}

# ---------------------------------------------------------------------------
# Part B – Distillation Column Base Operating Conditions
# ---------------------------------------------------------------------------

COLUMN_BASE: dict = {
    "num_stages": 20,
    "feed_stage": 9,         # 0-indexed  → Stage 10 (1-indexed)
    "reflux_ratio": 2.5,
    "distillate_flow": 50.0,  # mol/s
    "feed_temp": 330.0,       # K
    "feed_press": 202_650.0,  # Pa (2 atm)
}

# Feed composition: 50 % n-pentane / 50 % isopentane
COLUMN_FEED_COMPOSITION: list[float] = [0.5, 0.5]
COLUMN_FEED_FLOW: float = 100.0  # mol/s

# ---------------------------------------------------------------------------
# Part C – Parametric Sweep Ranges
# ---------------------------------------------------------------------------

# PFR sweep: Volume (m³) × Temperature (K)
PFR_SWEEP_VOLUMES: list[float] = [1.0, 2.5, 5.0, 7.5, 10.0]
PFR_SWEEP_TEMPS: list[float] = [350.15, 373.15, 393.15, 413.15]

# Column sweep: Reflux Ratio × Number of Stages
COLUMN_SWEEP_REFLUX: list[float] = [1.5, 2.0, 2.5, 3.5, 5.0]
COLUMN_SWEEP_STAGES: list[int] = [12, 16, 20, 24]
