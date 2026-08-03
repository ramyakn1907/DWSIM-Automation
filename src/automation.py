import os
import clr
import inspect

# ==========================================
# DWSIM Installation Path
# ==========================================

DWSIM_PATH = r"C:\Users\ramya\AppData\Local\DWSIM"

os.add_dll_directory(DWSIM_PATH)

clr.AddReference(os.path.join(DWSIM_PATH, "DWSIM.Automation.dll"))

from DWSIM.Automation import Automation3
from System.IO import Path
from System import Environment

# ==========================================
# Create Automation Manager
# ==========================================

automation = Automation3()

print("=" * 60)
print("DWSIM Automation Started")
print("=" * 60)

# ==========================================
# Create Flowsheet
# ==========================================

flowsheet = automation.CreateFlowsheet()

print("✅ Flowsheet Created")

# ==========================================
# Add Property Package
# ==========================================

flowsheet.CreateAndAddPropertyPackage("Raoult's Law")

print("✅ Property Package Added")

# ==========================================
# Add Water Compound
# ==========================================

flowsheet.AddCompound("Water")

print("✅ Water Compound Added")

# ==========================================
# Create Feed Stream
# ==========================================

feed = flowsheet.AddFlowsheetObject(
    "Material Stream",
    "Feed"
)

print("✅ Feed Stream Created")
print(feed)

# ==========================================
# Create Pump
# ==========================================

pump = flowsheet.AddFlowsheetObject(
    "Pump",
    "Pump-1"
)

print("✅ Pump Created")
print(pump)

# ==========================================
# Get Graphic Objects
# ==========================================

feed_graphic = feed.GraphicObject
pump_graphic = pump.GraphicObject

print("\n✅ Feed Graphic Object")
print(feed_graphic)

print("\n✅ Pump Graphic Object")
print(pump_graphic)

# ==========================================
# Connect Feed -> Pump
# ==========================================

print("\nConnecting Feed to Pump...")

flowsheet.ConnectObjects(
    feed_graphic,
    pump_graphic,
    0,
    0
)

print("✅ Feed Connected to Pump")

# ==========================================
# Save Flowsheet
# ==========================================

fileNameToSave = Path.Combine(
    Environment.GetFolderPath(
        Environment.SpecialFolder.Desktop
    ),
    "FirstSimulation.dwxmz"
)

automation.SaveFlowsheet(
    flowsheet,
    fileNameToSave,
    True
)

print("\n✅ Flowsheet Saved Successfully")
print(fileNameToSave)

print("\n" + "=" * 60)
print("Day 4 Completed")
print("=" * 60)