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

	#Precipitation
	cdo daysum $path_input/pr/pr_historical_${year}_cmcc2km_tn.nc $path_output/pr/provaP.nc
	
	#Temperature
	cdo -addc,-273.15 -daymean $path_input/tas/tas_historical_${year}_cmcc2km_tn.nc $path_output/tas/provaT.nc
        cdo -addc,-273.15 -daymax $path_input/tas/tas_historical_${year}_cmcc2km_tn.nc $path_output/tasmax/provaTx.nc
        cdo -addc,-273.15 -daymin $path_input/tas/tas_historical_${year}_cmcc2km_tn.nc $path_output/tasmin/provaTn.nc
	
	#Creation of the data:
	#Precipitation
        cdo -chname,TOT_PREC,pr -setattribute,TOT_PREC@units="mm" $path_output/pr/provaP.nc $path_output/pr/pr_historical_${year}_cmcc2km_tn.nc
	rm $path_output/pr/provaP.nc
		
	#Temperature
	cdo chname,T_2M,tas -setattribute,T_2M@units="C" $path_output/tas/provaT.nc $path_output/tas/tas_historical_${year}_cmcc2km_tn.nc
	cdo chname,T_2M,tasmax -setattribute,T_2M@units="C" $path_output/tasmax/provaTx.nc $path_output/tasmax/tasmax_historical_${year}_cmcc2km_tn.nc
	cdo chname,T_2M,tasmin -setattribute,T_2M@units="C" $path_output/tasmin/provaTn.nc $path_output/tasmin/tasmin_historical_${year}_cmcc2km_tn.nc
	
	rm $path_output/tas/provaT.nc
	rm $path_output/tasmin/provaTn.nc
	rm $path_output/tasmax/provaTx.nc
done

#RCP4.5
for year in {2006..2070} #2005
do
	echo "$year"

	#Precipitation
        cdo daysum $path_input/pr/pr_rcp45_${year}_cmcc2km_tn.nc $path_output/pr/provaP.nc

        #Temperature
        cdo -addc,-273.15 -daymean $path_input/tas/tas_rcp45_${year}_cmcc2km_tn.nc $path_output/tas/provaT.nc
        cdo -addc,-273.15 -daymax $path_input/tas/tas_rcp45_${year}_cmcc2km_tn.nc $path_output/tasmax/provaTx.nc
        cdo -addc,-273.15 -daymin $path_input/tas/tas_rcp45_${year}_cmcc2km_tn.nc $path_output/tasmin/provaTn.nc

        #Creation of the data:
        #Precipitation
        cdo -chname,TOT_PREC,pr -setattribute,TOT_PREC@units="mm" $path_output/pr/provaP.nc $path_output/pr/pr_rcp45_${year}_cmcc2km_tn.nc
        rm $path_output/pr/provaP.nc

        #Temperature
        cdo chname,T_2M,tas -setattribute,T_2M@units="C" $path_output/tas/provaT.nc $path_output/tas/tas_rcp45_${year}_cmcc2km_tn.nc
        cdo chname,T_2M,tasmax -setattribute,T_2M@units="C" $path_output/tasmax/provaTx.nc $path_output/tasmax/tasmax_rcp45_${year}_cmcc2km_tn.nc
        cdo chname,T_2M,tasmin -setattribute,T_2M@units="C" $path_output/tasmin/provaTn.nc $path_output/tasmin/tasmin_rcp45_${year}_cmcc2km_tn.nc

        rm $path_output/tas/provaT.nc
        rm $path_output/tasmin/provaTn.nc
        rm $path_output/tasmax/provaTx.nc
done

#RCP8.5
for year in {2006..2070} #2005
do
        echo "$year"

        #Precipitation
        cdo daysum $path_input/pr/pr_rcp85_${year}_cmcc2km_tn.nc $path_output/pr/provaP.nc

        #Temperature
        cdo -addc,-273.15 -daymean $path_input/tas/tas_rcp85_${year}_cmcc2km_tn.nc $path_output/tas/provaT.nc
        cdo -addc,-273.15 -daymax $path_input/tas/tas_rcp85_${year}_cmcc2km_tn.nc $path_output/tasmax/provaTx.nc
        cdo -addc,-273.15 -daymin $path_input/tas/tas_rcp85_${year}_cmcc2km_tn.nc $path_output/tasmin/provaTn.nc

        #Creation of the data:
        #Precipitation
        cdo -chname,TOT_PREC,pr -setattribute,TOT_PREC@units="mm" $path_output/pr/provaP.nc $path_output/pr/pr_rcp85_${year}_cmcc2km_tn.nc
        rm $path_output/pr/provaP.nc

        #Temperature
        cdo chname,T_2M,tas -setattribute,T_2M@units="C" $path_output/tas/provaT.nc $path_output/tas/tas_rcp85_${year}_cmcc2km_tn.nc
        cdo chname,T_2M,tasmax -setattribute,T_2M@units="C" $path_output/tasmax/provaTx.nc $path_output/tasmax/tasmax_rcp85_${year}_cmcc2km_tn.nc
        cdo chname,T_2M,tasmin -setattribute,T_2M@units="C" $path_output/tasmin/provaTn.nc $path_output/tasmin/tasmin_rcp85_${year}_cmcc2km_tn.nc

        rm $path_output/tas/provaT.nc
        rm $path_output/tasmin/provaTn.nc
        rm $path_output/tasmax/provaTx.nc
done

