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
# 15th Feb, 2022   EOBS
##############################################################

CDO_RESET_HISTORY=1 ;
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/HISTALP';
path_output='/home/climatedata/obs/regrid_data_0.95/HISTALP';

cdo -chname,TOT_PREC,pr -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/HISTALP_precipitation_all_abs_1801-2014.nc $path_output/HISTALP_precipitation_all_abs_1801-2014_rg.nc 

cdo -chname,T_2M,tas -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/HISTALP_temperature_1780-2014.nc $path_output/HISTALP_temperature_1780-2014_rg.nc

