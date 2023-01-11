# mergetime eurocordex

library(eurocordexr)
library(fs)
library(magrittr)
library(lubridate)

path_in <- "/home/climatedata/eurocordex/"
path_out <- "/home/climatedata/eurocordex-merged/"

dat_inv <- get_inventory(path_in, T)
dat_inv$variable %>% table
dat_inv <- dat_inv[variable != "orog"]

for(i in 1:nrow(dat_inv)){
  
  dat_i <- dat_inv[i]
  file_out <- path(path_out, 
                   dat_i$variable,
                   dat_i[, paste(variable, domain, gcm, experiment, ensemble, institute_rcm,
                                 downscale_realisation, timefreq, date_start, date_end,
                                 sep = "_")],
                   ext = "nc")
  
  dir_create(path_dir(file_out))
  
  files_in <- dat_i$list_files[[1]]
  
  cdo_call <- paste0("cdo mergetime ",
                     paste0(files_in, collapse = " "), " ",
                     file_out)
  
  system(cdo_call)
  
  
}