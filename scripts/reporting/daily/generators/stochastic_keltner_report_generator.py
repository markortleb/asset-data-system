import os
import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpl
import ta
import reader


def stochastic_keltner_report_generator(ticker_symbol):
    matplotlib.use('agg')
    ticker_df = reader.get_yahoo_daily_df(ticker_symbol)
    ticker_reports_dir = f'{os.environ["PROJECT_PATH"]}/reports/{ticker_symbol.lower()}'
    os.makedirs(ticker_reports_dir, exist_ok=True)
    
    keltner_channel = ta.volatility.KeltnerChannel(
        high=ticker_df['High'],
        low=ticker_df['Low'],
        close=ticker_df['Close']
    )

    keltner_channel_hband = keltner_channel.keltner_channel_hband()
    keltner_channel_mband = keltner_channel.keltner_channel_mband()
    keltner_channel_lband = keltner_channel.keltner_channel_lband()

    keltner_channel_mband_plot = mpl.make_addplot(keltner_channel_mband)
    keltner_channel_lband_plot = mpl.make_addplot(keltner_channel_lband)
    keltner_channel_hband_plot = mpl.make_addplot(keltner_channel_hband)

    stochastic_oscillator_df = ta.momentum.StochasticOscillator(
        high=ticker_df['High'],
        low=ticker_df['Low'],
        close=ticker_df['Close'],
        window=14
    ).stoch()
    stochastic_oscillator_plot = mpl.make_addplot(stochastic_oscillator_df, panel='lower')

    # Get 3 Plot
    stochastic_sma_3_df = ta.momentum.StochasticOscillator(
        high=ticker_df['High'],
        low=ticker_df['Low'],
        close=ticker_df['Close'],
        window=14,
        smooth_window=3
    ).stoch_signal()

    stochastic_sma_3_plot = mpl.make_addplot(stochastic_sma_3_df, panel='lower')
    mpl.plot(
        ticker_df,
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[
            stochastic_oscillator_plot, 
            stochastic_sma_3_plot,
            keltner_channel_mband_plot,
            keltner_channel_hband_plot,
            keltner_channel_lband_plot
        ], 
        savefig=f'{ticker_reports_dir}/keltner_channel_with_stochastic_oscillator__smoothed_3.svg',
        figscale=1.2,
        closefig=True
    )

    # Get 6 Plot
    stochastic_sma_6_df = ta.momentum.StochasticOscillator(
        high=ticker_df['High'],
        low=ticker_df['Low'],
        close=ticker_df['Close'],
        window=14,
        smooth_window=6
    ).stoch_signal()

    stochastic_sma_6_plot = mpl.make_addplot(stochastic_sma_6_df, panel='lower')
    mpl.plot(
        ticker_df,
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[
            stochastic_oscillator_plot, 
            stochastic_sma_6_plot,
            keltner_channel_mband_plot,
            keltner_channel_hband_plot,
            keltner_channel_lband_plot
        ], 
        savefig=f'{ticker_reports_dir}/keltner_channel_with_stochastic_oscillator__smoothed_6.svg',
        figscale=1.2,
        closefig=True
    )

    # Get 9 Plot
    stochastic_sma_9_df = ta.momentum.StochasticOscillator(
        high=ticker_df['High'],
        low=ticker_df['Low'],
        close=ticker_df['Close'],
        window=14,
        smooth_window=9
    ).stoch_signal()

    stochastic_sma_9_plot = mpl.make_addplot(stochastic_sma_9_df, panel='lower')
    mpl.plot(
        ticker_df,
        type='candle', 
        volume=True, 
        style='yahoo', 
        addplot=[
            stochastic_oscillator_plot, 
            stochastic_sma_9_plot,
            keltner_channel_mband_plot,
            keltner_channel_hband_plot,
            keltner_channel_lband_plot
        ], 
        savefig=f'{ticker_reports_dir}/keltner_channel_with_stochastic_oscillator__smoothed_9.svg',
        figscale=1.2,
        closefig=True
    )
