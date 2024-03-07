import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error : Creating directory. "+ directory)


directory = 'detail_data_100000_count/'

figure_directory = directory + 'figure_picture_histo/'
createFolder(figure_directory)

fontsize = 20
df = pd.read_csv(directory+'LUSEM_electron_main.csv')

incident_energy = df["Incident_energy"]
detected_energy = df["Detected_energy"]

# incident energy vs detected energy
plt.figure(figsize=(20,16))
plt.scatter(incident_energy, detected_energy, alpha=0.5)
plt.xlabel("Incident energy [keV]",fontsize=fontsize)
plt.ylabel("Detected energy [keV]",fontsize=fontsize)
plt.xlim(0,10000)
plt.ylim(0,10000)
plt.grid()
plt.title("incident energy vs detected energy",fontsize=fontsize)
plt.savefig(directory+'figure_picture_histo/incident energy vs detected energy.png')

plt.clf()

# # x = [i for i in range(10,10001)]

# incident energy histogram
plt.figure(figsize=(20,16))
plt.hist(incident_energy,bins=500)
plt.xlabel("Energy [keV]",fontsize=fontsize)
plt.ylabel("Frequency",fontsize=fontsize)
plt.title("Incident energy histogram",fontsize=fontsize)
plt.savefig(directory+'figure_picture_histo/incident_energy_histogram.png')

plt.clf()

# detected energy histogram
plt.figure(figsize=(20,16))
plt.hist(detected_energy,bins=500)
plt.xlabel("Energy [keV]",fontsize=fontsize)
plt.ylabel("Frequency",fontsize=fontsize)
plt.title("Detected energy histogram",fontsize=fontsize)
plt.savefig(directory+'figure_picture_histo/detected_energy_histogram.png')

plt.clf()


right_logic = ['F','FT','FTU','FTUO','O','TUO','UO']
df_right_logic = {}
# df_datalist = {}
df_total_datalist = {}

# right logic data
for x in right_logic:
    df_right_logic[x] = pd.read_csv(directory+f'right_logic/LUSEM_electron_{x}.csv')
    # df_datalist[x]={}


logic_columns = ['F','T','U','O']

# for i in range(len(df_right_logic)):
#     for j in range(len(logic_columns)):
#         df_datalist[right_logic[i]][logic_columns[j]] =df_right_logic[right_logic[i]][logic_columns[j]]

# print(df_datalist['FTUO']['O'])

for x in right_logic:
    df_total_datalist[x] = df_right_logic[x]['F'] + df_right_logic[x]['T'] + df_right_logic[x]['U'] + df_right_logic[x]['O']

# energy distribution for each right logic
x = [i for i in range(10,10001)]
for i in range(len(right_logic)):
    plt.figure(figsize=(25,16))
    plt.bar(x,df_total_datalist[right_logic[i]])
    plt.xticks(range(10,10001,1000))
    plt.xlabel("energy [keV]",fontsize=fontsize)
    plt.ylabel("Frequency",fontsize=fontsize)
    plt.ylim(0,1400)
    plt.title(f"Histogram {right_logic[i]} bins",fontsize=fontsize)
    plt.savefig(directory+f'figure_picture_histo/hisgoram_{right_logic[i]}_bins.png')
    


