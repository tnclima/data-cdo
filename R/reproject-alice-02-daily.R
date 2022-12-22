# reproject alice dataset for use with cdo

library(terra)
library(lubridate)
library(RNetCDF)
library(fs)
library(magrittr)

# daily - prec -------------------------------------------------------------

path_in <- "/home/climatedata/obs/CRESPI/daily_250m_lonlat/prec/"
path_out <- "/home/climatedata/obs/CRESPI/daily_250m_lonlat/prec-ll/"


files_in <- dir_ls(path_in)

for(i in seq_along(files_in)){
  
  fn_in <- files_in[i]
  fn_out <- path(path_out, path_file(fn_in))
  
  rr <- rast(fn_in)
  
  rr_lonlat <- project(rr, "EPSG:4326")
  # plot(rr_lonlat)
  # time(rr_lonlat)
  fn_in %>% 
    path_file() %>% 
    path_ext_remove() %>% 
    stringr::str_remove("daily_year_") %>% 
    paste0("01") %>% 
    ymd() -> date_start
  
  time(rr_lonlat) <- date_start + days(0:(nlyr(rr) - 1))
  
  # names(rr_lonlat)
  
  writeCDF(rr_lonlat,
           filename = fn_out, 
           varname = "precipitation", unit = "mm", overwrite = TRUE)
  
  
  # clean attributes
  
  ncobj <- open.nc(fn_out, write = T)
  # att.get.nc(ncobj, "time", "calendar")
  att.get.nc(ncobj, "precipitation", "grid_mapping")
  att.delete.nc(ncobj, "precipitation", "grid_mapping")
  close.nc(ncobj)
  
  
}



# daily - temp ------------------------------------------------------------



path_in <- "/home/climatedata/obs/CRESPI/daily_250m_lonlat/temp/"
path_out <- "/home/climatedata/obs/CRESPI/daily_250m_lonlat/temp-ll/"


files_in <- dir_ls(path_in)

for(i in seq_along(files_in)){
  
  fn_in <- files_in[i]
  fn_out <- path(path_out, path_file(fn_in))
  
  rr <- rast(fn_in)
  
  rr_lonlat <- project(rr, "EPSG:4326")
  # plot(rr_lonlat[[1]])
  # time(rr_lonlat)
  fn_in %>% 
    path_file() %>% 
    path_ext_remove() %>% 
    stringr::str_remove("daily_year_") %>% 
    paste0("01") %>% 
    ymd() -> date_start
  
  time(rr_lonlat) <- date_start + days(0:(nlyr(rr) - 1))
  
  # names(rr_lonlat)
  
  writeCDF(rr_lonlat,
           filename = fn_out, 
           varname = "temperature", unit = "C", overwrite = TRUE)
  
  
  # clean attributes
  
  ncobj <- open.nc(fn_out, write = T)
  # att.get.nc(ncobj, "time", "calendar")
  att.get.nc(ncobj, "temperature", "grid_mapping")
  att.delete.nc(ncobj, "temperature", "grid_mapping")
  close.nc(ncobj)
  
  
}


