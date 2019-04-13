# Project Proposal
## Done so far
 - Prepared a [first notebook](http://localhost:8888/notebooks/Downloads/York/group-projects/CSDA1050-CAP/playground/GDELT2/GDELT%20News%20Data%20Extraction%20for%20GTA%20Area.ipynb) 
 that for one day extracts GDELT events data (geo-fenced to GTA), parses the data extracting the news links and for ONE arbitrary link extracts the actual news narrative, tokenizes it and extracts 5 topics. Then it prepares visualizations, like PyLDAViz and Wordcloud.
 - Prepared a [second notebook](http://localhost:8888/notebooks/Downloads/York/group-projects/CSDA1050-CAP/playground/GDELT2/GDELT%20News%20Data%20Extraction%20for%20GTA%20Area%20-%20Aggregated%20Daily.ipynb) that runs
 extraction of GTA geo-fenced GDELD events daily (from yesterday backwards). For each day it extracts unique news links, extracts news narrative and create aggregated news narrative. This text is tokenized and then 30 topics are being extracted. After that the script prepares topics visualization using PyLDAViz and Wordcloud.
