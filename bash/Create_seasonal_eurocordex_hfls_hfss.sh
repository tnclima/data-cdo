#!/bin/bash

###############################################################
#
# This script calculates the climate change indices at
# seasonal scale
#
# 17 Sept, 2024
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged/merged_in_time';

path_output='/home/climatedata/eurocordex2-full/indices/hfls_mean_seasonal';

#################################################
#creation of seasonal dataset:
for file in "$path_input"/hfls/*
do
	echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
	echo "Nome del file senza percorso: $filename"

	#I calculate the seasonal mean
	cdo seasmean $file $path_output/${filename}
done

path_output='/home/climatedata/eurocordex2-full/indices/hfss_mean_seasonal';
#################################################
#creation of seasonal dataset:
for file in "$path_input"/hfss/*
do
        echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
        echo "Nome del file senza percorso: $filename"

        #I calculate the seasonal mean
        cdo seasmean $file $path_output/${filename}
done


