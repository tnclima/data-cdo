#!/bin/bash
###############################################################
#
# This script creates datasets regridded over the Alpine
# Region and characterized by CORDEX grid resolution. Here
# we use the conservative method with an area min of 95%.
#
# Moreover, here name variables are changed and sometimes also
# the unit of measure.
#
# 15th Feb, 2022   SWITZERLAND
##############################################################

CDO_RESET_HISTORY=1 ; 
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/SWITZERLAND';
path_output='/home/climatedata/obs/regrid_data_0.95/SWITZERLAND';

cdo -chname,RhiresD,pr -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/setgrid_noDuplicates/RhiresD_ch02h.lonlat_1961-2021_NoDuplicates.nc $path_output/RhiresD_ch02h.lonlat_1961-2021_rg.nc

cdo -chname,TabsD,tas -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/setgrid_noDuplicates/TabsD_ch02h.lonlat_1961-2021_NoDuplicates.nc $path_output/TabsD_ch02h.lonlat_1961-2021_NoDuplicates_rg.nc

cdo -chname,TminD,tasmin -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/setgrid_noDuplicates/TminD_ch02h.lonlat_1971-2021_NoDuplicates.nc $path_output/TminD_ch02h.lonlat_1971-2021_NoDuplicates_rg.nc

cdo -chname,TmaxD,tasmax -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/setgrid_noDuplicates/TmaxD_ch02h.lonlat_1971-2021_NoDuplicates.nc $path_output/TmaxD_ch02h.lonlat_1971-2021_NoDuplicates_rg.nc
