# generate coords file for CDO to remap rotatedpole to regular latlon

# taken from topoCLIM
# write remapbil config file
# remapping is done to grid centres thats why we add half a gridbox (res/2)



# get information from nc file --------------------------------------------

library(ncdf4)
library(magrittr)

# resolution
nc_obj <- nc_open("/home/climatedata/highlander/Daily/rcp45_1989-2070_tas.nc")
ncvar_get(nc_obj, "rlon") %>% diff %>% round(3) %>% table
ncvar_get(nc_obj, "rlat") %>% diff %>% round(3) %>% table
# -> res: 0.02
res <- 0.02
buffer <- 2*res

# extent (take interior only)
mat_lat <- ncvar_get(nc_obj, "lat")
mat_lon <- ncvar_get(nc_obj, "lon")
nc_close(nc_obj)

latS <- mat_lat %>% apply(1, min) %>% max
latN <- mat_lat %>% apply(1, max) %>% min
lonW <- mat_lon %>% apply(2, min) %>% max
lonE <- mat_lon %>% apply(2, max) %>% min


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
cat(file_content, file = "/home/climatedata/highlander/Daily_lonlat/coords_lonlat_same_xy.txt")

