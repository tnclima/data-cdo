# eu-dem preprocessing

library(terra)
library(sf)

# sameer ------------------------------------------------------------------


rs <- rast("/home/climatedata/dem/sameer-eu-dem.csv")
crs(rs) <- "epsg:3395"

plot(rs)




# from eea homepage -------------------------------------------------------

rs1 <- rast("/home/climatedata/dem/eu_dem_v11_E30N20/eu_dem_v11_E30N20.TIF")
rs2 <- rast("/home/climatedata/dem/eu_dem_v11_E40N20/eu_dem_v11_E40N20.TIF")
# plot(rs2)

rs <- merge(rs1, rs2, filename = "/home/climatedata/dem/eu_dem_full.tif")

# crop to GAR
rs_gar <- rast("/home/climatedata/obs/EOBS/tg_ens_mean_0.1deg_GAR_reg_v26.0e.nc", lyrs = 1)
sp_ext <- as.polygons(ext(rs_gar))
crs(sp_ext) <- crs(rs_gar)
sp_ext_laea <- project(sp_ext, rs)

rs_crop <- crop(rs, sp_ext_laea, filename = "/home/climatedata/dem/eu_dem_GAR.tif")



# resample to 1km ---------------------------------------------------------


rs_crop_1km <- aggregate(rs_crop, 40, filename = "/home/climatedata/obs/orography/eu_dem_gar_1km.tif")


