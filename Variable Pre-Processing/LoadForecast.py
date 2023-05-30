# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:40:06 2023

@author: rikke
"""

import pandas as pd

#%%

LoadForecast1 = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Load Data 2021-2022\Total Load - Day Ahead _ Actual_202101010000-202201010000.csv")

LoadForecast2 = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Load Data 2021-2022\Total Load - Day Ahead _ Actual_202201010000-202301010000.csv")

LoadForecast = pd.concat([LoadForecast1, LoadForecast2], ignore_index = True)

LoadForecast.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Load Data 2021-2022\LoadForecast.csv", index=False)

#%%

LoadForecast = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Load Data 2021-2022\LoadForecast.csv")

#%%

LoadActual = LoadForecast.copy()
LoadActual.drop(LoadActual.columns[[1]], axis=1, inplace=True)
LoadForecast.drop(LoadForecast.columns[[len(LoadForecast.columns)-1]],axis=1,inplace=True)

#%%

LoadForecast.columns.values[0] = 'LoadDate'
LoadForecast.columns.values[1] = 'LoadForecast'

LoadActual.columns.values[0] = 'LoadDate'
LoadActual.columns.values[1] = 'LoadActual'

#%%

# Extract the start time from the datetime column
LoadForecast['LoadDate'] = pd.to_datetime(LoadForecast['LoadDate'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')

# Convert the datetime column into the desired format "yyyy.mm.dd hh:mm:ss"
LoadForecast['LoadDate'] = LoadForecast['LoadDate'].dt.strftime('%Y.%m.%d %H:%M:%S')

LoadForecast['LoadDate'] = pd.to_datetime(LoadForecast['LoadDate'])

#%%

# Extract the start time from the datetime column
LoadActual['LoadDate'] = pd.to_datetime(LoadActual['LoadDate'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')

# Convert the datetime column into the desired format "yyyy.mm.dd hh:mm:ss"
LoadActual['LoadDate'] = LoadActual['LoadDate'].dt.strftime('%Y.%m.%d %H:%M:%S')

LoadActual['LoadDate'] = pd.to_datetime(LoadActual['LoadDate'])

#%%
# Create a new column for the minutes
LoadForecast['Minutes'] = LoadForecast['LoadDate'].dt.minute

# Pivot the dataframe to get the desired format
pivoted_df = LoadForecast.pivot(index='LoadDate', columns='Minutes', values='LoadForecast')

pivoted_df = pivoted_df.reset_index()

pivoted_df['LoadDate'] = pivoted_df['LoadDate'].dt.floor('H')

pivoted_df = pivoted_df.fillna(0)

pivoted_df = pivoted_df.groupby('LoadDate')[0, 15, 30, 45].sum().reset_index()

pivoted_df = pivoted_df.rename(columns={0: 'ForecastLoad0', 15: 'ForecastLoad15', 30: 'ForecastLoad30', 45: 'ForecastLoad45'})

#%%
# Create a new column for the minutes
LoadActual['Minutes'] = LoadActual['LoadDate'].dt.minute

# Pivot the dataframe to get the desired format
pivoted_df_actual = LoadActual.pivot(index='LoadDate', columns='Minutes', values='LoadActual')

pivoted_df_actual = pivoted_df_actual.reset_index()

pivoted_df_actual['LoadDate'] = pivoted_df_actual['LoadDate'].dt.floor('H')

pivoted_df_actual = pivoted_df_actual.fillna(0)

pivoted_df_actual = pivoted_df_actual.groupby('LoadDate')[0, 15, 30, 45].sum().reset_index()

pivoted_df_actual = pivoted_df_actual.rename(columns={0: 'ActualLoad0', 15: 'ActualLoad15', 30: 'ActualLoad30', 45: 'ActualLoad45'})

#%%

merged_df = pd.merge(LoadActual, LoadForecast)

#%%
merged_df.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\LoadForecast.csv", index=False)

#%%

LoadGermany = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\LoadForecast.csv")

#%%
# Set the datetime column as the index
LoadGermany['LoadDate'] = pd.to_datetime(LoadGermany['LoadDate'])

LoadGermany.set_index('LoadDate', inplace=True)

# Resample the dataframe to 5 minute intervals
LoadGermany = LoadGermany.resample('5T').ffill()

# Reset the index
LoadGermany.reset_index(inplace=True)

#%%

LoadGermany.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\LoadForecast.csv", index=False)




























