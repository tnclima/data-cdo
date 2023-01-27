# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex/merged/"
path_out = "/home/climatedata/eurocordex/indices/"

all_variables = os.listdir(path_in)
all_variables.sort()
all_variables = [x for x in all_variables if x != "orog"]
# all_variables = all_variables[0:4] # only a subset to start with

for i,var in enumerate(all_variables):
  
  all_files_rcm = os.listdir(os.path.join(path_in, var))
  all_files_rcm.sort()
  
  path_annual = os.path.join(path_out, "mean" + "_" + var, "annual")
  os.makedirs(path_annual, exist_ok=True)
  path_seasonal = os.path.join(path_out, "mean" + "_" + var, "seasonal")
  os.makedirs(path_seasonal, exist_ok=True)
  
  for j,file_rcm in enumerate(all_files_rcm):
    
    file_in = os.path.join(path_in, var, file_rcm)
    
    file_out = os.path.join(path_annual, file_rcm)
    if not os.path.exists(file_out):
      cdo.yearmean(input=file_in, output=file_out)
    
    file_out = os.path.join(path_seasonal, file_rcm)
    if not os.path.exists(file_out):
      cdo.seasmean(input=file_in, output=file_out)
    
