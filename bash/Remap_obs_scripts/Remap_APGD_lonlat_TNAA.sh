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
# 14th Feb, 2022   APGD
##############################################################

#CDO_RESET_HISTORY=1 ;
#export CDO_RESET_HISTORY
#export REMAP_AREA_MIN=0.95

path_input='/home/climatedata/obs/APGD';
path_output='/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/';
path_template='/home/climatedata/downscaling/rcm_lonlat_tnaa/orog/orog_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r0i0p0_CLMcom-CCLM4-8-17_v1_fx.nc';

cdo chname,PRECIPITATION,pr $path_input/APGD_laea_vertices.nc $path_output/prova.nc
cdo setattribute,pr@units="mm" $path_output/prova.nc $path_output/prova1.nc

CDO_RESET_HISTORY=1 ;
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

cdo remapcon,$path_template $path_output/prova1.nc $path_output/pr_apgd.nc

