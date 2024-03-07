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


directory1 = 'detail_data_gps_200000_1'+'/'
directory2 = 'detail_data_gps_200000_2'+'/'
directory3 = 'detail_data_gps_300000_1'+'/'
directory4 = 'detail_data_gps_300000_2'+'/'


figure_directory = 'plot_for_1000000' + '/figure_picture_histo'
createFolder(figure_directory)

fontsize = 30

df1 = pd.read_csv(directory1+'LUSEM_main.csv')
df2 = pd.read_csv(directory2+'LUSEM_main.csv')
df3 = pd.read_csv(directory3+'LUSEM_main.csv')
df4 = pd.read_csv(directory4+'LUSEM_main.csv')

df12 = pd.concat([df1, df2], ignore_index=True)
df123 = pd.concat([df12, df3], ignore_index=True)
df = pd.concat([df123, df4],  ignore_index=True)

incident_energy = df["Incident_energy"]
detected_energy = df["Detected_energy"]

r_detected_energy = []
r_incident_energy = []

for i in range(len(detected_energy)):
    if detected_energy[i]!=0:
        r_detected_energy.append(detected_energy[i])
        r_incident_energy.append(incident_energy[i])

# incident energy vs detected energy
plt.figure(figsize=(20,16))
plt.scatter(r_incident_energy, r_detected_energy, alpha=0.5)
plt.xlabel("Incident energy [keV]",fontsize=fontsize)
plt.ylabel("Detected energy [keV]",fontsize=fontsize)
plt.xlim(0,10000)
plt.ylim(0,10000)
plt.grid()
plt.title("incident energy vs detected energy",fontsize=fontsize)
plt.savefig(figure_directory+'/incident energy vs detected energy.png')
plt.clf()

# # x = [i for i in range(10,10001)]

# incident energy histogram
plt.figure(figsize=(20,16))
plt.hist(incident_energy,bins=500)
plt.xlabel("Energy [keV]",fontsize=fontsize)
plt.ylabel("Frequency",fontsize=fontsize)
plt.title("Incident energy histogram",fontsize=fontsize)
plt.savefig(figure_directory+'/incident_energy_histogram.png')
plt.clf()

# detected energy histogram
plt.figure(figsize=(20,16))
counts, bins, _ = plt.hist(r_detected_energy,bins=500)
max_count_index = np.argmax(counts)
most_frequent_bin = bins[max_count_index]
max_count = np.max(counts)
plt.text(most_frequent_bin, max_count, f'{round(most_frequent_bin,4)} / {max_count}', ha='center', va='bottom',fontsize = fontsize-5)
plt.xlabel("Energy [keV]",fontsize=fontsize)
plt.ylabel("Frequency",fontsize=fontsize)
plt.title("Detected energy histogram",fontsize=fontsize)
plt.savefig(figure_directory+'/detected_energy_histogram.png')
plt.clf()


bin_columns = ['Incident_energy','Detected_energy','F','O','FT','UO','FTU','TUO','FTUO'] # 'T','U','FU','FO','TU','TO','FTO','FUO'

Emin = 10
Emax = 10000
Einterval = 1

df_bin1 = pd.read_csv(directory1+'LUSEM_bin.csv')
df_bin2 = pd.read_csv(directory1+'LUSEM_bin.csv')
df_bin3 = pd.read_csv(directory1+'LUSEM_bin.csv')
df_bin4 = pd.read_csv(directory1+'LUSEM_bin.csv')

index_values = [Emin + i for i in range(0, Emax - Emin + 1, Einterval)]
df_bin = pd.DataFrame(index=index_values)
df_bin = df_bin1 + df_bin2 + df_bin3 + df_bin4

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















