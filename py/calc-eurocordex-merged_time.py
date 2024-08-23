# saved merged files
import os
import glob
import logging
# import shutil
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex2-full/merged/"
path_out = "/home/climatedata/eurocordex2-full/merged/merged_in_time/"
path_temp = "/home/climatedata/eurocordex2-full/tmp/"

variables = ["rlus","rsds","rsus"]

for var in variables:

    all_files_rcm = os.listdir(os.path.join(path_in, var))
    all_files_rcm.sort()

    all_files_rcm_hist = [x for x in all_files_rcm if "historical" in x]
    all_files_rcm_loop = [x for x in all_files_rcm if not "historical" in x]

    os.makedirs(os.path.join(path_out, var), exist_ok=True)

    for j,file_loop in enumerate(all_files_rcm_loop):

        # hist/rcp
        file_rcp = os.path.join(path_in, var, file_loop)
        (_, _, gcm, _, ens, rcm, ds, _, _) = file_loop[:-3].split("_")
        file_hist = os.path.join(path_in, var,
                                 [x for x in all_files_rcm_hist if
                                  gcm in x and ens in x and rcm in x and ds in x][0])
        # update start date in filename
        file_rcm = file_loop[:-20] + file_hist[-20:-12] + file_loop[-12:]
        file_out = os.path.join(path_out, var, file_rcm)

        # skip rest of loop if first file exists
        if os.path.exists(file_out):
            continue

        cdo.mergetime(input=[file_hist, file_rcp],
                      output=file_out)

