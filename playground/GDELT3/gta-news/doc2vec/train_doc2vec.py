import logging
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Documents(object):
    def __init__(self, documents):
        self.documents = documents

    def __iter__(self):
        for i, doc in enumerate(self.documents):
            yield TaggedDocument(words = doc, tags = [i])

file = "data/news-dataset.txt"

corpus = open(file, "r", encoding="utf8")
lines = corpus.read().lower().split("\n")


documents =[]
for t in lines:
    # get document tokent and label from the line
    res = t.split('], [')
    doc = res[0].strip('\'][\'')
    doc = doc.split('\', \'')
    if len(doc) < 10:
        continue
    label = res[1].strip('\'][\'')

    # new TaggedDocument
    documents.append(TaggedDocument(words = doc, tags = [label]))

count = len(documents)
print ("Documents prepared: ", count)

#iter = 1
model = Doc2Vec(size=100, dbow_words= 1, dm=0, iter=1,  
                window=5, seed=1337, min_count=5, 
                workers=10, alpha=0.025, min_alpha=0.025)

model.build_vocab(documents)

for epoch in range(10):
    print(">>>>>> EPOCH "+str(epoch))
    model.train(documents, total_examples=count, epochs=1)
    model.save('news-dataset-huffington.model')
    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay