import pandas as pd
import sys
from newspaper import Article
import d2v_utils

line_from = 0
line_to = -1
file_num = 0

# read args from command line - lazy version
if __name__ == "__main__":
    line_from = int(sys.argv[1:][0])
    print(line_from)
    line_to = int(sys.argv[1:][1])
    print(line_to)
    file_num = sys.argv[1:][2]
    print(file_num)

# Read the Kaggle news dataset file
# https://www.kaggle.com/rmisra/news-category-dataset/downloads/News_Category_Dataset_v2.json/2
#  awk '!a[$0]++' news-dataset-copy.txt

active_file = "../../data/kaggle-news-category-dataset/News_Category_Dataset_v2.json"
news = pd.read_json(active_file, lines=True)

print (news.info())
print (news['category'].unique())

# For each news link...
file_name = "data/news-dataset-" + file_num + ".txt"
with open(file_name, mode='w', encoding="utf8") as outfile:
 for index, row in news.iterrows():

    # work on the part of the input file
    if line_to >= 0 and index > line_to:
        break
    if index < line_from:
        continue

    print(str(index) + ": " + row.link)

    try:
        # get article text
        article = Article(row.link)
        article.download()
        article.parse()

        # extract tokens show some
        tokens = d2v_utils.prepare_text_for_lda(article.text)

        # save doc2vec document record
        #doc = str(gensim.models.doc2vec.TaggedDocument(tokens, [row.category])) + "\n"
        line = str([tokens, [row.category]]) + "\n"
        outfile.write(line)
        outfile.flush()

    except Exception as e:
        print("Error, skipped due to: ", e)
        continue

print ('done')