# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 10:59:39 2023

@author: kimsj
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("connect_commander.ui")[0]


class Connect_cmd(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

# open window

if __name__ == "__main__" :

    app = QApplication(sys.argv) 
    myWindow = Connect_cmd() 
    myWindow.show()
    app.exec_()