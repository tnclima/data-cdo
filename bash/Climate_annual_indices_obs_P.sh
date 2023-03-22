#!/bin/bash
###############################################################
#
# This script creates the datset useful for the study of climate
# indices at annual scale
#
# Indices produced: CDD, SDII, RR1, R95pTOT
#
# 16th March, 2023
##############################################################

path_input='/home/climatedata/obs/regrid_data_0.95/SWITZERLAND';
path_output='/home/climatedata/obs/regrid_data_0.95/data_in_time/climate_indices';
obs='SWITZERLAND';
name_file_dataset='RhiresD_ch02h.lonlat_1961-2021_rg.nc'
variable='pr';

first_year=1961;
last_year=2021;

#################################################
#creation ofmaxe seasonal dataset:
for year in $(eval echo "{$first_year..$last_year}")
do
    cdo selyear,${year} $path_input/$name_file_dataset $path_output/${year}_daily.nc

    #index 
#    cdo eca_cdd $path_output/${year}_daily.nc $path_output/CDD_1_${year}.nc
#    cdo eca_sdii $path_output/${year}_daily.nc $path_output/SII_1_${year}.nc
#     cdo eca_rr1 $path_output/${year}_daily.nc $path_output/RR1_1_${year}.nc
    #R95pTOT
    cp $path_output/${year}_daily.nc $path_output/${year}_daily_forR95.nc                                                             #useful because we need to rewrtite on the same natcdf
    cdo -ifthen -gtc,1 $path_output/${year}_daily_forR95.nc $path_output/${year}_daily_forR95.nc $path_output/${year}_daily_forR95_wetDays.nc #here we are creating a file that contains only data when precipitation is greater then 1mm per day. If precipitation is less than 1mm, it is a NaN. (gtc creates the mask)
    cdo timpctl,95 $path_output/${year}_daily_forR95_wetDays.nc -timmin $path_output/${year}_daily_forR95_wetDays.nc -timmax $path_output/${year}_daily_forR95_wetDays.nc $path_output/${year}_percentile.nc #percentile for each year calculated only over wet days
    cdo replace $path_output/${year}_daily_forR95_wetDays.nc $path_output/${year}_percentile.nc $path_output/${year}_percentile_moreTime.nc
    cdo eca_r95ptot $path_output/${year}_daily_forR95_wetDays.nc $path_output/${year}_percentile_moreTime.nc $path_output/R95pTOT_1_${year}.nc
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
rm $path_output/*percentile*
#############################################
#Calculate the mean:

if [ $obs == "v19HOM" ]; then

  #  cdo mergetime $path_output/CDD_1_* $path_output/CDD_EOBSv19_annual.nc
  #  cdo mergetime $path_output/SII_1_* $path_output/SII_EOBSv19_annual.nc
  #  cdo mergetime $path_output/RR1_1_* $path_output/RR1_EOBSv19_annual.nc
     cdo mergetime $path_output/R95pTOT_1_* $path_output/R95pTOT_EOBSv19_annual.nc 
else
    
  #  cdo mergetime $path_output/CDD_1_* $path_output/CDD_${obs}_annual.nc
  #  cdo mergetime $path_output/SII_1_* $path_output/SII_${obs}_annual.nc
  #  cdo mergetime $path_output/RR1_1_* $path_output/RR1_${obs}_annual.nc
     cdo mergetime $path_output/R95pTOT_1_* $path_output/R95pTOT_${obs}_annual.nc
fi

rm $path_output/*_1_*
