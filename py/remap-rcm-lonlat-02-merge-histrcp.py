# remap to regular lonlat and crop RCMs as specified by coords file
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_coords = "/home/michael.matiu/projects/downscaling/data/coords_tnaa.txt"

# orog ---------------------------------------------- #

path_in = "/home/climatedata/eurocordex2-rest/orog/"
path_out = "/home/climatedata/downscaling/rcm_lonlat_tnaa/orog/"
os.makedirs(path_out, exist_ok=True)

all_files = os.listdir(path_in)
all_files.sort()

for j,file_loop in enumerate(all_files):
  
  file_in = os.path.join(path_in, file_loop)
  file_out = os.path.join(path_out, file_loop)
  cdo.remapbil(file_coords, input=file_in, output=file_out)




# other vars ---------------------------------------------- #

path_in = "/home/climatedata/eurocordex2-rest/merged/"
path_out = "/home/climatedata/downscaling/rcm_lonlat_tnaa/"

variables = ["tas", "tasmin", "tasmax", "pr"]

for var in variables:

    all_files_rcm = os.listdir(os.path.join(path_in, var))
    all_files_rcm.sort()
    
    all_files_rcm_hist = [x for x in all_files_rcm if "historical" in x]
    all_files_rcm_loop = [x for x in all_files_rcm if not "historical" in x]
    
    os.makedirs(os.path.join(path_out, var), exist_ok=True)
    
    for j,file_loop in enumerate(all_files_rcm_loop):
        
        # hist/rcp
        file_rcp = os.path.join(path_in, var, file_loop)
        (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop[:-3].split("_")
        file_hist = os.path.join(path_in, var, 
                                 [x for x in all_files_rcm_hist if 
                                  gcm in x and ens in x and rcm in x and ds in x][0])
        # update start date in filename
        file_rcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
        file_out = os.path.join(path_out, var, file_rcm)

        # skip rest of loop if first file exists
        if os.path.exists(file_out):
            continue
        
        remap_modifier = " -remapbil," + file_coords + " "
        cdo.mergetime(input=remap_modifier + file_hist + " " + remap_modifier + file_rcp, 
                      output=file_out)

