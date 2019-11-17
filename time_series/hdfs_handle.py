import datalabframework as dlf
import pyspark.sql.functions as F
import pyspark.sql.types as T

from .utils import split_to_region, preprocess_data


class HDFSHandler:
    def __init__(self):
        self.dlf_pro = dlf.project
        self.dlf_pro.load()
        self.engine = self.dlf_pro.engine()
        self.spark = self.engine.context()

    def get_transaction_data(self, date=None):
        transaction_fact = self.engine.load('seller_id=2')
        cols = ['order_id', 'created_at', 'shipping_city_id', 'shipping_city_name',
                'sku_id', 'sku_name', 'brand_name', 'quantity_order']
        # udf_split_to_region = F.udf(split_to_region, T.StringType())
        data_pyspark = transaction_fact.select(cols) \
            .where('order_status == "SUCCESS" or order_status == "DRAFT"') \
            .where('cat_root_name == "Tã - Bỉm"') \
            .where('payment_status != "DA_HOAN_TIEN" and payment_status != "CHO_THANH_TOAN"') \
            .distinct() \
            # .withColumn('Kho', udf_split_to_region('shipping_city_id'))

        if date is not None:
            start_date, end_date = date
            data_pyspark = data_pyspark.where(F.col('created_at').between(start_date, end_date))

        return preprocess_data(data_pyspark.toPandas())

    def save_safety_stock_fact(self, df):
        safety_stock = self.engine.load('total_sale_forecast')
        df = self.spark.createDataFrame(df)
        safety_stock_df = safety_stock.union(df)
        self.engine.save(safety_stock_df, path='safety_stock', provider='output_fact', mode='overwrite')

    def save_sale_forecast_fact(self, df):
        sale_forecast = self.engine.load('total_sale_forecast')
        df = self.spark.createDataFrame(df)
        sale_forecast_df = sale_forecast.union(df)
        self.engine.save(sale_forecast_df, path='total_sale_forecast', provider='output_fact', mode='overwrite')
