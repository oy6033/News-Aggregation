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

def getDifference(date,startTime,endTime):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="fourHourChart")
    cursor = db.cursor()
    sql = "SELECT difference FROM fourHourChart " \
          "where date= '%s' AND startTime='%s' AND endTime='%s'" % (date,startTime,endTime)
    difference = ""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            difference = r[0]
        db.commit()
    except:
        print "error getDifference"
    db.close;
    return difference

#four hour chart
def findArticle(list):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    link = []
    first = []
    second = []
    countF = 0
    countL = 0
    count = 0
    #all date in list
    for l in list:
        sql = "SELECT artlink,arttime FROM articles " \
            "where artdate='%s'" % (l)
        cursor.execute(sql)
        results = cursor.fetchall()
        isVisitF = False
        isVisitL = False
        #all article from that date
        for r in results:
            link.append(r[0])
            stringToInt = int(r[1].replace(':',''))
            #print stringToInt

            if stringToInt>1230 and stringToInt<1630:

                if isVisitF == False:
                    count = count + 1
                    countF = count
                    isVisitF = True
                first.append(stringToInt)
                d = getDifference(l,"12:30","16:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],countF,l,r[1],d,sentence)

            if stringToInt > 1630 and stringToInt < 2030:
                if isVisitL == False:
                    count = count + 1
                    countL = count
                    isVisitL = True
                second.append(stringToInt)
                d = getDifference(l, "16:30", "20:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],countL, l, r[1], d,sentence)

    # print(link)
    # print(first)
    # print(second)



def separateFile(artlink,artFile,date,arttime,priceDifference,sentence):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="fourHourChart")
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
        print "fourHourChart has done"
        break

timer(3600)