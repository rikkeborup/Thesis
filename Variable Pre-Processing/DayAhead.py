# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:40:06 2023

@author: rikke
"""

import pandas as pd

#%%

DayAhead1 = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Day-Ahead Data 2021-2022\Day-ahead Prices_202101010000-202201010000.csv")

DayAhead2 = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Day-Ahead Data 2021-2022\Day-ahead Prices_202201010000-202301010000.csv")

DayAhead = pd.concat([DayAhead1, DayAhead2], ignore_index = True)

DayAhead.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Day-Ahead Data 2021-2022", index=False)

#%%

DayAhead = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Day-Ahead Data 2021-2022\DayAhead.csv")

#%%

DayAhead.drop(DayAhead.columns[[len(DayAhead.columns)-2,len(DayAhead.columns)-1]],axis=1,inplace=True)

#%%

DayAhead.columns.values[0] = 'Day-Ahead Date'
DayAhead.columns.values[1] = 'Day-Ahead Price'

#%%

# Extract the start time from the datetime column
DayAhead['Day-Ahead Date'] = pd.to_datetime(DayAhead['Day-Ahead Date'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')

# Convert the datetime column into the desired format "yyyy.mm.dd hh:mm:ss"
DayAhead['Day-Ahead Date'] = DayAhead['Day-Ahead Date'].dt.strftime('%Y.%m.%d %H:%M:%S')

DayAhead['Day-Ahead Date'] = pd.to_datetime(DayAhead['Day-Ahead Date'])

#%%
DayAhead.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\DayAhead.csv", index=False)