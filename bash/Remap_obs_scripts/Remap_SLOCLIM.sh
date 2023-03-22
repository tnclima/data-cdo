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
# 13th Feb, 2022   SLOCLIM
##############################################################

#CDO_RESET_HISTORY=1 ; 
#export CDO_RESET_HISTORY
#export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/SLOCLIM';
path_output='/home/climatedata/obs/regrid_data_0.95/SLOCLIM';

cdo -chname,pcp,pr -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/sloclim_pcp.nc $path_output/sloclim_pcp_rg_prova.nc

cdo -chname,tx,tasmax -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/sloclim_tmax_h.nc $path_output/sloclim_tmax_rg_prova.nc

#cdo -chname,tn,tasmin -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/sloclim_tmin_h.nc $path_output/sloclim_tmin_rg.nc
