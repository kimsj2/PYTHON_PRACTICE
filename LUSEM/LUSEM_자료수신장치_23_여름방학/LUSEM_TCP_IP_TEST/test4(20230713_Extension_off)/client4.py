# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:29:18 2023

@author: kimsj
"""

import socket
import binascii
import mod_datpar as datpar
import time

# TCP-IP 통신

# =============================================================================
# server_ip = '192.168.1.120'  # 위에서 설정한 서버 ip
# server_port = 4040 # 위에서 설정한 서버 포트번호
# 
# socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.connect((server_ip, server_port))
# 
# # /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
# 
# with open('test4_512.txt','w') as test4:
#     start = time.perf_counter()
#     while True:
#         data = socket.recv(4096)
#         hex_data = binascii.hexlify(data).decode('utf-8')
#         end = time.perf_counter()
#         print('echo msg:', len(hex_data))
#         count = end-start
#         print(round(count,4))
#         test4.write(hex_data)
#         if count >=1800:
#             break
# socket.close()
# =============================================================================


# try 문 이용해서 데이터 손실 났을 때 프로그램 죽지 않게 하기.

# data parsing


filename = r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_TEST\test4(20230713_Extension_off)\test4_512.txt'
datpar.datpar(filename, r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_TEST\test4(20230713_Extension_off)')


