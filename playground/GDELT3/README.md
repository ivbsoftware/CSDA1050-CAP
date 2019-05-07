# Visualizing GTA News Timeline
### *Igor Baranov*

## Introduction
This report is describing how to retrieve, process and present online news data related to Toronto and surrounding area (GTA). The main source of information is [The GDELT Project](https://www.gdeltproject.org/) which is a realtime network diagram and database of global human society for open research. GDELT Project monitors the world's broadcast, print, and web news from nearly every corner of every country in over 100 languages and identifies the people, locations, organizations, themes, sources, emotions, counts, quotes, images and events driving our global society every second of every day.


## Discussion

GDELT has lots of information useful for the task. GDELT designed to collect emotional and geolocational information related to the news.

One of the approaches to extract the GDELT information ([discussed here](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT/gdelt_gkg_affordable_housing.pdf)) was using Google BigQuery API. The GDELT data structure described in the [DDELT GKG DATA FORMAT CODEBOOK](http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf). The following document provides some examples of the queries to that API: [Google BigQuery + GKG 2.0: Sample Queries](https://blog.gdeltproject.org/google-bigquery-gkg-2-0-sample-queries/). Access to the API provided browsing on over to the [GKG table in BigQuery](https://bigquery.cloud.google.com/table/gdelt-bq:gdeltv2.gkg). The advantage of this approach is that it allows full text search inside the news articles which allows presise filtering of news of interest. Disadvantages of this approach are the lack of geolocational information in this dataset and high cost of the queries.

Another approach ([discussed here](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT2/proposal.md)) that is more suitable for extracting GDELT events data geo-fenced to GTA. As a proofe of concept, for each day unique GTA news links where identified, news narrative was extracted and aggregated news narrative was created. This text was tokenized and then 30 topics were being extracted using LDA. After that the topics were visualized using PyLDAViz and a single Wordcloud. This approach demonstrated that LDA generates too many topics that are difficult to analyze. It was not a useful method of classifying news articles.

To overcome the described above disadvantages, the approach of clustering the news topics and creating dynamic vizualization similar to one presented by [Hans Rosling](https://www.ted.com/talks/hans_rosling_shows_the_best_stats_you_ve_ever_seen?language=en) was attempted.

[Doc2vec](https://arxiv.org/pdf/1607.05368.pdf) is an unsupervised computer algorithm to generate vectors for sentence/paragraphs/documents. The algorithm is an adaptation of word2vec which can generate vectors for words. 

There few pre-trained Doc2Vec models are available online. One is by [Jey Han Lau](https://arxiv.org/pdf/1607.05368.pdf) was [trained on English Wikipedia](https://github.com/jhlau/doc2vec) but requires Python 2 and custom forked version of Doc2Vec library. Another one by [Google]() is also requires Python 2. 

Clustering news articles using Doc2Vec model was proven successful by [Rik Nijessen](https://towardsdatascience.com/automatic-topic-clustering-using-doc2vec-e1cea88449c). Unfortunatelly there no training data or the model are available to reproduce the research.
 
The following steps were suggested for the task:

1. For each day of the GDELT news dataset download news links and extract only GTA geo-fenced data, download HTML and extract narrative, clean and tokenize the text.
2. Find pre-trained or traing new Doc2Vec model.
3. Infer Doc2Vec vectors for each downloaded GTA news atricle using the model.
4. Cluster GTA news articles.
5. Design algorithm and extract meaningful cluster descriptions from the available data.
6. Prepare the vizualization(s).

## Doc2Vec model preparation

Python code used in this section located in [gta-news](https://github.com/ivbsoftware/CSDA1050-CAP/tree/master/playground/GDELT3/gta-news/doc2vec) folder. Below are the steps to download information for Doc2Vec model training:

### Preparing training data
Download, clean and tokenize the Haffington Post news corpus. Parameters of this script are start line number, end line number (-1 if to the end) and suffix of the file generated. This is in case multiple processes are needed to run to speed up the tokenizing.

```python
python prepare_train_corpus.py 0 -1 0 
```
### Training Doc2Vec model
 - TODO: Describe training process
 - TODO: Testing model to check if the results make sense

The script below reads __data/news-dataset.txt__ containig ~187K documents and creates Doc2Vec __news-dataset-huffington.model__ file.

```python
python train_doc2vec.py
```
### Testing the model
Test your model to check if the results make sense. Code below will run several tests.

```python
python inspect_doc2vec.py
```
### Data generated by the code
The data files generated here can be downloaded from [Google Drive](https://drive.google.com/open?id=1sXD0DDlBfDKu0AnKXqoxSb92WftFqJEo). 
It contains the following artifacts:

 - __News_Category_Dataset_v2.json__ is a list of 200K links of news articles from Haffington Post site taken from [Kaggle News Category Dataset](https://www.kaggle.com/rmisra/news-category-dataset).
 - __news-dataset.zip__ is a dataset containing cleaned tokenized articles from the source above.
 - __news-dataset-huffington.model__ is a Doc2Vec model trained on 186,513 articles (those having more than 10 tokens).
 
## Loading GDELT data related to GTA area

### Extract GDELT links related to GTA area.

The script below extracts/updates GDELT links related to GTA area. The script runs 60 days back, skipping previosly downloaded and processed files. Can be run daily to update with lates data.

```python
python get_gta_gdelt_links.py
```

### Process GTA news articles
Process files created before. Daily files are loaded, for each url the body of the article is extracted and tokenized. Each day file is saved to __data\gta-gdelt-corpus__ folder.

```python
python prepare_gdelt_articles.py
```

### Clustering GTA news articles

Loads files created on step 5 and generates 30 clusters for 60 days of the 9600 news articles. K-means clustering takes 2 hours on double Xeon worstation.

```python
python get_gta_news_clusters.py
```

### Preview the GTA news articles clusters 
To inspect clustes clusters, generated on Step 6, run the following script:

```python
python inspect_gta_news_clusters.py
```

 - [90_days_10 clusters.txt](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT3/notebooks/90_days_10%20clusters.txt)

 - [90_days_30 clusters.txt](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT3/notebooks/90_days_30%20clusters.txt)

 - [90_days_50 clusters](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT3/notebooks/90_days_50%20clusters.txt)


## Visualizing the data
To visualize the data it was decided to use WordClouds rendered for each news cluster for each of 90 days of the collected GTA news.

 ## Progressive circular packing algorithm
To prepare word cloud circles for all 50 cluster for each of 90 dates of collected data, a special ['progressive circle packing algorithm'](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT3/dev/packing/circle_pack/circle_packing/circle_packing.pde) was developed. The [input data](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT3/dev/packing/circle_pack/packing_input.csv) for the algorithm was preapared in ["GTA News 50 Clusters: generate input for packing"](https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/GDELT3/notebooks/GTA%20News%2090%20Days%2050%20Clusters%20generate%20input%20for%20Packing.ipynb) notebook.

The algorithm pushes the circles apart but pulls them together to some kind of 'gravitational line' in the middle. This allowed the circles to pack in the center of the canvas keeping the shape proportional to the containing rectangle. Places in the center at the first frame, the circles were sorting their positions other until movements settle after about 100-800 iterations. The algorithm was used  to generate circle packs for each day plus 9 transitional frames between (891 frames in total). To keep the positions consistent and movements fluent from frame to frame, each frame was given was given the previous frame position as starting point and then diameter of the circles were corrected to reflect new frame. Then the iterational process would re-pack the circles. In the demonstration of this process below each ankor frame shows for 1 second, the 9 transitions are blended in 0.5 second.

 [![Circular Packing](https://img.youtube.com/vi/4kubtjf-1uk/0.jpg)](https://www.youtube.com/watch?v=4kubtjf-1uk)

At the next step ["GTA News 50 Clusters Chart Using Packed Circles Rendering v.2"](http://localhost:8888/notebooks/Downloads/York/group-projects/CSDA1050-CAP/playground/GDELT3/notebooks/GTA%20News%2090%20Days%2050%20Clusters%20WordCloud%20v3.ipynb) notebook generates a combined daily WordCloud bubbles. All 50 clusters are reresented by circled clouds of the size proportional to the number of articles. Generation of all 891 slides takes about 5 minutes. The slides were assembled into the slide show of 4K video quality using [ProShow](http://www.photodex.com/proshow/producer) software by PhotoDex and uploaded to YouTube:
 
 [![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/I4tF6VbPuH0/0.jpg)](https://www.youtube.com/watch?v=I4tF6VbPuH0)
 
## Conclusion
The described approach to presening dynamic flow of news was proven to be feasible. The resulting presentation is informative. Some improvements could be done to the algorithm of circle packing to make it smoother. 

## Next Steps
The following step could taken to transform the presented approach to the production pipeline:

 1. Convert the packing algoritm and Jupyter notebooks to Python scripts.
 2. Develop interactive web application that would dynamically place WordCloud bubble i,ages using JavaScript/HTML5.
 3. Create scheduler that would download GDELT news daily and trigger generation of the data for rendering the bubble frames.
 
