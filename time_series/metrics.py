import numpy as np
import pandas as pd


def calc_mse(y_pred, y_true):
    return np.mean(np.square(y_true - y_pred))


def calc_mae(y_pred, y_true):
    return np.mean(np.abs(y_true - y_pred))


def calc_mape(y_pred, y_true):
    y_true[y_true == 0] = 1
    return np.mean(np.abs(y_true - y_pred) / np.abs(y_true))


def calc_corr_error(y_pred, y_true):
    return np.corrcoef(y_pred, y_true)[0, 1]


def calc_min_max_error(y_pred, y_true):
    mins = np.amin(np.hstack([y_pred[:, None],
                              y_true[:, None]]), axis=1)
    maxs = np.amax(np.hstack([y_pred[:, None],
                              y_true[:, None]]), axis=1)

    return 1 - np.mean(mins / maxs)


def measure_error(preds, test_df, target_col):
    cols = ['date', 'actual', 'forecast']
    test_df = pd.DataFrame(test_df[target_col]).reset_index()

    y_pred = preds
    y_true = test_df[target_col].values

    mse = calc_mse(y_pred, y_true)
    mae = calc_mae(y_pred, y_true)
    mape = calc_mape(y_pred, y_true)
    corr = calc_corr_error(y_pred, y_true)
    minmax = calc_min_max_error(y_pred, y_true)

    result_df = test_df.copy(deep=True)
    result_df['pred'] = y_pred
    result_df.columns = cols

    error = {'Mean Squared Error': mse,
             'Mean Absolute Error': mae,
             'Mean Absolute Percentage Error': mape,
             'Correlation between forecast and actual values': corr,
             'Min-Max Error': minmax}

    return result_df, error
