#!/bin/bash
###############################################################
#
# This script calculates the temperature range
# at annual and seasonal scale
#
# 14 May, 2023
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged';
path_output='/home/climatedata/eurocoerdex2-full/indices';

#################################################
#basename $path_input/tasmax/ciao.nc

#creation ofmaxe seasonal dataset:
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
		rm $path_output/temperature-range_mean_annual/difference.nc
	fi
done


