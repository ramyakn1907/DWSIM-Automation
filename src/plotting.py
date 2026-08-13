"""
src/plotting.py
===============
Optional parametric trend visualisation.

Generates two plots from sweep DataFrames:
  1. PFR Conversion vs Reactor Volume (one curve per feed temperature)
  2. Distillation Column Distillate Purity vs Reflux Ratio (one curve per stage count)

Both plots are saved to ``outputs/plots/`` as high-resolution PNG files.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

from config.simulation_config import PFR_PLOT, COLUMN_PLOT, PLOTS_DIR


class Plotter:
    """Generate and save parametric sweep trend plots."""

    @staticmethod
    def plot_sweeps(
        pfr_df: pd.DataFrame,
        col_df: pd.DataFrame,
        pfr_plot_path: str = PFR_PLOT,
        col_plot_path: str = COLUMN_PLOT,
    ) -> None:
        """
        Generate and save both PFR and column sweep trend plots.

        Parameters
        ----------
        pfr_df : pd.DataFrame
            PFR sweep results (from ``src.sweeps.sweep_pfr``).
        col_df : pd.DataFrame
            Column sweep results (from ``src.sweeps.sweep_column``).
        pfr_plot_path : str
            Output file path for the PFR plot.
        col_plot_path : str
            Output file path for the column plot.
        """
        os.makedirs(PLOTS_DIR, exist_ok=True)
        Plotter._plot_pfr(pfr_df, pfr_plot_path)
        Plotter._plot_column(col_df, col_plot_path)
        print(f"\n  → Plots saved to: {PLOTS_DIR}")

    @staticmethod
    def _plot_pfr(df: pd.DataFrame, save_path: str) -> None:
        """PFR Conversion vs Reactor Volume, one line per temperature."""
        valid = df[df["Success"] == True] if "Success" in df.columns else df

        plt.figure(figsize=(8, 5))
        for t_val, group in valid.groupby("PFR_Temperature_K"):
            plt.plot(
                group["PFR_Volume_m3"],
                group["PFR_Conversion_pct"],
                marker="o",
                label=f"T = {t_val:.1f} K",
            )

        plt.title("PFR Isomerization: Conversion vs Reactor Volume")
        plt.xlabel("Reactor Volume (m³)")
        plt.ylabel("n-Pentane Conversion (%)")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"    PFR plot → {save_path}")

    @staticmethod
    def _plot_column(df: pd.DataFrame, save_path: str) -> None:
        """Distillate Purity vs Reflux Ratio, one line per stage count."""
        valid = df[df["Success"] == True] if "Success" in df.columns else df

        plt.figure(figsize=(8, 5))
        for n_val, group in valid.groupby("Column_Stages"):
            plt.plot(
                group["Column_Reflux_Ratio"],
                group["Column_Distillate_Purity_pct"],
                marker="s",
                label=f"N = {n_val} stages",
            )

        plt.title("Distillation Column: Isopentane Distillate Purity vs Reflux Ratio")
        plt.xlabel("Reflux Ratio")
        plt.ylabel("Distillate Isopentane Purity (%)")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"    Column plot → {save_path}")
