# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:37:13 2023

@author: kimsj
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
filepath = r"C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_9(20230803_CASE_2_A)\modify code"
filename = "total.txt"

soh_data = []
sci_data = []
dum_data = []
noi_data = []

sci_time= []

d0 = ""

start_time = ""
end_time  = ""

ts = dt.datetime.now()
te = ts + dt.timedelta(seconds=3600)


def sci_hex_dec(data):
    time_decimal = (dt.datetime(2001,1,1,9)+dt.timedelta(seconds=(int(data[6]+data[7]+data[8]+data[9], 16)))).isoformat(timespec='seconds')
    sci_time.append(time_decimal)
    sci_flag = data[12]
    if sci_flag=='40': # compression (x), extension (o), 2 * 512 = 1024 bytes
        decimal_values = list(int(data[20:20+1024][i]+data[20:20+1024][i+1], 16) for i in range(0, len(data[20:20+1024]), 2))
        sci_data.append(decimal_values)
    elif sci_flag=='00': # compression (x), extension (x), 2 * 256 = 512 bytes
        decimal_values = list(int(data[20:20+512][i][0]+data[20:20+512][i+1][0], 16) for i in range(0, len(data[20:20+512]), 2))
        sci_data.append(decimal_values)
    elif sci_flag=='e0': # compression (o), extension (o), 1 * 512 = 512 bytes
        decimal_values = list(int(data[20:20+512][i][0], 16) for i in range(0, len(data[20:20+512]), 1))
        sci_data.append(decimal_values)
    elif sci_flag=='a0': # compression(o), extension (x), 1* 256 = 256 bytes
        decimal_values = list(int(data[20:20+256][i][0], 16) for i in range(0, len(data[20:20+256]), 1))
        sci_data.append(decimal_values)
    else:
        pass # nan list?


def sci_spectrogram_plot(ax, sci_time,sci_data,bins, time_interval): # ax / list / int / list / dt.timedelta(??)
    sci_time = pd.to_datetime(np.array(sci_time))
    sci_data = pd.DataFrame(np.array(sci_data),index=sci_time)
    
    current_time = sci_time[-1]
    t_slic_end = ""
    
    if sci_time[0] <= (current_time -time_interval):
        
        time = sci_time[sci_time >= (current_time - time_interval)]
        sci_slicing_data = sci_data[sci_time >= (current_time - time_interval)]
        
        t_slic_end = dt.datetime.now() # slicing end time
        X, Y = np.meshgrid(time, np.arange(0,bins))
        pcm = ax.pcolormesh(X,Y, sci_slicing_data.values.T, cmap='jet',shading='auto', norm=colors.LogNorm(vmin=1, vmax=1e3))
        cbar = plt.colorbar(pcm)
        cbar.set_label('Count rates')
        gc.collect()
        ax.remove()
        
    else:
        t_slic_end = dt.datetime.now() # slicing end time
        X, Y = np.meshgrid(sci_time, np.arange(0,bins))
        pcm = ax.pcolormesh(X,Y, sci_data.values.T, cmap='jet',shading='auto', norm=colors.LogNorm(vmin=1, vmax=1e3))
        cbar = plt.colorbar(pcm)
        cbar.set_label('Count rates')
        gc.collect()
        ax.remove()
        
    return t_slic_end
    
    
    
# =============================================================================
# def sci_bar_plot(ax,bin_, sci_data):
#     sci_data = np.array(sci_data)
#     sci_data_sum = sci_data.sum(axis=0)
#     ax2 = ax[1]
#     ax2.set_yscale('log')
#     ax2.bar(np.arange(1,len(sci_data_sum)+1),sci_data_sum)
# =============================================================================


i = 0    #interval count

while ts < te:
    data = socket.recv(4096)
    d1 = binascii.hexlify(data).decode('utf-8')
    d0 += d1
    if (len(d0)>2000):
        
        t_start = dt.datetime.now() # parsing start time
        
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
                    soh_data.append('a5'+x[6:]+'55deadbf5a')
                    
                elif x[:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                    noi.write('a5\t')
                    noi.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                    noi.write('\t55\tde\tad\tbf\t5a\n')
                    noi_data.append('a5'+x[6:]+'55deadbf5a')
                    
                elif x[:4] == 'c304': # dum
                    dum.write('a5\t')
                    dum.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                    dum.write('\t55\tde\tad\tbf\t5a\n')
                    dum_data.append('a5'+x[6:]+'55deadbf5a')
                    
                elif x[:6] == 'c3008a' and len(x[6:]) == 552: # sci (256 bytes)
                    sci.write('a5\t')
                    sci_list = textwrap.wrap(x[6:], width=2)
                    sci.write('\t'.join(sci_list))
                    sci.write('\t55\tde\tad\tbf\t5a\n')
                    sci_hex_dec(sci_list)
                    
                elif x[:6] == 'c3010a' and len(x[6:]) == 1064 :# sci (512 bytes)
                    sci.write('a5\t')
                    sci_list = textwrap.wrap(x[6:], width=2)
                    sci.write('\t'.join(sci_list))
                    sci.write('\t55\tde\tad\tbf\t5a\n')
                    sci_hex_dec(sci_list)
                    
                    
                elif x[:6] == 'c3020a' and len(x[6:]) == 2088: # sci (1024 bytes)
                    sci.write('a5\t')
                    sci_list = textwrap.wrap(x[6:], width=2)
                    sci.write('\t'.join(sci_list))
                    sci.write('\t55\tde\tad\tbf\t5a\n')
                    sci_hex_dec(sci_list)
            
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
            
        t_par_end = dt.datetime.now()  # parsing end time

        if i % 4 == 0 and i != 0:
            fig, ax = plt.subplots()
            t_slic_start = dt.datetime.now() # slicing start time
            t_slic_end = sci_spectrogram_plot(ax, sci_time,sci_data,512,dt.timedelta(minutes=10)) # return slicing end time 
            t_plot_end = dt.datetime.now() # plot end time
            
            print("Plot access")
            
            t_slicing = t_slic_end - t_slic_start
            
            with open(filepath +'\\'+'time_slicing.txt','a') as f2: # write slicing time
                f2.write(t_slic_start.isoformat() + '\t')
                f2.write(t_slic_end.isoformat()+'\t')
                f2.write(str(t_slicing.total_seconds()) + '\n')
                
            t_plot = t_plot_end - t_slic_end
            
            with open(filepath +'\\'+'time_plot.txt','a') as f2: # write plot time
                f2.write(t_slic_end.isoformat() + '\t')
                f2.write(t_plot_end.isoformat()+'\t')
                f2.write(str(t_plot.total_seconds()) + '\n')
            i = 0
        else:
            i += 1 #interval count
            
    #print(len(noi))
        t_parsing = t_par_end - t_start
        
        try:
            with open(filepath +'\\'+'time_parsing.txt','a') as f2: # write parsing time
                f2.write(t_start.isoformat() + '\t')
                f2.write(t_par_end.isoformat()+'\t')
                f2.write(str(t_parsing.total_seconds()) + '\n')
            
        except:
            pass
    
    else:
        pass
    
    ts = dt.datetime.now()

socket.close()
plt.close()
