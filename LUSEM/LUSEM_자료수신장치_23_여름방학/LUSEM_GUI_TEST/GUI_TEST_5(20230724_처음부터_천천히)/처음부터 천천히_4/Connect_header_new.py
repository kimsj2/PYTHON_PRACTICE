import socket
import binascii
import time
from datetime import datetime as dt

server_ip = '192.168.1.120'  # 위에서 설정한 서버 ip
server_port = 4040 # 위에서 설정한 서버 포트번호

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

# /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
start = time.perf_counter()
filepath = ""
filename = ""



d0 = ''

total

while True:
    # t0 = dt.now()
    s_time = time.process_time()
    data = socket.recv(4096)
    hex_data = binascii.hexlify(data).decode('utf-8')
    # code
    # t1 = dt.now()    
    e_time = time.process_time()
    with open(filepath+"\\"+filename,'a') as f:
        f.write(dt.now().strftime('%Y-%m-%d %H:%M:%S')+'\t')
        f.write(str((e_time - s_time)*1e6)+'\t')
        f.write(hex_data)
        f.write('\n')
    # t2 = dt.now()
    '''
    d1 = socket.recv(4096)
    
    d0 += d1
    
    if len(d0) > 1500:
        parsing -> a8 -> noi sci soh
        d2 = ~~~~
        total.append(d2)
        
        d0 = d0[30+1348:]
        
        
        
        
    else:
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    text
    t0 t1 t2 dt.timedelta(t2-t1) data
    
    '''
    print(len(hex_data)/2)
socket.close()