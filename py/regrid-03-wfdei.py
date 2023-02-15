# interpolate/regridd cdo 
import os
import glob
from cdo import Cdo

cdo = Cdo()

cdo.env = {"REMAP_AREA_MIN" : "0.95"}
file_template = "/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc"


file_input = "/home/climatedata/obs/WFDEI/pr_wfdei_1981_2010.nc4"
file_output = "/home/climatedata/obs/regrid_data/WFDEI/pr_wfdei_1981_2010_rg.nc"
cdo.remapbil(file_template, input=file_input, output=file_output)


file_input = "/home/climatedata/obs/WFDEI/tas_wfdei_1981_2010.nc4"
file_output = "/home/climatedata/obs/regrid_data/WFDEI/tas_wfdei_1981_2010_rg.nc"
cdo.remapbil(file_template, input=file_input, output=file_output)

file_input = "/home/climatedata/obs/WFDEI/tasmax_wfdei_1981_2010.nc4"
file_output = "/home/climatedata/obs/regrid_data/WFDEI/tasmax_wfdei_1981_2010_rg.nc"
cdo.remapbil(file_template, input=file_input, output=file_output)

file_input = "/home/climatedata/obs/WFDEI/tasmin_wfdei_1981_2010.nc4"
file_output = "/home/climatedata/obs/regrid_data/WFDEI/tasmin_wfdei_1981_2010_rg.nc"
cdo.remapbil(file_template, input=file_input, output=file_output)
