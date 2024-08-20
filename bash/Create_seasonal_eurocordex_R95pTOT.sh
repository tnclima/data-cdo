#!/bin/bash

###############################################################
#
# This script calculates the climate change indices at
# seasonal scale: R95pTOT
#
# 11 June, 2023
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged/merged_in_time/prova';
path_output='/home/climatedata/eurocordex2-full/indices_etccdi/R95pTOT_seasonal';

#################################################
#I need to
season=("DJF" "MAM" "JJA" "SON")

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

	cdo -mulc,86400 -selmon,3,4,5 ${file} $path_output/MAM_${filename}
	cdo -mulc,86400 -selmon,6,7,8 ${file} $path_output/JJA_${filename}
	cdo -mulc,86400 -selmon,9,10,11 ${file} $path_output/SON_${filename}
	cdo -mulc,86400 -selmon,12,1,2 ${file} $path_output/DJF_${filename}
	
	#index R95pTOT: calculation of the 95th percentile over the entire time series (only wet days) for each season
	for seas in "${season[@]}"
	do
		cdo -ifthen -gtc,1 $path_output/${seas}_${filename} $path_output/${seas}_${filename} $path_output/wet_days_for_95th_percentile.nc               #here we are creating a file that contains only data when precipitation is greater then 1mm per day. If precipitation is less than 1mm, it is a NaN. (gtc creates the mask)
                cdo timpctl,95 $path_output/wet_days_for_95th_percentile.nc -timmin $path_output/wet_days_for_95th_percentile.nc -timmax $path_output/wet_days_for_95th_percentile.nc $path_output/95th_percentile_${seas}.nc #percentile calculated only over wet days and over the entire time series
                rm $path_output/${seas}_${filename}
		rm $path_output/wet_days_for_95th_percentile.nc

		#now for each season and year I need to calculate the total amount of precipitation
		for year in $(seq $first_year $last_year)
		do
			cdo -setattribute,pr@units="mm" -mulc,86400 -selyear,${year} $file $path_output/${year}_daily.nc
			if [ "$seas" == "JJA" ]
                        then
				cdo selmon,6,7,8 $path_output/${year}_daily.nc $path_output/${year}_daily_${seas}.nc
				rm $path_output/${year}_daily.nc
			fi
			if [ "$seas" == "MAM" ]
                        then
                                cdo selmon,3,4,5 $path_output/${year}_daily.nc $path_output/${year}_daily_${seas}.nc
                                rm $path_output/${year}_daily.nc
                        fi
			if [ "$seas" == "SON" ]
                        then
                                cdo selmon,9,10,11 $path_output/${year}_daily.nc $path_output/${year}_daily_${seas}.nc
                                rm $path_output/${year}_daily.nc
                        fi
		        #Winter season is more complicated:
			if [ "$seas" == "DJF" ]
                        then
				if [ ${year} -gt ${first_year} ]
				then
					year_prec=$(( $year - 1 ))
					cdo selmon,1,2 $path_output/${year}_daily.nc $path_output/JF_${year}.nc
					cdo selmon,12 $path_output/${year_prec}_daily.nc $path_output/D_${year_prec}.nc
					cdo mergetime $path_output/D_${year_prec}.nc $path_output/JF_${year}.nc $path_output/${year}_daily_${seas}.nc
					rm $path_output/JF_${year}.nc
					rm $path_output/D_${year_prec}.nc
				fi
			fi

			#calculation of the index
			cp $path_output/${year}_daily_${seas}.nc $path_output/${year}_daily_for_R95.nc  #because I need to write over the data daily
                        cdo -ifthen -gt $path_output/${year}_daily_for_R95.nc $path_output/95th_percentile_${seas}.nc $path_output/${year}_daily_for_R95.nc $path_output/daily_wet_days_above_95th_${year}.nc  #select only days above the 95th percentile
                        cdo -div -timsum $path_output/daily_wet_days_above_95th_${year}.nc -timsum $path_output/${year}_daily_${seas}.nc $path_output/R95pTOT_${year}_${seas}.nc
#			rm $path_output/daily_wet_days_above_95th_${year}.nc

		done
	
	done

	rm 
	cdo mergetime $path_output/R95pTOT_* $path_output/${filename}
done
#	rm $path_output/DJF_*
#	rm $path_output/MAM_*
#	rm $path_output/JJA_*
#	rm $path_output/SON_*


#        rm $path_output/RR1_*
#	rm $path_output/*daily*

#done


