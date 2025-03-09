# imports from python modules
import os
import sys
import platform
import argparse
from pathlib import Path

# imports from my personal modules located in utils folder
from utils.proscheduler import Proscheduler 

PROMETRIC_LOGO = """

 ____                           _        _      
|  _ \ _ __ ___  _ __ ___   ___| |_ _ __(_) ___ 
| |_) | '__/ _ \| '_ ` _ \ / _ \ __| '__| |/ __|
|  __/| | | (_) | | | | | |  __/ |_| |  | | (__ 
|_|__ |_|  \___/|_| |_| |_|\___|\__|_|  |_|\___|
/ ___|  ___| |__   ___  __| |_   _| | ___ _ __  
\___ \ / __| '_ \ / _ \/ _` | | | | |/ _ \ '__| 
 ___) | (__| | | |  __/ (_| | |_| | |  __/ |    
|____/ \___|_| |_|\___|\__,_|\__,_|_|\___|_|    


"""

print(PROMETRIC_LOGO)
print("Welcome to the Test Center Availability Checker!")
print("------------------------------------------------")
print("This script helps you check for available test center slots for your exam.")
print("You'll be prompted to provide some initial information, such as the exam name,")
print("month and year, and date range to search for available slots. Also how often")
print("you want to run script automatically.")
print("Once dates found it will play alert.mp3")
print("Let's get started!")
print("------------------------------------------------")

USERFILE_NAME = "user_input.txt"

operating_system = platform.system()
script_name = __file__
script_dir = Path(script_name).resolve().parent
city_centers = ['Karachi, Pakistan', 'Lahore, Pakistan']



def main():
    pass




if __name__ == "__main__":
    python_version = sys.version_info

    if python_version < (3, 10):
        print(f'Python version {python_version} is not supported. Please use Python 3.10 or later.')
        sys.exit(1)

    main()