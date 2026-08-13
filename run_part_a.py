"""
run_part_a.py
=============
Thin wrapper – executes Part A (PFR simulation) standalone.
Simulation logic lives in src/pfr.py.

Usage:
    python run_part_a.py
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from tabulate import tabulate
from src.pfr import run_pfr
from config.simulation_config import PFR_BASE


def run_part_a(
    v_reactor: float = PFR_BASE["v_reactor"],
    t_feed: float = PFR_BASE["t_feed"],
    p_feed: float = PFR_BASE["p_feed"],
    flow_feed: float = PFR_BASE["flow_feed"],
    save_flowsheet: bool = True,
) -> dict:
    print("=" * 60)
    print("      PART A: PFR ISOMERIZATION REACTOR SIMULATION")
    print("=" * 60)
    print(f"  Reactor Volume   : {v_reactor:.2f} m³")
    print(f"  Feed Temperature : {t_feed:.2f} K")
    print(f"  Feed Pressure    : {p_feed / 101325:.2f} atm")
    print(f"  Feed Flow        : {flow_feed:.2f} mol/s (100% n-pentane)")
    print("  Running DWSIM headless simulation...")

    res = run_pfr(
        v_reactor=v_reactor,
        t_feed=t_feed,
        p_feed=p_feed,
        flow_feed=flow_feed,
        save_flowsheet=save_flowsheet,
    )

    table = [
        ["Reactor Volume (m³)",            f"{res.get('PFR_Volume_m3', 'N/A'):.2f}" if isinstance(res.get('PFR_Volume_m3'), (int, float)) else "N/A"],
        ["Feed Temperature (K)",           f"{res.get('PFR_Temperature_K', 'N/A'):.2f}" if isinstance(res.get('PFR_Temperature_K'), (int, float)) else "N/A"],
        ["Outlet Temperature (K / °C)",    f"{res.get('PFR_Outlet_Temp_K', 'N/A'):.2f} K / {res.get('PFR_Outlet_Temp_C', 'N/A'):.2f} °C" if isinstance(res.get('PFR_Outlet_Temp_K'), (int, float)) else "N/A"],
        ["n-Pentane Conversion (%)",       f"{res.get('PFR_Conversion_pct', 'N/A'):.4f}" if isinstance(res.get('PFR_Conversion_pct'), (int, float)) else "N/A"],
        ["Outlet n-Pentane Flow (mol/s)",  f"{res.get('PFR_NPentane_Outlet_mols', 'N/A'):.6f}" if isinstance(res.get('PFR_NPentane_Outlet_mols'), (int, float)) else "N/A"],
        ["Outlet Isopentane Flow (mol/s)", f"{res.get('PFR_Isopentane_Outlet_mols', 'N/A'):.6f}" if isinstance(res.get('PFR_Isopentane_Outlet_mols'), (int, float)) else "N/A"],
        ["Heat Duty (kW)",                 f"{res.get('PFR_Heat_Duty_kW', 'N/A'):.4f}" if isinstance(res.get('PFR_Heat_Duty_kW'), (int, float)) else "N/A"],
        ["Status",                         "SUCCESS" if res.get("Success") else f"FAILED: {res.get('Error_Message')}"],
    ]
    print("\n--- PART A RESULTS ---")
    print(tabulate(table, headers=["Parameter", "Value"], tablefmt="grid"))
    return res


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Part A: PFR Isomerization Reactor Simulation")
    parser.add_argument("-v", "--volume", type=float, default=PFR_BASE["v_reactor"], help="Reactor volume [m³]")
    parser.add_argument("-t", "--temp", type=float, default=PFR_BASE["t_feed"], help="Feed temperature [K]")
    parser.add_argument("-p", "--pressure", type=float, default=PFR_BASE["p_feed"], help="Feed pressure [Pa]")
    parser.add_argument("-f", "--flow", type=float, default=PFR_BASE["flow_feed"], help="Feed flow [mol/s]")
    parser.add_argument("--no-save", action="store_true", help="Do not save the flowsheet")
    args = parser.parse_args()

    run_part_a(
        v_reactor=args.volume,
        t_feed=args.temp,
        p_feed=args.pressure,
        flow_feed=args.flow,
        save_flowsheet=not args.no_save,
    )
