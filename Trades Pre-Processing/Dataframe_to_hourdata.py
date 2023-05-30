#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 13:25:51 2023

@author: rikkeborup
"""

import pandas as pd
import os
from datetime import timedelta
import numpy as np

#%%

#Loading cleaned data from csv file 

data = pd.read_csv("C:/Users/rikke/Documents/Speciale data/Speciale/German Intraday Data 2021-2022/intradaydataDEcleaned.csv")

#%%

#Creating list of all hours in a day
hour_values = data['DeliveryStart'].str.slice(11, 13).unique().tolist()

#%%

#Creating a seperate CSV file for each hour of the day with new columns and 5-minute interval
for hour in hour_values:
    hourdata = data.loc[data['DeliveryStart'].str.slice(11, 13) == hour].copy()
    
    hourdata['ExecutionTime'] = hourdata['ExecutionTime'].str.replace('T', ' ').str.replace('Z', '')
    hourdata['ExecutionTime'] = pd.to_datetime(hourdata['ExecutionTime'])
    
    hourdata['DeliveryStart'] = hourdata['DeliveryStart'].str.replace('T', ' ').str.replace('Z', '')
    hourdata['DeliveryStart'] = pd.to_datetime(hourdata['DeliveryStart'])
    
    hourdata['start_time'] = hourdata['DeliveryStart'].dt.date.astype(str) + ' ' + hour + ':00:00'
    hourdata['start_time'] = pd.to_datetime(hourdata['start_time']) - timedelta(hours=2, minutes=30)
    
    hourdata['end_time'] = hourdata['DeliveryStart'].dt.date.astype(str) + ' ' + hour + ':00:00'
    hourdata['end_time'] = pd.to_datetime(hourdata['end_time']) - timedelta(minutes=30)
    
    # Filter the dataframe to keep only rows between start_time and end_time
    hourdata = hourdata[(hourdata['ExecutionTime'] >= hourdata['start_time']) & (hourdata['ExecutionTime'] < hourdata['end_time'])]
    hourdata = hourdata.drop(['start_time', 'end_time'], axis=1)
    
    #Formatting into 5-minute interval 
    hourdata['ExecutionTime'] = pd.DatetimeIndex(hourdata['ExecutionTime']).floor('5T')
    
    #Calculating the weighted average price for the 5-minute intervals
    grouped = hourdata.groupby(['DeliveryStart', 'ExecutionTime'])
    weighted_average = grouped.apply(lambda x: np.average(x['Price'], weights=x['Volume']))
    output = pd.DataFrame(weighted_average, columns=['Weighted Average Price'])
    output.reset_index(inplace=True)
    
    #Creating a time_index with all expected 5-minute intervals
    start = output['DeliveryStart'].min() - timedelta(hours=2, minutes=30)
    end = output['DeliveryStart'].max() - timedelta(minutes=30)
    
    time_index = pd.date_range(start=start, end=end, freq='5min')
    time_index = pd.DataFrame({'ExecutionTime': time_index})
    time_index['start_time'] = pd.to_datetime(time_index['ExecutionTime'].dt.date.astype(str) + ' ' + start.time().strftime('%H:%M:%S'))
    time_index['x'] = time_index['ExecutionTime'] - time_index['start_time']
    time_index['x'] = time_index['x'].astype(str).str[-8:]
    time_index['x'] = pd.to_timedelta(time_index['x'])
    time_index['start_time'] = time_index['ExecutionTime'] - time_index['x']
    time_index['end_time'] = time_index['start_time'] +timedelta(hours=1, minutes=55)
    time_index = time_index[time_index['ExecutionTime'].between(time_index['start_time'], time_index['end_time'])]
    time_index = time_index.drop(columns=['start_time', 'end_time', 'x'])
    
    output = pd.merge(time_index, output, on='ExecutionTime', how='left')
    
    #Creating a date index with all expected dates
    #The time index and date index helps handle null values
    start_date = output['DeliveryStart'].min()
    end_date = output['DeliveryStart'].max()
    
    dt_list = pd.date_range(start=start_date, end=end_date, freq='D')
    dt_list = pd.np.repeat(dt_list, 24)
    output['DeliveryStart'] = dt_list

#%%

    #Saving CSV 
    path = 'C:/Users/rikke/Documents/Speciale data/Speciale/German Intraday Data 2021-2022'
    filename = "intradaydataDEhour" + hour + ".csv"
    full_path = os.path.join(path, filename)
    output.to_csv(full_path, index=False)

    print("Data saved to", full_path)
