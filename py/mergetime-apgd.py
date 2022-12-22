# interpolate/regridd cdo or iris
import os
import glob
from cdo import Cdo

cdo = Cdo()


file_input = glob.glob("/home/climatedata/obs/APGD/raw/**/Rapd*.nc", recursive=True)
file_output = "/home/climatedata/obs/APGD/APGD_laea.nc"
cdo.mergetime(input=file_input, output=file_output)


