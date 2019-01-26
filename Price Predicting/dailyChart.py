# coding:utf-8
#!/usr/bin/python
# 引入相关模块

import mysql.connector
from datetime import datetime


def mergerNews():
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    sql = "SELECT date,id FROM oneHourChart"
    list = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            if r[0] not in list:
                list.append(r[0])
        db.commit()
        #print list
    except:
        print "error merger news"
    db.close;
    return list

def getDifference(date):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="dailyChart")
    cursor = db.cursor()
    sql = "SELECT difference FROM dailyChart " \
          "where date= '%s'" % (date)
    difference = ""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            difference = r[0]
            print difference
        db.commit()
    except:
        print "error getDifference"
    db.close;
    return difference

#daily chart
def findArticle(list):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    link = []
    first = []
    count = 1
    #all date in list
    for l in list:
        sql = "SELECT artlink,arttime FROM articles " \
            "where artdate='%s'" % (l)
        cursor.execute(sql)
        results = cursor.fetchall()
        #all article from that date
        for r in results:
            link.append(r[0])
            stringToInt = int(r[1].replace(':',''))
            #print stringToInt
            first.append(stringToInt)
            d = getDifference(l)
            list = findAllSentences(r[0])
            for sentence in list:
                separateFile(r[0], count, l, r[1], d, sentence)
        count = count +1


    # print(link)
    # print(first)
    # print(second)



def separateFile(artlink,artFile,date,arttime,priceDifference,sentence):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="dailyChart")
    cursor = db.cursor()
    sql = "INSERT INTO separateFile (artlink,artFile,date,arttime,priceDifference,sentence) " \
            "VALUES ('%s','%s','%s','%s','%s','%s')" % (artlink, artFile ,date, arttime,priceDifference,sentence)
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
    except:
        print("Error separateFile")
        db.rollback()
    db.close

def findAllSentences(artlink):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    sql = "SELECT sentence FROM companysentences " \
          "where artlink='%s'" % (artlink)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        list = []
        for r in results:
            list.append(r[0])
    except:
        print("Error findAllSentences")
    return list




def timer(n):
    while True:
        getTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(getTime)
        findArticle(mergerNews())
        print "dailyChart has done"
        break

timer(3600)