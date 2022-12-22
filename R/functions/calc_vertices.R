# calculate vertices for netcdf cf convention from 2d-matrices of lon lat

calc_vertices <- function(mlon, mlat){
  
  x <- mlon
  y <- mlat
  
  nc <- ncol(x)
  nr <- nrow(x)
  
  tl_x <- matrix(nrow = nr, ncol = nc)
  tl_y <- matrix(nrow = nr, ncol = nc)
  bl_x <- matrix(nrow = nr, ncol = nc)
  bl_y <- matrix(nrow = nr, ncol = nc)
  tr_x <- matrix(nrow = nr, ncol = nc)
  tr_y <- matrix(nrow = nr, ncol = nc)
  br_x <- matrix(nrow = nr, ncol = nc)
  br_y <- matrix(nrow = nr, ncol = nc)
  
  # 2 to (n-1) cases:
  # for(i in 2:(nr-1)){
  #   for(j in 2:(nc-1)){
  #     
  #     tl_x[i,j] <- (x[i,j] + x[i+1,j-1])/2
  #     tl_y[i,j] <- (y[i,j] + y[i+1,j-1])/2
  #     
  #     tr_x[i,j] <- (x[i,j] + x[i+1,j+1])/2
  #     tr_y[i,j] <- (y[i,j] + y[i+1,j+1])/2
  #     
  #     bl_x[i,j] <- (x[i,j] + x[i-1,j+1])/2
  #     bl_y[i,j] <- (y[i,j] + y[i-1,j+1])/2
  #     
  #     br_x[i,j] <- (x[i,j] + x[i-1,j-1])/2
  #     br_y[i,j] <- (y[i,j] + y[i-1,j-1])/2
  #     
  #   }
  # }
   
  for(i in 1:nr){
    for(j in 1:nc){
      
      if(i != 1 & j != nc){
        tl_x[i,j] <- (x[i,j] + x[i-1,j+1])/2
        tl_y[i,j] <- (y[i,j] + y[i-1,j+1])/2
      }
      if(i != 1 & j != 1){
        bl_x[i,j] <- (x[i,j] + x[i-1,j-1])/2
        bl_y[i,j] <- (y[i,j] + y[i-1,j-1])/2  
      }
      if(i != nr & j != 1){
        br_x[i,j] <- (x[i,j] + x[i+1,j-1])/2
        br_y[i,j] <- (y[i,j] + y[i+1,j-1])/2
      }
      if(i != nr & j != nc){
        tr_x[i,j] <- (x[i,j] + x[i+1,j+1])/2
        tr_y[i,j] <- (y[i,j] + y[i+1,j+1])/2
      }
      
    }
  }
  
  # fill borders
  
  tl_x[1, ] <-  tl_x[2, ] - (tl_x[3, ] - tl_x[2, ])
  tl_x[, nc] <- tl_x[, nc-1] + (tl_x[, nc-1] - tl_x[, nc-2])
  tl_y[1, ] <-  tl_y[2, ] - (tl_y[3, ] - tl_y[2, ])
  tl_y[, nc] <- tl_y[, nc-1] + (tl_y[, nc-1] - tl_y[, nc-2])
  
  bl_x[1, ] <-  bl_x[2, ] - (bl_x[3, ] - bl_x[2, ])
  bl_x[, 1] <-  bl_x[, 2] - (bl_x[, 3] - bl_x[, 2])
  bl_y[1, ] <-  bl_y[2, ] - (bl_y[3, ] - bl_y[2, ])
  bl_y[, 1] <-  bl_y[, 2] - (bl_y[, 3] - bl_y[, 2])
  
  br_x[nr, ] <- br_x[nr-1, ] + (br_x[nr-1, ] - br_x[nr-2, ])
  br_x[, 1] <-  br_x[, 2] - (br_x[, 3] - br_x[, 2])
  br_y[nr, ] <- br_y[nr-1, ] + (br_y[nr-1, ] - br_y[nr-2, ])
  br_y[, 1] <-  br_y[, 2] - (br_y[, 3] - br_y[, 2])
  
  tr_x[nr, ] <- tr_x[nr-1, ] + (tr_x[nr-1, ] - tr_x[nr-2, ])
  tr_x[, nc] <-  tr_x[, nc-1] + (tr_x[, nc-1] - tr_x[, nc-2])
  tr_y[nr, ] <- tr_y[nr-1, ] + (tr_y[nr-1, ] - tr_y[nr-2, ])
  tr_y[, nc] <-  tr_y[, nc-1] + (tr_y[, nc-1] - tr_y[, nc-2])
  
  
  
  list(lon = abind::abind(tl_x, bl_x, br_x, tr_x, along = -1),
       lat = abind::abind(tl_y, bl_y, br_y, tr_y, along = -1))
  
}
