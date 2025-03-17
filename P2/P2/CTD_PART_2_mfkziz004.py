# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 12:36:28 2025

@author: mfaku
"""

## Part two 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ddmm2dd(ddmm):        
    thedeg = np.floor(ddmm/100.)     
    themin = (ddmm-thedeg*100.)/60.     
    return thedeg+themin

# Load the CSV file
file_path = r"C:\Users\mfaku\Downloads\SAA2_WC_2017_metocean_10min_avg.csv"  # Update with actual path


# Load the CSV without parsing dates to inspect column names
df = pd.read_csv(file_path, nrows=5)  # Read first 5 rows to check column names
print("Column names in the dataset:", df.columns)

# Manually check the correct time column name from printed output and replace 'Time' below
correct_time_column = "TIME_SERVER"  

# Load data with proper time indexing
df = pd.read_csv(file_path, parse_dates=[correct_time_column], index_col=correct_time_column)
df = df.replace(-999, np.nan)  # Replace missing values

# Ensure time column was parsed correctly
print(df)

# Select data up to July 4th
df_selected = df.loc[:'2017-07-04']

# Temperature time series plot
plt.style.use('grayscale')
plt.figure(figsize=(10, 5))
plt.plot(df_selected.index, df_selected['TSG_TEMP'], linewidth=1, label="Sea Temperature")
plt.plot(df_selected.index, df_selected['AIR_TEMPERATURE'], linewidth=1, label="Air Temperature")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Time Series of Temperature")
plt.legend()
plt.savefig("temperature_series.png", dpi=300)
plt.show()

## Plot a histogram 

## Choose the correct column

salinity_df = df_selected['TSG_SALINITY']

# Define the bin edges
bin_edges_salinity = np.arange(30, 35.5, 0.5)

# Plot the histogram
plt.hist(salinity_df, bins=bin_edges_salinity, edgecolor='black')

# Add labels and title
plt.xlabel('Salinity (psu)')
plt.ylabel('Frequency')
plt.title('Salinity Distribution')

# Show the plot
plt.show() 

## Calculating the mean, standard deviation and the interquartile range for 
#temperature and salinity and presenting  the results in a table.

# Calculate mean, standard deviation, and IQR for temperature and salinity
Sea_temperature_stats = {
    'Mean': df_selected['TSG_TEMP'].mean(),
    'Standard Deviation': df_selected['TSG_TEMP'].std(),
    'IQR': df_selected['TSG_TEMP'].quantile(0.75) - df_selected['TSG_TEMP'].quantile(0.25)
}

Air_temperature_stats = {
    'Mean': df_selected['AIR_TEMPERATURE'].mean(),
    'Standard Deviation': df['AIR_TEMPERATURE'].std(),
    'IQR': df_selected['AIR_TEMPERATURE'].quantile(0.75) - df_selected['AIR_TEMPERATURE'].quantile(0.25)
}

salinity_stats = {
    'Mean': df_selected['TSG_SALINITY'].mean(),
    'Standard Deviation': df_selected['TSG_SALINITY'].std(),
    'IQR': df_selected['TSG_SALINITY'].quantile(0.75) - df_selected['TSG_SALINITY'].quantile(0.25)
}

# Create a summary table
summary_stats = pd.DataFrame({
    'Air Temperature': Air_temperature_stats,
    'Sea Temperature': Sea_temperature_stats,
    'Salinity': salinity_stats
})

# Create a table for better readability
summary_stats_temp_salinity = summary_stats.T

# Display the table
print(summary_stats_temp_salinity)

## Creating the DataFrame with 'wind_speed', 'air_temperature', and 'latitude' columns

# Create the scatter plot
plt.figure(figsize=(8, 6))
scatter = plt.scatter(df_selected['WIND_SPEED_TRUE'], df_selected['AIR_TEMPERATURE'], c=df_selected['LATITUDE'], cmap='viridis', edgecolors='k')

# Add a color bar to show the latitude values
plt.colorbar(scatter, label='Latitude')

# Add labels and title
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Air Temperature (°C)')
plt.title('Scatter Plot of Wind Speed vs Air Temperature')

# Save the figure with 300 DPI resolution
plt.savefig('wind_speed_air_temperature_scatter.png', dpi=300)

# Show the plot
plt.show()
