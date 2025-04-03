# interpolate/regridd cdo or iris
import os
import glob
from cdo import Cdo

cdo = Cdo()


# split year-mon

path_in = "/home/climatedata/obs/ALPINE-TST/hourly_prec_250m_utm/"
for file in os.listdir(path_in):
  file_input = os.path.join(path_in, file)
  file_output = "/home/climatedata/obs/ALPINE-TST/zz_split_ym_prec/"
  cdo.splityearmon(input=file_input, output=file_output)
  
path_in = "/home/climatedata/obs/ALPINE-TST/hourly_temp_250m_utm/"
for file in os.listdir(path_in):
  file_input = os.path.join(path_in, file)
  file_output = "/home/climatedata/obs/ALPINE-TST/zz_split_ym_temp/"
  cdo.splityearmon(input=file_input, output=file_output)



# split day

path_in = "/home/climatedata/obs/ALPINE-TST/zz_split_ym_prec/"
for file in os.listdir(path_in):
  file_input = os.path.join(path_in, file)
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/zz_split_day_prec/",
                             file[0:6])
  cdo.splitday(input=file_input, output=file_output)
  
  

path_in = "/home/climatedata/obs/ALPINE-TST/zz_split_ym_temp/"
for file in os.listdir(path_in):
  file_input = os.path.join(path_in, file)
  file_output = os.path.join("/home/climatedata/obs/ALPINE-TST/zz_split_day_temp/",
                             file[0:6])
  cdo.splitday(input=file_input, output=file_output)



# project with terra (separate file)

# clean up manually!
