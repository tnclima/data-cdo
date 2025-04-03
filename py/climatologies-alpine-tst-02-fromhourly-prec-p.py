# calc climatologies from daily data

import os
import glob
import shutil
from cdo import Cdo

cdo = Cdo()

cdo.env = {"CDO_PCTL_NBINS" : "1001"}

path_out = "/home/climatedata/obs/ALPINE-TST/clim_1km_lonlat/seasonal/"
path_tmp = "/home/climatedata/obs/ALPINE-TST/zz_tmp/"

# if os.path.exists(path_tmp):
#   shutil.rmtree(path_tmp)
os.makedirs(path_tmp, exist_ok=True)

file_input = "/home/climatedata/obs/ALPINE-TST/hourly_prec_1km_lonlat_merged/ALPINE-TST-1km_hourly_prec_19910101-20201231.nc"

file_out95 = os.path.join(path_out, "ALPINE-TST-1km_prec-hourly-p95_1991-2020.nc")
file_out99 = os.path.join(path_out, "ALPINE-TST-1km_prec-hourly-p99_1991-2020.nc")
file_out999 = os.path.join(path_out, "ALPINE-TST-1km_prec-hourly-p99.9_1991-2020.nc")
  
if not os.path.exists(file_out999):
  
  file_tmp_min = os.path.join(path_tmp, "tmp_min.nc")
  file_tmp_max = os.path.join(path_tmp, "tmp_max.nc")
  cdo.timmin(input=file_input, output=file_tmp_min)
  cdo.timmax(input=file_input, output=file_tmp_max)
  
  cdo.seaspctl(95, 
              input=file_input+" "+file_tmp_min+" "+file_tmp_max, 
              output=file_out95)
  cdo.seaspctl(99, 
              input=file_input+" "+file_tmp_min+" "+file_tmp_max, 
              output=file_out99)
  cdo.seaspctl(99.9, 
              input=file_input+" "+file_tmp_min+" "+file_tmp_max, 
              output=file_out999)

