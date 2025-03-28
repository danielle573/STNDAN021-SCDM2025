# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 17:20:25 2025

@author: STNDAN021
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib_scalebar.scalebar import ScaleBar


grd_path = 'C:/Users/STNDAN021/Downloads/GMRTv4_3_0_20250327topo.grd'
ds = xr.open_dataset(grd_path, engine='netcdf4')


x_range = ds['x_range'].values
y_range = ds['y_range'].values
spacing = ds['spacing'].values
z = ds['z'].values

nx = int((x_range[1] - x_range[0]) / spacing[0]) + 1
ny = int((y_range[1] - y_range[0]) / spacing[1]) + 1

z_grid = z.reshape((ny, nx))
lon = np.linspace(x_range[0], x_range[1], nx)
lat = np.linspace(y_range[0], y_range[1], ny)
lon2d, lat2d = np.meshgrid(lon, lat)


lon_min, lon_max = 72.5, 74.5
lat_min, lat_max = -1.0, 5.0

lon_mask = (lon >= lon_min) & (lon <= lon_max)
lat_mask = (lat >= lat_min) & (lat <= lat_max)
lon_cropped = lon[lon_mask]
lat_cropped = lat[lat_mask]
z_cropped = z_grid[np.ix_(lat_mask, lon_mask)]
lon2d_cropped, lat2d_cropped = np.meshgrid(lon_cropped, lat_cropped)


land_mask = z_cropped > 0
z_cropped = np.where(land_mask, np.nan, z_cropped)  # keep ocean only


fig, ax = plt.subplots(figsize=(10, 12), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([lon_min, lon_max, lat_min, lat_max])
ax.set_title('Primary Bathymetry Map of Thinadhoo Atoll Region, Maldives', fontsize=14)


depth_plot = ax.pcolormesh(lon2d_cropped, lat2d_cropped, z_cropped,
                           cmap='Blues_r', shading='auto', zorder=0)


ax.contourf(
    lon2d_cropped, lat2d_cropped, land_mask.astype(int),
    levels=[0.5, 1.5],
    colors=['darkgray'], zorder=2, alpha=1.0
)


ax.contour(
    lon2d_cropped, lat2d_cropped, land_mask.astype(int),
    levels=[0.5],
    colors='black', linewidths=0.8, zorder=3
)


contour_levels = [100, 200, 500, 1000, 2000, 3000]
if not np.all(np.isnan(z_cropped)):
    contours = ax.contour(
        lon2d_cropped, lat2d_cropped, -z_cropped,  # Flip sign to make contours positive
        levels=contour_levels,
        colors='black', linewidths=0.4, linestyles='dashed', alpha=0.5
    )
    ax.clabel(contours, fmt='%d m', fontsize=7, inline_spacing=3)


ax.coastlines(resolution='10m', linewidth=0.6)
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
gl.top_labels = False
gl.right_labels = False


cb = plt.colorbar(depth_plot, ax=ax, orientation='vertical', label='Depth (m)')


islands = {
    "Malé": (73.51, 4.175),
    "Thinadhoo": (73.00, 0.53)
}
for name, (x, y) in islands.items():
    ax.text(x, y + 0.1, name, fontsize=9, fontweight='bold', color='black',  # label slightly above
            transform=ccrs.PlateCarree(), ha='center', va='bottom', zorder=4)

# === Scalebar (no text) ===
scalebar = ScaleBar(1, units="km", dimension="si-length", location='lower left',
                    length_fraction=0.25, scale_loc='none', box_alpha=0.2)
ax.add_artist(scalebar)

plt.tight_layout()
plt.show()


# ---------------- Zoomed-In Map ----------------


zoom_lon_min, zoom_lon_max = 72.85, 73.15
zoom_lat_min, zoom_lat_max = 0.4, 0.65

zoom_lon_mask = (lon >= zoom_lon_min) & (lon <= zoom_lon_max)
zoom_lat_mask = (lat >= zoom_lat_min) & (lat <= zoom_lat_max)
zoom_lon = lon[zoom_lon_mask]
zoom_lat = lat[zoom_lat_mask]
zoom_z = z_grid[np.ix_(zoom_lat_mask, zoom_lon_mask)]
zoom_lon2d, zoom_lat2d = np.meshgrid(zoom_lon, zoom_lat)


land_mask = zoom_z > 0
zoom_z_ocean = np.where(zoom_z > 0, np.nan, zoom_z)


fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([zoom_lon_min, zoom_lon_max, zoom_lat_min, zoom_lat_max])
ax.set_title('Secondary Bathymetry of Thinadhoo Atoll, Maldives', fontsize=13)


depth_plot = ax.pcolormesh(
    zoom_lon2d, zoom_lat2d, zoom_z_ocean,
    cmap='Blues_r', shading='auto', zorder=0
)


ax.contourf(
    zoom_lon2d, zoom_lat2d, land_mask.astype(int),
    levels=[0.5, 1.5],
    colors=['darkgray'], zorder=2, alpha=1.0
)


ax.contour(
    zoom_lon2d, zoom_lat2d, land_mask.astype(int),
    levels=[0.5],
    colors='black', linewidths=0.8, zorder=3
)


if not np.all(np.isnan(zoom_z_ocean)):
    zoom_contours = ax.contour(
        zoom_lon2d, zoom_lat2d, -zoom_z_ocean,
        levels=[100, 200, 500, 1000, 2000, 3000],
        colors='black', linewidths=0.4, linestyles='dashed', alpha=0.5
    )
    ax.clabel(zoom_contours, fmt='%d m', fontsize=7, inline_spacing=3)




cb = plt.colorbar(depth_plot, ax=ax, orientation='vertical', label='Depth (m)')


gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
gl.top_labels = False
gl.right_labels = False

plt.tight_layout()
plt.show()
