# hourly to daily alpine-tst
import os
import glob
import shutil
from cdo import Cdo

cdo = Cdo()

# only 1km lonlat for now...

path_in_prec = "/home/climatedata/obs/ALPINE-TST/hourly_prec_1km_lonlat/"
path_in_temp = "/home/climatedata/obs/ALPINE-TST/hourly_temp_1km_lonlat/"
path_tmp = "/home/climatedata/obs/ALPINE-TST/zz_tmp/"
path_out = "/home/climatedata/obs/ALPINE-TST/daily_1km_lonlat/"

if os.path.exists(path_tmp):
  shutil.rmtree(path_tmp)

os.makedirs(path_tmp, exist_ok=True)
os.makedirs(path_out, exist_ok=True)


# tmin
file_output2 = os.path.join(path_out, "ALPINE-TST-1km_tmin_19910101-20210731.nc")
if not os.path.exists(file_output2):
  for file in os.listdir(path_in_temp):
    file_input = os.path.join(path_in_temp, file)
    file_output = os.path.join(path_tmp, file)
    cdo.daymin(input=file_input, output=file_output)
  
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_tmp/*")
  cdo.mergetime(input=file_input, output=file_output2)
  
  [os.remove(x) for x in file_input]



# tmax
file_output2 = os.path.join(path_out, "ALPINE-TST-1km_tmax_19910101-20210731.nc")
if not os.path.exists(file_output2):
  for file in os.listdir(path_in_temp):
    file_input = os.path.join(path_in_temp, file)
    file_output = os.path.join(path_tmp, file)
    cdo.daymax(input=file_input, output=file_output)
  
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_tmp/*")
  cdo.mergetime(input=file_input, output=file_output2)

  [os.remove(x) for x in file_input]

# tmean
file_output2 = os.path.join(path_out, "ALPINE-TST-1km_tmean-from-hourly_19910101-20210731.nc")
if not os.path.exists(file_output2):
  for file in os.listdir(path_in_temp):
    file_input = os.path.join(path_in_temp, file)
    file_output = os.path.join(path_tmp, file)
    cdo.daymean(input=file_input, output=file_output)
  
  
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_tmp/*")
  cdo.mergetime(input=file_input, output=file_output2)
  
  [os.remove(x) for x in file_input]


# tmean=avg(tmin,tmax)
file_output = os.path.join(path_out, "ALPINE-TST-1km_tmean-from-tmin-tmax_19910101-20210731.nc")
if not os.path.exists(file_output):
  file_input = (os.path.join(path_out, "ALPINE-TST-1km_tmin_19910101-20210731.nc") + 
                " " + 
                os.path.join(path_out, "ALPINE-TST-1km_tmax_19910101-20210731.nc"))
  cdo.ensmean(input=file_input, output=file_output)




# for prec, first mergetime because of 8-8 UTC (and other stuff)
file_prec_merged = "/home/climatedata/obs/ALPINE-TST/hourly_prec_1km_lonlat_merged/ALPINE-TST-1km_hourly_prec_19910101-20210731.nc"
if not os.path.exists(file_prec_merged):
  file_input = glob.glob(os.path.join(path_in_prec, "*"))
  cdo.mergetime(input=file_input, output=file_prec_merged)
  

# prec0-0
file_output = os.path.join(path_out, "ALPINE-TST-1km_prec-0h-0h_19910101-20210731.nc")
if not file_output:
  cdo.daysum(input=file_prec_merged, output=file_output)
  
# prec8-8 (as crespi)
file_output = os.path.join(path_out, "ALPINE-TST-1km_prec-8h-8h_19910102-20210731.nc")
if not file_output:
  file_prec_merged_shifted_daysum = os.path.join(path_tmp, "prec_merged_shifted_daysum.nc")
  cdo.daysum(input=" -shifttime,+16hour " + file_prec_merged, 
             output=file_prec_merged_shifted_daysum)
  
  cdo.delete("timestep=1,11171", 
             input=file_prec_merged_shifted_daysum, 
             output=file_output)

# 1 mergetime, 2 shifttime, 3 daysum, 4 remove first and last timestep

# cdo shifttime,+7hour
# remove incomplete days? at start and end
# merge across years...? or just add next day for each year...





