from os import listdir
from os.path import *

class filepath:

    def __init__(self, filedir):
        self.filedir = filedir
        self.ksem_file_path = abspath(self.filedir)
        self.filelist = [f for f in listdir(self.ksem_file_path) if isfile(join(self.ksem_file_path, f))]

    def csvfilelist(self):
        Flist = self.filelist
        csvfile=[]
        for ch in Flist:
            if '.csv' in ch:
                 csvfile.append(join(self.ksem_file_path , ch))

        return csvfile

    def binfilelist(self):
        Flist = self.filelist
        binfile= []
        for bi in Flist:
            if '.SP' in bi:
                binfile.append(join(self.ksem_file_path, bi))

        return binfile

    def txtfilelist(self):
        Flist = self.filelist
        txtfile= []
        for txt in Flist:
            if '.txt' in txt:
                txtfile.append(join(self.ksem_file_path, txt))

        return txtfile

    def datfilelist(self):
        Flist = self.filelist
        datfile = []
        for dat in Flist:
            if '.dat' in dat:
                datfile.append(join(self.ksem_file_path, dat))

        return datfile