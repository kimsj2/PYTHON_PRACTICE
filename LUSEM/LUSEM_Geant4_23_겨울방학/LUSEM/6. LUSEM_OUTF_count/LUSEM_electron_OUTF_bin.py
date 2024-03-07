import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("LUSEM_electron.csv")
FTUO = data[['F (MeV)','T (MeV)','U (MeV)','O (MeV)']]
event_num = 1000
FTUO = FTUO[:event_num]
FTUO_sum = FTUO.sum(axis=1)

ax = sns.distplot