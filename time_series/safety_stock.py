import pandas as pd
import numpy as np
import os
import math

from .utils import export_to_excel
from time_series.data_manager import DataManager

os.environ['PYSPARK_PYTHON'] = '/opt/conda/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/opt/conda/bin/python'


class SafetyStock:
    def __init__(self, data_file_name=None, data_dir=None, report_dir=None):
        """
        Class to calculate safety stock from pandas DataFrame
        :param data_dir: data folder, contains old data file, lead_time csv files
        :param report_dir: reports folder, contains report files (excel, figures, etc.)
        """
        if data_dir is not None:
            self.data_dir = data_dir
        else:
            self.data_dir = os.path.join(os.path.split(os.getcwd())[0], 'data')

        if report_dir is not None:
            self.report_dir = report_dir
        else:
            self.report_dir = os.path.join(os.path.split(os.getcwd())[0], 'reports')

        self.data_manager = DataManager(data_file_name=data_file_name, data_dir=data_dir)

        self.max_lead_time = pd.read_csv(os.path.join(self.data_dir, 'max_lead_time.csv')).set_index('city')
        self.avg_lead_time = pd.read_csv(os.path.join(self.data_dir, 'avg_lead_time.csv')).set_index('city')

    def compute_safety_stock(self, period, export_excel=True):
        """
        Aggregate data from a DataFrame to produce a safety stock table
        :param period: Period of time to compute safety stock
        :param export_excel: if True, export an excel file with name "safety_stock_{start_date}_{end_date}.xlsx"
        :return: safety stock DataFrame
        """
        df = self.data_manager.filter_data_by_date(period)

        data = df.groupby(['Kho', 'sku', 'name'], as_index=False)['quantity'].sum()
        data = data.rename(columns={'quantity': 'total_sale'})
        data['percentage'] = data.apply(self.__compute_sku_percentage, df=data, axis=1)

        start_date = df['created_at'].min()
        end_date = df['created_at'].max()
        time_range = pd.Timedelta(end_date - start_date).days

        data['avg_sale'] = data['total_sale'] / time_range
        data['max_sale'] = data.apply(self.__get_max_sale, df=df, axis=1)

        data['safety_stock_hanoi'] = data.apply(self.__compute_safety_stock_by_warehouse,
                                                src='Hà Nội',
                                                axis=1)
        data['safety_stock_danang'] = data.apply(self.__compute_safety_stock_by_warehouse,
                                                 src='Đà Nẵng',
                                                 axis=1)
        data['safety_stock_binhduong'] = data.apply(self.__compute_safety_stock_by_warehouse,
                                                    src='Bình Dương',
                                                    axis=1)

        data = data.sort_values(['Kho', 'total_sale'], ascending=[False, False])

        start_period, end_period = period
        data['period'] = [f'{start_period} - {end_period}'] * len(data)
        data = data.reset_index(drop=True)

        if export_excel:
            export_to_excel(data, 'safety_stock', self.report_dir, 'safety_stock', start_date, end_date)
        return data

    def __get_sku_data(self, df, sku, warehouse):
        """
        Get total sale of sku from a DataFrame each day, sort by day
        :param df: Transaction DataFrame
        :param sku: sku id
        :param warehouse: warehouse name
        :return: series of total sale of sku each day, sort by day
        """
        idx = (df['sku'] == sku) & (df['Kho'] == warehouse)
        data = df.loc[idx, ['created_at', 'quantity']].set_index('created_at').resample('D').sum()
        return data

    def __get_max_sale(self, row, df):
        """
        Get max sale of a specific sku from a specific warehouse, use IQR to detect outlier
        :param row: contains sku and warehouse
        :param df: Transaction DataFrame
        :return: max sale of a specific sku from a specific warehouse
        """
        # row = row.tolist()
        quantity = self.__get_sku_data(df, row['sku'], row['Kho'])
        q25 = quantity.quantile(0.25)
        q75 = quantity.quantile(0.75)
        iqr = q75 - q25
        upper_limit = q75 + 1.5 * iqr

        max_sale = quantity[(quantity < upper_limit) & (quantity > row['avg_sale'])].max().values[0]
        if math.isnan(max_sale) or max_sale == 0:
            max_sale = quantity.max().values[0]
        return max_sale

    def __compute_sku_percentage(self, row, df):
        same_warehouse_sale = df.loc[df['Kho'] == row['Kho'], :]
        total_sale_per_warehouse = same_warehouse_sale['total_sale'].sum()
        return row['total_sale'] / total_sale_per_warehouse * 100

    def __compute_safety_stock_by_warehouse(self, row, src):
        """
        Get safety stock data
        :param row: aggregated sale Series (Kho, sku, sales info)
        :param src: origin warehouse
        :return: safety stock needed from origin warehouse
        """
        dest = row['Kho'].replace('Kho ', '')
        max_lead_time = float(self.max_lead_time.loc[src, dest])
        avg_lead_time = float(self.avg_lead_time.loc[src, dest])
        return int(row['max_sale'] * max_lead_time - row['avg_sale'] * avg_lead_time)
