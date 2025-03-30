# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 13:14:38 2025

@author: mfaku
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean

# Load the dataset
gmrt_path = r"C:\Users\mfaku\Downloads\GMRT_West_coast_SA.grd"
ds = xr.open_dataset(gmrt_path)

da = ds.altitude
da.plot()

plt.show()  # I did this to show whether the plot has issues or it can be used. 
# It showed the plot window and the plot can be used. 

# Extract relevant variables
lon = ds['lon'].values 
lat = ds['lat'].values
bathy = ds['altitude']

# Create coordinate grid
lon2d, lat2d = np.meshgrid(lon, lat)

# Mask land values
masked_bathy = np.where(bathy < 0, bathy, np.nan)

# Define coastal cities and their coordinates
cities = {
    "False Bay": (18.43, -34.20),
    "Cape Town": (18.42, -33.92),
    "Lamberts Bay": (18.31, -32.09),
}

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})

# Set extent
ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=ccrs.PlateCarree())

# Add features
ax.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='black', alpha=0.6)
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.coastlines(resolution='10m')


# Add bathymetry
pc = ax.pcolormesh(lon2d, lat2d, masked_bathy, cmap=cmocean.cm.deep, shading='auto', transform=ccrs.PlateCarree())

# Add contour lines
contour_levels = [-5000, -2000, -1000, -500, -200, -100, -50, -20, 0]
ax.contour(lon2d, lat2d, masked_bathy, levels=contour_levels, colors='black', linewidths=0.7, transform=ccrs.PlateCarree())

# Add city markers and labels
for city, (lon_c, lat_c) in cities.items():
    ax.scatter(lon_c, lat_c, color='red', marker='o', edgecolor='black', zorder=5, transform=ccrs.PlateCarree())
    ax.text(lon_c + 0.1, lat_c, city, fontsize=10, color='black', transform=ccrs.PlateCarree())
    
# Add gridlines
gridlines = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
gridlines.right_labels = False
gridlines.top_labels = False

# Add colorbar
cbar = plt.colorbar(pc, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label("Depth (m)")

# Title
ax.set_title("Bathymetry Map of South Africa's West Coast")

plt.tight_layout()
plt.savefig("Bathymetry_South_Africa.pdf", bbox_inches='tight')
plt.show()
