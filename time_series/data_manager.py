import os
import pandas as pd


class DataManager:
    def __init__(self, data_file_name=None, data_dir=None):
        if data_dir is not None:
            self.data_dir = data_dir
        else:
            self.data_dir = os.path.join(os.path.split(os.getcwd())[0], 'data')

        if data_file_name is None:
            data_file_name = 'transaction_20191111.csv'
        fact_df_filepath = os.path.join(self.data_dir, data_file_name)

        self.excel_data = pd.read_excel(os.path.join(self.data_dir, 'vnshop_order.xlsx'), sheet_name=0)
        self.excel_data = self.excel_data.drop('shipping_address', axis=1)
        self.fact_df = pd.read_csv(fact_df_filepath)
        self.fact_df['created_at'] = pd.to_datetime(self.fact_df['created_at'])

        self.df = pd.concat([self.excel_data, self.fact_df])
        self.df = self.df.set_index('created_at').sort_values(by='created_at')['2018-11':].reset_index()

    def aggregate_data(self, df=None):
        if df is None:
            df = self.df
        df_sortdate = df.set_index('created_at').sort_values(by='created_at')

        def sort_by_warehouse(dff, warehouse):
            df_warehouse = dff[dff['Kho'] == warehouse]
            warehouse_name = warehouse.replace('Kho ', '')

            dfbymonth = df_warehouse.resample('M')['quantity'].sum().rename(warehouse_name)
            dfbyweek = df_warehouse.resample('W')['quantity'].sum().rename(warehouse_name)
            dfbyday = df_warehouse.resample('D')['quantity'].sum().rename(warehouse_name)

            return df_warehouse, dfbymonth, dfbyweek, dfbyday

        warehouse_list = df_sortdate['Kho'].unique().tolist()

        df_dict = {}
        df_by_day = []
        df_by_week = []
        df_by_month = []

        for warehouse in warehouse_list:
            df_dict[warehouse] = sort_by_warehouse(df_sortdate, warehouse)
            df_by_month.append(df_dict[warehouse][1])
            df_by_week.append(df_dict[warehouse][2])
            df_by_day.append(df_dict[warehouse][3])

        df_by_day = pd.concat(df_by_day, axis=1, join='inner')
        df_by_week = pd.concat(df_by_week, axis=1, join='inner')
        df_by_month = pd.concat(df_by_month, axis=1, join='inner')
        df_by_weekday = df_by_day.copy(deep=True)
        df_by_weekday['weekday'] = df_by_weekday.index.weekday_name

        return df_by_day, df_by_week, df_by_month, df_by_weekday

    def filter_data_by_date(self, period, df=None):
        start_date, end_date = period
        if df is None:
            df = self.df
        dff = df.set_index('created_at')[start_date:end_date].reset_index()
        return dff

    # Based on Cooks distance
    def filter_outlier(self, warehouse, windows=30, df=None):
        windows = f'{windows}D'
        df_by_day, _, _, _ = self.aggregate_data(df=df)
        series = df_by_day[warehouse]
        mean = series.rolling(window=windows, closed='neither').mean()
        std = series.rolling(window=windows, closed='neither').std()

        mean[mean.isna()] = series[mean.isna()]
        std[std.isna()] = 0

        upper_limit = mean + 3 * std

        violate_idx = series > upper_limit
        series[violate_idx] = mean[violate_idx]

        return series

    def filter_outlier_by_sku(self, warehouse, sku, windows=30, df=None):
        if df is None:
            df = self.df

        idx = df['sku'] == sku
        df = df.loc[idx, :]
        return self.filter_outlier(warehouse, windows, df=df)
