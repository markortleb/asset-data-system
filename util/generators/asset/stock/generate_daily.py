import argparse
import csv
import os
import errno
from jinja2 import Template


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r',
        '--repo-path',
        dest='repo_path',
        required=True,
        help='Path to repo'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def main():
    args = ARGS
    repo_path = os.path.dirname(args.repo_path)

    ticker_symbols_file_name = 'ticker_symbols.csv'
    ticker_symbols = []

    with open(ticker_symbols_file_name) as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            ticker_symbols.append(row[0])

    for ticker_symbol in ticker_symbols:
        template_args = {
            'etl_name': f'asset_stock_{ticker_symbol.lower()}_daily',
            'etl_path': f'asset/stock/{ticker_symbol.lower()}/daily',
            'ticker_symbol': ticker_symbol
        }

        output_file_path = f'{repo_path}/etl/' + template_args['etl_path'] + '/config.yml'
        if not os.path.exists(os.path.dirname(output_file_path)):
            try:
                os.makedirs(os.path.dirname(output_file_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open('templates/config_template_1.yml', 'r') as template_file:
            config_template = Template(template_file.read())
            out_string = config_template.render(template_args)
            with open(os.path.expanduser(output_file_path), 'w+') as out_file:
                    out_file.write(out_string)
            
        



main()
