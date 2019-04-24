import os.path
from os import listdir
from os.path import isfile, join
import pandas as pd
from newspaper import Article
import random
import d2v_utils

# directories
dir_path = os.getcwd()
print('Working dir: ' + dir_path)

local_path = dir_path + '\\data\\'
links_files_path = local_path + 'gta-gdelt-data'
if not os.path.exists(links_files_path):
    print('Working dir does not exist: ' + links_files_path)
    exit(-1)

# files with GTA links in reverse ordrer
files = [f for f in listdir(links_files_path) if isfile(join(links_files_path, f))]
files.sort(reverse=True)
print (files)

# Get the GDELT field names from an external helper file
colnames = pd.read_excel('data/CSV.header.fieldids.xlsx', sheet_name='Sheet1',
                         index_col='Column ID', usecols=1)['Field Name']
print (colnames)


# output folder
gta_gdelt_corpus_dir = local_path + 'gta-gdelt-corpus'
if not os.path.exists(gta_gdelt_corpus_dir):
    os.makedirs(gta_gdelt_corpus_dir)

# for each GDELT news links daily file
for active_file in files:
    print("Processing: " + active_file)
    dfc = pd.read_csv(
        links_files_path+'\\'+active_file, sep='\t', header=None, dtype=str,
        names=colnames, index_col=['GLOBALEVENTID'])

    dfc = dfc.sort_values('SOURCEURL').groupby('SOURCEURL').first()
    print("... found " + str(len(dfc)) + " unique news links")

    # Identify unique news locations
    locs  = dfc.groupby(['ActionGeo_Lat','ActionGeo_Long'], as_index=False).first() \
        [['ActionGeo_Lat','ActionGeo_Long','ActionGeo_FullName']]
    print ("... unique locations: ")
    print (locs)

    # for each article
    # create only new files
    fdate = active_file.split(".")[1]
    fname = 'gta.' + fdate + '.txt'
    outfile_name = gta_gdelt_corpus_dir + '\\' + fname
    if os.path.exists(outfile_name):
        continue

    # open the infile and outfile
    with open(outfile_name, mode='w', encoding="utf8") as outfile:
        for index, row in dfc.iterrows():
            print(row.name)

            try:
                # get article text
                article = Article(row.name)
                article.download()
                article.parse()

                # extract tokens, show some
                tokens = d2v_utils.prepare_text_for_lda(article.text)
                if random.random() > .5:
                    print(tokens[1:10])

                #TODO:
                # skip_terms =['toronto','canada','canadian','ontario']
                # tokens = [word for word in tokens if word not in skip_terms and not word.isdigit()]
                # add AvgTone and some other items
                # use JSON ?

                # save article record
                if len(tokens) > 10:
                    line = str([tokens, [index], [article.title]]) + "\n"
                    outfile.write(line)
                    outfile.flush()

            except Exception as e:
                print("Some error processing the URL.. skipped")
                continue

print ('done')