
import socket
import binascii
import time
import datetime as dt
import numpy as np

server_ip = '192.168.1.120'  # 위에서 설정한 서버 ip
server_port = 4040 # 위에서 설정한 서버 포트번호

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

# /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
start = time.perf_counter()
filepath = r"C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_6(20230727_parsing)"
filename = "parsing.txt"



d0 = ""

while True:
    t0 = dt.datetime.now()
    data = socket.recv(4096)
    d1 = binascii.hexlify(data).decode('utf-8')
    d0 += d1
    if (len(d0)>2000):
        with open(filepath +'\\'+filename,'a') as f:
            with open(filepath +'\\'+'soh.txt','a') as soh:   
                with open(filepath +'\\'+'sci.txt','a') as sci:
                    with open(filepath +'\\'+'noi.txt','a') as noi:
                        with open(filepath +'\\'+'dum.txt','a') as dum:
                            f.write(d0 + '\n')
                            num_hex_data = np.array(d0.split('a82900'))
                            
                            if num_hex_data[0]=="":
                                num_hex_data = num_hex_data[1:]
                            
                            print(len(num_hex_data))
                            
                            for x in num_hex_data:
                                if x[:6]=='c30026' and len(x[6:])==152: # soh (76 bytes)
                                    soh.write('a5'+x[6:] + '55deadbf5a\n')
                                    
                                elif x[:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                                    noi.write('a5'+x[6:]+ '55deadbf5a\n')
                                    
                                elif x[:4] == 'c304': # dum
                                    dum.write('a5'+x[6:]+ '55deadbf5a\n')
                                elif x[:6] == 'c3008a' and len(x[6:]) == 552: # sci (256 bytes)
                                    sci.write('a5'+x[6:]+ '55deadbf5a\n')
                                elif x[:6] == 'c3010a' and len(x[6:]) == 1064 :# sci (512 bytes)
                                    sci.write('a5'+x[6:]+ '55deadbf5a\n')
                                elif x[:6] == 'c3020a' and len(x[6:]) == 2088: # sci (1024 bytes)
                                    sci.write('a5'+x[6:]+ '55deadbf5a\n')
                            
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
        
    else:
        pass
    
    t1 = dt.datetime.now()
    t2 = t1 - t0
    
    with open(filepath +'\\'+'time.txt','a') as f2:
        f2.write(t0.isoformat() + '\t')
        f2.write(t1.isoformat() + '\n')
        #f2.write(t2.isoformat())
        #f2.write('\n')
    
    
    '''
    text
    t0 t1 t2 dt.timedelta(t2-t1) data
    
    '''
    
socket.close()

# =============================================================================
# import socket
# import binascii
# import time
# from datetime import datetime as dt
# import numpy as np
# 
# server_ip = '192.168.1.120'
# server_port = 4040
# 
# socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.connect((server_ip, server_port))
# 
# filepath = r"C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_6(20230727_parsing)"
# filename = "parsing.txt"
# 
# data_buffer = ""
# 
# 
# # 해당 데이터를 처리하여 soh, sci, noi, dum 배열에 추가하는 함수(return: data, buffer(temporary data))
# 
# def process_data(hex_data):
#    
#     if hex_data.startswith('c3'):
#         
#         if hex_data.startswith('c30026') and len(hex_data[6:]) == 152:
#             return 'a5' + hex_data[6:] + '55deadbf5a\n', ''
#         elif hex_data.startswith('c3005a') and len(hex_data[6:]) == 360:
#             return 'a5' + hex_data[6:] + '55deadbf5a\n', ''
#         elif hex_data.startswith('c304'):
#             return 'a5' + hex_data[6:] + '55deadbf5a\n', ''
#         elif hex_data.startswith('c3008a') and len(hex_data[6:]) == 512:
#             return 'a5' + hex_data[6:] + '55deadbf5a\n', ''
#         elif hex_data.startswith('c3010a') and len(hex_data[6:]) == 1024:
#             return 'a5' + hex_data[6:] + '55deadbf5a\n', ''
#         elif hex_data.startswith('c3020a') and len(hex_data[6:]) == 2048:
#             return 'a5' + hex_data[6:] + '55deadbf5a\n', ''
#         else:
#             # 해당 데이터가 아직 완전하지 않은 경우 (다음 루프에서 추가 처리)
#             return '', hex_data
#         
#     else:
#         pass
#         
# noi = np.array([])
# soh = np.array([])
# dum = np.array([])
# sci = np.array([])
# data_buffer = ''
# while True:
#     t0 = dt.now()
#     data = socket.recv(4096)
#     
#     hex_data = binascii.hexlify(data).decode('utf-8')
#     
#     data_buffer += hex_data
#     if len(data_buffer) >= 2600:
#         with open(filepath + '\\' + filename, 'a') as f:
#             f.write(data_buffer + '\n')
# 
#         data_list = data_buffer.split('a82900')
#         if data_list[0] == "":
#             data_list = data_list[1:]
#         
#         for x in data_list:
#             processed_data, data_buffer = process_data(x)
#             if processed_data:
#                 if processed_data.startswith('a5c30026'):
#                     soh = np.append(soh, processed_data)
#                 elif processed_data.startswith('a5c3005a'):
#                     noi = np.append(noi, processed_data)
#                 elif processed_data.startswith('a5c304'):
#                     dum = np.append(dum, processed_data)
#                 else:
#                     sci = np.append(sci, processed_data)
#     print(len(noi))
#     '''
#     text
#     t0 t1 t2 dt.timedelta(t2-t1) data
# 
#     '''
# 
# socket.close()
# =============================================================================
