# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:49:54 2025

@author: mfaku
"""

# Plotting oceanographic data and time series 

## Part one
import os
import pandas as pd
import matplotlib.pyplot as plt  # Ensure this import is included

# Load the file (replace with your file path)
file_path = r"C:\Users\mfaku\Downloads\CTD_data.csv"  # Update with your actual path

# Check if the file exists before trying to load it
if os.path.exists(file_path):
    # Use raw string for sep argument
    df = pd.read_csv(file_path, header=None, sep=r'\s+')
    # Assign column names
    df.columns = ["Date", "Time", "Depth (m)", "Temperature (°C)", "Salinity (psu)"]
    print("File loaded successfully!")
else:
    print("File does not exist.")

# Create subplots
fig, ax = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

# Plot Temperature
ax[0].plot(df['Temperature (°C)'], df['Depth (m)'], color='blue')
ax[0].set_xlabel("Temperature (°C)")
ax[0].set_ylabel("Depth (m)")
ax[0].set_title("Temperature Profile")
ax[0].set_ylim(0, df['Depth (m)'].max())  # Ensures 0 is at the top

# Plot Salinity
ax[1].plot(df['Salinity (psu)'], df['Depth (m)'], color='green')
ax[1].set_xlabel("Salinity (psu)")
ax[1].set_title("Salinity Profile")
ax[1].set_ylim(0, df['Depth (m)'].max())  # Ensures 0 is at the top

# Adjust layout
plt.gca().invert_yaxis()  # Invert y-axis globally to ensure depth increases downward
plt.tight_layout()

# Save the figure before displaying
figure_path = "profile_plot.png"
plt.savefig(figure_path, dpi=300)

# Show the plot
plt.show()

# Close the figure to free memory
plt.close()







