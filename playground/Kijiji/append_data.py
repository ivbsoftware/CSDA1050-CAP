import pandas as pd
import csv
import datetime
from datetime import timedelta

csv.field_size_limit(100000000)

data_gta = pd.read_csv("kijiji_GTA.csv", sep="&=", header=None, encoding='utf-8')
data_base = pd.read_csv("kijiji_GTA_basement.csv", sep="&=", header=None, encoding='utf-8')
data_apt = pd.read_csv("kijiji_GTA_apt.csv", sep="&=", header=None, encoding='utf-8')
data_house = pd.read_csv("kijiji_GTA_house.csv", sep="&=", header=None, encoding='utf-8')
data_one = pd.read_csv("kijiji_GTA_one_bed.csv", sep="&=", header=None, encoding='utf-8')
data_two = pd.read_csv("kijiji_GTA_two_bed.csv", sep="&=", header=None, encoding='utf-8')

data_all=data_gta.append(data_base)
data_all=data_all.append(data_apt)
data_all=data_all.append(data_house)
data_all=data_all.append(data_one)
data_all=data_all.append(data_two)
#data_all=data_all.reset_index()
#data_all=data_all.drop(['unnamed 0'], axis=1)
data_all.drop_duplicates([0],keep='first',inplace=True)
#print(data_all)

ad = {'Date': '< 5 minutes ago'}
#def return_number(text):
    #return [int(s) for s in text.split() if s.isdigit()]#you can add a test to see "if minutes" is in the text
#def return_postdate(minutes_ago):
    #return datetime.datetime.now() - timedelta(minutes=minutes_ago[0])#can parse numbers for hours too
#minutes_ago = return_number(data_all[3].to_string())
#for m in minutes_ago:
    #data_all[3] = return_postdate(minutes_ago).date()
    # make date-posted today's date
#print(data_all[3].str.contains('ago'))
#if (data_all[3].str.contains('ago')):


data_all.to_csv("data_all_test.csv", index=False)
#data_all.to_csv("data_all.csv")

#data_t1 = pd.read_csv("test1.csv", sep="&=", header=None, encoding='utf-8')
#data_t2 = pd.read_csv("test2.csv", sep="&=", header=None, encoding='utf-8')
#data_all = data_t1.append(data_t2)
#data_all.drop_duplicates([0],keep='first',inplace=True)
#print (data_all)
#print (data_t1[0])
#print (data_t1.merge(data_t2.drop_duplicates(), on=[0], how='right', indicator=True ))

#print (data_two)
#data1.to_csv("testxx.csv")