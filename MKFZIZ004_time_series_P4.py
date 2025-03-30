# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 10:32:45 2025

@author: mfaku
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr

# Load chlorophyll dataset
chl_path = r"C:\Users\mfaku\Downloads\ESA_CHL-fv5.0.nc"
ds_chl = xr.open_dataset(chl_path)

# Extract variables
chlor_data = ds_chl['chlor_a']
lat_data = ds_chl['lat']
lon_data = ds_chl['lon']
time_data = ds_chl['time']

# Convert time to pandas datetime format
time = pd.to_datetime(time_data.values)

# Define region coordinates for Lambert's Bay to False Bay
lat_min, lat_max = -35.0, -25.0
lon_min, lon_max = 10.0, 24.0

# Subset chlorophyll data for the region
region_chl_data = chlor_data.sel(
    lat=slice(lat_max, lat_min),  # Flip latitudes since they decrease
    lon=slice(lon_min, lon_max)
)

# Find the closest available time indices
start_time = np.datetime64('1997-01-01')
end_time = np.datetime64('1998-12-31')

# Use `.where()` to filter time values within the range
valid_times = time_data.where((time_data >= start_time) & (time_data <= end_time), drop=True)

# Subset the chlorophyll data for the time range
region_chl_data_1997_1998 = region_chl_data.sel(time=valid_times)

# Calculate the mean chlorophyll concentration over time for the whole region
mean_region_data = region_chl_data_1997_1998.mean(dim=['lat', 'lon'])

# Select a grid point near False Bay (latitude = -34.20, longitude = 18.43)
single_point_data = region_chl_data_1997_1998.sel(
    lat=-34.20, lon=18.43, method='nearest'
)

# Create time series for both the mean region data and the single grid point data
date_range = pd.date_range(start='1997-01-01', periods=len(valid_times), freq='D')

# Convert the data into pandas Series
mean_region_series = pd.Series(mean_region_data.values, index=date_range)
single_point_series = pd.Series(single_point_data.values, index=date_range)

# Plotting the time series
plt.figure(figsize=(10, 6))

# Plot mean seasonal cycle (whole region)
plt.plot(mean_region_series.index, mean_region_series.values, label='Mean Seasonal Cycle (Region)', color='green', linewidth=2)

# Plot time series for the single grid point (False Bay)
plt.plot(single_point_series.index, single_point_series.values, label='Single Grid Point (False Bay)', color='blue', linewidth=2)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Chlorophyll Concentration (mg/m³)')
plt.title('Chlorophyll Concentration Time Series: Mean Seasonal Cycle vs. Single Grid Point')
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
