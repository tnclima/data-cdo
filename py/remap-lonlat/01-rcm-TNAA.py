# remap to regular lonlat and crop RCMs as specified by coords file
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_coords = "/home/michael.matiu/projects/downscaling/data/coords_tnaa.txt"

# orog
path_in = "/home/climatedata/eurocordex3-reanalysis/orog/"
path_out = "/home/climatedata/downscaling/rcm_lonlat_tnaa_eraint/orog/"
os.makedirs(path_out, exist_ok=True)

all_files = os.listdir(path_in)
all_files.sort()

for j,file_loop in enumerate(all_files):
  
  file_in = os.path.join(path_in, file_loop)
  file_out = os.path.join(path_out, file_loop)
  cdo.remapbil(file_coords, input=file_in, output=file_out)


# other vars
path_in = "/home/climatedata/eurocordex3-reanalysis/merged/"
path_out = "/home/climatedata/downscaling/rcm_lonlat_tnaa_eraint/"

variables = ["tas", "tasmin", "tasmax", "pr"]

for var in variables:

    all_files = os.listdir(os.path.join(path_in, var))
    all_files.sort()
    os.makedirs(os.path.join(path_out, var), exist_ok=True)
    
    for j,file_loop in enumerate(all_files):
  
        file_in = os.path.join(path_in, var, file_loop)
        file_out = os.path.join(path_out, var, file_loop)
        cdo.remapbil(file_coords, input=file_in, output=file_out)

