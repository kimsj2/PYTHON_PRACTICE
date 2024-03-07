# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 15:09:33 2021

@author: Seolwh
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
import tkinter as tk
from tkinter import filedialog
import glob
import os
import gc
import time
import mod_datpar as datpar

start_codetime = time.time()


#%% Data read.
#path = r'F:\Research\Energy Calibration_LUSEM\2022_LUSEM_EQM_Energy-Channel Calibration\Test Results\Temp2'


####################################################################################################
# =============================================================================
# # datpar -> dat file -> txt file (1차: dat file --> 1 byte 씩 쪼개서 저장)
# root = tk.Tk()
# root.withdraw()
# 
# path = r'C:/Users/kimsj/.spyder-py3/LUSEM/mod_Program'
# 
# dat_filename = glob.glob(path+'/*.dat')
# datpar.datpar(dat_filename, path)
# =============================================================================
####################################################################################################

path = r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_TEST\test4(20230713_Extension_off)'

sci_path = glob.glob(path+'/*sci.txt')
soh_path = glob.glob(path+'/*soh.txt')
noi_path = glob.glob(path+'/*noi.txt')

sci = []
with open(sci_path[0], 'r') as file:    
    for line in file:
        sci.append(line.split()[:-5])

sci = pd.DataFrame(sci, dtype='str')
soh = pd.read_csv(soh_path[0], sep='\t', dtype='str', header=None)
noi = pd.read_csv(noi_path[0], sep='\t', dtype='str', header=None)
print('Data read: complete', dt.datetime.now().replace(microsecond=0))

#%% Data processing
# time cal.
pn_sci = len(sci.iloc[:,0]) # packet number of sci data
pn_soh = len(soh.iloc[:,0]) # packet number of soh data
pn_noi = len(noi.iloc[:,0]) # packet number of noi data

sci_met = sci.iloc[:,7] + sci.iloc[:,8] + sci.iloc[:,9] + sci.iloc[:,10] # LSP mission elapsed time, total seconds from 20010101T09:00:00
soh_met = soh.iloc[:,7] + soh.iloc[:,8] + soh.iloc[:,9] + soh.iloc[:,10]
noi_met = noi.iloc[:,7] + noi.iloc[:,8] + noi.iloc[:,9] + noi.iloc[:,10]

def time_cal(met):
    time_iso = []
    packet_num = len(met)
    for i in np.arange(packet_num):
        dt0 = int(met.iloc[i], 16)
        dt1 = dt.datetime(2001,1,1,9) + dt.timedelta(seconds=(dt0))
        time_iso.append(dt1.isoformat(timespec='seconds'))
    time_ut = pd.to_datetime(time_iso)
    time_iso = pd.DataFrame(time_iso, columns=['Time'])
    return time_ut, time_iso

time_sci, time_sci_iso = time_cal(sci_met)
time_soh, time_soh_iso = time_cal(soh_met)
time_noi, time_noi_iso = time_cal(noi_met)

start_time = time_sci[0]
end_time = time_sci[-1]
st_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
et_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
t_delta = str(pn_sci)

print('Time conversion: complete', dt.datetime.now().replace(microsecond=0))

'''
sci_scpktif (compression type, 1 byte) = LCCSNNNN
L: Log compressed
CC: compression type (extension + compression)
S: summing

256 bin, 2 byte = 0b0000 = 0x00 -> total 512 bytes
256 bin, 1 byte = 0b1010 = 0xA0 -> total 256 bytes
512 bin, 2 byte = 0b0100 = 0x40 -> total 1024 bytes
512 bin, 1 byte = 0b1110 = 0xE0 -> total 512 bytes
'''

logmap = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124, 
128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 
256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496,
512, 544, 576, 608, 640, 672, 704, 736, 768, 800, 832, 864, 896, 928, 960, 992,
1024, 1088, 1152, 1216, 1280, 1344, 1408, 1472, 1536, 1600, 1664, 1728, 1792, 1856, 1920, 1984,
2048, 2176, 2304, 2432, 2560, 2688, 2816, 2944, 3072, 3200, 3328, 3456, 3584, 3712, 3840, 3968,
4096, 4352, 4608, 4864, 5120, 5376, 5632, 5888, 6144, 6400, 6656, 6912, 7168, 7424, 7680, 7936,
8192, 8704, 9216, 9728, 10240, 10752, 11264, 11776, 12288, 12800, 13312, 13824, 14336, 14848, 15360, 15872,
16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, 30720, 31744,
32768, 34816, 36864, 38912, 40960, 43008, 45056, 47104, 49152, 51200, 53248, 55296, 57344, 59392, 61440, 63488,
65536, 69632, 73728, 77824, 81920, 86016, 90112, 94208, 98304, 102400, 106496, 110592, 114688, 118784, 122880, 126976,
131072, 139264, 147456, 155648, 163840, 172032, 180224, 188416, 196608, 204800, 212992, 221184, 229376, 237568, 245760, 253952]
import warnings
warnings.filterwarnings("ignore", message="Attempted to set non-positive bottom ylim on a log-scaled axis.\nInvalid limit will be ignored.")

def fit_gaussian(x, a, b, c):
    return (a / (b * np.sqrt(2 * np.pi))) * np.exp(-(x-c)**2/(2*b**2))

def fit_sh(x, a, b, c): # Steinhart-Hart equation
    return 1 / (a + b * np.log(x) + c * ((np.log(x))**3))

def signhex2dec(data):
    dlen = len(data)
    ddec = []
    for i in np.arange(dlen):
        data0 = bin(int(data[i], 16))[2:].zfill(16)
        msb0 = data0[0]
        data1 = data0[1:]
        if msb0 == '0':
            ddec.append(int(data1,2))
        elif msb0 == '1':
            ddec.append(-2**15 + int(data1,2))
        else:
            pass
    return np.array(ddec)

