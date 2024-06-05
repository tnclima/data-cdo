# reproject to lonlat from non CF-conform original grids

library(terra)
library(lubridate)
library(ncdf4)
library(RNetCDF)
library(fs)
library(magrittr)
library(stringr)

path_in <- "/home/climatedata/obs/METEOFRANCE/ANASTASIA/"
path_out <- "/home/climatedata/obs/METEOFRANCE/01-lonlat/"
path_temp <- path(path_out, "temp-daily")

files_in <- dir_ls(path_in)

all_vars <- setNames(c("TM", "TN", "TX"), c("tas", "tasmin", "tasmax"))

for(i_fn in files_in){
  
  nc1 <- nc_open(i_fn)
  
  # mat_lon <- ncvar_get(nc1, "lon")
  mat_x <- ncvar_get(nc1, "x")
  mat_y <- ncvar_get(nc1, "y")

  times <- ncdf4.helpers::nc.get.time.series(nc1, "TM") %>% ymd()
  

  
  for(i_var in seq_along(all_vars)){
    
    dir_create(path(path_out, names(all_vars)[i_var]))
    dir_create(path(path_temp, names(all_vars)[i_var]))
    
    file_out_annual <- path(path_out, names(all_vars)[i_var], year(times[1]), ext = "nc")
    if(file_exists(file_out_annual)) next
    
    for(i_date in seq_along(times)){
      
      file_out <- path(path_temp, names(all_vars)[i_var], times[i_date], ext = "nc")
      if(file_exists(file_out)) next
      
      rr_new <- rast(nrows = ncol(mat_x), ncols = nrow(mat_x), 
                     xmin = min(mat_x), xmax = max(mat_x),
                     ymin = min(mat_y), ymax = max(mat_y),
                     nlyrs = 1, time = times[i_date],
                     crs = "EPSG:27572")
      
      mat1 <- ncvar_get(nc1, all_vars[i_var], start = c(1, 1, i_date), count = c(-1, -1, 1))
      rr_new[] <- as.vector(mat1[,ncol(mat1):1])
      
      rr_new_ll <- project(rr_new, "EPSG:4326")
      
      writeCDF(rr_new_ll, 
               file_out,
               varname = names(all_vars)[i_var], unit = "degC")
      
      ncobj <- open.nc(file_out, write = T)
      # att.get.nc(ncobj, "time", "calendar")
      # att.get.nc(ncobj, names(all_vars)[i_var], "grid_mapping")
      att.delete.nc(ncobj, names(all_vars)[i_var], "grid_mapping")
      close.nc(ncobj)
      
      
    }
    
    
    files_lonlat <- dir_ls(path(path_temp, names(all_vars)[i_var]))
    
    cdo_call <- str_c("cdo --no_history mergetime ",
                      " ", str_flatten(files_lonlat, " "),
                      " ", file_out_annual)
    system(cdo_call)
    
    file_delete(files_lonlat)
    
  }
  
  
  
}



