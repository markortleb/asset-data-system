import argparse
import csv
import os
import errno
from jinja2 import Template


def file_to_array(file_name):
    with open(file_name) as f:
        f_string = f.read()
    return f_string.split('\n')


def safe_open_w(path):
    # Open "path" for writing, creating any parent directories as needed.
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


def write_task_yml(output_file_path, template_args):
    with open(f'{os.path.dirname(__file__)}/templates/config_template_daily.yml', 'r') as template_file:
        config_template = Template(template_file.read())
        out_string = config_template.render(template_args)
        with safe_open_w(output_file_path) as out_file:
            out_file.write(out_string)


def main():
    ticker_symbols_file_name = 'selected_ticker_symbols.txt'
    ticker_symbols = file_to_array(ticker_symbols_file_name)

    for ticker_symbol in ticker_symbols:
        etl_name = f'{ticker_symbol.lower()}_daily_etl'
        output_file_path = f'{os.environ["PROJECT_PATH"]}/tasks/{ticker_symbol.lower()}/daily_etl.yml'
        # create_dir_for_file(output_file_path)

        write_task_yml(
            output_file_path,
            {
                'etl_name': etl_name,
                'ticker_symbol': ticker_symbol
            }
        )


main()
