# calculate annual and seasonal indices
# only tas and pr, annual and seasonal, mean for a start?

import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/cmip5/large-ensemble-monthly/tas/"
path_out = "/home/climatedata/cmip5/large-ensemble-monthly/tas-annual/"
path_temp = "/home/climatedata/cmip5/large-ensemble-monthly/tmp/"


os.makedirs(path_temp, exist_ok=True)
tmp_merge_hist = os.path.join(path_temp, "tmp_merge_hist.nc")

all_files = os.listdir(path_in)
all_files.sort()

all_files_hist = [x for x in all_files if "historical" in x]
all_files_loop = [x for x in all_files if not "historical" in x]
    
for j,file_loop in enumerate(all_files_loop):
      
  # merge hist temporarily
  file_rcp = os.path.join(path_in, file_loop)
  (_, _, gcm, _, ens, _) = file_loop[:-3].split("_")
  file_hist = os.path.join(path_in, 
                           [x for x in all_files_hist if gcm+"_" in x and ens in x][0])
  # update start date in filename
  file_rcm = file_loop[:-16] + file_hist[-16:-9] + file_loop[-9:]
      
  # skip rest of loop if first file exists
  if os.path.exists(os.path.join(path_out, file_rcm)):
    continue
        
  cdo.mergetime(input=file_hist + " " + file_rcp, output=tmp_merge_hist)
  file_in = tmp_merge_hist      
      
  file_out = os.path.join(path_out, file_rcm)
  if not os.path.exists(file_out):
    cdo.yearmean(input=file_in, output=file_out)
      
 

    
