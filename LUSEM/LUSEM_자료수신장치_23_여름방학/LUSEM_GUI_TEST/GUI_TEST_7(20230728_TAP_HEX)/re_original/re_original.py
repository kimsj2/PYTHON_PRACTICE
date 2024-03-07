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
filepath = r"C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_7(20230728_TAP_HEX)"
filename = "total.txt"

soh_data = np.array([])
sci_data = np.array([])
dum_data = np.array([])
noi_data = np.array([])

d0 = ""

ts = dt.datetime.now()
te = ts + dt.timedelta(seconds=5)

while ts < te:
    t0 = dt.datetime.now()
    data = socket.recv(4096)
    d1 = binascii.hexlify(data).decode('utf-8')
    d0 += d1
    if (len(d0)>2000):
        t1 = dt.datetime.now()
        with open(filepath +'\\'+filename,'a') as f:
            with open(filepath +'\\'+'soh.txt','a') as soh:   
                with open(filepath +'\\'+'sci.txt','a') as sci:
                    with open(filepath +'\\'+'noi.txt','a') as noi:
                        with open(filepath +'\\'+'dum.txt','a') as dum:
                            f.write(re.sub(f".{{2}}",f"\\g<0>\\t",d0))
                            f.write('\n')
                            num_hex_data = np.array(d0.split('a82900'))
                            
                            if num_hex_data[0]=="":
                                num_hex_data = num_hex_data[1:]
                            
                            print(len(num_hex_data))
                            
                            for x in num_hex_data:
                                if x[:6]=='c30026' and len(x[6:])==152: # soh (76 bytes)
                                    soh.write('a5\t')
                                    soh.write(re.sub(f".{{2}}",f"\\g<0>\\t",x[6:]))
                                    soh.write('55deadbf5a\n')
                                    np.append(soh_data,'a5\t'+x[6:] + '55deadbf5a\n')
                                elif x[:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                                    noi.write('a5\t')
                                    noi.write(re.sub(f".{{2}}",f"\\g<0>\\t",x[6:]))
                                    noi.write('55deadbf5a\n')
                                    np.append(noi_data,'a5'+x[6:] + '55deadbf5a\n')
                                elif x[:4] == 'c304': # dum
                                    dum.write('a5\t')
                                    dum.write(re.sub(f".{{2}}",f"\\g<0>\\t",x[6:]))
                                    dum.write('55deadbf5a\n')
                                    np.append(dum_data,'a5'+x[6:] + '55deadbf5a\n')
                                elif x[:6] == 'c3008a' and len(x[6:]) == 552: # sci (256 bytes)
                                    sci.write('a5\t')
                                    sci.write(re.sub(f".{{2}}",f"\\g<0>\\t",x[6:]))
                                    sci.write('55deadbf5a\n')
                                    np.append(sci_data,'a5'+x[6:] + '55deadbf5a\n')
                                elif x[:6] == 'c3010a' and len(x[6:]) == 1064 :# sci (512 bytes)
                                    sci.write('a5\t')
                                    sci.write(re.sub(f".{{2}}",f"\\g<0>\\t",x[6:]))
                                    sci.write('55deadbf5a\n')
                                    np.append(sci_data,'a5'+x[6:] + '55deadbf5a\n')
                                elif x[:6] == 'c3020a' and len(x[6:]) == 2088: # sci (1024 bytes)
                                    sci.write('a5\t')
                                    sci.write(re.sub(f".{{2}}",f"\\g<0>\\t",x[6:]))
                                    sci.write('55deadbf5a\n')
                                    np.append(sci_data,'a5'+x[6:] + '55deadbf5a\n')
                            
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
    else:
        pass
    
    
    try:
        with open(filepath +'\\'+'time.txt','a') as f2:
            f2.write(t1.isoformat() + '\t')
            f2.write(t2.isoformat() + '\n')
            #f2.write(t3.total_seconds() + '\n')
            #f2.write(t2.isoformat())
            #f2.write('\n')
    except:
        pass
    
    ts = dt.datetime.now()
    '''
    text
    t0 t1 t2 dt.timedelta(t2-t1) data
    
    '''
    
socket.close()