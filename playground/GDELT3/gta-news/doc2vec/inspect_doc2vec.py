from gensim.models import Doc2Vec

fname = "news-dataset-huffington.model"
model = Doc2Vec.load(fname)

print(">>> Test 1:")
print (model.most_similar(['handgun']))

print(">>> Test 2:")
print (model.most_similar(['toronto']))

print(">>> Test 3:")
print(model.infer_vector(['survivor', 'shooting', 'husband', 'child']))
