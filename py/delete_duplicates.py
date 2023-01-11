##############################################################################
#
# This script deletes duplicates in date
#
# 18 Dec, 2022 
# Anna
##############################################################################
import xarray as xr
import numpy as np
import os

path_in = "/home/climatedata/obs/SWISS/setgrid_noDuplicates/"

# read the dataset with duplicates
infile = os.path.join(path_in,"TmaxD_ch02h.lonlat_1971-2021.nc")

ds = xr.open_dataset(infile)
print(ds['time'])

# Numpy provides the function np.unique to create an index list of unique time 
# records of a dataset or array
_, index = np.unique(ds['time'], return_index=True)
print(index)

# create a new dataset which doesn't contain time record duplicates
ds_unique = ds.isel(time=index)
print(ds_unique['time'])

# write the dataset with unique time records to a new netCDF file
ds_unique.to_netcdf(os.path.join(path_in,"TmaxD_ch02h.lonlat_1971-2021_NoDuplicates.nc"))
