# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 16:01:55 2023

@author: SSIL_B104_1
"""

import socket
import binascii
import time
from datetime import datetime
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import textwrap
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as colors


# /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
filepath = r"C:\Users\kimsj\Documents\data\LUSEM_GUI_TEST\GUI_TEST_8(20230801_spectrogram)"
filename = "sci_1800.txt"

soh_data = []
sci_data = []
dum_data = []
noi_data = []
sci_flag=""
sci_time= []
ts = dt.datetime.now()
te = ts + dt.timedelta(seconds=3600)

def sci_hex_dec(data):
    time_decimal = (dt.datetime(2001,1,1,9)+dt.timedelta(seconds=(int(data[7]+data[8]+data[9]+data[10], 16)))).isoformat(timespec='seconds')
    sci_time.append(time_decimal)
    sci_flag = data[13]
    if sci_flag=='40': # compression (x), extension (o), 2 * 512 = 1024 bytes
        decimal_values = list(int(data[21:21+1024][i]+data[21:21+1024][i+1], 16) for i in range(0, len(data[21:21+1024]), 2))
        sci_data.append(decimal_values)
    elif sci_flag=='00': # compression (x), extension (x), 2 * 256 = 512 bytes
        decimal_values = list(int(data[21:21+512][i][0]+data[21:21+512][i+1][0], 16) for i in range(0, len(data[21:21+512]), 2))
        sci_data.append(decimal_values)
    elif sci_flag=='e0': # compression (o), extension (o), 1 * 512 = 512 bytes
        decimal_values = list(int(data[21:21+512][i][0], 16) for i in range(0, len(data[21:21+512]), 1))
        sci_data.append(decimal_values)
    elif sci_flag=='a0': # compression(o), extension (x), 1* 256 = 256 bytes
        decimal_values = list(int(data[21:21+256][i][0], 16) for i in range(0, len(data[21:21+256]), 1))
        sci_data.append(decimal_values)
    else:
        pass # nan list?

# =============================================================================
# def time_cal(met):
#     time_iso = []
#     packet_num = len(met)
#     for i in np.arange(packet_num):
#         dt0 = int(met.iloc[i], 16)
#         dt1 = dt.datetime(2001,1,1,9) + dt.timedelta(seconds=(dt0))
#         time_iso.append(dt1.isoformat(timespec='seconds'))
#     time_ut = pd.to_datetime(time_iso)
#     time_iso = pd.DataFrame(time_iso, columns=['Time'])
#     return time_ut, time_iso
# 
# =============================================================================
t1 = dt.datetime.now()
# 데이터 읽기
data = np.loadtxt(filepath + '\\'+filename,dtype = str,delimiter="\t")

for i in range(len(data)):
    sci_hex_dec(data[i])

# numpy array 변환




# Plot the pcolormesh using combined_data

def sci_plot(sci_time,bins,sci_data):
    sci_data = np.array(sci_data)
    sci_time = pd.to_datetime(np.array(sci_time))
    flg, ax = plt.subplots()
    X, Y = np.meshgrid(sci_time, np.arange(0,bins))
    pcm = ax.pcolormesh(X,Y, sci_data.T, cmap='jet',shading='auto', norm=colors.LogNorm(vmin=1, vmax=1e3))
    plt.colorbar(pcm)
    plt.show()


total_t = dt.datetime.now()
final_t = total_t - t1
print(final_t.total_seconds())



