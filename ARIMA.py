# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:19:18 2023

@author: rikke
"""
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime, timedelta
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Load the historical data
data = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\TimeSeriesDataSet - Trades (Extended).csv")
data = data.drop('Time_index', axis=1)
data = data.drop('Timeseries_ID', axis=1)

#%%
#As ARIMA model assumes stationarity, we log transform to make the varaince more constant.

min_value = data['Weighted Average Price'].min()

data["Weighted Average Price"] = data["Weighted Average Price"] + abs(min_value) + 1

data["Weighted Average Price"] = np.log(data["Weighted Average Price"])

#%%

TrainingData = data[data['DeliveryStart'] <= '2022-12-13']

#%%

data['DeliveryStart'] = pd.to_datetime(data['DeliveryStart'])

validation = []
for i in range(7):
    day = datetime.strptime('2022-12-13 17:00:00', '%Y-%m-%d %H:%M:%S')
    target_date = day + timedelta(1 * i)
    df = data[data['DeliveryStart'] == target_date]
    print(f'{target_date}: {len(df)} rows')
    validation.append(df)

#%%
#Checking for stationarity

acf_original = plot_acf(TrainingData['Weighted Average Price'])
pacf_original = plot_pacf(TrainingData['Weighted Average Price'])

#%%

train_diff = TrainingData['Weighted Average Price'].diff().dropna()
train_diff.plot()
acf_diff = plot_acf(train_diff)
pacf_diff = plot_pacf(train_diff)

#%%

mae_sum = 0
mape_sum = 0
rmse_sum = 0
smape_sum = 0
bias_sum = 0


for i in range(len(validation)):
    TrainingData = pd.concat([TrainingData, validation[i].head(6)])
    
    model = sm.tsa.ARIMA(TrainingData['Weighted Average Price'], order=(0, 1, 4))
    results = model.fit()

    start = TrainingData.index[-1] + 1
    end = start + 23

    forecast = results.predict(start=start, end=end)
    forecast = np.exp(forecast)
    forecast = forecast - (abs(min_value) + 1)
    
    TrainingData = TrainingData.iloc[:-6]
    TrainingData = pd.concat([TrainingData, validation[i]])
    
    actuals = TrainingData.copy()
    actuals["Weighted Average Price"] = np.exp(actuals["Weighted Average Price"])
    actuals["Weighted Average Price"] = actuals["Weighted Average Price"] - (abs(min_value) + 1)
    
    plt.plot(actuals["Weighted Average Price"])
    plt.plot(forecast)
    plt.legend(['Actual', 'Predicted'])

    last_24_obs = len(TrainingData) - 24
    min_val = actuals["Weighted Average Price"].tail(24).min()
    max_val = actuals["Weighted Average Price"].tail(24).max()

    last_30_obs = len(actuals) - 30
    plt.xlim(actuals.index[last_30_obs], actuals.index[-1])
    plt.ylim([min_val - 10, max_val + 10])
    
    
    actual_values = actuals["Weighted Average Price"]
    predicted_values = forecast[-24:]
    
    mae = np.mean(np.abs(predicted_values - actual_values))
    mape = np.mean(np.abs((predicted_values - actual_values) / actual_values))
    rmse = np.sqrt(np.mean(np.square(predicted_values - actual_values)))
    smape = np.mean(2 * np.abs(predicted_values - actual_values) / (np.abs(predicted_values) + np.abs(actual_values)))
    bias = np.mean(predicted_values - actual_values)
    mae_sum += mae
    mape_sum += mape
    rmse_sum += rmse
    smape_sum += smape
    bias_sum += bias
    
    plt.title('Validation day ' + str(i+1) + "\nMAE: " + str(round(mae, 2)) + ", MAPE: " + str(round(mape, 2)) + ", RMSE: " + str(round(rmse, 2)) + ", SMAPE: " + str(round(smape, 2)) + ", Bias: " + str(round(bias,2)))
    plt.show()

mae_avg = mae_sum / len(validation)
mape_avg = mape_sum / len(validation)
rmse_avg = rmse_sum / len(validation)
smape_avg = smape_sum / len(validation)
bias_avg = bias_sum / len(validation)

print(f'mae: {mae_avg}')
print(f'mape: {mape_avg}')
print(f'rmse: {rmse_avg}')
print(f'SMAPE: {smape_avg}')
print(f'Forecast Bias: {bias_avg}')


#%%

cutoff_date = '2022-12-29'  # set the cutoff date

# filter out rows where date_col is after the cutoff date
data = data[data['ExecutionTime'] <= cutoff_date]

#%%
data.info()

data.plot()

#%%

import numpy as np
data['Weighted Average Price'] = np.log(data['Weighted Average Price']) # don't forget to transform the data back when making real predictions

data.plot()

#%%

msk = (data.index < len(data)-30)
df_train = data[msk].copy()
df_test = data[~msk].copy()

#%%

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

acf_original = plot_acf(df_train['Weighted Average Price'])

pacf_original = plot_pacf(df_train['Weighted Average Price'])

#%%

from statsmodels.tsa.stattools import adfuller
adf_test = adfuller(df_train['Weighted Average Price'])
print(f'p-value: {adf_test[1]}')

#%%

df_train_diff = df_train['Weighted Average Price'].diff().dropna()
df_train_diff.plot()

#%%

acf_diff = plot_acf(df_train_diff)

pacf_diff = plot_pacf(df_train_diff)

#%%

adf_test = adfuller(df_train_diff)
print(f'p-value: {adf_test[1]}')

#%%

from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(TrainingData['Weighted Average Price'], order=(1,1,1))
model_fit = model.fit()
print(model_fit.summary())

#%%

import matplotlib.pyplot as plt
residuals = model_fit.resid[1:]
fig, ax = plt.subplots(1,2)
residuals.plot(title='Residuals', ax=ax[0])
residuals.plot(title='Density', kind='kde', ax=ax[1])
plt.show()

#%%

forecast_test = model_fit.forecast(len(df_test['Weighted Average Price']))

data['forecast_manual'] = [None]*len(df_train['Weighted Average Price']) + list(forecast_test)

data.plot()

plt.xlim(21290, 21330)

# show the plot
plt.show()

#%%

from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

mae = mean_absolute_error(df_test['Weighted Average Price'], forecast_test)
mape = mean_absolute_percentage_error(df_test['Weighted Average Price'], forecast_test)
rmse = np.sqrt(mean_squared_error(df_test['Weighted Average Price'], forecast_test))

print(f'mae - manual: {mae}')
print(f'mape - manual: {mape}')
print(f'rmse - manual: {rmse}')
