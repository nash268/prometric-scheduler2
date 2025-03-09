import platform
import subprocess
import os
from pathlib import Path

operating_system = platform.system()

class TaskManager:
    def __init__(self):
        pass

    def task_status(self, task_name: str):
        if operating_system == "Windows":
            query_command = f'schtasks /query /tn "{task_name}"'
            result = subprocess.run(query_command, shell=True, capture_output=True, text=True)
            return task_name in result.stdout

        elif operating_system in {"Linux", "Darwin"}:
            query_command = f'crontab -l 2>/dev/null | grep "{task_name}"'
            result = subprocess.run(query_command, shell=True, capture_output=True, text=True)
            return task_name in result.stdout

        return False

    def delete_task(self, task_name: str):
        if operating_system == "Windows":
            command = f'schtasks /delete /tn "{task_name}" /f'
        elif operating_system in {"Linux", "Darwin"}:
            command = f'crontab -l 2>/dev/null | grep -v "{task_name}" | crontab -'
        else:
            return
        
        subprocess.run(command, shell=True, check=True)

    def create_task(self, task_name: str, schedule: str, script_path: Path):
        script_dir = script_path.parent
        script_name = script_path.name

        if operating_system == "Windows":
            command = (
                f'schtasks /create /sc minute /mo {schedule} /tn "{task_name}" '
                f'/tr "cmd /c cd /d {script_dir} && py {script_name}" /f'
            )

        elif operating_system == "Linux":
            os.environ["DISPLAY"] = os.environ.get("DISPLAY", ":0")
            cron_command = f'{schedule} export DISPLAY={os.environ["DISPLAY"]}; cd {script_dir} && python3 {script_name} >> {script_dir}/logfile 2>&1'
            command = f'(crontab -l 2>/dev/null; echo "{cron_command}") | crontab -'

        elif operating_system == "Darwin":
            cron_command = f'{schedule} cd {script_dir} && python3 {script_name} >> {script_dir}/logfile 2>&1'
            command = f'(crontab -l 2>/dev/null; echo "{cron_command}") | crontab -'

        else:
            return

        subprocess.run(command, shell=True, check=True)