# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_out = "/home/climatedata/temp-analysis/highlander/"
path_temp = "/home/climatedata/temp-analysis/tmp/"

os.makedirs(path_out, exist_ok=True)
os.makedirs(path_temp, exist_ok=True)

pctl = [1, 5, 10, 50, 90, 95, 99]
tmp_pct_yearmin = os.path.join(path_temp, "tmp_pct_yearmin.nc")
tmp_pct_yearmax = os.path.join(path_temp, "tmp_pct_yearmax.nc")
tmp_pct_seasmin = os.path.join(path_temp, "tmp_pct_seasmin.nc")
tmp_pct_seasmax = os.path.join(path_temp, "tmp_pct_seasmax.nc")

tmp_merge_hist = os.path.join(path_temp, "tmp_merge_hist.nc")


for var in ["pr", "tas", "tasmin", "tasmax"]:
  
  # for rcp in ["rcp45", "rcp85"]:
  for rcp in ["rcp45"]:
    
    file_in_hist = "/home/climatedata/highlander/Daily/historical_1989-2005_" + var + ".nc"
    file_in_rcp = "/home/climatedata/highlander/Daily/" + rcp + "_2006-2070_" + var + ".nc"
    
    cdo.mergetime(input=file_in_hist + " " + file_in_rcp, output=tmp_merge_hist)
    file_in = tmp_merge_hist
    
    # means    
    file_out = os.path.join(path_out, rcp + "_" + var + "_mean_annual.nc")
    if not os.path.exists(file_out):
      cdo.yearmean(input=file_in, output=file_out)
    
    file_out = os.path.join(path_out, rcp + "_" + var + "_mean_seasonal.nc")
    if not os.path.exists(file_out):
      cdo.seasmean(input=file_in, output=file_out)
    
    # pctl extra
    cdo.yearmin(input=file_in, output=tmp_pct_yearmin)
    cdo.yearmax(input=file_in, output=tmp_pct_yearmax)
    cdo.seasmin(input=file_in, output=tmp_pct_seasmin)
    cdo.seasmax(input=file_in, output=tmp_pct_seasmax)
    
    for i,p in enumerate(pctl):
      
      file_out = os.path.join(path_out, rcp + "_" + var + "_" + str(p) + "pct_annual.nc")
      if not os.path.exists(file_out):
        cdo.yearpctl(p, input=file_in+" "+tmp_pct_yearmin+" "+tmp_pct_yearmax, output=file_out)
      
      file_out = os.path.join(path_out, rcp + "_" + var + "_" + str(p) + "pct_seasonal.nc")
      if not os.path.exists(file_out):
        cdo.seaspctl(p, input=file_in+" "+tmp_pct_seasmin+" "+tmp_pct_seasmax, output=file_out)
    

  
    
