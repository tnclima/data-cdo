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
# 15th Feb, 2022   WFDEI
##############################################################

path_input='/home/climatedata/obs/WFDEI';
path_output='/home/climatedata/obs/regrid_data_0.95/WFDEI';

cdo -mulc,86400 -selvar,pr $path_input/pr_wfdei_1981_2010.nc4 $path_input/pr.nc

cdo -addc,-273.15 -selvar,tasmax $path_input/tasmax_wfdei_1981_2010.nc4 $path_input/T1.nc
cdo -addc,-273.15 -selvar,tasmin $path_input/tasmin_wfdei_1981_2010.nc4 $path_input/T2.nc
cdo -addc,-273.15 -selvar,tas $path_input/tas_wfdei_1981_2010.nc4 $path_input/T3.nc

CDO_RESET_HISTORY=1 ;
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

cdo -setattribute,pr@units="mm" -remapbil,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/pr.nc $path_output/pr_wfdei_1981_2010_rg.nc

cdo -setattribute,tasmax@units="°C" -remapbil,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/T1.nc $path_output/tasmax_wfdei_1981_2010_rg.nc

cdo -setattribute,tasmin@units="°C" -remapbil,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/T2.nc $path_output/tasmin_wfdei_1981_2010_rg.nc

cdo -setattribute,tas@units="°C" -remapbil,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/T3.nc $path_output/tas_wfdei_1981_2010_rg.nc

