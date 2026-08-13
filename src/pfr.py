"""
src/pfr.py
==========
Part A – Plug Flow Reactor (PFR) simulation.

Builds an n-pentane isomerisation PFR flowsheet programmatically using the
DWSIM Automation API and returns a result dictionary.  No prebuilt flowsheet
is loaded; every object is created at runtime.
"""

import os
from typing import Optional

from src.dwsim_automation import DWSIMEnvironment
from config.simulation_config import (
    COMPOUNDS,
    PROPERTY_PACKAGE,
    KINETIC_PRE_EXP,
    KINETIC_ACTIVATION_ENERGY,
    PFR_BASE,
    PFR_FLOWSHEET,
)


def run_pfr(
    v_reactor: float = PFR_BASE["v_reactor"],
    t_feed: float = PFR_BASE["t_feed"],
    p_feed: float = PFR_BASE["p_feed"],
    flow_feed: float = PFR_BASE["flow_feed"],
    save_flowsheet: bool = False,
    flowsheet_path: Optional[str] = None,
) -> dict:
    """
    Simulate the isothermal isomerisation of n-pentane to isopentane in a PFR.

    Parameters
    ----------
    v_reactor : float
        Reactor volume [m³].
    t_feed : float
        Feed (and isothermal operating) temperature [K].
    p_feed : float
        Feed pressure [Pa].
    flow_feed : float
        Feed molar flow rate [mol/s] – pure n-pentane.
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
        if v_reactor <= 0:
            raise ValueError("Reactor volume must be greater than 0.")
        if t_feed <= 0:
            raise ValueError("Feed temperature must be greater than 0 K.")
        if p_feed <= 0:
            raise ValueError("Feed pressure must be greater than 0.")
        if flow_feed <= 0:
            raise ValueError("Feed molar flow must be greater than 0.")

        auto = DWSIMEnvironment.initialize()

        import System  # type: ignore
        from System import Array, Double  # type: ignore
        from System.Collections.Generic import Dictionary  # type: ignore
        from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType  # type: ignore
        from DWSIM.UnitOperations.Reactors import OperationMode  # type: ignore

        #  Build empty flowsheet 
        sim = auto.CreateFlowsheet()
        for compound in COMPOUNDS:
            sim.AddCompound(compound)
        sim.CreateAndAddPropertyPackage(PROPERTY_PACKAGE)

        #  Streams 
        feed = sim.AddObject(ObjectType.MaterialStream, 50, 50, "Feed")
        feed_obj = feed.GetAsObject()
        feed_obj.SetTemperature(t_feed)
        feed_obj.SetPressure(p_feed)
        feed_obj.SetMolarFlow(flow_feed)
        feed_obj.SetOverallComposition(Array[Double]([1.0, 0.0]))  # 100 % n-pentane

        prod = sim.AddObject(ObjectType.MaterialStream, 250, 50, "Product")
        energy = sim.AddObject(ObjectType.EnergyStream, 150, 150, "Energy")

        # Kinetic reaction  (n-Pentane → Isopentane) 
        stoich = Dictionary[System.String, System.Double]()
        stoich["n-Pentane"] = -1.0
        stoich["Isopentane"] = 1.0

        dord = Dictionary[System.String, System.Double]()
        dord["n-Pentane"] = 1.0
        dord["Isopentane"] = 0.0

        rord = Dictionary[System.String, System.Double]()
        rord["n-Pentane"] = 0.0
        rord["Isopentane"] = 0.0

        rxn = sim.CreateKineticReaction(
            "Isom", "n-Pentane to Isopentane Isomerization",
            stoich, dord, rord, "n-Pentane", "Vapor",
            # basis: lowercase as required by DWSIM API
            # rateunits: must include amount + volume + time ("mol/m3.s")
            # amountunits: "mol"
            "molar concentration", "mol", "mol/m3.s",
            KINETIC_PRE_EXP, KINETIC_ACTIVATION_ENERGY,
            0.0, 0.0, "", "",
        )
        sim.AddReaction(rxn)

        rset = sim.CreateReactionSet("IsomSet", "Isomerization Reaction Set")
        sim.AddReactionSet(rset)
        sim.AddReactionToSet(rxn.ID, rset.ID, True, 1)

        #  PFR unit operation 
        pfr = sim.AddObject(ObjectType.RCT_PFR, 150, 50, "PFR")
        pfr_obj = pfr.GetAsObject()

        sim.ConnectObjects(feed.GraphicObject, pfr.GraphicObject, 0, 0)
        sim.ConnectObjects(pfr.GraphicObject, prod.GraphicObject, 0, 0)
        sim.ConnectObjects(energy.GraphicObject, pfr.GraphicObject, 0, 1)

        pfr_obj.ReactionSetID = rset.ID
        pfr_obj.ReactorOperationMode = OperationMode.Isothermic
        pfr_obj.Volume = v_reactor

        #  Solve 
        auto.CalculateFlowsheet2(sim)

        # Save flowsheet (output artefact only) 
        if save_flowsheet:
            save_path = flowsheet_path or PFR_FLOWSHEET
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            auto.SaveFlowsheet2(sim, save_path)

        #  Extract results 
        prod_obj = prod.GetAsObject()
        energy_obj = energy.GetAsObject()

        comp_out = list(prod_obj.GetOverallComposition())
        x_npentane = comp_out[0]
        x_isopentane = comp_out[1]

        total_flow = prod_obj.GetMolarFlow()
        flow_np_out = total_flow * x_npentane
        flow_ip_out = total_flow * x_isopentane
        conversion = (flow_feed - flow_np_out) / flow_feed * 100.0

        duty_kw = energy_obj.EnergyFlow if energy_obj.EnergyFlow is not None else 0.0
        outlet_temp_k = prod_obj.GetTemperature()

        is_success = bool(pfr_obj.Calculated)

        return {
            # metadata
            "Simulation_Type": "PFR",
            "Success": is_success,
            "Error_Message": "" if is_success else "PFR solver did not converge",
            # sweep variables
            "PFR_Volume_m3": v_reactor,
            "PFR_Temperature_K": t_feed,
            # KPIs
            "PFR_Outlet_Temp_K": outlet_temp_k,
            "PFR_Outlet_Temp_C": outlet_temp_k - 273.15,
            "PFR_Conversion_pct": conversion,
            "PFR_NPentane_Outlet_mols": flow_np_out,
            "PFR_Isopentane_Outlet_mols": flow_ip_out,
            "PFR_Heat_Duty_kW": duty_kw,
        }

    except Exception as exc:
        return {
            "Simulation_Type": "PFR",
            "Success": False,
            "Error_Message": str(exc),
            "PFR_Volume_m3": v_reactor,
            "PFR_Temperature_K": t_feed,
            "PFR_Outlet_Temp_K": None,
            "PFR_Outlet_Temp_C": None,
            "PFR_Conversion_pct": None,
            "PFR_NPentane_Outlet_mols": None,
            "PFR_Isopentane_Outlet_mols": None,
            "PFR_Heat_Duty_kW": None,
        }
