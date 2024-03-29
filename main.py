import os
import sys
import platform
import argparse
from utils.proscheduler import Proscheduler 
from utils.taskmanager import WindowsTasks, CronJobs
from utils.customui import sanitised_input

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
script_dir = os.fspath(__file__).rsplit(os.sep, 1)[0]
script_name = "main.py"
userfile_name = "user_input.txt"
city_centers = ['Karachi, Pakistan', 'Lahore, Pakistan']

class UserInput:
    def __init__(self):
        pass
    
    def userfile(self):
        try:
            with open(os.path.join(script_dir, userfile_name), "r") as file:
                # If file exists, read values from it
                exam_name, month_year, selected_city_indices, start_date, end_date= file.read().split(',')
                print("Values loaded from previous session file user_input.txt.")
        except FileNotFoundError:
            # If file doesn't exist, prompt user for input
            exam_name = sanitised_input("Enter exam name (STEP1/STEP2): ", str.upper, range_=('STEP1', 'STEP2'))
            month_year = sanitised_input("Enter month and year (03 2024): ", str, length_=7)

            # Display available cities to the user and prompt for selection
            print("Available cities:")
            for index, city in enumerate(city_centers, start=1):
                print(f"{index}. {city}")

            # input for cities
            selected_city_indices = sanitised_input("Enter the numbers corresponding to the cities you want to check (separated by space): ", str, range_=('1', '2', '1 2')) or '1 2'

            start_date = sanitised_input("Enter start date (1): ", int, 1, 31)
            end_date = sanitised_input("Enter end date (31): ", int, 1, 31)

            self.create_schedule(operating_system)

            # Write input values to file for later use
            with open(os.path.join(script_dir, userfile_name), "w") as file:
                file.write(f"{exam_name},{month_year},{selected_city_indices},{start_date},{end_date}")
                print("Values stored for later use in user_input.txt.")
        return exam_name, month_year, selected_city_indices, start_date, end_date

    def create_schedule(self, operating_system):
            if (operating_system == "Linux" or operating_system == "Darwin"):
                print("")
                print("\033[33mWarning! This will delete all other cronjobs\033[0m")
                schedule_task = sanitised_input("Schedule script to run automatically(yes/no): ", str.lower, range_=('yes', 'no'))    
                if schedule_task == "yes":
                    print("")
                    print("------------------------------------------------------------")
                    print("Input crontab entry. e.g (*/30 * * * *) will run script every 30 minutes")
                    print("\033[94mfor more info visit https://crontab.guru website\033[0m")
                    print("------------------------------------------------------------")
                    schedule = input("how frequently you want to run script?: ")
                    print("")

                    # create a schedule using crontab
                    cron = CronJobs()
                    cron.delete()
                    cron.create(operating_system, schedule, script_dir, script_name)

            if (operating_system == "Windows"):
                schedule_task = sanitised_input("Schedule script to run automatically(yes/no): ", str.lower, range_=('yes', 'no'))
                if schedule_task == "yes":
                    print("")
                    print("------------------------------------------------------")
                    print("for example, To run script after every 30 minutes input 30")
                    schedule = sanitised_input("Input number of minutes (30): ", int, 5)

                    # create task on windows
                    tasks = WindowsTasks()
                    if not tasks.exists(task_name):
                        tasks.create(task_name, script_dir, script_name, schedule)
                    else:
                        tasks.delete(task_name)
                        tasks.create(task_name, script_dir, script_name, schedule)

            



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

    if python_version < (3, 6):
        print(f'Python version {python_version} is not supported. Please use Python 3.6 or later.')
        sys.exit(1)

    main()