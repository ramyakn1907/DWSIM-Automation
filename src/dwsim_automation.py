"""
src/dwsim_automation.py
=======================
DWSIM Automation API bootstrap layer.

Handles .NET runtime initialisation, assembly loading, and provides a
singleton ``DWSIMEnvironment`` whose ``initialize()`` class-method returns
a ready-to-use ``Automation3`` object.

All other modules (pfr, distillation, sweeps …) call
``DWSIMEnvironment.initialize()`` to obtain the automation handle.
"""

import os
import sys

# Lazily imported after pythonnet is available
_Automation3 = None


class DWSIMEnvironment:
    """Singleton bootstrap for the DWSIM .NET Automation API."""

    _initialized: bool = False
    _auto = None  # DWSIM.Automation.Automation3 instance

    @classmethod
    def initialize(cls):
        """
        Load DWSIM assemblies and return the ``Automation3`` handle.

        Reads ``DWSIM_PATH`` from the active config so the path is never
        hard-coded here.
        """
        if cls._initialized:
            return cls._auto

        # Import config here to avoid circular imports at module level
        from config.simulation_config import DWSIM_PATH, THERMOCS_PATH

        # Extend PATH so that native DLLs (e.g. ThermoCS) are resolved
        for path in [DWSIM_PATH, THERMOCS_PATH]:
            if os.path.exists(path):
                if path not in sys.path:
                    sys.path.append(path)
                current_path = os.environ.get("PATH", "")
                if path not in current_path:
                    os.environ["PATH"] = path + os.pathsep + current_path

        import clr  # noqa: F401 – pythonnet
        clr.AddReference("DWSIM.Automation")
        clr.AddReference("DWSIM.Interfaces")
        clr.AddReference("DWSIM.Thermodynamics")
        clr.AddReference("DWSIM.UnitOperations")
        clr.AddReference("DWSIM.FlowsheetSolver")

        from DWSIM.Automation import Automation3  # type: ignore

        cls._auto = Automation3()
        cls._initialized = True
        return cls._auto
