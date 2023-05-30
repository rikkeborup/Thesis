#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:16:52 2023

@author: rikkeborup
"""

import pandas as pd
import glob
import os

#%%

#Load all individual csv files and combine into one dataframe

# Define the path to the top-level folder
path = '/Users/rikkeborup/Downloads/Speciale/German Intraday Data 2021-2022'

dfs = []

# Loop through all folders in the top-level folder
for foldername in os.listdir(path):
    folderpath = os.path.join(path, foldername)
 
    count = 1 
    
    # Loop through all CSV files in the current folder
    for fname in glob.glob(os.path.join(folderpath, '*.csv')):
        df = pd.read_csv(fname)
        dfs.append(df)
        
        print(count)
        count = count + 1
    
data = pd.concat(dfs, ignore_index=True)

#%%

#Save dataframe as new csv file with all cleaned data

path = '/Users/rikkeborup/Downloads/Speciale/German Intraday Data 2021-2022'
filename = "intradaydataDEcleaned.csv"
full_path = os.path.join(path, filename)

data.to_csv(full_path, index=False)

print("Data saved to", full_path)

