#!/bin/bash
###############################################################
#
# This scripts creates the datset useful for the study subdivided
# into annual and seasonal data
#
# 15th Feb, 2023
##############################################################

path_input='/home/climatedata/obs/regrid_data_0.95/METEOFRANCE';
path_output='/home/climatedata/obs/regrid_data_0.95/data_in_time';
obs='METEOFRANCE';
name_file_dataset='pr_rg.nc'
variable='pr';

first_year=1958;
last_year=2018;

#################################################
#creation ofmaxe seasonal dataset:
for year in $(eval echo "{$first_year..$last_year}")
do
    cdo selyear,${year} $path_input/$name_file_dataset $path_output/${year}_daily.nc

    #Seasonal
    cdo selmon,3,4,5 $path_output/${year}_daily.nc $path_output/MAM_${year}.nc
    cdo selmon,6,7,8 $path_output/${year}_daily.nc $path_output/JJA_${year}.nc
    cdo selmon,9,10,11 $path_output/${year}_daily.nc $path_output/SON_${year}.nc
    
    #Winter season is more complicated:
        if [ ${year} -gt ${first_year} ]
        then
                year_prec=$(( $year - 1 ))
                cdo selmon,1,2 $path_output/${year}_daily.nc $path_output/JF_${year}.nc
                cdo selmon,12 $path_output/${year_prec}_daily.nc $path_output/D_${year_prec}.nc
                cdo mergetime $path_output/D_${year_prec}.nc $path_output/JF_${year}.nc $path_output/DJF_${year}.nc

                rm $path_output/JF_${year}.nc
                rm $path_output/D_${year_prec}.nc
        fi
done

if [ $obs == "EOBS" ]; then
   echo "yep EOBS!"
   rm $path_output/JJA_2022.nc
fi
if [ $obs == "SPARTACUS" ]; then
   echo "yep SPARTACUS!"
   rm $path_output/JJA_2022.nc
fi
if [ $obs == "HYRAS" ]; then
	if [ $variable == "pr" ]; then
           echo "yep HYRAS!"
           rm $path_output/SON_2022.nc
	fi
fi

cdo mergetime $path_output/DJF* $path_output/MAM* $path_output/JJA* $path_output/SON* $path_output/seasonal.nc

rm $path_output/DJF*
rm $path_output/MAM*
rm $path_output/JJA*
rm $path_output/SON*

#Creation annual dataset
if [ $obs == "EOBS" ]; then
   echo "yep EOBS!"
   rm $path_output/2022_daily.nc
fi
if [ $obs == "v19HOM" ]; then
   echo "yep EOBS v19HOM!"
   rm $path_output/2018_daily.nc
fi
if [ $obs == "SPARTACUS" ]; then
   echo "yep SPARTACUS!"
   rm $path_output/2022_daily.nc
fi
if [ $obs == "HYRAS" ]; then
  	if [ $variable == "pr" ]; then
           echo "yep HYRAS!"
           rm $path_output/2022_daily.nc
        fi
fi

cdo mergetime $path_output/*daily* $path_output/annual.nc
rm $path_output/*daily*

#############################################
#Calculate the mean:
if [ $obs == "v19HOM" ]; then

    cdo seasmean $path_output/seasonal.nc $path_output/${variable}_EOBSv19_mean_seasonal.nc
    cdo yearmean $path_output/annual.nc $path_output/${variable}_EOBSv19_mean_annual.nc
else
    cdo seasmean $path_output/seasonal.nc $path_output/${variable}_${obs}_mean_seasonal.nc
    cdo yearmean $path_output/annual.nc $path_output/${variable}_${obs}_mean_annual.nc
fi

#Calculate percentiles:
for VARIABLE in 1 5 10 50 90 95 99
do
   if [ $obs == "v19HOM" ]; then
      cdo yearpctl,${VARIABLE} $path_output/annual.nc -yearmin $path_output/annual.nc -yearmax $path_output/annual.nc $path_output/${variable}_EOBSv19_${VARIABLE}pct_annual.nc
      cdo seaspctl,${VARIABLE} $path_output/seasonal.nc -seasmin $path_output/seasonal.nc -seasmax $path_output/seasonal.nc $path_output/${variable}_EOBSv19_${VARIABLE}pct_seasonal.nc
   else
      cdo yearpctl,${VARIABLE} $path_output/annual.nc -yearmin $path_output/annual.nc -yearmax $path_output/annual.nc $path_output/${variable}_${obs}_${VARIABLE}pct_annual.nc
      cdo seaspctl,${VARIABLE} $path_output/seasonal.nc -seasmin $path_output/seasonal.nc -seasmax $path_output/seasonal.nc $path_output/${variable}_${obs}_${VARIABLE}pct_seasonal.nc
   fi

done
rm $path_output/seasonal.nc
rm $path_output/annual.nc

