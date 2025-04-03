# reproject alice dataset for use with cdo

library(terra)
library(lubridate)
library(RNetCDF)
library(fs)
library(magrittr)

# prec -------------------------------------------------------------

path_in <- "/home/climatedata/obs/ALPINE-TST/zz_split_day_prec/"
path_out_ll <- "/home/climatedata/obs/ALPINE-TST/zz_split_day_prec_lonlat/"
path_out_ll_1km <- "/home/climatedata/obs/ALPINE-TST/zz_split_day_prec_lonlat_1km/"
path_out_1km <- "/home/climatedata/obs/ALPINE-TST/zz_split_day_prec_1km/"


files_in <- dir_ls(path_in)

for(i in seq_along(files_in)){
  
  fn_in <- files_in[i]
  rr <- rast(fn_in)

  # skip
  # rr_lonlat <- project(rr, "EPSG:4326")
  # fn_out <- path(path_out_ll, path_file(fn_in))
  # writeCDF(rr_lonlat,
  #          filename = fn_out, 
  #          varname = "pr", unit = "kg m-2", overwrite = TRUE)
  # 
  # 
  # # clean attributes
  # 
  # ncobj <- open.nc(fn_out, write = T)
  # # att.get.nc(ncobj, "time", "calendar")
  # # att.get.nc(ncobj, "pr", "grid_mapping")
  # att.delete.nc(ncobj, "pr", "grid_mapping")
  # att.put.nc(ncobj, "pr", "standard_name", "NC_CHAR", "precipitation_amount")
  # close.nc(ncobj)
  
  
  # upscale to 1km
  
  rr_1km <- aggregate(rr, 4, fun = "mean")
  time(rr_1km) <- time(rr)
  
  fn_out <- path(path_out_1km, path_file(fn_in))
  writeCDF(rr_1km,
           filename = fn_out, 
           varname = "pr", unit = "kg m-2", overwrite = TRUE)
  
  
  # reproject 1km version
  
  rr_lonlat_1km <- project(rr_1km, "EPSG:4326")
  # plot(rr_lonlat[[1]])
  # time(rr_lonlat)
  # names(rr_lonlat)
  
  fn_out <- path(path_out_ll_1km, path_file(fn_in))
  writeCDF(rr_lonlat_1km,
           filename = fn_out, 
           varname = "pr", unit = "kg m-2", overwrite = TRUE)
 
  ncobj <- open.nc(fn_out, write = T)
  # att.get.nc(ncobj, "time", "calendar")
  # att.get.nc(ncobj, "pr", "grid_mapping")
  att.delete.nc(ncobj, "pr", "grid_mapping")
  att.put.nc(ncobj, "pr", "standard_name", "NC_CHAR", "precipitation_amount")
  close.nc(ncobj)
   
}


