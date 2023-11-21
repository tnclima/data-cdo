# remap to regular lonlat and crop RCMs as specified by coords file
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_coords = "/home/climatedata/highlander/Daily_lonlat/coords_lonlat_var_xy.txt"
# file_coords = "/home/climatedata/highlander/Daily_lonlat/coords_lonlat_same_xy.txt"

# orog
# path_in = "/home/climatedata/highlander/Daily_lonlat/zz.nc"
# path_out = "/home/climatedata/highlander/Daily_lonlat/zz_ll.nc"
# os.makedirs(path_out, exist_ok=True)

# all_files = os.listdir(path_in)
# all_files.sort()

# for j,file_loop in enumerate(all_files):

  # file_in = os.path.join(path_in, file_loop)
  # file_out = os.path.join(path_out, file_loop)
  # file_in = "/home/climatedata/highlander/Daily_lonlat/zz.nc"
  # file_out = "/home/climatedata/highlander/Daily_lonlat/zz_ll_fix.nc"
  # cdo.remapbil(file_coords, input=file_in, output=file_out)


# other vars
path_in = "/home/climatedata/highlander/Daily/"
path_out = "/home/climatedata/highlander/Daily_lonlat/"

files_in = glob.glob(os.path.join(path_in, "*.nc"))
files_in.sort()

for file_in in files_in:

    file_out = os.path.join(path_out, os.path.basename(file_in))
    cdo.remapbil(file_coords, input=file_in, output=file_out)

