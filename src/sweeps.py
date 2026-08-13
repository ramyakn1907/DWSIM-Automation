"""
src/sweeps.py
=============
Part C – Multi-variable parametric sweeps for PFR and Distillation Column.

Each sweep iterates over all combinations of the configured variable ranges,
runs the corresponding simulation, and appends the result to a list.
Failed cases are caught and logged — they do NOT abort the sweep.
Results are saved to CSV via ``src.results``.
"""

import pandas as pd

from src.pfr import run_pfr
from src.distillation import run_distillation
from config.simulation_config import (
    PFR_SWEEP_VOLUMES,
    PFR_SWEEP_TEMPS,
    COLUMN_SWEEP_REFLUX,
    COLUMN_SWEEP_STAGES,
    PFR_SWEEP_CSV,
    COLUMN_SWEEP_CSV,
)


def sweep_pfr(
    v_range: list[float] = PFR_SWEEP_VOLUMES,
    t_range: list[float] = PFR_SWEEP_TEMPS,
    csv_path: str = PFR_SWEEP_CSV,
) -> pd.DataFrame:
    """
    Run a two-variable parametric sweep for the PFR.

    Variables swept
    ---------------
    - Reactor Volume  [m³]
    - Feed Temperature [K]

    Parameters
    ----------
    v_range : list[float]
        Reactor volumes to evaluate.
    t_range : list[float]
        Feed temperatures to evaluate.
    csv_path : str
        Path to save the sweep results CSV.

    Returns
    -------
    pd.DataFrame
        One row per case, including all KPIs, success flags, and error messages.
    """
    results = []
    print("\n--- PFR Parametric Sweep ---")

    for v in v_range:
        for t in t_range:
            res = run_pfr(v_reactor=v, t_feed=t)
            results.append(res)

            conv_str = (
                f"{res['PFR_Conversion_pct']:.2f}%"
                if res["PFR_Conversion_pct"] is not None
                else "N/A"
            )
            duty_str = (
                f"{res['PFR_Heat_Duty_kW']:.2f} kW"
                if res["PFR_Heat_Duty_kW"] is not None
                else "N/A"
            )
            status = "OK" if res["Success"] else f"FAILED: {res['Error_Message']}"
            print(
                f"  PFR | V={v:.1f} m³ | T={t:.1f} K | "
                f"Conv={conv_str} | Duty={duty_str} | {status}"
            )

    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)
    print(f"  → Saved: {csv_path}")
    return df


def sweep_column(
    rr_range: list[float] = COLUMN_SWEEP_REFLUX,
    stage_range: list[int] = COLUMN_SWEEP_STAGES,
    csv_path: str = COLUMN_SWEEP_CSV,
) -> pd.DataFrame:
    """
    Run a two-variable parametric sweep for the Distillation Column.

    Variables swept
    ---------------
    - Reflux Ratio
    - Number of Stages

    Parameters
    ----------
    rr_range : list[float]
        Reflux ratios to evaluate.
    stage_range : list[int]
        Stage counts to evaluate.
    csv_path : str
        Path to save the sweep results CSV.

    Returns
    -------
    pd.DataFrame
        One row per case, including all KPIs, success flags, and error messages.
    """
    results = []
    print("\n--- Distillation Column Parametric Sweep ---")

    for n in stage_range:
        feed_st = n // 2 - 1  # middle feed stage (0-indexed)
        for rr in rr_range:
            res = run_distillation(num_stages=n, feed_stage=feed_st, reflux_ratio=rr)
            results.append(res)

            purity_str = (
                f"{res['Column_Distillate_Purity_pct']:.2f}%"
                if res["Column_Distillate_Purity_pct"] is not None
                else "N/A"
            )
            qc_str = (
                f"{res['Column_Condenser_Duty_kW']:.1f} kW"
                if res["Column_Condenser_Duty_kW"] is not None
                else "N/A"
            )
            status = "OK" if res["Success"] else f"FAILED: {res['Error_Message']}"
            print(
                f"  COL | Stages={n} | RR={rr:.1f} | "
                f"Purity={purity_str} | Qc={qc_str} | {status}"
            )

    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)
    print(f"  → Saved: {csv_path}")
    return df
