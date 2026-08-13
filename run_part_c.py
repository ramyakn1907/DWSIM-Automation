"""
run_part_c.py
=============
Thin wrapper – executes Part C (Parametric Sweeps + Plotting) standalone.
Sweep logic lives in src/sweeps.py; plotting in src/plotting.py.

Usage:
    python run_part_c.py
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from tabulate import tabulate
from src.sweeps import sweep_pfr, sweep_column
from src.plotting import Plotter


def run_part_c():
    print("=" * 60)
    print("      PART C: PARAMETRIC SWEEPS (PFR & DISTILLATION)")
    print("=" * 60)

    # PFR sweep
    pfr_df = sweep_pfr()

    # Column sweep
    col_df = sweep_column()

    # Plots
    Plotter.plot_sweeps(pfr_df, col_df)

    # Sample table summaries
    print("\n--- PFR Sweep Sample (T = 373.15 K) ---")
    pfr_sub = pfr_df[pfr_df["PFR_Temperature_K"] == 373.15][
        ["PFR_Volume_m3", "PFR_Temperature_K", "PFR_Conversion_pct", "PFR_Heat_Duty_kW"]
    ]
    print(tabulate(pfr_sub, headers="keys", tablefmt="grid", showindex=False))

    print("\n--- Column Sweep Sample (Stages = 20) ---")
    col_sub = col_df[col_df["Column_Stages"] == 20][
        ["Column_Stages", "Column_Reflux_Ratio", "Column_Distillate_Purity_pct",
         "Column_Condenser_Duty_kW", "Column_Reboiler_Duty_kW"]
    ]
    print(tabulate(col_sub, headers="keys", tablefmt="grid", showindex=False))

    return pfr_df, col_df


if __name__ == "__main__":
    run_part_c()
