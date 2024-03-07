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
import textwrap

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
filepath = r"C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_7(20230728_TAP_HEX)\use_data\str vs list"
filename = "total.txt"

soh_data = []
sci_data = []
dum_data = []
noi_data = []
sci_flag=""

d0 = ""

ts = dt.datetime.now()
te = ts + dt.timedelta(seconds=60)

def sci_hex_dec(data):
    sci_flag = data[12][0]
    if sci_flag=='40': # compression (x), extension (o), 2 * 512 = 1024 bytes
        decimal_values = list(int(data[20:20+1024][i][0]+data[20:20+1024][i+1][0], 16) for i in range(0, len(data[20:20+1024]), 2))
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


while ts < te:
    t0 = dt.datetime.now()
    data = socket.recv(4096)
    d1 = binascii.hexlify(data).decode('utf-8')
    d0 += d1
    if (len(d0)>2000):
        t1 = dt.datetime.now()
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
                elif x[:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                    noi.write('a5\t')
                    noi.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                    noi.write('\t55\tde\tad\tbf\t5a\n')
                elif x[:4] == 'c304': # dum
                    dum.write('a5\t')
                    dum.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                    dum.write('\t55\tde\tad\tbf\t5a\n')
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
    #print(len(noi))
        t2 = dt.datetime.now()
        t3 = t2 - t1
        
        try:
            with open(filepath +'\\'+'time.txt','a') as f2:
                f2.write(t1.isoformat() + '\t')
                f2.write(t2.isoformat() + '\t')
                f2.write(str(t3.total_seconds()) + '\n')
                
        except:
            pass
    
    else:
        pass

    ts = dt.datetime.now()

socket.close()


