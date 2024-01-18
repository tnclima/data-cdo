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

path_input='/home/climatedata/obs/EOBS';
path_output='/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/';
path_template='/home/climatedata/downscaling/rcm_lonlat_tnaa/orog/orog_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r0i0p0_CLMcom-CCLM4-8-17_v1_fx.nc';

cdo -chname,rr,pr -remapcon,$path_template $path_input/rr_ens_mean_0.1deg_GAR_reg_v26.0e.nc $path_output/pr_eobs_v26.nc

cdo -chname,tn,tasmin -remapcon,$path_template $path_input/tn_ens_mean_0.1deg_GAR_reg_v26.0e.nc $path_output/tasmin_eobs_v26.nc

cdo -chname,tx,tasmax -remapcon,$path_template $path_input/tx_ens_mean_0.1deg_GAR_reg_v26.0e.nc $path_output/tasmax_eobs_v26.nc

cdo -chname,tg,tas -remapcon,$path_template $path_input/tg_ens_mean_0.1deg_GAR_reg_v26.0e.nc $path_output/tas_eobs_v26.nc



