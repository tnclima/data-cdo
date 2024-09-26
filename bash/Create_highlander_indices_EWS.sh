#!/bin/bash

###############################################################
#
# This script calculates the climate change index (highlander)
# EWS
#
# 25 Sept, 2024
##############################################################

path_input='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_orario';
path_output='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_giornaliero/prova';

#################################################

#for year in {1981..2005}
#do
	#hourly Wind speed
 #       cdo mul $path_input/vas/vas_historical_${year}_cmcc2km_tn.nc $path_input/vas/vas_historical_${year}_cmcc2km_tn.nc $path_output/vas2_${year}.nc
#        cdo mul $path_input/uas/uas_historical_${year}_cmcc2km_tn.nc $path_input/uas/uas_historical_${year}_cmcc2km_tn.nc $path_output/uas2_${year}.nc

#	cdo add $path_output/vas2_${year}.nc $path_output/uas2_${year}.nc $path_output/sum_${year}.nc
#	cdo -chname,V_10M,WSPD10 -sqrt $path_output/sum_${year}.nc $path_input/wind_speed_calculated/wspd10_historical_${year}_cmcc2km_tn.nc
#	rm $path_output/sum_${year}.nc
#	rm $path_output/vas2_${year}.nc
#	rm $path_output/uas2_${year}.nc

#	#daily max of wind speed
#	cdo daymax $path_input/wind_speed_calculated/wspd10_historical_${year}_cmcc2km_tn.nc $path_output/daily_max_${year}.nc
#	cdo timpctl,98 $path_output/daily_max_${year}.nc -timmin $path_output/daily_max_${year}.nc -timmax $path_output/daily_max_${year}.nc $path_output/ESW_${year}.nc
#	rm $path_output/daily_max_${year}.nc
#
#done
#cdo -chname,WSPD10,ESW -mergetime $path_output/ESW_* $path_output/ESWdata_historical_cmcc2km_tn.nc
#rm $path_output/ESW_*

#RCP45
for year in {2006..2070}
do
        #hourly Wind speed
        cdo mul $path_input/vas/vas_rcp45_${year}_cmcc2km_tn.nc $path_input/vas/vas_rcp45_${year}_cmcc2km_tn.nc $path_output/vas2_${year}.nc
        cdo mul $path_input/uas/uas_rcp45_${year}_cmcc2km_tn.nc $path_input/uas/uas_rcp45_${year}_cmcc2km_tn.nc $path_output/uas2_${year}.nc

        cdo add $path_output/vas2_${year}.nc $path_output/uas2_${year}.nc $path_output/sum_${year}.nc
        cdo -chname,V_10M,WSPD10 -sqrt $path_output/sum_${year}.nc $path_input/wind_speed_calculated/wspd10_rcp45_${year}_cmcc2km_tn.nc
        rm $path_output/sum_${year}.nc
        rm $path_output/vas2_${year}.nc
        rm $path_output/uas2_${year}.nc

        #daily max of wind speed
        cdo daymax $path_input/wind_speed_calculated/wspd10_rcp45_${year}_cmcc2km_tn.nc $path_output/daily_max_${year}.nc
        cdo timpctl,98 $path_output/daily_max_${year}.nc -timmin $path_output/daily_max_${year}.nc -timmax $path_output/daily_max_${year}.nc $path_output/ESW_${year}.nc
        rm $path_output/daily_max_${year}.nc

done
cdo -chname,WSPD10,ESW -mergetime $path_output/ESW_* $path_output/ESWdata_rcp45_cmcc2km_tn.nc
rm $path_output/ESW_*

#RCP85
for year in {2006..2070}
do
        #hourly Wind speed
        cdo mul $path_input/vas/vas_rcp85_${year}_cmcc2km_tn.nc $path_input/vas/vas_rcp85_${year}_cmcc2km_tn.nc $path_output/vas2_${year}.nc
        cdo mul $path_input/uas/uas_rcp85_${year}_cmcc2km_tn.nc $path_input/uas/uas_rcp85_${year}_cmcc2km_tn.nc $path_output/uas2_${year}.nc

        cdo add $path_output/vas2_${year}.nc $path_output/uas2_${year}.nc $path_output/sum_${year}.nc
        cdo -chname,V_10M,WSPD10 -sqrt $path_output/sum_${year}.nc $path_input/wind_speed_calculated/wspd10_rcp85_${year}_cmcc2km_tn.nc
        rm $path_output/sum_${year}.nc
        rm $path_output/vas2_${year}.nc
        rm $path_output/uas2_${year}.nc

        #daily max of wind speed
        cdo daymax $path_input/wind_speed_calculated/wspd10_rcp85_${year}_cmcc2km_tn.nc $path_output/daily_max_${year}.nc
        cdo timpctl,98 $path_output/daily_max_${year}.nc -timmin $path_output/daily_max_${year}.nc -timmax $path_output/daily_max_${year}.nc $path_output/ESW_${year}.nc
        rm $path_output/daily_max_${year}.nc

done
cdo -chname,WSPD10,ESW -mergetime $path_output/ESW_* $path_output/ESWdata_rcp85_cmcc2km_tn.nc
rm $path_output/ESW_*
