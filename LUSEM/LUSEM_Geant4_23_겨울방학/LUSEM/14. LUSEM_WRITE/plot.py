import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error : Creating directory. "+ directory)


directory = 'detail_data_write_final_1000000'+'/'

figure_directory = directory + 'figure_picture_histo'
createFolder(figure_directory)


bin_directory = '/bin_plot'
createFolder(figure_directory+bin_directory)

fontsize = 30
fontsize_tick = 20

particle_type = []
incident_energy = []
logic = []
detected_energy = []
r_incident_energy = []
r_detected_energy = []

Emin = 10
Emax = 10000
Einterval = 1

with open(directory+"Incident_energy.txt",'r') as f:
    for line in f:
        data = line.strip().split('\t')
        particle_type.append(data[0])
        incident_energy.append(float(data[1]))
        
with open(directory+"Detected_energy.txt",'r') as f:
    for line in f:
        data = line.strip().split('\t')
        logic.append(data[0])
        detected_energy.append(float(data[1]))

for i in range(len(incident_energy)):
    if detected_energy[i] >= Emin:
        r_incident_energy.append(incident_energy[i])
        r_detected_energy.append(detected_energy[i])

# # incident vs detected energy
plt.figure(figsize=(20,16))
plt.scatter(r_incident_energy, r_detected_energy, alpha=0.5)
plt.xlabel("Incident energy [keV]",fontsize=fontsize)
plt.ylabel("Detected energy [keV]",fontsize=fontsize)
plt.xlim(0,10000)
plt.ylim(0,10000)
plt.xticks(fontsize= fontsize_tick)
plt.yticks(fontsize= fontsize_tick)
plt.grid()
plt.title("Incident energy vs Detected energy",fontsize=fontsize)
plt.savefig(figure_directory+'/incident energy vs detected energy.png')
plt.clf()

# # incident energy histogram
plt.figure(figsize=(20,16))
plt.hist(incident_energy,bins=500)
plt.xlabel("Energy [keV]",fontsize=fontsize)
plt.ylabel("Counts",fontsize=fontsize)
plt.xticks(fontsize= fontsize_tick)
plt.yticks(fontsize= fontsize_tick)
plt.title("Incident energy histogram",fontsize=fontsize)
plt.savefig(figure_directory+'/incident_energy_histogram.png')
plt.clf()

# # detected energy histogram
plt.figure(figsize=(20,16))
counts, bins, _ = plt.hist(r_detected_energy,bins=100)
max_count_index = np.argmax(counts)
most_frequent_bin = bins[max_count_index]
max_count = np.max(counts)
plt.text(most_frequent_bin, max_count, f'{round(most_frequent_bin,4)} / {max_count}', ha='center', va='bottom',fontsize = fontsize-5)
plt.xlabel("Energy [keV]",fontsize=fontsize)
plt.ylabel("Counts",fontsize=fontsize)
plt.xticks(fontsize= fontsize_tick)
plt.yticks(fontsize= fontsize_tick)
plt.title("Detected energy histogram",fontsize=fontsize)
plt.savefig(figure_directory+'/detected_energy_histogram.png')
plt.clf()

# bin plot
df_bins = pd.read_csv(directory+'LUSEM_bin.csv')
bin_columns = ['Incident_energy','Detected_energy','F','O','FT','UO','FTU','TUO','FTUO'] # 'T','U','FU','FO','TU','TO','FTO','FUO'

x = [Emin + i for i in range(0, Emax - Emin + 1, Einterval)]

for i in range(len(bin_columns)):
    bin_list = list(df_bins[bin_columns[i]])
    plt.figure(figsize=(40,16))
    # sns.set_theme(style="whitegrid")
    # ax = sns.barplot(x=x,y=bin_list)
    plt.bar(x,bin_list)
    dic = {bin_list:x for x, bin_list in zip(x,bin_list)}
    plt.text(dic[max(bin_list)],max(bin_list), f'{dic[max(bin_list)]} / {max(bin_list)}',ha='center', va='bottom',fontsize = fontsize-5)
    plt.xticks(([Emin] + list(range(500, Emax, 500))), fontsize= fontsize_tick)
    plt.xlabel("energy [keV]",fontsize=fontsize)
    plt.ylabel("Counts",fontsize=fontsize)
    plt.yticks(fontsize= fontsize_tick)
    plt.title(f"Histogram_bin {bin_columns[i]} bins",fontsize=fontsize)
    plt.savefig(figure_directory+ bin_directory+f'/hisgoram_bin_{bin_columns[i]}.png')















