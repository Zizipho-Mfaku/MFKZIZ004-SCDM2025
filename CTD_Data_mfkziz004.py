# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:40:05 2025

@author: mfaku
"""

# CTD 

import os
import pandas as pd

# Use the absolute path to the Downloads folder
file_path = r"C:\Users\mfaku\Downloads\CTD_data.csv"  # This makes the file get loaded in

# Check if the file exists before trying to load it
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("File loaded successfully!")
    print(df.head())  # Display the first few rows