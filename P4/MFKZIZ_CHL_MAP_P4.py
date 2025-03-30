# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 01:58:56 2025

@author: mfaku
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from scipy.interpolate import griddata

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

# Calculate the mean chlorophyll concentration over time
mean_region_data = region_chl_data_1997_1998.mean(dim='time')

# Mask data to exclude values below 0.05
masked_mean_region_data = mean_region_data.where(mean_region_data > 0.05)

# Interpolate to fill gaps at the edges
lon_grid, lat_grid = np.meshgrid(masked_mean_region_data.lon.values, masked_mean_region_data.lat.values)
points = np.array([lon_grid.flatten(), lat_grid.flatten()]).T
values = masked_mean_region_data.values.flatten()
interpolated_data = griddata(points, values, (lon_grid, lat_grid), method='linear')

# Set up the plot
fig, ax = plt.subplots(figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# Add land and ocean features
ax.add_feature(cfeature.LAND, color='grey')
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)

# Add gridlines
gridlines = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
gridlines.right_labels = False
gridlines.top_labels = False

# Plot chlorophyll concentration with a logarithmic scale
chl_plot = ax.contourf(
    lon_grid, lat_grid, np.log10(interpolated_data),
    cmap='summer', levels=np.linspace(-1, 1, 100),
    transform=ccrs.PlateCarree()
)

# Add labels for key locations
locations = {
    "False Bay": (18.43, -34.20),
    "Cape Town": (18.42, -33.92),
    "Lambert's Bay": (18.31, -32.09)
}
for name, (lon, lat) in locations.items():
    ax.plot(lon, lat, marker='o', color='red', transform=ccrs.PlateCarree())
    ax.text(lon + 0.1, lat - 0.1, name, fontsize=10, color='black', transform=ccrs.PlateCarree())

# Add colorbar
cbar = plt.colorbar(chl_plot, ax=ax, orientation='vertical', shrink=0.7)
cbar.set_label(r'Log10(Chlorophyll Concentration) (mg/m$^3$)')

# Add title and labels
ax.set_title('Chlorophyll Concentration (1997-1998) - West Coast of South Africa', fontsize=14)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.tight_layout()
plt.show()
