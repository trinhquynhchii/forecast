import math
import numpy as np
import pandas as pd
from fbprophet import Prophet
import time


class ProphetModel:
    """
    Using Prophet model for prediction
    """

    label = 'Prophet'

    def __init__(self, train_series, target_col):
        self.train_series = train_series
        self.target_col = target_col
        self.model = Prophet()
    
    def fit(self):
        """
        Fitting Prohphet model
        """
    
        df_train = self.train_series[self.target_col].reset_index()
        df_train.columns = ['ds', 'y']
        self.model.fit(df_train)
        
    def forecast(self, period):
        future = self.model.make_future_dataframe(periods=period)
        forecast = self.model.predict(future)
#         self.model.plot(preds)
        preds_series = forecast['yhat']
        return preds_series, forecast

    def plot_forecast(self, forecast):
        self.model.plot(forecast)
        
    def plot_forecast_component(self, forecast):
        self.model.plot_components(forecast)
    
    def get_label(self):
        return 'Prophet'