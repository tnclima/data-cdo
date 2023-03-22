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
# 15th Feb, 2022   HYRAS
##############################################################

CDO_RESET_HISTORY=1 ; 
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/HYRAS';
path_output='/home/climatedata/obs/regrid_data_0.95/HYRAS';

cdo remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/pr_hyras_1_1951-2022_v3-0_de.nc $path_output/pr_hyras_1_1951-2022_v3-0_de_rg.nc

cdo -chname,tmax,tasmax -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/tmax_hyras_5_1951-2015_v4-0_de.nc $path_output/tmax_hyras_5_1951-2015_v4-0_de_rg.nc

cdo -chname,tmin,tasmin -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/tmin_hyras_5_1951-2015_v4-0_de.nc $path_output/tmin_hyras_5_1951-2015_v4-0_de_rg.nc

cdo remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/tas_hyras_5_1951-2015_v4-0_de.nc $path_output/tas_hyras_5_1951-2015_v4-0_de_rg.nc

