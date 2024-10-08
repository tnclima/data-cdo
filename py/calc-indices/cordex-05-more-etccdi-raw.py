# calculate annual and seasonal indices
import os
# import glob
# import shutil
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex2-full/merged/"
path_out = "/home/climatedata/eurocordex2-full/indices_etccdi/"
path_temp = "/home/climatedata/tmp/"
os.makedirs(path_temp, exist_ok=True)
tmp_merge_hist = os.path.join(path_temp, "tmp_merge_hist.nc")


# helper function
def calc_index(var_in, var_out, cdo_fun):
    path_in_index = os.path.join(path_in, var_in)
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    
    all_files_rcm = os.listdir(path_in_index)
    all_files_rcm.sort()
    all_files_rcm_hist = [x for x in all_files_rcm if "historical" in x]
    all_files_rcm_loop = [x for x in all_files_rcm if not "historical" in x]
    
    for j,file_loop in enumerate(all_files_rcm_loop):
        # merge hist temporarily
        file_rcp = os.path.join(path_in_index, file_loop)
        (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop[:-3].split("_")
        file_hist = os.path.join(path_in_index, 
                                 [x for x in all_files_rcm_hist if 
                                  gcm in x and ens in x and rcm in x and ds in x][0])
        # update start date in filename
        file_rcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
        file_in = tmp_merge_hist
        file_out = os.path.join(path_out_index, file_rcm)
        if not os.path.exists(file_out):
            cdo.mergetime(input=file_hist + " " + file_rcp, output=tmp_merge_hist)
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
all_files_rcm = os.listdir(path_in_index)
all_files_rcm.sort()
all_files_rcm_hist = [x for x in all_files_rcm if "historical" in x]
all_files_rcm_loop = [x for x in all_files_rcm if not "historical" in x]

for j,file_loop in enumerate(all_files_rcm_loop):
    # merge hist temporarily
    file_rcp = os.path.join(path_in_index, file_loop)
    (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop[:-3].split("_")
    file_hist = os.path.join(path_in_index, 
                             [x for x in all_files_rcm_hist if 
                              gcm in x and ens in x and rcm in x and ds in x][0])
    # update start date in filename
    file_rcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
    file_in = tmp_merge_hist

    
    # skip rest of loop if last file exists
    if os.path.exists(os.path.join(path_out, "SU30_annual", file_rcm)):
      continue
    
    cdo.mergetime(input=file_hist + " " + file_rcp, output=tmp_merge_hist)

    # ID
    var_out = "ID_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_in_chain = "-ltc,273.15 " + file_in
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
    
    
    # SU30
    var_out = "SU30_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_in_chain = "-ltc,273.15 " + file_in
    if not os.path.exists(file_out):
        cdo.etccdi_su(30, input=file_in_chain, output=file_out)



# tas indices
var_in = "tas"
path_in_index = os.path.join(path_in, var_in)
all_files_rcm = os.listdir(path_in_index)
all_files_rcm.sort()
all_files_rcm_hist = [x for x in all_files_rcm if "historical" in x]
all_files_rcm_loop = [x for x in all_files_rcm if not "historical" in x]


for j,file_loop in enumerate(all_files_rcm_loop):
    # merge hist temporarily
    file_rcp = os.path.join(path_in_index, file_loop)
    (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop[:-3].split("_")
    file_hist = os.path.join(path_in_index, 
                             [x for x in all_files_rcm_hist if 
                              gcm in x and ens in x and rcm in x and ds in x][0])
    # update start date in filename
    file_rcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
    file_in = tmp_merge_hist
    
    # skip rest of loop if last file exists
    if os.path.exists(os.path.join(path_out, "coolDD_annual", file_rcm)):
      continue
    
    cdo.mergetime(input=file_hist + " " + file_rcp, output=tmp_merge_hist)


    # heatDD
    var_out = "heatDD_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_tmp = os.path.join(path_temp, "threshold.nc")
    file_in_chain = "-setmisstoc,0 -expr,'heatDD=-tas' -subc,291.15 " + file_tmp
    if not os.path.exists(file_out):
        cdo.ifthen(input="-ltc,291.15 " + file_in + " " + file_in, output=file_tmp)
        cdo.yearsum(input=file_in_chain, output=file_out)
    
    
    # coolDD
    var_out = "coolDD_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_tmp = os.path.join(path_temp, "threshold.nc")
    if not os.path.exists(file_out):
        cdo.ifthen(input="-gtc,295.15 " + file_in + " " + file_in, output=file_tmp)
        cdo.yearsum(input="-setmisstoc,0 -subc,295.15 " + file_tmp, output=file_out)


# SDII and RR1 destroy time information, R95pTOT unclear
# ---------------------------------------------------- #

var_in = "pr"
path_in_index = os.path.join(path_in, var_in)
all_files_rcm = os.listdir(path_in_index)
all_files_rcm.sort()
all_files_rcm_hist = [x for x in all_files_rcm if "historical" in x]
all_files_rcm_loop = [x for x in all_files_rcm if not "historical" in x]

for j,file_loop in enumerate(all_files_rcm_loop):
    # merge hist temporarily
    file_rcp = os.path.join(path_in_index, file_loop)
    (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop[:-3].split("_")
    file_hist = os.path.join(path_in_index, 
                             [x for x in all_files_rcm_hist if 
                              gcm in x and ens in x and rcm in x and ds in x][0])
    # update start date in filename
    file_rcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
    file_in = tmp_merge_hist

    # skip rest of loop if last file exists
    # if os.path.exists(os.path.join(path_out, "R20mm_annual", file_rcm)):
    #   continue    

    cdo.mergetime(input=file_hist + " " + file_rcp, output=tmp_merge_hist)

    # SDII
    var_out = "SDII_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    file_in_chain = "-ifthen -gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.yearmean(input=file_in_chain, output=file_out)

    # RR1
    var_out = "RR1_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    file_in_chain = "-gtc,1 -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)

    # R95pTOT
    var_out1 = "R95pTOT_annual"
    path_out_index1 = os.path.join(path_out, var_out1)
    os.makedirs(path_out_index1, exist_ok=True)
    file_out1 = os.path.join(path_out_index1, file_rcm)
    var_out2 = "R95p_annual"
    path_out_index2 = os.path.join(path_out, var_out2)
    os.makedirs(path_out_index2, exist_ok=True)
    file_out2 = os.path.join(path_out_index2, file_rcm)

    file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
    file_tmp_wd81 = os.path.join(path_temp, "wetdays_81.nc")
    file_tmp_wd_p95 = os.path.join(path_temp, "wetdays_p95.nc")
    file_tmp_wd_p95_gt = os.path.join(path_temp, "wetdays_p95_gt.nc")
  
    if not os.path.exists(file_out2):
        cdo.ifthen(input= "-gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in, output=file_tmp_wd)
        cdo.selyear("1981/2010", input=file_tmp_wd, output=file_tmp_wd81)
        cdo.timpctl(95, input=file_tmp_wd81+" -timmin "+file_tmp_wd81+" -timmax "+file_tmp_wd81, output=file_tmp_wd_p95)
        cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p95+ " "+file_tmp_wd,output=file_tmp_wd_p95_gt)
        cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p95_gt+" -yearsum -mulc,86400 "+file_in,output=file_out1)
        cdo.yearsum(input=" -gt -mulc,86400 "+file_in+" "+file_tmp_wd_p95,output=file_out2)
   
    # R99pTOT
    var_out1 = "R99pTOT_annual"
    path_out_index1 = os.path.join(path_out, var_out1)
    os.makedirs(path_out_index1, exist_ok=True)
    file_out1 = os.path.join(path_out_index1, file_rcm)
    var_out2 = "R99p_annual"
    path_out_index2 = os.path.join(path_out, var_out2)
    os.makedirs(path_out_index2, exist_ok=True)
    file_out2 = os.path.join(path_out_index2, file_rcm)

    file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
    file_tmp_wd81 = os.path.join(path_temp, "wetdays_81.nc")
    file_tmp_wd_p99 = os.path.join(path_temp, "wetdays_p99.nc")
    file_tmp_wd_p99_gt = os.path.join(path_temp, "wetdays_p99_gt.nc")
  
    if not os.path.exists(file_out2):
        cdo.ifthen(input= "-gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in, output=file_tmp_wd)
        cdo.selyear("1981/2010", input=file_tmp_wd, output=file_tmp_wd81)
        cdo.timpctl(99, input=file_tmp_wd81+" -timmin "+file_tmp_wd81+" -timmax "+file_tmp_wd81, output=file_tmp_wd_p99)
        cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p99+ " "+file_tmp_wd,output=file_tmp_wd_p99_gt)
        cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p99_gt+" -yearsum -mulc,86400 "+file_in,output=file_out1)
        cdo.yearsum(input=" -gt -mulc,86400 "+file_in+" "+file_tmp_wd_p99,output=file_out2)
    
    
    
    # Rx1day
    var_out = "Rx1day_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_in_chain = " -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.etccdi_rx1day(input=file_in_chain, output=file_out)
     
    
    # Rx5day
    var_out = "Rx5day_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_in_chain = " -runsum,5 -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.etccdi_rx5day(input=file_in_chain, output=file_out)
    
    # R10mm
    var_out = "R10mm_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_in_chain = " -gec,10 -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
    
    # R20mm
    var_out = "R20mm_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm)
    
    file_in_chain = " -gec,20 -mulc,86400 " + file_in
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
    

    

   
