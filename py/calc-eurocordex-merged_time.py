# saved merged files
import os
import glob
import logging
# import shutil
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex2-full/merged/tasmax/"
path_out = "/home/climatedata/eurocordex2-full/merged/tasmax/merged_in_time/"
path_temp = "/home/climatedata/eurocordex2-full/tmp/"
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
