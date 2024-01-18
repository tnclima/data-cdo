# interpolate/regridd cdo 
import os
import glob
from cdo import Cdo

cdo = Cdo()

file_template = "/home/climatedata/downscaling/rcm_lonlat_tnaa/orog/orog_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r0i0p0_CLMcom-CCLM4-8-17_v1_fx.nc"

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
file_output = "/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/orog_apgd.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)

# eobs ----------------------------------------- #

file_input = "/home/climatedata/obs/orography/eobs_elev_0.1deg_reg_v26.0e.nc"
file_output = "/home/climatedata/downscaling/obs4rcm_lonlat_tnaa/orog_eobs.nc"
cdo.remapcon(file_template, input=file_input, output=file_output)



