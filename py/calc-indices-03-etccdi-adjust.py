# calculate annual and seasonal indices
import os
import glob
import shutil
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex/merged/"
path_out = "/home/climatedata/eurocordex/indices_etccdi/"
path_temp = "/home/climatedata/eurocordex/tmp/"
os.makedirs(path_temp, exist_ok=True)
# shutil.rmtree(path_temp)


# helper function
def calc_index(var_in, var_out, cdo_fun):
  path_in_index = os.path.join(path_in, var_in)
  path_out_index = os.path.join(path_out, var_out)
  os.makedirs(path_out_index, exist_ok=True)
  
  all_files_rcm = os.listdir(path_in_index)
  all_files_rcm.sort()
  for j,file_rcm in enumerate(all_files_rcm):
    file_in = os.path.join(path_in_index, file_rcm)
    if var_in.startswith("pr"):
      file_in = "-mulc,86400 " + file_in
    file_out = os.path.join(path_out_index, file_rcm)
    if not os.path.exists(file_out):
      cdo_fun(input=file_in, output=file_out)




calc_index("tasminAdjust", "FD_annual", cdo.etccdi_fd)
calc_index("tasmaxAdjust", "ID_annual", cdo.etccdi_id)
calc_index("tasminAdjust", "TR_annual", cdo.etccdi_tr)
calc_index("tasmaxAdjust", "SU_annual", cdo.etccdi_su)
calc_index("prAdjust", "CDD_annual", cdo.etccdi_cdd)


# SDII and RR1 destroy time information, R95pTOT unclear
# ---------------------------------------------------- #

# SDII
var_in = "prAdjust"
var_out = "SDII_annual"

path_in_index = os.path.join(path_in, var_in)
path_out_index = os.path.join(path_out, var_out)
os.makedirs(path_out_index, exist_ok=True)

all_files_rcm = os.listdir(path_in_index)
all_files_rcm.sort()
for j,file_rcm in enumerate(all_files_rcm):
  file_in = os.path.join(path_in_index, file_rcm)
  file_in_chain = "-ifthen -gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in
  file_out = os.path.join(path_out_index, file_rcm)
  if not os.path.exists(file_out):
    cdo.yearmean(input=file_in_chain, output=file_out)


# RR1

var_in = "prAdjust"
var_out = "RR1_annual"

path_in_index = os.path.join(path_in, var_in)
path_out_index = os.path.join(path_out, var_out)
os.makedirs(path_out_index, exist_ok=True)

all_files_rcm = os.listdir(path_in_index)
all_files_rcm.sort()
for j,file_rcm in enumerate(all_files_rcm):
  file_in = os.path.join(path_in_index, file_rcm)
  file_in_chain = "-gtc,1 -mulc,86400 " + file_in
  file_out = os.path.join(path_out_index, file_rcm)
  if not os.path.exists(file_out):
    cdo.yearsum(input=file_in_chain, output=file_out)




# R95pTOT
var_in = "prAdjust"
var_out = "R95pTOT_annual"

path_in_index = os.path.join(path_in, var_in)
path_out_index = os.path.join(path_out, var_out)
os.makedirs(path_out_index, exist_ok=True)

all_files_rcm = os.listdir(path_in_index)
all_files_rcm.sort()
# file_rcm = all_files_rcm[0]
for j,file_rcm in enumerate(all_files_rcm):
  file_out = os.path.join(path_out_index, file_rcm)
  file_in = os.path.join(path_in_index, file_rcm)
  file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
  file_tmp_wd_p95 = os.path.join(path_temp, "wetdays_p95.nc")
  file_tmp_wd_p95_gt = os.path.join(path_temp, "wetdays_p95_gt.nc")
  
  if not os.path.exists(file_out):
    cdo.ifthen(input= "-gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in, output=file_tmp_wd)
    cdo.timpctl(95, input=file_tmp_wd+" -timmin "+file_tmp_wd+" -timmax "+file_tmp_wd, output=file_tmp_wd_p95)
    cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p95+ " "+file_tmp_wd,output=file_tmp_wd_p95_gt)
    cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p95_gt+" -yearsum -mulc,86400 "+file_in,output=file_out)




