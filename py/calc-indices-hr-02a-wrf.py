# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/run_4km_GAR_anna/hist/"
# path_out = "/home/climatedata/temp-analysis/wrf-anna/"
path_temp = "/home/climatedata/temp-analysis/tmp/"

# os.makedirs(path_out, exist_ok=True)
os.makedirs(path_temp, exist_ok=True)


# calc daily sums/means first
years = os.listdir(path_in)
years.sort()

for y in years:
  
  tmp_merged = os.path.join(path_temp, "merged_" + y + ".nc")
  if not os.path.exists(tmp_merged):
    cdo.mergetime(input=os.path.join(path_in, y, "pr_*"), output=tmp_merged)

  tmp_daily = os.path.join(path_temp, "daily_" + y + ".nc")
  if not os.path.exists(tmp_daily):
    cdo.daysum(input=tmp_merged, output=tmp_daily)

# merge daily
file_out_dailymerged = "/home/climatedata/temp-analysis/wrf-anna/daily/historical_pr_1979-2008.nc"
if not os.path.exists(file_out_dailymerged):
  cdo.mergetime(input=os.path.join(path_temp, "daily_*.nc"), 
                output=file_out_dailymerged)



# calc indices (pr only)
path_out = "/home/climatedata/temp-analysis/wrf-anna/indices/"
os.makedirs(path_out, exist_ok=True)

pctl = [1, 5, 10, 50, 90, 95, 99]
tmp_pct_yearmin = os.path.join(path_temp, "tmp_pct_yearmin.nc")
tmp_pct_yearmax = os.path.join(path_temp, "tmp_pct_yearmax.nc")
tmp_pct_seasmin = os.path.join(path_temp, "tmp_pct_seasmin.nc")
tmp_pct_seasmax = os.path.join(path_temp, "tmp_pct_seasmax.nc")

file_in = file_out_dailymerged

# means    
file_out = os.path.join(path_out, "hist_pr_mean_annual.nc")
if not os.path.exists(file_out):
  cdo.yearmean(input=file_in, output=file_out)

file_out = os.path.join(path_out, "hist_pr_mean_seasonal.nc")
if not os.path.exists(file_out):
  cdo.seasmean(input=file_in, output=file_out)

# pctl extra
cdo.yearmin(input=file_in, output=tmp_pct_yearmin)
cdo.yearmax(input=file_in, output=tmp_pct_yearmax)
cdo.seasmin(input=file_in, output=tmp_pct_seasmin)
cdo.seasmax(input=file_in, output=tmp_pct_seasmax)

for i,p in enumerate(pctl):
  
  file_out = os.path.join(path_out, "hist_pr_" + str(p) + "pct_annual.nc")
  if not os.path.exists(file_out):
    cdo.yearpctl(p, input=file_in+" "+tmp_pct_yearmin+" "+tmp_pct_yearmax, output=file_out)
  
  file_out = os.path.join(path_out, "hist_pr_" + str(p) + "pct_seasonal.nc")
  if not os.path.exists(file_out):
    cdo.seaspctl(p, input=file_in+" "+tmp_pct_seasmin+" "+tmp_pct_seasmax, output=file_out)
    

  
    
