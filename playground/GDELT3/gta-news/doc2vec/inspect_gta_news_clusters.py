import os
from os import listdir
from os.path import isfile, join
import pandas as pd

# directories
dir_path = os.getcwd()
print('Working dir: ' + dir_path)

local_path = dir_path + '\\data\\'
df = pd.read_pickle(local_path+'backup'+'-gta'+'.pickle')

daily_clusters = df.groupby(['date','cluster'])['title']

for name, group in daily_clusters:
    print("Date: ", name[0])
    print("Cluster " + str(name[1]))
    print(group)