#!/bin/bash

###############################################################
#
# This script calculates the climate change indices (highlander)
# R9XpTOT and R9X
#
# 24 Sept, 2024
##############################################################

path_input='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_giornaliero';
path_output='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_annuale/indices/prova';

#################################################

#calculation of the 95th and 99th percentile over the 1981-2010 time period (only wet days)

cdo selyear,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010 $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/pr_rcp45.nc
cdo -ifthen -gtc,1 $path_output/pr_rcp45.nc $path_output/pr_rcp45.nc $path_output/wet_days_for_percentile_rcp45.nc               #here we are creating a file that contains only data when precipitation is greater then 1mm per day. If precipitation is less than 1mm, it is a NaN. (gtc creates the mask)
cdo selyear,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010 $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/pr_rcp85.nc
cdo -ifthen -gtc,1 $path_output/pr_rcp85.nc $path_output/pr_rcp85.nc $path_output/wet_days_for_percentile_rcp85.nc               #here we are creating a file that contains only data when precipitation is greater then 1mm per day. If precipitation is less than 1mm, it is a NaN. (gtc creates the mask)

#percentile calculation
cdo timpctl,95 $path_output/wet_days_for_percentile_rcp45.nc -timmin $path_output/wet_days_for_percentile_rcp45.nc -timmax $path_output/wet_days_for_percentile_rcp45.nc $path_output/95th_percentile_rcp45.nc 
cdo timpctl,95 $path_output/wet_days_for_percentile_rcp85.nc -timmin $path_output/wet_days_for_percentile_rcp85.nc -timmax $path_output/wet_days_for_percentile_rcp85.nc $path_output/95th_percentile_rcp85.nc

cdo timpctl,99 $path_output/wet_days_for_percentile_rcp45.nc -timmin $path_output/wet_days_for_percentile_rcp45.nc -timmax $path_output/wet_days_for_percentile_rcp45.nc $path_output/99th_percentile_rcp45.nc
cdo timpctl,99 $path_output/wet_days_for_percentile_rcp85.nc -timmin $path_output/wet_days_for_percentile_rcp85.nc -timmax $path_output/wet_days_for_percentile_rcp85.nc $path_output/99th_percentile_rcp85.nc

rm $path_output/wet_days_for_percentile_rcp85.nc
rm $path_output/wet_days_for_percentile_rcp45.nc
rm $path_output/pr_rcp85.nc
rm $path_output/pr_rcp45.nc

