# interpolate/regridd cdo 
import os
import glob
from cdo import Cdo

cdo = Cdo()

cdo.env = {"REMAP_AREA_MIN" : "0.95"}
file_template = "/home/climatedata/downscaling/rcm_lonlat_tnaa/orog/orog_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r0i0p0_CLMcom-CCLM4-8-17_v1_fx.nc"




file_input = "/home/climatedata/obs/CRESPI/daily_1km_lonlat/DailySeries_1980_2020_MaxTemp.nc"
file_output = "/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/tasmax_crespi.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

file_input = "/home/climatedata/obs/CRESPI/daily_1km_lonlat/DailySeries_1980_2020_MinTemp.nc"
file_output = "/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/tasmin_crespi.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

file_input = "/home/climatedata/obs/CRESPI/daily_1km_lonlat/DailySeries_1980_2020_Prec.nc"
file_output = "/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/pr_crespi.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

file_input = "/home/climatedata/obs/orography/crespi_lonlat_1km_precipitation.nc"
file_output = "/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/orog_crespi_precipitation.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

file_input = "/home/climatedata/obs/orography/crespi_lonlat_1km_temperature.nc"
file_output = "/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/orog_crespi_temperature.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

