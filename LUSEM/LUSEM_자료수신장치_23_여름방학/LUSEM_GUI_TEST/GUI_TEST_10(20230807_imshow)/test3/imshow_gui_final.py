# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:49:21 2023

@author: SSIL_B104_1
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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

## import 추가 
from collections import deque
import textwrap
import matplotlib.colors as colors
import matplotlib.pyplot as plt 
import matplotlib as mpl
import matplotlib.dates as mdates
import gc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import gridspec
from matplotlib.figure import Figure


##

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

#%% main class
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        # QThread 
        
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
        
        # save data #
        
        self.soh_data = deque([])
        self.sci_data = deque([])
        self.dum_data = deque([])
        self.noi_data = deque([])

        self.sci_time = deque([])

        self.soh_left = []
        self.sci_left = []
        self.noi_left = []
        self.dum_left = []
        self.sci_time_left = []
        
        self.deque_length = 600
        self.plot_interval = 0
        self.connect_state = True
        
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

        self.running = True
        self.fig = None
        self.timer = None
        
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
        
        self.connect_state = True
        while self.connect_state:
            try:
                self.func_tcpip_run()
            except Exception as ex:
                time.sleep(1)
                print(ex)
        
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
        
        self.connect_state = False
        
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

    
    
    def func_tcpip_run(self):
        ip_address = self.lineEdit_IP.text()
        port_number = int(self.lineEdit_Port.text())
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((ip_address, port_number))
            sock.settimeout(None)
            print('connected')
            
            t_slic_end = ''
            t_slic_start = ''
            d0=''
            while self.connect_state:
                QtWidgets.QApplication.processEvents()
                data = sock.recv(4096)
                d1 = binascii.hexlify(data).decode('utf-8')
                d0 += d1
                if (len(d0)>2000):
                    filepath = os.path.join(save_path0, self.lineEdit_filename.text())
                    with open(filepath +'\\'+'total.txt','a') as f, open(filepath +'\\'+'soh.txt','a') as soh, open(filepath +'\\'+'sci.txt','a') as sci, open(filepath +'\\'+'noi.txt','a') as noi, open(filepath +'\\'+'dum.txt','a') as dum:
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
                                
                                if (len(self.soh_data) == self.deque_length):
                                    soh_temp = self.soh_data.popleft()
                                    self.soh_left.append(soh_temp)
                                    self.soh_data.append('a5'+x[6:]+'55deadbf5a')
                                else:
                                    self.soh_data.append('a5'+x[6:]+'55deadbf5a')
                                
                            elif x[:6]=='c3005a' and len(x[6:])==360: # noi (180 bytes)
                                noi.write('a5\t')
                                noi.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                                noi.write('\t55\tde\tad\tbf\t5a\n')
                                
                                if (len(self.noi_data) == self.deque_length):
                                    noi_temp = self.noi_data.popleft()
                                    self.noi_left.append(noi_temp)
                                    self.noi_data.append('a5'+x[6:]+'55deadbf5a')
                                else:
                                    self.noi_data.append('a5'+x[6:]+'55deadbf5a')
                                
                            elif x[:4] == 'c304': # dum
                                dum.write('a5\t')
                                dum.write('\t'.join(textwrap.wrap(x[6:], width=2)))
                                dum.write('\t55\tde\tad\tbf\t5a\n')
                                
                                if (len(self.dum_data) == self.deque_length):
                                    dum_temp = self.dum_data.popleft()
                                    self.dum_left.append(dum_temp)
                                    self.dum_data.append('a5'+x[6:]+'55deadbf5a')
                                else:
                                    self.dum_data.append('a5'+x[6:]+'55deadbf5a')
                                
                            elif x[:6] == 'c3008a' and len(x[6:]) == 552: # sci (256 bytes)
                                sci.write('a5\t')
                                sci_list = textwrap.wrap(x[6:], width=2)
                                sci.write('\t'.join(sci_list))
                                sci.write('\t55\tde\tad\tbf\t5a\n')
                                t_slic_start = dt.datetime.now()
                                self.sci_hex_dec(sci_list)
                                t_slic_end = dt.datetime.now()
                                
                            elif x[:6] == 'c3010a' and len(x[6:]) == 1064 :# sci (512 bytes)
                                sci.write('a5\t')
                                sci_list = textwrap.wrap(x[6:], width=2)
                                sci.write('\t'.join(sci_list))
                                sci.write('\t55\tde\tad\tbf\t5a\n')
                                t_slic_start = dt.datetime.now()
                                self.sci_hex_dec(sci_list)
                                t_slic_end = dt.datetime.now()
                                
                            elif x[:6] == 'c3020a' and len(x[6:]) == 2088: # sci (1024 bytes)
                                sci.write('a5\t')
                                sci_list = textwrap.wrap(x[6:], width=2)
                                sci.write('\t'.join(sci_list))
                                sci.write('\t55\tde\tad\tbf\t5a\n')
                                t_slic_start = dt.datetime.now()
                                self.sci_hex_dec(sci_list)
                                t_slic_end = dt.datetime.now()
                                
                        t_slicing = t_slic_end - t_slic_start
                        
                        with open(filepath +'\\'+'time_slicing.txt','a') as f2:
                            f2.write(t_slic_start.isoformat() + '\t')
                            f2.write(t_slic_end.isoformat()+'\t')
                            f2.write(str(t_slicing.total_seconds()) + '\n')
                        
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
                        
                        self.plot_interval +=1
                else:
                    pass
            sock.close()
            print('disconnected')

    
    def sci_hex_dec(self, data):
        time_decimal = (dt.datetime(2001,1,1,9)+dt.timedelta(seconds=(int(data[6]+data[7]+data[8]+data[9], 16)))).isoformat(timespec='seconds')
        if len(self.sci_time) ==self.deque_length:
            time_temp = self.sci_time.popleft()
            self.sci_time_left.append(time_temp)
            self.sci_time.append(time_decimal)
        else:
            self.sci_time.append(time_decimal)
            
        sci_flag = data[12]
        
        if sci_flag=='40': # compression (x), extension (o), 2 * 512 = 1024 bytes
            decimal_values = list(int(data[20:20+1024][i]+data[20:20+1024][i+1], 16) for i in range(0, len(data[20:20+1024]), 2))
            if (len(self.sci_data) == self.deque_length):
                sci_temp = self.sci_data.popleft()
                self.sci_left.append(sci_temp)
                self.sci_data.append(decimal_values)
            else:
                self.sci_data.append(decimal_values)
                    
        elif sci_flag=='00': # compression (x), extension (x), 2 * 256 = 512 bytes
            decimal_values = list(int(data[20:20+512][i][0]+data[20:20+512][i+1][0], 16) for i in range(0, len(data[20:20+512]), 2))
            if (len(self.sci_data) == self.deque_length):
                sci_temp = self.sci_data.popleft()
                self.sci_left.append(sci_temp)
                self.sci_data.append(decimal_values)
            else:
                self.sci_data.append(decimal_values)
                
        elif sci_flag=='e0': # compression (o), extension (o), 1 * 512 = 512 bytes
            decimal_values = list(int(data[20:20+512][i][0], 16) for i in range(0, len(data[20:20+512]), 1))
            if (len(self.sci_data) == self.deque_length):
                sci_temp = self.sci_data.popleft()
                self.sci_left.append(sci_temp)
                self.sci_data.append(decimal_values)
            else:
                self.sci_data.append(decimal_values)
                
        elif sci_flag=='a0': # compression(o), extension (x), 1* 256 = 256 bytes
            decimal_values = list(int(data[20:20+256][i][0], 16) for i in range(0, len(data[20:20+256]), 1))
            if (len(self.sci_data) == self.deque_length):
                sci_temp = self.sci_data.popleft()
                self.sci_left.append(sci_temp)
                self.sci_data.append(decimal_values)
            else:
                self.sci_data.append(decimal_values)
                
        else:
            pass # nan list?
    
    def func_btn_plot_start(self):
        if self.fig is not None:
            plt.close(self.fig)
        self.fig = plt.figure(figsize=(10,10))
        dynamic_canvas = FigureCanvas(self.fig)
        self.verticalLayout.addWidget(dynamic_canvas)
        fontsize=10
        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.dynamic_ax.set_title("imshow", fontsize=fontsize)
        self.dynamic_ax.set_xlabel('Time', fontsize=fontsize)
        self.dynamic_ax.set_ylabel('Bins', fontsize=fontsize)
        
        self.running = True
        self.timer = dynamic_canvas.new_timer(
          5000, [(self.func_sci_plot, (), {})])
        
        if self.running:
            self.timer.start()
        else:
            self.timer.stop()
        
        
    def func_btn_plot_stop(self):
        self.running = False
    
    def func_sci_plot(self):
        t_plot_start = dt.datetime.now()
        fontsize=10
        self.dynamic_ax.clear()
        self.dynamic_ax.set_title("imshow", fontsize=fontsize)
        self.dynamic_ax.set_xlabel('Time', fontsize=fontsize)
        self.dynamic_ax.set_ylabel('Bins', fontsize=fontsize)
        s_time = pd.to_datetime(self.sci_time)
        s_data = np.array(self.sci_data)
        
        pcm = self.dynamic_ax.imshow(s_data.T, cmap='jet', aspect='auto', norm=colors.LogNorm(vmin=1, vmax=1e3),extent=[s_time[0], s_time[-1], 512, 0],interpolation='None')
        cbar = self.fig.colorbar(pcm)
        cbar.set_label('Count rates', fontsize=fontsize)
        self.dynamic_ax.invert_yaxis()
        self.dynamic_ax.figure.canvas.draw()
        major_locator = mdates.AutoDateLocator()
        minor_locator = mdates.AutoDateLocator(maxticks=4)
        self.dynamic_ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d %H:%M:%S'))
        self.dynamic_ax.xaxis.set_major_locator(major_locator)
        self.dynamic_ax.xaxis.set_minor_locator(minor_locator)
        plt.close(self.fig)
        gc.collect()
        del pcm
        
        cbar.remove()
        t_plot_end = dt.datetime.now()
        t_plot = t_plot_end - t_plot_start
        print((t_plot).total_seconds())
        with open(os.path.join(save_path0, self.lineEdit_filename.text()) +'\\'+'time_plot.txt','a') as f2:
            f2.write(t_plot_start.isoformat() + '\t')
            f2.write(t_plot_end.isoformat()+'\t')
            f2.write(str(t_plot.total_seconds()) + '\n')
    
    
        
