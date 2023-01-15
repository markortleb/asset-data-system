import argparse
import generators


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--ticker-symbol',
        dest='ticker_symbol',
        required=True,
        help='Ticker symbol to generate report for.'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def main():
    args = ARGS
    ticker_symbol = args.ticker_symbol

    generators.ema_14_generator(ticker_symbol)
    generators.macd_report_generator(ticker_symbol)
    generators.on_balance_volume_report_generator(ticker_symbol)
    generators.sma_5_10_generator(ticker_symbol)
    generators.sma_high_low_generator(ticker_symbol)
    generators.stochastic_bollinger_report_generator(ticker_symbol)
    generators.stochastic_keltner_report_generator(ticker_symbol)


if __name__ == '__main__':
    main()
