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
# 14th Feb, 2022   MESAN
##############################################################

path_input='/home/climatedata/obs/MESAN';
path_output='/home/climatedata/obs/regrid_data_0.95/MESAN';

cdo -mulc,86400 -selvar,pr $path_input/pr_GAR-05_SMHI-HIRLAM_RegRean_v1d1-v1d2_SMHI-MESAN_v1_day_1989-2010_vertices.nc $path_input/pr.nc

cdo -addc,-273.15 -selvar,tas $path_input/tas_GAR-05_SMHI-HIRLAM_RegRean_v1d1-v1d2_SMHI-MESAN_v1_day_1989-2010_vertices.nc $path_input/T.nc

CDO_RESET_HISTORY=1 ;
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

cdo -setattribute,pr@units="mm" -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/pr.nc $path_output/pr_GAR-05_SMHI-HIRLAM_RegRean_v1d1-v1d2_SMHI-MESAN_v1_day_1989-2010_vertices_rg.n

cdo -setattribute,tas@units="°C" -remapcon,/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc $path_input/T.nc $path_output/tas_GAR-05_SMHI-HIRLAM_RegRean_v1d1-v1d2_SMHI-MESAN_v1_day_1989-2010_vertices_rg.n
