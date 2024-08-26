# use remapcon to crop remo2009 because of gridcell issues (center/corner)

import os
import glob
from cdo import Cdo

cdo = Cdo()

file_template = "/home/climatedata/obs/regrid_data_0.95/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc"
file_grid = "/home/climatedata/temp-eur11/regcm/clt/clt_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_ICTP-RegCM4-6_v2_day_19700101-19701231.nc"
file_zz = "/home/climatedata/temp-eur11/regcm/zz-temp.nc"

path_in = "/home/climatedata/temp-eur11/regcm/"
path_out = "/home/climatedata/eurocordex2-full/split/"

variables = ["rsus", "rlds", "rlus"]


for i_var in variables:
  path_in_var = os.path.join(path_in, i_var)
  path_out_var = os.path.join(path_out, i_var)
  
  os.makedirs(path_out_var, exist_ok=True)
  
  all_files = glob.glob(os.path.join(path_in_var, "*.nc"))
  all_files.sort()

  for file_in in all_files:
    file_out = os.path.join(path_out_var, os.path.basename(file_in))
    if not os.path.exists(file_out):
      cdo.remapnn(file_template, input=" -setgrid,"+file_grid+" "+file_in, output=file_zz)
      cdo.delname("lat_2,lon_2", input=file_zz, output=file_out)



