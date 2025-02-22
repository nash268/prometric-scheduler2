import platform
import subprocess

class TaskManager:
    def __init__(self):
        pass

    def task_status(self, task_name):
        if (platform.system() == "Windows"):
            # Command to query existing tasks
            query_command = f'schtasks /query /tn "{task_name}"'
            
            # Execute the command and capture the output
            result = subprocess.run(query_command, shell=True, capture_output=True, text=True)

            # Return True if task name is found in the output
            if (task_name in result.stdout):
                return True
            else:
                return False

        if (platform.system() == "Linux" or operating_system == "Darwin"):
            query_command = f'crontab -l | grep "{task_name}"'
            result = subprocess(query_command, shell=True, capture_output=True, text=True)
            if (task_name in result.stdout):
                return True
            else:
                return False

    def delete_task(self, task_name):
        if (platform.system() == "Windows"):
            # Command to delete the task on windows
            command = f'schtasks /delete /tn "{task_name}" /f'
            subprocess.run(command, shell=True)

        if (platform.system() == "Linux" or operating_system == "Darwin"):
            # list all tasks, removes line containing task name, rewrite crontab file.
            command = f'crontab -l | grep -v "{task_name}" | crontab -'
            subprocess.run(command, shell=True)

    def create_task(self, task_name, schedule, script_path):
        if (platform.system() == "Windows"):
            # Command to schedule the task
            command = f'schtasks /create /sc minute /mo {schedule} /tn "{task_name}" /tr "cmd /c cd /d {script_dir} && py {script_name}"'
            subprocess.run(command, shell=True)