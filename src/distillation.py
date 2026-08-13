"""
src/distillation.py
===================
Part B – Distillation Column simulation.

Builds an n-pentane / isopentane distillation column flowsheet programmatically
using the DWSIM Automation API and returns a result dictionary.
No prebuilt flowsheet is loaded or required.
"""

import os
from typing import Optional

from src.dwsim_automation import DWSIMEnvironment
from config.simulation_config import (
    COMPOUNDS,
    PROPERTY_PACKAGE,
    COLUMN_BASE,
    COLUMN_FEED_COMPOSITION,
    COLUMN_FEED_FLOW,
    DISTILLATION_FLOWSHEET,
)


def run_distillation(
    num_stages: int = COLUMN_BASE["num_stages"],
    feed_stage: int = COLUMN_BASE["feed_stage"],
    reflux_ratio: float = COLUMN_BASE["reflux_ratio"],
    distillate_flow: float = COLUMN_BASE["distillate_flow"],
    feed_temp: float = COLUMN_BASE["feed_temp"],
    feed_press: float = COLUMN_BASE["feed_press"],
    save_flowsheet: bool = False,
    flowsheet_path: Optional[str] = None,
) -> dict:
    """
    Simulate binary distillation of n-pentane and isopentane.

    Parameters
    ----------
    num_stages : int
        Total number of equilibrium stages.
    feed_stage : int
        Feed stage index (0-indexed).
    reflux_ratio : float
        Condenser reflux ratio specification.
    distillate_flow : float
        Distillate molar flow rate specification [mol/s].
    feed_temp : float
        Feed stream temperature [K].
    feed_press : float
        Feed stream pressure [Pa].
    save_flowsheet : bool
        Whether to save the generated flowsheet to disk.
    flowsheet_path : str, optional
        Override the default flowsheet save path.

    Returns
    -------
    dict
        Simulation inputs, KPIs, success flag, and error message.
    """
    try:
        # Input validation
        if num_stages < 2:
            raise ValueError("Number of stages must be at least 2.")
        if not (0 <= feed_stage < num_stages):
            raise ValueError(f"Feed stage index ({feed_stage}) must be between 0 and {num_stages - 1} (inclusive).")
        if reflux_ratio <= 0:
            raise ValueError("Reflux ratio must be greater than 0.")
        if distillate_flow <= 0:
            raise ValueError("Distillate flow must be greater than 0.")
        if feed_temp <= 0:
            raise ValueError("Feed temperature must be greater than 0 K.")
        if feed_press <= 0:
            raise ValueError("Feed pressure must be greater than 0.")

        auto = DWSIMEnvironment.initialize()

        from System import Array, Double  # type: ignore
        from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType  # type: ignore

        # Build empty flowsheet 
        sim = auto.CreateFlowsheet()
        for compound in COMPOUNDS:
            sim.AddCompound(compound)
        sim.CreateAndAddPropertyPackage(PROPERTY_PACKAGE)

        #  Streams 
        feed = sim.AddObject(ObjectType.MaterialStream, 50, 50, "Feed")
        feed_obj = feed.GetAsObject()
        feed_obj.SetTemperature(feed_temp)
        feed_obj.SetPressure(feed_press)
        feed_obj.SetMolarFlow(COLUMN_FEED_FLOW)
        feed_obj.SetOverallComposition(Array[Double](COLUMN_FEED_COMPOSITION))

        distillate = sim.AddObject(ObjectType.MaterialStream, 400, 20, "Distillate")
        bottoms = sim.AddObject(ObjectType.MaterialStream, 400, 200, "Bottoms")
        qc = sim.AddObject(ObjectType.EnergyStream, 350, 20, "Q_Condenser")
        qr = sim.AddObject(ObjectType.EnergyStream, 350, 200, "Q_Reboiler")

        # ── Distillation column unit operation ───────────────────────────────
        col = sim.AddObject(ObjectType.DistillationColumn, 200, 50, "Col")
        col_obj = col.GetAsObject()
        
        # Sizing stages and initializing stage pressures explicitly.
        # This prevents new stages from being created at 0.0 Pa pressure,
        # which crashes flash calculation routines and breaks solver convergence.
        col_obj.SetNumberOfStages(num_stages)
        for stage in col_obj.Stages:
            stage.P = feed_press
            
        col_obj.RebuildEstimates()

        col_obj.ConnectFeed(feed, feed_stage)
        col_obj.ConnectDistillate(distillate)
        col_obj.ConnectBottoms(bottoms)
        col_obj.ConnectCondenserDuty(qc)
        col_obj.ConnectReboilerDuty(qr)

        # Column specs: Spec "C" = reflux ratio, Spec "R" = distillate flow
        col_obj.Specs["C"].SpecValue = reflux_ratio
        col_obj.Specs["R"].SpecValue = distillate_flow
        col_obj.RebuildEstimates()

        #  Solve 
        auto.CalculateFlowsheet2(sim)

        #  Save flowsheet (output artefact only) 
        if save_flowsheet:
            save_path = flowsheet_path or DISTILLATION_FLOWSHEET
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            auto.SaveFlowsheet2(sim, save_path)

        #  Extract results 
        dist_obj = distillate.GetAsObject()
        bot_obj = bottoms.GetAsObject()

        dist_comp = list(dist_obj.GetOverallComposition())
        bot_comp = list(bot_obj.GetOverallComposition())

        # Isopentane (index 1) has a lower boiling point → concentrates in distillate
        x_ip_dist = dist_comp[1]
        x_np_bot = bot_comp[0]

        #  Extract column duties 
        # Prefer DWSIM's native column properties (most reliable post-convergence).
        # Fall back to energy stream EnergyFlow if the property is unavailable.
        try:
            q_cond = float(col_obj.CondenserDuty) if col_obj.CondenserDuty is not None else 0.0
            q_reb  = float(col_obj.ReboilerDuty)  if col_obj.ReboilerDuty  is not None else 0.0
        except AttributeError:
            qc_obj = qc.GetAsObject()
            qr_obj = qr.GetAsObject()
            q_cond = float(qc_obj.EnergyFlow) if qc_obj.EnergyFlow is not None else 0.0
            q_reb  = float(qr_obj.EnergyFlow) if qr_obj.EnergyFlow is not None else 0.0

        #  Convergence criterion 
        # Use col_obj.Calculated exclusively — it is set to True only when the
        # column MESH equations have converged.  Stream-flow heuristics are
        # unreliable and can mask partial / non-converged solutions.
        is_success = bool(col_obj.Calculated)

        return {
            # metadata
            "Simulation_Type": "Distillation",
            "Success": is_success,
            "Error_Message": "" if is_success else "Column solver did not converge",
            # sweep variables
            "Column_Stages": num_stages,
            "Column_Feed_Stage": feed_stage + 1,   # 1-indexed for reporting
            "Column_Reflux_Ratio": reflux_ratio,
            "Column_Distillate_Flow_mols": distillate_flow,
            # KPIs
            "Column_Distillate_Purity_pct": x_ip_dist * 100.0,
            "Column_Bottoms_Purity_pct": x_np_bot * 100.0,
            "Column_Condenser_Duty_kW": q_cond,
            "Column_Reboiler_Duty_kW": q_reb,
        }

    except Exception as exc:
        return {
            "Simulation_Type": "Distillation",
            "Success": False,
            "Error_Message": str(exc),
            "Column_Stages": num_stages,
            "Column_Feed_Stage": feed_stage + 1,
            "Column_Reflux_Ratio": reflux_ratio,
            "Column_Distillate_Flow_mols": distillate_flow,
            "Column_Distillate_Purity_pct": None,
            "Column_Bottoms_Purity_pct": None,
            "Column_Condenser_Duty_kW": None,
            "Column_Reboiler_Duty_kW": None,
        }
