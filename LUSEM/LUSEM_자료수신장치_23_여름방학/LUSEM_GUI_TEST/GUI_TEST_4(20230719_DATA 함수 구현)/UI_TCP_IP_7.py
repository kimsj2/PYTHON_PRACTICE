# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_commander_final.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
import socket
from datetime import datetime
import binascii
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import glob

# prepare socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# logo file path
Logo_filename_path = r'SSIL_logo.PNG'
save_path = r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_4(20230719_DATA 함수 구현)'

# UI

# UI (button)
# pushButton : Connect to
# psuhButton_2 : Disconnect
# pushButton_3 : Write to
# pushButton_4 : New
# pushButton_5 : Execute
# pushButton_6 : Start
# pushButton_8 : Clear
# pushButton_7 : Graph total save
# pushButton_9 : Graph SOH save

# UI (lineEdit)
# lineEdit : IP
# lineEdit_2 : port
# lineEdit_3 : nbyte
# lineEdit_4 : save_filename
# lineEdit_13 : interval second

# UI (listView)
# listView : byte per sec / disconnect

# UI (timeEdit)
# timeEdit : parsing start time
# timeEdit_2 : parsing stop time
# timeEdit_3 : poll interval time

# UI (check box)
# checkBox : poll interval second apply

# UI (Graphic viewer)
# graphicsView : Total graph
# graphicsView_9 : SOH graph

# main class

