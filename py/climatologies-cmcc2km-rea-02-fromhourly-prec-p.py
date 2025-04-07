# calc climatologies from daily data

import os
import glob
import shutil
from cdo import Cdo

cdo = Cdo()

cdo.env = {"CDO_PCTL_NBINS" : "1001"}

path_out = "/home/climatedata/CMCC_COSMO_2km/vhr-rea-tnaa-lonlat-clim/seasonal/"
path_tmp = "/home/climatedata/CMCC_COSMO_2km/zz_tmp/"

# if os.path.exists(path_tmp):
#   shutil.rmtree(path_tmp)
os.makedirs(path_tmp, exist_ok=True)


file_output = "/home/climatedata/CMCC_COSMO_2km/vhr-rea-tnaa-lonlat-hourly-pr-merged/pr_19910101-20201231.nc"
if not os.path.exists(file_output):
  file_input = "/home/climatedata/CMCC_COSMO_2km/vhr-rea-tnaa-lonlat-hourly-pr-merged/pr_19810101-20231231.nc"
  cdo.selyear("1991/2020", input=file_input, output=file_output)


file_input = "/home/climatedata/CMCC_COSMO_2km/vhr-rea-tnaa-lonlat-hourly-pr-merged/pr_19910101-20201231.nc"

file_out95 = os.path.join(path_out, "VHR-REA-2km_prec-hourly-p95_1991-2020.nc")
file_out99 = os.path.join(path_out, "VHR-REA-2km_prec-hourly-p99_1991-2020.nc")
file_out999 = os.path.join(path_out, "VHR-REA-2km_prec-hourly-p99.9_1991-2020.nc")
  
if not os.path.exists(file_out999):
  
  file_tmp_min = os.path.join(path_tmp, "tmp_min.nc")
  file_tmp_max = os.path.join(path_tmp, "tmp_max.nc")
  cdo.yseasmin(input=file_input, output=file_tmp_min)
  cdo.yseasmax(input=file_input, output=file_tmp_max)
  
  cdo.yseaspctl(95, 
              input=file_input+" "+file_tmp_min+" "+file_tmp_max, 
              output=file_out95)
  cdo.yseaspctl(99, 
              input=file_input+" "+file_tmp_min+" "+file_tmp_max, 
              output=file_out99)
  cdo.seaspctl(99.9, 
              input=file_input+" "+file_tmp_min+" "+file_tmp_max, 
              output=file_out999)

