# calculate annual and seasonal indices
import os
import glob
from cdo import Cdo

cdo = Cdo()

path_in = "/home/climatedata/downscaling/validation-cv-reanalysis/data-daily-v2/"
path_out = "/home/climatedata/downscaling/validation-cv-reanalysis/etccdi-v2/"
path_temp = "/home/climatedata/tmp/"

os.makedirs(path_out, exist_ok=True)
os.makedirs(path_temp, exist_ok=True)

all_rcms = [
  'CLMcom-CCLM4-8-17', 
  'CLMcom-ETH-COSMO-crCLIM-v1-1',
  'CNRM-ALADIN63',
  'DMI-HIRHAM5',
  'GERICS-REMO2015',
  'ICTP-RegCM4-6', 
  'IPSL-WRF381P',
  'KNMI-RACMO22E',
  'MOHC-HadREM3-GA7-05',
  'MPI-CSC-REMO2009', 
  'SMHI-RCA4'
  ]

all_path_in = [os.path.join(path_in, x) for x in os.listdir(path_in)]
all_path_in.append("/home/climatedata/downscaling/validation-cv-reanalysis/data-daily-v1/bads-mbcn")
all_path_in.append("/home/climatedata/downscaling/validation-cv-reanalysis/data-daily-v1/bads-qdm")

