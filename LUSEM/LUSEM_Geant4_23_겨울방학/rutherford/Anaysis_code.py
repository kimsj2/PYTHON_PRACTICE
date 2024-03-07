# -*- coding: utf-8 -*-
"""
Created on Fri Jan 5 10:15:49 2024

@author: kimsj
"""

import pandas as pd

detector_num = 5

df = pd.read_csv("Particle_position_nt_step.csv", skiprows=9,names=["events","x (cm)","y (cm)","z (cm)","VolumeID"])

column_5_values = df.iloc[:, 4]
df2 = df[column_5_values != detector_num]


df2.to_csv("Exception_for_Particle_position_nt_step.csv",index=False)


