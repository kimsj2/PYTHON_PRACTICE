# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 10:59:39 2023

@author: SSIL_B104_1
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import uic


form_class = uic.loadUiType("connect_commander.ui")[0]
class Connect_cmd(QMainWindow, form_class):
    def __init__
    


self.line_edit.text()


# =============================================================================
# def create_main_window():
#     # 어플리케이션 생성
#     app = QApplication(sys.argv)
#     
#     # UI 파일 로드
#     ui_file = r"C:\Users\SSIL_B104_1\Desktop\자료 수신 장치\LUSEM_GUI\connect_cmd\connect_commander.ui"  # your_ui_file.ui에는 실제 UI 파일 경로를 입력하세요
#     window = QMainWindow()
#     loadUi(ui_file, window)
#     
#     # 버튼 클릭 시 동작 설정
#     def new_button_clicked():
#         print("New button clicked")
#     
#     def write_to_button_clicked():
#         window.
#     
#     def connect_to_button_clicked():
#         print("Connect to button clicked")
#         
#     
#     # 버튼 시그널과 슬롯 연결
#     window.pushButton.clicked.connect(new_button_clicked)
#     window.pushButton_2.clicked.connect(write_to_button_clicked)
#     window.pushButton_4.clicked.connect(connect_to_button_clicked)
#     
#     # 창 실행
#     window.show()
#     
#     # 어플리케이션 실행
#     app.exec_()
#     
#     
#     
# create_main_window()
# =============================================================================

