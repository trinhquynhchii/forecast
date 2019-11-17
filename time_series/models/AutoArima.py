import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pmdarima as pm


class AutoARIMA:
    def __init__(self, df, target_col, cfg):
        self.df = df
        self.target_col = target_col
        # TODO: create cfg class
        self.model = pm.auto_arima(df[target_col].values, start_p=1, start_q=1,
                                   test='adf',  # use adftest to find optimal 'd'
                                   max_p=7, max_q=3,  # maximum p and q
                                   d=None,  # let model determine 'd'
                                   seasonal=True,
                                   start_P=0,
                                   m=7,  # weekly seasonality
                                   D=0,
                                   trace=True,
                                   error_action='ignore',
                                   suppress_warnings=True,
                                   stepwise=True)

        print(self.model.summary())

    def forecast(self, period):
        fc, conf_int = self.model.predict(n_periods=period, return_conf_int=True)
        fc = np.ceil(fc)
        return fc, conf_int

    def plot_diagnostic(self):
        self.model.plot_diagnostics(figsize=(20, 8))
        plt.show()

    def plot_forecast(self, period, forecast, conf_int, actual_df=None, title='Sale Forecast'):
#         index_of_fc = np.arange(len(self.df[self.target_col].values), len(self.df[self.target_col].values) + period)
        index_of_fc = []
        for day in range(period):
            time_shift = pd.to_timedelta(day + 1, unit='D')
            index_of_fc.append(self.df.index[-1] + time_shift)

        fc_series = pd.Series(forecast, index=index_of_fc)
        lower_series = pd.Series(conf_int[:, 0], index=index_of_fc)
        upper_series = pd.Series(conf_int[:, 1], index=index_of_fc)

        # Plot
        sns.set(rc={'figure.figsize': (20, 8)})

        plt.plot(self.df[self.target_col])
        if actual_df is not None:
            plt.plot(actual_df[self.target_col])
        plt.plot(fc_series, color='darkgreen')
        plt.fill_between(lower_series.index,
                         lower_series,
                         upper_series,
                         color='k', alpha=.15)

        plt.title(title)
        plt.show()
