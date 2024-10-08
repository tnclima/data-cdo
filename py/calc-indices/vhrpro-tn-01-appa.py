#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# calc indices (etccdi)


import os
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_giornaliero/"
path_out = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_annuale_indici/"

all_rcps = ["rcp45", "rcp85"]

path_temp = "/home/climatedata/tmp/"
os.makedirs(path_temp, exist_ok=True)


for rcp in all_rcps:
    
    all_files = os.listdir(path_in)
    
    file_tasmax = [x for x in all_files if "tasmax" in x and rcp in x][0]
    file_tasmin = [x for x in all_files if "tasmin" in x and rcp in x][0]
    file_tas = [x for x in all_files if "tas_" in x and rcp in x][0]
    file_tdew = [x for x in all_files if "tdew" in x and rcp in x][0]
    file_pr = [x for x in all_files if "pr" in x and rcp in x][0]
    
    file_in_tasmax = os.path.join(path_in, file_tasmax)
    file_in_tasmin = os.path.join(path_in, file_tasmin)
    file_in_tas = os.path.join(path_in, file_tas)
    file_in_tdew = os.path.join(path_in, file_tdew)
    file_in_pr = os.path.join(path_in, file_pr)
    
    
    # CDD_1981-2070_rcp45_cmcc2km_tn.nc
    suffix_fn = "_1981-2070_" + rcp + "_cmcc2km_tn.nc"
    
    # other indices
    file_out = os.path.join(path_out, "HNd" + suffix_fn)
    # file_in_chain = "-mul -gec,2 " + file_in_pr + " -ltc,2 " + file_in_tasmin
    file_in_chain = "-mul -gec,1 " + file_in_pr + " -ltc,2 " + file_in_tas
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
    
    file_out = os.path.join(path_out, "HN" + suffix_fn)
    # file_in_chain = (" -ifthen -ltc,2 " + file_in_tasmin +
    #                  " -mul " + file_in_pr + 
    #                  " -div -subc,2 " + file_in_tasmin + 
    #                  " -sub " + file_in_tasmin + " " + file_in_tasmax)
    file_in_chain = (" -setmisstoc,0 -ifthen -ltc,2 " + file_in_tas + " " + file_in_pr)
    if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
  

    file_out1 = os.path.join(path_out, "Humidex3" + suffix_fn)
    file_out2 = os.path.join(path_out, "Humidex4" + suffix_fn)
    file_out3 = os.path.join(path_out, "Humidex5" + suffix_fn)
    file_tmp_hum = os.path.join(path_temp, "humidex.nc")
    file_in_chain1 = " -gtc,30 -add " + file_in_tas + " " + file_tmp_hum
    file_in_chain2 = " -gtc,40 -add " + file_in_tas + " " + file_tmp_hum
    file_in_chain3 = " -gtc,45 -add " + file_in_tas + " " + file_tmp_hum
    if not os.path.exists(file_out1):
        cdo.expr("'humidex=0.5555*(6.11*exp(5417.7530*(1/273.15-1/(273.15+tdew)))-10)'",
                 input=file_in_tdew, output=file_tmp_hum)
        cdo.yearsum(input=file_in_chain1, output=file_out1)
        cdo.yearsum(input=file_in_chain2, output=file_out2)
        cdo.yearsum(input=file_in_chain3, output=file_out3)
   


