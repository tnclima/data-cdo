#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# calc indices (etccdi)


import os
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_orario/"
path_out = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_annuale_indici/"

# all_rcps = ["rcp45", "rcp85"]

path_temp = "/home/climatedata/tmp/"
path_temp_humidex = "/home/climatedata/tmp/humidex/"
path_temp_humidex3 = "/home/climatedata/tmp/humidex3/"
path_temp_humidex4 = "/home/climatedata/tmp/humidex4/"
path_temp_humidex5 = "/home/climatedata/tmp/humidex5/"
os.makedirs(path_temp, exist_ok=True)
os.makedirs(path_temp_humidex, exist_ok=True)
os.makedirs(path_temp_humidex3, exist_ok=True)
os.makedirs(path_temp_humidex4, exist_ok=True)
os.makedirs(path_temp_humidex5, exist_ok=True)


all_files = os.listdir(os.path.join(path_in, "tas"))
all_files.sort()

# for i_file in all_files:
    
#     file_in_tas = os.path.join(path_in, "tas", i_file)
#     file_in_tdew = os.path.join(path_in, "tdew", i_file.replace("tas_", "tdew_"))
    
#     file_tmp_hum = os.path.join(path_temp, "hum-part2.nc")
#     cdo.expr("'humidex=0.5555*(6.11*exp(5417.7530*(1/273.15-1/(TD_2M)))-10)'",
#              input=file_in_tdew, output=file_tmp_hum)
    
#     file_tmp_hum2 = os.path.join(path_temp_humidex, i_file)
#     cdo.add(input=file_tmp_hum + " " + file_in_tas,
#             output=file_tmp_hum2)
    
#     file_out1 = os.path.join(path_temp_humidex3, i_file)
#     file_out2 = os.path.join(path_temp_humidex4, i_file)
#     file_out3 = os.path.join(path_temp_humidex5, i_file)
#     file_in_chain1 = " -gtc,30 " + " -subc,273.15 " + file_tmp_hum2
#     file_in_chain2 = " -gtc,40 " + " -subc,273.15 " + file_tmp_hum2
#     file_in_chain3 = " -gtc,45 " + " -subc,273.15 " + file_tmp_hum2
#     cdo.yearsum(input=file_in_chain1, output=file_out1)
#     cdo.yearsum(input=file_in_chain2, output=file_out2)
#     cdo.yearsum(input=file_in_chain3, output=file_out3)
    


# humidex3
all_files = os.listdir(path_temp_humidex3)
all_files.sort()

files_hist = [os.path.join(path_temp_humidex3, x) for x in all_files if "hist" in x]
files_rcp45 = [os.path.join(path_temp_humidex3, x) for x in all_files if "rcp45" in x]
files_rcp85 = [os.path.join(path_temp_humidex3, x) for x in all_files if "rcp85" in x]

files_in = " ".join(files_hist) + " " + " ".join(files_rcp45)
file_out = os.path.join(path_out, "Humidex3-hourly_1981-2070_rcp45_cmcc2km_tn.nc")
cdo.mergetime(input=files_in, output=file_out)

files_in = " ".join(files_hist) + " " + " ".join(files_rcp85)
file_out = os.path.join(path_out, "Humidex3-hourly_1981-2070_rcp85_cmcc2km_tn.nc")
cdo.mergetime(input=files_in, output=file_out)


# humidex4
all_files = os.listdir(path_temp_humidex4)
all_files.sort()

files_hist = [os.path.join(path_temp_humidex4, x) for x in all_files if "hist" in x]
files_rcp45 = [os.path.join(path_temp_humidex4, x) for x in all_files if "rcp45" in x]
files_rcp85 = [os.path.join(path_temp_humidex4, x) for x in all_files if "rcp85" in x]

files_in = " ".join(files_hist) + " " + " ".join(files_rcp45)
file_out = os.path.join(path_out, "Humidex4-hourly_1981-2070_rcp45_cmcc2km_tn.nc")
cdo.mergetime(input=files_in, output=file_out)

files_in = " ".join(files_hist) + " " + " ".join(files_rcp85)
file_out = os.path.join(path_out, "Humidex4-hourly_1981-2070_rcp85_cmcc2km_tn.nc")
cdo.mergetime(input=files_in, output=file_out)


# humidex5
all_files = os.listdir(path_temp_humidex5)
all_files.sort()

files_hist = [os.path.join(path_temp_humidex5, x) for x in all_files if "hist" in x]
files_rcp45 = [os.path.join(path_temp_humidex5, x) for x in all_files if "rcp45" in x]
files_rcp85 = [os.path.join(path_temp_humidex5, x) for x in all_files if "rcp85" in x]

files_in = " ".join(files_hist) + " " + " ".join(files_rcp45)
file_out = os.path.join(path_out, "Humidex5-hourly_1981-2070_rcp45_cmcc2km_tn.nc")
cdo.mergetime(input=files_in, output=file_out)

files_in = " ".join(files_hist) + " " + " ".join(files_rcp85)
file_out = os.path.join(path_out, "Humidex5-hourly_1981-2070_rcp85_cmcc2km_tn.nc")
cdo.mergetime(input=files_in, output=file_out)

