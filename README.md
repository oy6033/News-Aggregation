# Directional Stock Price Prediction
## Group 11 - 
Raghavendran Ramakrishnan\
Balaji Gokulakrishnan \
Yangkang Ou\
Manish Vishnoi\
Gourab Mitra\
Prateek Jain

## Overview
Predicting how the stock market will perform is one of the most difficult things to do. There are so many factors involved in the prediction – physical factors vs. physhological, rational and irrational behaviour, etc. All these aspects combine to make share prices volatile and very difficult to predict with a high degree of accuracy. 

To challenge one part of this problem, we built and analysed different models to predict direction of stock price's change of Amazon and Apple. For this we used different models and compared their performnaces. Models can be divided into three major parts :
* Supervised Learning.
* Unsupervised Learning.
* Neural Netowrk.

Evaluation metrices can be accessed under evaluation folder while source code can be accessed under code folder. Initial and processed data can be accessed under Data folder.( Additional data maybe required based on classifier)

## Installation guide

As this project doesn't have any front end, we tried to provide a installation script which can be used to install packages and run classifiers based upon your choice.

* This project requires **Python** for running.
* Though script is executable, it is safe to run command : \
``` chmod +x install.sh ```
* Once script is executed you can run individual classifiers as required.

**Not all classfiers are runnable as they have multiple dependencies, for e.g MySql database to run unsupervised kmeans.**

## Library Functions
* **Vectoriation** : GloVe word embeddings, Word2Vec & Doc2Vec
* **Data Preprocessing** : numpy, nltk 
* **Classification** : BERT, Keras, Tensorflow, Scikit-Learn

 
## REFERENCES

* Towards Data science blog- (https://towardsdatascience.commulti-class-text-classification-with-doc2vec-logistic-regression-9da9947b43f4)

* BERT - (https://github.com/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb)

* GloVe - (https://nlp.stanford.edu/projects/glove/)

* Combination of Convolutional and Recurrent Neural Network for Sentiment Analysis of Short Texts : (https://www.aclweb.org/anthology/C16-1229)
