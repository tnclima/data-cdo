#!/bin/bash

###############################################################
#
# This script calculates the climate change indices at
# seasonal scale: RR1
#
# 11 June, 2023
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged/merged_in_time';
path_output='/home/climatedata/eurocordex2-full/indices_etccdi/RR1_seasonal';

#################################################
#basename $path_input/tasmax/ciao.nc

#creation of seasonal dataset:
for file in "$path_input"/pr/*
do
	echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
	echo "Nome del file senza percorso: $filename"

	#I need the first and the last year
	dates=$(cdo showdate $file)
	first_year=$(echo "$dates" | head -n 1 | cut -d'-' -f1)
	last_year=$(echo "$dates" | tail -n 1 | cut -d'-' -f1)
	echo "first year $first_year"
	echo "last year $last_year"

	#I need to calculate the index for each season of the year because CDO works with the entire time series
	for year in $(seq $first_year $last_year)
        do
		cdo -setattribute,pr@units="mm" -mulc,86400 -selyear,${year} $file $path_output/${year}_daily.nc

		#subdivide in seasons
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
		cdo -timsum -gtc,1 -mergetime $path_output/DJF_${year}* $path_output/RR1_DJF_${year}.nc
		cdo -timsum -gtc,1 -mergetime $path_output/MAM_${year}* $path_output/RR1_MAM_${year}.nc
		cdo -timsum -gtc,1 -mergetime $path_output/JJA_${year}* $path_output/RR1_JJA_${year}.nc
		cdo -timsum -gtc,1 -mergetime $path_output/SON_${year}* $path_output/RR1_SON_${year}.nc

	done

	rm $path_output/DJF_*
	rm $path_output/MAM_*
	rm $path_output/JJA_*
	rm $path_output/SON_*

	cdo mergetime $path_output/RR1_DJF_* $path_output/RR1_MAM* $path_output/RR1_JJA* $path_output/RR1_SON* $path_output/${filename}

        rm $path_output/RR1_*
	rm $path_output/*daily*

done


