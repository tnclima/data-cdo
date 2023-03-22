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
# 28th Feb, 2023   E-OBS homo
##############################################################

CDO_RESET_HISTORY=1 ; 
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/EOBS/v19HOM';
path_output='/home/climatedata/obs/regrid_data_0.95/EOBS/v19HOM';

cdo -chname,tn,tasmin -remapcon,/home/climatedata/obs/regrid_data_0.95/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/tn_ens_mean_0.1deg_GAR_reg_v19.0eHOM.nc $path_output/tn_ens_mean_0.1deg_GAR_reg_v19.0eHOM_rg.nc

cdo -chname,tg,tas -remapcon,/home/climatedata/obs/regrid_data_0.95/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/tg_ens_mean_0.1deg_GAR_reg_v19.0eHOM.nc $path_output/tg_ens_mean_0.1deg_GAR_reg_v19.0eHOM_rg.nc

cdo -chname,tx,tasmax -remapcon,/home/climatedata/obs/regrid_data_0.95/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/tx_ens_mean_0.1deg_GAR_reg_v19.0eHOM.nc $path_output/tx_ens_mean_0.1deg_GAR_reg_v19.0eHOM_rg.nc
