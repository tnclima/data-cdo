########################################################################
# This script calculates the daily precipitation from hourly highlander
# dataset

# 8 June, 2023   Anna Napoli
########################################################################
path_output='/home/climatedata/highlander/Daily/RCP85'
path_input='/home/climatedata/highlander/rcp85_2006-2070'
##########################################################################
CDO_RESET_HISTORY=1 ;
export CDO_RESET_HISTORY
export REMAP_AREA_MIN=0.95

# Now the loop starts:
count=0
for year in {2045..2070} #2005
do
        for month in {1..12} #12 #`seq -w 8 12`  #01 02 03 04 05 06 07 08 09 10 11 12
        do
		var_mon=$(printf %02d $month)
		
		#Precipitation
	#	cdo daysum $path_input/precipitation/climate-projections-downscaled-over-italy-hourly-precipitation_amount-${year}-${var_mon}_GAR.nc $path_output/provaP.nc

		#Temperature
	#	cdo -addc,-273.15 -daymean $path_input/temperature/climate-projections-downscaled-over-italy-hourly-air_temperature-${year}-${var_mon}_GAR.nc $path_output/provaT.nc
        #       cdo -addc,-273.15 -daymax $path_input/temperature/climate-projections-downscaled-over-italy-hourly-air_temperature-${year}-${var_mon}_GAR.nc $path_output/provaTx.nc
                cdo -addc,-273.15 -daymin $path_input/temperature/climate-projections-downscaled-over-italy-hourly-air_temperature-${year}-${var_mon}_GAR.nc $path_output/provaTm.nc

		#Creation of the data:
		#Precipitation
        #        cdo -chname,TOT_PREC,pr -setattribute,TOT_PREC@units="mm" $path_output/provaP.nc $path_output/rcp85_pr_${year}_${var_mon}.nc
	#	rm $path_output/provaP.nc
		
		#Temperature
	#	cdo chname,T_2M,tas -setattribute,T_2M@units="C" $path_output/provaT.nc $path_output/rcp85_tas_${year}_${var_mon}.nc
        #        cdo chname,T_2M,tasmax -setattribute,T_2M@units="C" $path_output/provaTx.nc $path_output/rcp85_tasmax_${year}_${var_mon}.nc
                cdo chname,T_2M,tasmin -setattribute,T_2M@units="C" $path_output/provaTm.nc $path_output/rcp85_tasmin_${year}_${var_mon}.nc

	#	rm $path_output/provaT.nc
		rm $path_output/provaTm.nc
	#	rm $path_output/provaTx.nc
	done
done