class Ui_MainWindow(object):
    def __init__(self):
        # 변수 추가
        self.IP = ""
        self.port = ""
        self.nbyte =""
        self.filename_current = str(datetime.now())
        self.hex_data = ""
        self.comm_stop = 0
        
        # save 
        self.start_time =""
        self.start_dd = ""
        self.start_hh = ""
        self.start_mm = ""
        self.start_ss = ""
        
        self.stop_time =""
        self.stop_dd = ""
        self.stop_hh = ""
        self.stop_ss = ""
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(795, 802)
        MainWindow.setWindowIcon(QIcon(Logo_filename_path))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1480, 919))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 40, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(90, 40, 150, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(90, 20, 21, 20))
        self.label.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 40, 91, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(250, 20, 31, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(350, 40, 51, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 40, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.listView = QtWidgets.QListView(self.groupBox)
        self.listView.setGeometry(QtCore.QRect(10, 70, 481, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setObjectName("listView")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(350, 20, 31, 20))
        self.label_8.setObjectName("label_8")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 200, 431, 161))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.groupBox_3)
        self.timeEdit_2.setGeometry(QtCore.QRect(190, 60, 82, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeEdit_2.sizePolicy().hasHeightForWidth())
        self.timeEdit_2.setSizePolicy(sizePolicy)
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(11, 31, 173, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.timeEdit = QtWidgets.QTimeEdit(self.groupBox_3)
        self.timeEdit.setGeometry(QtCore.QRect(190, 32, 82, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeEdit.sizePolicy().hasHeightForWidth())
        self.timeEdit.setSizePolicy(sizePolicy)
        self.timeEdit.setObjectName("timeEdit")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(11, 60, 163, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 90, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 90, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(93, 91, 251, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_8.setGeometry(QtCore.QRect(350, 120, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 120, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setObjectName("pushButton_6")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 120, 501, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.timeEdit_3 = QtWidgets.QTimeEdit(self.groupBox_2)
        self.timeEdit_3.setGeometry(QtCore.QRect(20, 30, 66, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeEdit_3.sizePolicy().hasHeightForWidth())
        self.timeEdit_3.setSizePolicy(sizePolicy)
        self.timeEdit_3.setObjectName("timeEdit_3")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(120, 30, 96, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setObjectName("checkBox")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_13.setGeometry(QtCore.QRect(230, 30, 91, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_13.sizePolicy().hasHeightForWidth())
        self.lineEdit_13.setSizePolicy(sizePolicy)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(330, 30, 59, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setGeometry(QtCore.QRect(410, 30, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setObjectName("pushButton_5")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 1, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_3.addWidget(self.pushButton_9, 1, 0, 1, 1)
        self.graphicsView_9 = QtWidgets.QGraphicsView(self.tab_3)
        self.graphicsView_9.setObjectName("graphicsView_9")
        self.gridLayout_3.addWidget(self.graphicsView_9, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 795, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        MainWindow.setTabOrder(self.lineEdit_3, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.listView)
        MainWindow.setTabOrder(self.listView, self.timeEdit_3)
        MainWindow.setTabOrder(self.timeEdit_3, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.lineEdit_13)
        MainWindow.setTabOrder(self.lineEdit_13, self.pushButton_5)
        MainWindow.setTabOrder(self.pushButton_5, self.timeEdit)
        MainWindow.setTabOrder(self.timeEdit, self.timeEdit_2)
        MainWindow.setTabOrder(self.timeEdit_2, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.lineEdit_4)
        MainWindow.setTabOrder(self.lineEdit_4, self.pushButton_4)
        MainWindow.setTabOrder(self.pushButton_4, self.pushButton_6)
        MainWindow.setTabOrder(self.pushButton_6, self.pushButton_8)
        MainWindow.setTabOrder(self.pushButton_8, self.pushButton_7)
        MainWindow.setTabOrder(self.pushButton_7, self.graphicsView)
        MainWindow.setTabOrder(self.graphicsView, self.pushButton_9)
        MainWindow.setTabOrder(self.pushButton_9, self.graphicsView_9)
        
        # 버튼 클릭
        self.pushButton.clicked.connect(self.button_event_conn)
        self.pushButton_2.clicked.connect(self.button_event_disconn)
        

    # 서버 연결 (connect to)

    # Connect button
    def button_event_conn(self):
        self.IP = self.lineEdit.text()
        self.port = int(self.lineEdit_2.text())
        self.nbyte = self.lineEdit_3.text()
        socket.connect((self.IP, self.port))
        while (self.comm_stop==0):
            QtWidgets.QApplication.processEvents()
            data = socket.recv(4096)
            self.hex_data = binascii.hexlify(data).decode('utf-8')
            with open(r'C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI_TEST\GUI_TEST_4(20230719_DATA 함수 구현)\test1','w') as f:
                f.write(self.hex_data)
            print('hex_data :', len(data))
        socket.close()
        
    # write('w')
    # write('w+')
    
    # Disconnect button
    def button_event_disconn(self):
        self.comm_stop=1
    
    def show_hex_data(self):
        return self.hex_data
    
    # save file name (write to)
    def button_event_write(self):
        self.filename = self.lineEdit_4.text()
        
    
    
    # save start
# =============================================================================
#     def button_event_save_start(self):
#         self.start_time = self.timeEdit.time()
#         self.start_dd = self.start_time.days()
#         self.start_hh = self.start_time.hours()
#         self.start_mm = self.start_time.minutes()
#         self.start_ss = self.start_time.seconds()
#         
#         self.stop_time = self.timeEdit.time()
#         self.stop_dd = self.stop.time.day()
#         self.stop_hh = self.stop.time.hour()
#         self.stop_mm = self.stop.time.minute()
#         self.stop_ss = self.stop.time.second()
# =============================================================================
        

        
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("LUSEM_DATA", "LUSEM_DATA"))
        self.groupBox.setTitle(_translate("LUSEM_DATA", "Connect Setup"))
        self.pushButton.setText(_translate("LUSEM_DATA", "Connect to"))
        self.label.setText(_translate("LUSEM_DATA", "<html><head/><body><p>IP</p></body></html>"))
        self.label_3.setText(_translate("LUSEM_DATA", "<html><head/><body><p>port</p></body></html>"))
        self.pushButton_2.setText(_translate("LUSEM_DATA", "Disconnect"))
        self.label_8.setText(_translate("LUSEM_DATA", "<html><head/><body><p>nbyte</p></body></html>"))
        self.groupBox_3.setTitle(_translate("LUSEM_DATA", "Time Parsing Setup"))
        self.timeEdit_2.setDisplayFormat(_translate("LUSEM_DATA", "dd.hh.mm.ss"))
        self.label_4.setText(_translate("LUSEM_DATA", "<html><head/><body><p><span style=\" font-size:11pt;\">Start time(dd.hh.mm.ss) : </span></p></body></html>"))
        self.timeEdit.setDisplayFormat(_translate("LUSEM_DATA", "dd.hh.mm.ss"))
        self.label_5.setText(_translate("LUSEM_DATA", "<html><head/><body><p><span style=\" font-size:11pt;\">End time(dd.hh.mm.ss) :</span></p></body></html>"))
        self.pushButton_4.setText(_translate("LUSEM_DATA", "New"))
        self.pushButton_3.setText(_translate("LUSEM_DATA", "Write to"))
        self.pushButton_8.setText(_translate("LUSEM_DATA", "Clear"))
        self.pushButton_6.setText(_translate("LUSEM_DATA", "Start"))
        self.groupBox_2.setTitle(_translate("LUSEM_DATA", "Poll Interval Setup"))
        self.timeEdit_3.setDisplayFormat(_translate("LUSEM_DATA", "hh.mm.ss"))
        self.checkBox.setText(_translate("LUSEM_DATA", "Poll Interval :"))
        self.label_2.setText(_translate("LUSEM_DATA", "<html><head/><body><p><span style=\" font-size:11pt;\">Seconds</span></p></body></html>"))
        self.pushButton_5.setText(_translate("LUSEM_DATA", "Execute"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("LUSEM_DATA", "Setting"))
        self.pushButton_7.setText(_translate("LUSEM_DATA", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("LUSEM_DATA", "Graph_total"))
        self.pushButton_9.setText(_translate("LUSEM_DATA", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("LUSEM_DATA", "Graph_SOH"))


# main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
