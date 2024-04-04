# copy and add vertices

library(ncdf4)
library(magrittr)
source("R/functions/calc_vertices.R")


fs::file_copy("/home/climatedata/obs/APGDv2/APGD_laea.nc",
              "/home/climatedata/obs/APGDv2/APGD_laea_vertices.nc", 
              overwrite = T)

nc_apgd <- nc_open("/home/climatedata/obs/APGDv2/APGD_laea_vertices.nc", write = T)
# for cleaner printing
ncatt_get(nc_apgd, 0)
ncatt_put(nc_apgd, 0, "history", "")

mat_lat <- ncvar_get(nc_apgd, "lat")
mat_lon <- ncvar_get(nc_apgd, "lon")
l_vert <- calc_vertices(mat_lon, mat_lat)

ncatt_get(nc_apgd, "lat")
ncatt_put(nc_apgd, "lat", "bounds", "lat_vertices")
ncatt_put(nc_apgd, "lon", "bounds", "lon_vertices")

dim_x <- ncdim_def("X", units = "", vals = 1:length(ncvar_get(nc_apgd, "X")),  create_dimvar = F)
dim_y <- ncdim_def("Y", units = "", vals = 1:length(ncvar_get(nc_apgd, "Y")),  create_dimvar = F)
dim_vert <- ncdim_def("vertices", units = "", vals = 1:4,  create_dimvar = F)

l_vert$lat %>% dim
# var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_x, dim_y, dim_vert))
# arr_lat_vert <- aperm(l_vert$lat, c(2, 3, 1))
# var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_y, dim_x))
# arr_lat_vert <- aperm(l_vert$lat, c(1, 3, 2))
var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_x, dim_y))
arr_lat_vert <- aperm(l_vert$lat, c(1, 2, 3))
nc_apgd2 <- ncvar_add(nc_apgd, var_lat_vert)
ncvar_put(nc_apgd2, var_lat_vert, arr_lat_vert)

l_vert$lon %>% dim
# var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_x, dim_y, dim_vert))
# arr_lon_vert <- aperm(l_vert$lon, c(2, 3, 1))
# var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_y, dim_x))
# arr_lon_vert <- aperm(l_vert$lon, c(1, 3, 2))
var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_x, dim_y))
arr_lon_vert <- aperm(l_vert$lon, c(1, 2, 3))

nc_apgd3 <- ncvar_add(nc_apgd2, var_lon_vert)
ncvar_put(nc_apgd3, var_lon_vert, arr_lon_vert)

nc_close(nc_apgd3)


