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
# 15th Feb, 2022   CRESPI
##############################################################

CDO_RESET_HISTORY=1 ; 
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/CRESPI';
path_output='/home/climatedata/obs/regrid_data_0.95/CRESPI';

cdo -O -s -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc -chname,temperature,tas $path_input/daily_250m_lonlat/DailySeries_1980_2018_MeanTemp.nc $path_output/DailySeries_1980_2018_MeanTemp_rg.nc

cdo -O -s -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc -chname,precipitation,pr $path_input/daily_250m_lonlat/DailySeries_1980_2018_Prec.nc $path_output/DailySeries_1980_2018_Prec_rg.nc

