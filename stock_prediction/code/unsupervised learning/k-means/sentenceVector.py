from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
import logging
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
import numpy as np

model = KeyedVectors.load("AAPL+AMZN.model")
y2 = model.most_similar("up", topn=10)
for item in y2:
    print (item[0], item[1])
# print model['good']
y1 = model.most_similar(positive=['up', 'increase'], negative=['down'], topn=1)
print y1


from nltk.tokenize import word_tokenize
import json
import nltk
import glob
from langdetect import detect
import os

def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences

def resolveJson(filename):
    # C:\\Users\\Michael\\Desktop\\AMZN\\
    try:
        file = open(filename, "rb")
        fileJson = json.load(file)
        #print fileJson["published"]
        date = fileJson["published"][:10].replace('-','.')
        time = fileJson["published"][11:13]
        temp = int(time) -2
        if temp < 0:
            temp = temp + 24
        s = str(temp)
        time = fileJson["published"][11:16].replace(time,s,1)
        link = filename[30:]
        text = fileJson["text"]
        if detect(text) != "en":
            print link," Language other than English"
            return ("","","","")
        return (date, link, text, time)

    except:
        print "read error", filename
        return ("", "", "", "")

class trainingSet():
    def __init__(self, path):
        self.path = path

    def All(self):
        dirs = os.listdir(self.path)
        list = ["171211", "180111"]
        sentenceVector = np.zeros((1, 200))
        count = 0
        try:
            for fileName in dirs:
                if fileName in list:
                    for x in glob.glob(os.path.join(self.path+fileName, '*.json')):
                        x = x.replace("\\", "/")
                        result = resolveJson(x)
                        try:
                            for sentence in splitSentence(result[2]):
                                wordVector = np.zeros((1, 200))
                                sentence = sentence.replace('\r\n', '').replace("'", "")
                                tokens = word_tokenize(sentence)
                                words = [word.lower() for word in tokens if word.isalpha()]
                                # from nltk.corpus import stopwords
                                # stop_words = set(stopwords.words('english'))
                                # words = [w for w in words if not w in stop_words]
                                word_count = len(words)
                                for word in words:
                                    try:
                                        wordVector = np.array(model[word]) + np.array(wordVector)

                                    except:
                                        print "no word %s" %(word)
                                        word_count -= 1

                                wordVector = wordVector/word_count
                                try:
                                    sentenceVector = np.append(sentenceVector, wordVector, axis=0)
                                except:
                                    print "sentenceVector error"
                                count += 1
                        except:
                            print "unkonw error"
            print count
            np.save("a.npy", sentenceVector)


        except:
            print "write error"

# t = trainingSet("C:/Users/Michael/Desktop/AMZN/").All()
# b = np.load("a.npy")
# print b.shape
# print b
