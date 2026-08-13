"""
run_part_b.py
=============
Thin wrapper – executes Part B (Distillation Column simulation) standalone.
Simulation logic lives in src/distillation.py.

Usage:
    python run_part_b.py
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from tabulate import tabulate
from src.distillation import run_distillation
from config.simulation_config import COLUMN_BASE


def run_part_b(save_flowsheet: bool = True) -> dict:
    print("=" * 60)
    print("      PART B: DISTILLATION COLUMN SIMULATION")
    print("=" * 60)
    print(f"  Number of Stages : {COLUMN_BASE['num_stages']}")
    print(f"  Feed Stage       : Stage {COLUMN_BASE['feed_stage'] + 1}  (1-indexed)")
    print(f"  Reflux Ratio     : {COLUMN_BASE['reflux_ratio']:.2f}")
    print(f"  Distillate Flow  : {COLUMN_BASE['distillate_flow']:.2f} mol/s")
    print("  Running DWSIM headless simulation...")

    res = run_distillation(save_flowsheet=save_flowsheet)

    table = [
        ["Total Stages",                       res.get("Column_Stages", "N/A")],
        ["Feed Stage",                         f"Stage {res.get('Column_Feed_Stage', 'N/A')}"],
        ["Reflux Ratio",                       f"{res.get('Column_Reflux_Ratio', 'N/A'):.2f}"],
        ["Distillate Flow (mol/s)",            f"{res.get('Column_Distillate_Flow_mols', 'N/A'):.2f}"],
        ["Distillate Isopentane Purity (%)",   f"{res.get('Column_Distillate_Purity_pct', 'N/A'):.4f}"],
        ["Distillate n-Pentane Fraction",      f"{res.get('Column_Distillate_nPentane_Frac', 'N/A'):.6f}"],
        ["Bottoms n-Pentane Purity (%)",       f"{res.get('Column_Bottoms_Purity_pct', 'N/A'):.4f}"],
        ["Bottoms Isopentane Fraction",        f"{res.get('Column_Bottoms_Isopentane_Frac', 'N/A'):.6f}"],
        ["Condenser Duty (kW)",                f"{res.get('Column_Condenser_Duty_kW', 'N/A'):.2f}"],
        ["Reboiler Duty (kW)",                 f"{res.get('Column_Reboiler_Duty_kW', 'N/A'):.2f}"],
        ["Status",                             "SUCCESS" if res.get("Success") else f"FAILED: {res.get('Error_Message')}"],
    ]
    print("\n--- PART B RESULTS ---")
    print(tabulate(table, headers=["Parameter", "Value"], tablefmt="grid"))
    return res


if __name__ == "__main__":
    run_part_b()
