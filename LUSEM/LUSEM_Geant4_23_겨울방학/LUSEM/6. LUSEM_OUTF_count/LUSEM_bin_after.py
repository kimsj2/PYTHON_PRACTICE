import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error : Creating directory. "+ directory)


directory = 'detail_data(2024-02-08_14-33-26)'+'/'

figure_directory = directory + 'figure_picture_histo/'
createFolder(figure_directory)

fontsize = 20
df = pd.read_csv(directory+'LUSEM_main.csv')

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
counts, bins, _ = plt.hist(detected_energy,bins=500)

max_count_index = np.argmax(counts)
most_frequent_bin = bins[max_count_index]

max_count = np.max(counts)

plt.text(most_frequent_bin, max_count, f'{round(most_frequent_bin,4)} / {max_count}', ha='center', va='bottom',fontsize = fontsize-5)

plt.xlabel("Energy [keV]",fontsize=fontsize)
plt.ylabel("Frequency",fontsize=fontsize)
plt.title("Detected energy histogram",fontsize=fontsize)
plt.savefig(directory+'figure_picture_histo/detected_energy_histogram.png')

plt.clf()


main_columns = ['particle_name', 'config','Incident_energy','Detected_energy','start_time','end_time','total_time']
bin_columns = ['Incident_energy','Detected_energy','F','O','FT','UO','FTU','TUO','FTUO'] # 'T','U','FU','FO','TU','TO','FTO','FUO'

df_right_logic = {}
# df_datalist = {}
df_total_datalist = {}

Emin = 10
Emax = 10000
Einterval = 1

df_bin = pd.read_csv(directory+'LUSEM_bin.csv')

x = [Emin + i for i in range(0, Emax - Emin + 1, Einterval)]
for i in range(len(bin_columns)):
    bin_list = list(df_bin[bin_columns[i]])
    plt.figure(figsize=(40,16))
    # sns.set_theme(style="whitegrid")
    # sns.barplot(x=x,y=bin_list)
    plt.bar(x,bin_list)
    dic = {bin_list:x for x, bin_list in zip(x,bin_list)}
    plt.text(dic[max(bin_list)],max(bin_list), f'{dic[max(bin_list)]} / {max(bin_list)}',ha='center', va='bottom',fontsize = fontsize-5)
    plt.xticks([Emin] + list(range(500, Emax, 500)))
    plt.xlabel("energy [keV]",fontsize=fontsize)
    plt.ylabel("Frequency",fontsize=fontsize)
    plt.title(f"Histogram {bin_columns[i]} bins",fontsize=fontsize)
    plt.savefig(directory+ f'figure_picture_histo/hisgoram_{bin_columns[i]}.png')















