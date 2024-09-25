#!/bin/bash

###############################################################
#
# This script calculates the climate change indices (highlander)
#
# 12 Sept, 2024
##############################################################

path_input='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_giornaliero';
path_output='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_annuale/indices';

#################################################
for year in {1981..2070}
do
	echo "${year}"

	#CDD
	cdo -eca_cdd -selyear,${year} $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/CDD_rcp45_${year}.nc
        cdo -eca_cdd -selyear,${year} $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/CDD_rcp85_${year}.nc

	#SDII
	cdo selyear,${year} $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/pr_45.nc
	cdo selyear,${year} $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/pr_85.nc

	cdo -timmean -ifthen -gtc,1 $path_output/pr_45.nc $path_output/pr_45.nc $path_output/SDII_rcp45_${year}.nc
	cdo -timmean -ifthen -gtc,1 $path_output/pr_85.nc $path_output/pr_85.nc $path_output/SDII_rcp85_${year}.nc
	rm $path_output/pr_45.nc
	rm $path_output/pr_85.nc

        #RR1
	cdo -timsum -gtc,1 -selyear,${year} $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/pr_45.nc
        cdo -timsum -gtc,1 -selyear,${year} $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/pr_85.nc
        cdo -setattribute,RR1@units="" -chname,pr,RR1 $path_output/pr_45.nc $path_output/RR1_rcp45_${year}.nc
	cdo -setattribute,RR1@units="" -chname,pr,RR1 $path_output/pr_85.nc $path_output/RR1_rcp85_${year}.nc
        rm $path_output/pr_45.nc
        rm $path_output/pr_85.nc

	#R20
        cdo -timsum -gtc,20 -selyear,${year} $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/pr_45.nc
        cdo -timsum -gtc,20 -selyear,${year} $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/pr_85.nc
        cdo -setattribute,R20@units="" -chname,pr,R20 $path_output/pr_45.nc $path_output/R20_rcp45_${year}.nc
        cdo -setattribute,R20@units="" -chname,pr,R20 $path_output/pr_85.nc $path_output/R20_rcp85_${year}.nc
        rm $path_output/pr_45.nc
        rm $path_output/pr_85.nc

        #Rx1day
        cdo -yearmax -selyear,${year} $path_input/pr_rcp45_1981-2070_cmcc2km_tn.nc $path_output/Rx1day_rcp45_${year}.nc
        cdo -yearmax -selyear,${year} $path_input/pr_rcp85_1981-2070_cmcc2km_tn.nc $path_output/Rx1day_rcp85_${year}.nc

	#TR
	cdo -timsum -gtc,20 -selyear,${year} $path_input/tasmin_rcp45_1981-2070_cmcc2km_tn.nc $path_output/tasmin_45.nc
	cdo -timsum -gtc,20 -selyear,${year} $path_input/tasmin_rcp85_1981-2070_cmcc2km_tn.nc $path_output/tasmin_85.nc
        cdo -setattribute,TR@units="" -chname,tasmin,TR $path_output/tasmin_45.nc $path_output/TR_rcp45_${year}.nc
        cdo -setattribute,TR@units="" -chname,tasmin,TR $path_output/tasmin_85.nc $path_output/TR_rcp85_${year}.nc
	rm $path_output/tasmin_45.nc
        rm $path_output/tasmin_85.nc

	#ID
	cdo -timsum -ltc,0 -selyear,${year} $path_input/tasmax_rcp45_1981-2070_cmcc2km_tn.nc $path_output/tasmax_45.nc
        cdo -timsum -ltc,0 -selyear,${year} $path_input/tasmax_rcp85_1981-2070_cmcc2km_tn.nc $path_output/tasmax_85.nc
        cdo -setattribute,ID@units="" -chname,tasmax,ID $path_output/tasmax_45.nc $path_output/ID_rcp45_${year}.nc
        cdo -setattribute,ID@units="" -chname,tasmax,ID $path_output/tasmax_85.nc $path_output/ID_rcp85_${year}.nc
        rm $path_output/tasmax_45.nc
        rm $path_output/tasmax_85.nc

	#SU30
        cdo -timsum -gtc,30 -selyear,${year} $path_input/tasmax_rcp45_1981-2070_cmcc2km_tn.nc $path_output/tasmax_45.nc
        cdo -timsum -gtc,30 -selyear,${year} $path_input/tasmax_rcp85_1981-2070_cmcc2km_tn.nc $path_output/tasmax_85.nc
        cdo -setattribute,SU30@units="" -chname,tasmax,SU30 $path_output/tasmax_45.nc $path_output/SU30_rcp45_${year}.nc
        cdo -setattribute,SU30@units="" -chname,tasmax,SU30 $path_output/tasmax_85.nc $path_output/SU30_rcp85_${year}.nc
        rm $path_output/tasmax_45.nc
        rm $path_output/tasmax_85.nc

        cdo -timsum -gtc,25 -selyear,${year} $path_input/tasmax_rcp45_1981-2070_cmcc2km_tn.nc $path_output/tasmax_45.nc
        cdo -timsum -gtc,25 -selyear,${year} $path_input/tasmax_rcp85_1981-2070_cmcc2km_tn.nc $path_output/tasmax_85.nc
        cdo -setattribute,SU@units="" -chname,tasmax,SU $path_output/tasmax_45.nc $path_output/SU_rcp45_${year}.nc
        cdo -setattribute,SU@units="" -chname,tasmax,SU $path_output/tasmax_85.nc $path_output/SU_rcp85_${year}.nc
        rm $path_output/tasmax_45.nc
        rm $path_output/tasmax_85.nc

done

cdo mergetime $path_output/CDD_rcp45_* $path_output/CDD_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/CDD_rcp85_* $path_output/CDD_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/CDD_rcp45_*
rm $path_output/CDD_rcp85_*

cdo mergetime $path_output/SDII_rcp45_* $path_output/SDII_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/SDII_rcp85_* $path_output/SDII_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/SDII_rcp45_*
rm $path_output/SDII_rcp85_*

cdo mergetime $path_output/RR1_rcp45_* $path_output/RR1_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/RR1_rcp85_* $path_output/RR1_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/RR1_rcp45_*
rm $path_output/RR1_rcp85_*

cdo mergetime $path_output/R20_rcp45_* $path_output/R20_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/R20_rcp85_* $path_output/R20_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/R20_rcp45_*
rm $path_output/R20_rcp85_*

cdo mergetime $path_output/Rx1day_rcp45_* $path_output/Rx1day_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/Rx1day_rcp85_* $path_output/Rx1day_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/Rx1day_rcp45_*
rm $path_output/Rx1day_rcp85_*

cdo mergetime $path_output/TR_rcp45_* $path_output/TR_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/TR_rcp85_* $path_output/TR_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/TR_rcp45_*
rm $path_output/TR_rcp85_*

cdo mergetime $path_output/ID_rcp45_* $path_output/ID_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/ID_rcp85_* $path_output/ID_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/ID_rcp45_*
rm $path_output/ID_rcp85_*

cdo mergetime $path_output/SU30_rcp45_* $path_output/SU30_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/SU30_rcp85_* $path_output/SU30_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/SU30_rcp45_*
rm $path_output/SU30_rcp85_*

cdo mergetime $path_output/SU_rcp45_* $path_output/SU_1981-2070_rcp45_cmcc2km_tn.nc
cdo mergetime $path_output/SU_rcp85_* $path_output/SU_1981-2070_rcp85_cmcc2km_tn.nc
rm $path_output/SU_rcp45_*
rm $path_output/SU_rcp85_*

