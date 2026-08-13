"""
src/results.py
==============
Result collection and unified CSV logging.

``ResultsLogger.generate`` merges the Part A baseline, Part B baseline, and
all Part C sweep cases into a single ``results.csv`` file that contains:

  - Case metadata   (Case_ID, Case_Name, Simulation_Type)
  - Execution status (Success, Error_Message)
  - PFR sweep variables  (PFR_Volume_m3, PFR_Temperature_K)
  - Column sweep variables (Column_Stages, Column_Reflux_Ratio, …)
  - PFR KPIs
  - Column KPIs

Fields that are not applicable to a given simulation type are left empty (NaN).
"""

from datetime import datetime
import os
from typing import Optional

import pandas as pd

from config.simulation_config import RESULTS_CSV

# Final column ordering in results.csv — exactly these columns, no extras
_COL_ORDER = [
    # Case metadata
    "Timestamp",
    "Case_ID",
    "Case_Name",
    "Simulation_Type",
    # Execution status
    "Success",
    "Error_Message",
    # PFR sweep variables
    "PFR_Volume_m3",
    "PFR_Temperature_K",
    # PFR KPIs
    "PFR_Outlet_Temp_K",
    "PFR_Outlet_Temp_C",
    "PFR_Conversion_pct",
    "PFR_NPentane_Outlet_mols",
    "PFR_Isopentane_Outlet_mols",
    "PFR_Heat_Duty_kW",
    # Column sweep variables
    "Column_Stages",
    "Column_Feed_Stage",
    "Column_Reflux_Ratio",
    # Column KPIs
    "Column_Distillate_Purity_pct",
    "Column_Bottoms_Purity_pct",
    "Column_Condenser_Duty_kW",
    "Column_Reboiler_Duty_kW",
]


class ResultsLogger:
    """Collect and persist simulation results."""

    @staticmethod
    def generate(
        part_a_result: dict,
        part_b_result: dict,
        pfr_sweep_df: pd.DataFrame,
        col_sweep_df: pd.DataFrame,
        output_path: str = RESULTS_CSV,
    ) -> pd.DataFrame:
        """
        Merge all cases and write the unified ``results.csv``.

        Parameters
        ----------
        part_a_result : dict
            Result dict from ``src.pfr.run_pfr`` (baseline case).
        part_b_result : dict
            Result dict from ``src.distillation.run_distillation`` (baseline).
        pfr_sweep_df : pd.DataFrame
            DataFrame returned by ``src.sweeps.sweep_pfr``.
        col_sweep_df : pd.DataFrame
            DataFrame returned by ``src.sweeps.sweep_column``.
        output_path : str
            Destination CSV file path.

        Returns
        -------
        pd.DataFrame
            The unified results DataFrame (also written to disk).
        """
        rows = []
        counter = 1

        # Get a single timestamp for the entire run
        run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Part A baseline
        r = dict(part_a_result)
        r["Timestamp"] = run_timestamp
        r["Case_ID"] = f"CASE-{counter:03d}"
        r["Case_Name"] = "Part_A_PFR_Baseline"
        rows.append(r)
        counter += 1

        # Part B baseline
        r = dict(part_b_result)
        r["Timestamp"] = run_timestamp
        r["Case_ID"] = f"CASE-{counter:03d}"
        r["Case_Name"] = "Part_B_Column_Baseline"
        rows.append(r)
        counter += 1

        # Part C – PFR sweep
        for _, row in pfr_sweep_df.iterrows():
            r = row.to_dict()
            v = r.get("PFR_Volume_m3", "")
            t = r.get("PFR_Temperature_K", "")
            r["Timestamp"] = run_timestamp
            r["Case_ID"] = f"CASE-{counter:03d}"
            r["Case_Name"] = f"Part_C_PFR_V{v}_T{t}"
            rows.append(r)
            counter += 1

        # Part C – Column sweep
        for _, row in col_sweep_df.iterrows():
            r = row.to_dict()
            n = r.get("Column_Stages", "")
            rr = r.get("Column_Reflux_Ratio", "")
            r["Timestamp"] = run_timestamp
            r["Case_ID"] = f"CASE-{counter:03d}"
            r["Case_Name"] = f"Part_C_Col_N{n}_RR{rr}"
            rows.append(r)
            counter += 1

        unified = pd.DataFrame(rows)

        # Enforce strict column set — only _COL_ORDER, no extras leaked from return dicts
        for col in _COL_ORDER:
            if col not in unified.columns:
                unified[col] = None
        unified = unified[_COL_ORDER]

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        unified.to_csv(output_path, index=False)

        total = len(unified)
        succeeded = unified["Success"].sum() if "Success" in unified.columns else "?"
        print(
            f"\n  → Unified results.csv saved: {output_path}"
            f"\n    Total cases: {total}  |  Successful: {succeeded}"
        )
        return unified
