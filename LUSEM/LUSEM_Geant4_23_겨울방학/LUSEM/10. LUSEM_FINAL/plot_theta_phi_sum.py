import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import math
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error : Creating directory. "+ directory)


folder1 = 'detail_data_gps_200000_1'+'/'
folder2 = 'detail_data_gps_200000_2'+'/'
folder3 = 'detail_data_gps_300000_1'+'/'
folder4 = 'detail_data_gps_300000_2'+'/'
folder = 'plot_for_1000000' + '/'

file = 'LUSEM_incident.csv'

figure_directory = folder + 'theta_phi_plot'


df1 = pd.read_csv(folder1+file)
df2 = pd.read_csv(folder2+file)
df3 = pd.read_csv(folder2+file)
df4 = pd.read_csv(folder2+file)

df12 = pd.concat([df1,df2])
df123 = pd.concat([df12,df3])
df = pd.concat([df123, df4])

createFolder(figure_directory)


x = df['x']
y = df['y']
z = df['z']

theta = df['theta']
phi = df['phi']

bin_list_1 = [i for i in range(181)]
bin_list_2 = [i for i in range(361)]

fontsize = 30

# Theta distribution
plt.figure(figsize=(20,16))
plt.hist(theta, bins=181)
plt.xticks([0,90,180])
plt.xlabel("Theta (deg)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('Theta Distribution',fontsize=fontsize)
plt.grid()
plt.savefig(figure_directory+'/'+'Theta Distribution.png')
plt.clf()

# Phi distribution
plt.figure(figsize=(20,16))
plt.hist(phi, bins=361)
plt.xticks([-180,0,180])
plt.xlabel("Phi (deg)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('Phi Distribution',fontsize=fontsize)
plt.grid()
plt.savefig(figure_directory+'/'+'Phi Distribution.png')
plt.clf()

# X distribution
plt.figure(figsize=(20,16))
plt.hist(x, bins=361)
plt.xlabel("x (cm)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('x Distribution',fontsize=fontsize)
plt.grid()
plt.savefig(figure_directory+'/'+'x Distribution.png')
plt.clf()

# Y distribution
plt.figure(figsize=(20,16))
plt.hist(y, bins=361)
plt.xlabel("y (cm)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('y Distribution',fontsize=fontsize)
plt.grid()
plt.savefig(figure_directory+'/'+'y Distribution.png')
plt.clf()

# Z distribution
plt.figure(figsize=(20,16))
plt.hist(z, bins=361)
plt.xlabel("z (cm)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('z Distribution',fontsize=fontsize)
plt.grid()
plt.savefig(figure_directory+'/'+'z Distribution.png')
plt.clf()




