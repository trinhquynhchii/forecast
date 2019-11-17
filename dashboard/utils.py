import math


# Display big numbers in readable format
def human_format(num):
    try:
        num = float(num)
        # If value is 0
        if num == 0:
            return 0
        # Else value is a number
        if num < 1000000:
            return num
        magnitude = int(math.log(num, 1000))
        mantissa = str(int(num / (1000 ** magnitude)))
        return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]
    except:
        return num


def clean_safety_stock_df(df):
    dff = df.copy(deep=True)
    dff.columns = ['SKU', 'Name', 'Total Sale', 'Percentage', 'Average Sale', 'Max Sale',
                   'In Hà Nội', 'In Đà Nẵng', 'In Bình Dương', 'Predict Sale']
    dff['Percentage'] = dff['Percentage'].map('{:,.2f}%'.format)
    dff['Average Sale'] = dff['Average Sale'].map('{:,.2f}'.format)
    return dff
