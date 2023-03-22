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
path_output='/home/climatedata/obs/regrid_data_0.95/APGD';

cdo chname,PRECIPITATION,pr $path_input/APGD_laea_vertices.nc $path_output/prova.nc
cdo setattribute,pr@units="mm" $path_output/prova.nc $path_output/prova1.nc

CDO_RESET_HISTORY=1 ;
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

cdo remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_output/prova1.nc $path_output/APGD_laea_vertices_rg.nc

