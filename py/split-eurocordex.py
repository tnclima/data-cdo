# split eurocordex into years and seasons
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/eurocordex/merged/"
path_out = "/home/climatedata/eurocordex/data_in_time/"

all_variables = os.listdir(path_in)
all_variables.sort()
all_variables = [x for x in all_variables if x != "orog"]
all_variables = all_variables[0:4] # only a subset to start with

for i,var in enumerate(all_variables):
  rcm_files = os.listdir(os.path.join(path_in, var))
  rcm_files.sort()
  
  for j,file_rcm in enumerate(rcm_files):
    file_noext = file_rcm[:-3]
    file_info = file_noext.split("_")
    dates = file_info[-1].split("-")
    year_first = int(dates[0][0:4])
    year_last = int(dates[1][0:4])
    
    # few models have start 1949-12-01, which causes errors -> min_start 1950
    if year_first == 1949:
      year_first = 1950
    
    path_annual = os.path.join(path_out, "Annual", var, file_noext)
    os.makedirs(path_annual, exist_ok=True)
    path_seasonal = os.path.join(path_out, "Seasonal", var, file_noext)
    os.makedirs(path_seasonal, exist_ok=True)
    
    # skip rest of loop if final file exists
    if os.path.exists(os.path.join(path_seasonal, "DJF_annual_mean.nc")):
      continue
    
    for year in range(year_first, year_last + 1):

      cdo.selyear(year, 
                  input=os.path.join(path_in, var, file_rcm), 
                  output=os.path.join(path_annual, str(year) + "_daily.nc"))
      cdo.timmean(input=os.path.join(path_annual, str(year) + "_daily.nc"), 
                  output=os.path.join(path_annual, "Mean_" + str(year) + ".nc"))
      
      cdo.selmon("3,4,5",
                 input=os.path.join(path_annual, str(year) + "_daily.nc"),
                 output=os.path.join(path_seasonal, "MAM_" + str(year) + "_daily.nc"))
      cdo.timmean(input=os.path.join(path_seasonal, "MAM_" + str(year) + "_daily.nc"), 
                  output=os.path.join(path_seasonal, "MAM_Mean_" + str(year) + ".nc"))
                  
      cdo.selmon("6,7,8",
                 input=os.path.join(path_annual, str(year) + "_daily.nc"),
                 output=os.path.join(path_seasonal, "JJA_" + str(year) + "_daily.nc"))
      cdo.timmean(input=os.path.join(path_seasonal, "JJA_" + str(year) + "_daily.nc"), 
                  output=os.path.join(path_seasonal, "JJA_Mean_" + str(year) + ".nc"))
                  
      cdo.selmon("9,10,11",
                 input=os.path.join(path_annual, str(year) + "_daily.nc"),
                 output=os.path.join(path_seasonal, "SON_" + str(year) + "_daily.nc"))
      cdo.timmean(input=os.path.join(path_seasonal, "SON_" + str(year) + "_daily.nc"), 
                  output=os.path.join(path_seasonal, "SON_Mean_" + str(year) + ".nc"))
                  
      if year > year_first:
        year_prev = year - 1
        cdo.selmon("12",
                   input=os.path.join(path_annual, str(year_prev) + "_daily.nc"),
                   output=os.path.join(path_seasonal, "D_" + str(year) + "_daily.nc"))
        cdo.selmon("1,2",
                   input=os.path.join(path_annual, str(year) + "_daily.nc"),
                   output=os.path.join(path_seasonal, "JF_" + str(year) + "_daily.nc"))
        cdo.mergetime(input=[os.path.join(path_seasonal, "D_" + str(year) + "_daily.nc"),
                             os.path.join(path_seasonal, "JF_" + str(year) + "_daily.nc")],
                      output=os.path.join(path_seasonal, "DJF_" + str(year) + "_daily.nc"))
        
        cdo.timmean(input=os.path.join(path_seasonal, "DJF_" + str(year) + "_daily.nc"), 
                    output=os.path.join(path_seasonal, "DJF_Mean_" + str(year) + ".nc"))
        
        os.remove(os.path.join(path_seasonal, "D_" + str(year) + "_daily.nc"))
        os.remove(os.path.join(path_seasonal, "JF_" + str(year) + "_daily.nc"))
        
    
    

    cdo.mergetime(input=glob.glob(os.path.join(path_annual, "Mean_*")),
                  output=os.path.join(path_annual, "Annual_mean.nc"))
    cdo.mergetime(input=glob.glob(os.path.join(path_seasonal, "MAM_Mean_*")),
                  output=os.path.join(path_seasonal, "MAM_annual_mean.nc"))
    cdo.mergetime(input=glob.glob(os.path.join(path_seasonal, "JJA_Mean_*")),
                  output=os.path.join(path_seasonal, "JJA_annual_mean.nc"))
    cdo.mergetime(input=glob.glob(os.path.join(path_seasonal, "SON_Mean_*")),
                  output=os.path.join(path_seasonal, "SON_annual_mean.nc"))
    cdo.mergetime(input=glob.glob(os.path.join(path_seasonal, "DJF_Mean_*")),
                  output=os.path.join(path_seasonal, "DJF_annual_mean.nc"))
    
    
    for f in glob.glob(os.path.join(path_annual, "Mean_*")):
      os.remove(f)
    for f in glob.glob(os.path.join(path_seasonal, "MAM_Mean_*")):
      os.remove(f)
    for f in glob.glob(os.path.join(path_seasonal, "JJA_Mean_*")):
      os.remove(f)
    for f in glob.glob(os.path.join(path_seasonal, "SON_Mean_*")):
      os.remove(f)
    for f in glob.glob(os.path.join(path_seasonal, "DJF_Mean_*")):
      os.remove(f)

    
                  
