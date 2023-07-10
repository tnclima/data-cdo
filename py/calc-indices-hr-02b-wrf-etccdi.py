# calculate annual and seasonal indices
import os
import glob
# import shutil
from cdo import Cdo

cdo = Cdo()

# all_rcps = ["rcp45", "rcp85"]
# all_rcps = ["rcp45"]
all_rcps = ["hist"]

# path_in = "/home/climatedata/highlander/Daily/"
path_out = "/home/climatedata/temp-analysis/wrf-anna/indices-etccdi/"
path_temp = "/home/climatedata/temp-analysis/tmp/"
os.makedirs(path_temp, exist_ok=True)

file_in = "/home/climatedata/temp-analysis/wrf-anna/daily/historical_pr_1979-2008.nc"

# helper function
def calc_index(var_in, var_out, cdo_fun, celsius=False):
  for rcp in all_rcps:
    # file_in = os.path.join("/home/climatedata/temp-analysis/highlander-merged/",
                           # rcp + "_1989-2070_" + var_in + ".nc")
    file_in = "/home/climatedata/temp-analysis/wrf-anna/daily/historical_pr_1979-2008.nc"
    if celsius:
      file_in = "-addc,273.15 " + file_in
    file_out = os.path.join(path_out, rcp + "_" + var_out + ".nc")
    if not os.path.exists(file_out):
      cdo_fun(input=file_in, output=file_out)




# calc_index("tasmin", "FD_annual", cdo.etccdi_fd, celsius=True)
# calc_index("tasmin", "TR_annual", cdo.etccdi_tr, celsius=True)
# calc_index("tasmax", "SU_annual", cdo.etccdi_su, celsius=True)
calc_index("pr", "CDD_annual", cdo.etccdi_cdd)

# ID also destroys time information
# ---------------------------------------------------- #
# 
# var_in = "tasmax"
# for rcp in all_rcps:
#   file_in = os.path.join("/home/climatedata/temp-analysis/highlander-merged/",
#                          rcp + "_1989-2070_" + var_in + ".nc")
# 
#   # ID
#   var_out = "ID_annual"
#   file_out = os.path.join(path_out, rcp + "_" + var_out + ".nc")
# 
#   if not os.path.exists(file_out):
#     file_in_chain = "-ltc,0 " + file_in
#     cdo.yearsum(input=file_in_chain, output=file_out)


# SDII and RR1 destroy time information, R95pTOT unclear
# ---------------------------------------------------- #

var_in = "pr"

for rcp in all_rcps:
  
  # file_in = os.path.join("/home/climatedata/temp-analysis/highlander-merged/",
                         # rcp + "_1989-2070_" + var_in + ".nc")

  # SDII
  var_out = "SDII_annual"
  file_out = os.path.join(path_out, rcp + "_" + var_out + ".nc")
  # file_in_chain = "-ifthen -gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in
  file_in_chain = "-ifthen -gtc,1 " + file_in + " " + file_in
  if not os.path.exists(file_out):
    cdo.yearmean(input=file_in_chain, output=file_out)

  # RR1
  var_out = "RR1_annual"
  file_out = os.path.join(path_out, rcp + "_" + var_out + ".nc")
  file_in_chain = "-gtc,1 " + file_in
  if not os.path.exists(file_out):
    cdo.yearsum(input=file_in_chain, output=file_out)

  # R95pTOT
  var_out = "R95pTOT_annual"
  file_out = os.path.join(path_out, rcp + "_" + var_out + ".nc")
  file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
  file_tmp_wd_p95 = os.path.join(path_temp, "wetdays_p95.nc")
  file_tmp_wd_p95_gt = os.path.join(path_temp, "wetdays_p95_gt.nc")
  if not os.path.exists(file_out):
    # cdo.ifthen(input= "-gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in, output=file_tmp_wd)
    cdo.ifthen(input= "-gtc,1 " + file_in + " " + file_in, output=file_tmp_wd)
    cdo.timpctl(95, input=file_tmp_wd+" -timmin "+file_tmp_wd+" -timmax "+file_tmp_wd, output=file_tmp_wd_p95)
    cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p95+ " "+file_tmp_wd,output=file_tmp_wd_p95_gt)
    cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p95_gt+" -yearsum "+file_in,output=file_out)



