# use remapcon to crop remo2009 because of gridcell issues (center/corner)

import os
import glob
from cdo import Cdo

cdo = Cdo()

file_template = "/home/climatedata/obs/regrid_data/template_rotpole_eurocordex/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19500101-19501231.nc"

path_in = "/home/climatedata/eurocordex-temp/prAdjust/"
path_out = "/home/climatedata/eurocordex-temp2/prAdjust/"

os.makedirs(path_out, exist_ok=True)

all_files = glob.glob(path_in + "*.nc")
all_files.sort()

for file_in in all_files:
  file_out = os.path.join(path_out, os.path.basename(file_in))
  cdo.remapcon(file_template, input=file_in, output=file_out)




