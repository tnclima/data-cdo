#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# calc indices (monthly for SPEI, seasonal, annual)


import os
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/downscaling-1km_giornaliero/"
path_out = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/"

path_out_monthly = os.path.join(path_out, "downscaling-1km_mensile")
path_out_seasonal = os.path.join(path_out, "downscaling-1km_stagionale")
path_out_annual = os.path.join(path_out, "downscaling-1km_annuale")

all_rcps = os.listdir(path_in)


for rcp in all_rcps:
    
    path_in_rcp = os.path.join(path_in, rcp)
    all_files = os.listdir(path_in_rcp)
    
    path_out_monthly_rcp = os.path.join(path_out_monthly, rcp)
    path_out_seasonal_rcp = os.path.join(path_out_seasonal, rcp)
    path_out_annual_rcp = os.path.join(path_out_annual, rcp)
    os.makedirs(path_out_monthly_rcp, exist_ok=True)
    os.makedirs(path_out_seasonal_rcp, exist_ok=True)
    os.makedirs(path_out_annual_rcp, exist_ok=True)
    
    for file in all_files:
        
        file_in = os.path.join(path_in_rcp, file)
        
        if file.startswith("pr"):
            file_out = os.path.join(path_out_monthly_rcp, file)
            if not os.path.exists(file_out):
                cdo.monsum(input=file_in, output=file_out)
              
            file_out = os.path.join(path_out_seasonal_rcp, file)
            if not os.path.exists(file_out):
                cdo.seassum(input=file_in, output=file_out)
            
            file_out = os.path.join(path_out_annual_rcp, file)
            if not os.path.exists(file_out):
                cdo.yearsum(input=file_in, output=file_out)
        else:
            file_out = os.path.join(path_out_monthly_rcp, file)
            if not os.path.exists(file_out):
                cdo.monmean(input=file_in, output=file_out)
              
            file_out = os.path.join(path_out_seasonal_rcp, file)
            if not os.path.exists(file_out):
                cdo.seasmean(input=file_in, output=file_out)
            
            file_out = os.path.join(path_out_annual_rcp, file)
            if not os.path.exists(file_out):
                cdo.yearmean(input=file_in, output=file_out)
