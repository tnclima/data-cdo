# interpolate/regridd cdo 
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_template = "/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc"

# to convert tif to netcdf: use gdal in shell
# gdal_translate -of NetCDF infile outfile

# apgd ----------------------------------------- #

# setgrid first (and remove the added time dimension)
file_input = "/home/climatedata/obs/orography/apgd_height.nc"
file_output = "/home/climatedata/obs/orography/apgd_height_setgrid.nc"
cdo.setgrid("/home/climatedata/obs/APGD/APGD_laea_vertices.nc",
            input=file_input, output=file_output)

file_input = "/home/climatedata/obs/orography/apgd_height_setgrid.nc"
file_output = "/home/climatedata/obs/orography/apgd_height_setgrid_notime.nc"
cdo.copy(options="--reduce_dim",
         input=file_input, output=file_output)

file_input = "/home/climatedata/obs/orography/apgd_height_setgrid_notime.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/apgd_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

# crespi ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/crespi_1km_precipitation.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/crespi_1km_precipitation_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

file_input = "/home/climatedata/obs/orography/crespi_1km_temperature.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/crespi_1km_temperature_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)


# eobs ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/eobs_elev_0.1deg_reg_v26.0e.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/eobs_elev_0.1deg_reg_v26.0e_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

# eu-dem ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/eu_dem_gar_1km.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/eu_dem_gar_1km_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)





# histalp ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/histalp_elevation_temperature.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/histalp_elevation_temperature_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)


# laprec ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/laprec_dem.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/laprec_dem_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)



# mesan ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/MESAN_GAR_orography_vertices.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/MESAN_GAR_orography_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)



# swiss ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/topo.swiss02_ch02.lonlat.nc"
file_output = "/home/climatedata/obs/regrid_data/orography/topo.swiss02_ch02.lonlat_rg.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)




