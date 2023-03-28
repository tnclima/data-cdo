#!/bin/bash
###############################################################
#
# This script creates the datset useful for the study of climate
# indices at annual scale
#
# Indices produced: FD, ID, SU, TR
#
# 22th March, 2023
##############################################################

path_input='/home/climatedata/obs/regrid_data_0.95/EOBS/v19HOM';
path_output='/home/climatedata/obs/regrid_data_0.95/data_in_time/climate_indices';
obs='v19HOM';
name_file_dataset_Tmax='tx_ens_mean_0.1deg_GAR_reg_v19.0eHOM_rg.nc'
name_file_dataset_Tmin='tn_ens_mean_0.1deg_GAR_reg_v19.0eHOM_rg.nc'

first_year=1950;
last_year=2018;

#################################################
#creation ofmaxe seasonal dataset:
for year in $(eval echo "{$first_year..$last_year}")
do
    cdo -addc,273.15 -selyear,${year} $path_input/$name_file_dataset_Tmax $path_output/${year}_daily_Tmax.nc
    cdo -addc,273.15 -selyear,${year} $path_input/$name_file_dataset_Tmin $path_output/${year}_daily_Tmin.nc

    #indices     
    cdo eca_fd $path_output/${year}_daily_Tmin.nc $path_output/FD_1_${year}.nc   #TN (daily dataset) have to be given in units of Kelvin
    cdo eca_su $path_output/${year}_daily_Tmax.nc $path_output/SU_1_${year}.nc   #TX (daily dataset) have to be given in units of Kelvin, the parameter T (eca_su,[T]) in Celsius
    cdo eca_tr $path_output/${year}_daily_Tmin.nc $path_output/TR_1_${year}.nc   #TN (daily dataset) have to be given in units of Kelvin, the parameter T (eca_tr,[T]) in Celsius
    #The eca_id function modifies the time, so we calculate by ourselves
    cdo -yearsum -ltc,273.15 $path_output/${year}_daily_Tmax.nc $path_output/ID_1_${year}.nc
done

#Creation annual dataset
if [ $obs == "EOBS" ]; then
   echo "yep EOBS!"
   rm $path_output/*_2022.nc
fi
if [ $obs == "v19HOM" ]; then
   echo "yep EOBS v19HOM!"
   rm $path_output/*_2018.nc
fi
if [ $obs == "SPARTACUS" ]; then
   echo "yep SPARTACUS!"
   rm $path_output/*_2022.nc
fi
if [ $obs == "HYRAS" ]; then
  	if [ $variable == "pr" ]; then
           echo "yep HYRAS!"
           rm $path_output/*_2022.nc
        fi
fi

rm $path_output/*daily*
#############################################
#Calculate the mean:

if [ $obs == "v19HOM" ]; then
      cdo mergetime $path_output/FD_1_* $path_output/FD_EOBSv19_annual.nc
      cdo mergetime $path_output/SU_1_* $path_output/SU_EOBSv19_annual.nc 
      cdo mergetime $path_output/TR_1_* $path_output/TR_EOBSv19_annual.nc
      cdo mergetime $path_output/ID_1_* $path_output/ID_EOBSv19_annual.nc
else
      cdo mergetime $path_output/FD_1_* $path_output/FD_${obs}_annual.nc
      cdo mergetime $path_output/SU_1_* $path_output/SU_${obs}_annual.nc
      cdo mergetime $path_output/TR_1_* $path_output/TR_${obs}_annual.nc
      cdo mergetime $path_output/ID_1_* $path_output/ID_${obs}_annual.nc
fi

rm $path_output/*_1_*
