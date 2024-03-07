# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:29:18 2023

@author: kimsj
"""

# Extension에 맞추어 parsing 하도록 코드 수정

import os

def datpar(filename, savepath):
    directory = savepath + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + "soh.txt", "w") as SOH, \
            open(directory + "sci.txt", "w") as SCI, \
            open(directory + "noi.txt", "w") as NOI, \
            open(directory + "dum.txt", "w") as DUM:
                
        with open(filename, 'r') as f:
            while True:
                bytedata = f.readline(2)
                if not bytedata:
                    break

                if bytedata == 'a8':
                    bytedata = f.readline(2)
                    if bytedata == '29':
                        bytedata = f.readline(2)
                        if bytedata == '00':
                            bytedata = f.readline(2)
                            if bytedata == 'c3':
                                bytedata = f.readline(2)
                                if bytedata == '00':
                                    bytedata = f.readline(2)
                                    if bytedata == '26':
                                        SOH.write("a5\t")
                                        bytedata = f.readline(76 * 2).upper()
                                        for i in range(76):
                                            SOH.write(bytedata[2*i:2*i+2].upper()+"\t")
                                        SOH.write("55\tde\tad\tbf\t5a\n")
                                    elif bytedata == '5a':
                                        NOI.write("a5\t")
                                        bytedata = f.readline(180 * 2)
                                        for i in range(180):
                                            NOI.write(bytedata[2*i:2*i+2].upper()+'\t')
                                        NOI.write("55\tde\tad\tbf\t5a\n")
                                    elif bytedata == '8a':
                                        bytedata = f.readline(13 * 2)
                                        if bytedata[-2:] == "a0":
                                            print('256')
                                            SCI.write("a5\t")
                                            for i in range(6):
                                                SCI.write(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                            bytedata = f.readline((256 + 7) * 2)
                                            for i in range((256+7) ):
                                                SCI.write(bytedata[2*i:2*i+2].upper()+'\t')
                                            SCI.write("55\tde\tad\tbf\t5a\n")

                                elif bytedata == '01':
                                    bytedata = f.readline(2)
                                    if bytedata == '0a':
                                        bytedata = f.readline(13 * 2)
                                        if bytedata[-2:] == "00":
                                            print('512')
                                            SCI.write("a5\t")
                                            for i in range(6):
                                                SCI.write(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                            bytedata = f.readline((512 + 7) * 2)
                                            for i in range((512+7)):
                                                SCI.write(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                            SCI.write("55\tde\tad\tbf\t5a\n")

                                elif bytedata == '02':
                                    bytedata = f.readline(2)
                                    if bytedata == '0a':
                                        print('1024')
                                        SCI.write("a5\t")
                                        bytedata = f.readline((1024 + 20) * 2)
                                        for i in range(1024+20):
                                            SCI.write(bytedata[2*i:2*i+2].upper()+'\t')
                                        SCI.write("55\tde\tad\tbf\t5a\n")

                                elif bytedata == '04':
                                    bytedata = f.readline(2)
                                    if bytedata == '0c':
                                        DUM.write("a5\t")
                                        bytedata = f.readline(2072 * 2)
                                        for i in range(2072):
                                            DUM.write(bytedata[2*i:2*i+2].upper()+'\t')
                                        DUM.write("55\tde\tad\tbf\t5a\n")

                            elif bytedata == 'c1':
                                bytedata = f.readline(2)
                                if bytedata == '00':
                                    bytedata = f.readline(2)
                                    if bytedata == '0c':
                                        f.readline(24 * 2)

    return directory
#name = 'aobo0_ao_am241_bo_ba133.dat'
#datpar(filename=r'E:\1. Graduate\2. Project\LUSEM\2. Test\Plot code\aobo0_ao_am241_bo_ba133/'+name,savepath=r"E:\1. Graduate\2. Project\LUSEM\2. Test\Plot code\aobo0_ao_am241_bo_ba133/")