# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 11:41:59 2023

@author: whseol-lab
"""

import os
import sys
import numpy as np
import pandas as pd
import datetime as dt
import binascii
import textwrap
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import socket
import threading

# =============================================================================
# from matplotlib import cm
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import matplotlib.style
# import matplotlib.dates as mdates
# import matplotlib.colors as colors
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# import matplotlib.ticker as ticker
# from matplotlib.ticker import FormatStrFormatter
# from matplotlib.ticker import AutoMinorLocator
# from matplotlib import gridspec
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import matplotlib.animation as animation
# =============================================================================
#socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ui file connect
form_class = uic.loadUiType("SSIL_Data Communication_UI.ui")[0]

# SSIL Logo
path_logo = r'SSIL Logo\SSIL_logo.png'
path_logo2 = r'SSIL Logo\SSIL_logo2.png'

# save path
save_path0 = r'Test Results'
os.makedirs(save_path0, exist_ok=True)

# =============================================================================
# Example, plot
# =============================================================================
#path_ex = r'F:\1. Research\28. 자료 수신 장치\GUI Program\20230801_Data_GUI\Example2'
#sci = pd.read_csv(os.path.join(path_ex, 'sci_parsed.csv'))
#time_sci = pd.to_datetime(sci.loc[:,'Time'])
#sci0 = sci.loc[:,'A_Bin_0':'B_Bin_255']


class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
######## Signal & setting ################################################################
##########################################################################################
        #QtWidgets.QApplication.processEvents()
        self.setWindowTitle('SSIL Data Communication')
        self.setWindowIcon(QIcon(path_logo))
        
        # connect button status
        #self.btn_connect.clicked.connect(self.recognize_connect)
        
        self.btn_connect.clicked.connect(self.func_btn_connect)
        
        self.btn_disconnect.clicked.connect(self.func_btn_disconnect)
        
        # text browser clear
        self.btn_textbrower_clear.clicked.connect(self.func_btn_text_clear)
        
        # save folder name
        self.lineEdit_filename.setText(f'{dt.datetime.now().strftime("%Y%m%d")}_folder name')
        
        self.groupBox_plot.setDisabled(True)
        
        # plot_radio button
        self.func_rbtn_setting()
        
        # Plot start & stop
        self.btn_plot_start.clicked.connect(self.func_btn_plot_start)
        self.btn_plot_stop.clicked.connect(self.func_btn_plot_stop)
        
        self.btn_plot_start.setDisabled(True)
        self.btn_plot_stop.setDisabled(True)
        
        #self.checkBox_plot_start.setDisabled(True)
        
        #self.checkBox_plot_start.clicked.connect(self.func_btn_plot_start)
        
        
        
        
        
        # image load
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(path_logo2)
        self.qPixmapFileVar.setDevicePixelRatio(4)
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1300)
        self.label_logo.setPixmap(self.qPixmapFileVar)
        
        
######## Slot (Function) #################################################################
##########################################################################################
    def func_btn_connect(self):
        self.textBrowser_connect.append(f'{dt.datetime.now().isoformat(sep=" ", timespec="seconds")}: LUSEM Connect')
        
        save_foldername = self.lineEdit_filename.text()
        
        save_path = os.path.join(save_path0, save_foldername)
        os.makedirs(save_path, exist_ok=True)
        
        self.btn_disconnect.setEnabled(True)
        self.btn_connect.setDisabled(True)
        
        self.lineEdit_IP.setDisabled(True)
        self.lineEdit_Port.setDisabled(True)
        self.lineEdit_filename.setDisabled(True)
        
        self.label_connect_status.setText('Status: Connect !!')
        
        self.dateTimeEdit_start.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEdit_end.setDateTime(QDateTime.currentDateTime())
        
        self.timeEdit_duration.setTime(QTime(0,10,0))
        self.timeEdit_interval.setTime(QTime(0,0,5))
        
        self.groupBox_plot.setEnabled(True)
        
# =============================================================================
#         while True:
#             try:
#                 self.func_tcpip_run()
#             except Exception as ex:
#                 time.sleep(1)
#                 print(ex)
# =============================================================================
        
        #self.func_tcp_ip()
        
    def func_btn_disconnect(self):
        self.textBrowser_connect.append(f'{dt.datetime.now().isoformat(sep=" ", timespec="seconds")}: LUSEM Disconnect')
        
        self.btn_disconnect.setDisabled(True)
        self.btn_connect.setEnabled(True)
        
        self.lineEdit_IP.setEnabled(True)
        self.lineEdit_Port.setEnabled(True)
        self.lineEdit_filename.setEnabled(True)
        
        self.label_connect_status.setText('Status: Disconnect !!')
        
        self.groupBox_plot.setDisabled(True)
        
        #socket.close()
        
    def func_btn_text_clear(self):
        self.textBrowser_connect.clear()
        
    def func_rbtn_setting(self):
        self.rbtn_plot_dynamic.clicked.connect(lambda: self.func_rbtn_change('1'))
        self.rbtn_plot_static.clicked.connect(lambda: self.func_rbtn_change('2'))
    
    def func_rbtn_change(self, get):
        if get == '1':
            self.btn_plot_start.setEnabled(True)
            self.btn_plot_stop.setEnabled(True)

        elif get == '2':
            self.btn_plot_start.setEnabled(True)
            self.btn_plot_stop.setEnabled(True)

    
    def func_btn_plot_start(self):
        print('plot start btn')

    def func_btn_plot_stop(self):
        print('plot stop btn')
    
    def func_tcpip_run(self):
        ip_address = self.lineEdit_IP.text()
        port_number = int(self.lineEdit_Port.text())
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            QtWidgets.QApplication.processEvents()
            sock.settimeout(5)
            sock.connect((ip_address, port_number))
            sock.settimeout(None)
            print('connected')
            
            while True:
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
                                np.append(soh_data,'a5'+x[6:] + '55deadbf5a\n')
                            elif x[:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                                noi.write('a5\t')
                                noi.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                                noi.write('\t55\tde\tad\tbf\t5a\n')
                                np.append(noi_data,'a5'+x[6:] + '55deadbf5a\n')
                            elif x[:4] == 'c304': # dum
                                dum.write('a5\t')
                                dum.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                                dum.write('\t55\tde\tad\tbf\t5a\n')
                                np.append(dum_data,'a5'+x[6:] + '55deadbf5a\n')
                            elif x[:6] == 'c3008a' and len(x[6:]) == 552: # sci (256 bytes)
                                sci.write('a5\t')
                                sci.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                                sci.write('\t55\tde\tad\tbf\t5a\n')
                                np.append(sci_data,'a5'+x[6:] + '55deadbf5a\n')
                            elif x[:6] == 'c3010a' and len(x[6:]) == 1064 :# sci (512 bytes)
                                sci.write('a5\t')
                                sci.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                                sci.write('\t55\tde\tad\tbf\t5a\n')
                                np.append(sci_data,'a5'+x[6:] + '55deadbf5a\n')
                            elif x[:6] == 'c3020a' and len(x[6:]) == 2088: # sci (1024 bytes)
                                sci.write('a5\t')
                                sci.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                                sci.write('\t55\tde\tad\tbf\t5a\n')
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
                else:
                    pass
    
    
    

    

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    sys.exit(app.exec_())