def header_creation(data, pktnum):    
    data_header = pd.DataFrame(columns=['Packet Version Number', 'Packet Type', 'Secondary Header', 'APID', 'Packet Sequence Flag', 'Packet Sequence Count', 'Packet Data Length', 'Mission Elapsed Time','Science Mode','Extension', 'Compression', 'MapID', 'Packet Mode', 'Reserved Length', 'SCICOM', 'CRC'])
    
    h0 = (data.iloc[:, 1] + data.iloc[:, 2]).apply(int, base=16).apply(bin).str[2:].str.zfill(16)
    data_header.loc[:, 'Packet Version Number'] = '0b' + h0.str[:3]
    data_header.loc[:, 'Packet Type'] = '0b' + h0.str[3:4]
    data_header.loc[:, 'Secondary Header'] = '0b' + h0.str[4:5]
    data_header.loc[:, 'APID'] = h0.str[5:].apply(int, base=2).apply(hex)
    
    h1 = (data.iloc[:, 3] + data.iloc[:, 4]).apply(int, base=16).apply(bin).str[2:].str.zfill(16)
    data_header.loc[:, 'Packet Sequence Flag'] = '0b' + h1.str[:2]
    data_header.loc[:, 'Packet Sequence Count'] = h1.str[2:].apply(int, base=2).apply(hex)
    
    h2 = data.iloc[:, 5] + data.iloc[:, 6]
    data_header.loc[:, 'Packet Data Length'] = '0x' + h2
    
    h3 = data.iloc[:, 7] + data.iloc[:, 8] + data.iloc[:, 9] + data.iloc[:, 10] + data.iloc[:, 11] + data.iloc[:, 12]
    data_header.loc[:, 'Mission Elapsed Time'] = '0x' + h3
    
    h4 = '0x' + data.iloc[:, 13]
    data_header.loc[:, 'Science Mode'] = h4
    
    h4a = (data.iloc[:, 13]).apply(int, base=16).apply(bin).str[2:].str.zfill(8)
    data_header.loc[:, 'Extension'] = (h4a.str[1] == '1')
    data_header.loc[:, 'Compression'] = (h4a.str[0] == '1')
    
    h5 = '0x' + data.iloc[:, 14]
    data_header.loc[:, 'MapID'] = h5
    
    h6 = '0x' + data.iloc[:, 15]
    data_header.loc[:, 'Packet Mode'] = h6
    
    h7 = '0x' + data.iloc[:, 16] + data.iloc[:, 17]
    data_header.loc[:, 'Reserved Length'] = h7
    
    h8 = '0x' + data.iloc[:, 18]
    data_header.loc[:, 'SCICOM'] = h8
    
    h9 = '0x' + data.iloc[:, 19] + data.iloc[:, 20]
    data_header.loc[:, 'CRC'] = h9
    return data_header

def get_bar(data_a, data_b, time_test, ct, mapid, plot_num):
    if ct == '00':
        ct0 = '256 bin (2-byte)'
    elif ct == 'A0':
        ct0 = '256 bin (1-byte)'
    elif ct == '40':
        ct0 = '512 bin (2-byte)'
    elif ct == 'E0':
        ct0 = '512 bin (1-byte)'
    
    data_a = data_a.drop(data_a.loc[data_a.iloc[:,-1] > 50000].index)
    data_b = data_b.drop(data_b.loc[data_b.iloc[:,-1] > 50000].index)
    
    data_a = data_a.iloc[:-15,:]
    data_b = data_b.iloc[:-15,:]
    
    start_time = time_test[0].strftime('%Y-%m-%d %H:%M:%S')
    end_time = time_test[-1].strftime('%Y-%m-%d %H:%M:%S')
    #t_delta = str((time_test[-1] - time_test[0]).seconds + 1)
    
    d_pktnum = len(data_a.iloc[:,0])
    
    
    his_a = data_a.sum(axis=0) / d_pktnum
    his_b = data_b.sum(axis=0) / d_pktnum    
    d_bin = len(his_a)
    d_bin_range = np.arange(d_bin-1)
    
    his_a = his_a.iloc[:(d_bin-1)]
    his_b = his_b.iloc[:(d_bin-1)]
    
    
    onec = 1 / d_pktnum # one count
    
    peak_a, prop_a = find_peaks(his_a, height=2*onec, prominence=10*onec)
    peak_a_height = prop_a['peak_heights']
    lbase_a = prop_a['left_bases']
    rbase_a = prop_a['right_bases']
    
    peak_b, prop_b = find_peaks(his_b, height=2*onec, prominence=10*onec)
    peak_b_height = prop_b['peak_heights']
    lbase_b = prop_b['left_bases']
    rbase_b = prop_b['right_bases']
    
    # =============================================================================
    # range0 = np.arange(left_base[0], right_base[0]+1, 1)
    # y0 = his_a[range0]
    # 
    # init_g = [peak1_height[0], np.sqrt(peak1_height[0]), peak1[0]]
    # 
    # popt, pcov = curve_fit(fit_gaussian, range0, y0, p0=init_g)
    # perr=np.sqrt(np.diag(pcov))
    # fit0 = fit_gaussian(range0, *popt)
    # =============================================================================
    
    if d_bin == 128:
        minor_loc = 2
        major_loc = 8
    elif d_bin == 256:
        minor_loc = 4
        major_loc = 16
    else:
        pass
    
    
    # label size
    xl = 18
    yl = 18
    # Tick label size
    xtl = 14
    ytl = 14
    # Tck Mark Length and Width
    w1= 1.00
    l1 = 10.0
    w2 = 0.75
    l2= 5.0  
    
    # Tick mark interval
    mpl.style.use('classic')
    plt.rcParams['font.family'] = 'Times New Roman'
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    
    plt.ioff()
    fig = plt.figure(num=2, figsize=(10,10))
    gs = gridspec.GridSpec(2, 1, height_ratios=(1,1), hspace=0.06) 
    
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharey=ax1)
    
    ax1.axhline(onec, 0, 1, color='g', ls='dashed', alpha=0.8, label='1-count')
    ax1.step(d_bin_range, his_b, where='mid', color='b', label='Measured')
    ax1.plot(peak_b, peak_b_height, 'ro', alpha=0.2, label='Peak')
    text_kwargs1 = dict(ha='center', va='top', fontsize=12, color='r')
    for i in np.arange(len(peak_b)):
        ax1.text(peak_b[i], peak_b_height[i]*1.5 , str(peak_b[i]), **text_kwargs1)
    
    ax1.legend(fontsize=14, ncol=1, bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    ax1.set_title('Integration Time: '+str(d_pktnum)+'\nTest time: '+start_time+' - '+end_time+'\nExtension & Compression: '+ct0+', MAP ID: '+mapid, loc='left')
    ax1.set_ylabel('TELESCOPE-B, Count/s', size=yl, fontweight='bold', labelpad=10)
    ax1.set_yscale('log')
    ax1.set_xlim([0, d_bin])
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(major_loc))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(minor_loc))
    ax1.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
    ax1.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
    ax1.grid(True, which="both", alpha=0.5)
    plt.setp(ax1.get_xticklabels(),visible=False)    
    
    ax2.axhline(onec, 0, 1, color='g', ls='dashed', alpha=0.8, label='1-count')
    ax2.step(d_bin_range, his_a, where='mid', color='b', label='Measured')
    ax2.plot(peak_a, peak_a_height, 'ro', alpha=0.2, label='Peak')
    text_kwargs1 = dict(ha='center', va='top', fontsize=12, color='r')
    for i in np.arange(len(peak_a)):
        ax2.text(peak_a[i], peak_a_height[i]*1.5 , str(peak_a[i]), **text_kwargs1)
    
    #ax2.legend(fontsize=12, ncol=1)
    ax2.set_ylabel('TELESCOPE-A, Count/s', size=yl, fontweight='bold', labelpad=10)
    ax2.set_xlabel('ADC', size=xl, fontweight='bold')
    ax2.set_yscale('log')
    ax2.set_xlim([0, d_bin])
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(major_loc))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(minor_loc))
    ax2.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
    ax2.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
    ax2.grid(True, which="both", alpha=0.5)
    ax2.xaxis.set_tick_params(which='major', pad=5)
    plt.setp(ax2.get_xticklabels(),visible=True)
    fig.align_labels()
    plt.savefig(path+'/plot_bar_'+ct+'_'+mapid+'_'+str(plot_num)+'.png', dpi=200, bbox_inches='tight')
    #plt.show()
    plt.clf()
    gc.collect()
    return



