# interpolate/regridd cdo or iris
import os
import glob
from cdo import Cdo

cdo = Cdo()

cdo.env = {"REMAP_AREA_MIN" : "0.95"}
file_template = "/home/climatedata/obs/regrid_data_0.95/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc"


for vv in ["pr", "tas", "tasmin", "tasmax"]:
  # remap annual
  files_input = glob.glob(os.path.join("/home/climatedata/obs/METEOFRANCE/01-lonlat/", vv, "*"))
  path_out = os.path.join("/home/climatedata/obs/METEOFRANCE/99-tmp/", vv)
  os.makedirs(path_out, exist_ok=True)
  for file_in in files_input: 
    file_out = os.path.join(path_out, os.path.basename(file_in))
    cdo.remapcon(file_template, input=file_in, output=file_out)

  # merge
  files_in = glob.glob(os.path.join(path_out, "*"))
  file_out = os.path.join("/home/climatedata/obs/regrid_data_0.95/METEOFRANCE/", vv+"_rg.nc")
  cdo.mergetime(input=files_in, output=file_out)


# clean up manually!
