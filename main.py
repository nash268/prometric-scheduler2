# imports from python modules
import os
import sys
import platform
import argparse
from pathlib import Path

# imports from my personal modules located in utils folder
from utils.proscheduler import Proscheduler 
from utils.userinput import UserInput

prometric_logo = """

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

print(prometric_logo)
print("Welcome to the Test Center Availability Checker!")
print("------------------------------------------------")
print("This script helps you check for available test center slots for your exam.")
print("You'll be prompted to provide some initial information, such as the exam name,")
print("month and year, and date range to search for available slots. Also how often")
print("you want to run script automatically.")
print("Once dates found it will play alert.mp3")
print("Let's get started!")
print("------------------------------------------------")

operating_system = platform.system()
script_name = __file__
script_dir = Path(script_name).resolve().parent
userfile_name = "user_input.txt"
city_centers = ['Karachi, Pakistan', 'Lahore, Pakistan']



def main():

    user_input = UserInput()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e',
        action='store_true',
        help='Edit user input file and create new schedule'
    )
    parser.add_argument(
        '-s',
        action='store_true',
        help='Create new schedule'
    )
    args = parser.parse_args()

    if args.e:
        if os.path.exists(os.path.join(script_dir, userfile_name)):
            os.remove(os.path.join(script_dir, userfile_name))
        user_input.userfile()
    if args.s: 
        user_input.create_schedule(operating_system)
        exit()


    # load values from user_input.txt file
    exam_name, month_year, selected_city_indices, start_date, end_date = user_input.userfile()
    selected_city_indices = [int(index) for index in selected_city_indices.split(' ')]
    selected_cities = [city_centers[index - 1] for index in selected_city_indices]


    # create Proscheduler instance
    ps = Proscheduler()
    ps.start()
    dates = ps.get_dates(exam_name, selected_cities, month_year)
    print(dates)
    ps.halt()






if __name__ == "__main__":
    python_version = sys.version_info

    if python_version < (3, 10):
        print(f'Python version {python_version} is not supported. Please use Python 3.10 or later.')
        sys.exit(1)

    main()