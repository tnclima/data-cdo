# copy and add vertices

library(ncdf4)
library(magrittr)
source("R/functions/calc_vertices.R")


# don't copy because too large
# fs::file_copy("/home/climatedata/obs/HYRAS/pr_hyras_1_1951-2022_v3-0_de.nc",
#               "/home/climatedata/obs/HYRAS/pr_hyras_1_1951-2022_v3-0_de_vertices.nc", 
#               overwrite = T)

all_files <- c("/home/climatedata/obs/HYRAS/tas_hyras_5_1951-2015_v4-0_de.nc",
               "/home/climatedata/obs/HYRAS/tmax_hyras_5_1951-2015_v4-0_de.nc",
               "/home/climatedata/obs/HYRAS/tmin_hyras_5_1951-2015_v4-0_de.nc")


for(i_fn in all_files){
  nc_hyras <- nc_open(i_fn, write = T)
  # for cleaner printing (clear history)
  # ncatt_get(nc_hyras, 0)
  # ncatt_put(nc_hyras, 0, "history", "")
  
  nc_hyras
  
  mat_lat <- ncvar_get(nc_hyras, "lat")
  mat_lon <- ncvar_get(nc_hyras, "lon")
  l_vert <- calc_vertices(mat_lon, mat_lat)
  
  ncatt_get(nc_hyras, "lat")
  ncatt_put(nc_hyras, "lat", "bounds", "lat_vertices")
  ncatt_put(nc_hyras, "lon", "bounds", "lon_vertices")
  
  dim_x <- ncdim_def("x", units = "", vals = 1:length(ncvar_get(nc_hyras, "x")),  create_dimvar = F)
  dim_y <- ncdim_def("y", units = "", vals = 1:length(ncvar_get(nc_hyras, "y")),  create_dimvar = F)
  dim_vert <- ncdim_def("vertices", units = "", vals = 1:4,  create_dimvar = F)
  
  l_vert$lat %>% dim
  # var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_x, dim_y, dim_vert))
  # arr_lat_vert <- aperm(l_vert$lat, c(2, 3, 1))
  # var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_y, dim_x))
  # arr_lat_vert <- aperm(l_vert$lat, c(1, 3, 2))
  var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_x, dim_y))
  arr_lat_vert <- aperm(l_vert$lat, c(1, 2, 3))
  nc_hyras2 <- ncvar_add(nc_hyras, var_lat_vert)
  ncvar_put(nc_hyras2, var_lat_vert, arr_lat_vert)
  
  l_vert$lon %>% dim
  # var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_x, dim_y, dim_vert))
  # arr_lon_vert <- aperm(l_vert$lon, c(2, 3, 1))
  # var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_y, dim_x))
  # arr_lon_vert <- aperm(l_vert$lon, c(1, 3, 2))
  var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_x, dim_y))
  arr_lon_vert <- aperm(l_vert$lon, c(1, 2, 3))
  
  nc_hyras3 <- ncvar_add(nc_hyras2, var_lon_vert)
  ncvar_put(nc_hyras3, var_lon_vert, arr_lon_vert)
  
  nc_close(nc_hyras3)
  
  
  
}
