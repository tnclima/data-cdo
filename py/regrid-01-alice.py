# interpolate/regridd cdo or iris
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_template = "/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc"

# clim - temp

file_input = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/Climatologies_1981_2010_MonthlyMeanTemp.nc"
file_output = "/home/climatedata/obs/regrid_data/CRESPI/daily_250m/Climatologies_1981_2010_MonthlyMeanTemp_rg.nc"

cdo.remapbil(file_template, input=file_input, output=file_output)

# clim - prec

file_input = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/Climatologies_1981_2010_MonthlyTotPrec.nc"
file_output = "/home/climatedata/obs/regrid_data/CRESPI/daily_250m/Climatologies_1981_2010_MonthlyTotPrec_rg.nc"

cdo.remapcon(file_template, input=file_input, output=file_output)



# split year for daily series

file_input = "/home/climatedata/obs/CRESPI/daily_250m/DailySeries_1980_2018_Prec.nc"
file_output = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/prec/daily_year_"
cdo.splityearmon(input=file_input, output=file_output)

file_input = "/home/climatedata/obs/CRESPI/daily_250m/DailySeries_1980_2018_MeanTemp.nc"
file_output = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/temp/daily_year_"
cdo.splityearmon(input=file_input, output=file_output)



# project with terra (separate file)

# merge back

file_input = glob.glob("/home/climatedata/obs/CRESPI/daily_250m_lonlat/prec-ll/daily_year_*")
file_output = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/DailySeries_1980_2018_Prec.nc"
cdo.mergetime(input=file_input, output=file_output)

file_input = glob.glob("/home/climatedata/obs/CRESPI/daily_250m_lonlat/temp-ll/daily_year_*")
file_output = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/DailySeries_1980_2018_MeanTemp.nc"
cdo.mergetime(input=file_input, output=file_output)


# remap

file_input = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/DailySeries_1980_2018_Prec.nc"
file_output = "/home/climatedata/obs/regrid_data/CRESPI/daily_250m/DailySeries_1980_2018_Prec_rg.nc"
cdo.remapbil(file_template, input=file_input, output=file_output)


file_input = "/home/climatedata/obs/CRESPI/daily_250m_lonlat/DailySeries_1980_2018_MeanTemp.nc"
file_output = "/home/climatedata/obs/regrid_data/CRESPI/daily_250m/DailySeries_1980_2018_MeanTemp_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

