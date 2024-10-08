#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# calc indices (etccdi)


import os
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/downscaling-1km_giornaliero/"
path_out = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/downscaling-1km_annuale_indici/"

all_rcps = os.listdir(path_in)

path_temp = "/home/climatedata/tmp/"
os.makedirs(path_temp, exist_ok=True)


for rcp in all_rcps:
    
    path_in_rcp = os.path.join(path_in, rcp)
    all_files = os.listdir(path_in_rcp)
    
    
    
    all_models = [x.split("_")[1] for x in all_files]
    all_models = list(set(all_models))
    all_models.sort()
    
    for model in all_models:
        
        files_model = [x for x in all_files if model in x]
        
        file_tasmax = [x for x in files_model if "tasmax" in x][0]
        file_tasmin = [x for x in files_model if "tasmin" in x][0]
        file_tas = [x for x in files_model if "tas_" in x][0]
        file_pr = [x for x in files_model if "pr" in x][0]
        
        file_in_tasmax = os.path.join(path_in_rcp, file_tasmax)
        file_in_tasmin = os.path.join(path_in_rcp, file_tasmin)
        file_in_tas = os.path.join(path_in_rcp, file_tas)
        file_in_pr = os.path.join(path_in_rcp, file_pr)
        
        i_path_out = os.path.join(
            path_out, rcp, file_tasmax.replace(".nc", "").replace("tasmax_", "")
            )
        os.makedirs(i_path_out, exist_ok=True)
        
        # tasmax indices
        
        file_out = os.path.join(i_path_out, "SU.nc")
        if not os.path.exists(file_out):
            cdo.etccdi_su(input="-addc,273.15 " + file_in_tasmax, output=file_out)
        
        file_out = os.path.join(i_path_out, "SU30.nc")
        if not os.path.exists(file_out):
            cdo.etccdi_su(30, input="-addc,273.15 " + file_in_tasmax, output=file_out)
        
        file_out = os.path.join(i_path_out, "ID.nc")
        if not os.path.exists(file_out):
            file_in_chain = "-ltc,0 " + file_in_tasmax
            cdo.yearsum(input=file_in_chain, output=file_out)
          
          
        # tasmin indices
        
        file_out = os.path.join(i_path_out, "FD.nc")
        if not os.path.exists(file_out):
            cdo.etccdi_fd(input="-addc,273.15 " + file_in_tasmin, output=file_out)
      
        file_out = os.path.join(i_path_out, "TR.nc")
        if not os.path.exists(file_out):
            cdo.etccdi_tr(input="-addc,273.15 " + file_in_tasmin, output=file_out)
        
        # tas indices
        
        file_out = os.path.join(i_path_out, "heatDD.nc")
        file_tmp = os.path.join(path_temp, "threshold.nc")
        file_tmp2 = os.path.join(path_temp, "beforemask.nc")
        file_in_chain = "-setmisstoc,0 -expr,'heatDD=-tas' -subc,18 " + file_tmp
        if not os.path.exists(file_out):
            cdo.ifthen(input="-ltc,18 " + file_in_tas + " " + file_in_tas, output=file_tmp)
            cdo.yearsum(input=file_in_chain, output=file_tmp2)
            cdo.div(input=file_tmp2+" -gtc,-1 -timmin "+file_in_pr,output=file_out) # for masking
        
        file_out = os.path.join(i_path_out, "coolDD.nc")
        file_tmp = os.path.join(path_temp, "threshold.nc")
        file_tmp2 = os.path.join(path_temp, "beforemask.nc")
        if not os.path.exists(file_out):
            cdo.ifthen(input="-gtc,22 " + file_in_tas + " " + file_in_tas, output=file_tmp)
            cdo.yearsum(input="-setmisstoc,0 -subc,22 " + file_tmp, output=file_tmp2)
            cdo.div(input=file_tmp2+" -gtc,-1 -timmin "+file_in_pr,output=file_out) # for masking
        
        # pr indices
        
        file_out = os.path.join(i_path_out, "CDD.nc")
        if not os.path.exists(file_out):
            cdo.etccdi_cdd(input=file_in_pr, output=file_out)
    
        file_out = os.path.join(i_path_out, "SDII.nc")
        file_in_chain = "-ifthen -gec,1 " + file_in_pr + " " + file_in_pr
        if not os.path.exists(file_out):
            cdo.yearmean(input=file_in_chain, output=file_out)
    
        file_out = os.path.join(i_path_out, "RR1.nc")
        file_in_chain = "-gec,1 " + file_in_pr
        if not os.path.exists(file_out):
            cdo.yearsum(input=file_in_chain, output=file_out)
        
        
        file_out1 = os.path.join(i_path_out, "R95pTOT.nc")
        file_out2 = os.path.join(i_path_out, "R95p.nc")
        file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
        file_tmp_wd81 = os.path.join(path_temp, "wetdays_81.nc")
        file_tmp_wd_p95 = os.path.join(path_temp, "wetdays_p95.nc")
        file_tmp_wd_p95_gt = os.path.join(path_temp, "wetdays_p95_gt.nc")
        if not os.path.exists(file_out2):
            cdo.ifthen(input= "-gec,1 " + file_in_pr + " " + file_in_pr, output=file_tmp_wd)
            cdo.selyear("1981/2010",input=file_tmp_wd,output=file_tmp_wd81)
            cdo.timpctl(95, input=file_tmp_wd81+" -timmin "+file_tmp_wd81+" -timmax "+file_tmp_wd81, output=file_tmp_wd_p95)
            cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p95+ " "+file_tmp_wd,output=file_tmp_wd_p95_gt)
            cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p95_gt+" -yearsum "+file_in_pr,output=file_out1)
            cdo.yearsum(input=" -gt "+file_in_pr+" "+file_tmp_wd_p95,output=file_out2)
            
        file_out1 = os.path.join(i_path_out, "R99pTOT.nc")
        file_out2 = os.path.join(i_path_out, "R99p.nc")
        file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
        file_tmp_wd81 = os.path.join(path_temp, "wetdays_81.nc")
        file_tmp_wd_p99 = os.path.join(path_temp, "wetdays_p99.nc")
        file_tmp_wd_p99_gt = os.path.join(path_temp, "wetdays_p99_gt.nc")
        if not os.path.exists(file_out2):
            cdo.ifthen(input= "-gec,1 " + file_in_pr + " " + file_in_pr, output=file_tmp_wd)
            cdo.selyear("1981/2010",input=file_tmp_wd,output=file_tmp_wd81)
            cdo.timpctl(99, input=file_tmp_wd81+" -timmin "+file_tmp_wd81+" -timmax "+file_tmp_wd81, output=file_tmp_wd_p99)
            cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p99+ " "+file_tmp_wd,output=file_tmp_wd_p99_gt)
            cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p99_gt+" -yearsum "+file_in_pr,output=file_out1)
            cdo.yearsum(input=" -gt "+file_in_pr+" "+file_tmp_wd_p99,output=file_out2)
            
           
    
        file_out = os.path.join(i_path_out, "rx1day.nc")
        if not os.path.exists(file_out):
            cdo.etccdi_rx1day(input=file_in_pr, output=file_out)
        
        file_out = os.path.join(i_path_out, "rx5day.nc")
        file_in_chain = "-runsum,5 " + file_in_pr
        if not os.path.exists(file_out):
            cdo.etccdi_rx5day(input=file_in_chain, output=file_out)
        
        file_out = os.path.join(i_path_out, "r10mm.nc")
        file_in_chain = "-gec,10 " + file_in_pr
        if not os.path.exists(file_out):
            cdo.yearsum(input=file_in_chain, output=file_out)
        
        file_out = os.path.join(i_path_out, "r20mm.nc")
        file_in_chain = "-gec,20 " + file_in_pr
        if not os.path.exists(file_out):
            cdo.yearsum(input=file_in_chain, output=file_out)
            
            
        # other indices
        file_out = os.path.join(i_path_out, "HNd.nc")
        # file_in_chain = "-mul -gec,1 " + file_in_pr + " -ltc,2 " + file_in_tasmin
        file_in_chain = "-mul -gec,1 " + file_in_pr + " -ltc,2 " + file_in_tas
        if not os.path.exists(file_out):
            cdo.yearsum(input=file_in_chain, output=file_out)
        
        file_out = os.path.join(i_path_out, "HN.nc")
        # file_in_chain = (" -ifthen -ltc,2 " + file_in_tasmin +
        #                  " -mul " + file_in_pr + 
        #                  " -div -subc,2 " + file_in_tasmin + 
        #                  " -sub " + file_in_tasmin + " " + file_in_tasmax)
        file_in_chain = ("-setmisstoc,0 -ifthen -ltc,2 " + file_in_tas + " " + file_in_pr)
        file_tmp = os.path.join(path_temp, "beforemask.nc")
        if not os.path.exists(file_out):
            cdo.yearsum(input=file_in_chain, output=file_tmp)
            cdo.div(input=file_tmp+" -gtc,-1 -timmin "+file_in_pr,output=file_out) # for masking



