# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 09:54:14 2025

@author: mfaku
"""

# CTD assignment 

import os
import pandas as pd

# Use the absolute path to the Downloads folder
file_path = r"C:\Users\mfaku\Downloads\CTD_data.csv"  # This makes the file get loaded in

# Check if the file exists before trying to load it
if os.path.exists(file_path):
    df = pd.read_csv(file_path,header=None, sep='\s+') # the sep='\s+' is able to match white spaces characters directly with their columns
    print("File loaded successfully!")
    print(df.head())  # Display the first few rows


# Assign column names directly
df.columns = ["Date", "Time", "Depth (m)", "Temperature (°C)", "Salinity (psu)"]

# Print the data: 
    
print(df)




