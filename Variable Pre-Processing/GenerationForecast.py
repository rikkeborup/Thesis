# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:40:06 2023

@author: rikke
"""

import pandas as pd

#%%

GenerationForecast1 = pd.read_csv(r"C:\Users\rikke\Downloads\Generation Forecast - Day ahead_202101010000-202201010000.csv")

GenerationForecast2 = pd.read_csv(r"C:\Users\rikke\Downloads\Generation Forecast - Day ahead_202201010000-202301010000.csv")

GenerationForecast = pd.concat([GenerationForecast1, GenerationForecast2], ignore_index = True)

#GenerationForecast.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Generation Forecast Data 2021-2022\GenerationForecast.csv", index=False)

GenerationActual1 = pd.read_csv(r"C:\Users\rikke\Downloads\Actual Generation per Production Type_202101010000-202201010000 (3).csv")

GenerationActual2 = pd.read_csv(r"C:\Users\rikke\Downloads\Actual Generation per Production Type_202201010000-202301010000 (2).csv")

GenerationActual = pd.concat([GenerationActual1, GenerationActual2], ignore_index = True)

#%%

GenerationForecast = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Generation Forecast Data 2021-2022\GenerationForecast.csv")

#%%

GenerationForecast.drop(GenerationForecast.columns[[len(GenerationForecast.columns)-1]],axis=1,inplace=True)

#%%

GenerationForecast.columns.values[0] = 'GenerationDate'
GenerationForecast.columns.values[1] = 'GenerationForecast'

#%%

# Extract the start time from the datetime column
GenerationForecast['GenerationDate'] = pd.to_datetime(GenerationForecast['GenerationDate'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')

# Convert the datetime column into the desired format "yyyy.mm.dd hh:mm:ss"
GenerationForecast['GenerationDate'] = GenerationForecast['GenerationDate'].dt.strftime('%Y.%m.%d %H:%M:%S')

GenerationForecast['GenerationDate'] = pd.to_datetime(GenerationForecast['GenerationDate'])

#%%
GenerationForecast.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\GenerationForecast.csv", index=False)

#%%

GenerationActual = GenerationActual.loc[:, ~GenerationActual.isin(['n/e']).any()]

GenerationActual.iloc[:, [15, 16]] = GenerationActual.iloc[:, [16, 15]].values

GenerationActual['sum'] = GenerationActual.iloc[:, 2:16].sum(axis=1)

GenerationActual.rename(columns={GenerationActual.columns[2]: 'GenerationActualsGermany'}, inplace=True)

GenerationActual.drop(GenerationActual.iloc[:, 2:16], axis=1, inplace=True)

GenerationActual['ReneweableActualsGermany'] = GenerationActual.iloc[:, 2:5].sum(axis=1)

GenerationActual.drop(GenerationActual.iloc[:, 2:5], axis=1, inplace=True)

GenerationActual.drop(GenerationActual.columns[0], axis=1, inplace=True)

GenerationActual.columns.values[0] = 'GenerationDate'

#%%

# Extract the start time from the datetime column
GenerationActual['GenerationDate'] = pd.to_datetime(GenerationActual['GenerationDate'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')

# Convert the datetime column into the desired format "yyyy.mm.dd hh:mm:ss"
GenerationActual['GenerationDate'] = GenerationActual['GenerationDate'].dt.strftime('%Y.%m.%d %H:%M:%S')

GenerationActual['GenerationDate'] = pd.to_datetime(GenerationActual['GenerationDate'])

#%%

# Set the datetime column as the index
GenerationActual.set_index('GenerationDate', inplace=True)

# Resample the dataframe to 5 minute intervals
GenerationActual = GenerationActual.resample('5T').ffill()

# Reset the index
GenerationActual.reset_index(inplace=True)

#%%
GenerationActual.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\GenerationActual.csv", index=False)

#%%
ReneweableForecast1 = pd.read_csv(r"C:\Users\rikke\Downloads\Generation Forecasts for Wind and Solar_202101010000-202201010000.csv")

ReneweableForecast2 = pd.read_csv(r"C:\Users\rikke\Downloads\Generation Forecasts for Wind and Solar_202201010000-202301010000.csv")

ReneweableForecast = pd.concat([ReneweableForecast1, ReneweableForecast2], ignore_index = True)

#%%

ReneweableForecast.drop(ReneweableForecast.iloc[:, 2:4], axis=1, inplace=True)

ReneweableForecast.drop(ReneweableForecast.iloc[:, 3:5], axis=1, inplace=True)

ReneweableForecast.drop(ReneweableForecast.iloc[:, 4:6], axis=1, inplace=True)

ReneweableForecast['ReneweableForecast'] = ReneweableForecast.iloc[:, 1:4].sum(axis=1)

ReneweableForecast.drop(ReneweableForecast.iloc[:, 1:4], axis=1, inplace=True)

ReneweableForecast.columns.values[0] = 'GenerationDate'

#%%

# Extract the start time from the datetime column
ReneweableForecast['GenerationDate'] = pd.to_datetime(ReneweableForecast['GenerationDate'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')

# Convert the datetime column into the desired format "yyyy.mm.dd hh:mm:ss"
ReneweableForecast['GenerationDate'] = ReneweableForecast['GenerationDate'].dt.strftime('%Y.%m.%d %H:%M:%S')

ReneweableForecast['GenerationDate'] = pd.to_datetime(ReneweableForecast['GenerationDate'])

#%%

# Set the datetime column as the index
ReneweableForecast.set_index('GenerationDate', inplace=True)

# Resample the dataframe to 5 minute intervals
ReneweableForecast = ReneweableForecast.resample('5T').ffill()

# Reset the index
ReneweableForecast.reset_index(inplace=True)

#%%

ReneweableForecast.to_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\ReneweableForecastl.csv", index=False)



