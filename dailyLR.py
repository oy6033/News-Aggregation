from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.datasets import load_files
import mysql.connector
from sklearn import datasets
#import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def LR():
    stock = load_files('/Users/yangkangou/Desktop/CSE485/JsonData/json/TrainingData_Daily')
    #feature x
    stock_X = stock.data
    #category
    stock_Y = stock.target
    # stock_X = stock_X.reshape(len(stock_Y),2)
    #print len(stock_Y)
    stock_Z = stock.filenames

    X_train, X_test, y_train, y_test, z_train, z_test = train_test_split(
        stock_X, stock_Y, stock_Z, test_size=0.18)

    count_vec = TfidfVectorizer(binary = False, decode_error = 'ignore',\
                                stop_words = 'english')

    x_train = count_vec.fit_transform(X_train)
    x_test  = count_vec.transform(X_test)

    cls = LogisticRegression()
    cls.fit(x_train, y_train)
    predict = cls.predict(x_test)
    #print (predict)
    #print(y_test)
    return predict,y_test, z_test

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

# def show(n_samples,n_features,n_targets):
#     X, y = datasets.make_regression(n_samples, n_features, n_targets, noise=10)
#     plt.scatter(X, y)
#     plt.show()

if __name__ == '__main__':
    (predict, y_test, z_test) = LR()
    accuracy(predict,y_test, z_test)