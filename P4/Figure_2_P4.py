# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 10:06:16 2025

@author: STNDAN021
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Path to your chlorophyll data file
grd_file_path = "C:/Users/STNDAN021/Downloads/ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHLY_4km_PML_CHL-fv5.0.nc"

# Step 1: Open the NetCDF file
ds_chlorophyll = xr.open_dataset(grd_file_path)

# Inspect dataset to check variables and dimensions
print("Dataset variables:", ds_chlorophyll.variables)
print("Dataset dimensions:", ds_chlorophyll.dims)

# Step 2: Extract chlorophyll, lat, lon, and time variables
chlorophyll_data = ds_chlorophyll['chlor_a']  # Chlorophyll concentration variable
lats_chlorophyll = ds_chlorophyll['lat']  # Latitude
lons_chlorophyll = ds_chlorophyll['lon']  # Longitude
time_chlorophyll = ds_chlorophyll['time']  # Time

# Check the shapes and dimensions of the lat, lon, and chlorophyll variables
print("Latitude dimensions:", lats_chlorophyll.shape)
print("Longitude dimensions:", lons_chlorophyll.shape)
print("Chlorophyll data shape:", chlorophyll_data.shape)

# Step 3: Convert the 'time' variable to pandas datetime format for easier slicing
time_chlorophyll = pd.to_datetime(time_chlorophyll.values)

# Step 4: Define region coordinates for Thinadhoo Atoll
lat_min, lat_max = -0.2056, 1.0248  # Latitude range for Thinadhoo Atoll
lon_min, lon_max = 71.4165, 74.6245  # Longitude range for Thinadhoo Atoll

# Step 5: Mask the dataset for the Thinadhoo Atoll region
lat_mask = (lats_chlorophyll >= lat_min) & (lats_chlorophyll <= lat_max)
lon_mask = (lons_chlorophyll >= lon_min) & (lons_chlorophyll <= lon_max)

# Step 6: Apply the mask and slice the data correctly
region_chlorophyll_data = chlorophyll_data.sel(lat=lats_chlorophyll[lat_mask], lon=lons_chlorophyll[lon_mask])

# Check the shape of the sliced region
print("Region chlorophyll data shape:", region_chlorophyll_data.shape)

# Step 7: Slice the data for the years 1997 to 1998
time_1997_1998 = time_chlorophyll[(time_chlorophyll >= '1997-01-01') & (time_chlorophyll <= '1998-12-31')]

# Slice the data for the time period of interest
region_chlorophyll_data_1997_1998 = region_chlorophyll_data.sel(time=time_1997_1998)

# Step 8: Check if data is selected correctly
print("Selected region shape for 1997-1998:", region_chlorophyll_data_1997_1998.shape)

# Step 9: Calculate the mean chlorophyll concentration for the time period
mean_chlorophyll_data_region = region_chlorophyll_data_1997_1998.mean(dim='time')

# Step 10: Mask invalid chlorophyll values (optional)
mean_chlorophyll_data_region = mean_chlorophyll_data_region.where(mean_chlorophyll_data_region > 0.05)  # Mask low values

# Step 11: Plot the mean chlorophyll data for the Thinadhoo Atoll region
plt.figure(figsize=(12, 10))

# Use a logarithmic scale for chlorophyll concentration
cmap_chlorophyll = plt.cm.viridis  # Choose a suitable colormap
plt.imshow(np.log(mean_chlorophyll_data_region), cmap=cmap_chlorophyll,
           extent=[lon_min, lon_max, lat_min, lat_max],
           origin='lower')

# Add a colorbar for chlorophyll concentration
plt.colorbar(label='Log(Chlorophyll Concentration) (mg/m³)')

# Add title and labels for chlorophyll plot
plt.title("Mean Chlorophyll Concentration (1997-1998) in Thinadhoo Atoll, Maldives)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Add gridlines for better readability
plt.grid(True)

# Step 12: Show the plot
plt.tight_layout()
plt.show()

