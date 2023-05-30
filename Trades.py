# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:10:45 2023

@author: rikke
"""

import pandas as pd
import os

#%%
#Load data

TimeSeriesData = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\German Intraday Data 2021-2022\intradaydataDEhour17(Extended).csv")

#%%
#Add time index, and remove NA's

TimeSeriesData['Time_index'] = TimeSeriesData.index
TimeSeriesData['Timeseries_ID'] = "1"
TimeSeriesData['ExecutionTime'] = pd.to_datetime(TimeSeriesData['ExecutionTime'])
TimeSeriesData = TimeSeriesData.set_index('ExecutionTime')
TimeSeriesData['Weighted Average Price'] = TimeSeriesData['Weighted Average Price'].interpolate(method='nearest')
TimeSeriesData = TimeSeriesData.reset_index()

#%%
#Saving CSV 

path = 'C:/Users/rikke/Documents/Speciale data/Speciale/Data'
filename = "TimeSeriesDataSet - Trades (Extended).csv"
full_path = os.path.join(path, filename)
TimeSeriesData.to_csv(full_path, index=False)

print("Data saved to", full_path)
