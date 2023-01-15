import os
import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpl
import ta
import reader


def sma_high_low_generator(ticker_symbol):
    matplotlib.use('agg')
    ticker_df = reader.get_yahoo_daily_df(ticker_symbol)
    ticker_reports_dir = f'{os.environ["PROJECT_PATH"]}/reports/{ticker_symbol.lower()}'
    os.makedirs(ticker_reports_dir, exist_ok=True)

    sma_low_df = ta.trend.SMAIndicator(ticker_df['Low'], window=5).sma_indicator()
    sma_low_plot = mpl.make_addplot(sma_low_df)

    sma_high_df = ta.trend.SMAIndicator(ticker_df['High'], window=5).sma_indicator()
    sma_high_plot = mpl.make_addplot(sma_high_df)

    mpl.plot(
        ticker_df, 
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[sma_low_plot, sma_high_plot],
        savefig=f'{ticker_reports_dir}/sma_high_low_channel__window_5.svg',
        closefig=True
    )
