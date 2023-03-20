# Add the vertices coordinates of the cells of a curvilinear grid
# Ref: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.10/cf-conventions.html#_data_representative_of_cells

import numpy as np
import netCDF4 as nc
import datetime
import os
from calc_vertices import *  


path_data='/rhomes/lisa.bernini/CHAPTER/W_UP/Data/Upsc_grid/Strength/Remapcon_corners/Wt_corners'


for root, directories, file in os.walk(path_data):
        for file in file:
                if(file.startswith("W_val")):
                    ncdata=nc.Dataset(os.path.join(path_data,file),mode='a')
                    lat=ncdata['XLAT']
                    lon=ncdata['XLONG']
                    # Number of cell vertices
                    ncdata.createDimension('vertices',4)
                    print('Dimension created')
                    # Creation of the boundary variable
                    lat_vert=ncdata.createVariable(varname='lat_vertices',dimensions=('south_north','west_east','vertices'),
                                                datatype='float',compression='zlib')
                    lon_vert=ncdata.createVariable(varname='lon_vertices',dimensions=('south_north','west_east','vertices'),
                                                datatype='float',compression='zlib')
                    # Compute the coordinates of the corners of each cell
                    (lon_v,lat_v)=calc_vertices(lon[:].data,lat[:].data)
                    lat_vert[:,:,:]=lat_v
                    lon_vert[:,:,:]=lon_v
                    # It is not necessary to provide units and long_name to the bounds
                    #lat_vert.units = 'degrees_north' 
                    #lon_vert.units = 'degrees_east'
                    #lat_vert.long_name = 'latitude vertices'
                    #lon_vert.long_name = 'longitude vertices'
                    # Specify the boundary variable of each coordinates variables
                    lat.bounds='lat_vertices'
                    lon.bounds='lon_vertices'
