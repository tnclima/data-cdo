#!/bin/bash

###############################################################
#
# This script calculates the climate change indices at
# seasonal scale for clt and snc
#
# 2 July, 2023
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged/merged_in_time';
path_output='/home/climatedata/eurocordex2-full/indices/clt_mean_seasonal';

#################################################
#creation of seasonal dataset:
#for file in "$path_input"/clt/*
#do
#	echo "File corrente: $file"
#        #name of the file
#        filename=$(basename "$file")
#	echo "Nome del file senza percorso: $filename"
#
#	#I calculate the seasonal mean
#	cdo seasmean $file $path_output/${filename}
#done
#
##################################################
path_output='/home/climatedata/eurocordex2-full/indices/snc_mean_seasonal';

#################################################
#creation of seasonal dataset:
for file in "$path_input"/snc/*
do
        echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
        echo "Nome del file senza percorso: $filename"

	if [[ "$filename" != "problem" ]]
	then
		#I calculate the seasonal mean
		cdo seasmean $file $path_output/${filename}
	fi
done

