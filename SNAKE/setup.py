import os 
import sys
import platform

print("Installing the python modules required for the snake game:")
if sys.platform.startswith("win"):
    "WINDOWS"
    os.system("pip install --upgrade pip install pygame")

if sys.platform.startswith("linux"):
    "LINUX"
    os.system("pip install --upgrade pip install pygame")
