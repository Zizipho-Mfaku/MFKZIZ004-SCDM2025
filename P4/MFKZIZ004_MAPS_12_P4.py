# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 10:53:50 2025

@author: mfaku
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load chlorophyll dataset
chl_path = r"C:\Users\mfaku\Downloads\ESA_CHL-fv5.0.nc"
ds_chl = xr.open_dataset(chl_path)

# Extract variables
chlor_data = ds_chl['chlor_a']

# Define region coordinates for Lambert's Bay to False Bay
lat_min, lat_max = -35.0, -30.0
lon_min, lon_max = 14.0, 20.0

# Subset chlorophyll data for the region
region_chl_data = chlor_data.sel(
    lat=slice(lat_max, lat_min),  # Flip latitudes since they decrease
    lon=slice(lon_min, lon_max)
)

# Group data by month
monthly_chlorophyll = region_chl_data.groupby('time.month').mean()

# Create faceted figure for monthly maps
fig, axes = plt.subplots(3, 4, figsize=(15, 12), subplot_kw={'projection': ccrs.PlateCarree()})
axes = axes.ravel()  # Flatten the axes array for easier indexing

# Define gridlines and months for labels
gridlines_settings = {'draw_labels': True, 'linewidth': 0.5, 'color': 'gray', 'alpha': 0.7, 'linestyle': '--'}
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

# Plot each month's map
vmin, vmax = -1, 1  # Logarithmic range for chlorophyll concentrations
cmap = 'viridis'
contour_handles = []

for month, ax in zip(range(1, 13), axes):
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, color='grey')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    
    # Add gridlines
    gl = ax.gridlines(**gridlines_settings)
    gl.right_labels = False
    gl.top_labels = False
    
    # Plot chlorophyll concentration for the month
    chl_plot = ax.contourf(
        monthly_chlorophyll.lon, monthly_chlorophyll.lat,
        np.log10(monthly_chlorophyll.sel(month=month)), 
        cmap=cmap, levels=np.linspace(vmin, vmax, 100),
        transform=ccrs.PlateCarree()
    )
    
    # Save the handle for the color bar
    contour_handles.append(chl_plot)
    
    # Add title for each month
    ax.set_title(months[month - 1], fontsize=12)

# Add a single vertical color bar for the entire figure
cbar = plt.colorbar(
    contour_handles[0], ax=axes, pad=0.05, 
    fraction=0.03, aspect=20, location='bottom'
)

# Adjust the colorbar label
cbar.set_label(r'Log10(Chlorophyll-a Concentration) (mg/m³)')



# Adjust layout
plt.tight_layout()
plt.show()