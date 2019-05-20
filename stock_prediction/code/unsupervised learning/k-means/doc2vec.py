
#import gensim library
import gensim
from gensim.models.doc2vec import LabeledSentence
import mysql.connector
import numpy as np
import os
import time
import codecs
from nltk.tokenize import word_tokenize
import nltk
from os import listdir

#
# actual_label = []
# file_db = []
# db = mysql.connector.connect(host="127.0.0.1"
#                              , user="root", passwd="12345678", database="oneHourChart")
# cursor = db.cursor()
# sql = "SELECT artFile,priceDifference FROM onehourchart.separatefile GROUP BY artFile order by artFile ASC;"
# try:
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     for r in results:
#         if r[1]!="" and float(r[1])>0:
#             actual_label.append('0')
#             file_db.append(r[0])
#         if r[1]!="" and float(r[1])<0:
#             actual_label.append('1')
#             file_db.append(r[0])
# except:
#     print "query error"
# print actual_label
#parameters
data_dir = 'AAPL/total'# data directory containing input.txt
save_dir = 'AAPL/total' # directory to store models
file_list_temp = [f.replace('.txt','') for f in listdir("AAPL/total") if f.endswith('.txt')]
file_list = []
results = map(int, file_list_temp)
results.sort()
for i in results:
    file_list.append(str(i)+".txt")
# print file_list
# print file_db
# print len(file_list)
# print len(actual_label)

from gensim.models.doc2vec import LabeledSentence
class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield gensim.models.doc2vec.LabeledSentence(doc,[self.labels_list[idx]])


def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences


sentences = []
sentences_label = []
sentences_cutoff = []
sentences_infile = {}
actual_label = np.loadtxt('total_2/actual_label_aapl')
print len(actual_label)
k_mean_label = np.loadtxt('total_2/k-mean-label')
g_count = 0
# create sentences from files
label_length = 0
for file_name in file_list:
    int_file = file_name.replace('.txt','')
    input_file = os.path.join(data_dir, file_name)
    # read data
    with codecs.open(input_file, "r") as f:
        count = 0
        for line in f:
            tokens = word_tokenize(line)
            sentences.append(tokens)
            count += 1
            g_count += 1
            if actual_label[label_length] == 1:
                sentences_label.append("1")
            else:
                sentences_label.append("0")
        sentences_infile[file_name] = count
        sentences_cutoff.append(g_count-1)
        label_length += 1
print sentences_infile
print sentences_cutoff


np.savetxt("total_2/sentences_cutoff_four",sentences_cutoff)







""""""
def train_doc2vec_model(data, docLabels, size=300, sample=0.000001, dm=0, hs=1, window=10, min_count=0, workers=8,
                        alpha=0.024, min_alpha=0.024, epoch=15, save_file='doc2vec_four'):
    startime = time.time()

    print("{0} articles loaded for model".format(len(data)))

    it = LabeledLineSentence(data, docLabels)

    model = gensim.models.Doc2Vec(size=size, sample=sample, dm=dm, window=window, min_count=min_count, workers=workers,
                                  alpha=alpha, min_alpha=min_alpha, hs=hs)  # use fixed learning rate
    model.build_vocab(it)
    for epoch in range(epoch):
        print("Training epoch {}".format(epoch + 1))
        model.train(it, total_examples=model.corpus_count, epochs=model.iter)
        # model.alpha -= 0.002 # decrease the learning rate
        # model.min_alpha = model.alpha # fix the learning rate, no decay

    # saving the created model
    model.save(os.path.join(save_file))
    print('model saved')

train_doc2vec_model(sentences, sentences_label, size=300,sample=0.0,alpha=0.025, min_alpha=0.001, min_count=0, window=10, epoch=20, dm=0, hs=1, save_file='doc2vec_four')
""""""
""""""
#import library
from six.moves import cPickle

#load the model
d2v_model = gensim.models.doc2vec.Doc2Vec.load('doc2vec_four')

sentences_vector = []


t = 5

for i in range(len(sentences)):
    if i % t == 0:
        print("sentence", i, ":", sentences[i])
        print("***")
    # if i == 100:
    #     break
    sentences_vector.append(d2v_model.infer_vector(sentences[i], alpha=0.001, min_alpha=0.001, steps=10000))

# save the sentences_vector
sentences_vector_file = os.path.join(save_dir, "sentences_vector_500_a001_ma001_s10000_four_AAPL.pkl")
with open(os.path.join(sentences_vector_file), 'wb') as f:
    cPickle.dump((sentences_vector), f)

np.savetxt("total_2//sentence_vector_four_AAPL",sentences_vector)
# """"""""""""""""""""""""""""""""""""""""""
sentences_vector = np.loadtxt('total_2/sentence_vector_four_AAPL')
X_train = np.array(sentences_vector)
nb_sequenced_sentences = 4
vector_dim = 300

