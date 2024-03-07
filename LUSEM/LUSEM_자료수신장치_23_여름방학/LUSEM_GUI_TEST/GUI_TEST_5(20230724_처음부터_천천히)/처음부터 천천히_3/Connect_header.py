import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from datetime import datetime as dt
import socket
import binascii
import time
import threading

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
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_conn_text)
        self.timer.start(1000)  # 1000 밀리초 (1초)마다 업데이트
        
        # self.hex_data
        self.hex_data = ""
        
        # 쓰레드 관련 변수
        self.thread = None
        self.connected = False
        self.stop_flag = threading.Event()

    def recognize_connect(self):
        if not self.connected:
            self.start_connection()
        else:
            self.stop_connection()
    
    def start_connection(self):
        # IP. port 연결하기
        try:
            socket.connect((self.IP.text(), int(self.port.text())))
        except ConnectionRefusedError:
            print("Connection refused.")
            return
        
        # 쓰레드 생성 및 실행
        self.thread = threading.Thread(target=self.connect_tcp_ip)
        self.connected = True
        self.connect.setText("Disconnect")
        self.connect.setEnabled(True)  # 버튼 비활성화
        
        # 쓰레드 시작
        self.thread.start()
        
        # ip, port fix
        self.IP.setEnabled(False)
        self.port.setEnabled(False)
        
    def stop_connection(self):
        self.stop_flag.set()  # 쓰레드 종료 플래그 설정
        self.thread.join()  # 쓰레드가 종료될 때까지 대기
        self.timer.stop()
        socket.close()
        self.connected = False
        self.connect.setText("Connect to")
        self.connect.setEnabled(False)  # 버튼 비활성화
        self.hex_data = ""
    
    def update_conn_text(self):
        # 텍스트를 실시간으로 업데이트하는 함수
        if len(self.hex_data)==0:
            new_text = 'Connect state : Disconnect'
        else:
            new_text = f'Connect state : {len(self.hex_data)/2} bytes per 1 sec'
        self.connect_state.setText(new_text)
    
    # time.sleep(1) 이용
    def connect_tcp_ip(self):
        while not self.stop_flag.is_set():
            QtWidgets.QApplication.processEvents()
            self.s_time = time.process_time()
            data = socket.recv(4096)
            hex_data = binascii.hexlify(data).decode('utf-8')
            self.seperate_with_data_length(hex_data)
            print(len(self.hex_data)/2)

    def seperate_with_data_length(self, hex_data):
        if hex_data[:2]=='a8':
            self.e_time = time.process_time()
            with open(r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_5(20230724_처음부터_천천히)\처음부터 천천히_3\test3','a') as f:
                f.write(dt.now().strftime('%Y-%m-%d %H:%M:%S')+'\t')
                f.write(str((self.e_time - self.s_time)*1000)+'\t')
                f.write(self.hex_data)
                f.write('\n')
            # self.datpar(self.hex_data)
            self.hex_data = hex_data
        else:
            self.hex_data += hex_data

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
