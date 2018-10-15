'''

   plot maps using the data generated by gendata_map_X.py 


'''

import numpy as np
import xarray as xr

from matplotlib import pyplot as plt
import mpl_toolkits.basemap as bm


# Load data

#fname = '/home/ecougnon/ana/SST_map_mhw_Aus'
header = '/home/ecougnon/data/DPS/reanalysis/ETKF/'
fname = header + 'SSTa_stats_map_Aus.nc'
#'/home/ecougnon/ana/SSTa_map_Aus.nc'
fname2 = header + 'SSTa_stats_nina_map_Aus.nc'
#'/home/ecougnon/ana/SSTa_map_nina075Yr_Aus.nc'
fname2_sig = header + 'SSTa_stats_nina_map_Aus_sig'
#'/home/ecougnon/ana/SSTa_map_nina075Yr_Aus_sig'
fname3 = header + 'SSTa_stats_nino_map_Aus.nc'
#'/home/ecougnon/ana/SSTa_map_nino075Yr_Aus.nc'
fname3_sig = header + 'SSTa_stats_nino_map_Aus_sig'
#'/home/ecougnon/ana/SSTa_map_nino075Yr_Aus_sig'
figfile = header + 'map_ssta_thetadiff_sig_dps_enso_Aus.png'
#'/home/ecougnon/ana/map_ssta_distribution_enso_oz_sig.eps'

SST_nina = xr.open_dataset(fname2)
ninap10 = SST_nina['Tp10']
ninap90 = SST_nina['Tp90']
SST_nino = xr.open_dataset(fname3)
ninop10 = SST_nino['Tp10']
ninop90 = SST_nino['Tp90']
SST_X = xr.open_dataset(fname)
sst_p10 = SST_X['Tp10']
sst_p90 = SST_X['Tp90']
lon_map = SST_X['lon'] + 360 # to use with DPS model
lat_map = SST_X['lat']

# limits for a 95% significance
data_LaN = np.load(fname2_sig + '.npz')
data_ElN = np.load(fname3_sig + '.npz')
rt_low_LaN_p90 = data_LaN['rt_low_LaN_p90']
rt_high_LaN_p90 = data_LaN['rt_high_LaN_p90']
rt_low_LaN_p10 = data_LaN['rt_low_LaN_p10']
rt_high_LaN_p10 = data_LaN['rt_high_LaN_p10']
rt_low_ElN_p90 = data_ElN['rt_low_ElN_p90']
rt_high_ElN_p90 = data_ElN['rt_high_ElN_p90']
rt_low_ElN_p10 = data_ElN['rt_low_ElN_p10']
rt_high_ElN_p10 = data_ElN['rt_high_ElN_p10']
# create masked array for the hatched area (region with 95% 
#  significance level -- mask == 1 with the level of significance
#  is reached -- easier to plot hatched areas of mask==1
mask_LaN_p90 = np.ones(rt_low_LaN_p90.shape)
mask_LaN_p90 = np.ma.masked_where((ninap90>rt_low_LaN_p90) & \
                                  (ninap90<rt_high_LaN_p90), \
                                  mask_LaN_p90)
mask_LaN_p10 = np.ones(rt_low_LaN_p10.shape)
mask_LaN_p10 = np.ma.masked_where((ninap10>rt_low_LaN_p10) & \
                                  (ninap10<rt_high_LaN_p10), \
                                  mask_LaN_p10)
mask_ElN_p90 = np.ones(rt_low_ElN_p90.shape)
mask_ElN_p90 = np.ma.masked_where((ninop90>rt_low_ElN_p90) & \
                                  (ninop90<rt_high_ElN_p90), \
                                  mask_ElN_p90)
mask_ElN_p10 = np.ones(rt_low_ElN_p10.shape)
mask_ElN_p10 = np.ma.masked_where((ninop10>rt_low_ElN_p10) & \
                                  (ninop10<rt_high_ElN_p10), \
                                  mask_ElN_p10)

# Maps
domain = [-55, 90, 10, 180] #[-55, 90, 10, 180]
domain_draw = [-50, 90, 10, 180] #[-55, 90, 10, 180]
dlat = 10
dlon = 30
#llat, llon = np.meshgrid(lat_map, lon_map)
llon, llat = np.meshgrid(lon_map, lat_map)
bg_col = '0.6'
cont_col = '1.0'
bin_col = 0.1
bin_bar = 0.5

my_dpi = 300

plt.figure(figsize=(4000/my_dpi,3500/my_dpi))
#plt.figure(figsize=(15,17))
plt.clf()
# plot p10 threshold
plt.subplot(2,2,1, facecolor=bg_col)
proj = bm.Basemap(projection='merc', llcrnrlat=domain[0], llcrnrlon=domain[1], \
                  urcrnrlat=domain[2], urcrnrlon=domain[3], resolution='i')
proj.fillcontinents(color=(0,0,0), lake_color=None, ax=None, \
                    zorder=None, alpha=None)
proj.drawparallels(range(domain_draw[0],domain_draw[2]+1,dlat), \
                   labels=[True,False,False,False], fontsize=14)
proj.drawmeridians(range(domain_draw[1],domain_draw[3]+1,dlon), \
                   labels=[False,False,False,True], fontsize=14)
lonproj, latproj = proj(llon, llat)
plt.contourf(lonproj, latproj, ninop90-sst_p90, \
             levels=np.arange(-2,2+bin_col,bin_col), cmap=plt.cm.seismic)
