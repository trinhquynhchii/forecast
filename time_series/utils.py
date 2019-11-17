import os
import pandas as pd


def split_to_region(city_id):
    """
    Assign city to region
    :param city_id: city id
    :return: region the city belong
    """
    if int(city_id) in range(38):
        return 'Kho Hà Nội'
    elif int(city_id) in range(38, 69):
        return 'Kho Đà Nẵng'
    else:
        return 'Kho Bình Dương'


def export_to_excel(df, filename, report_dir, sheet_name, start_date, end_date):
    start_date = start_date.strftime('%m%d')
    end_date = end_date.strftime('%m%d')

    filename = '{}_{}_{}.xlsx'.format(filename, start_date, end_date)
    filepath = os.path.join(report_dir, filename)

    df.to_excel(filepath, index=False, sheet_name=sheet_name)


def preprocess_data(data):
    data['created_at'] = pd.to_datetime(data['created_at'].dt.strftime('%Y-%m-%d'))
    data['Kho'] = data['shipping_city_id'].apply(split_to_region)

    data = data.drop(['shipping_city_id'], axis=1)
    data = data.rename(
        columns={'order_id': 'order_sn', 'sku_id': 'sku', 'sku_name': 'name', 'quantity_order': 'quantity',
                 'shipping_city_name': 'state',
                 'brand_name': 'brand'}
    )
    data = data.reindex(['created_at', 'order_sn', 'name', 'sku', 'quantity',
                         'state', 'brand', 'Kho'], axis=1)

    return data