#%% Science data
sci_header = header_creation(sci, pn_sci)
sci_mapid = sci.iloc[:,14] # MAP ID
sci_scpktif = sci.iloc[:,13] # compression type
print('Science header: complete', dt.datetime.now().replace(microsecond=0))

def func_dropd(data): # drop_duplicates
    data_len = len(data)
    data_range = np.arange(data_len)
    data_shift = data.shift()
    index_min, index_max = [], []
    for i in data_range:
        dx1 = data[i]
        dx2 = data_shift[i]
        if dx1 != dx2:
            index_min.append(i)
            if i == 0:
                index_max.append(data_len-1)
            else:
                index_max.append(data_range[i-1])
    data_id = data[index_min]
    data_id = list(data_id)
    index_max.sort()
    return data_id, index_min, index_max

mapid, mapid_min, mapid_max = func_dropd(sci_mapid)

ct_list = list(sci_scpktif.drop_duplicates())
comp_type, comp_min, comp_max = func_dropd(sci_scpktif) # compression type, drop_duplicates

# sci data
sci_data = sci.iloc[:,21:].T.reset_index(drop=True).T
sci_a = pd.DataFrame()
sci_b = pd.DataFrame()

fig_num = 0

savepath_his = f'{path}\Science data_separate'
os.makedirs(savepath_his, exist_ok=True)

for i in np.arange(len(comp_type)): #len(comp_type)
    ct0 = comp_type[i]
    ct0_min, ct0_max = comp_min[i], comp_max[i]+1
    sci0 = sci_data.iloc[ct0_min:ct0_max, :]
    sci0_len = len(sci0.iloc[:,0])
    
    if ct0 == '00':
        sci0 = sci0.iloc[:, :512]
        sci0 = sci0.iloc[:,::2].T.reset_index(drop=True).T + sci0.iloc[:,1::2].T.reset_index(drop=True).T
        sci0 = sci0.fillna(0).apply(lambda x: x.astype(str).map(lambda x: int(x, base=16)))
        sci0a = sci0.iloc[:,:128].T.reset_index(drop=True).T
        sci0b = sci0.iloc[:,128:].T.reset_index(drop=True).T
        sci_a = pd.concat([sci_a, sci0a])
        sci_b = pd.concat([sci_b, sci0b])
        
        sci_map0 = sci_mapid[sci0.index].reset_index(drop=True)
        mapid0, map0_min, map0_max = func_dropd(sci_map0)
        time0 = time_sci[sci0.index]
        bar_a0 = sci0a.copy().reset_index(drop=True)
        bar_b0 = sci0b.copy().reset_index(drop=True)
        
        for j in np.arange(len(mapid0)):
            if mapid0[j] == '00':
                pass
            else:
                bar_a = bar_a0.loc[map0_min[j]:map0_max[j]+1, :]
                bar_b = bar_b0.loc[map0_min[j]:map0_max[j]+1, :]
                time1 = time0[map0_min[j]:map0_max[j]+1]
                bar_len = len(time1)
                if bar_len < 60:
                    pass
                else:
                    get_bar(bar_a, bar_b, time1, ct0, mapid0[j], fig_num)
                    print(f'Mode {ct0}, mapid {mapid0[j]}, figure number {fig_num}: complete', dt.datetime.now().replace(microsecond=0))
                    
                    scia_filename = f'\science data_A_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    scib_filename = f'\science data_B_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    bar_a.to_csv(savepath_his+scia_filename)
                    bar_b.to_csv(savepath_his+scib_filename)
                    
                    fig_num += 1
            
    elif ct0 == 'A0':
        sci0 = sci0.iloc[:, :256]
        sci0 = sci0.fillna(0).apply(lambda x: x.astype(str).map(lambda x: int(x, base=16)))
        sci0a = sci0.iloc[:,:128].T.reset_index(drop=True).T
        sci0b = sci0.iloc[:,128:].T.reset_index(drop=True).T
        sci0a = sci0a.apply(lambda x: x.astype(int).map(lambda x: logmap[x]))
        sci0b = sci0b.apply(lambda x: x.astype(int).map(lambda x: logmap[x]))
        sci_a = pd.concat([sci_a, sci0a])
        sci_b = pd.concat([sci_b, sci0b])
        
        sci_map0 = sci_mapid[sci0.index].reset_index(drop=True)
        mapid0, map0_min, map0_max = func_dropd(sci_map0)
        time0 = time_sci[sci0.index]
        bar_a0 = sci0a.copy().reset_index(drop=True)
        bar_b0 = sci0b.copy().reset_index(drop=True)
        
        for j in np.arange(len(mapid0)):
            if mapid0[j] == '00':
                pass
            else:
                bar_a = bar_a0.loc[map0_min[j]:map0_max[j]+1, :]
                bar_b = bar_b0.loc[map0_min[j]:map0_max[j]+1, :]
                time1 = time0[map0_min[j]:map0_max[j]+1]
                bar_len = len(time1)
                if bar_len < 60:
                    pass
                else:
                    get_bar(bar_a, bar_b, time1, ct0, mapid0[j], fig_num)
                    print(f'Mode {ct0}, mapid {mapid0[j]}, figure number {fig_num}: complete', dt.datetime.now().replace(microsecond=0))                    
                    
                    scia_filename = f'\science data_A_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    scib_filename = f'\science data_B_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    bar_a.to_csv(savepath_his+scia_filename)
                    bar_b.to_csv(savepath_his+scib_filename)
                    
                    fig_num += 1
            
    elif ct0 == '40':
        sci0 = sci0.iloc[:,::2].T.reset_index(drop=True).T + sci0.iloc[:,1::2].T.reset_index(drop=True).T
        sci0 = sci0.fillna(0).apply(lambda x: x.astype(str).map(lambda x: int(x, base=16)))
        sci0a = sci0.iloc[:,:256].T.reset_index(drop=True).T
        sci0b = sci0.iloc[:,256:].T.reset_index(drop=True).T
        sci_a = pd.concat([sci_a, sci0a])
        sci_b = pd.concat([sci_b, sci0b])
        
        sci_map0 = sci_mapid[sci0.index].reset_index(drop=True)
        mapid0, map0_min, map0_max = func_dropd(sci_map0)
        time0 = time_sci[sci0.index]
        bar_a0 = sci0a.copy().reset_index(drop=True)
        bar_b0 = sci0b.copy().reset_index(drop=True)
        
        for j in np.arange(len(mapid0)):
            if mapid0[j] == '00':
                pass
            else:
                bar_a = bar_a0.loc[map0_min[j]:map0_max[j]+1, :]
                bar_b = bar_b0.loc[map0_min[j]:map0_max[j]+1, :]
                time1 = time0[map0_min[j]:map0_max[j]+1]
                bar_len = len(time1)
                if bar_len < 60:
                    pass
                else:
                    get_bar(bar_a, bar_b, time1, ct0, mapid0[j], fig_num)
                    print(f'Mode {ct0}, mapid {mapid0[j]}, figure number {fig_num}: complete', dt.datetime.now().replace(microsecond=0))
                                        
                    scia_filename = f'\science data_A_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    scib_filename = f'\science data_B_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    bar_a.to_csv(savepath_his+scia_filename)
                    bar_b.to_csv(savepath_his+scib_filename)
                    
                    fig_num += 1
        
    elif ct0 == 'E0':
        sci0 = sci0.iloc[:, :512]
        sci0 = sci0.fillna(0).apply(lambda x: x.astype(str).map(lambda x: int(x, base=16)))
        sci0a = sci0.iloc[:,:256].T.reset_index(drop=True).T
        sci0b = sci0.iloc[:,256:].T.reset_index(drop=True).T
        sci0a = sci0a.apply(lambda x: x.astype(int).map(lambda x: logmap[x]))
        sci0b = sci0b.apply(lambda x: x.astype(int).map(lambda x: logmap[x]))
        sci_a = pd.concat([sci_a, sci0a])
        sci_b = pd.concat([sci_b, sci0b])
        
        sci_map0 = sci_mapid[sci0.index].reset_index(drop=True)
        mapid0, map0_min, map0_max = func_dropd(sci_map0)
        time0 = time_sci[sci0.index]
        bar_a0 = sci0a.copy().reset_index(drop=True)
        bar_b0 = sci0b.copy().reset_index(drop=True)
        
        for j in np.arange(len(mapid0)):
            if mapid0[j] == '00':
                pass
            else:
                bar_a = bar_a0.loc[map0_min[j]:map0_max[j]+1, :]
                bar_b = bar_b0.loc[map0_min[j]:map0_max[j]+1, :]
                time1 = time0[map0_min[j]:map0_max[j]+1]
                bar_len = len(time1)
                if bar_len < 60:
                    pass
                else:
                    get_bar(bar_a, bar_b, time1, ct0, mapid0[j], fig_num)
                    print(f'Mode {ct0}, mapid {mapid0[j]}, figure number {fig_num}: complete', dt.datetime.now().replace(microsecond=0))                    
                    
                    scia_filename = f'\science data_A_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    scib_filename = f'\science data_B_separate_{ct0}_{mapid0[j]}_{fig_num}.csv'
                    bar_a.to_csv(savepath_his+scia_filename)
                    bar_b.to_csv(savepath_his+scib_filename)
                    
                    fig_num += 1
    else:
        pass