for year in {1981..2070}
do
	#R95pTOT and R95
	cdo selyear,${year} $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/pr_rcp45.nc
        cdo -ifthen -gt $path_output/pr_rcp45.nc $path_output/95th_percentile_rcp45.nc $path_output/pr_rcp45.nc $path_output/daily_wet_days_above_95th_rcp45.nc  #select only days above the 95th percentile
	cdo setmisstoc,0 $path_output/daily_wet_days_above_95th_rcp45.nc $path_output/daily_wet_days_above_95th_rcp45_noNaN.nc #here I change NaNs with zeros, in this case we don't have problems with the yearsum
        cdo -div -yearsum $path_output/daily_wet_days_above_95th_rcp45_noNaN.nc -yearsum $path_output/pr_rcp45.nc $path_output/R95pTOT_rcp45_${year}.nc #here R95pTOT
        cdo -timsum -gt $path_output/pr_rcp45.nc $path_output/95th_percentile_rcp45.nc $path_output/R95_rcp45_${year}.nc  #here R95
	rm $path_output/pr_rcp45.nc
	rm $path_output/daily_wet_days_above_95th_rcp45.nc
	rm $path_output/daily_wet_days_above_95th_rcp45_noNaN.nc

	cdo selyear,${year} $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/pr_rcp85.nc
        cdo -ifthen -gt $path_output/pr_rcp85.nc $path_output/95th_percentile_rcp85.nc $path_output/pr_rcp85.nc $path_output/daily_wet_days_above_95th_rcp85.nc  #select only days above the 95th percentile
        cdo setmisstoc,0 $path_output/daily_wet_days_above_95th_rcp85.nc $path_output/daily_wet_days_above_95th_rcp85_noNaN.nc #here I change NaNs with zeros, in this case we don't have problems with the yearsum
	cdo -div -yearsum $path_output/daily_wet_days_above_95th_rcp85_noNaN.nc -yearsum $path_output/pr_rcp85.nc $path_output/R95pTOT_rcp85_${year}.nc
        cdo -timsum -gt $path_output/pr_rcp85.nc $path_output/95th_percentile_rcp85.nc $path_output/R95_rcp85_${year}.nc  #here R95
	rm $path_output/pr_rcp85.nc
        rm $path_output/daily_wet_days_above_95th_rcp85.nc
        rm $path_output/daily_wet_days_above_95th_rcp85_noNaN.nc

        #R99pTOT and R99
        cdo selyear,${year} $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/pr_rcp45.nc
        cdo -ifthen -gt $path_output/pr_rcp45.nc $path_output/99th_percentile_rcp45.nc $path_output/pr_rcp45.nc $path_output/daily_wet_days_above_99th_rcp45.nc  #select only days above the 95th percentile
        cdo setmisstoc,0 $path_output/daily_wet_days_above_99th_rcp45.nc $path_output/daily_wet_days_above_99th_rcp45_noNaN.nc #here I change NaNs with zeros, in this case we don't have problems with the yearsum  
  	cdo -div -yearsum $path_output/daily_wet_days_above_99th_rcp45_noNaN.nc -yearsum $path_output/pr_rcp45.nc $path_output/R99pTOT_rcp45_${year}.nc
        cdo -timsum -gt $path_output/pr_rcp45.nc $path_output/99th_percentile_rcp45.nc $path_output/R99_rcp45_${year}.nc  #here R99
	rm $path_output/pr_rcp45.nc
        rm $path_output/daily_wet_days_above_99th_rcp45.nc
	rm $path_output/daily_wet_days_above_99th_rcp45_noNaN.nc

        cdo selyear,${year} $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/pr_rcp85.nc
        cdo -ifthen -gt $path_output/pr_rcp85.nc $path_output/99th_percentile_rcp85.nc $path_output/pr_rcp85.nc $path_output/daily_wet_days_above_99th_rcp85.nc  #select only days above the 95th percentile
        cdo setmisstoc,0 $path_output/daily_wet_days_above_99th_rcp85.nc $path_output/daily_wet_days_above_99th_rcp85_noNaN.nc #here I change NaNs with zeros, in this case we don't have problems with the yearsum
	cdo -div -yearsum $path_output/daily_wet_days_above_99th_rcp85_noNaN.nc -yearsum $path_output/pr_rcp85.nc $path_output/R99pTOT_rcp85_${year}.nc
        cdo -timsum -gt $path_output/pr_rcp85.nc $path_output/99th_percentile_rcp85.nc $path_output/R99_rcp85_${year}.nc  #here R99
	rm $path_output/pr_rcp85.nc
        rm $path_output/daily_wet_days_above_99th_rcp85.nc
	rm $path_output/daily_wet_days_above_99th_rcp85_noNaN.nc
done

cdo -setattribute,R95pTOT@units="" -chname,pr,R95pTOT -mergetime $path_output/R95pTOT_rcp45_* $path_output/R95pTOT_1981-2070_rcp45_cmcc2km_tn.nc
cdo -setattribute,R95pTOT@units="" -chname,pr,R95pTOT -mergetime $path_output/R95pTOT_rcp85_* $path_output/R95pTOT_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/R95pTOT_rcp45_*
rm $path_output/R95pTOT_rcp85_*

cdo -setattribute,R99pTOT@units="" -chname,pr,R99pTOT -mergetime $path_output/R99pTOT_rcp45_* $path_output/R99pTOT_1981-2070_rcp45_cmcc2km_tn.nc
cdo -setattribute,R99pTOT@units="" -chname,pr,R99pTOT -mergetime $path_output/R99pTOT_rcp85_* $path_output/R99pTOT_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/R99pTOT_rcp45_*
rm $path_output/R99pTOT_rcp85_*

cdo -setattribute,R95@units="" -chname,pr,R95 -mergetime $path_output/R95_rcp45_* $path_output/R95_1981-2070_rcp45_cmcc2km_tn.nc
cdo -setattribute,R95@units="" -chname,pr,R95 -mergetime $path_output/R95_rcp85_* $path_output/R95_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/R95_rcp45_*
rm $path_output/R95_rcp85_*

cdo -setattribute,R99@units="" -chname,pr,R99 -mergetime $path_output/R99_rcp45_* $path_output/R99_1981-2070_rcp45_cmcc2km_tn.nc
cdo -setattribute,R99@units="" -chname,pr,R99 -mergetime $path_output/R99_rcp85_* $path_output/R99_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/R99_rcp45_*
rm $path_output/R99_rcp85_*
