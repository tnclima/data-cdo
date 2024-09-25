#!/bin/bash

###############################################################
#
# This script calculates the climate change indices at
# seasonal scale for clt and snc
#
# 2 July, 2023
##############################################################

path_input='/home/climatedata/eurocordex2-full/merged/merged_in_time';

path_output='/home/climatedata/eurocordex2-full/indices/rlds_mean_seasonal';

#################################################
#creation of seasonal dataset:
for file in "$path_input"/rlds/*
do
	echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
	echo "Nome del file senza percorso: $filename"

	#I calculate the seasonal mean
	cdo seasmean $file $path_output/${filename}
done

path_output='/home/climatedata/eurocordex2-full/indices/rlus_mean_seasonal';

#################################################
#creation of seasonal dataset:
for file in "$path_input"/rlus/*
do
        echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
        echo "Nome del file senza percorso: $filename"

        #I calculate the seasonal mean
        cdo seasmean $file $path_output/${filename}
done

path_output='/home/climatedata/eurocordex2-full/indices/rsds_mean_seasonal';

#################################################
#creation of seasonal dataset:
for file in "$path_input"/rsds/*
do
        echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
        echo "Nome del file senza percorso: $filename"

        #I calculate the seasonal mean
        cdo seasmean $file $path_output/${filename}
done

path_output='/home/climatedata/eurocordex2-full/indices/rsus_mean_seasonal';

#################################################
#creation of seasonal dataset:
for file in "$path_input"/rsus/*
do
        echo "File corrente: $file"
        #name of the file
        filename=$(basename "$file")
        echo "Nome del file senza percorso: $filename"

        #I calculate the seasonal mean
        cdo seasmean $file $path_output/${filename}
done