sci_a = sci_a.sort_index()
sci_b = sci_b.sort_index()
sci_bin = len(sci_a.iloc[0,:])

binname_a, binname_b = [], []
for i in np.arange(sci_bin):
    binname_a.append('A_Bin_'+str(i))
    binname_b.append('B_Bin_'+str(i))

sci_a.columns = binname_a
sci_b.columns = binname_b

sci_save = pd.concat([time_sci_iso, sci_header, sci_a, sci_b], axis=1)
sci_save.to_csv(path+'/sci_parsed.csv', index=False)

print('Science data save: complete', dt.datetime.now().replace(microsecond=0))

# shade cal.
shade_min, shade_max = [], []
for i in np.arange(pn_sci):
    sci_mode = sci_scpktif.iloc[i]
    if sci_mode == '00' or sci_mode == 'A0':
        shade_min.append(128)
        shade_max.append(256)
    elif sci_mode == '40' or sci_mode == 'E0':
        shade_min.append(256)
        shade_max.append(256)
    else:
        pass
shade_min = np.array(shade_min)
shade_max = np.array(shade_max)


#%% Noise data
noi_header = header_creation(noi, pn_noi)

noi_data0 = noi.iloc[:, 21:21+160].T.reset_index(drop=True).T
noi_data = noi_data0.iloc[:,::2].T.reset_index(drop=True).T + noi_data0.iloc[:,1::2].T.reset_index(drop=True).T
noi_data = noi_data.fillna(0).apply(lambda x: x.astype(str).map(lambda x: int(x, base=16)))

noi_cal = noi_data.diff()

for i in np.arange(pn_noi):
    for j in np.arange(len(noi_data.iloc[0,:])):
        dn0 = noi_cal.iloc[i,j]
        if dn0 >= 0:
            pass
        elif dn0 < 0:
            dn1 = 65535 + dn0
            noi_cal.iloc[i,j] = dn1
        else:
            pass
noi_num = len(noi_cal.iloc[0,:])

noi_col = []
for i in ['A', 'B']:
    for j in ['O', 'U', 'T', 'F']:
        for k in np.arange(10):
            noi_col.append(i+j+'_Ch '+str(k))

noi_cal.columns = noi_col

noi_save = pd.concat([time_noi_iso, noi_header, noi_cal], axis=1)
noi_save.to_csv(path+'/noi_parsed.csv', index=False)
print('Noise data save: complete', dt.datetime.now().replace(microsecond=0))

#%% Housekeeping data
soh_header = header_creation(soh, pn_soh)

