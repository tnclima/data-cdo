#!/bin/bash

###############################################################
#
# This script calculates the climate change indices at
# seasonal scale for ts
#
# 10 Sept, 2024
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged/merged_in_time';

path_output='/home/climatedata/eurocordex2-full/indices/cll_mean_seasonal';

#################################################
#creation of seasonal dataset:
for file in "$path_input"/cll/*
do
	echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
	echo "Nome del file senza percorso: $filename"

	#I calculate the seasonal mean
	cdo seasmean $file $path_output/${filename}
done

path_output='/home/climatedata/eurocordex2-full/indices/huss_mean_seasonal';
#################################################
#creation of seasonal dataset:
for file in "$path_input"/huss/*
do
        echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
        echo "Nome del file senza percorso: $filename"

        #I calculate the seasonal mean
        cdo seasmean $file $path_output/${filename}
done

