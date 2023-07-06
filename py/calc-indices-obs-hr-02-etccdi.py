# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_out = "/home/climatedata/obs/data_in_time/etccdi/"
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
  # tas_SWITZERLAND = "/home/climatedata/obs/SWITZERLAND/setgrid_noDuplicates/TabsD_ch02h.lonlat_1961-2021_NoDuplicates.nc",
  tasmax_SWITZERLAND = "/home/climatedata/obs/SWITZERLAND/setgrid_noDuplicates/TmaxD_ch02h.lonlat_1971-2021_NoDuplicates.nc",
  tasmin_SWITZERLAND = "/home/climatedata/obs/SWITZERLAND/setgrid_noDuplicates/TminD_ch02h.lonlat_1971-2021_NoDuplicates.nc"
)

for lbl, file_in in all_files.items():

  # tasmax indices
  if lbl.startswith("tasmax"):
    file_out = os.path.join(path_out, lbl + "_SU_annual.nc")
    if not os.path.exists(file_out):
      cdo.etccdi_su(input="-addc,273.15 " + file_in, output=file_out)
    
    file_out = os.path.join(path_out, lbl + "_ID_annual.nc")
    if not os.path.exists(file_out):
      file_in_chain = "-ltc,0 " + file_in
      cdo.yearsum(input=file_in_chain, output=file_out)
  
  # tasmin indices
  if lbl.startswith("tasmin"):
    file_out = os.path.join(path_out, lbl + "_FD_annual.nc")
    if not os.path.exists(file_out):
      cdo.etccdi_fd(input="-addc,273.15 " + file_in, output=file_out)
  
    file_out = os.path.join(path_out, lbl + "_TR_annual.nc")
    if not os.path.exists(file_out):
      cdo.etccdi_tr(input="-addc,273.15 " + file_in, output=file_out)
  
  # pr indices
  if lbl.startswith("pr"):
    file_out = os.path.join(path_out, lbl + "_CDD_annual.nc")
    if not os.path.exists(file_out):
      cdo.etccdi_cdd(input=file_in, output=file_out)

    file_out = os.path.join(path_out, lbl + "_SDII_annual.nc")
    file_in_chain = "-ifthen -gtc,1 " + file_in + " " + file_in
    if not os.path.exists(file_out):
      cdo.yearmean(input=file_in_chain, output=file_out)

    file_out = os.path.join(path_out, lbl + "_RR1_annual.nc")
    file_in_chain = "-gtc,1 " + file_in
    if not os.path.exists(file_out):
      cdo.yearsum(input=file_in_chain, output=file_out)
    
    file_out = os.path.join(path_out, lbl + "_R95pTOT_annual.nc")
    file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
    file_tmp_wd_p95 = os.path.join(path_temp, "wetdays_p95.nc")
    file_tmp_wd_p95_gt = os.path.join(path_temp, "wetdays_p95_gt.nc")
    if not os.path.exists(file_out):
      # cdo.ifthen(input= "-gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in, output=file_tmp_wd)
      cdo.ifthen(input= "-gtc,1 " + file_in + " " + file_in, output=file_tmp_wd)
      cdo.timpctl(95, input=file_tmp_wd+" -timmin "+file_tmp_wd+" -timmax "+file_tmp_wd, output=file_tmp_wd_p95)
      cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p95+ " "+file_tmp_wd,output=file_tmp_wd_p95_gt)
      cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p95_gt+" -yearsum "+file_in,output=file_out)