def soh_parsed(soh):
    soh_data = pd.DataFrame(columns=['Bias Cur Monitor', 'Bias Voltage Monitor', '-5VA', '+5VA', '+5VD', 'FPGA Thermistor', '+2.5VD_(1)', '+2.5VD_(2)', 'FPGA Revision Number', 'Valid Command Counter', 'Invalid Command Counter', 'Board ID', 'Test Pulse Enable', 'Test Pulse FTUO Pattern', 'Baseline Restoration Mode', 'Detector Enable', 'Noise Measurement Enable', 'Noise Data Resolution', 'Noise Period', 'Memory Fill Address', 'LUT Checksum', 'PPS Counter', 'Event Count Number', 'Count Rate_AO', 'Count Rate_AU', 'Count Rate_AT', 'Count Rate_AF', 'Count Rate_BO', 'Count Rate_BU', 'Count Rate_BT', 'Count Rate_BF', 'Bus Timeout Count_Memory Fill Process', 'Bus Timeout Count_Telemetry Process', 'Bus Timeout Count_Event Process', 'Bus Timeout Count_Noise Measurement', 'Detector Timeout Error Count', 'Valid without Peak Anomaly Count'])
    
    soh_data.loc[:, 'Bias Cur Monitor'] = (signhex2dec(soh.iloc[:,21] + soh.iloc[:,22]) * 2.5 / 32768)
    soh_data.loc[:, 'Bias Voltage Monitor'] = (signhex2dec(soh.iloc[:,23] + soh.iloc[:,24]) * 2.5 / 32768)
    soh_data.loc[:, '-5VA'] = (signhex2dec(soh.iloc[:,25] + soh.iloc[:,26]) * 2.5 / 32768 ) * (16.65 / 6.65)
    soh_data.loc[:, '+5VA'] = (signhex2dec(soh.iloc[:,27] + soh.iloc[:,28]) * 2.5 / 32768 ) * (16.65 / 6.65)
    soh_data.loc[:, '+5VD'] = (signhex2dec(soh.iloc[:,29] + soh.iloc[:,30]) * 2.5 / 32768 ) * (16.65 / 6.65)
    
    Ther1 = (signhex2dec(soh.iloc[:,31] + soh.iloc[:,32]) * 2.5 / 32768)
    Ther1_res = 49.9 * (1/(2.5/Ther1 -1))
    
    # LSP Thermistor: 311P18-07S7R6 (NTC thermistor)
    tt_ref = np.array([-55,-54,-53,-52,-51,-50,-49,-48,-47,-46,-45,-44,-43,-42,-41,-40,-39,-38,-37,-36,-35,-34,-33,-32,-31,
                      -30,-29,-28,-27,-26,-25,-24,-23,-22,-21,-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,
                      -5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,
                      30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,
                      62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90])
    tr_ref = np.array([607.8,569.6,534.1,501,470.1,441.3,414.5,389.4,366,344.1,323.7,304.6,286.7,270,254.4,239.8,226,213.2,201.1,
              189.8,179.2,169.3,160,151.2,143,135.2,127.9,121.1,114.6,108.6,102.9,97.49,92.43,87.66,83.16,78.91,74.91,71.13,
              67.57,64.2,61.02,58.01,55.17,52.48,49.94,47.54,45.27,43.11,41.07,39.14,37.31,35.57,33.93,32.37,30.89,
              29.49,28.15,26.89,25.69,24.55,23.46,22.43,21.45,20.52,19.63,18.79,17.98,17.22,16.49,15.79,15.13,14.5,
              13.9,13.33,12.79,12.26,11.77,11.29,10.84,10.41,10,9.605,9.227,8.867,8.523,8.194,7.88,7.579,7.291,7.016,
              6.752,6.5,6.258,6.026,5.805,5.592,5.389,5.193,5.006,4.827,4.655,4.489,4.331,4.179,4.033,3.893,3.758,3.629,
              3.504,3.385,3.27,3.16,3.054,2.952,2.854,2.76,2.669,2.582,2.497,2.417,2.339,2.264,2.191,2.122,2.055,1.99,
              1.928,1.868,1.81,1.754,1.7,1.648,1.598,1.549,1.503,1.458,1.414,1.372,1.332,1.293,1.255,1.218,1.183,1.149,1.116,1.084])
    
    popt_t, pcov_t = curve_fit(fit_sh, tr_ref, tt_ref+273.15)
    perr_t = np.sqrt(np.diag(pcov_t))
    tt_fit = fit_sh(tr_ref, *popt_t) - 273.15
    
    Ther1_temp = fit_sh(Ther1_res, *popt_t) - 273.15
    soh_data.loc[:, 'FPGA Thermistor'] = Ther1_temp
    
    soh_data.loc[:, '+2.5VD_(1)'] = (signhex2dec(soh.iloc[:,33] + soh.iloc[:,34]) * 2.5 / 32768)
    soh_data.loc[:, '+2.5VD_(2)'] = (signhex2dec(soh.iloc[:,35] + soh.iloc[:,36]) * 2.5 / 32768)
    
    soh_data.loc[:, 'FPGA Revision Number'] = '0x' + soh.iloc[:,38]
    soh_data.loc[:, 'Valid Command Counter'] = '0x' + soh.iloc[:,39]
    soh_data.loc[:, 'Invalid Command Counter'] = '0x' + soh.iloc[:,40]
    
    for i in np.arange(len(soh.iloc[:,41])):
        b0 = bin(int(soh.iloc[i,41], base=16))[2:].zfill(8)
        soh_data.loc[i,'Board ID'] = '0b' + b0[2:4]
        soh_data.loc[i,'Test Pulse Enable'] = '0b' + b0[7]
    
    soh_data.loc[:, 'Test Pulse FTUO Pattern'] = '0b' + soh.iloc[:,42].apply(lambda x: bin(int(x, base=16))[2:].zfill(8))
    soh_data.loc[:, 'Baseline Restoration Mode'] = '0x' + soh.iloc[:,43]
    soh_data.loc[:, 'Detector Enable'] = '0b' + soh.iloc[:,44].apply(lambda x: bin(int(x, base=16))[2:].zfill(8))
    
    for i in np.arange(len(soh.iloc[:,45])):
        b0 = bin(int(soh.iloc[i,45], base=16))[2:].zfill(8)
        soh_data.loc[i,'Noise Measurement Enable'] = '0b' + b0[4]
        soh_data.loc[i,'Noise Data Resolution'] = '0b' + b0[5:]
    
    soh_data.loc[:, 'Noise Period'] = '0x' + soh.iloc[:,46]
    soh_data.loc[:, 'Memory Fill Address'] = '0x' + soh.iloc[:,47] + soh.iloc[:,48]
    soh_data.loc[:, 'LUT Checksum'] = '0x' + soh.iloc[:,49]
    soh_data.loc[:, 'PPS Counter'] = '0x' + soh.iloc[:,50]
    soh_data.loc[:, 'Event Count Number'] = '0x' + soh.iloc[:,51] + soh.iloc[:,52]
    
    soh_hkprate0 = soh.iloc[:, 53:53+16]
    soh_hkprate = soh_hkprate0.iloc[:,::2].T.reset_index(drop=True).T + soh_hkprate0.iloc[:,1::2].T.reset_index(drop=True).T
    soh_hkprate = soh_hkprate.fillna(0).apply(lambda x: x.astype(str).map(lambda x: int(x, base=16)))
    
    soh_data.loc[:, 'Count Rate_AO'] = soh_hkprate.iloc[:,0]
    soh_data.loc[:, 'Count Rate_AU'] = soh_hkprate.iloc[:,1]
    soh_data.loc[:, 'Count Rate_AT'] = soh_hkprate.iloc[:,2]
    soh_data.loc[:, 'Count Rate_AF'] = soh_hkprate.iloc[:,3]
    soh_data.loc[:, 'Count Rate_BO'] = soh_hkprate.iloc[:,4]
    soh_data.loc[:, 'Count Rate_BU'] = soh_hkprate.iloc[:,5]
    soh_data.loc[:, 'Count Rate_BT'] = soh_hkprate.iloc[:,6]
    soh_data.loc[:, 'Count Rate_BF'] = soh_hkprate.iloc[:,7]
    
    for i in np.arange(len(soh.iloc[:,69])):
        b0 = bin(int(soh.iloc[i,69], base=16))[2:].zfill(8)
        soh_data.loc[i,'Bus Timeout Count_Memory Fill Process'] = '0b' + b0[:4]
        soh_data.loc[i,'Bus Timeout Count_Telemetry Process'] = '0b' + b0[4:]
    
    for i in np.arange(len(soh.iloc[:,70])):
        b0 = bin(int(soh.iloc[i,70], base=16))[2:].zfill(8)
        soh_data.loc[i,'Bus Timeout Count_Event Process'] = '0b' + b0[:4]
        soh_data.loc[i,'Bus Timeout Count_Noise Measurement'] = '0b' + b0[4:]
    
    soh_data.loc[:, 'Detector Timeout Error Count'] = '0x' + soh.iloc[:,71]
    soh_data.loc[:, 'Valid without Peak Anomaly Count'] = '0x' + soh.iloc[:,72]
    return soh_data

