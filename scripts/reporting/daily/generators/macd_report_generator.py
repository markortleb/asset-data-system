import os
import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpl
import ta
import reader


def macd_report_generator(ticker_symbol):
    matplotlib.use('agg')
    ticker_df = reader.get_yahoo_daily_df(ticker_symbol)
    ticker_reports_dir = f'{os.environ["PROJECT_PATH"]}/reports/{ticker_symbol.lower()}'
    os.makedirs(ticker_reports_dir, exist_ok=True)

    macd_obj = ta.trend.MACD(
        close=ticker_df['Close']
    )

    macd = macd_obj.macd()
    macd_signal = macd_obj.macd_signal()

    macd_plot = mpl.make_addplot(macd, panel='lower')
    macd_signal_plot = mpl.make_addplot(macd_signal, panel='lower')

    mpl.plot(
        ticker_df, 
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[
            macd_plot,
            macd_signal_plot
        ], 
        savefig=f'{ticker_reports_dir}/macd.svg',
        figscale=1.2,
        closefig=True
    )

