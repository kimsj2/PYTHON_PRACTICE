# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 16:01:55 2023

@author: SSIL_B104_1
"""

import socket
import binascii
import time
import datetime as dt
import numpy as np
import re
import os
import math
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd


# /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
filepath = r"C:\Users\kimsj\Documents\data\LUSEM_GUI_TEST\GUI_TEST_7(20230728_TAP_HEX)\use_data"
filename = "sci_simple.txt"

soh_data = []
sci_data = []
dum_data = []
noi_data = []
sci_flag=""


ts = dt.datetime.now()
te = ts + dt.timedelta(seconds=3600)

    
# def hex_to_decimal(sci_data,data,num):
#     try:
#         decimal_values = [int(data[i:i+num], 16) for i in range(0, len(data), num)]
#         return decimal_values
#     except ValueError:
#         return None
    
def sci_hex_dec(data):
    sci_flag = data[26:28]
    if sci_flag=='40': # compression (x), extension (o), 2 * 512 = 1024 bytes
        decimal_values = list(int(data[42:42+2048][i:i+4], 16) for i in range(0, len(data[42:42+2048]), 4))
        sci_data.append(decimal_values)
    elif sci_flag=='00': # compression (x), extension (x), 2 * 256 = 512 bytes
        decimal_values = list(int(data[42:42+1024][i:i+4], 16) for i in range(0, len(data[42:42+1024]), 4))
        sci_data.append(decimal_values)
    elif sci_flag=='e0': # compression (o), extension (o), 1 * 512 = 512 bytes
        decimal_values = list(int(data[42:42+1024][i:i+2], 2) for i in range(0, len(data[42:42+1024]), 2))
        sci_data.append(decimal_values)
    elif sci_flag=='a0': # compression(o), extension (x), 1* 256 = 256 bytes
        decimal_values = list(int(data[42:42+512][i:i+2], 2) for i in range(0, len(data[42:42+512]), 2))
        sci_data.append(decimal_values)
    else:
        pass # nan list?

t1 = dt.datetime.now()

with open(filepath + '\\'+filename, 'r') as f:
    while True:
        instant_data = f.readline()
        if not instant_data:  # 파일의 끝에 도달하면 루프를 종료
           break
        sci_hex_dec(instant_data)

total_t = dt.datetime.now()
final_t = total_t - t1

with open(filepath + '\\'+'sci_test.txt','w') as s:
    for i in range(len(sci_data)):
        s.write(str(sci_data[i]))
        s.write('\n')

print(final_t.total_seconds())


# 기존 hex_to_decimal data 불러와서 txt로 저장
sci_data_ori = pd.read_excel(r'C:\Users\kimsj\Documents\data\LUSEM_GUI_TEST\GUI_TEST_7(20230728_TAP_HEX)\use_data\50_sci.xlsx')
sci_data_ori_list = sci_data_ori.values.tolist()

with open(filepath + '\\'+'sci_test_ori.txt','w') as s:
    for i in range(len(sci_data_ori_list)):
        s.write(str(sci_data_ori_list[i]))
        s.write('\n')
    
dt=0.0001
w=2
t=np.linspace(0,5,math.ceil(5/dt))
A=20*(np.sin(3 * np.pi * t))

plt.specgram(A,Fs=1)
plt.show() 



