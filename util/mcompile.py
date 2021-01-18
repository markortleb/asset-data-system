import argparse
import yaml
from shutil import copyfile
import os
import errno
from jinja2 import Template


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--in-repo-config-path',
        dest='in_repo_config_path',
        required=True,
        help='In-Repo Config Path'
    )
    parser.add_argument(
        '-r',
        '--repo-path',
        dest='repo_path',
        required=True,
        help='Path to config.yml that user wants to compile'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def generate_associated_files(associated_files, repo_path, config_path):
    templates_path = repo_path + '/util/templates'
    for associated_file in associated_files:
        if 'file_template' in associated_file:
            file_template = associated_file['file_template'].replace('<template>', templates_path)
            dest_file = '/'.join(config_path.split('/')[:-1]) + '/' +associated_file['file_path']
            print(f'Copying File: {file_template} --> {dest_file}')
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            copyfile(file_template, dest_file)


def apply_step(step_config, repo_path, config_path):
    generate_associated_files(
        step_config['associated_files'], 
        repo_path,
        config_path
    )


def apply_config(config, repo_path, config_path):
    file_path = repo_path + '/' + config['table_name'].replace('_', '/')
    # if 'steps' in config:
    #     for step in config['steps']:
    #         apply_step(step, repo_path, config_path)
    if 'associated_files' in config:
        for associated_file in config['associated_files']:
            input_file_path = associated_file['file_template']
            if '<template>' in input_file_path:
                input_file_path = input_file_path.replace('<template>', f'{repo_path}/util/templates')
            
            output_file_path = associated_file['file_path']
            if '<airflow_path>' in output_file_path:
                output_file_path = output_file_path.replace('<airflow_path>', f'~/airflow')
            elif '<repo_path>' in output_file_path:
                output_file_path = output_file_path.replace('<repo_path>', f'{repo_path}')

            template_args = {}
            if 'template_args' in associated_file:
                template_args = associated_file['template_args']

            with open(os.path.expanduser(input_file_path), 'r') as in_file:
                in_file_template = Template(in_file.read())
                out_string = in_file_template.render(template_args)
                
                output_file_path = os.path.expanduser(output_file_path)
                output_dir = '/'.join(output_file_path.split('/')[:-1])

                if not os.path.exists(output_dir):
                    try:
                        os.makedirs(output_dir)
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

                with open(output_file_path, 'w+') as out_file:
                    out_file.write(out_string)


def main():
    # python3 util/mcompile.py -c /etl/asset/stock/aapl/daily/config.yml -r ~/Repos/asset_data_system
    args = ARGS
    in_repo_config_path = args.in_repo_config_path
    repo_path = args.repo_path
    config_path = repo_path + in_repo_config_path
    
    with open(config_path, 'r') as stream:
        try:
            apply_config(yaml.safe_load(stream)['config'], repo_path, config_path)
        except yaml.YAMLError as exc:
            print(exc)


main()
