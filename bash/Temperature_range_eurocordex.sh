#!/bin/bash
###############################################################
#
# This script calculates the temperature range
# at annual and seasonal scale
#
# 14 May, 2023
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged/merged_in_time';
path_output='/home/climatedata/eurocordex2-full/indices';

#################################################
#At first I need to merge the rcp with the correspondent historical
#for historical_file in "${path_input}"/tasmax/*_historical_*
#do
#	file_name=$(basename "$historical_file")
#	prefix=$(echo "$file_name" | sed -r 's|^(.*)_historical_([^_]+_[^_]+)_[0-9]{8}-[0-9]{8}.nc$|\1_\2|')
#	echo $prefix
#done


#Here, I can create the datasets based on the merged models:
for file_tasmax in "$path_input"/tasmax/*
do
	echo "File corrente: $file_tasmax"
        #name of the file without tasmax at the beginning
        filename_tasmax=$(basename "$file_tasmax")
	echo "Nome del file senza percorso: $filename_tasmax"

	#extract the name of the file without the first word
	filename="${filename_tasmax#*_}"

	#construct the file for tasmin
	file_tasmin="$path_input/tasmin/tasmin_${filename}"
	echo "file in tasmin: $file_tasmin"

	#verify that the correspondent file in tasmin exists
	if [ -f "$file_tasmin" ]
	then
		cdo sub $file_tasmax $file_tasmin $path_output/difference.nc
		cdo yearmean $path_output/difference.nc $path_output/temperature-range_mean_annual/$filename_tasmax
		cdo seasmean $path_output/difference.nc $path_output/temperature-range_mean_seasonal/$filename_tasmax
		rm $path_output/difference.nc
	fi
done


