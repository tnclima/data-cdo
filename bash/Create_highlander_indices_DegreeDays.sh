#!/bin/bash

###############################################################
#
# This script calculates the climate change indices (highlander)
# Degree Days
#
# 24 Sept, 2024
##############################################################

path_input='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_giornaliero';
path_output='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_annuale/indices/prova2';

#################################################

for year in {1981..2070}
do
	#HDDs
        cdo selyear,${year} $path_input/tas_rcp45_1981-2070_cmcc2km_tn.nc $path_output/tas_rcp45.nc
        cdo -ifthen -ltc,18 $path_output/tas_rcp45.nc $path_output/tas_rcp45.nc $path_output/less_t.nc
	cdo -timsum -expr,"HDDs=-tas" -subc,18 $path_output/less_t.nc $path_output/HDDs_rcp45_${year}.nc
        rm $path_output/tas_rcp45.nc
        rm $path_output/less_t.nc

        cdo selyear,${year} $path_input/tas_rcp85_1981-2070_cmcc2km_tn.nc $path_output/tas_rcp85.nc
        cdo -ifthen -ltc,18 $path_output/tas_rcp85.nc $path_output/tas_rcp85.nc $path_output/less_t.nc
        cdo -timsum -expr,"HDDs=-tas" -subc,18 $path_output/less_t.nc $path_output/HDDs_rcp85_${year}.nc
        rm $path_output/tas_rcp85.nc
        rm $path_output/less_t.nc

	#CDDs
        cdo selyear,${year} $path_input/tas_rcp45_1981-2070_cmcc2km_tn.nc $path_output/tas_rcp45.nc
        cdo -subc,22 -ifthen -gtc,22 $path_output/tas_rcp45.nc $path_output/tas_rcp45.nc $path_output/above_t.nc
        cdo timsum $path_output/above_t.nc $path_output/CDDs_rcp45_${year}.nc
        rm $path_output/tas_rcp45.nc
        rm $path_output/above_t.nc

        cdo selyear,${year} $path_input/tas_rcp85_1981-2070_cmcc2km_tn.nc $path_output/tas_rcp85.nc
        cdo -subc,22 -ifthen -gtc,22 $path_output/tas_rcp85.nc $path_output/tas_rcp85.nc $path_output/above_t.nc
        cdo timsum $path_output/above_t.nc $path_output/CDDs_rcp85_${year}.nc
        rm $path_output/tas_rcp85.nc
        rm $path_output/above_t.nc
done

cdo -setattribute,HDDs@units="" -mergetime $path_output/HDDs_rcp45_* $path_output/HDDs_1981-2070_rcp45_cmcc2km_tn.nc
cdo -setattribute,CDDs@units="" -chname,tas,CDDs -mergetime $path_output/CDDs_rcp45_* $path_output/CDDs_1981-2070_rcp45_cmcc2km_tn.nc
rm $path_output/HDDs_rcp45_*
rm $path_output/CDDs_rcp45_*
cdo setmisstoc,0 $path_output/HDDs_1981-2070_rcp45_cmcc2km_tn.nc $path_output/HDDs_1981-2070_rcp45_cmcc2km_tn.nc #here I change NaNs with zeros
cdo setmisstoc,0 $path_output/CDDs_1981-2070_rcp45_cmcc2km_tn.nc $path_output/CDDs_1981-2070_rcp45_cmcc2km_tn.nc #here I change NaNs with zeros

cdo -setattribute,HDDs@units="" -mergetime $path_output/HDDs_rcp85_* $path_output/HDDs_1981-2070_rcp85_cmcc2km_tn.nc
cdo -setattribute,CDDs@units="" -chname,tas,CDDs -mergetime $path_output/CDDs_rcp85_* $path_output/CDDs_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/HDDs_rcp85_*
rm $path_output/CDDs_rcp85_*
cdo setmisstoc,0 $path_output/HDDs_1981-2070_rcp85_cmcc2km_tn.nc $path_output/HDDs_1981-2070_rcp85_cmcc2km_tn.nc #here I change NaNs with zeros
cdo setmisstoc,0 $path_output/CDDs_1981-2070_rcp85_cmcc2km_tn.nc $path_output/CDDs_1981-2070_rcp85_cmcc2km_tn.nc #here I change NaNs with zeros

