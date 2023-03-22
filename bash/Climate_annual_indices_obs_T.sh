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

path_input='/home/climatedata/obs/regrid_data_0.95/WFDEI';
path_output='/home/climatedata/obs/regrid_data_0.95/data_in_time/climate_indices';
obs='WFDEI';
name_file_dataset='tasmax_wfdei_1981_2010_rg.nc'
variable='tasmax';

first_year=1981;
last_year=2010;

#################################################
#creation ofmaxe seasonal dataset:
for year in $(eval echo "{$first_year..$last_year}")
do
    cdo -addc,273.15 -selyear,${year} $path_input/$name_file_dataset $path_output/${year}_daily.nc

    #index     
  #  cdo eca_fd $path_output/${year}_daily.nc $path_output/FD_1_${year}.nc   #TN (daily dataset) have to be given in units of Kelvin
 #   cdo eca_su $path_output/${year}_daily.nc $path_output/SU_1_${year}.nc   #TX (daily dataset) have to be given in units of Kelvin, the parameter T (eca_su,[T]) in Celsius
   # cdo eca_tr $path_output/${year}_daily.nc $path_output/TR_1_${year}.nc   #TN (daily dataset) have to be given in units of Kelvin, the parameter T (eca_tr,[T]) in Celsius
     cdo eca_id $path_output/${year}_daily.nc $path_output/ID_1_${year}.nc   #TX (daily dataset) have to be given in units of Kelvin
done

#Creation annual dataset
if [ $obs == "EOBS" ]; then
   echo "yep EOBS!"
   rm $path_output/2022_*
fi
if [ $obs == "v19HOM" ]; then
   echo "yep EOBS v19HOM!"
   rm $path_output/2018_*
fi
if [ $obs == "SPARTACUS" ]; then
   echo "yep SPARTACUS!"
   rm $path_output/2022_*
fi
if [ $obs == "HYRAS" ]; then
  	if [ $variable == "pr" ]; then
           echo "yep HYRAS!"
           rm $path_output/2022_*
        fi
fi

rm $path_output/*daily*
#############################################
#Calculate the mean:

if [ $obs == "v19HOM" ]; then
    # cdo mergetime $path_output/FD_1_* $path_output/FD_EOBSv19_annual.nc
    # cdo mergetime $path_output/SU_1_* $path_output/SU_EOBSv19_annual.nc 
    # cdo mergetime $path_output/TR_1_* $path_output/TR_EOBSv19_annual.nc
      cdo mergetime $path_output/ID_1_* $path_output/ID_EOBSv19_annual.nc
else
    # cdo mergetime $path_output/FD_1_* $path_output/FD_${obs}_annual.nc
    # cdo mergetime $path_output/SU_1_* $path_output/SU_${obs}_annual.nc
    # cdo mergetime $path_output/TR_1_* $path_output/TR_${obs}_annual.nc
     cdo mergetime $path_output/ID_1_* $path_output/ID_${obs}_annual.nc
fi

rm $path_output/*_1_*
