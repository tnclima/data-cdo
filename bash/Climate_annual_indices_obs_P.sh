#!/bin/bash
###############################################################
#
# This script creates the datset useful for the study of climate
# indices at annual scale
#
# Indices produced: CDD, SDII, RR1, R95pTOT
#
# We didn't use the eca command in cdo for RR1, SDII, R95pTOT
# because it destroys the time information in the netcdf files. 
#
# 24th March, 2023
##############################################################

path_input='/home/climatedata/obs/regrid_data_0.95/CRESPI';
path_output='/home/climatedata/obs/regrid_data_0.95/data_in_time/climate_indices';
obs='CRESPI';
name_file_dataset='DailySeries_1980_2018_Prec_rg.nc'
variable='pr';

first_year=1980;
last_year=2018;

#################################################

#index R95pTOT: calculation of the 95th percentile over the entire time series (only wet days)

cp $path_input/${name_file_dataset} $path_output/copy_${name_file_dataset}
cdo -ifthen -gtc,1 $path_output/copy_${name_file_dataset} $path_output/copy_${name_file_dataset} $path_output/wet_days_for_95th_percentile.nc               #here we are creating a file that contains only data when precipitation is greater then 1mm per day. If precipitation is less than 1mm, it is a NaN. (gtc creates the mask)
cdo timpctl,95 $path_output/wet_days_for_95th_percentile.nc -timmin $path_output/wet_days_for_95th_percentile.nc -timmax $path_output/wet_days_for_95th_percentile.nc $path_output/95th_percentile.nc #percentile calculated only over wet days and over the entire time series

rm $path_output/copy_${name_file_dataset}

#creation of the indices at annual time scale:
for year in $(eval echo "{$first_year..$last_year}")
do
    cdo selyear,${year} $path_input/$name_file_dataset $path_output/${year}_daily.nc

    #index CDD
    if [ $obs == "CRESPI" ]; then
       cdo -setctomiss,0 -eca_cdd  $path_output/${year}_daily.nc $path_output/CDD_1_${year}.nc
       else
       cdo eca_cdd $path_output/${year}_daily.nc $path_output/CDD_1_${year}.nc
    fi

    #index SDII
    cp $path_output/${year}_daily.nc $path_output/${year}_daily_for_RR1.nc  #because I need to write over the data daily
    cdo -timmean -ifthen -gtc,1 $path_output/${year}_daily_for_RR1.nc $path_output/${year}_daily_for_RR1.nc $path_output/SDII_1_${year}.nc 

    #index RR1
    cdo -yearsum -gtc,1 $path_output/${year}_daily.nc $path_output/RR1_1_${year}.nc

    #index R95pTOT
    cp $path_output/${year}_daily.nc $path_output/${year}_daily_for_R95.nc  #because I need to write over the data daily
    cdo -ifthen -gt $path_output/${year}_daily_for_R95.nc $path_output/95th_percentile.nc $path_output/${year}_daily_for_R95.nc $path_output/daily_wet_days_above_95th_${year}.nc  #select only days above the 95th percentile
    cdo -div -yearsum $path_output/daily_wet_days_above_95th_${year}.nc -yearsum $path_output/${year}_daily.nc $path_output/R95pTOT_1_${year}.nc
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
rm $path_output/*percentile*
#############################################
#Calculate the mean:

if [ $obs == "v19HOM" ]; then

     cdo mergetime $path_output/CDD_1_* $path_output/CDD_EOBSv19_annual.nc
     cdo mergetime $path_output/SDII_1_* $path_output/SDII_EOBSv19_annual.nc
     cdo mergetime $path_output/RR1_1_* $path_output/RR1_EOBSv19_annual.nc
     cdo mergetime $path_output/R95pTOT_1_* $path_output/R95pTOT_EOBSv19_annual.nc 
else
    
     cdo mergetime $path_output/CDD_1_* $path_output/CDD_${obs}_annual.nc
     cdo mergetime $path_output/SDII_1_* $path_output/SDII_${obs}_annual.nc
     cdo mergetime $path_output/RR1_1_* $path_output/RR1_${obs}_annual.nc
     cdo mergetime $path_output/R95pTOT_1_* $path_output/R95pTOT_${obs}_annual.nc
fi

rm $path_output/*_1_*
