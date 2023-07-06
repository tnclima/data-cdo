# copy and add vertices

library(ncdf4)
source("R/functions/calc_vertices.R")
library(magrittr)

fs::file_copy("/home/climatedata/obs/regrid_highlander/template/template.nc",
              "/home/climatedata/obs/regrid_highlander/template/template_vertices.nc", 
              overwrite = T)

nc_hl <- nc_open("/home/climatedata/obs/regrid_highlander/template/template_vertices.nc", write = T)
# for cleaner printing
ncatt_get(nc_hl, 0)
ncatt_put(nc_hl, 0, "history", "")

mat_lat <- ncvar_get(nc_hl, "lat")
mat_lon <- ncvar_get(nc_hl, "lon")
l_vert <- calc_vertices(mat_lon, mat_lat)

ncatt_get(nc_hl, "lat")
ncatt_put(nc_hl, "lat", "bounds", "lat_vertices")
ncatt_put(nc_hl, "lon", "bounds", "lon_vertices")

dim_x <- ncdim_def("rlon", units = "", vals = 1:length(ncvar_get(nc_hl, "rlon")),  create_dimvar = F)
dim_y <- ncdim_def("rlat", units = "", vals = 1:length(ncvar_get(nc_hl, "rlat")),  create_dimvar = F)
dim_vert <- ncdim_def("vertices", units = "", vals = 1:4,  create_dimvar = F)

l_vert$lat %>% dim
# var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_x, dim_y, dim_vert))
# arr_lat_vert <- aperm(l_vert$lat, c(2, 3, 1))
# var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_y, dim_x))
# arr_lat_vert <- aperm(l_vert$lat, c(1, 3, 2))
var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_x, dim_y))
arr_lat_vert <- aperm(l_vert$lat, c(1, 2, 3))
nc_hl2 <- ncvar_add(nc_hl, var_lat_vert)
ncvar_put(nc_hl2, var_lat_vert, arr_lat_vert)

l_vert$lon %>% dim
# var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_x, dim_y, dim_vert))
# arr_lon_vert <- aperm(l_vert$lon, c(2, 3, 1))
# var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_y, dim_x))
# arr_lon_vert <- aperm(l_vert$lon, c(1, 3, 2))
var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_x, dim_y))
arr_lon_vert <- aperm(l_vert$lon, c(1, 2, 3))

nc_hl3 <- ncvar_add(nc_hl2, var_lon_vert)
ncvar_put(nc_hl3, var_lon_vert, arr_lon_vert)

nc_close(nc_hl3)


