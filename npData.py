import fourHourSVM
import fourHourKNN
import fourHourLR
import oneHourSVM
import oneHourKNN
import oneHourLR
import dailyKNN
import dailyLR
import dailySVM
import numpy as np


if __name__ == '__main__':
    list = []
    for i in range(1,101):
        (predict, y_test,z_test) = oneHourSVM.SVM()
        (acc,gain,loss,total) = oneHourSVM.accuracy(predict,y_test,z_test)
        list.append([acc,gain,loss,total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/oneHourSVM", list)
    print("oneHourSVM npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = oneHourKNN.KNN()
        (acc, gain, loss, total) = oneHourKNN.accuracy(predict,y_test,z_test)
        list.append([acc,gain,loss,total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/oneHourKNN", list)
    print("oneHourKNN npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = oneHourLR.LR()
        (acc, gain, loss, total) = oneHourLR.accuracy(predict,y_test,z_test)
        list.append([acc,gain,loss,total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/oneHourLR", list)
    print("oneHourLR npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = fourHourSVM.SVM()
        (acc, gain, loss, total) = fourHourSVM.accuracy(predict,y_test,z_test)
        list.append([acc, gain, loss, total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/fourHourSVM", list)
    print("fourHourSVM npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = fourHourKNN.KNN()
        (acc, gain, loss, total) = fourHourKNN.accuracy(predict,y_test,z_test)
        list.append([acc, gain, loss, total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/fourHourKNN", list)
    print("fourHourKNN npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = fourHourLR.LR()
        (acc, gain, loss, total) = fourHourLR.accuracy(predict,y_test,z_test)
        list.append([acc, gain, loss, total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/fourHourLR", list)
    print("fourHourLR npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = dailySVM.SVM()
        (acc, gain, loss, total) = dailySVM.accuracy(predict,y_test,z_test)
        list.append([acc, gain, loss, total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/dailySVM", list)
    print("dailySVM npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = dailyKNN.KNN()
        (acc, gain, loss, total) = dailyKNN.accuracy(predict,y_test,z_test)
        list.append([acc, gain, loss, total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/dailyKNN", list)
    print("dailyKNN npdata completed")
    list[:] = []
    for i in range(1,101):
        (predict, y_test,z_test) = dailyLR.LR()
        (acc, gain, loss, total) = dailyLR.accuracy(predict,y_test,z_test)
        list.append([acc, gain, loss, total])
    np.savetxt("/Users/yangkangou/Desktop/CSE485/JsonData/json/dailyLR", list)
    print("dailyLR npdata completed")
