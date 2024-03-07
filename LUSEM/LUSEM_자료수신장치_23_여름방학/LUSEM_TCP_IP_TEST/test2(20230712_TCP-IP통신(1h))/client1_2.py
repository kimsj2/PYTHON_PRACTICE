# =============================================================================
# # 클라이언트 프로그램
# # 서버 프로그램은 주피터, 이것은 파이참으로 실행 - 동시에 두개 프로그램 실행을 위해서.
# import socket
# 
# server_ip = 'localhost' # 위에서 설정한 서버 ip
# server_port = 3333 # 위에서 설정한 서버 포트번호
# 
# socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.connect((server_ip, server_port))
# 
# msg = input('msg:') # 서버로 보낼 msg 입력
# socket.sendall(msg.encode(encoding='utf-8'))
# 
# # 서버가 에코로 되돌려 보낸 메시지를 클라이언트가 받음
# data = socket.recv(100)
# msg = data.decode() # 읽은 데이터 디코딩
# print('echo msg:', msg)
# 
# socket.close()
# =============================================================================

# 클라이언트
import socket
import binascii
import mod_datpar as datpar
import mod_filearg as filearg
import time

#dat_filename = glob.glob(path+'/*.dat')[0]
#datpar.datpar(dat_filename, path)


# =============================================================================
# server_ip = '192.168.1.120'  # 위에서 설정한 서버 ip
# server_port = 4040 # 위에서 설정한 서버 포트번호
# 
# socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.connect((server_ip, server_port))
# 
# # /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
# start = time.perf_counter()
# 
# with open('test2.txt','w') as test2:
#     while True:
#         #msg = input('msg:') 
#         #socket.sendall(msg.encode(encoding='utf-8'))
#         data = socket.recv(4096*2)
#         #msg = data.decode() 
#         #print('echo msg:', data)
#         hex_data = binascii.hexlify(data).decode('utf-8')
#         print('echo msg:', len(hex_data))
#         end = time.perf_counter()
#         count = end-start
#         print(round(count,4))
#         test2.write(hex_data)
#         if count >=3600:
#             break
# socket.close()
# =============================================================================


# try 문 이용해서 데이터 손실 났을 때 프로그램 죽지 않게 하기
# 나중에는 쓰고 지우고 하기

filename = r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\Program\test2.txt'
datpar.datpar(filename, r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\Program')




# =============================================================================
# import socket
# 
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
# sock.connect(('192.168.109.226', 9008))     # 접속할 서버의 ip주소와 포트번호를 입력.
# sock.send('Hello'.encode())                 # 내가 전송할 데이터를 보냄.
# =============================================================================
