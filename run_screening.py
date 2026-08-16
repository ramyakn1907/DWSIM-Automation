"""
run_screening.py
================
Main entry point for the DWSIM Automation API Candidate Screening Suite.

Executes:
  Part A – PFR Isomerization Reactor simulation
  Part B – Distillation Column simulation
  Part C – Multi-variable parametric sweeps (PFR & Column)

Outputs written to outputs/:
  outputs/results.csv                           ← unified case log
  outputs/pfr_sweep_results.csv
  outputs/column_sweep_results.csv
  outputs/flowsheets/pfr_flowsheet.dwxmz
  outputs/flowsheets/distillation_flowsheet.dwxmz
  outputs/plots/pfr_conversion_vs_volume.png
  outputs/plots/column_purity_vs_reflux.png

Usage:
  python run_screening.py
"""

import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config.simulation_config import OUTPUTS_DIR, FLOWSHEETS_DIR, PLOTS_DIR
from src.pfr import run_pfr
from src.distillation import run_distillation
from src.sweeps import sweep_pfr, sweep_column
from src.results import ResultsLogger
from src.plotting import Plotter

import os
# Ensure all output directories exist before any simulation runs
for _d in [OUTPUTS_DIR, FLOWSHEETS_DIR, PLOTS_DIR]:
    os.makedirs(_d, exist_ok=True)


def main() -> None:
    t0 = time.time()

    #  Part A: PFR Baseline Simulation 
    print("\n" + "─" * 60)
    print("  PART A: PFR Isomerization Reactor Simulation")
    print("─" * 60)
    res_a = run_pfr(save_flowsheet=True)
    _print_pfr_result(res_a)

    # Part B: Distillation Column Baseline Simulation 
    print("\n" + "─" * 60)
    print("  PART B: Distillation Column Simulation")
    print("─" * 60)
    res_b = run_distillation(save_flowsheet=True)
    _print_col_result(res_b)

    # Part C: Parametric Sweeps 
    print("\n" + "─" * 60)
    print("  PART C: Parametric Sweeps")
    print("─" * 60)
    pfr_df = sweep_pfr()
    col_df = sweep_column()

    # Plots 
    Plotter.plot_sweeps(pfr_df, col_df)

    # Unified results.csv 
    ResultsLogger.generate(res_a, res_b, pfr_df, col_df)

    elapsed = time.time() - t0
    print("\n" + "=" * 70)
    print(f"  ALL TASKS COMPLETED IN {elapsed:.2f}s")
    print("\n  Output files:")
    print("    outputs/results.csv")
    print("    outputs/pfr_sweep_results.csv")
    print("    outputs/column_sweep_results.csv")
    print("    outputs/flowsheets/pfr_flowsheet.dwxmz")
    print("    outputs/flowsheets/distillation_flowsheet.dwxmz")
    print("    outputs/plots/pfr_conversion_vs_volume.png")
    print("    outputs/plots/column_purity_vs_reflux.png")
    print("=" * 70)


def _print_pfr_result(res: dict) -> None:
    from tabulate import tabulate
    table = [
        ["Reactor Volume (m³)",               f"{res.get('PFR_Volume_m3', 'N/A'):.2f}"],
        ["Feed Temperature (K)",              f"{res.get('PFR_Temperature_K', 'N/A'):.2f}"],
        ["Outlet Temperature (K)",            f"{res.get('PFR_Outlet_Temp_K', 'N/A'):.4f}"],
        ["n-Pentane Conversion (%)",          f"{res.get('PFR_Conversion_pct', 'N/A'):.4f}"],
        ["Outlet n-Pentane Flow (mol/s)",     f"{res.get('PFR_NPentane_Outlet_mols', 'N/A'):.6f}"],
        ["Outlet Isopentane Flow (mol/s)",    f"{res.get('PFR_Isopentane_Outlet_mols', 'N/A'):.6f}"],
        ["Heat Duty (kW)",                    f"{res.get('PFR_Heat_Duty_kW', 'N/A'):.4f}"],
        ["Status",                            "SUCCESS" if res.get("Success") else f"FAILED: {res.get('Error_Message')}"],
    ]
    print(tabulate(table, headers=["Parameter", "Value"], tablefmt="grid"))


def _print_col_result(res: dict) -> None:
    from tabulate import tabulate
    table = [
        ["Stages",                            res.get("Column_Stages", "N/A")],
        ["Feed Stage",                        res.get("Column_Feed_Stage", "N/A")],
        ["Reflux Ratio",                      f"{res.get('Column_Reflux_Ratio', 'N/A'):.2f}"],
        ["Distillate Flow (mol/s)",           f"{res.get('Column_Distillate_Flow_mols', 'N/A'):.2f}"],
        ["Distillate Isopentane Purity (%)",  f"{res.get('Column_Distillate_Purity_pct', 'N/A'):.4f}"],
        ["Bottoms n-Pentane Purity (%)",      f"{res.get('Column_Bottoms_Purity_pct', 'N/A'):.4f}"],
        ["Condenser Duty (kW)",               f"{res.get('Column_Condenser_Duty_kW', 'N/A'):.2f}"],
        ["Reboiler Duty (kW)",                f"{res.get('Column_Reboiler_Duty_kW', 'N/A'):.2f}"],
        ["Status",                            "SUCCESS" if res.get("Success") else f"FAILED: {res.get('Error_Message')}"],
    ]
    print(tabulate(table, headers=["Parameter", "Value"], tablefmt="grid"))


if __name__ == "__main__":
    main()
