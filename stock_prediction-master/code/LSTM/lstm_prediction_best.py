#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import tensorflow as tf
import re
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import median_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import accuracy_score as acc
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras import initializers
from keras.layers import Dropout, Activation, Embedding, Convolution1D, MaxPooling1D, Input, Dense,                          BatchNormalization, Flatten, Reshape, Concatenate, Merge
from keras.layers.recurrent import LSTM, GRU
from keras.callbacks import Callback, ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.models import Model
from keras.optimizers import Adam, SGD, RMSprop
from keras import regularizers




data = pd.read_csv("Labeled_news/AMAZON_1440_labeled_news.csv")
data.head()

data.isnull().sum()

data = data.drop(['Published_date', 'Title', 'Text', 'Time'],1)

data=data[data.Positive_Sentiment.notnull()]

data.isnull().sum()

data = data.drop(['Unnamed: 0'],1)

data.isnull().sum()

news = pd.read_csv("Labeled_news/AMAZON_1440_labeled_news.csv")

news=news.drop(['Unnamed: 0','Published_date', 'Title', 'Positive_Sentiment', 'Time'],1)

news.head()
news=news[news.Text.notnull()]

news.isnull().sum()

news_text = news.Text

word_counts = {}

for date in news_text:
    for article in date:
        for word in article.split():
            if word not in word_counts:
                word_counts[word] = 1
            else:
                word_counts[word] += 1
            


embeddings_index = {}
with open('glove.840B.300d.txt', encoding='utf-8') as f:
    for line in f:
        values = line.split(' ')
        word = values[0]
        embedding = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = embedding



missing_words = 0
threshold = 3

for word, count in word_counts.items():
    if count > threshold:
        if word not in embeddings_index:
            missing_words += 1
            
missing_ratio = round(missing_words/len(word_counts),4)*100
            


vocab_to_int = {} 

value = 0
for word, count in word_counts.items():
    if count >= threshold or word in embeddings_index:
        vocab_to_int[word] = value
        value += 1
codes = ["<UNK>","<PAD>"]   
for code in codes:
    vocab_to_int[code] = len(vocab_to_int)

int_to_vocab = {}
for word, value in vocab_to_int.items():
    int_to_vocab[value] = word

usage_ratio = round(len(vocab_to_int) / len(word_counts),4)*100



embedding_dim = 300

nb_words = len(vocab_to_int)
word_embedding_matrix = np.zeros((nb_words, embedding_dim))
for word, i in vocab_to_int.items():
    if word in embeddings_index:
        word_embedding_matrix[i] = embeddings_index[word]
    else:
        # If word not in GloVe, create a random embedding for it
        new_embedding = np.array(np.random.uniform(-1.0, 1.0, embedding_dim))
        embeddings_index[word] = new_embedding
        word_embedding_matrix[i] = new_embedding



# Change the text from words to integers
# If word is not in vocab, replace it with <UNK> (unknown)
word_count = 0
unk_count = 0

int_news_text = []

for date in news_text:
    int_daily_news_text = []
    for article in date:
        int_article = []
        for word in article.split():
            word_count += 1
            if word in vocab_to_int:
                int_article.append(vocab_to_int[word])
            else:
                int_article.append(vocab_to_int["<UNK>"])
                unk_count += 1
        int_daily_news_text.append(int_article)
    int_news_text.append(int_daily_news_text)

unk_percent = round(unk_count/word_count,4)*100


lengths = []
for date in int_news_text:
    for article in date:
        lengths.append(len(article))

lengths = pd.DataFrame(lengths, columns=['counts'])




lengths.describe()


max_article_length = 16
max_daily_length = 200
pad_news_text = []

for date in int_news_text:
    pad_daily_news_text = []
    for article in date:
        # Add article if it is less than max length
        if len(article) <= max_article_length:
            for word in article:
                pad_daily_news_text.append(word)
        # Limit article if it is more than max length  
        else:
            article = article[:max_article_length]
            for word in article:
                pad_daily_news_text.append(word)
    
    # Pad daily_news_text if they are less than max length
    if len(pad_daily_news_text) < max_daily_length:
        for i in range(max_daily_length-len(pad_daily_news_text)):
            pad = vocab_to_int["<PAD>"]
            pad_daily_news_text.append(pad)
    # Limit daily_news_text if they are more than max length
    else:
        pad_daily_news_text = pad_daily_news_text[:max_daily_length]
    pad_news_text.append(pad_daily_news_text)




