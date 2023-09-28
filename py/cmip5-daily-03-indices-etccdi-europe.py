# calculate annual and seasonal indices
import os
import glob
# import shutil
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/cmip5/eurocordex-ensemble-daily/merged-europe/"
path_out = "/home/climatedata/cmip5/eurocordex-ensemble-daily/indices-etccdi-europe/"
path_temp = "/home/climatedata/cmip5/eurocordex-ensemble-daily/tmp/"

# path_in = "/home/climatedata/cmip5/cmcc-cm-daily/merged-europe/"
# path_out = "/home/climatedata/cmip5/cmcc-cm-daily/indices-etccdi-europe/"
# path_temp = "/home/climatedata/cmip5/cmcc-cm-daily/tmp/"

os.makedirs(path_temp, exist_ok=True)
tmp_merge_hist = os.path.join(path_temp, "tmp_merge_hist.nc")


# helper function
def calc_index(var_in, var_out, cdo_fun):
    path_in_index = os.path.join(path_in, var_in)
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    
    all_files_gcm = os.listdir(path_in_index)
    all_files_gcm.sort()
    all_files_gcm_hist = [x for x in all_files_gcm if "historical" in x]
    all_files_gcm_loop = [x for x in all_files_gcm if not "historical" in x]
    
    for j,file_loop in enumerate(all_files_gcm_loop):
        # merge hist temporarily
        file_rcp = os.path.join(path_in, var_in, file_loop)
        (_, _, gcm, _, ens, _) = file_loop[:-3].split("_")
        file_hist = os.path.join(path_in, var_in,
                                 [x for x in all_files_gcm_hist if gcm+"_" in x and ens in x][0])
        # update start date in filename
        file_gcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
        
        file_in = tmp_merge_hist   
        file_out = os.path.join(path_out_index, file_gcm)
        if not os.path.exists(file_out):
            cdo.mergetime(input=" -seldate,1800-01-01,2005-12-31 " + file_hist + " " + file_rcp, 
                          output=tmp_merge_hist)
            if var_in.startswith("pr"):
                file_in = "-mulc,86400 " + file_in
            cdo_fun(input=file_in, output=file_out)




calc_index("tasmin", "FD_annual", cdo.etccdi_fd)
calc_index("tasmin", "TR_annual", cdo.etccdi_tr)
calc_index("tasmax", "SU_annual", cdo.etccdi_su)
calc_index("pr", "CDD_annual", cdo.etccdi_cdd)

# ID also destroys time information
# ---------------------------------------------------- #

var_in = "tasmax"
path_in_index = os.path.join(path_in, var_in)
all_files_gcm = os.listdir(path_in_index)
all_files_gcm.sort()
all_files_gcm_hist = [x for x in all_files_gcm if "historical" in x]
all_files_gcm_loop = [x for x in all_files_gcm if not "historical" in x]

for j,file_loop in enumerate(all_files_gcm_loop):
    # merge hist temporarily
    file_rcp = os.path.join(path_in, var_in, file_loop)
    (_, _, gcm, _, ens, _) = file_loop[:-3].split("_")
    file_hist = os.path.join(path_in, var_in,
                             [x for x in all_files_gcm_hist if gcm+"_" in x and ens in x][0])
    # update start date in filename
    file_gcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
    file_in = tmp_merge_hist
    
    # ID
    var_out = "ID_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_gcm)
    
    if not os.path.exists(file_out):
        cdo.mergetime(input=" -seldate,1800-01-01,2005-12-31 " + file_hist + " " + file_rcp, 
                      output=tmp_merge_hist)

        file_in_chain = "-ltc,273.15 " + file_in
        if not os.path.exists(file_out):
            cdo.yearsum(input=file_in_chain, output=file_out)

   


# SDII and RR1 destroy time information, R95pTOT unclear
# ---------------------------------------------------- #

var_in = "pr"
path_in_index = os.path.join(path_in, var_in)
all_files_gcm = os.listdir(path_in_index)
all_files_gcm.sort()
all_files_gcm_hist = [x for x in all_files_gcm if "historical" in x]
all_files_gcm_loop = [x for x in all_files_gcm if not "historical" in x]

for j,file_loop in enumerate(all_files_gcm_loop):
    # merge hist temporarily
    file_rcp = os.path.join(path_in, var_in, file_loop)
    (_, _, gcm, _, ens, _) = file_loop[:-3].split("_")
    file_hist = os.path.join(path_in, var_in,
                             [x for x in all_files_gcm_hist if gcm+"_" in x and ens in x][0])
    # update start date in filename
    file_gcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
    file_in = tmp_merge_hist

    # skip rest of loop if last file exists
    if os.path.exists(os.path.join(path_out, "R95pTOT_annual", file_gcm)):
        continue    

    cdo.mergetime(input=" -seldate,1800-01-01,2005-12-31 " + file_hist + " " + file_rcp, 
                  output=tmp_merge_hist)

    # SDII
    var_out = "SDII_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_gcm)
    file_in_chain = "-ifthen -gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.yearmean(input=file_in_chain, output=file_out)

    # RR1
    var_out = "RR1_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_gcm)
    file_in_chain = "-gtc,1 -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)

    # R95pTOT
    var_out = "R95pTOT_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_gcm)
    file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
    file_tmp_wd_p95 = os.path.join(path_temp, "wetdays_p95.nc")
    file_tmp_wd_p95_gt = os.path.join(path_temp, "wetdays_p95_gt.nc")
  
    if not os.path.exists(file_out):
        cdo.ifthen(input= "-gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in, output=file_tmp_wd)
        cdo.timpctl(95, input=file_tmp_wd+" -timmin "+file_tmp_wd+" -timmax "+file_tmp_wd, output=file_tmp_wd_p95)
        cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p95+ " "+file_tmp_wd,output=file_tmp_wd_p95_gt)
        cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p95_gt+" -yearsum -mulc,86400 "+file_in,output=file_out)



