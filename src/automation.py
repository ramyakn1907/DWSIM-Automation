import os
import clr

# ==========================================
# DWSIM Installation Path
# ==========================================

DWSIM_PATH = r"C:\Users\ramya\AppData\Local\DWSIM"

# Add DWSIM DLL path
os.add_dll_directory(DWSIM_PATH)

# Load DWSIM Automation DLL
clr.AddReference(os.path.join(DWSIM_PATH, "DWSIM.Automation.dll"))

# Import Automation API
from DWSIM.Automation import Automation3

# .NET Classes
from System.IO import Path
from System import Environment

# ==========================================
# Create Automation Manager
# ==========================================

automation = Automation3()

print("=" * 50)
print("Creating Flowsheet...")
print("=" * 50)

# ==========================================
# Create Flowsheet
# ==========================================

flowsheet = automation.CreateFlowsheet()

print("✅ Flowsheet Created")

# ==========================================
# Add Property Package
# ==========================================

package = flowsheet.CreateAndAddPropertyPackage("Raoult's Law")

print("✅ Property Package Added")

# ==========================================
# Add Water Compound
# ==========================================

flowsheet.AddCompound("Water")

print("✅ Water Compound Added")

# ==========================================
# Display Selected Compounds
# ==========================================

print("\nSelected Compounds:")
print("-" * 50)

for compound in flowsheet.SelectedCompounds:
    print(compound)

# ==========================================
# Display Property Packages
# ==========================================

print("\nProperty Packages:")
print("-" * 50)

for pkg in flowsheet.PropertyPackages:
    print(pkg)

# ==========================================
# Save Flowsheet
# ==========================================

fileNameToSave = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
    "FirstSimulation.dwxmz"
)

automation.SaveFlowsheet(
    flowsheet,
    fileNameToSave,
    True
)

print("\n✅ Flowsheet Saved Successfully!")
print("Location :", fileNameToSave)