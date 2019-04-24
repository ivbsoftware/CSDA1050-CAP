#TODO: remove file?
import os
import pandas as pd
from collections import Counter
import d2v_utils

# directories
dir_path = os.getcwd()
print('Working dir: ' + dir_path)

local_path = dir_path + '\\data\\'
df = pd.read_pickle(local_path+'backup'+'-gta.2'+'.pickle')

skip_terms =['toronto','canada','canadian','ontario']

# Global cluster descriptions
daily_clusters = df.groupby(['cluster'])['title']
cluster_descr = []
for cluster, titles in daily_clusters:
    #print("\nCluster: ", cluster)
    filtered_words = []
    for title in titles:
        t = title[0:-4]
        #print(">>>", t)
        tokens = d2v_utils.prepare_text_for_lda(t)
        tokens = [word for word in tokens if word not in skip_terms and not word.isdigit()]
        #print("  >", tokens)
        filtered_words = filtered_words + tokens
    count = Counter(filtered_words)
    cluster_descr = count.most_common()[:8]
    print ("cluster " + str(cluster) + str(cluster_descr))

print ('done')