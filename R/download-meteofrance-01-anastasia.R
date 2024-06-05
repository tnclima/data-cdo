
library(curl)

path_out <- "/home/climatedata/obs/METEOFRANCE/ANASTASIA/"
fs::dir_create(path_out)
all_years <- 1969:2021
baseurl <- "https://climatedata.umr-cnrm.fr/public/dcsc/projects/ANASTASIA/"

for(i_year in all_years){
  
  file_i <- paste0("ANASTASIA_", i_year, ".nc")
  # download.file(
  #   paste0(baseurl, file_i),
  #   fs::path(path_out, file_i)
  # )
  
  curl_download(paste0(baseurl, file_i), 
                fs::path(path_out, file_i))
  
}