cb=plt.colorbar(ticks=np.arange(-2,2+bin_bar,bin_bar),shrink=0.9)
cb.ax.tick_params(labelsize=14)
plt.contourf(lonproj, latproj, mask_ElN_p90, hatches = '.', alpha=0)
plt.title('a) p90$_{EN}$ - p90$_{ALL}$', \
          fontsize=16, y=1.02)


plt.subplot(2,2,3, facecolor=bg_col)
proj = bm.Basemap(projection='merc', llcrnrlat=domain[0], llcrnrlon=domain[1], \
                  urcrnrlat=domain[2], urcrnrlon=domain[3], resolution='i')
proj.fillcontinents(color=(0,0,0), lake_color=None, ax=None, \
                    zorder=None, alpha=None)
proj.drawparallels(range(domain_draw[0],domain_draw[2]+1,dlat), \
                   labels=[True,False,False,False], fontsize=14)
proj.drawmeridians(range(domain_draw[1],domain_draw[3]+1,dlon), \
                   labels=[False,False,False,True], fontsize=14)
lonproj, latproj = proj(llon, llat)
plt.contourf(lonproj, latproj, ninop10-sst_p10, \
             levels=np.arange(-2,2+bin_col,bin_col), cmap=plt.cm.seismic)
cb=plt.colorbar(ticks=np.arange(-2,2+bin_bar,bin_bar),shrink=0.9)
cb.ax.tick_params(labelsize=14)
plt.contourf(lonproj, latproj, mask_ElN_p10, hatches = '.', alpha=0)
plt.title('b)  p10$_{EN}$ - p10$_{ALL}$', \
          fontsize=16, y=1.02)


plt.subplot(2,2,2, facecolor=bg_col)
proj = bm.Basemap(projection='merc', llcrnrlat=domain[0], llcrnrlon=domain[1], \
                  urcrnrlat=domain[2], urcrnrlon=domain[3], resolution='i')
proj.fillcontinents(color=(0,0,0), lake_color=None, ax=None, \
                    zorder=None, alpha=None)
proj.drawparallels(range(domain_draw[0],domain_draw[2]+1,dlat), \
                   labels=[True,False,False,False], fontsize=14)
proj.drawmeridians(range(domain_draw[1],domain_draw[3]+1,dlon), \
                   labels=[False,False,False,True], fontsize=14)
lonproj, latproj = proj(llon, llat)
plt.contourf(lonproj, latproj, ninap90-sst_p90, \
             levels=np.arange(-2,2+bin_col,bin_col), cmap=plt.cm.seismic)
cb=plt.colorbar(ticks=np.arange(-2,2+bin_bar,bin_bar),shrink=0.9)
cb.ax.tick_params(labelsize=14)
plt.contourf(lonproj, latproj, mask_LaN_p90, hatches = '.', alpha=0)
plt.title('c)  p90$_{LN}$ - p90$_{ALL}$', \
          fontsize=16, y=1.02)


plt.subplot(2,2,4, facecolor=bg_col)
proj = bm.Basemap(projection='merc', llcrnrlat=domain[0], llcrnrlon=domain[1], \
                  urcrnrlat=domain[2], urcrnrlon=domain[3], resolution='i')
proj.fillcontinents(color=(0,0,0), lake_color=None, ax=None, \
                    zorder=None, alpha=None)
proj.drawparallels(range(domain_draw[0],domain_draw[2]+1,dlat), \
                   labels=[True,False,False,False], fontsize=14)
proj.drawmeridians(range(domain_draw[1],domain_draw[3]+1,dlon), \
                   labels=[False,False,False,True], fontsize=14)
lonproj, latproj = proj(llon, llat)
plt.contourf(lonproj, latproj, ninap10-sst_p10, \
             levels=np.arange(-2,2+bin_col,bin_col), cmap=plt.cm.seismic)
cb=plt.colorbar(ticks=np.arange(-2,2+bin_bar,bin_bar),shrink=0.9)
cb.ax.tick_params(labelsize=14)
plt.contourf(lonproj, latproj, mask_LaN_p10, hatches = '.', alpha=0)
plt.title('d)  p10$_{LN}$ - p10$_{ALL}$', \
          fontsize=16, y=1.02)

plt.savefig(figfile,bbox_inches='tight', format='png', dpi=300)

plt.show()

'''
## plot std from the monthly mean field, p90/p10 monthly field
plt.figure(figsize=(20,12))
plt.clf()
# plot p10 threshold
plt.subplot(1,3,1, facecolor=bg_col)
proj = bm.Basemap(projection='merc', llcrnrlat=domain[0], llcrnrlon=domain[1], \
                  urcrnrlat=domain[2], urcrnrlon=domain[3], resolution='i')
proj.fillcontinents(color=(0,0,0), lake_color=None, ax=None, \
                    zorder=None, alpha=None)
proj.drawparallels(range(domain_draw[0],domain_draw[2]+1,dlat), \
                   lys_LaN_p90p10_Aus_dpsabels=[True,False,False,False])
proj.drawmeridians(range(domain_draw[1],domain_draw[3]+1,dlon), \
                   labels=[False,False,False,True])
lonproj, latproj = proj(llon, llat)
plt.contourf(lonproj, latproj, ,SST_X['Tstd'] \
             levels=np.arange(-2,2+bin_col,bin_col), cmap=plt.cm.seismic)
cb=plt.colorbar(ticks=np.arange(-2,2+bin_bar,bin_bar),shrink=0.9)
cb.ax.tick_params(labelsize=14)
plt.title('El Nino - the whole time series (90th p.)', \
          fontsize=16, y=1.08)
'''





