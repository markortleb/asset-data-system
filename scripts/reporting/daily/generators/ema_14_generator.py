import os
import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpl
import ta
import reader


def ema_14_generator(ticker_symbol):
    matplotlib.use('agg')
    ticker_df = reader.get_yahoo_daily_df(ticker_symbol)
    ticker_reports_dir = f'{os.environ["PROJECT_PATH"]}/reports/{ticker_symbol.lower()}'
    os.makedirs(ticker_reports_dir, exist_ok=True)

    ema_14_df = ta.trend.EMAIndicator(ticker_df['Close']).ema_indicator().to_frame()
    ema_14_plot = mpl.make_addplot(ema_14_df['ema_14'])

    mpl.plot(
        ticker_df, 
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[ema_14_plot], 
        savefig=f'{ticker_reports_dir}/ema__window_14.svg',
        closefig=True
    )
