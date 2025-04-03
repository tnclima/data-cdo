# remap to regular lonlat and crop RCMs as specified by coords file
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_coords = "/home/climatedata/highlander/Daily_lonlat/coords_lonlat_var_xy.txt"
# file_coords = "/home/climatedata/highlander/Daily_lonlat/coords_lonlat_same_xy.txt"

# orog
file_in = "/home/climatedata/highlander/elevation.nc"
file_out = "/home/climatedata/highlander/elevation_lonlat.nc"
cdo.remapbil(file_coords, input=file_in, output=file_out)


# other vars
path_in = "/home/climatedata/highlander/Daily/"
path_out = "/home/climatedata/highlander/Daily_lonlat/"

files_in = glob.glob(os.path.join(path_in, "*.nc"))
files_in.sort()

for file_in in files_in:

    file_out = os.path.join(path_out, os.path.basename(file_in))
    cdo.remapbil(file_coords, input=file_in, output=file_out)