for i_path in all_path_in:

  all_files = os.listdir(i_path)
  
  for i_rcm in all_rcms:
    
    i_path_out = os.path.join(path_out, os.path.basename(i_path), i_rcm)
    os.makedirs(i_path_out, exist_ok=True)

    i_files = [x for x in all_files if i_rcm in x]
    
    file_in_tasmax = os.path.join(i_path, [x for x in i_files if "tasmax" in x][0])
    file_in_tasmin = os.path.join(i_path, [x for x in i_files if "tasmin" in x][0])
    file_in_pr = [x for x in i_files if "pr" in x]
    if file_in_pr:
      file_in_pr = os.path.join(i_path, file_in_pr[0])


    # tasmax indices
    file_out = os.path.join(i_path_out, "SU.nc")
    if not os.path.exists(file_out):
      cdo.etccdi_su(input="-addc,273.15 " + file_in_tasmax, output=file_out)
    
    file_out = os.path.join(i_path_out, "ID.nc")
    if not os.path.exists(file_out):
      file_in_chain = "-ltc,0 " + file_in_tasmax
      cdo.yearsum(input=file_in_chain, output=file_out)
      
    # file_out = os.path.join(i_path_out, "tx90p.nc")
    # file_tmp = os.path.join(path_temp, "tmp_tx90p.nc")
    # file_in_chain = "-ydrunmin,5 -addc,273.15" + file_in_tasmax + 
    #                   " -ydrunmax,5 -addc,273.15" + file_in_tasmax
    # if not os.path.exists(file_out):
    #   cdo.ydrunpctl("90,5", input=file_in_chain, output=file_tmp)
    #   cdo.etccdi_tx90p(input="-addc,273.15 " + file_in_tasmax, output=file_out)
    #   
    # file_out = os.path.join(i_path_out, "tx10p.nc")
    # if not os.path.exists(file_out):
    #   cdo.etccdi_tx10p(input="-addc,273.15 " + file_in_tasmax, output=file_out)
  
  
    # tasmin indices
    file_out = os.path.join(i_path_out, "FD.nc")
    if not os.path.exists(file_out):
      cdo.etccdi_fd(input="-addc,273.15 " + file_in_tasmin, output=file_out)
  
    file_out = os.path.join(i_path_out, "TR.nc")
    if not os.path.exists(file_out):
      cdo.etccdi_tr(input="-addc,273.15 " + file_in_tasmin, output=file_out)
      
    # file_out = os.path.join(i_path_out, "tn10p.nc")
    # if not os.path.exists(file_out):
    #   cdo.etccdi_tn10p(input="-addc,273.15 " + file_in_tasmin, output=file_out)
    # 
    # file_out = os.path.join(i_path_out, "tn90p.nc")
    # if not os.path.exists(file_out):
    #   cdo.etccdi_tn90p(input="-addc,273.15 " + file_in_tasmin, output=file_out)
  
  
    # tas indices
    # file_in_tas = os.path.join(path_temp, "tas.nc")
    # cdo.ensmean(input=file_in_tasmax + " " + file_in_tasmin, output=file_in_tas)
    # 
    # file_out = os.path.join(i_path_out, "heatdd.nc")
    # file_in_chain = "-ifthen -ltc,15.5 " + file_in_tas + " " + "-subc,15.5 " + file_in_tas
    # if not os.path.exists(file_out):
    #   cdo.yearsum(input="-mulc,-1 " + file_in_chain, output=file_out)
    # 
    # file_out = os.path.join(i_path_out, "cooldd.nc")
    # file_in_chain = "-ifthen -gtc,22 " + file_in_tas + " " + "-subc,22 " + file_in_tas
    # if not os.path.exists(file_out):
    #   cdo.yearsum(input=file_in_chain, output=file_out)
    
    # pr indices
    if file_in_pr:
      
      file_out = os.path.join(i_path_out, "CDD.nc")
      if not os.path.exists(file_out):
        cdo.etccdi_cdd(input=file_in_pr, output=file_out)
  
      file_out = os.path.join(i_path_out, "SDII.nc")
      file_in_chain = "-ifthen -gtc,1 " + file_in_pr + " " + file_in_pr
      if not os.path.exists(file_out):
        cdo.yearmean(input=file_in_chain, output=file_out)
  
      file_out = os.path.join(i_path_out, "RR1.nc")
      file_in_chain = "-gtc,1 " + file_in_pr
      if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
      
      file_out = os.path.join(i_path_out, "R95pTOT.nc")
      file_tmp_wd = os.path.join(path_temp, "wetdays.nc")
      file_tmp_wd_p95 = os.path.join(path_temp, "wetdays_p95.nc")
      file_tmp_wd_p95_gt = os.path.join(path_temp, "wetdays_p95_gt.nc")
      if not os.path.exists(file_out):
        # cdo.ifthen(input= "-gtc,1 -mulc,86400 " + file_in + " -mulc,86400 " + file_in, output=file_tmp_wd)
        cdo.ifthen(input= "-gtc,1 " + file_in_pr + " " + file_in_pr, output=file_tmp_wd)
        cdo.timpctl(95, input=file_tmp_wd+" -timmin "+file_tmp_wd+" -timmax "+file_tmp_wd, output=file_tmp_wd_p95)
        cdo.ifthen(input="-gt "+file_tmp_wd+" "+file_tmp_wd_p95+ " "+file_tmp_wd,output=file_tmp_wd_p95_gt)
        cdo.div(input="-yearsum -setmisstoc,0 "+file_tmp_wd_p95_gt+" -yearsum "+file_in_pr,output=file_out)
  
      file_out = os.path.join(i_path_out, "rx1day.nc")
      if not os.path.exists(file_out):
        cdo.etccdi_rx1day(input=file_in_pr, output=file_out)
      
      file_out = os.path.join(i_path_out, "rx5day.nc")
      file_in_chain = "-runsum,5 " + file_in_pr
      if not os.path.exists(file_out):
        cdo.etccdi_rx5day(input=file_in_chain, output=file_out)
      
      file_out = os.path.join(i_path_out, "r10mm.nc")
      file_in_chain = "-gtc,10 " + file_in_pr
      if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
      
      file_out = os.path.join(i_path_out, "r20mm.nc")
      file_in_chain = "-gtc,20 " + file_in_pr
      if not os.path.exists(file_out):
        cdo.yearsum(input=file_in_chain, output=file_out)
