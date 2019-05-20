from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
import logging
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec

# 200 feature
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus("AMZN.txt")
model = word2vec.Word2Vec(sentences, sg=1, size=200, window=5, min_count=10, workers=3, negative=5, iter= 5)
model.save("AMZN.model", ignore=[])