#%% plot class
# =============================================================================
# class Plot_func(QThread):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         
#         
#     def sci_plot_start(self):
#         if self.fig is not None:
#             plt.close(self.fig)
#         self.fig = plt.figure(figsize=(10,10))
#         dynamic_canvas = FigureCanvas(self.fig)
#         self.parent.verticalLayout.addWidget(dynamic_canvas)
#         fontsize=10
#         self.dynamic_ax = dynamic_canvas.figure.subplots()
#         self.dynamic_ax.set_title("imshow", fontsize=fontsize)
#         self.dynamic_ax.set_xlabel('Time', fontsize=fontsize)
#         self.dynamic_ax.set_ylabel('Bins', fontsize=fontsize)
#         
#         self.running = True
#         self.timer = dynamic_canvas.new_timer(
#           2000, [(self.func_sci_plot, (), {})])
#         
#         if self.running:
#             self.timer.start()
#         else:
#             self.timer.stop()
#         
#     def sci_plot_stop(self):
#         self.running = False
#     
#     def func_sci_plot(self):
#         t1 = dt.datetime.now()
#         fontsize=10
#         self.dynamic_ax.clear()
#         self.dynamic_ax.set_title("imshow", fontsize=fontsize)
#         self.dynamic_ax.set_xlabel('Time', fontsize=fontsize)
#         self.dynamic_ax.set_ylabel('Bins', fontsize=fontsize)
#         s_time = pd.to_datetime(self.parent.sci_time)
#         s_data = np.array(self.parent.sci_data)
#         
#         pcm = self.dynamic_ax.imshow(s_data.T, cmap='jet', aspect='auto', norm=colors.LogNorm(vmin=1, vmax=1e3),extent=[s_time[0], s_time[-1], 512, 0],interpolation='None')
#         cbar = self.fig.colorbar(pcm)
#         cbar.set_label('Count rates', fontsize=fontsize)
#         self.dynamic_ax.invert_yaxis()
#         self.dynamic_ax.figure.canvas.draw()
#         major_locator = mdates.AutoDateLocator()
#         minor_locator = mdates.AutoDateLocator(maxticks=4)
#         self.dynamic_ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d %H:%M:%S'))
#         self.dynamic_ax.xaxis.set_major_locator(major_locator)
#         self.dynamic_ax.xaxis.set_minor_locator(minor_locator)
#         gc.collect()
#         t2 = dt.datetime.now()
#         cbar.remove()
#         print((t2-t1).total_seconds())
# =============================================================================
# =============================================================================
#     def func_btn_plot_start(self):
#         self.plot_number=0
#         fontsize=10
#         # self.canvas.clear()
#         
#         ax1.set_title("imshow", fontsize=fontsize)
#         ax1.set_xlabel('Time', fontsize=fontsize)
#         ax1.set_ylabel('Bins', fontsize=fontsize)
#         
# # =============================================================================
# #         mpl.rcParams['path.simplify_threshold'] = 1.0
# #         mpl.style.use('classic')
# #         params = {'mathtext.default': 'regular' }          
# #         plt.rcParams['font.family'] = 'Times New Roman'
# #         plt.rcParams.update(params)
# #         #
# # =============================================================================
#         # while self.plot_number==0:
#             
#             # t_plot_start = dt.datetime.now()
#             
#         s_time = pd.to_datetime(self.sci_time)
#         s_data = np.array(self.sci_data)
#         
#         pcm = self.canvas.imshow(s_data.T, cmap='jet', aspect='auto', norm=colors.LogNorm(vmin=1, vmax=1e3),extent=[s_time[0], s_time[-1], 512, 0],interpolation='None')
#         cbar = self.fig.colorbar(pcm, ax=ax1)
#         
#         ax1.invert_yaxis()
#         ax1.set_xticks(ax1.get_xticks())
#         
#         major_locator = mdates.AutoDateLocator()
#         minor_locator = mdates.AutoDateLocator(maxticks=4)
#         
#         ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d %H:%M:%S'))
#         ax1.xaxis.set_major_locator(major_locator)
#         ax1.xaxis.set_minor_locator(minor_locator)    
#         
#         cbar.set_label('Count rates', fontsize=fontsize)
#         self.canvas.draw()
#         self.canvas.ax1.clear()
#         gc.collect()
#         cbar.remove()
#                 
#                 # t_plot_end = dt.datetime.now()
#                 
#                 # t_plot = t_plot_end - t_plot_start
#                 
#                 # with open(self.filepath +'\\'+'time_plot.txt','a') as f2:
#                 #     f2.write(t_plot_start.isoformat() + '\t')
#                 #     f2.write(t_plot_end.isoformat()+'\t')
#                 #     f2.write(str(t_plot.total_seconds()) + '\n')
#                 
#                 # self.plot_interval =0
# =============================================================================
    
#%% GUI main
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    sys.exit(app.exec_())