# coding:utf-8
#!/usr/bin/python


import scipy as sp
import numpy as np
import mysql.connector
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
#import matplotlib.pyplot as plt
#from sklearn import preprocessing


def KNN():
    stock = load_files('/Users/yangkangou/Desktop/CSE485/JsonData/json/TrainingData_Daily')
    #feature x
    stock_X = stock.data
    #category
    stock_Y = stock.target
    # stock_X = stock_X.reshape(len(stock_Y),2)
    stock_Z = stock.filenames
    # print stock_Y
    # print stock.filenames


    X_train, X_test, y_train, y_test, z_train, z_test = train_test_split(
        stock_X, stock_Y, stock_Z, test_size=0.1)

    count_vec = TfidfVectorizer(binary = False, decode_error = 'ignore',\
                                stop_words = 'english')
    # print z_test
    # print y_test
    x_train = count_vec.fit_transform(X_train)
    x_test  = count_vec.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(x_train, y_train)
    predict = knn.predict(x_test)
    #print(predict)
    #print(y_test)
    return predict,y_test,z_test

def accuracy(predict,y_test,z_test):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="dailyChart")
    cursor = db.cursor()
    accu = float(0)
    gain = 0;
    loss = 0;
    for i in range(len(predict)):
        if predict[i] == y_test[i]:
            fileID = int(z_test[i].replace("up","").replace("down","")[67:-4])
            sql = "SELECT priceDifference FROM priceDifference " \
                  "where artFile = '%d'" %(fileID)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for r in results:
                    if(float(r[0])>0):
                        gain = gain + abs(float(r[0]))
                db.commit()
                #print list
            except:
                print "error get price"
            db.close;
            accu += 1
        else:
            fileID = int(z_test[i].replace("up","").replace("down","")[67:-4])
            sql = "SELECT priceDifference FROM priceDifference " \
                  "where artFile = '%d'" %(fileID)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for r in results:
                    if(float(r[0])< 0):
                        loss = loss - abs(float(r[0]))
                db.commit()
                #print list
            except:
                print "error get price"
            db.close;
    #print(accu)
    accu = float(accu / len(predict))
    dailyGain = gain/len(predict)
    dailyLoss = loss/len(predict)
    total = dailyGain + dailyLoss
    print('the accuracy is %f' %(accu*100) + '%')
    print('daily gain is %f' %(dailyGain))
    print('daily loss is %f' %(dailyLoss))
    print('daily gain-loss is %f '%(total))
    return accu*100,dailyGain,dailyLoss,total

if __name__ == '__main__':
    (predict, y_test, z_test) = KNN()
    accuracy(predict,y_test,z_test)


