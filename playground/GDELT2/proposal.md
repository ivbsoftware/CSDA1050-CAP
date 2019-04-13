# Project Proposal
## Done so far
 - Prepared a [first notebook](http://localhost:8888/notebooks/Downloads/York/group-projects/CSDA1050-CAP/playground/GDELT2/GDELT%20News%20Data%20Extraction%20for%20GTA%20Area.ipynb) 
 that for one day extracts GDELT events data (geo-fenced to GTA), parses the data extracting the news links and for ONE arbitrary link extracts the actual news narrative, tokenizes it and extracts 5 topics. Then it prepares visualizations, like PyLDAViz and Wordcloud.
 - Prepared a [second notebook](http://localhost:8888/notebooks/Downloads/York/group-projects/CSDA1050-CAP/playground/GDELT2/GDELT%20News%20Data%20Extraction%20for%20GTA%20Area%20-%20Aggregated%20Daily.ipynb) that runs
 extraction of GTA geo-fenced GDELD events daily (from yesterday backwards). For each day it extracts unique news links, extracts news narrative and create aggregated news narrative. This text is tokenized and then 30 topics are being extracted. After that the script prepares topics visualization using PyLDAViz and Wordcloud.

## Conclusions
 - GDELT event data contains records of news articles. In addition to the date, location and the url, the data might have names of up to 2 main actors of the event (with their locations) and characterization of their interaction/conflict. There is also estimations of the news sentiment.
 - GDELT event dataset has about 200K new articles per day.
 - There are 200-800 GTA related unique news per day.
 - GDELT geo coordinates are not detailed and usually refer to city center. Average daily news set brings about 4 unique geo coordinates, so the data can't be used for detailed mapping visualizations inside GTA.
  - It was proven by sampling the data and by exploratory processing, that it is feasible to use GDELT information for NLP-related analysis of the news and some limited geo-location analysis of the sentiment if it's combined with other sources of data.

## Proposals

The following ideas are being researched:

1. "What kind of movies we are watching?" - look at the daily news as movie reviews. Cluster news by topic, create aggregated 'reviews' and identify 'movie' genres. Quick research by *'python movie genre classification using plots'* brings [Movie Genre Classification using Plot](https://github.com/ishmeetkohli/imdbGenreClassification), [Predicting Movie Genres Based on Plot Summaries](https://www.researchgate.net/publication/322517980_Predicting_Movie_Genres_Based_on_Plot_Summaries) and other sources. This can be done as daily time series.
2. Use GDELT event data 'actors' to visualize how GTA relates to other geographical places over time - day by day.
3. Make an attempt to extract real news from 'fake' (needs definithin) analyzing objectivity and bias by NLP. Next step - group news sources by that criteria.
