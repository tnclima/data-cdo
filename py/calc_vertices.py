import numpy as np
import datetime

def calc_vertices(mlon,mlat):
# calculate vertices for netcdf cf convention from 2d-matrices of lon lat
    x = mlon
    y = mlat
    (nr,nc)=np.shape(x)
    tl_x=np.empty((nr,nc))
    tl_y=np.empty((nr,nc)) 
    bl_x=np.empty((nr,nc))
    bl_y=np.empty((nr,nc))
    tr_x=np.empty((nr,nc))
    tr_y=np.empty((nr,nc))
    br_x=np.empty((nr,nc))
    br_y=np.empty((nr,nc))
    for i in range(nr):
        print('i :',i,' ; date :',datetime.datetime.now())
        for j in range(nc):
            if i!=0 and j!=nc-1:
                tl_x[i,j] = (x[i,j] + x[i-1,j+1])/2
                tl_y[i,j] = (y[i,j] + y[i-1,j+1])/2
            if i!=0 and j!=0:
                bl_x[i,j] = (x[i,j] + x[i-1,j-1])/2
                bl_y[i,j] = (y[i,j] + y[i-1,j-1])/2
            if i!=nr-1 and j!=0:
                br_x[i,j] = (x[i,j] + x[i+1,j-1])/2
                br_y[i,j] = (y[i,j] + y[i+1,j-1])/2
            if i!=nr-1 and j!=nc-1:
                tr_x[i,j] = (x[i,j] + x[i+1,j+1])/2
                tr_y[i,j] = (y[i,j] + y[i+1,j+1])/2
    tl_x[0,:] =  tl_x[1,:] - (tl_x[2,:] - tl_x[1,:])
    tl_x[:,nc-1] = tl_x[:,nc-2] + (tl_x[:,nc-2] - tl_x[:,nc-3])
    tl_y[0,:] =  tl_y[1,:] - (tl_y[2,:] - tl_y[1,:])
    tl_y[:,nc-1] = tl_y[:,nc-2] + (tl_y[:,nc-2] - tl_y[:,nc-3])
    bl_x[0,:] =  bl_x[1,:] - (bl_x[2,:] - bl_x[1,:])
    bl_x[:,0] =  bl_x[:,1] - (bl_x[:,2] - bl_x[:,1])
    bl_y[0,:] =  bl_y[1,:] - (bl_y[2,:] - bl_y[1,:])    
    bl_y[:,0] =  bl_y[:,1] - (bl_y[:,2] - bl_y[:,1])
    br_x[nr-1,:] = br_x[nr-2,:] + (br_x[nr-2,:] - br_x[nr-3,:])
    br_x[:,0] =  br_x[:,1] - (br_x[:,2] - br_x[:,1])
    br_y[nr-1,:] = br_y[nr-2,:] + (br_y[nr-2,:] - br_y[nr-3,:])
    br_y[:,0] =  br_y[:,1] - (br_y[:,2] - br_y[:,1]) 
    tr_x[nr-1,:] = tr_x[nr-2,:] + (tr_x[nr-2,:] - tr_x[nr-3,:])
    tr_x[:,nc-1] =  tr_x[:,nc-2] + (tr_x[:,nc-2] - tr_x[:,nc-3])
    tr_y[nr-1,:] = tr_y[nr-2,:] + (tr_y[nr-2,:] - tr_y[nr-3,:])
    tr_y[:,nc-1] =  tr_y[:,nc-2] + (tr_y[:,nc-2] - tr_y[:,nc-3])
    lat=np.empty((nr, nc, 4))
    lon=np.empty((nr, nc, 4))
    lat[:,:,0]=br_y
    lat[:,:,1]=tr_y
    lat[:,:,2]=tl_y
    lat[:,:,3]=bl_y
    lon[:,:,0]=br_x
    lon[:,:,1]=tr_x
    lon[:,:,2]=tl_x
    lon[:,:,3]=bl_x
    return(lon,lat)
