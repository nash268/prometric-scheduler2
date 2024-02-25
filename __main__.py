from proscheduler import Proscheduler 
from taskmanager import WindowsTasks, CronJobs
from customui import print_progress_bar, sanitised_input

exam_name = 'STEP1'
addresses = ['Karachi, Pakistan', 'Lahore, Pakistan']
month_year = '06 2024'

ps = Proscheduler()
ps.start()
dates = ps.check_prometric(exam_name, addresses, month_year)
print(dates)
ps.halt()