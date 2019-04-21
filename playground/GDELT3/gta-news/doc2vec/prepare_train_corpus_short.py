import pandas as pd
import d2v_utils

# Read the Kaggle news dataset file
# https://www.kaggle.com/rmisra/news-category-dataset/downloads/News_Category_Dataset_v2.json/2
#  awk '!a[$0]++' news-dataset-copy.txt

active_file = "../../data/kaggle-news-category-dataset/News_Category_Dataset_v2.json"
news = pd.read_json(active_file, lines=True)

print (news.info())
print (news['category'].unique())

# For each news link...
file_name = "news-dataset-short-v1.txt"
with open(file_name, mode='w', encoding="utf8") as outfile:
 for index, row in news.iterrows():

    print(str(index) + ": " + row.link)

    try:
        # extract tokens show some
        tokens = d2v_utils.prepare_text_for_lda(row.short_description)

        # save document record
        if len(tokens) > 9:
            line = str([tokens, [row.category]]) + "\n"
            outfile.write(line)
            outfile.flush()

    except Exception as e:
        print("Error, skipped due to: ", e)
        continue

print ('done')