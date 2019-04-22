import nltk, codecs
from gensim.models import Doc2Vec
from nltk.cluster.kmeans import KMeansClusterer
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
from nltk.corpus import stopwords
import datetime

NUM_CLUSTERS = 10

# directories
dir_path = os.getcwd()
print('Working dir: ' + dir_path)

local_path = dir_path + '\\data\\'
corpus_files_path = local_path + 'gta-gdelt-corpus'
if not os.path.exists(corpus_files_path):
    print('Working dir does not exist: ' + corpus_files_path)
    exit(-1)

fname = "data/news-dataset-huffington.model"
model = Doc2Vec.load(fname)

# GTA corpus files in reverse ordrer
files = [f for f in listdir(corpus_files_path) if isfile(join(corpus_files_path, f))]
files.sort(reverse=True)
print (files)

# for each daily file
DFlist = []
vectors = []
for active_file in files:
    print("Processing: " + active_file)

    corpus = codecs.open(corpus_files_path + '\\' + active_file, mode="r", encoding="utf-8")
    lines = corpus.read().lower().split("\n")

    urls = []
    titles = []
    dates = []

    for t in lines:
        # parse document token and label from the line
        res = t.split('], [')
        doc = res[0].strip('\'][\'')
        doc = doc.split('\', \'')
        if len(doc) < 10:
            continue

        url = res[1].strip('\'][\'')
        title = res[2].strip('\'][\'')

        fdate = active_file.split(".")[1]
        date = datetime.datetime.strptime(fdate, "%Y%m%d")

        urls.append(url)
        titles.append(title)
        dates.append(date)
        vectors.append(model.infer_vector(doc))

    # this day dataframe object
    df = pd.DataFrame({"date": dates,
                       "url": urls,
                       "title": titles,
                       })
    DFlist.append(df)

count = len(vectors)
print ("Vectors infered: ", count)

# K-means clustering of news articles
print ("Preparing clusters")
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)

# Merge the file-based dataframes and serialize the dataframe
print ("Merge the file-based dataframes and serialize the dataframe")
DF = pd.concat(DFlist)
DF['cluster'] = assigned_clusters
DF.to_pickle(local_path+'backup'+'-gta.2'+'.pickle')

print("Done")