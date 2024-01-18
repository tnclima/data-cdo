# mergetime eurocordex

library(eurocordexr)
library(data.table)
setDTthreads(4)
library(fs)
library(magrittr)
library(lubridate)

# source("R/functions/inventory_cmip5.R")

path_in <- "/home/climatedata/temp-cmip5/ec-earth-mon/"
path_out <- "/home/climatedata/cmip5/large-ensemble-monthly/merged/"

dat_inv <- get_inventory_cmip5(path_in)

dat_inv$variable %>% table
dat_inv <- dat_inv[variable != "orog"]

dat_inv$gcm %>% table
dat_inv$gcm %>% table %>% length
dat_inv$experiment %>% table
dat_inv %>% with(table(experiment, gcm))

dat_inv[period_contiguous == F]

with(dat_inv, table(experiment, date_start))
with(dat_inv, table(experiment, date_end))
dat_inv$total_simulation_years %>% table

# not all ensembles have the full century
dat_inv[year(date_end) > 2006 & year(date_end) < 2090]
dat_inv[gcm == "MIROC5"]
dat_inv[gcm == "MIROC4h"]
dat_inv[gcm == "HadCM3"]

# does not have all historical (removed manually)
dat_inv[gcm == "MIROC-ESM-CHEM"]



# dat_inv[, period := paste0(format(date_start, "%Y%m%d"), "-", format(date_end, "%Y%m%d"))]
dat_inv[, period := paste0(format(date_start, "%Y%m"), "-", format(date_end, "%Y%m"))]

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
  
  if(length(files_in) == 1) {
    fs::file_copy(files_in, file_out)
  } else {
    cdo_call <- paste0("cdo mergetime ",
                       paste0(files_in, collapse = " "), " ",
                       file_out)
    system(cdo_call)
  }

  
}
