# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_out = "/home/climatedata/obs/data_in_time/mean_pctl/"
path_temp = "/home/climatedata/obs/data_in_time/tmp/"

os.makedirs(path_out, exist_ok=True)
os.makedirs(path_temp, exist_ok=True)

all_files = dict(
  # tas_CRESPI = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/DailySeries_1980_2018_MeanTemp.nc",
  # pr_CRESPI = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/DailySeries_1980_2018_Prec.nc",
  tasmax_CRESPI = "/home/climatedata/obs/CRESPI/daily_1km/DailySeries_1980_2020_MaxTemp.nc",
  tasmin_CRESPI = "/home/climatedata/obs/CRESPI/daily_1km/DailySeries_1980_2020_MinTemp.nc",
  pr_CRESPI = "/home/climatedata/obs/CRESPI/daily_1km/DailySeries_1980_2020_Prec.nc",
  # pr_HYRAS = "/home/climatedata/obs/HYRAS/pr_hyras_1_1951-2022_v3-0_de.nc",
  # tas_HYRAS = "/home/climatedata/obs/HYRAS/tas_hyras_5_1951-2015_v4-0_de.nc",
  # tasmax_HYRAS = "/home/climatedata/obs/HYRAS/tmax_hyras_5_1951-2015_v4-0_de.nc",
  # tasmin_HYRAS = "/home/climatedata/obs/HYRAS/tmin_hyras_5_1951-2015_v4-0_de.nc",
  pr_SLOCLIM = "/home/climatedata/obs/SLOCLIM/sloclim_pcp.nc",
  tasmax_SLOCLIM = "/home/climatedata/obs/SLOCLIM/sloclim_tmax_h.nc",
  tasmin_SLOCLIM = "/home/climatedata/obs/SLOCLIM/sloclim_tmin_h.nc",
  pr_SPARTACUS = "/home/climatedata/obs/SPARTACUS/Prec_day_1961-2022.nc",
  tasmax_SPARTACUS = "/home/climatedata/obs/SPARTACUS/Tmax_day_1961-2022.nc",
  tasmin_SPARTACUS = "/home/climatedata/obs/SPARTACUS/Tmin_day_1961-2022.nc",
  pr_SWITZERLAND = "/home/climatedata/obs/SWITZERLAND/setgrid_noDuplicates/RhiresD_ch02h.lonlat_1961-2021_NoDuplicates.nc",
  tas_SWITZERLAND = "/home/climatedata/obs/SWITZERLAND/setgrid_noDuplicates/TabsD_ch02h.lonlat_1961-2021_NoDuplicates.nc",
  tasmax_SWITZERLAND = "/home/climatedata/obs/SWITZERLAND/setgrid_noDuplicates/TmaxD_ch02h.lonlat_1971-2021_NoDuplicates.nc",
  tasmin_SWITZERLAND = "/home/climatedata/obs/SWITZERLAND/setgrid_noDuplicates/TminD_ch02h.lonlat_1971-2021_NoDuplicates.nc"
)



for lbl, file_in in all_files.items():

  pctl = [1, 5, 10, 50, 90, 95, 99]
  tmp_pct_yearmin = os.path.join(path_temp, "tmp_pct_yearmin.nc")
  tmp_pct_yearmax = os.path.join(path_temp, "tmp_pct_yearmax.nc")
  tmp_pct_seasmin = os.path.join(path_temp, "tmp_pct_seasmin.nc")
  tmp_pct_seasmax = os.path.join(path_temp, "tmp_pct_seasmax.nc")
  
  
  # means    
  
  file_out = os.path.join(path_out, lbl + "_mean_annual.nc")
  if not os.path.exists(file_out):
    cdo.yearmean(input=file_in, output=file_out)
  
  file_out = os.path.join(path_out, lbl + "_mean_seasonal.nc")
  if not os.path.exists(file_out):
    cdo.seasmean(input=file_in, output=file_out)
  
  # pctl extra
  cdo.yearmin(input=file_in, output=tmp_pct_yearmin)
  cdo.yearmax(input=file_in, output=tmp_pct_yearmax)
  cdo.seasmin(input=file_in, output=tmp_pct_seasmin)
  cdo.seasmax(input=file_in, output=tmp_pct_seasmax)
  
  for i,p in enumerate(pctl):
    
    file_out = os.path.join(path_out, lbl + "_" + str(p) + "pct_annual.nc")
    if not os.path.exists(file_out):
      cdo.yearpctl(p, input=file_in+" "+tmp_pct_yearmin+" "+tmp_pct_yearmax, output=file_out)
    
    file_out = os.path.join(path_out, lbl + "_" + str(p) + "pct_seasonal.nc")
    if not os.path.exists(file_out):
      cdo.seaspctl(p, input=file_in+" "+tmp_pct_seasmin+" "+tmp_pct_seasmax, output=file_out)
  

  
    
