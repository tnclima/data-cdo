# reproject alice dataset for use with cdo

library(terra)
library(lubridate)
library(RNetCDF)


# clim - temp -------------------------------------------------------------

fn_in <- "/home/climatedata/obs/CRESPI/daily_250m/Climatologies_1981_2010_MonthlyMeanTemp.nc"
fn_out <- "/home/climatedata/obs/CRESPI/daily_250m_lonlat/Climatologies_1981_2010_MonthlyMeanTemp.nc"

rr <- rast(fn_in)

rr_lonlat <- project(rr, "EPSG:4326")
# rr_lonlat %>% plot
time(rr_lonlat)
time(rr_lonlat) <- ymd("1990-01-15") + months(0:11)

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


# clim - prec -------------------------------------------------------------

fn_in <- "/home/climatedata/obs/CRESPI/daily_250m/Climatologies_1981_2010_MonthlyTotPrec.nc"
fn_out <- "/home/climatedata/obs/CRESPI/daily_250m_lonlat/Climatologies_1981_2010_MonthlyTotPrec.nc"

rr <- rast(fn_in)

rr_lonlat <- project(rr, "EPSG:4326")
# rr_lonlat %>% plot
time(rr_lonlat)
time(rr_lonlat) <- ymd("1990-01-15") + months(0:11)

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

