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
# 14th Feb, 2022   SPARTACUS
##############################################################

CDO_RESET_HISTORY=1 ; 
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/SPARTACUS';
path_output='/home/climatedata/obs/regrid_data_0.95/SPARTACUS';

cdo -setattribute,pr@units="mm" -chname,RR,pr -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/Prec_day_1961-2022.nc $path_output/Prec_day_1961-2022_rg.nc

cdo -chname,Tx,tasmax -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/Tmax_day_1961-2022.nc $path_output/Tmax_day_1961-2022_rg.nc

cdo -chname,Tn,tasmin -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/Tmin_day_1961-2022.nc $path_output/Tmin_day_1961-2022_rg.nc


