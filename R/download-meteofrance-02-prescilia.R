
library(curl)

path_out <- "/home/climatedata/obs/METEOFRANCE/PRESCILIA/"
fs::dir_create(path_out)
all_years <- 1958:2018
baseurl <- "https://climatedata.umr-cnrm.fr/public/dcsc/projects/PRESCILIA/"



for(i_year in all_years){
  
  file_i <- paste0("PRESCILIA_", i_year, ".nc")
  # download.file(
  #   paste0(baseurl, file_i),
  #   fs::path(path_out, file_i)
  # )
  
  curl_download(paste0(baseurl, file_i), 
                fs::path(path_out, file_i))
  
}