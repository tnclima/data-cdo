# generate coords file for CDO to remap rotatedpole to regular latlon
# variable xy resolution: better match initial dimension


# taken from topoCLIM
# write remapbil config file
# remapping is done to grid centres thats why we add half a gridbox (res/2)

# buffer (potentially useful if cropping)
buffer <- 0


# get information from nc file --------------------------------------------

library(ncdf4)
library(magrittr)

# resolution
nc_obj <- nc_open("/home/climatedata/temp-cmcc-dds/vhr-pro/huss/huss_historical_1981_cmcc2km_tn.nc")
ncvar_get(nc_obj, "rlon") %>% diff %>% round(3) %>% table
ncvar_get(nc_obj, "rlat") %>% diff %>% round(3) %>% table
# -> res: 0.02
res <- 0.02
# buffer <- 2*res

# extent (take interior only)
mat_lat <- ncvar_get(nc_obj, "lat")
mat_lon <- ncvar_get(nc_obj, "lon")
nc_close(nc_obj)

latS <- mat_lat %>% apply(1, min) %>% max
latN <- mat_lat %>% apply(1, max) %>% min
lonW <- mat_lon %>% apply(2, min) %>% max
lonE <- mat_lon %>% apply(2, max) %>% min


# same-xy 0.02 ------------------------------------------------------------


file_content <- paste0(
  "gridtype = lonlat\n",
  "xsize = ", round((lonE - lonW + 2*buffer) / res), "\n",
  "ysize = ", round((latN - latS + 2*buffer) / res), "\n",
  "xfirst = ", (lonW - buffer + res / 2), "\n",
  "xinc = ", res, "\n",
  "yfirst = ", (latS - buffer + res / 2), "\n",
  "yinc = ", res, "\n"
)
cat(file_content)
cat(file_content, file = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_orario/coords_lonlat_same_xy_0.02.txt")



# var-xy 0.029 0.02 ------------------------------------------------------------


# resolution (different for x and y)
mat_lat %>% apply(1, diff) %>% as.vector %>% summary # -> y 0.02 ok
res_y <- 0.02

mat_lon %>% apply(2, diff) %>% as.vector %>% summary # -> between 0.0284 and 0.2911
# mat_lon %>% apply(2, diff) %>% as.vector %>% hist(50) # -> between 0.0284 and 0.2911
res_x <- mat_lon %>% apply(2, diff) %>% as.vector %>% mean %>% round(3)


file_content <- paste0(
  "gridtype = lonlat\n",
  "xsize = ", round((lonE - lonW + 2*buffer) / res_x), "\n",
  "ysize = ", round((latN - latS + 2*buffer) / res_y), "\n",
  "xfirst = ", (lonW - buffer + res_x / 2), "\n",
  "xinc = ", res_x, "\n",
  "yfirst = ", (latS - buffer + res_y / 2), "\n",
  "yinc = ", res_y, "\n"
)
cat(file_content)
cat(file_content, file = "/home/climatedata/climate_scenarios_appa/dati_spaziotemporali/vhr-pro-it-2km_orario/coords_lonlat_var_x0.029_y0.02.txt")

