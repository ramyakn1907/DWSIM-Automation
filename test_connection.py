import clr
import os

# Path to your DWSIM installation
dwsim_path = r"C:\Users\ramya\AppData\Local\DWSIM"

# Add DWSIM folder to search path
os.add_dll_directory(dwsim_path)

# Load the Automation DLL
clr.AddReference(os.path.join(dwsim_path, "DWSIM.Automation.dll"))

print("✅ DWSIM Automation DLL loaded successfully!")