soh_data = soh_parsed(soh)

soh_save = pd.concat([time_soh_iso, soh_header, soh_data], axis=1)
soh_save.to_csv(path+'/soh_parsed.csv', index=False)
print('Housekeeping data save: complete', dt.datetime.now().replace(microsecond=0))

#%% Plot

# label size
xl = 16
yl = 16
# Tick label size
xtl = 14
ytl = 14
ytl2 = 14
# Tck Mark Length and Width
w1= 1.00
l1 = 10.0
w2 = 0.75
l2= 5.0  

# Tick mark interval
major_locator = mdates.AutoDateLocator()
minor_locator = mdates.AutoDateLocator(maxticks=30)
xformatter = mdates.DateFormatter('%b-%d\n%H:%M:%S')
xformatter1 = mdates.DateFormatter('%M')
mpl.style.use('classic')
plt.rcParams['font.family'] = 'Times New Roman'
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

plt.ioff()
fig = plt.figure(num=1, figsize=(16,12))
gs = gridspec.GridSpec(7, 1, height_ratios=(1,1,1,1,1,1,1), hspace=0.2) 

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])
ax4 = fig.add_subplot(gs[3])
ax5 = fig.add_subplot(gs[4])
ax6 = fig.add_subplot(gs[5])
ax7 = fig.add_subplot(gs[6])


#fig.suptitle('Power-Temperature', color='r',fontsize=40, fontweight='bold', y=0.95)    
ax1.set_title('Test time: '+st_str+' - '+et_str+' ('+t_delta+' s)', loc='right')
ax1.plot(time_soh, soh_data.loc[:, 'Bias Cur Monitor'])
ax1.set_ylabel('CurMon', size=yl, fontweight='bold', labelpad=10)
ax1.grid(True, which="both")
#ax1.set_ylim([-2.5, 0])
ax1.set_xlim([start_time, end_time])    
ax1.xaxis.set_major_locator(major_locator)
ax1.xaxis.set_minor_locator(minor_locator)
ax1.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax1.tick_params(which='minor', width=w2, length=l2, direction='in')
#ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
plt.setp(ax1.get_xticklabels(),visible=False)    

ax2.plot(time_soh, soh_data.loc[:, 'Bias Voltage Monitor'])
ax2.set_ylabel('BiasMon', size=yl, fontweight='bold', labelpad=10)
ax2.grid(True, which="both")
#ax2.set_ylim([-5, 0])
ax2.set_xlim([start_time, end_time])    
ax2.xaxis.set_major_locator(major_locator)
ax2.xaxis.set_minor_locator(minor_locator)
ax2.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax2.tick_params(which='minor', width=w2, length=l2, direction='in')
#ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax2.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
plt.setp(ax2.get_xticklabels(),visible=False)    

ax3.plot(time_soh, soh_data.loc[:, '-5VA'])
ax3.set_ylabel('-5VA', size=yl, fontweight='bold', labelpad=10)
ax3.grid(True, which="both")
ax3.set_xlim([start_time, end_time])    
ax3.xaxis.set_major_locator(major_locator)
ax3.xaxis.set_minor_locator(minor_locator)
ax3.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax3.tick_params(which='minor', width=w2, length=l2, direction='in')
#ax3.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax3.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
plt.setp(ax3.get_xticklabels(),visible=False)    

ax4.plot(time_soh, soh_data.loc[:, '+5VA'])
ax4.set_ylabel('+5VA', size=yl, fontweight='bold', labelpad=10)
ax4.grid(True, which="both")
ax4.set_xlim([start_time, end_time])    
ax4.xaxis.set_major_locator(major_locator)
ax4.xaxis.set_minor_locator(minor_locator)
ax4.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax4.tick_params(which='minor', width=w2, length=l2, direction='in')
#ax4.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax4.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
plt.setp(ax4.get_xticklabels(),visible=False)

ax5.plot(time_soh, soh_data.loc[:, '+5VD'])
ax5.set_ylabel('+5VD', size=yl, fontweight='bold', labelpad=10)
ax5.grid(True, which="both")
ax5.set_xlim([start_time, end_time])    
ax5.xaxis.set_major_locator(major_locator)
ax5.xaxis.set_minor_locator(minor_locator)
ax5.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax5.tick_params(which='minor', width=w2, length=l2, direction='in')
#ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
#ax5.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
plt.setp(ax5.get_xticklabels(),visible=False)

ax6.plot(time_soh, soh_data.loc[:, 'FPGA Thermistor'])
ax6.set_ylabel('Temp., \u2103', size=yl, fontweight='bold', labelpad=10)
ax6.grid(True, which="both")
ax6.set_xlim([start_time, end_time])    
ax6.xaxis.set_major_locator(major_locator)
ax6.xaxis.set_minor_locator(minor_locator)
ax6.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax6.tick_params(which='minor', width=w2, length=l2, direction='in')
#ax6.yaxis.set_major_locator(ticker.MultipleLocator(1))
#ax6.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
plt.setp(ax6.get_xticklabels(),visible=False)

ax7.plot(time_soh, soh_data.loc[:, '+2.5VD_(1)'], label='+2.5VD_1')
ax7.plot(time_soh, soh_data.loc[:, '+2.5VD_(2)'], label='+2.5VD_2')
ax7.legend(fontsize=12, ncol=2, framealpha=0.5)
ax7.set_xlim([start_time, end_time])
ax7.set_ylabel('+2.5VD', size=yl, fontweight='bold', labelpad=10)
ax7.set_xlabel('Time, KST', size=xl, fontweight='bold')
ax7.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax7.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
ax7.grid(True, which="both")
ax7.xaxis.set_major_locator(major_locator)
ax7.xaxis.set_minor_locator(minor_locator)
ax7.xaxis.set_major_formatter(xformatter)
#ax7.xaxis.set_minor_formatter(xformatter1)
ax7.xaxis.set_tick_params(which='major', pad=10)
plt.setp(ax7.get_xticklabels(),visible=True)

#plt.tight_layout()
fig.align_labels()
plt.savefig(path+'/plot_soh_power-temp.png', dpi=300, bbox_inches='tight')
plt.clf()
gc.collect()

print('soh_power-temp plot: complete', dt.datetime.now().replace(microsecond=0))

