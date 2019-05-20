
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
        list = ["1801", "1802", "1803", "1804", "1805", "1806", "1807", "1808", "1809", "1810", "1811", "1812", "1901",
                "1902"]
        f = open('AAPL.txt', 'a')
        try:
            for fileName in dirs:
                if fileName in list:
                    for x in glob.glob(os.path.join(self.path+fileName, '*.json')):
                        x = x.replace("\\", "/")
                        result = resolveJson(x)
                        for sentence in splitSentence(result[2]):
                            sentence = sentence.replace('\r\n', '').replace("'", "")
                            tokens = word_tokenize(sentence)
                            words = [word.lower() for word in tokens if word.isalpha()]
                            # from nltk.corpus import stopwords
                            # stop_words = set(stopwords.words('english'))
                            # words = [w for w in words if not w in stop_words]
                            for word in words:
                                f.write(word.encode('utf-8') + ' ')
        except:
            print "write error"
        finally:
            f.close()
t = trainingSet("C:/Users/Michael/Desktop/AAPL/").All()