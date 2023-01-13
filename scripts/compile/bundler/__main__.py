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


def write_task_yml(output_file_path, template_file_name, template_args):
    with open(f'{os.path.dirname(__file__)}/templates/{template_file_name}', 'r') as template_file:
        config_template = Template(template_file.read())
        out_string = config_template.render(template_args)
        with safe_open_w(output_file_path) as out_file:
            out_file.write(out_string)


def bundle_template_file(template_file_name):
    ticker_symbols_file_name = 'selected_ticker_symbols.txt'
    ticker_symbols = file_to_array(ticker_symbols_file_name)

    for ticker_symbol in ticker_symbols:
        etl_name = f'{ticker_symbol.lower()}_daily_etl'
        rendered_file_name = '.'.join(template_file_name.split('.')[:-1])
        output_file_path = f'{os.environ["PROJECT_PATH"]}/tasks/{ticker_symbol.lower()}/{rendered_file_name}'

        write_task_yml(
            output_file_path,
            template_file_name,
            {
                'etl_name': etl_name,
                'ticker_symbol': ticker_symbol
            }
        )


def main():
    for template_file_name in os.listdir(f'{os.path.dirname(__file__)}/templates/'):
        if template_file_name.split('.')[-1] == 'template':
            bundle_template_file(template_file_name)


if __name__ == "__main__":
    main()
