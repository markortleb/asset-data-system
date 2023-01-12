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

    ticker_symbols_file_name = 'selected_ticker_symbols.txt'

    with open(ticker_symbols_file_name) as f:
        ticker_symbols_string = f.read()

    ticker_symbols = ticker_symbols_string.split('\n')

    for ticker_symbol in ticker_symbols:
        template_args = {
            'etl_name': f'asset_stock_{ticker_symbol.lower()}_daily',
            'ticker_symbol': ticker_symbol,
            'repo_path': repo_path
        }

        output_file_path = f'{repo_path}/etl/asset/stock/{ticker_symbol.lower()}/daily/config.yml'
        output_dir = '/'.join(output_file_path.split('/')[:-1]) + '/'
        if not os.path.exists(os.path.dirname(output_dir)):
            try:
                os.makedirs(os.path.dirname(output_dir))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        print(output_dir)

        with open('templates/config_template_daily.yml', 'r') as template_file:
            config_template = Template(template_file.read())
            out_string = config_template.render(template_args)
            with open(os.path.expanduser(output_file_path), 'w+') as out_file:
                    out_file.write(out_string)


main()
