# interpolate/regridd cdo or iris
import os
import glob
from cdo import Cdo

cdo = Cdo()

# project with terra (separate file)

# merge back


all_years = range(1991, 2022)
for year in all_years:
  
  # 250m ll
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_split_day_prec_lonlat/" + str(year) + "*")
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/hourly_prec_250m_lonlat/",
                             "ALPINE-TST-250_hourly_prec_" + str(year) + ".nc")
  if not os.path.exists(file_output):
    cdo.mergetime(input=file_input, output=file_output)
  
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_split_day_temp_lonlat/" + str(year) + "*")
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/hourly_temp_250m_lonlat/",
                             "ALPINE-TST-250_hourly_temp_" + str(year) + ".nc")
  if not os.path.exists(file_output):
    cdo.mergetime(input=file_input, output=file_output)


  # 1km ll
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_split_day_prec_lonlat_1km/" + str(year) + "*")
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/hourly_prec_1km_lonlat/",
                             "ALPINE-TST-1km_hourly_prec_" + str(year) + ".nc")
  if not os.path.exists(file_output):
    cdo.mergetime(input=file_input, output=file_output)
  
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_split_day_temp_lonlat_1km/" + str(year) + "*")
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/hourly_temp_1km_lonlat/",
                             "ALPINE-TST-1km_hourly_temp_" + str(year) + ".nc")
  if not os.path.exists(file_output):
    cdo.mergetime(input=file_input, output=file_output)


  # 1km utm
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_split_day_prec_1km/" + str(year) + "*")
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/hourly_prec_1km_utm/",
                             "ALPINE-TST-1km_hourly_prec_" + str(year) + ".nc")
  if not os.path.exists(file_output):
    cdo.mergetime(input=file_input, output=file_output)
  
  file_input = glob.glob("/home/climatedata/obs/ALPINE-TST/zz_split_day_temp_1km/" + str(year) + "*")
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/hourly_temp_1km_utm/",
                             "ALPINE-TST-1km_hourly_temp_" + str(year) + ".nc")
  if not os.path.exists(file_output):
    cdo.mergetime(input=file_input, output=file_output)


# clean up manually!
