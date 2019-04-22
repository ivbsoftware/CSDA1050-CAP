import warnings
warnings.filterwarnings('ignore')

import requests
import lxml.html as lh

gdelt_base_url = 'http://data.gdeltproject.org/events/'

# Get the list of all the links on the gdelt file page
page = requests.get(gdelt_base_url+'index.html')
doc = lh.fromstring(page.content)
link_list = doc.xpath("//*/ul/li/a/@href")

# separate out those links that begin with four digits
file_list = [x for x in link_list if str.isdigit(x[0:4])]

# preview the list
print(file_list[0:5])

# Input Data
# geo-fence
lt1 = 43.403221
lt2 = 43.855401
lg1 = -79.639319
lg2 = -78.905820

# days back to process
days_back = 5

# Extract Relevant GDELT Rows
import os.path
import urllib
import zipfile
import glob
import operator

infilecounter = 0
outfilecounter = 0

dir_path = os.getcwd()
print('Working dir: ' + dir_path)

# make some dirs
local_path = dir_path + '\\data\\'
if not os.path.exists(local_path + 'gdelt-zips'):
    os.makedirs(local_path + 'gdelt-zips')
if not os.path.exists(local_path + 'gta-data'):
    os.makedirs(local_path + 'gta-data')

for compressed_file in file_list[infilecounter:]:
    print('gdelt-zips\\' + compressed_file),

    # if we dont have the compressed file stored locally, go get it. Keep trying if necessary.
    while not os.path.isfile(local_path + 'gdelt-zips\\' + compressed_file):
        print('...downloading,'),
        urllib.request.urlretrieve(url=gdelt_base_url + compressed_file,
                                   filename=local_path + 'gdelt-zips\\' + compressed_file)

    # extract the contents of the compressed file to a temporary directory
    print('...extracting,'),
    z = zipfile.ZipFile(file=local_path + 'gdelt-zips\\' + compressed_file, mode='r')
    z.extractall(path=local_path + 'tmp/')

    # parse each of the csv files in the working directory,
    print('...parsing,'),
    for infile_name in glob.glob(local_path + 'tmp/*'):

        # create only new files
        fdate = compressed_file.split(".")[0]
        fname ='gta.' + fdate + '.tsv'
        outfile_name = local_path + 'gta-data\\' + fname
        if os.path.exists(outfile_name):
            continue

        # open the infile and outfile
        with open(infile_name, mode='r', encoding="utf8") as infile, \
                open(outfile_name, mode='w', encoding="utf8") as outfile:

            for line in infile:
                vals = line.split('\t')

                # extract geo-coordinates
                try:
                    lat = float(vals[53])  # ActionGeo_Lat
                    long = float(vals[54])  # ActionGeo_Long
                except Exception as e:
                    # means no coordinates provided, skipping
                    continue

                # only use events inside geo-fence
                if long >= lg1 and long <= lg2 and lat >= lt1 and lat <= lt2:
                    outfile.write(line)

            outfilecounter += 1

        # delete the temporary file
        os.remove(infile_name)

    infilecounter += 1
    if infilecounter >= days_back:
        print('done')
        break

# Create dataframe with GDELT news info
import glob
import pandas as pd

# Get the GDELT field names from an external helper file
colnames = pd.read_excel('data/CSV.header.fieldids.xlsx', sheet_name='Sheet1',
                         index_col='Column ID', usecols=1)['Field Name']

# Build DataFrames from each of the intermediary files
files = glob.glob(local_path + 'gta-data/' + '*')
DFlist = []
for active_file in files:
    print(active_file)
    DFlist.append(pd.read_csv(active_file, sep='\t', header=None, dtype=str,
                              names=colnames, index_col=['GLOBALEVENTID']))

# Merge the file-based dataframes and serialize the dataframe
DF = pd.concat(DFlist)
DF.to_pickle(local_path + 'backup' + '-gta' + '.pickle')

# remove the temporary files
for active_file in files:
    os.remove(active_file)

# Text cleaning function
import spacy
from spacy.lang.en import English

parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

# Use NLTK’s Wordnet to find the meanings of words
import nltk

nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

# Filter out stop words
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

# Function to prepare the text for topic modelling
def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


# For each news link
from newspaper import Article
import random

dfc = DF.sort_values('SOURCEURL').groupby('SOURCEURL').first()
print("Found " + str(len(dfc)) + " unique news links")

text_data = []
for index, row in dfc.iterrows():
    print(row.name)

    try:
        # get article text
        article = Article(row.name)
        article.download()
        article.parse()

        # extract tokensm show some
        tokens = prepare_text_for_lda(article.text)
        if random.random() > .5:
            print(tokens[1:10])

        text_data.append(tokens)
    except Exception as e:
        print("Some error processing the URL.. skipped")
        continue

# Serialize the dataframe to disk
import pickle
pickle.dump(dfc, open('gdelt-corpus-v1.pkl', 'wb'))

# Identify unique news locations
locs  = DF.groupby(['ActionGeo_Lat','ActionGeo_Long'], as_index=False).first() \
    [['ActionGeo_Lat','ActionGeo_Long','ActionGeo_FullName']]

print (locs)