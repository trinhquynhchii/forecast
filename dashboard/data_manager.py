import os
import math
import numpy as np
import pandas as pd

from time_series.models.AutoArima import AutoARIMA
from time_series.safety_stock import SafetyStock
from time_series.data_manager import DataManager


class DashboardDataManager:
    def __init__(self, data_file_name=None, data_dir=None, report_dir=None, pre_forecasted=False):
        self.data_manager = DataManager(data_file_name=data_file_name, data_dir=data_dir)
        self.df = self.data_manager.df.set_index('created_at')
        self.df_by_day, self.df_by_week, self.df_by_month, self.df_by_weekday = self.data_manager.aggregate_data()

        self.pre_forecasted = pre_forecasted
        if not self.pre_forecasted:
            self.models = {}
            for warehouse in self.df_by_day.columns:
                model = AutoARIMA(self.df_by_day, warehouse, None)
                self.models[warehouse] = model
        else:
            self.forecast_df = {}
            # for period in ['1_day', '7_day', '14_day', '30_day']:
            for period in ['7_day', '14_day', '30_day']:
                filename = f'forecast_{period}.csv'
                filepath = os.path.join(self.data_manager.data_dir, filename)
                df = pd.read_csv(filepath)
                df = df.rename({df.columns[0]: 'created_at'}, axis=1)
                df = df.set_index('created_at')
                self.forecast_df[period] = df

        self.safety_stock = SafetyStock(data_file_name, data_dir, report_dir)

    def get_max_date(self):
        return self.df_by_day.index.max().to_pydatetime()

    def get_min_date(self):
        return self.df_by_day.index.min().to_pydatetime()

    def calculate_safety_stock(self, period, export_excel=False):
        return self.safety_stock.compute_safety_stock(period, export_excel)

    def forecast(self, warehouse, period):
        if not self.pre_forecasted:
            return self.models[warehouse].forecast(period)
        else:
            period = f'{period}_day'
            df = self.forecast_df[period]
            # print(df.columns)
            fc = df[warehouse]
            fc = fc.apply(lambda x: math.ceil(x))
            lower_limit = df[f'{warehouse}_lower_limit'].values.reshape((-1, 1))
            upper_limit = df[f'{warehouse}_upper_limit'].values.reshape((-1, 1))
            conf_int = np.hstack((lower_limit, upper_limit))
            return fc, conf_int
