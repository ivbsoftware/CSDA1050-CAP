import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import pickle

NUM_CLUSTERS = 50

# directories
dir_path = os.getcwd()
print('Working dir: ' + dir_path)

# Load Haffington Post doc2Vec model
local_path = dir_path + '\\data\\'
corpus_files_path = local_path + 'gta-gdelt-corpus'
if not os.path.exists(corpus_files_path):
    print('Working dir does not exist: ' + corpus_files_path)
    exit(-1)

fname = "data/news-dataset-huffington.model"
model = Doc2Vec.load(fname)