soh_tppa = soh_data.loc[:,'Test Pulse FTUO Pattern'].str.slice(2,6)
soh_tppa_f = pd.to_numeric(soh_tppa.str.slice(0,1))
soh_tppa_t = pd.to_numeric(soh_tppa.str.slice(1,2))
soh_tppa_u = pd.to_numeric(soh_tppa.str.slice(2,3))
soh_tppa_o = pd.to_numeric(soh_tppa.str.slice(3,4))
soh_tppa = pd.concat([soh_tppa_f, soh_tppa_t, soh_tppa_u, soh_tppa_o], axis=1)
soh_rate = soh_data.loc[:,'Count Rate_AO':'Count Rate_BF']

# label size
xl = 18
yl = 18
# Tick label size
xtl = 16
ytl = 16
# Tck Mark Length and Width
w1= 1.00
l1 = 10.0
w2 = 0.75
l2= 5.0  

# Tick mark interval
major_locator = mdates.AutoDateLocator()
minor_locator = mdates.AutoDateLocator(maxticks=30)
xformatter = mdates.DateFormatter('%b-%d\n%H:%M:%S')
xformatter1 = mdates.DateFormatter('%M')
mpl.style.use('classic')
plt.rcParams['font.family'] = 'Times New Roman'
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

plt.ioff()
fig = plt.figure(num=2, figsize=(16,12))
gs = gridspec.GridSpec(3, 1, height_ratios=(1,3,3), hspace=0.1) 

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])

#fig.suptitle('LUSEM Plot Example', color='k',fontsize=40, fontweight='bold', y=0.95)    

ax1.set_title('Test time: '+st_str+' - '+et_str+' ('+t_delta+' s)', loc='right')
plt1 = ax1.pcolor(time_soh, np.arange(4), soh_tppa.T, cmap='binary', shading='auto')
#ax1.plot(hkp_time, CurMon)
ax1.set_ylabel('TP Pattern', size=yl, fontweight='bold', labelpad=10)

ax1.set_ylim([-0.5, 3.5])
ax1.set_yticks(ticks=[0,1,2,3], labels=['F', 'T', 'U', 'O'])
ax1.set_xlim([start_time, end_time])    
ax1.xaxis.set_major_locator(major_locator)
ax1.xaxis.set_minor_locator(minor_locator)
ax1.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
#ax1.tick_params(which='minor', width=w2, length=l2, direction='in')
ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
ax1.grid(True, which="minor")
plt.setp(ax1.get_xticklabels(),visible=False)    

ax2.plot(time_soh, soh_rate.iloc[:,4], color='r', ls='--', lw=4, label='T2_O', alpha=0.6)
ax2.plot(time_soh, soh_rate.iloc[:,5], color='g', ls='--', lw=4, label='T2_U', alpha=0.6)
ax2.plot(time_soh, soh_rate.iloc[:,6], color='b', ls='--', lw=4, label='T2_T', alpha=0.6)
ax2.plot(time_soh, soh_rate.iloc[:,7], color='k', ls='--', lw=4, label='T2_F', alpha=0.6)
ax2.legend(fontsize=14, ncol=4)
ax2.set_yscale('log')
ax2.set_xlim([start_time, end_time])
ax2.set_ylabel('Telescope-B\nCount Rate, #/s', size=yl, fontweight='bold', labelpad=10)
#ax2.set_xlabel('Time, KST', size=xl, fontweight='bold')
ax2.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax2.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
ax2.grid(True, which="both")
ax2.xaxis.set_major_locator(major_locator)
ax2.xaxis.set_minor_locator(minor_locator)
plt.setp(ax2.get_xticklabels(),visible=False)


ax3.plot(time_soh, soh_rate.iloc[:,0], color='r', ls='--', lw=4, label='T1_O', alpha=0.6)
ax3.plot(time_soh, soh_rate.iloc[:,1], color='g', ls='--', lw=4, label='T1_U', alpha=0.6)
ax3.plot(time_soh, soh_rate.iloc[:,2], color='b', ls='--', lw=4, label='T1_T', alpha=0.6)
ax3.plot(time_soh, soh_rate.iloc[:,3], color='k', ls='--', lw=4, label='T1_F', alpha=0.6)
ax3.legend(fontsize=14, ncol=4)
ax3.set_yscale('log')
ax3.set_xlim([start_time, end_time])
ax3.set_ylabel('Telescope-A\nCount Rate, #/s', size=yl, fontweight='bold', labelpad=10)
ax3.set_xlabel('Time, KST', size=xl, fontweight='bold')
ax3.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax3.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
ax3.grid(True, which="both")
ax3.xaxis.set_major_locator(major_locator)
ax3.xaxis.set_minor_locator(minor_locator)
ax3.xaxis.set_major_formatter(xformatter)
#ax2.xaxis.set_minor_formatter(xformatter1)
ax3.xaxis.set_tick_params(which='major', pad=10)
plt.setp(ax3.get_xticklabels(),visible=True)

#plt.tight_layout()
#fig.align_ylabels([ax1,ax2,ax5,ax6,ax7])
fig.align_labels()
plt.savefig(path+'/plot_soh_count rate-TP.png', dpi=300, bbox_inches='tight')
#plt.show()
plt.clf()
gc.collect()

print('soh_count rate & test pulse pattern plot: complete', dt.datetime.now().replace(microsecond=0))

# label size
xl = 16
yl = 16
# Tick label size
xtl = 12
ytl = 12
# Tck Mark Length and Width
w1= 1.00
l1 = 10.0
w2 = 0.75
l2= 5.0  

# Tick mark interval
major_locator = mdates.AutoDateLocator()
minor_locator = mdates.AutoDateLocator(maxticks=30)
xformatter = mdates.DateFormatter('%b-%d\n%H:%M:%S')
xformatter1 = mdates.DateFormatter('%M')
mpl.style.use('classic')
plt.rcParams['font.family'] = 'Times New Roman'
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

plt.ioff()
fig = plt.figure(num=3, figsize=(16,12))
gs = gridspec.GridSpec(6, 1, height_ratios=(0.3,0.3,1,4,4,4), hspace=0.1) 

# spectrogram axis
ax_sci = fig.add_subplot(gs[3:5])
ax_sci.spines['top'].set_color('none')
ax_sci.spines['bottom'].set_color('none')
ax_sci.spines['left'].set_color('none')
ax_sci.spines['right'].set_color('none')
ax_sci.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])
ax4 = fig.add_subplot(gs[3])
ax5 = fig.add_subplot(gs[4])
ax6 = fig.add_subplot(gs[5])

#fig.suptitle('LUSEM Plot Example', color='k',fontsize=40, fontweight='bold', y=0.95)    

ax1.set_title('Test time: '+st_str+' - '+et_str+' ('+t_delta+' s)', loc='right')

for i in np.arange(len(mapid_min)):
    ax1.axvspan(time_sci[mapid_min[i]], time_sci[mapid_max[i]], alpha=0.2, fc=np.random.rand(3,))
    m_delta0 = (time_sci[mapid_max[i]] - time_sci[mapid_min[i]]).seconds / 2
    m_delta1 = dt.timedelta(seconds = m_delta0)
    ax1.text(time_sci[mapid_min[i]]+m_delta1, 0.5, mapid[i], weight='bold', ha='center', va='center')

