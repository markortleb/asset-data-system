import os
import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpl
import ta
import reader


def on_balance_volume_report_generator(ticker_symbol):
    matplotlib.use('agg')
    ticker_df = reader.get_yahoo_daily_df(ticker_symbol)
    ticker_reports_dir = f'{os.environ["PROJECT_PATH"]}/reports/{ticker_symbol.lower()}'
    os.makedirs(ticker_reports_dir, exist_ok=True)

    on_balance_volume = ta.volume.OnBalanceVolumeIndicator(
        close=ticker_df['Close'],
        volume=ticker_df['Volume']
    ).on_balance_volume()

    obv_sma = ta.trend.SMAIndicator(
        close=on_balance_volume,
        window=20
    ).sma_indicator()

    obv_plot = mpl.make_addplot(on_balance_volume)
    obv_sma_plot = mpl.make_addplot(obv_sma)

    mpl.plot(
        ticker_df,
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[
            obv_plot,
            obv_sma_plot
        ], 
        savefig=f'{ticker_reports_dir}/on_balance_volume.svg',
        figscale=1.2,
        closefig=True
    )
