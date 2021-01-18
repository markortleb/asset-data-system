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
        '-r',
        '--repo-path',
        dest='repo_path',
        required=True,
        help='Path to config.yml that user wants to compile'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def main():
  args = ARGS
  repo_path = os.path.expanduser(args.repo_path)

  config_list = []

  for root, directories, filenames in os.walk(repo_path):
    for filename in filenames:
      config_file_path = (os.path.join(root,filename))
      if config_file_path.split('/')[-1] == 'config.yml':
        config_list.append(config_file_path)

  for config in config_list:
    in_repo_config_path = config.replace(repo_path, '')
    cmd = f'python3 {repo_path}/util/mcompile.py --in-repo-config-path {in_repo_config_path} --repo-path {repo_path}'
    print(f'Running: {cmd}')
    proc = subprocess.Popen(cmd.split(' '))
    proc.wait()



main()
