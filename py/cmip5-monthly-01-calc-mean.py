# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/cmip5/large-ensemble-monthly/merged/"
path_out = "/home/climatedata/cmip5/large-ensemble-monthly/indices/"
path_temp = "/home/climatedata/cmip5/large-ensemble-monthly/tmp/"

variables = ["tas", "pr"]

os.makedirs(path_temp, exist_ok=True)
tmp_merge_hist = os.path.join(path_temp, "tmp_merge_hist.nc")


for var in variables:

    all_files = os.listdir(os.path.join(path_in, var))
    all_files.sort()
    
    all_files_hist = [x for x in all_files if "historical" in x]
    all_files_loop = [x for x in all_files if not "historical" in x]
        
    for j,file_loop in enumerate(all_files_loop):
          
        # merge hist temporarily
        file_rcp = os.path.join(path_in, var, file_loop)
        (_, _, gcm, _, ens, _) = file_loop[:-3].split("_")
        file_hist = os.path.join(path_in, var,
                                 [x for x in all_files_hist if gcm+"_" in x and ens in x][0])
        # update start date in filename
        file_gcm = file_loop[:-16] + file_hist[-16:-9] + file_loop[-9:]
        
        file_out_annual = os.path.join(path_out, var + "_mean_annual", file_gcm)
        file_out_seasonal = os.path.join(path_out, var + "_mean_seasonal", file_gcm)
        
        os.makedirs(os.path.join(path_out, var + "_mean_annual"), exist_ok=True)
        os.makedirs(os.path.join(path_out, var + "_mean_seasonal"), exist_ok=True)
        
        if not os.path.exists(file_out_annual) or not os.path.exists(file_out_seasonal):
            # cdo.mergetime(input=file_hist + " " + file_rcp, output=tmp_merge_hist)
            cdo.mergetime(input=" -seldate,1800-01-01,2005-12-31 " + file_hist + " " + file_rcp, 
                          output=tmp_merge_hist)
            file_in = tmp_merge_hist      
            
            if not os.path.exists(file_out_annual):
                cdo.yearmean(input=file_in, output=file_out_annual)
            
            if not os.path.exists(file_out_seasonal):
                cdo.seasmean(input=file_in, output=file_out_seasonal)
      
 

    
