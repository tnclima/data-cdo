# remap to regular lonlat and crop RCMs as specified by coords file
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_coords = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_orario/coords_lonlat_var_x0.029_y0.02.txt"

# orog
file_in = "/home/climatedata/temp-cmcc-dds/vhr-pro/orog_cmcc2km_tn.nc"
file_out = "/home/climatedata/climate_scenarios_appa/dati_topografia/orog_vhrpro_tn.nc"
cdo.remapbil(file_coords, input=file_in, output=file_out)


# other vars
path_in = "/home/climatedata/temp-cmcc-dds/vhr-pro/"
path_out = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_orario/"


variables = os.listdir(path_in)
variables.sort()

for var in variables:
    
    os.makedirs(os.path.join(path_out, var), exist_ok=True)
    
    all_files = glob.glob(os.path.join(path_in, var, "*.nc"))
    all_files.sort()

    for file_in in all_files:

        file_out = os.path.join(path_out, var, os.path.basename(file_in))
        
        if not os.path.exists(file_out):
            cdo.remapbil(file_coords, input=file_in, output=file_out)

