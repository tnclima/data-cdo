# calc climatologies from daily data

import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/obs/ALPINE-TST/daily_1km_lonlat/"
path_out = "/home/climatedata/obs/ALPINE-TST/clim_1km_lonlat/"

all_files = os.listdir(path_in)
all_files.sort()

for file in all_files:

  file_input = " -selyear,1991/2020 " + os.path.join(path_in, file)
  file_output = os.path.join(path_out, file.replace("19910101-20210731", "1991-2020"))
  if not os.path.exists(file_output):
    if "prec" in file:
      cdo.ymonmean(input= " -monsum " + file_input, output=file_output)
    else:
      cdo.ymonmean(input=file_input, output=file_output)
      
