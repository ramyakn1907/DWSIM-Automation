"""
tests/test_configuration.py
============================
Basic validation tests for the project configuration and environment.

Run with:
    python tests/test_configuration.py

Checks:
  - DWSIM_PATH directory exists
  - Required DWSIM DLLs are present
  - ThermoCS sub-directory exists
  - Config values are of the expected types and within plausible ranges
  - Output directories are creatable
"""

import os
import sys
import traceback

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Allow imports from project root
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from config.simulation_config import (
    DWSIM_PATH,
    THERMOCS_PATH,
    OUTPUTS_DIR,
    FLOWSHEETS_DIR,
    PLOTS_DIR,
    KINETIC_PRE_EXP,
    KINETIC_ACTIVATION_ENERGY,
    PFR_BASE,
    COLUMN_BASE,
    PFR_SWEEP_VOLUMES,
    PFR_SWEEP_TEMPS,
    COLUMN_SWEEP_REFLUX,
    COLUMN_SWEEP_STAGES,
)

PASS = "  [PASS]"
FAIL = "  [FAIL]"

results: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    tag = PASS if condition else FAIL
    msg = f"{tag}  {name}"
    if detail:
        msg += f"\n         {detail}"
    print(msg)
    results.append((name, condition, detail))


# ---------------------------------------------------------------------------
# 1. DWSIM installation
# ---------------------------------------------------------------------------
print("\n=== 1. DWSIM Installation ===")
check("DWSIM_PATH exists", os.path.isdir(DWSIM_PATH), DWSIM_PATH)
check("ThermoCS sub-directory exists", os.path.isdir(THERMOCS_PATH), THERMOCS_PATH)

required_dlls = [
    "DWSIM.Automation.dll",
    "DWSIM.Interfaces.dll",
    "DWSIM.Thermodynamics.dll",
    "DWSIM.UnitOperations.dll",
    "DWSIM.FlowsheetSolver.dll",
]
for dll in required_dlls:
    dll_path = os.path.join(DWSIM_PATH, dll)
    check(f"DLL present: {dll}", os.path.isfile(dll_path), dll_path)

thermocs_dll = os.path.join(THERMOCS_PATH, "ThermoCS.dll")
check("ThermoCS.dll present", os.path.isfile(thermocs_dll), thermocs_dll)

# ---------------------------------------------------------------------------
# 2. Output directory creation
# ---------------------------------------------------------------------------
print("\n=== 2. Output Directories ===")
for label, path in [
    ("outputs/", OUTPUTS_DIR),
    ("outputs/flowsheets/", FLOWSHEETS_DIR),
    ("outputs/plots/", PLOTS_DIR),
]:
    try:
        os.makedirs(path, exist_ok=True)
        check(f"Can create/access: {label}", True, path)
    except Exception as exc:
        check(f"Can create/access: {label}", False, str(exc))

# ---------------------------------------------------------------------------
# 3. Kinetic parameters
# ---------------------------------------------------------------------------
print("\n=== 3. Kinetic Parameters ===")
check(
    "KINETIC_PRE_EXP > 0",
    isinstance(KINETIC_PRE_EXP, (int, float)) and KINETIC_PRE_EXP > 0,
    f"Value: {KINETIC_PRE_EXP}",
)
check(
    "KINETIC_ACTIVATION_ENERGY > 0",
    isinstance(KINETIC_ACTIVATION_ENERGY, (int, float)) and KINETIC_ACTIVATION_ENERGY > 0,
    f"Value: {KINETIC_ACTIVATION_ENERGY}",
)

# ---------------------------------------------------------------------------
# 4. PFR base configuration
# ---------------------------------------------------------------------------
print("\n=== 4. PFR Base Config ===")
check("PFR volume > 0", PFR_BASE.get("v_reactor", 0) > 0, str(PFR_BASE.get("v_reactor")))
check("PFR temp in [200, 1000] K", 200 < PFR_BASE.get("t_feed", 0) < 1000, str(PFR_BASE.get("t_feed")))
check("PFR pressure > 0", PFR_BASE.get("p_feed", 0) > 0, str(PFR_BASE.get("p_feed")))
check("PFR feed flow > 0", PFR_BASE.get("flow_feed", 0) > 0, str(PFR_BASE.get("flow_feed")))

# ---------------------------------------------------------------------------
# 5. Column base configuration
# ---------------------------------------------------------------------------
print("\n=== 5. Column Base Config ===")
check("Column stages >= 2", COLUMN_BASE.get("num_stages", 0) >= 2, str(COLUMN_BASE.get("num_stages")))
check(
    "Feed stage within range",
    0 <= COLUMN_BASE.get("feed_stage", -1) < COLUMN_BASE.get("num_stages", 0),
    f"feed_stage={COLUMN_BASE.get('feed_stage')}, num_stages={COLUMN_BASE.get('num_stages')}",
)
check("Reflux ratio > 0", COLUMN_BASE.get("reflux_ratio", 0) > 0, str(COLUMN_BASE.get("reflux_ratio")))
check("Distillate flow > 0", COLUMN_BASE.get("distillate_flow", 0) > 0, str(COLUMN_BASE.get("distillate_flow")))

# ---------------------------------------------------------------------------
# 6. Sweep ranges
# ---------------------------------------------------------------------------
print("\n=== 6. Sweep Ranges ===")
check("PFR sweep volumes non-empty", len(PFR_SWEEP_VOLUMES) > 0, str(PFR_SWEEP_VOLUMES))
check("PFR sweep temps non-empty", len(PFR_SWEEP_TEMPS) > 0, str(PFR_SWEEP_TEMPS))
check("PFR sweep volumes have >=2 variables", len(PFR_SWEEP_VOLUMES) >= 2, "")
check("PFR sweep temps have >=2 variables", len(PFR_SWEEP_TEMPS) >= 2, "")
check("Column sweep reflux non-empty", len(COLUMN_SWEEP_REFLUX) > 0, str(COLUMN_SWEEP_REFLUX))
check("Column sweep stages non-empty", len(COLUMN_SWEEP_STAGES) > 0, str(COLUMN_SWEEP_STAGES))
check("Column sweep reflux has >=2 variables", len(COLUMN_SWEEP_REFLUX) >= 2, "")
check("Column sweep stages has >=2 variables", len(COLUMN_SWEEP_STAGES) >= 2, "")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 55)
total = len(results)
passed = sum(1 for _, ok, _ in results if ok)
failed = total - passed
print(f"  Results: {passed}/{total} passed  |  {failed} failed")
if failed:
    print("\n  Failed checks:")
    for name, ok, detail in results:
        if not ok:
            print(f"    ✗ {name}")
            if detail:
                print(f"      {detail}")
print("=" * 55 + "\n")

sys.exit(0 if failed == 0 else 1)
