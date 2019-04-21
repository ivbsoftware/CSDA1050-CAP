from gensim.models import Doc2Vec

fname = "news-dataset-huffington.model"
model = Doc2Vec.load(fname)

print (model.most_similar(['handgun']))