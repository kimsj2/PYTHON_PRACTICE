import mod_filearg, os
import binascii

def datpar(filename, savepath):
    # relname = os.path.basename(filename)[:-4]
    directory = savepath + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + "soh.txt", "w") as f3, \
            open(directory + "sci.txt", "w") as f4, \
            open(directory + "noi.txt", "w") as f5, \
            open(directory + "dum.txt", "w") as f6:
                
# =============================================================================
#         hex_data = binascii.hexlify(binf.read()).decode('utf-8')
#         f2.write(hex_data)
# =============================================================================
        
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
                                        f3.write("a5\t")
                                        bytedata = f.readline(76 * 2).upper()
                                        for i in range(76):
                                            f3.write(bytedata[2*i:2*i+2].upper()+"\t")
                                        f3.write("\t55\tde\tad\tbf\t5a\n")
                                    elif bytedata == '5a':
                                        f5.write("a5\t")
                                        bytedata = f.readline(180 * 2)
                                        for i in range(180):
                                            f5.write(bytedata[2*i:2*i+2].upper()+'\t')
                                        f5.write("\t55\tde\tad\tbf\t5a\n")
                                    elif bytedata == '8a':
                                        bytedata = f.readline(6 * 2)
                                        if bytedata[-4:] == "010d":
                                            print('256')
                                            f4.write("a5\t")
                                            for i in range(6):
                                                f4.write(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                            bytedata = f.readline((256 + 8 + 6) * 2)
                                            for i in range((256+8+6) ):
                                                f4.write(bytedata[2*i:2*i+2].upper()+'\t')
                                            f4.write("\t55\tde\tad\tbf\t5a\n")

                                elif bytedata == '01':
                                    bytedata = f.readline(2)
                                    if bytedata == '0a':
                                        bytedata = f.readline(6 * 2)
                                        if bytedata[-4:] == "020d":
                                            print('512')
                                            f4.write("a5\t")
                                            for i in range(6):
                                                f4.write(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                            bytedata = f.readline((512 + 8 + 6) * 2)
                                            for i in range((512+8+6)):
                                                f4.write(bytedata[2 * i:2 * i + 2].upper() + '\t')
                                            f4.write("\t55\tde\tad\tbf\t5a\n")

                                elif bytedata == '02':
                                    bytedata = f.readline(2)
                                    if bytedata == '0a':
                                        print('1024')
                                        f4.write("a5\t")
                                        bytedata = f.readline((1024 + 20) * 2)
                                        for i in range(1024+20):
                                            f4.write(bytedata[2*i:2*i+2].upper()+'\t')
                                        f4.write("\t55\tde\tad\tbf\t5a\n")

                                elif bytedata == '04':
                                    bytedata = f.readline(2)
                                    if bytedata == '0c':
                                        f6.write("a5\t")
                                        bytedata = f.readline(2072 * 2)
                                        for i in range(2072):
                                            f6.write(bytedata[2*i:2*i+2].upper()+'\t')
                                        f6.write("\t55\tde\tad\tbf\t5a\n")

                            elif bytedata == 'c1':
                                bytedata = f.readline(2)
                                if bytedata == '00':
                                    bytedata = f.readline(2)
                                    if bytedata == '0c':
                                        f.readline(24 * 2)

    return directory
#name = 'aobo0_ao_am241_bo_ba133.dat'
#datpar(filename=r'E:\1. Graduate\2. Project\LUSEM\2. Test\Plot code\aobo0_ao_am241_bo_ba133/'+name,savepath=r"E:\1. Graduate\2. Project\LUSEM\2. Test\Plot code\aobo0_ao_am241_bo_ba133/")