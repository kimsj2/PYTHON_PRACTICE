# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:50:05 2023

@author: SSIL_B104_1
"""

import socket
import binascii
import time
import datetime as dt
import numpy as np
import pandas as pd
import textwrap
import matplotlib.colors as colors
import matplotlib.pyplot as plt 
import gc
from collections import deque

try:
    pass
except:
    socket.close()

server_ip = '192.168.1.120'  # 위에서 설정한 서버 ip
server_port = 4040 # 위에서 설정한 서버 포트번호

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

# /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
start = time.perf_counter()
filepath = r"C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_9(20230803_CASE_2_A)\deque"
filename = "total.txt"

soh_data = deque([])
sci_data = deque([])
dum_data = deque([])
noi_data = deque([])

sci_time = deque([])


soh_left = []
sci_left = []
noi_left = []
dum_left = []
sci_time_left = []


    

d0 = ""

start_time = ""
end_time  = ""

ts = dt.datetime.now()
te = ts + dt.timedelta(seconds=3600)


def sci_hex_dec(data):
    time_decimal = (dt.datetime(2001,1,1,9)+dt.timedelta(seconds=(int(data[6]+data[7]+data[8]+data[9], 16)))).isoformat(timespec='seconds')
    if len(sci_time) ==600:
        time_temp = sci_time.popleft()
        sci_time_left.append(time_temp)
        sci_time.append(time_decimal)
    else:
        sci_time.append(time_decimal)
        
    sci_flag = data[12]
    if sci_flag=='40': # compression (x), extension (o), 2 * 512 = 1024 bytes
        decimal_values = list(int(data[20:20+1024][i]+data[20:20+1024][i+1], 16) for i in range(0, len(data[20:20+1024]), 2))
        if (len(sci_data) == 600):
            sci_temp = sci_data.popleft()
            sci_left.append(sci_temp)
            sci_data.append(decimal_values)
        else:
            sci_data.append(decimal_values)
                
    elif sci_flag=='00': # compression (x), extension (x), 2 * 256 = 512 bytes
        decimal_values = list(int(data[20:20+512][i][0]+data[20:20+512][i+1][0], 16) for i in range(0, len(data[20:20+512]), 2))
        if (len(sci_data) == 600):
            sci_temp = sci_data.popleft()
            sci_left.append(sci_temp)
            sci_data.append(decimal_values)
        else:
            sci_data.append(decimal_values)
    elif sci_flag=='e0': # compression (o), extension (o), 1 * 512 = 512 bytes
        decimal_values = list(int(data[20:20+512][i][0], 16) for i in range(0, len(data[20:20+512]), 1))
        if (len(sci_data) == 600):
            sci_temp = sci_data.popleft()
            sci_left.append(sci_temp)
            sci_data.append(decimal_values)
        else:
            sci_data.append(decimal_values)
    elif sci_flag=='a0': # compression(o), extension (x), 1* 256 = 256 bytes
        decimal_values = list(int(data[20:20+256][i][0], 16) for i in range(0, len(data[20:20+256]), 1))
        if (len(sci_data) == 600):
            sci_temp = sci_data.popleft()
            sci_left.append(sci_temp)
            sci_data.append(decimal_values)
        else:
            sci_data.append(decimal_values)
    else:
        pass # nan list?


def sci_spectrogram_plot(ax, sci_time,sci_data,bins): # ax / list / int / list / pd.timestamp / pd.timestamp   

    
    # t_slic_end = dt.datetime.now()

    sci_time = pd.to_datetime(sci_time)    
    X, Y = np.meshgrid(sci_time, np.arange(0,bins))
    
    pcm = ax.pcolormesh(X,Y, np.array(sci_data).T, cmap='jet',shading='auto', norm=colors.LogNorm(vmin=1, vmax=1e3))
    cbar = plt.colorbar(pcm)
    cbar.set_label('Count rates')

    gc.collect()
    ax.remove()
    
def sci_bar_plot(ax,bin_, sci_data):
    sci_data = np.array(sci_data)
    sci_data_sum = sci_data.sum(axis=0)
    ax2 = ax[1]
    ax2.set_yscale('log')
    ax2.bar(np.arange(1,len(sci_data_sum)+1),sci_data_sum)


i = 0    #interval count
t_slic_end = ''
t_slic_start = ''

while ts < te:
    data = socket.recv(4096)
    d1 = binascii.hexlify(data).decode('utf-8')
    d0 += d1
    if (len(d0)>2000):
        
        t_start = dt.datetime.now()
        
        with open(filepath +'\\'+filename,'a') as f, open(filepath +'\\'+'soh.txt','a') as soh, open(filepath +'\\'+'sci.txt','a') as sci, open(filepath +'\\'+'noi.txt','a') as noi, open(filepath +'\\'+'dum.txt','a') as dum:
            f.write('\t'.join(textwrap.wrap(d0, width=2)))
            f.write('\n')
            num_hex_data = np.array(d0.split('a82900'))
                            
            if num_hex_data[0]=="":
                num_hex_data = num_hex_data[1:]
                
            print(len(num_hex_data))
                            
            for x in num_hex_data:
                if x[:6]=='c30026' and len(x[6:])==152: # soh (76 bytes)
                    soh.write('a5\t')
                    soh.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                    soh.write('\t55\tde\tad\tbf\t5a\n')
                    
                    if (len(soh_data) == 600):
                        soh_temp = soh_data.popleft()
                        soh_left.append(soh_temp)
                        soh_data.append('a5'+x[6:]+'55deadbf5a')
                    else:
                        soh_data.append('a5'+x[6:]+'55deadbf5a')
                        
                    
                elif x[:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                    noi.write('a5\t')
                    noi.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                    noi.write('\t55\tde\tad\tbf\t5a\n')
                    noi_data.append('a5'+x[6:]+'55deadbf5a')
                    
                    if (len(noi_data) == 600):
                        noi_temp = noi_data.popleft()
                        noi_left.append(noi_temp)
                        noi_data.append('a5'+x[6:]+'55deadbf5a')
                    else:
                        noi_data.append('a5'+x[6:]+'55deadbf5a')
                    
                elif x[:4] == 'c304': # dum
                    dum.write('a5\t')
                    dum.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                    dum.write('\t55\tde\tad\tbf\t5a\n')
                    
                    
                    if (len(dum_data) == 600):
                        dum_temp = dum_data.popleft()
                        dum_left.append(dum_temp)
                        dum_data.append('a5'+x[6:]+'55deadbf5a')
                    else:
                        dum_data.append('a5'+x[6:]+'55deadbf5a')
                    
                elif x[:6] == 'c3008a' and len(x[6:]) == 552: # sci (256 bytes)
                    sci.write('a5\t')
                    sci_list = textwrap.wrap(x[6:], width=2)
                    sci.write('\t'.join(sci_list))
                    sci.write('\t55\tde\tad\tbf\t5a\n')
                    t_slic_start = dt.datetime.now()
                    sci_hex_dec(sci_list)
                    t_slic_end = dt.datetime.now()
                    
                   
                    
                elif x[:6] == 'c3010a' and len(x[6:]) == 1064 :# sci (512 bytes)
                    sci.write('a5\t')
                    sci_list = textwrap.wrap(x[6:], width=2)
                    sci.write('\t'.join(sci_list))
                    sci.write('\t55\tde\tad\tbf\t5a\n')
                    t_slic_start = dt.datetime.now()
                    sci_hex_dec(sci_list)
                    t_slic_end = dt.datetime.now()
                    
                                       
                    
                elif x[:6] == 'c3020a' and len(x[6:]) == 2088: # sci (1024 bytes)
                    sci.write('a5\t')
                    sci_list = textwrap.wrap(x[6:], width=2)
                    sci.write('\t'.join(sci_list))
                    sci.write('\t55\tde\tad\tbf\t5a\n')
                    t_slic_start = dt.datetime.now()
                    sci_hex_dec(sci_list)
                    t_slic_end = dt.datetime.now()
                    
                    
            if num_hex_data[-1][:6]=='c30026' and len(x[6:])==152: # soh (76 bytes)
                d0 = ""
            elif num_hex_data[-1][:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                d0 = ""
            elif num_hex_data[-1][:4] == 'c304': # dum
                d0 = ""
            elif num_hex_data[-1][:6] == 'c3008a' and len(x[6:]) == 552: # sci (256 bytes)
                d0 = ""
            elif num_hex_data[-1][:6] == 'c3010a' and len(x[6:]) == 1064 :# sci (512 bytes)
                d0 = ""
            elif num_hex_data[-1][:6] == 'c3020a' and len(x[6:]) == 2088: # sci (1024 bytes)
                d0 = ""
            else:
                d0 = num_hex_data[-1]
            
       
        
        
        if i % 4 == 0 and i != 0:
            
            
            t_plot_start = dt.datetime.now()
            fig, ax = plt.subplots()
            sci_spectrogram_plot(ax,sci_time,sci_data,512) # t_slic_end = 
            t_plot_end = dt.datetime.now()
            print("Plot access")
            t_slicing = t_slic_end - t_slic_start
            with open(filepath +'\\'+'time_slicing.txt','a') as f2:
                f2.write(t_slic_start.isoformat() + '\t')
                f2.write(t_slic_end.isoformat()+'\t')
                f2.write(str(t_slicing.total_seconds()) + '\n')
                
            t_plot = t_plot_end - t_slic_end
            with open(filepath +'\\'+'time_plot.txt','a') as f2:
                f2.write(t_slic_end.isoformat() + '\t')
                f2.write(t_plot_end.isoformat()+'\t')
                f2.write(str(t_plot.total_seconds()) + '\n')
            i = 0
        else:
            i += 1 #interval count
            
    #print(len(noi))
        
        
        
    
    else:
        pass
    
    ts = dt.datetime.now()

socket.close()
plt.close()