ax1.set_xlim([start_time, end_time])    
ax1.tick_params(which='major', bottom=False, top=False, left=False, right=False)
#ax1.tick_params(which='minor', width=w2, length=l2, direction='in')
plt.setp(ax1.get_xticklabels(),visible=False)    
plt.setp(ax1.get_yticklabels(),visible=False)    

for i in np.arange(len(comp_min)):
    ax2.axvspan(time_sci[comp_min[i]], time_sci[comp_max[i]], alpha=0.2, fc=np.random.rand(3,))
    m_delta0 = (time_sci[comp_max[i]] - time_sci[comp_min[i]]).seconds / 2
    m_delta1 = dt.timedelta(seconds = m_delta0)
    ax2.text(time_sci[comp_min[i]]+m_delta1, 0.5, comp_type[i], weight='bold', ha='center', va='center')

ax2.set_xlim([start_time, end_time])    
ax2.tick_params(which='major', bottom=False, top=False, left=False, right=False)
#ax1.tick_params(which='minor', width=w2, length=l2, direction='in')
plt.setp(ax2.get_xticklabels(),visible=False)    
plt.setp(ax2.get_yticklabels(),visible=False)    

hkp_color = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:cyan']
for i in np.arange(len(soh_rate.iloc[0,:])):
    if i < 4:
        ax3.plot(time_soh, soh_rate.iloc[:,i], marker='+', markevery=20, ms=4, label=soh_rate.columns[i], color=hkp_color[i])
    elif i >= 4:
        ax3.plot(time_soh, soh_rate.iloc[:,i], marker='x', markevery=20, ms=4, label=soh_rate.columns[i], color=hkp_color[i])
    else:
        pass
ax3.legend(fontsize=8, framealpha=0.5, bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0., ncol=2)
ax3.set_ylabel('HKP\nRATES', size=yl, fontweight='bold', labelpad=10)
ax3.set_yscale('log')
ax3.set_xlim([start_time, end_time])    
ax3.xaxis.set_major_locator(major_locator)
ax3.xaxis.set_minor_locator(minor_locator)
ax3.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax3.tick_params(which='minor', width=w2, length=l2, direction='in')
plt.setp(ax3.get_xticklabels(),visible=False)

sci_bin = len(sci_a.iloc[0,:])
cbar_min, cbar_max = 1, 1e3

plt1 = ax4.pcolormesh(time_sci, np.arange(sci_bin,sci_bin*2,1), sci_b.T, cmap='jet', norm=colors.LogNorm(vmin=cbar_min, vmax=cbar_max), shading='auto')
ax4.fill_between(time_sci, shade_max+256, shade_min+256, color='gray', alpha=0.1, step='mid', hatch='/', ec=None)
box = ax_sci.get_position()
axColor = plt.axes([box.x0 + box.width * 1.01, box.y0, 0.01, box.height])
cbar1 = fig.colorbar(plt1, cax=axColor, orientation="vertical")
cbar1.ax.set_ylabel(ylabel='Counts', size=xl, weight='bold')
cbar1.ax.tick_params(which='major', labelsize=xtl, direction='in', width=w1, length=l1)
cbar1.ax.tick_params(which='minor', width=w2, length=l2, direction='in')
ax4.set_ylabel('SCI DATA\nTELESCOPE-B', size=yl, fontweight='bold', labelpad=10)
ax4.set_ylim([sci_bin,sci_bin*2])
ax4.set_xlim([start_time, end_time])
ax4.xaxis.set_major_locator(major_locator)
ax4.xaxis.set_minor_locator(minor_locator)
ax4.yaxis.set_major_locator(ticker.MultipleLocator(32))
ax4.yaxis.set_minor_locator(ticker.MultipleLocator(8))
ax4.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax4.tick_params(which='minor', width=w2, length=l2, direction='in')
plt.setp(ax4.get_xticklabels(),visible=False)

plt2 = ax5.pcolormesh(time_sci, np.arange(0,sci_bin,1), sci_a.T, cmap='jet', norm=colors.LogNorm(vmin=cbar_min, vmax=cbar_max), shading='auto')
ax5.fill_between(time_sci, shade_max, shade_min, color='gray', alpha=0.1, step='mid', hatch='/', ec=None)
ax5.set_ylabel('SCI DATA\nTELESCOPE-A', size=yl, fontweight='bold', labelpad=10)
ax5.set_ylim([0,sci_bin])
ax5.set_xlim([start_time, end_time])
ax5.xaxis.set_major_locator(major_locator)
ax5.xaxis.set_minor_locator(minor_locator)
ax5.yaxis.set_major_locator(ticker.MultipleLocator(32))
ax5.yaxis.set_minor_locator(ticker.MultipleLocator(8))
ax5.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax5.tick_params(which='minor', width=w2, length=l2, direction='in')
plt.setp(ax5.get_xticklabels(),visible=False)

plt3 = ax6.pcolormesh(time_noi, np.arange(0,80,1), noi_cal.T, cmap='jet', norm=colors.LogNorm(vmin=1, vmax=1e3), shading='auto')
box = ax6.get_position()
axColor = plt.axes([box.x0 + box.width * 1.01, box.y0, 0.01, box.height])
cbar1 = fig.colorbar(plt3, cax=axColor, orientation="vertical")
cbar1.ax.set_ylabel(ylabel='Counts', size=xl, weight='bold')
cbar1.ax.tick_params(which='major', labelsize=xtl, direction='in', width=w1, length=l1)
cbar1.ax.tick_params(which='minor', width=w2, length=l2, direction='in')
ax6.set_ylim([0,80])
ax6.set_xlim([start_time, end_time])
ax6.set_ylabel('NOISE DATA', size=yl, fontweight='bold', labelpad=10)
ax6.set_xlabel('Time, KST', size=xl, fontweight='bold')
ax6.tick_params(which='major', labelsize=ytl, width=w1, length=l1, direction='in')
ax6.tick_params(which='minor', labelsize=12, width=w2, length=l2, direction='in')
#ax7.grid(True, which="both")
ax6.xaxis.set_major_locator(major_locator)
ax6.xaxis.set_minor_locator(minor_locator)
ax6.xaxis.set_major_formatter(xformatter)
#ax7.xaxis.set_minor_formatter(xformatter1)
ax6.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax6.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax6.xaxis.set_tick_params(which='major', pad=10)
plt.setp(ax6.get_xticklabels(),visible=True)

#plt.tight_layout()
#fig.align_ylabels([ax1,ax2,ax5,ax6,ax7])
fig.align_labels()
plt.savefig(path+'/plot_sci_spectrogram.png', dpi=300, bbox_inches='tight')
#plt.show()
plt.clf()
gc.collect()

print('sci_spectrogram plot: complete', dt.datetime.now().replace(microsecond=0))

import winsound
duration = 1000
freq = 500
winsound.Beep(freq, duration)

print('processing time: ', time.time() - start_codetime)