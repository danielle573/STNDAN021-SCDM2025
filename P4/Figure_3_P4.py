# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 11:52:58 2025

@author: STNDAN021
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import calendar

# Load the dataset
file_path = 'ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHLY_4km_PML_CHL-fv5.0.nc'
ds = xr.open_dataset(file_path)

# Extract chlorophyll data and time
chl = ds['chlor_a']

# Compute regional average
chl_regional = chl.mean(dim=['lat', 'lon'])

# Get Thinadhoo Atoll location
thinadhoo_lat, thinadhoo_lon = 0.5305, 73.5346
chl_thinadhoo = chl.sel(lat=thinadhoo_lat, lon=thinadhoo_lon, method='nearest')

# X-axis: month names
months = [calendar.month_abbr[i] for i in range(1, 13)]  # ['Jan', 'Feb', ..., 'Dec']
x = np.arange(12)

# Plotting
plt.figure(figsize=(13, 6))
plt.plot(x, chl_regional, label='Regional Mean', marker='o', linewidth=2)
plt.plot(x, chl_thinadhoo, label='Thinadhoo Atoll', marker='s', linewidth=2)

plt.xticks(ticks=x, labels=months)
plt.title('Seasonal Cycle of Chlorophyll-a in the Maldives: Regional Average vs. Thinadhoo Atoll Region', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Chlorophyll-a Concentration (mg/m³)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

