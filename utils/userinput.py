from utils.customui import sanitised_input
from utils.taskmanager import WindowsTasks, CronJobs


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