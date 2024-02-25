# class for managing tasks on windows
class WindowsTasks:
    def __init__(self):
        pass

    def exists(self, task_name):
        # Command to query existing tasks
        query_command = f'schtasks /query /tn "{task_name}"'
        
        # Execute the command and capture the output
        result = subprocess.run(query_command, shell=True, capture_output=True, text=True)
        
        # Check if the task name is found in the output
        return task_name in result.stdout
    
    def delete(self, task_name):
        # Command to delete the task
        command = f'schtasks /delete /tn "{task_name}" /f'
        subprocess.run(command, shell=True)

    def create(self, task_name, schedule, script_path, script_name):
        
        # Command to schedule the task
        command = f'schtasks /create /sc minute /mo {schedule} /tn "{task_name}" /tr "cmd /c cd /d {script_path} && py {script_name}"'

        # Execute the command to create the task
        subprocess.run(command, shell=True)



class CronJobs:
    def __init__(self):
        pass

    def delete(self):
        # Command to remove the cron job
        delete_command = f'crontab -r'
        subprocess.run(delete_command, shell=True)
        print("SUCCESS: all previous cronjobs deleted.")

    def create(self, operating_system, schedule, script_path, script_name):
        if operating_system == "Linux":
            # for Linux, the DISPLAY environment variable is used for GUI applications.
            # Find the display value
            display = subprocess.check_output(["echo", "$DISPLAY"]).decode().strip()
            # command for setting up cronjob
            command = f'(echo "{schedule} export DISPLAY={display}; cd {script_path} && python3 {script_name} >> {script_path}/logfile 2>&1") | crontab -'

        elif operating_system == "Darwin":
            # cron jobs on macOS can work without setting the DISPLAY environment variable
            command = f'(echo "{schedule} cd {script_path} && python3 {script_name} >> {script_path}/logfile 2>&1") | crontab -'
            
        subprocess.run(command, shell=True)
        print("SUCCESS: prometric cronjob created successfully.")