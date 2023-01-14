import argparse
import yaml
from shutil import copyfile
import os
import errno
from jinja2 import Template
import subprocess


def get_task_list(search_path):
    task_list = []

    for root, directories, filenames in os.walk(search_path):
        for filename in filenames:
            task_file_path = (os.path.join(root, filename))
            if task_file_path.split('.')[-1] == 'yml':
                task_list.append(task_file_path)

    task_list.sort()
    return task_list


def submit_task(task_path):
    with open(task_path, 'r') as f:
        config = yaml.safe_load(f)['config']

        crontab_remove_cmd = f'crontab -l | grep -v \'{config["bash_command"]}\'  | crontab -'
        print(f'Running: {crontab_remove_cmd}')
        proc = subprocess.Popen(crontab_remove_cmd, shell=True)
        proc.wait()

        for schedule in config['schedules']:
            crontab_add_cmd = f'(crontab -l; echo "{schedule} {config["bash_command"]}") | crontab -'
            print(f'Running: {crontab_add_cmd}')
            proc = subprocess.Popen(crontab_add_cmd, shell=True)
            proc.wait()
    

def main():
    task_list = get_task_list(f'{os.environ["PROJECT_PATH"]}/tasks/')
    
    for task_path in task_list:
        # submit_task(task_path)
        print(task_path)


main()
