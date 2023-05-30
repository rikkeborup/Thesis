# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:54:51 2023

@author: rikke
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

#%%

TimeSeriesData = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\Trades.csv")

#%%
# Add day-ahead data

DayAhead = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\DayAhead.csv")

specific_times = ['16:00:00', '17:00:00', '18:00:00']
DayAhead['Day-Ahead Date'] = pd.to_datetime(DayAhead['Day-Ahead Date'])
DayAhead['time'] = DayAhead['Day-Ahead Date'].dt.strftime('%H:%M:%S')
mask = DayAhead['time'].isin(specific_times)
df_filtered = DayAhead[mask]

df_pivoted = df_filtered.pivot(columns='time', values='Day-Ahead Price')
df_pivoted = df_pivoted.reset_index(drop=True)
df_pivoted.columns = ['HourBefore', 'CurrentHour', 'HourAfter']

TimeSeriesData = pd.merge(TimeSeriesData, DayAhead, left_on='DeliveryStart', right_on='Day-Ahead Date', how='inner')

TimeSeriesData = TimeSeriesData.drop('Day-Ahead Date', axis=1)

#%%
#Add engineered date variables data

Dummies = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\Dummies.csv")

TimeSeriesData = pd.merge(TimeSeriesData, Dummies, left_on='ExecutionTime', right_on='ExecutionTime', how='inner')

#%%
#Add flow data

Flow = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\Flow.csv")

TimeSeriesData = pd.merge(TimeSeriesData, Flow, left_on='ExecutionTime', right_on='ExecutionTime', how='inner')

#%%
#Add Forecast

Forecast = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\Forecasts.csv")

TimeSeriesData = pd.merge(TimeSeriesData, Forecast, left_on='ExecutionTime', right_on='ExecutionTime', how='inner')

#%%
#Add generation actual

GenerationActual = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\GenerationActual.csv")

TimeSeriesData = pd.merge(TimeSeriesData, GenerationActual, left_on='ExecutionTime', right_on='GenerationDate', how='inner')

TimeSeriesData = TimeSeriesData.drop('GenerationDate', axis=1)

#%%
#Add generation forecast

GenerationForecast = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\GenerationForecast.csv")

TimeSeriesData = pd.merge(TimeSeriesData, GenerationForecast, left_on='DeliveryStart', right_on='GenerationDate', how='inner')

TimeSeriesData = TimeSeriesData.drop('GenerationDate', axis=1)

#%%
#Add Load forecast

LoadForecast = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\LoadForecast.csv")

TimeSeriesData = pd.merge(TimeSeriesData, LoadForecast, left_on='ExecutionTime', right_on='LoadDate', how='inner')

TimeSeriesData = TimeSeriesData.drop('LoadDate', axis=1)

#%%
#Add reneweable forecast

ReneweableForecast = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\ReneweableForecast.csv")

TimeSeriesData = pd.merge(TimeSeriesData, ReneweableForecast, left_on='ExecutionTime', right_on='GenerationDate', how='inner')

TimeSeriesData = TimeSeriesData.drop('GenerationDate', axis=1)

#%%

num_rows = len(TimeSeriesData)  # Total number of rows in the DataFrame
copy_interval = 30  # Number of rows to copy and skip in each iteration
copy_size = 6       # Number of rows to copy in each iteration

for i in range(0, num_rows, copy_interval):
    average_value = np.mean(TimeSeriesData.loc[i:i+copy_size-1, 'Weighted Average Price'])
    TimeSeriesData.loc[i:i+copy_interval-1, 'Pre-prices'] = average_value
    

#%%
TimeSeriesData.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\FullGermanModel(Extended).csv", index=False)
