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
tmp_merge_hist_tas = os.path.join(path_temp, "tmp_merge_hist_tas.nc")
tmp_merge_hist_pr = os.path.join(path_temp, "tmp_merge_hist_pr.nc")


path_in_index_tas = os.path.join(path_in, "tas")
all_files_rcm_tas = os.listdir(path_in_index_tas)
all_files_rcm_tas.sort()
all_files_rcm_tas_hist = [x for x in all_files_rcm_tas if "historical" in x]
all_files_rcm_tas_loop = [x for x in all_files_rcm_tas if not "historical" in x]

path_in_index_pr = os.path.join(path_in, "pr")
all_files_rcm_pr = os.listdir(path_in_index_pr)
all_files_rcm_pr.sort()
all_files_rcm_pr_hist = [x for x in all_files_rcm_pr if "historical" in x]
all_files_rcm_pr_loop = [x for x in all_files_rcm_pr if not "historical" in x]


# HN 

for j,file_loop_tas in enumerate(all_files_rcm_tas_loop):
    # merge hist temporarily
    file_rcp_tas = os.path.join(path_in_index_tas, file_loop_tas)
    (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop_tas[:-3].split("_")
    file_hist_tas = os.path.join(path_in_index_tas, 
                             [x for x in all_files_rcm_tas_hist if 
                              gcm in x and ens in x and rcm in x and ds in x][0])
    # update start date in filename
    file_rcm_tas = file_loop_tas[:-20] + file_hist_tas[-20:-12] + file_loop_tas[-12:]
    file_in_tas = tmp_merge_hist_tas
    
    
    file_hist_pr = file_hist_tas.replace("tas", "pr")
    file_rcp_pr = file_rcp_tas.replace("tas", "pr")
    file_rcm_pr = file_rcm_tas.replace("tas", "pr")
    file_in_pr = tmp_merge_hist_pr
    # # skip rest of loop if last file exists
    if not os.path.exists(file_hist_pr):
      continue


    # # skip rest of loop if last file exists
    if os.path.exists(os.path.join(path_out, "HN_annual", file_rcm_tas)):
      continue
    
    cdo.mergetime(input=file_hist_tas + " " + file_rcp_tas, output=tmp_merge_hist_tas)
    cdo.mergetime(input=file_hist_pr + " " + file_rcp_pr, output=tmp_merge_hist_pr)


    # HNd
    var_out = "HNd_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm_pr)
    
    file_in_chain = " -mul -gec,1 -mulc,86400 " + file_in_pr + " -ltc,275.15 " + file_in_tas
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
    
    # HN
    var_out = "HN_annual"
    path_out_index = os.path.join(path_out, var_out)
    os.makedirs(path_out_index, exist_ok=True)
    file_out = os.path.join(path_out_index, file_rcm_pr)
    
    file_in_chain = (" -setmisstoc,0 -ifthen -ltc,275.15 " + file_in_tas + " -mulc,86400 " + file_in_pr)
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
    

