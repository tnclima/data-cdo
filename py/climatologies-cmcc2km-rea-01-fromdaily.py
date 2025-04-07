# calc climatologies from daily data

import os
import glob
import re
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/CMCC_COSMO_2km/vhr-rea-tnaa-lonlat-daily/"
path_out = "/home/climatedata/CMCC_COSMO_2km/vhr-rea-tnaa-lonlat-clim/monthly/"

all_files = os.listdir(path_in)
all_files.sort()

for file in all_files:

  file_input = " -selyear,1991/2020 " + os.path.join(path_in, file)
  file_output = os.path.join(path_out,
                             re.sub(r"1981010.-20231231", "1991-2020", file))
  if not os.path.exists(file_output):
    if "prec" in file:
      cdo.ymonmean(input= " -monsum " + file_input, output=file_output)
    else:
      cdo.ymonmean(input=file_input, output=file_output)
      
