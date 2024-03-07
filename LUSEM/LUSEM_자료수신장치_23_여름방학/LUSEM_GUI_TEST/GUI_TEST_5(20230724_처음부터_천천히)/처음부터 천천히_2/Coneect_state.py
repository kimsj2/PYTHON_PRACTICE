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
        self.connect.clicked.connect(self.recognize_connect)
        
        # 시간 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_conn_text)
        self.timer.start(1000)  # 1000 밀리초 (1초)마다 업데이트
        
        # self.hex_data
        self.hex_data = ""
        
    def recognize_connect(self):
        if self.connect.text() == "Connect to":
            self.connect_tcp_ip()
            self.change_conn_button_text()
        elif self.connect.text() =="Disconnect":
            self.disconnect_tcp_ip()
            self.change_conn_button_text()
    
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
    def connect_tcp_ip(self):
        # IP. port 연결하기
        socket.connect((self.IP.text(), int(self.port.text())))
        self.timer.start(1000)
        while True:
            QtWidgets.QApplication.processEvents()
            s_time = time.process_time()
            data = socket.recv(4096)
            self.hex_data = binascii.hexlify(data).decode('utf-8')
            e_time = time.process_time()
            with open(r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_5(20230724_처음부터_천천히)\처음부터 천천히_2\test2','a') as f:
                f.write(dt.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')+'\t')
                f.write(str((e_time - s_time)*1000)+'\t')
                f.write(self.hex_data)
                f.write('\n')
            print(len(self.hex_data)/2)
            # print(self.datpar(hex_data))
    
    def disconnect_tcp_ip(self):
        self.timer.stop()
        socket.close()
        self.hex_data =""
        
    
    def datpar(self,data):
        sci = []
        noi = []
        soh = []
        dum = []
        
        if (len(data) >= 1348):
            bytedata = data[:6]
            if not bytedata:
                pass
            if bytedata == 'a82900':
                bytedata = data[6:8]
                if bytedata == 'c3':
                    bytedata = data[8:10]
                    if bytedata == '00':
                        bytedata = data[10:12]
                        if bytedata == '26':
                            soh.append("a5\t")
                            bytedata = data[12:164].upper()
                            for i in range(76):
                                soh.append(bytedata[2*i:2*i+2].upper()+"\t")
                            soh.append("55\tde\tad\tbf\t5a\n")
                        elif bytedata == '5a':
                            noi.append("a5\t")
                            bytedata = data[12:372]
                            for i in range(180):
                                noi.append(bytedata[2*i:2*i+2].upper()+'\t')
                            noi.append("55\tde\tad\tbf\t5a\n")
                        elif bytedata == '8a':
                            bytedata = data[12:24]
                            if bytedata[-4:] == "010d":
                                print('256')
                                sci.append("a5\t")
                                for i in range(6):
                                    sci.append(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                bytedata = data[24:564]
                                for i in range((256+8+6) ):
                                    sci.append(bytedata[2*i:2*i+2].upper()+'\t')
                                sci.append("55\tde\tad\tbf\t5a\n")

                    elif bytedata == '01':
                        bytedata = data[10:12]
                        if bytedata == '0a':
                            bytedata = data[12:24]
                            if bytedata[-4:] == "020d":
                                print('512')
                                sci.append("a5\t")
                                for i in range(6):
                                    sci.append(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                bytedata = data[24:1076]
                                for i in range((512+8+6)):
                                    sci.append(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                sci.append("55\tde\tad\tbf\t5a\n")

                    elif bytedata == '02':
                        bytedata = data[10:12]
                        if bytedata == '0a':
                            print('1024')
                            sci.append("a5\t")
                            bytedata = data[12:2100]
                            for i in range(1024+20):
                                sci.append(bytedata[2*i:2*i+2].upper()+'\t')
                            sci.append("55\tde\tad\tbf\t5a\n")

                    elif bytedata == '04':
                        bytedata = data[10:12]
                        if bytedata == '0c':
                           dum.append("a5\t")
                           bytedata = data[12:4156]
                           for i in range(2072):
                               dum.append(bytedata[2*i:2*i+2].upper()+'\t')
                           dum.append("55\tde\tad\tbf\t5a\n")

                elif bytedata == 'c1':
                    bytedata = data[8:10]
                    if bytedata == '00':
                        bytedata = data[10:12]
                        if bytedata == '0c':
                            bytedata = data[12:60]
                            
            data = data[1348:]  # 처리된 데이터 다음으로 넘어가도록 data 갱신              
        return "".join(sci), "".join(noi), "".join(soh), "".join(dum)
    
# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