result = data.Positive_Sentiment
updated_result=[]
for re in result:
    if re==1:
        updated_result.append(1)
    else:
        updated_result.append(0)

import random
while len(updated_result)!=len(pad_news_text):
    updated_result.append(random.choice([1, 0]))


x_train, x_test, y_train, y_test = train_test_split(pad_news_text, updated_result, test_size = 0.15, random_state = 2)

x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)


filter_length1 = 3
filter_length2 = 5
dropout = 0.5
learning_rate = 0.001
weights = initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=2)
nb_filter = 16
rnn_output_size = 128
hidden_dims = 128
wider = True
deeper = True

if wider == True:
    nb_filter *= 2
    rnn_output_size *= 2
    hidden_dims *= 2


def build_model():
    
    model1 = Sequential()
    
    model1.add(Embedding(nb_words, 
                         embedding_dim,
                         weights=[word_embedding_matrix], 
                         input_length=max_daily_length))
    model1.add(Dropout(dropout))
    
    model1.add(Convolution1D(filters = nb_filter, 
                             kernel_size = filter_length1, 
                             padding = 'same',
                            activation = 'relu'))
    model1.add(Dropout(dropout))
    
    if deeper == True:
        model1.add(Convolution1D(filters = nb_filter, 
                                 kernel_size = filter_length1, 
                                 padding = 'same',
                                activation = 'relu'))
        model1.add(Dropout(dropout))
    
    model1.add(LSTM(rnn_output_size, 
                   activation=None,
                   kernel_initializer=weights,
                   dropout = dropout))
    
    ####

    model2 = Sequential()
    
    model2.add(Embedding(nb_words, 
                         embedding_dim,
                         weights=[word_embedding_matrix], 
                         input_length=max_daily_length))
    model2.add(Dropout(dropout))
    
    
    model2.add(Convolution1D(filters = nb_filter, 
                             kernel_size = filter_length2, 
                             padding = 'same',
                             activation = 'relu'))
    model2.add(Dropout(dropout))
    
    if deeper == True:
        model2.add(Convolution1D(filters = nb_filter, 
                                 kernel_size = filter_length2, 
                                 padding = 'same',
                                 activation = 'relu'))
        model2.add(Dropout(dropout))
    
    model2.add(LSTM(rnn_output_size, 
                    activation=None,
                    kernel_initializer=weights,
                    dropout = dropout))
    
    ####

    model = Sequential()

    model.add(Merge([model1, model2], mode='concat'))
    
    model.add(Dense(hidden_dims, kernel_initializer=weights))
    model.add(Dropout(dropout))
    
    if deeper == True:
        model.add(Dense(hidden_dims//2, kernel_initializer=weights))
        model.add(Dropout(dropout))

    model.add(Dense(1, 
                    kernel_initializer = weights,
                    name='output'))

    model.compile(loss='mean_squared_error',
                  optimizer=Adam(lr=learning_rate,clipvalue=1.0))
    return model



# Make predictions with the best weights
deeper=False
wider=False
dropout=0.3
learning_Rate = 0.001
# Need to rebuild model in case it is different from the model that was trained most recently.
model = build_model()

model.load_weights('./question_pairs_weights_deeper={}_wider={}_lr={}_dropout={}.h5'.format(
                    deeper,wider,learning_rate,dropout))
predictions = model.predict([x_test,x_test], verbose = True)
print(predictions)



direction_pred = []
for pred in predictions:
    if pred > 0.5:
        direction_pred.append(1)
    else:
        direction_pred.append(0)
direction_test = []
for value in y_test:
    if value > 0.0:
        direction_test.append(1)
    else:
        direction_test.append(0)




direction = acc(direction_test, direction_pred)
direction = round(direction,4)*100
print("Predicted values matched the actual direction {}% of the time.".format(direction))

