# Directional Stock Prediction

## Summary
We are going to use GloVe’s larger common crawl vectors to create our word embeddings and Keras to build our model. This model was inspired by the work described in below mentioned paper. Similar to the paper, we will be using CNNs with two input vectors of different length, but rather than using GRU as RNN network we will LSTM which shows better results for sequential training.

## Library Functions
 `Numpy`, `matplotlib`,`Keras` , `Tensorflow`, `NLTK` , `scikit-learn` , `Glove`

## Install Instructions
**You must download GloVe's vectors to run this classifier.** \
Please run "install.sh" file provided at the root directory of project which will install python dependencies. 

As we know Training a neural network takes very large amount of time, You can directly run this netowork using pretrained saved vectors for amazon for test purposes. This will not take more than 5 minutes. (You still need to download GloVe for word embeddings)


 
## REFERENCES
Combination of CNN and RNN-
(https://www.aclweb.org/anthology/C16-1229)


## GloVe Link
This repository doen't involve GloVe's crawl vectors due to very big size of file(~5gb). Please proceed to below mentioned link to download gloVe's vector.
(http://nlp.stanford.edu/data/glove.840B.300d.zip) 
