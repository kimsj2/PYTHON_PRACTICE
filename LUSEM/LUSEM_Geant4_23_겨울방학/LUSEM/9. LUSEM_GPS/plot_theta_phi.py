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


folder = 'detail_data_gps_10000_(2024-02-16_15-12-13)'+'/'
file = 'LUSEM_incident.csv'
figure_directory = folder + 'theta_phi_plot'
df = pd.read_csv(folder+file)

createFolder(figure_directory)

position = df['position']
momentum = df['momentum_direction']
theta = df['theta']
phi = df['phi']
bin_list_1 = [i for i in range(181)]
bin_list_2 = [i for i in range(361)]

fontsize = 20

def only_numbers(s):
    numbers = re.findall(r'-?\d+\.?\d*', s)
    return numbers

# -?: 음수 기호가 있거나 없음을 나타냅니다.
# \d+: 하나 이상의 숫자를 나타냅니다.
# \.?: 소수점이 있거나 없음을 나타냅니다.
# \d*: 소수점 뒤에 하나 이상의 숫자가 올 수 있습니다.

position_split = position.apply(only_numbers)
position_x = []
position_y = []
position_z = []

for i in range(len(position_split)):
    position_x.append(float(position_split[i][0]))
    position_y.append(float(position_split[i][1]))
    position_z.append(float(position_split[i][2]))

momentum_split = momentum.apply(only_numbers)
momentum_x = []
momentum_y = []
momentum_z = []

for i in range(len(momentum_split)):
    momentum_x.append(float(momentum_split[i][0]))
    momentum_y.append(float(momentum_split[i][1]))
    momentum_z.append(float(momentum_split[i][2]))

# cal_theta = []
# cal_phi = []

# for i in range(len(momentum_x)):
#     cal_theta.append(180/(math.pi)*np.arccos(momentum_x[i]))
#     cal_phi.append(180/(math.pi)*np.arctan2(momentum_y[i],momentum_z[i]))

# Theta distribution

plt.figure(figsize=(20,16))
# plt.bar(theta,bin_list_1)
plt.hist(theta, bins=181)
plt.xticks([0,90,180])
# plt.xticks([-360,0,360])
plt.xlabel("Theta (deg)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('Theta Distribution',fontsize=fontsize)
plt.savefig(figure_directory+'Theta Distribution.png')

plt.clf()

# Phi distribution

plt.figure(figsize=(20,16))
# plt.bar(phi,bin_list_2)
plt.hist(phi, bins=361)
plt.xticks([-180,0,180])
# plt.xticks([-360,0,360])
plt.xlabel("Phi (deg)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('Phi Distribution',fontsize=fontsize)
plt.savefig(figure_directory+'Phi Distribution.png')

plt.clf()

# X distribution

plt.figure(figsize=(20,16))
# plt.bar(phi,bin_list_2)
plt.hist(position_x, bins=361)
plt.xlabel("x (cm)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('x Distribution',fontsize=fontsize)
plt.savefig(figure_directory+'x Distribution.png')

plt.clf()

# Y distribution

plt.figure(figsize=(20,16))
# plt.bar(phi,bin_list_2)
plt.hist(position_y, bins=361)
plt.xlabel("y (cm)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('y Distribution',fontsize=fontsize)
plt.savefig(figure_directory+'y Distribution.png')

plt.clf()

# Z distribution

plt.figure(figsize=(20,16))
# plt.bar(phi,bin_list_2)
plt.hist(position_z, bins=361)
plt.xlabel("z (cm)",fontsize=fontsize)
plt.ylabel("Number of Produced Electron (count)",fontsize=fontsize)
plt.title('z Distribution',fontsize=fontsize)
plt.savefig(figure_directory+'z Distribution.png')

plt.clf()




