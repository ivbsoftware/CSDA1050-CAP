import pandas as pd
import csv
import datetime
import subprocess
from datetime import timedelta

csv.field_size_limit(100000000)

data_all_url=pd.read_csv("data_all_test.csv", sep=",", header=None, encoding='utf-8')
test=data_all_url[2]
ct=range(test.count())
#print(data_all_url.)

for i in range(test.count()):
    print(test._ndarray_values[i])
    subprocess.call(" python Kijiji-Scraper_s.py " +test._ndarray_values[i]+" -f All_Page_Data.txt",shell=True)

print()