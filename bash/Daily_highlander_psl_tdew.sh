#######################################################################
# This script calculates the daily precipitation and temperature from 
# hourly highlander dataset

# 8 June, 2023   Anna Napoli
########################################################################
path_output='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_giornaliero'
path_input='/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_orario'
##########################################################################
CDO_RESET_HISTORY=1 ;
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

# Now the loop starts:
# HISTORICAL
for year in {1981..2005} #2005
do
	echo "$year"

	cdo -addc,-273.15 -daymean $path_input/tdew/tdew_historical_${year}_cmcc2km_tn.nc $path_output/tdew/provaTdew.nc
        cdo daymean $path_input/psl/psl_historical_${year}_cmcc2km_tn.nc $path_output/psl/psl_historical_${year}_cmcc2km_tn.nc

        cdo -chname,TD_2M,tdew -setattribute,TD_2M@units="C" $path_output/tdew/provaTdew.nc $path_output/tdew/tdew_historical_${year}_cmcc2km_tn.nc
	rm $path_output/tdew/provaTdew.nc

done

#RCP4.5
for year in {2006..2070} #2005
do
	echo "$year"

        cdo -addc,-273.15 -daymean $path_input/tdew/tdew_rcp45_${year}_cmcc2km_tn.nc $path_output/tdew/provaTdew.nc
        cdo daymean $path_input/psl/psl_rcp45_${year}_cmcc2km_tn.nc $path_output/psl/psl_rcp45_${year}_cmcc2km_tn.nc

	cdo -chname,TD_2M,tdew -setattribute,TD_2M@units="C" $path_output/tdew/provaTdew.nc $path_output/tdew/tdew_rcp45_${year}_cmcc2km_tn.nc
        rm $path_output/tdew/provaTdew.nc

done

#RCP8.5
for year in {2006..2070} #2005
do
        echo "$year"

        cdo -addc,-273.15 -daymean $path_input/tdew/tdew_rcp85_${year}_cmcc2km_tn.nc $path_output/tdew/provaTdew.nc
        cdo daymean $path_input/psl/psl_rcp85_${year}_cmcc2km_tn.nc $path_output/psl/psl_rcp85_${year}_cmcc2km_tn.nc
       
        cdo -chname,TD_2M,tdew -setattribute,TD_2M@units="C" $path_output/tdew/provaTdew.nc $path_output/tdew/tdew_rcp85_${year}_cmcc2km_tn.nc
        rm $path_output/tdew/provaTdew.nc

done

