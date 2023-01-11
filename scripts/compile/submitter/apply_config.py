import argparse
import yaml
from shutil import copyfile
import os
import errno
from jinja2 import Template
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--search-path',
        dest='search_path',
        required=True,
        help='Search for all config.yml in this directory'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def get_config_list(search_path):
    config_list = []

    for root, directories, filenames in os.walk(search_path):
        for filename in filenames:
            config_file_path = (os.path.join(root,filename))
            if config_file_path.split('/')[-1] == 'config.yml':
                config_list.append(config_file_path)

    config_list.sort()
    return config_list


def apply_config(config_path):
    with open(config_path, 'r+') as f:
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
    args = ARGS
    search_path = os.path.expanduser(args.search_path)
    config_list = get_config_list(search_path)
    
    for config_path in config_list:
        apply_config(config_path)


main()
