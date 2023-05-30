# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 23:08:55 2023

@author: rikke
"""
import os
import pandas as pd

folder_path = 'C:/Users/rikke/Nextcloud/Rikke/Continuous_Trades-DE-2021'

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Load the CSV file into a pandas dataframe
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, skiprows=[0])

        # Remove duplicate rows based on the first column
        df.drop_duplicates(subset=['TradeId'], keep='first', inplace=True)
        
        df = df[df["TradePhase"].str.contains("CONT") == True]
        
        df = df[df["UserDefinedBlock"].str.contains("Y") == False]
        
        df = df[df["Product"].str.contains("Quarter") == False]

        df = df[df["Product"].str.contains("Half") == False]
        
        df = df.drop(['TradeId', 'RemoteTradeId', 'Side', 'Product', 'DeliveryArea', 'TradePhase', 'UserDefinedBlock', 'SelfTrade', 'Currency', 'VolumeUnit', 'OrderID'], axis=1)

        # Save the cleaned data back to the original CSV file
        df.to_csv(file_path, index=False)