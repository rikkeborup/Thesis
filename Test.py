# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:54:23 2023

@author: rikke
"""

import pandas as pd
import torch
from pytorch_forecasting import TimeSeriesDataSet
from pytorch_forecasting.models.temporal_fusion_transformer import TemporalFusionTransformer
from pytorch_forecasting.metrics import QuantileLoss
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import RobustScaler

#%%

TimeSeriesData = pd.read_csv(r"C:\Users\rikke\Documents\Speciale data\Speciale\Data\FullGermanModelWithLag.csv")
TimeSeriesData['Timeseries_ID'] = TimeSeriesData['Timeseries_ID'].astype(str)
TimeSeriesData['year'] = TimeSeriesData['year'].astype(str)
TimeSeriesData['quarter'] = TimeSeriesData['quarter'].astype(str)
TimeSeriesData['month'] = TimeSeriesData['month'].astype(str)
TimeSeriesData['dayofweek'] = TimeSeriesData['dayofweek'].astype(str)

#%%
columns_to_keep = ['Time_index', 'Timeseries_ID', 'ExecutionTime', 'DeliveryStart', 'Weighted Average Price', 'dayofweek', 'Pre-prices', 'year', 'Day-Ahead Price', 'quarter', 'LoadForecast', 'GenerationForecast', 'ReneweableForecast']
# Select the desired columns
TimeSeriesData = TimeSeriesData[columns_to_keep]

#%%
#scale data
cols_to_scale = ['Weighted Average Price', 'Day-Ahead Price', 'ReneweableForecast', 'LoadForecast', 'Pre-prices', 'GenerationForecast']

scaler = RobustScaler()
TimeSeriesData_scaled = scaler.fit_transform(TimeSeriesData[cols_to_scale])

TimeSeriesData[cols_to_scale] = TimeSeriesData_scaled

#%%

data_cutoff = 21329
obs_per_day = 30
max_encoder_length = obs_per_day * 710
max_prediction_length = 24
test_days = 7

data = TimeSeriesDataSet(
    TimeSeriesData[lambda x: x.Time_index <= data_cutoff],
    time_idx="Time_index",
    target="Weighted Average Price",
    group_ids=["Timeseries_ID"],
    min_encoder_length=max_encoder_length // 2,
    max_encoder_length=max_encoder_length,
    max_prediction_length=max_prediction_length,
    static_categoricals=["Timeseries_ID"],
    time_varying_known_categoricals=['year','dayofweek', 'quarter'],
    time_varying_known_reals=['Time_index', 'Day-Ahead Price', 'ReneweableForecast', 'LoadForecast', 'GenerationForecast', 'Pre-prices'],
    time_varying_unknown_reals=['Weighted Average Price'],
    add_relative_time_idx=True,
    add_target_scales=True,
    add_encoder_length=True)

test_datasets = []

for i in range(test_days):
    test_start = data_cutoff + 1 + (i * obs_per_day)
    test_datasets.append(
        TimeSeriesDataSet.from_dataset(
            data,
            TimeSeriesData[lambda x: x.Time_index < test_start + obs_per_day],
            predict=True,
            stop_randomization=True)
    )
    
batch_size = 32
test_dataloaders = [test_day.to_dataloader(train=False, batch_size=batch_size * 10) for test_day in test_datasets]

#%%

best_model_path=r"C:\Users\rikke\Documents\Speciale data\Speciale\Saved models\Grid Search + pre-prices\version_2 - Grid Search + Lag (Default)\checkpoints\epoch=4-step=3195.ckpt"
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)

#%%
#Get mean and variance for "Weighted Average Price"

variable_index = 0
center = scaler.center_[variable_index]
scale = scaler.scale_[variable_index]

#%%

total_average_loss = 0
mae_sum = 0
mape_sum = 0
rmse_sum = 0
smape_sum = 0
bias_sum = 0

for i, test_day in enumerate(test_dataloaders):
    raw_predictions, x = best_tft.predict(test_day, mode="raw", return_x=True)
    
    ### COMMENT OUT FOR UNSCALED ###
    x['encoder_target'] = x['encoder_target'] * scale + center
    x['decoder_target'] = x['decoder_target'] * scale + center
    prediction_tensor = raw_predictions['prediction']
    unscaled_prediction_tensor = prediction_tensor * scale + center
    out = {"prediction": unscaled_prediction_tensor}
    ###
    
    ### COMMENT OUT FOR SCALED ####
    #out = {"prediction": raw_predictions['prediction']}
    ###
    
    min_val = torch.minimum(torch.min(out['prediction'][:, :, 0]), x['decoder_target'].min())
    max_val = torch.maximum(torch.max(out['prediction'][:, :, -1]), x['decoder_target'].max())

    # create two y-axes, one on the left and one on the right
    fig, ax_left = plt.subplots(figsize=(10, 4))
    ax_right = ax_left.twinx()
    
    # plot the data on the left axis
    best_tft.plot_prediction(x, out, idx=0, plot_attention=False, add_loss_to_title=False, ax=ax_left)

    # plot additional data on the right axis
    ax_left.set_ylabel("Price")
    
    # set the limits for the left y-axis to zoom in
    plt.xlim(-5, 24)
    ax_left.set_ylim([min_val - 10, max_val + 10])
    
    Quantile_loss = QuantileLoss()
    loss_value = Quantile_loss(out['prediction'], x['decoder_target'])
    
    mae = np.mean(np.abs(np.array(out['prediction'][0,:,3]) - np.array(x['decoder_target'])))
    mape = np.mean(np.abs((np.array(out['prediction'][0,:,3]) - np.array(x['decoder_target'])) / np.array(x['decoder_target'])))
    rmse = np.sqrt(np.mean(np.square(np.array(out['prediction'][0,:,3]) - np.array(x['decoder_target']))))
    smape = np.mean(2 * np.abs(np.array(out['prediction'][0,:,3]) - np.array(x['decoder_target'])) / (np.abs(np.array(out['prediction'][0,:,3])) + np.abs(np.array(x['decoder_target']))))
    bias = np.mean(np.array(out['prediction'][0,:,3]) - np.array(x['decoder_target']))
    mae_sum += mae
    mape_sum += mape
    rmse_sum += rmse
    smape_sum += smape
    bias_sum += bias
    
    title = 'Validation day ' + str(i+1) + "\nQuantile Loss: " + str(round(loss_value.item(), 2)) + ", MAE: " + str(round(mae, 2)) + ", MAPE: " + str(round(mape, 2)) + ", RMSE: " + str(round(rmse, 2)) + ", SMAPE: " + str(round(smape, 2)) + ", Bias: " + str(round(bias,2))
    plt.title(title)
    
    total_average_loss = total_average_loss + loss_value.item()
    # show the plot
    plt.show()
    
print(total_average_loss/7)
mae_avg = mae_sum / 7
mape_avg = mape_sum / 7
rmse_avg = rmse_sum / 7
smape_avg = smape_sum / 7
bias_avg = bias_sum / 7

print(f'mae: {mae_avg}')
print(f'mape: {mape_avg}')
print(f'rmse: {rmse_avg}')
print(f'SMAPE: {smape_avg}')
print(f'Forecast Bias: {bias_avg}')