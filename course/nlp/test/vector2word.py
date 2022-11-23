# Imports
from scipy.spatial import distance
import spacy
import numpy as np

# Load the spacy vocabulary
nlp = spacy.load("zh_core_web_lg")

# Format the input vector for use in the distance function
# In this case we will artificially create a word vector from a real word ("frog")
# but any derived word vector could be used
input_word = "测试"
p = np.array([nlp.vocab[input_word].vector])

# Format the vocabulary for use in the distance function
ids = [x for x in nlp.vocab.vectors.keys()]
vectors = [nlp.vocab.vectors[x] for x in ids]
vectors = np.array(vectors)

# *** Find the closest word below ***
closest_index = distance.cdist(p, vectors).argmin()
word_id = ids[closest_index]
output_word = nlp.vocab[word_id].text
print(output_word)
# assert output_word==input_word, "input word not eq to output word."
# output_word is identical, or very close, to the input word