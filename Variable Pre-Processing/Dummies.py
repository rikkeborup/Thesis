# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:23:00 2023

@author: rikke
"""
import pandas as pd
import os

#%%

TimeSeriesData = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\TimeSeriesDataSet - Trades (Extended).csv")

#%%

TimeSeriesData['DeliveryStart'] = pd.to_datetime(TimeSeriesData['DeliveryStart'])

TimeSeriesData['year'] = TimeSeriesData['DeliveryStart'].dt.year
TimeSeriesData['quarter'] = TimeSeriesData['DeliveryStart'].dt.quarter
TimeSeriesData['month'] = TimeSeriesData['DeliveryStart'].dt.month
TimeSeriesData['dayofweek'] = TimeSeriesData['DeliveryStart'].dt.dayofweek
TimeSeriesData = TimeSeriesData.drop(['DeliveryStart', 'Weighted Average Price'], axis=1)

TimeSeriesData = TimeSeriesData.drop(TimeSeriesData.columns[[1, 2]], axis=1)
#%%
#Saving CSV 

path = 'C:/Users/rikke/Documents/Speciale data/Speciale/Data'
filename = "Dummies.csv"
full_path = os.path.join(path, filename)
TimeSeriesData.to_csv(full_path, index=False)

print("Data saved to", full_path)

