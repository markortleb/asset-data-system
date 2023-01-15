import os
import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpl
import ta
import reader


def sma_5_10_generator(ticker_symbol):
    matplotlib.use('agg')
    ticker_df = reader.get_yahoo_daily_df(ticker_symbol)
    ticker_reports_dir = f'{os.environ["PROJECT_PATH"]}/reports/{ticker_symbol.lower()}'
    os.makedirs(ticker_reports_dir, exist_ok=True)

    # 5 Day and 10 Day SMA
    sma_5_df = ta.trend.SMAIndicator(ticker_df['Close'], window=5).sma_indicator().to_frame()
    sma_5_plot = mpl.make_addplot(sma_5_df['sma_5'])

    sma_10_df = ta.trend.SMAIndicator(ticker_df['Close'], window=10).sma_indicator().to_frame()
    sma_10_plot = mpl.make_addplot(sma_10_df['sma_10'])

    mpl.plot(
        ticker_df, 
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[sma_5_plot, sma_10_plot],
        savefig=f'{ticker_reports_dir}/sma__windows_5_10.svg',
        closefig=True
    )
