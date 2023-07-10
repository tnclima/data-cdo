# mergetime cmip5 daily and crop to europe

# library(eurocordexr)
library(data.table)
setDTthreads(4)
library(fs)
library(magrittr)
library(lubridate)

source("R/functions/inventory_cmip5.R")

# path_in <- "/home/climatedata/cmip5/eurocordex-ensemble-daily/split/"
# path_out <- "/home/climatedata/cmip5/eurocordex-ensemble-daily/merged-europe/"

path_in <- "/home/climatedata/cmip5/cmcc-cm-daily/split/"
path_out <- "/home/climatedata/cmip5/cmcc-cm-daily/merged-europe/"

dat_inv <- inventory_cmip5(path_in, T)

dat_inv$variable %>% table
# dat_inv <- dat_inv[variable != "orog"]

dat_inv$gcm %>% table
dat_inv$gcm %>% table %>% length
dat_inv$experiment %>% table
dat_inv %>% with(table(experiment, gcm))

dat_inv[period_contiguous == F]

with(dat_inv, table(experiment, date_start))
with(dat_inv, table(experiment, date_end))
dat_inv$total_simulation_years %>% table

dat_inv[, period := paste0(format(date_start, "%Y%m%d"), "-", format(date_end, "%Y%m%d"))]
# dat_inv[, period := paste0(format(date_start, "%Y%m"), "-", format(date_end, "%Y%m"))]
dat_inv$period %>% table

for(i in 1:nrow(dat_inv)){
  
  dat_i <- dat_inv[i]
  file_out <- path(path_out, 
                   dat_i$variable,
                   dat_i[, paste(variable, timefreq, gcm, experiment, ensemble, period,
                                 sep = "_")],
                   ext = "nc")
  
  if(file_exists(file_out)) next
  
  dir_create(path_dir(file_out))
  
  files_in <- dat_i$list_files[[1]]

  # test cropping
  # sellonlatbox,lon1,lon2,lat1,lat2  infile outfile  
  # cdo_call <- paste0("cdo sellonlatbox,330,50,20,75 ",
  #                    files_in[1], " ",
  #                    file_out)
  
  cdo_call <- paste0("cdo mergetime ",
                     paste0("-sellonlatbox,330,50,20,75 ", files_in, collapse = " "), " ",
                     file_out)
  system(cdo_call)

  
}