three_d_X_train = np.zeros((len(sentences), nb_sequenced_sentences, vector_dim), dtype=np.float)
three_d_y_train = np.zeros((len(sentences), vector_dim), dtype=np.float)

t = 4
for i in range(len(sentences_label) - nb_sequenced_sentences - 1):
    # if i % t == 0: print("new sequence: ", i)

    for k in range(nb_sequenced_sentences):
        sent = sentences_label[i + k]
        vect = sentences_vector[i + k]

        # if i % t == 0:
        #     print("  ", k + 1, "th vector for this sequence. Sentence ", sent, "(vector dim = ", len(vect), ")")

        for j in range(len(vect)):
            three_d_X_train[i, k, j] = vect[j]

    senty = sentences_label[i + nb_sequenced_sentences]
    vecty = sentences_vector[i + nb_sequenced_sentences]
    # if i % t == 0: print("  y vector for this sequence ", senty, ": (vector dim = ", len(vecty), ")")
    for j in range(len(vecty)):
        three_d_y_train[i, j] = vecty[j]

print(three_d_X_train.shape, three_d_y_train.shape)
""""""""""""""""""""""""""""""""""""""""""
print three_d_y_train
""""""


from sklearn.cluster import KMeans
import numpy as np
from sklearn.datasets import load_files


sentences_vector = np.loadtxt('total_2/sentence_vector_four_AAPL')
X_train = np.array(sentences_vector)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X_train)

array = kmeans.labels_
count_file = 0
predcit_y = []

sentences_cutoff = np.loadtxt('total_2/sentences_cutoff_four')
sentences_cutoff = list(sentences_cutoff)
start = sentences_cutoff.pop(0)
for i in range(len(array)):
    if i == start:
        if count_file > 0:
            predcit_y.append(1)
        else:
            predcit_y.append(0)
        if i != len(array)-1:
            start = sentences_cutoff.pop(0)
        count_file = 0
    if(array[i] == 1):
        count_file += 1
    else:
        count_file -= 1
np.savetxt('total_2/k-mean-label',array)
print array
print predcit_y
actual_label = np.loadtxt('total_2/actual_label_aapl')
print actual_label
accuray = 0
for i in range(len(predcit_y)):
    if actual_label[i] == predcit_y[i]:
        accuray += 1
print accuray
result = float(accuray)/float(len(predcit_y))
print result
print len(predcit_y)
# print kmeans.predict([[0, 0], [4, 4]])

#print kmeans.cluster_centers

import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs

plt.scatter(X_train[:, 0], X_train[:, 1], c=array, s=10, cmap='viridis')
plt.title('Classification for Apple')
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.show()









# from keras import regularizers
# from keras.models import Sequential, Model
# from keras.layers import Dense, Activation, Dropout, Embedding, Flatten, Bidirectional, Input, LSTM
# from keras.callbacks import EarlyStopping,ModelCheckpoint
# from keras.optimizers import Adam
# from keras.metrics import categorical_accuracy, mean_squared_error, mean_absolute_error, logcosh
# from keras.layers.normalization import BatchNormalization
#
#
# rnn_size = 128 # size of RNN
# vector_dim = 300
# learning_rate = 0.0001 #learning rate
#
#
#
#
# def bidirectional_lstm_model(vector_dim):
#     print('Building LSTM model...')
#     model = Sequential()
#     model.add(Bidirectional(LSTM(rnn_size, activation="relu"), input_shape=(4, vector_dim)))
#     model.add(Dropout(0.3))
#
#
#     model.add(Dense(vector_dim))
#
#     optimizer = Adam(lr=learning_rate)
#     callbacks = [EarlyStopping(patience=2, monitor='val_loss')]
#     model.compile(loss='logcosh', optimizer=optimizer, metrics=['acc'])
#     print('LSTM model built.')
#     return model
#
#
#
# model_sequence = bidirectional_lstm_model(vector_dim)
#
#
#
# print len(X_train)
#
#
#
# stock = load_files('/home/michael/Desktop/CSE573/TrainingData_FourHour')
# #feature x
# #stock_X = stock.data
# #category
# stock_Y = stock.target
# # stock_X = stock_X.reshape(len(stock_Y),2)
# #print len(stock_Y)
# stock_Z = stock.filenames
#
# print (stock_Y)
#
#
#
#
# batch_size = 15 # minibatch size
#
# callbacks=[EarlyStopping(patience=3, monitor='val_loss'),
#            ModelCheckpoint(filepath=save_dir + "/" + 'my_model_sequence_lstm.{epoch:02d}.hdf5',\
#                            monitor='val_loss', verbose=1, mode='auto', period=5)]
#
# history = model_sequence.fit(three_d_X_train, three_d_y_train,
#                  batch_size=batch_size,
#                  shuffle=True,
#                  epochs=40,
#                  callbacks=callbacks,
#                  validation_split=0.2)
#
# #save the model
# model_sequence.save(save_dir + "/" + 'my_model_sequence_lstm.final2.hdf5')


