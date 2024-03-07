# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:41:57 2024

@author: kimsj
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Particle_position_nt_step.csv", skiprows=7, names=["events", "Path length (cm)","step length (cm)",
                                                                     "Loss Energy (MeV)", "Total Energy (MeV)"])

plt.figure(figsize=(10, 9))

path_length = df["Path length (cm)"]
step_length = df["step length (cm)"]
deposit_energy = df["Loss Energy (MeV)"]

lossEnergyperlength = deposit_energy/step_length

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

# ax1 = sns.regplot(x=path_length, y=lossEnergyperlength, data=df, order=17, line_kws={'color': 'red'})
# ax1.set(xlabel='Path length (cm)', ylabel='Stopping Power (MeV/cm)')
plt.show()

