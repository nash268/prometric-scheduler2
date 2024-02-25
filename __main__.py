import os
import sys
import platform
import argparse
from proscheduler import Proscheduler 
from taskmanager import WindowsTasks, CronJobs
from customui import sanitised_input

class UserInput:
    def __init__(self):
        pass
    
    def userfile(self):
        try:
            with open("user_input.txt", "r") as file:
                # If file exists, read values from it
                exam_name, month_year, selected_city_indices, start_date, end_date= file.read().split(',')
                print("Values loaded from previous session file user_input.txt.")
        except FileNotFoundError:
            # If file doesn't exist, prompt user for input
            exam_name = sanitised_input("Enter exam name (STEP1/STEP2): ", str.upper, range_=('STEP1', 'STEP2'))
            month_year = sanitised_input("Enter month and year (3 2024): ", str)

            # Display available cities to the user and prompt for selection
            print("Available cities:")
            for index, city in enumerate(city_centers.keys(), start=1):
                print(f"{index}. {city}")

            # input for cities
            selected_city_indices = sanitised_input("Enter the numbers corresponding to the cities you want to check (separated by space): ", str, range_=('1', '2', '1 2')) or '1 2'

            start_date = sanitised_input("Enter start date (1): ", int, 1, 31)
            end_date = sanitised_input("Enter end date (31): ", int, 1, 31)

                # Write input values to file for later use
            with open("user_input.txt", "w") as file:
                file.write(f"{exam_name},{month_year},{selected_city_indices},{start_date},{end_date}")
                print("Values stored for later use in user_input.txt.")

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

            if (operating_system == "Windows"):
                schedule_task = sanitised_input("Schedule script to run automatically(yes/no): ", str.lower, range_=('yes', 'no'))
                if schedule_task == "yes":
                    print("")
                    print("------------------------------------------------------")
                    print("for example, To run script after every 30 minutes input 30")
                    schedule = sanitised_input("Input number of minutes (30): ", int, 5)
            return schedule


def main():

    operating_system = platform.system()
    script_path = os.getcwd()
    script_name = os.path.basename(script_path)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e',
        action='store_true',
        help='Edit user input file'
    )
    parser.add_argument(
        '-s',
        action='store_true',
        help='Create new schedule'
    )
    args = parser.parse_args()

    if args.e:
        user_input = UserInput()
        user_input.userfile()
    if args.s: 
        schedule = UserInput().create_schedule(operating_system)
        if operating_system == "Windows":
            task_name = "Prometric-Scheduler"
            tasks = WindowsTasks()
            if not tasks.task_exists():
                tasks.create_task(task_name, schedule, script_path, script_name)
            else:
                tasks.delete_task(task_name)
                tasks.create_task(task_name, schedule, script_path, script_name)

        if operating_system == "Linux" or operating_system == "Darwin":
            cron = CronJobs()
            cron.delete_job()
            cron.create_job(operating_system, schedule, script_path, script_name)


    # create Proscheduler instance
    ps = Proscheduler()
    ps.start()
    dates = ps.get_dates(exam_name, addresses, month_year)
    print(dates)
    ps.halt()






if __name__ == "__main__":
    python_version = sys.version.split()[0]

    if python_version < (3, 6):
        print(f'Python version {python_version} is not supported. Please use Python 3.6 or later.')
        sys.exit(1)

    main()