# copy and add vertices

library(ncdf4)
source("R/functions/calc_vertices.R")


fs::file_copy("/home/climatedata/obs/MESAN/tas_GAR-05_SMHI-HIRLAM_RegRean_v1d1-v1d2_SMHI-MESAN_v1_day_1989-2010.nc",
              "/home/climatedata/obs/MESAN/tas_GAR-05_SMHI-HIRLAM_RegRean_v1d1-v1d2_SMHI-MESAN_v1_day_1989-2010_vertices.nc", 
              overwrite = T)

nc_mesan <- nc_open("/home/climatedata/obs/MESAN/tas_GAR-05_SMHI-HIRLAM_RegRean_v1d1-v1d2_SMHI-MESAN_v1_day_1989-2010_vertices.nc", write = T)
# for cleaner printing (clear history)
ncatt_get(nc_mesan, 0)
ncatt_put(nc_mesan, 0, "history", "")

nc_mesan

mat_lat <- ncvar_get(nc_mesan, "lat")
mat_lon <- ncvar_get(nc_mesan, "lon")
l_vert <- calc_vertices(mat_lon, mat_lat)

ncatt_get(nc_mesan, "lat")
ncatt_put(nc_mesan, "lat", "bounds", "lat_vertices")
ncatt_put(nc_mesan, "lon", "bounds", "lon_vertices")

dim_x <- ncdim_def("rlon", units = "", vals = 1:length(ncvar_get(nc_mesan, "rlon")),  create_dimvar = F)
dim_y <- ncdim_def("rlat", units = "", vals = 1:length(ncvar_get(nc_mesan, "rlat")),  create_dimvar = F)
dim_vert <- ncdim_def("vertices", units = "", vals = 1:4,  create_dimvar = F)

l_vert$lat %>% dim
# var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_x, dim_y, dim_vert))
# arr_lat_vert <- aperm(l_vert$lat, c(2, 3, 1))
# var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_y, dim_x))
# arr_lat_vert <- aperm(l_vert$lat, c(1, 3, 2))
var_lat_vert <- ncvar_def("lat_vertices", "degrees_north", dim = list(dim_vert, dim_x, dim_y))
arr_lat_vert <- aperm(l_vert$lat, c(1, 2, 3))
nc_mesan2 <- ncvar_add(nc_mesan, var_lat_vert)
ncvar_put(nc_mesan2, var_lat_vert, arr_lat_vert)

l_vert$lon %>% dim
# var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_x, dim_y, dim_vert))
# arr_lon_vert <- aperm(l_vert$lon, c(2, 3, 1))
# var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_y, dim_x))
# arr_lon_vert <- aperm(l_vert$lon, c(1, 3, 2))
var_lon_vert <- ncvar_def("lon_vertices", "degrees_east", dim = list(dim_vert, dim_x, dim_y))
arr_lon_vert <- aperm(l_vert$lon, c(1, 2, 3))

nc_mesan3 <- ncvar_add(nc_mesan2, var_lon_vert)
ncvar_put(nc_mesan3, var_lon_vert, arr_lon_vert)

nc_close(nc_mesan3)


