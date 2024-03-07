# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 12:02:25 2024

@author: kimsj
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("SD_final_nt_Hit.csv", skiprows=6, names=["Length (cm)", "Loss Energy (MeV)"])

plt.figure(figsize=(10, 9))

path_length = df["Length (cm)"]
deposit_energy = df["Loss Energy (MeV)"]


lossEnergyperlength = deposit_energy/0.01

# plt.plot(path_length, lossEnergyperlength, label="Loss Energy (MeV) vs. path length (cm)")
# plt.xlim([0,5])
# plt.xlabel("Path length (cm)")
# plt.ylabel("Loss Energy (MeV/cm)")
# plt.title("Loss Energy (MeV/cm) vs. path length (cm)")
# plt.legend()
# plt.show()


sns.set_style('whitegrid')
# ax = sns.lineplot(x=path_length, y=lossEnergyperlength, data=df)
# ax.set(xlabel='Path length (cm)', ylabel='Stopping Power (MeV/cm)')

ax1 = sns.regplot(x=path_length, y=lossEnergyperlength, data=df, order=13, line_kws={'color': 'red'})
ax1.set(xlabel='Path length (cm)', ylabel='Stopping Power (MeV/cm)')
plt.show()

