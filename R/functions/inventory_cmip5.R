inventory_cmip5 <- function(path, add_files = TRUE){
  
  all_files_fullpath <- fs::dir_ls(path,
                                   regexp = "[.]nc$",
                                   recurse = TRUE)
  
  all_files_base <- fs::path_file(all_files_fullpath)
  
  # create info data
  data.table(fn = fs::path_ext_remove(all_files_base)) %>%
    .[, tstrsplit(fn, "_")] -> dat_info
  
  # add period column (V9), if it does not exist, as e.g. for OROG
  # if(! "V9" %in% names(dat_info)){
  #   dat_info[, V9 := NA_character_]
  # }
  
  setnames(dat_info,
           old = paste0("V", 1:6),
           new = c("variable", "timefreq", "gcm", "experiment","ensemble", "period"))
  
  # check for errors in period encoding
  # dat_info[period == ensemble, period := NA]
  
  # add file
  dat_info[, file_fullpath := all_files_fullpath]
  
  # prep dates
  dat_info[, c("date_start", "date_end") := tstrsplit(period, "-")]
  dat_info[, date_start := ymd(date_start, truncated = 1 )]
  dat_info[, date_end := ymd(date_end, truncated = 1)]
  
  # helper fun to check for complete contiguous period
  f_date_complete_month <- function(date_start, date_end){
    
    if(all(is.na(date_start))) return(NA)
    # if(length(date_start) == 1) return(TRUE)
    
    # 360 calendar adjustment
    # lgl_check <- month(date_end) == 12 & day(date_end) == 30
    # day(date_end[lgl_check]) <- 31
    
    mapply(seq, date_start, date_end, by = "month") %>%
      unlist %>%
      # do.call(c, .) %>% 
      sort %>%
      unique %>%
      diff %>%
      is_weakly_less_than(31) %>%
      all
    
  }
  
  f_sim_years <- function(date_start, date_end){
    
    if(all(is.na(date_start))) return(NA_integer_)
    
    mapply(seq, year(date_start), year(date_end), SIMPLIFY = FALSE) %>%
      unlist %>%
      unique %>%
      length
    
  }
  
  
  # get unique models
  dat_info_summary <- dat_info[,
                               .(nn_files = .N,
                                 date_start = min(date_start),
                                 date_end = max(date_end),
                                 total_simulation_years = f_sim_years(date_start, date_end),
                                 period_contiguous = f_date_complete_month(date_start, date_end),
                                 list_files = list(file_fullpath)),
                               keyby = .(variable, timefreq, gcm, experiment, ensemble)]
  
  # remove files if not requested
  if(!add_files) dat_info_summary[, list_files := NULL]
  
  # make a class to define specific print options
  # setattr(dat_info_summary, "class", c("eurocordexr_inv", class(dat_info_summary)))
  
  return(dat_info_summary)
}

