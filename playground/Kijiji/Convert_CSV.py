
import ast
import numpy as np
import pandas as pd
import kijijiscr


ad_dict = {}
ad_dict_new = {}
df = pd.DataFrame()
file1 = open('kijiji_GTA.csv', 'ab')
file2 = open('kijiji_GTA_basement.csv', 'ab')
file3 = open('kijiji_GTA_apt.csv', 'ab')
file4 = open('kijiji_GTA_house.csv', 'ab')
file5 = open('kijiji_GTA_one_bed.csv', 'ab')
file6 = open('kijiji_GTA_two_bed.csv', 'ab')
with open('kijiji_GTA.txt', 'rb') as file:
     for line in file:
         if line.strip() != '':
            index = line.find('{'.encode('utf-8'))
            ad_id = line[:index].decode('utf-8')
            dictionary = line[index:].decode('utf-8')
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
            ad_dict_new = str(ad_id).strip()
            ad_dict_new += '&='+ad_dict[ad_id]['Title'].replace("\n", '').strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Url'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Date'].strip()
            ad_dict_new += '&=' +ad_dict[ad_id]['Location'].strip()
            ad_dict_new += '&=' + "NA"
            ad_dict_new += '&=' +str(ad_dict[ad_id]['Price']).strip() + "\n"
           # print(ad_dict_new)
         file1.write(ad_dict_new.encode('utf-8'))
file1.close()

with open('kijiji_GTA_basement.txt', 'rb') as file:
    for line in file:
        if line.strip() != '':
            index = line.find('{'.encode('utf-8'))
            ad_id = line[:index].decode('utf-8')
            dictionary = line[index:].decode('utf-8')
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
            ad_dict_new = str(ad_id).strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Title'].replace("\n", '').strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Url'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Date'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Location'].strip()
            ad_dict_new += '&=' + "basement"
            ad_dict_new += '&=' + str(ad_dict[ad_id]['Price']).strip() + "\n"
            #print(ad_dict_new)
        file2.write(ad_dict_new.encode('utf-8'))
file2.close()

with open('kijiji_GTA_apt.txt', 'rb') as file:
    for line in file:
        if line.strip() != '':
            index = line.find('{'.encode('utf-8'))
            ad_id = line[:index].decode('utf-8')
            dictionary = line[index:].decode('utf-8')
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
            ad_dict_new = str(ad_id).strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Title'].replace("\n", '').strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Url'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Date'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Location'].strip()
            ad_dict_new += '&=' + "apt"
            ad_dict_new += '&=' + str(ad_dict[ad_id]['Price']).strip() + "\n"
            #print(ad_dict_new)
        file3.write(ad_dict_new.encode('utf-8'))
file3.close()

with open('kijiji_GTA_house.txt', 'rb') as file:
    for line in file:
        if line.strip() != '':
            index = line.find('{'.encode('utf-8'))
            ad_id = line[:index].decode('utf-8')
            dictionary = line[index:].decode('utf-8')
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
            ad_dict_new = str(ad_id).strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Title'].replace("\n", '').strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Url'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Date'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Location'].strip()
            ad_dict_new += '&=' + "house"
            ad_dict_new += '&=' + str(ad_dict[ad_id]['Price']).strip() + "\n"
            #print(ad_dict_new)
        file4.write(ad_dict_new.encode('utf-8'))
file4.close()

with open('kijiji_GTA_one_bed.txt', 'rb') as file:
    for line in file:
        if line.strip() != '':
            index = line.find('{'.encode('utf-8'))
            ad_id = line[:index].decode('utf-8')
            dictionary = line[index:].decode('utf-8')
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
            ad_dict_new = str(ad_id).strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Title'].replace("\n", '').strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Url'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Date'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Location'].strip()
            ad_dict_new += '&=' + "one_bed"
            ad_dict_new += '&=' + str(ad_dict[ad_id]['Price']).strip() + "\n"
            #print(ad_dict_new)
        file5.write(ad_dict_new.encode('utf-8'))
file5.close()

with open('kijiji_GTA_two_bed.txt', 'rb') as file:
    for line in file:
        if line.strip() != '':
            index = line.find('{'.encode('utf-8'))
            ad_id = line[:index].decode('utf-8')
            dictionary = line[index:].decode('utf-8')
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
            ad_dict_new = str(ad_id).strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Title'].replace("\n", '').strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Url'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Date'].strip()
            ad_dict_new += '&=' + ad_dict[ad_id]['Location'].strip()
            ad_dict_new += '&=' + "two_bed"
            ad_dict_new += '&=' + str(ad_dict[ad_id]['Price']).strip() + "\n"
            #print(ad_dict_new)
        file6.write(ad_dict_new.encode('utf-8'))
file6.close()



