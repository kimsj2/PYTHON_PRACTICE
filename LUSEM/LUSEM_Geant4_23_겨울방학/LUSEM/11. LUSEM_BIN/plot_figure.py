import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error : Creating directory. "+ directory)


directory1 = 'detail_data_gps_10000_(2024-02-16_15-12-13)'+'/'

figure_directory = 'plot_for_1000000' + '/figure_picture'

createFolder(figure_directory)

fontsize = 20

df_bin = pd.read_csv(directory1+'LUSEM_bin.csv')

incident_energy = df_bin['Incident_energy']
detected_energy = df_bin['Detected_energy']

# incident energy vs detected energy
plt.figure(figsize=(20,16))
plt.scatter(incident_energy, detected_energy, alpha=0.5)
plt.xlabel("Incident energy [keV]",fontsize=fontsize)
plt.ylabel("Detected energy [keV]",fontsize=fontsize)
plt.xlim(0,10000)
plt.ylim(0,10000)
plt.grid()
plt.title("incident energy vs detected energy",fontsize=fontsize)
plt.savefig(figure_directory+'/incident energy vs detected energy.png')
plt.clf()


bin_columns = ['Incident_energy','Detected_energy','F','O','FT','UO','FTU','TUO','FTUO'] # 'T','U','FU','FO','TU','TO','FTO','FUO'

Emin = 10
Emax = 10000
Einterval = 1

index_values = [Emin + i for i in range(0, Emax - Emin + 1, Einterval)]

for i in range(len(bin_columns)):
    bin_list = list(df_bin[bin_columns[i]])
    plt.figure(figsize=(40,16))
    # sns.set_theme(style="whitegrid")
    # sns.barplot(x=x,y=bin_list)
    plt.bar(index_values,bin_list)
    dic = {bin_list:index_values for index_values, bin_list in zip(index_values,bin_list)}
    plt.text(dic[max(bin_list)],max(bin_list), f'{dic[max(bin_list)]} / {max(bin_list)}',ha='center', va='bottom',fontsize = fontsize-5)
    plt.xticks([Emin] + list(range(500, Emax, 500)))
    plt.xlabel("energy [keV]",fontsize=fontsize)
    plt.ylabel("Frequency",fontsize=fontsize)
    plt.title(f"Histogram_bin {bin_columns[i]} bins",fontsize=fontsize)
    plt.savefig(figure_directory+ f'/hisgoram_bin_{bin_columns[i]}.png')















