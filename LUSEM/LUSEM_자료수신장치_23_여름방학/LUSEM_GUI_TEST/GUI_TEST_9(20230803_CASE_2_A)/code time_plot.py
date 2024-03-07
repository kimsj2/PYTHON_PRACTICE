# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:09:05 2023

@author: whseol-lab
"""

import pandas as pd
import numpy as np
import datetime as dt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.style
import matplotlib.dates as mdates
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
from glob import glob
import os
import gc
import sys
import time
start_codetime = time.time()
start_ct = dt.datetime.now().isoformat(timespec='seconds')
################################################################################
################################################################################

init_path = r'Z:\2023_Summer\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_9(20230803_CASE_2_A)\deque\test1(1h)\slicing'


data = pd.read_csv(os.path.join(init_path,'time_slicing.txt'), header=None, sep='\s+')

t0 = pd.to_datetime(data.iloc[:,0])
t1 = pd.to_datetime(data.iloc[:,1])

dt0 = t1 - t0


s0 = []

for i in dt0:
    s0.append(i.total_seconds())

# label size
xl = 28
yl = 28
# Tick label size
xtl = 20
ytl = 20
# Tck Mark Length and Width
w1= 1.00
l1 = 10.0
w2 = 0.75
l2= 5.0  

# Tick mark interval
major_locator = mdates.AutoDateLocator()
minor_locator = mdates.AutoDateLocator(maxticks=30)
xformatter = mdates.DateFormatter('%b-%d\n%H:%M:%S')
xformatter1 = mdates.DateFormatter('%H')
mpl.style.use('classic')
plt.rcParams['font.family'] = 'Times New Roman'
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

plt.ioff()
fig = plt.figure(num=1, figsize=(16,12))
gs = gridspec.GridSpec(1, 1) 

ax1 = fig.add_subplot(gs[0])

ax1.plot(t0, s0, 'ro')

ax1.set_yscale('log')
#ax6.set_ylim([0,80])
#ax6.set_xlim([start_time, end_time])
ax1.set_ylabel('Processing time', size=yl, fontweight='bold', labelpad=10)
ax1.set_xlabel('Time', size=xl, fontweight='bold')
ax1.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax1.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
ax1.grid(True, which="both")
ax1.xaxis.set_major_locator(major_locator)
ax1.xaxis.set_minor_locator(minor_locator)
ax1.xaxis.set_major_formatter(xformatter)
#ax7.xaxis.set_minor_formatter(xformatter1)
#ax1.yaxis.set_major_locator(ticker.MultipleLocator(10))
#ax1.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax1.xaxis.set_tick_params(which='major', pad=10)
plt.setp(ax1.get_xticklabels(),visible=True)

#plt.tight_layout()
#fig.align_ylabels([ax1,ax2,ax5,ax6,ax7])
fig.align_labels()
plt.savefig(os.path.join(init_path,'time.png'), dpi=300, bbox_inches='tight')
#plt.show()
plt.clf()
gc.collect()



plt.ioff()
fig = plt.figure(num=1, figsize=(16,12))
gs = gridspec.GridSpec(1, 1) 

ax1 = fig.add_subplot(gs[0])

ax1.hist(s0, bins=100)

ax1.set_yscale('log')
#ax6.set_ylim([0,80])
#ax1.set_xlim([0,50])
ax1.set_xlabel('Processing time, s', size=xl, fontweight='bold')
ax1.set_ylabel('Frequency', size=yl, fontweight='bold', labelpad=10)
ax1.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax1.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
ax1.grid(True, which="both")
#ax1.xaxis.set_major_locator(major_locator)
#ax1.xaxis.set_minor_locator(minor_locator)
#ax1.xaxis.set_major_formatter(xformatter)
#ax7.xaxis.set_minor_formatter(xformatter1)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax1.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax1.xaxis.set_tick_params(which='major', pad=10)
plt.setp(ax1.get_xticklabels(),visible=True)

#plt.tight_layout()
#fig.align_ylabels([ax1,ax2,ax5,ax6,ax7])
fig.align_labels()
plt.savefig(os.path.join(init_path,'time_hist.png'), dpi=300, bbox_inches='tight')
#plt.show()
plt.clf()
gc.collect()











################################################################################
################################################################################
print('\n\n\n######################################################')
print('Code time: ', start_ct, '~', dt.datetime.now().isoformat(timespec='seconds'))
codetime = np.round(time.time() - start_codetime, 2)
print('processing time: ', f'{codetime} s ({np.round(codetime/3600,2)} hr)')
print('######################################################')