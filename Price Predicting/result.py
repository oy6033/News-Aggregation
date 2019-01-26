import numpy as np
from tabulate import tabulate


if __name__ == '__main__':
    print "-----one hour chart SVM,KNN,LR algorithm 100 time result-----"
    listSVM = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/oneHourSVM");
    listKNN = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/oneHourKNN")
    listLR = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/oneHourLR")
    max_acc = ["max accuracy: ",str(round(max(listSVM[:,0]),2))+'%',str(round(max(listKNN[:,0]),2))+'%'
           ,str(round(max(listLR[:,0]),2))+'%']
    min_acc = ["min accuracy: ",str(round(min(listSVM[:,0]),2))+'%',str(round(min(listKNN[:,0]),2))+'%'
           ,str(round(min(listLR[:,0]),2))+'%']
    median_acc = ["median accuracy: ",str(round(np.median(listSVM[:,0]),2))+'%',str(round(np.median(listKNN[:,0]),2))+'%'
           ,str(round(np.median(listLR[:,0]),2))+'%']
    aver_acc = ["average accuracy: ",str(round(sum(listSVM[:,0])/len(listSVM[:,0]),2))+'%',
                str(round(sum(listKNN[:,0])/len(listKNN[:,0]),2))+'%',str(round(sum(listLR[:,0])/len(listLR[:,0]),2))+'%']

    max_gain = ["max gain: ",str(round(max(listSVM[:,1]),2))+'$',str(round(max(listKNN[:,1]),2))+'$'
           ,str(round(max(listLR[:,1]),2))+'$']
    min_gain = ["min gain: ",str(round(min(listSVM[:,1]),2))+'$',str(round(min(listKNN[:,1]),2))+'$'
           ,str(round(min(listLR[:,1]),2))+'$']
    median_gain = ["median gain: ",str(round(np.median(listSVM[:,1]),2))+'$',str(round(np.median(listKNN[:,1]),2))+'$'
           ,str(round(np.median(listLR[:,1]),2))+'$']
    aver_gain = ["average gain: ",str(round(sum(listSVM[:,1])/len(listSVM[:,1]),2))+'$',
                str(round(sum(listKNN[:,1])/len(listKNN[:,1]),2))+'$',str(round(sum(listLR[:,1])/len(listLR[:,1]),2))+'$']

    max_loss = ["max loss: ",str(round(max(listSVM[:,2]),2))+'$',str(round(max(listKNN[:,2]),2))+'$'
           ,str(round(max(listLR[:,2]),2))+'$']
    min_loss = ["min loss: ",str(round(min(listSVM[:,2]),2))+'$',str(round(min(listKNN[:,2]),2))+'$'
           ,str(round(min(listLR[:,2]),2))+'$']
    median_loss = ["median loss: ",str(round(np.median(listSVM[:,2]),2))+'$',str(round(np.median(listKNN[:,2]),2))+'$'
           ,str(round(np.median(listLR[:,2]),2))+'$']
    aver_loss = ["average loss: ",str(round(sum(listSVM[:,2])/len(listSVM[:,2]),2))+'$',
                str(round(sum(listKNN[:,2])/len(listKNN[:,2]),2))+'$',str(round(sum(listLR[:,2])/len(listLR[:,2]),2))+'$']

    max_total = ["max gain-loss: ",str(round(max(listSVM[:,3]),2))+'$',str(round(max(listKNN[:,3]),2))+'$'
           ,str(round(max(listLR[:,3]),2))+'$']
    min_total = ["min gain-loss: ",str(round(min(listSVM[:,3]),2))+'$',str(round(min(listKNN[:,3]),2))+'$'
           ,str(round(min(listLR[:,3]),2))+'$']
    median_total = ["median gain-loss: ",str(round(np.median(listSVM[:,3]),2))+'$',str(round(np.median(listKNN[:,3]),2))+'$'
           ,str(round(np.median(listLR[:,3]),2))+'$']
    aver_total = ["average gain-loss: ",str(round(sum(listSVM[:,3])/len(listSVM[:,3]),2))+'$',
                str(round(sum(listKNN[:,3])/len(listKNN[:,3]),2))+'$',str(round(sum(listLR[:,3])/len(listLR[:,3]),2))+'$']

    print tabulate([max_acc,min_acc,median_acc,aver_acc,
                    max_gain,min_gain,median_gain,aver_gain,
                    max_loss,min_loss,median_loss,aver_loss,
                    max_total,min_total,median_total,aver_total], headers=[' ', 'SVM','KNN','LR'])

    print "\n-----four hour chart SVM,KNN,LR algorithm 100 time result-----"
    listSVM = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/fourHourSVM");
    listKNN = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/fourHourKNN")
    listLR = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/fourHourLR")
    max_acc = ["max accuracy: ",str(round(max(listSVM[:,0]),2))+'%',str(round(max(listKNN[:,0]),2))+'%'
           ,str(round(max(listLR[:,0]),2))+'%']
    min_acc = ["min accuracy: ",str(round(min(listSVM[:,0]),2))+'%',str(round(min(listKNN[:,0]),2))+'%'
           ,str(round(min(listLR[:,0]),2))+'%']
    median_acc = ["median accuracy: ",str(round(np.median(listSVM[:,0]),2))+'%',str(round(np.median(listKNN[:,0]),2))+'%'
           ,str(round(np.median(listLR[:,0]),2))+'%']
    aver_acc = ["average accuracy: ",str(round(sum(listSVM[:,0])/len(listSVM[:,0]),2))+'%',
                str(round(sum(listKNN[:,0])/len(listKNN[:,0]),2))+'%',str(round(sum(listLR[:,0])/len(listLR[:,0]),2))+'%']

    max_gain = ["max gain: ",str(round(max(listSVM[:,1]),2))+'$',str(round(max(listKNN[:,1]),2))+'$'
           ,str(round(max(listLR[:,1]),2))+'$']
    min_gain = ["min gain: ",str(round(min(listSVM[:,1]),2))+'$',str(round(min(listKNN[:,1]),2))+'$'
           ,str(round(min(listLR[:,1]),2))+'$']
    median_gain = ["median gain: ",str(round(np.median(listSVM[:,1]),2))+'$',str(round(np.median(listKNN[:,1]),2))+'$'
           ,str(round(np.median(listLR[:,1]),2))+'$']
    aver_gain = ["average gain: ",str(round(sum(listSVM[:,1])/len(listSVM[:,1]),2))+'$',
                str(round(sum(listKNN[:,1])/len(listKNN[:,1]),2))+'$',str(round(sum(listLR[:,1])/len(listLR[:,1]),2))+'$']

    max_loss = ["max loss: ",str(round(max(listSVM[:,2]),2))+'$',str(round(max(listKNN[:,2]),2))+'$'
           ,str(round(max(listLR[:,2]),2))+'$']
    min_loss = ["min loss: ",str(round(min(listSVM[:,2]),2))+'$',str(round(min(listKNN[:,2]),2))+'$'
           ,str(round(min(listLR[:,2]),2))+'$']
    median_loss = ["median loss: ",str(round(np.median(listSVM[:,2]),2))+'$',str(round(np.median(listKNN[:,2]),2))+'$'
           ,str(round(np.median(listLR[:,2]),2))+'$']
    aver_loss = ["average loss: ",str(round(sum(listSVM[:,2])/len(listSVM[:,2]),2))+'$',
                str(round(sum(listKNN[:,2])/len(listKNN[:,2]),2))+'$',str(round(sum(listLR[:,2])/len(listLR[:,2]),2))+'$']

    max_total = ["max gain-loss: ",str(round(max(listSVM[:,3]),2))+'$',str(round(max(listKNN[:,3]),2))+'$'
           ,str(round(max(listLR[:,3]),2))+'$']
    min_total = ["min gain-loss: ",str(round(min(listSVM[:,3]),2))+'$',str(round(min(listKNN[:,3]),2))+'$'
           ,str(round(min(listLR[:,3]),2))+'$']
    median_total = ["median gain-loss: ",str(round(np.median(listSVM[:,3]),2))+'$',str(round(np.median(listKNN[:,3]),2))+'$'
           ,str(round(np.median(listLR[:,3]),2))+'$']
    aver_total = ["average gain-loss: ",str(round(sum(listSVM[:,3])/len(listSVM[:,3]),2))+'$',
                str(round(sum(listKNN[:,3])/len(listKNN[:,3]),2))+'$',str(round(sum(listLR[:,3])/len(listLR[:,3]),2))+'$']

    print tabulate([max_acc,min_acc,median_acc,aver_acc,
                    max_gain,min_gain,median_gain,aver_gain,
                    max_loss,min_loss,median_loss,aver_loss,
                    max_total,min_total,median_total,aver_total], headers=[' ', 'SVM','KNN','LR'])

    print "\n-----daily chart SVM,KNN,LR algorithm 100 time result-----"
    listSVM = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/dailySVM");
    listKNN = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/dailyKNN")
    listLR = np.loadtxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/dailyLR")
    max_acc = ["max accuracy: ", str(round(max(listSVM[:, 0]), 2)) + '%', str(round(max(listKNN[:, 0]), 2)) + '%'
        , str(round(max(listLR[:, 0]), 2)) + '%']
    min_acc = ["min accuracy: ", str(round(min(listSVM[:, 0]), 2)) + '%', str(round(min(listKNN[:, 0]), 2)) + '%'
        , str(round(min(listLR[:, 0]), 2)) + '%']
    median_acc = ["median accuracy: ", str(round(np.median(listSVM[:, 0]), 2)) + '%',
                  str(round(np.median(listKNN[:, 0]), 2)) + '%'
        , str(round(np.median(listLR[:, 0]), 2)) + '%']
    aver_acc = ["average accuracy: ", str(round(sum(listSVM[:, 0]) / len(listSVM[:, 0]), 2)) + '%',
                str(round(sum(listKNN[:, 0]) / len(listKNN[:, 0]), 2)) + '%',
                str(round(sum(listLR[:, 0]) / len(listLR[:, 0]), 2)) + '%']

    max_gain = ["max gain: ", str(round(max(listSVM[:, 1]), 2)) + '$', str(round(max(listKNN[:, 1]), 2)) + '$'
        , str(round(max(listLR[:, 1]), 2)) + '$']
    min_gain = ["min gain: ", str(round(min(listSVM[:, 1]), 2)) + '$', str(round(min(listKNN[:, 1]), 2)) + '$'
        , str(round(min(listLR[:, 1]), 2)) + '$']
    median_gain = ["median gain: ", str(round(np.median(listSVM[:, 1]), 2)) + '$',
                   str(round(np.median(listKNN[:, 1]), 2)) + '$'
        , str(round(np.median(listLR[:, 1]), 2)) + '$']
    aver_gain = ["average gain: ", str(round(sum(listSVM[:, 1]) / len(listSVM[:, 1]), 2)) + '$',
                 str(round(sum(listKNN[:, 1]) / len(listKNN[:, 1]), 2)) + '$',
                 str(round(sum(listLR[:, 1]) / len(listLR[:, 1]), 2)) + '$']

    max_loss = ["max loss: ", str(round(max(listSVM[:, 2]), 2)) + '$', str(round(max(listKNN[:, 2]), 2)) + '$'
        , str(round(max(listLR[:, 2]), 2)) + '$']
    min_loss = ["min loss: ", str(round(min(listSVM[:, 2]), 2)) + '$', str(round(min(listKNN[:, 2]), 2)) + '$'
        , str(round(min(listLR[:, 2]), 2)) + '$']
    median_loss = ["median loss: ", str(round(np.median(listSVM[:, 2]), 2)) + '$',
                   str(round(np.median(listKNN[:, 2]), 2)) + '$'
        , str(round(np.median(listLR[:, 2]), 2)) + '$']
    aver_loss = ["average loss: ", str(round(sum(listSVM[:, 2]) / len(listSVM[:, 2]), 2)) + '$',
                 str(round(sum(listKNN[:, 2]) / len(listKNN[:, 2]), 2)) + '$',
                 str(round(sum(listLR[:, 2]) / len(listLR[:, 2]), 2)) + '$']

    max_total = ["max gain-loss: ", str(round(max(listSVM[:, 3]), 2)) + '$', str(round(max(listKNN[:, 3]), 2)) + '$'
        , str(round(max(listLR[:, 3]), 2)) + '$']
    min_total = ["min gain-loss: ", str(round(min(listSVM[:, 3]), 2)) + '$', str(round(min(listKNN[:, 3]), 2)) + '$'
        , str(round(min(listLR[:, 3]), 2)) + '$']
    median_total = ["median gain-loss: ", str(round(np.median(listSVM[:, 3]), 2)) + '$',
                    str(round(np.median(listKNN[:, 3]), 2)) + '$'
        , str(round(np.median(listLR[:, 3]), 2)) + '$']
    aver_total = ["average gain-loss: ", str(round(sum(listSVM[:, 3]) / len(listSVM[:, 3]), 2)) + '$',
                  str(round(sum(listKNN[:, 3]) / len(listKNN[:, 3]), 2)) + '$',
                  str(round(sum(listLR[:, 3]) / len(listLR[:, 3]), 2)) + '$']

    print tabulate([max_acc, min_acc, median_acc, aver_acc,
                    max_gain, min_gain, median_gain, aver_gain,
                    max_loss, min_loss, median_loss, aver_loss,
                    max_total, min_total, median_total, aver_total], headers=[' ', 'SVM', 'KNN', 'LR'])
