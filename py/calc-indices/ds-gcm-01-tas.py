#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# calc indices (monthly for SPEI, seasonal, annual)


import os
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/downscaling-1km_giornaliero/"
path_out = path_in

all_rcps = os.listdir(path_in)

for rcp in all_rcps:
    
    path_in_rcp = os.path.join(path_in, rcp)
    all_files = os.listdir(path_in_rcp)
    
    path_out_rcp = path_in_rcp
    # os.makedirs(path_out_rcp, exist_ok=True)
    
    all_models = [x.split("_")[1] for x in all_files]
    all_models = list(set(all_models))
    all_models.sort()
    
    for model in all_models:
        
        file_tasmax = [x for x in all_files if x.startswith("tasmax") and model in x][0]
        file_tasmin = [x for x in all_files if x.startswith("tasmin") and model in x][0]
        
        file_in_chain = (" -setattribute,tas@cell_methods='time: mean'" + 
                         " -chname,tasmax,tas " +
                         " -ensmean " + 
                         os.path.join(path_in_rcp, file_tasmax) + " " + 
                         os.path.join(path_in_rcp, file_tasmin))
        file_out = os.path.join(path_out_rcp, file_tasmax.replace("tasmax", "tas"))
        if not os.path.exists(file_out):        
            cdo.setattribute("tas@long_name='Daily Mean Near-Surface Air Temperature'",
                             input=file_in_chain, output=file_out)