# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex2-full/merged/"
path_out = "/home/climatedata/other-projects/zanzare/02-monthly-subset-20yr/"

# periods = [[2010, 2023], [2040, 2050], [2070, 2080]]
periods = [[2006, 2025], [2036, 2055], [2066, 2085]]

for var in ["tas", "pr"]:
  
  all_files_rcm = os.listdir(os.path.join(path_in, var))
  all_files_rcm.sort()
  
  all_files_rcm = [x for x in all_files_rcm if "_rcp85_" in x]
  
  
  for (year_min, year_max) in periods:
    
    path_out_period = os.path.join(path_out, var + "_" + str(year_min) + "-" + str(year_max))
    os.makedirs(path_out_period, exist_ok=True)
    
    for i,file_rcm in enumerate(all_files_rcm):
      
      file_in = os.path.join(path_in, var, file_rcm)
      file_out = os.path.join(path_out_period, file_rcm)
      
      prefix = " -selyear," + str(year_min) + "/" + str(year_max) + " "
      
      if not os.path.exists(file_out):
        cdo.ymonmean(input=  prefix + file_in, output=file_out)
      
    
 

    
