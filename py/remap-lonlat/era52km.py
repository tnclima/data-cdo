# remap to regular lonlat and crop RCMs as specified by coords file
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_coords = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/coords_lonlat_var_xy.txt"
# file_coords = "/home/climatedata/highlander/Daily_lonlat/coords_lonlat_same_xy.txt"


file_in = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/95percentile_pr_1989_2020_noSEA.nc"
file_out = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/95percentile_pr_1989_2020_noSEA_lonlat.nc"
cdo.remapbil(file_coords, input=file_in, output=file_out)

file_in = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/95percentile_tasmax_1989_2020_noSEA.nc"
file_out = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/95percentile_tasmax_1989_2020_noSEA_lonlat.nc"
cdo.remapbil(file_coords, input=file_in, output=file_out)

file_in = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/5percentile_tasmin_1989_2020_noSEA.nc"
file_out = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/5percentile_tasmin_1989_2020_noSEA_lonlat.nc"
cdo.remapbil(file_coords, input=file_in, output=file_out)

file_in = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/Annual_wet_days_pr_1989_2020_noSEA.nc"
file_out = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/Annual_wet_days_pr_1989_2020_noSEA_lonlat.nc"
cdo.remapbil(file_coords, input=file_in, output=file_out)


# other vars
#path_in = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km"
#path_out = "/home/anna.napoli/projects/Local_Anna/Marche/dati/ERA52km/lonlat"

#files_in = glob.glob(os.path.join(path_in, "*.nc"))
#files_in.sort()

#for file_in in files_in:

#    file_out = os.path.join(path_out, os.path.basename(file_in))
#    cdo.remapbil(file_coords, input=file_in, output=file_out)

