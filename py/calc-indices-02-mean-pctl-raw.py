# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex/merged/"
path_out = "/home/climatedata/eurocordex/indices/"
path_temp = "/home/climatedata/eurocordex/tmp/"

pctl = [1, 5, 10, 50, 90, 95, 99]
os.makedirs(path_temp, exist_ok=True)
tmp_pct_yearmin = os.path.join(path_temp, "tmp_pct_yearmin.nc")
tmp_pct_yearmax = os.path.join(path_temp, "tmp_pct_yearmax.nc")
tmp_pct_seasmin = os.path.join(path_temp, "tmp_pct_seasmin.nc")
tmp_pct_seasmax = os.path.join(path_temp, "tmp_pct_seasmax.nc")

tmp_merge_hist = os.path.join(path_temp, "tmp_merge_hist.nc")

all_variables = os.listdir(path_in)
all_variables.sort()
all_variables = [x for x in all_variables if x != "orog"]
# all_variables = all_variables[0:4] # only a subset to start with

for i,var in enumerate(all_variables):
  
  if not "Adjust" in var:
    
    all_files_rcm = os.listdir(os.path.join(path_in, var))
    all_files_rcm.sort()
    
    all_files_rcm_hist = [x for x in all_files_rcm if "historical" in x]
    all_files_rcm_loop = [x for x in all_files_rcm if not "historical" in x]
    
    path_mean_annual = os.path.join(path_out, var + "_mean_annual")
    os.makedirs(path_mean_annual, exist_ok=True)
    path_mean_seasonal = os.path.join(path_out,  var + "_mean_seasonal")
    os.makedirs(path_mean_seasonal, exist_ok=True)
    paths_pctl_annual = [os.path.join(path_out, var + "_" + str(p) + "pct_annual") for p in pctl]
    [os.makedirs(x, exist_ok=True) for x in paths_pctl_annual]
    paths_pctl_seasonal = [os.path.join(path_out, var + "_" + str(p) + "pct_seasonal") for p in pctl]
    [os.makedirs(x, exist_ok=True) for x in paths_pctl_seasonal]
    
    for j,file_loop in enumerate(all_files_rcm_loop):
      
      # merge hist temporarily
      file_rcp = os.path.join(path_in, var, file_loop)
      (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop[:-3].split("_")
      file_hist = os.path.join(path_in, var, 
                               [x for x in all_files_rcm_hist if 
                                gcm in x and ens in x and rcm in x and ds in x][0])
      cdo.mergetime(input=file_hist + " " + file_rcp, output=tmp_merge_hist)
      file_in = tmp_merge_hist
      # update start date in filename
      file_rcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
      
      
      file_out = os.path.join(path_mean_annual, file_rcm)
      if not os.path.exists(file_out):
        cdo.yearmean(input=file_in, output=file_out)
      
      file_out = os.path.join(path_mean_seasonal, file_rcm)
      if not os.path.exists(file_out):
        cdo.seasmean(input=file_in, output=file_out)
      
      # pctl extra
      cdo.yearmin(input=file_in, output=tmp_pct_yearmin)
      cdo.yearmax(input=file_in, output=tmp_pct_yearmax)
      cdo.seasmin(input=file_in, output=tmp_pct_seasmin)
      cdo.seasmax(input=file_in, output=tmp_pct_seasmax)
      
      for i,p in enumerate(pctl):
        
        file_out = os.path.join(paths_pctl_annual[i], file_rcm)
        if not os.path.exists(file_out):
          cdo.yearpctl(p, input=file_in+" "+tmp_pct_yearmin+" "+tmp_pct_yearmax, output=file_out)
        
        file_out = os.path.join(paths_pctl_seasonal[i], file_rcm)
        if not os.path.exists(file_out):
          cdo.seaspctl(p, input=file_in+" "+tmp_pct_seasmin+" "+tmp_pct_seasmax, output=file_out)
      

 

    
