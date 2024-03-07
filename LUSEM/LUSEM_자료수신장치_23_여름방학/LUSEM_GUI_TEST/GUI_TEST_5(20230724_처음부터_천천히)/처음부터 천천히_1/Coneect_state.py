import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from datetime import datetime as dt
import socket
import binascii
import numpy as np
import time
# prepare socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# logo
Logo_filename_path = r'SSIL_logo.PNG'

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # load ui
        loadUi("Connect_state.ui", self)
        # logo 설정 & 창 이름 설정
        app.setWindowIcon(QIcon(Logo_filename_path))
        self.setWindowTitle("LUSEM_DATA")
        
        # conn_button_disconn_button
        if self.connect.text() == "Connect to":
            self.connect.clicked.connect(self.change_conn_button_text)
            self.connect.clicked.connect(self.connect_tcp_ip)
        elif self.connect.text() =="Disconnect":
            self.connect.clicked.connect(self.change_conn_button_text)
        
        # 시간 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_conn_text)
        self.timer.start(1000)  # 1000 밀리초 (1초)마다 업데이트
        
        # self.hex_data
        self.hex_data = ""
        
    def change_conn_button_text(self):
        if self.connect.text() == "Connect to":
            self.connect.setText("Disconnect")
        else:
            self.connect.setText("Connect to")
            
    def update_conn_text(self):
        # 텍스트를 실시간으로 업데이트하는 함수
        if len(self.hex_data)==0:
            new_text = 'Connect state : Disconnect'
        else:
            new_text = f'Connect state : {len(self.hex_data)/2} bytes per 1 sec'
        self.connect_state.setText(new_text)
    
    
    # time.sleep(1) 이용
# =============================================================================
#     def connect_tcp_ip(self):
#         # IP. port 연결하기
#         socket.connect((self.IP.text(), int(self.port.text())))
#         while True:
#             QtWidgets.QApplication.processEvents()
#             data = socket.recv(4096)
#             time.sleep(1)
#             self.hex_data = binascii.hexlify(data).decode('utf-8')
#             with open(r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_5(20230724_처음부터_천천히)\처음부터 천천히\test1','w') as f:
#                 f.write(self.hex_data)
#             print(len(self.hex_data)/2)
# =============================================================================
    
    # header 이용 + time.sleep(1)
    def connect_tcp_ip(self):
        # IP. port 연결하기
        socket.connect((self.IP.text(), int(self.port.text())))
        while True:
            if self.connect.text()=="Connect to":
                socket.close()
                break
            QtWidgets.QApplication.processEvents()
            data = socket.recv(4096)
            time.sleep(1)
            self.hex_data = binascii.hexlify(data).decode('utf-8')
            if self.hex_data[:2]=='a8':    
                with open(r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_5(20230724_처음부터_천천히)\처음부터 천천히\test1','w') as f:
                    f.write(self.hex_data)
            print(len(self.hex_data)/2)
            
            
# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
