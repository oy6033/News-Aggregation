# coding:utf-8
#!/usr/bin/python
# 引入相关模块
import sys
import re
import string
import nltk
import requests
import mysql.connector
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import time
import json, urllib
from urllib import urlencode
from langdetect import detect
import os
import glob


count = 0



def getLink(id):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    sql = "SELECT artid,artlink FROM articles " \
          "where artid='%d'" % (id)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            link = r[1]
        db.commit()
    except:
        print "error get Link"
        db.rollback()
    db.close;
    return link

def splitWhiteSpace(AllUrl):
    res = AllUrl.split(" ");
    return res

def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences

def splitWord(Sentence):
    words = nltk.word_tokenize(Sentence)
    return words

def resolveJson(filename):
    try:
        file = open(filename, "rb")
        fileJson = json.load(file)
        #print fileJson["published"]
        date = fileJson["published"][:10].replace('-','.');
        time = fileJson["published"][11:13]
        temp = int(time) -2
        if temp < 0:
            temp = temp + 24;
        s = str(temp)
        time = fileJson["published"][11:16].replace(time,s,1)
        print time
        link = filename[47:]
        text = fileJson["text"]
        if detect(text) != "en":
            print link," Language other than English"
            return
        return (date, link, text, time)

    except:
        print "read error", filename
        return

def output(filename):
    try:
        result = resolveJson(filename)
        insertTitle(None, result[1], result[0], result[3], None).conn()
        local_aritcleID = queryID(result[1]).conn()
        sentenceTOword(local_aritcleID, result[2])
    except:
        return

def readAll(path):
    #path = "/Users/yangkangou/Desktop/CSE485/JsonData/json/1809/"
    for filename in glob.glob(os.path.join(path, '*.json')):
        #print(filename[47:64])
        #print getLink(1)
        output(filename)

class insert:
    def __init__(self, artid, arssentence):
        self.artid = artid;
        self.arssentence = arssentence;

    def conn(self):
        #db = mysql.connector.connect(host ="localhost", user="root", passwd="0B001ce7bf1f", database ="news")
        db = mysql.connector.connect(host="localhost"
                                     , user="root", passwd="12345678", database="oneHourChart")
        cursor = db.cursor()

        # sql = "INSERT INTO articlesentences(arsid, \
        #              arsatxid, arsnumber, arssentence) \
        #              VALUES ('%d', '%d', '%d', '%s' )" % (self.Aid, self.Arsid, self.Snumber, self.Sentences)
        sql = "INSERT INTO articlesentences(artid, \
                        arssentence) \
                     VALUES ('%d', '%s' )" % (self.artid, self.arssentence)
        id = 0
        try:
            cursor.execute(sql)
            cursor.execute("SELECT LAST_INSERT_ID()")
            results = cursor.fetchall()
            for r in results:
                id = r[0]

            db.commit()
        except:
            print(self.artid," to ",self.arssentence)
            db.rollback()
        #print "insert, sentence_number: ", self.number, " sentence: ", self.sentences
        db.close()
        return id

class insertsymbol:
    def __init__(self, artid, arsnumber, stockSymbol, stockPrice, sentence):
        self.artid = artid;
        self.arsnumber = arsnumber;
        self.stockSymbol = stockSymbol;
        self.stockPrice = stockPrice;
        self.sentence = sentence;

    def companysentences(self):
        #db = mysql.connector.connect(host="localhost", user="root", passwd="0B001ce7bf1f", database="news")
        db = mysql.connector.connect(host="localhost"
                                     , user="root", passwd="12345678", database="oneHourChart")
        cursor = db.cursor()

        # sql = "INSERT INTO articlesentences(arsid, \
        #              arsatxid, arsnumber, arssentence) \
        #              VALUES ('%d', '%d', '%d', '%s' )" % (self.Aid, self.Arsid, self.Snumber, self.Sentences)
        sql = "INSERT INTO companysentences(artid, \
                     arssnumber, companySymbol,artlink, sentence) \
                     VALUES ('%d', '%d', '%s', '%s', '%s')" % \
              (self.artid, self.arsnumber,  self.stockSymbol, self.stockPrice, self.sentence)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print "error symbol"
            print(self.artid," to ", self.arsnumber,self.stockSymbol,self.stockPrice,self.sentence)
            db.rollback()
        #print "insert, sentence_number: ", self.number, " sentence: ", self.sentences
        db.close()


class query:
    def __init__(self, companyName, sentence,locSentenceID,local_aritcleID):
        self.companyName = companyName
        self.sentence = sentence
        self.locSentenceID = locSentenceID
        self.local_aritcleID = local_aritcleID
    def conn(self):
        #db = mysql.connector.connect(host="localhost", user="root", passwd="0B001ce7bf1f", database="news")
        db = mysql.connector.connect(host="localhost"
                                     , user="root", passwd="12345678", database="oneHourChart")
        cursor = db.cursor()
        sql = "SELECT companySymbol,companyName FROM companies " \
              "where companySymbol='%s'" % (self.companyName)
        try:
            link = getLink(self.local_aritcleID)
            charu = insertsymbol(self.local_aritcleID, self.locSentenceID, "AMZN", link, self.sentence)
            charu.companysentences()
        except:
            print("query error")
            db.rollback()
            # print "insert, sentence_number: ", self.number, " sentence: ", self.sentences
        db.close()

class queryID:
    def __init__(self, websiteURL):
        self.websiteURL = websiteURL;
    def conn(self):
        #db = mysql.connector.connect(host="localhost", user="root", passwd="0B001ce7bf1f", database="news")
        db = mysql.connector.connect(host="localhost"
                                     , user="root", passwd="12345678", database="oneHourChart")
        cursor = db.cursor()
        sql = "SELECT artid FROM articles " \
            "where artlink='%s'" % (self.websiteURL)
        id = 0
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for r in results:
                id = r[0]
            db.commit()
        except:
            print("query error")
            db.rollback()
        db.close()
        return id

class insertTitle:
    def __init__(self, source, url, artdate, arttime, author):
        self.source = source;
        self.url = url;
        self.artdate = artdate;
        self.arttime = arttime;
        self.author = author;
    def conn(self):
        #db = mysql.connector.connect(host="localhost", user="root", passwd="0B001ce7bf1f", database="news")
        db = mysql.connector.connect(host="localhost"
                                     , user="root", passwd="12345678", database="oneHourChart")
       #cursor = db.cursor()
        cursor_2 = db.cursor()
        #sql_1 = "SELECT arttitle FROM articles WHERE arttitle='%s'" % (self.arttime)
        sql_2 = "INSERT INTO articles (artsource,artlink,artdate,arttime,artauthor) " \
						"VALUES ('%s','%s','%s','%s','%s')" % (self.source, self.url,
                                                              self.artdate,self.arttime, self.author)
        longurl = ""
        global count
        try:
            cursor_2.execute(sql_2)
            db.commit()
            count = count +1
            cursor_2.close()
        except:
            print("insertTitle error: not support the format title ",
                  self.artdate)
            db.rollback()
        db.close
        return longurl


def sentenceTOword(local_aritcleID,article):
    for sentence in splitSentence(article):
        sentence = sentence.replace('\n', '').replace("'","")
        locSentenceID = insert(local_aritcleID, sentence).conn()
        if "AMZN" in sentence:
            word = "AMZN"
            query(word, sentence, locSentenceID, local_aritcleID).conn()



def currentTime(time):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    sql = "INSERT INTO currentTime(time) \
    VALUES('%s')" % (time)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print "error get current time"
    db.close;


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
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    sql = "SELECT difference FROM oneHourChart " \
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



def findArticle(list):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
    cursor = db.cursor()
    link = []
    first = []
    second = []
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0
    count = 0
    #all date in list
    for l in list:
        sql = "SELECT artlink,arttime FROM articles " \
            "where artdate='%s'" % (l)
        cursor.execute(sql)
        results = cursor.fetchall()
        isVisit1 = False
        isVisit2 = False
        isVisit3 = False
        isVisit4 = False
        isVisit5 = False
        isVisit6 = False
        isVisit7 = False
        isVisit8 = False
        #all article from that date
        for r in results:
            link.append(r[0])
            stringToInt = int(r[1].replace(':',''))
            #print stringToInt
            #13:30-14:30
            if stringToInt>1230 and stringToInt<1330:

                if isVisit1 == False:
                    count = count + 1
                    count1 = count
                    isVisit1 = True

                first.append(stringToInt)
                d = getDifference(l,"12:30","13:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count1,l,r[1],d,sentence)

            if stringToInt > 1330 and stringToInt < 1430:

                if isVisit2 == False:
                    count = count + 1
                    count2 = count
                    isVisit2 = True

                second.append(stringToInt)
                d = getDifference(l, "13:30", "14:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count2, l, r[1], d,sentence)

            if stringToInt > 1430 and stringToInt < 1530:

                if isVisit3 == False:
                    count = count + 1
                    count3 = count
                    isVisit3 = True
                second.append(stringToInt)
                d = getDifference(l, "14:30", "15:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count3, l, r[1], d,sentence)

            if stringToInt > 1530 and stringToInt < 1630:

                if isVisit4 == False:
                    count = count + 1
                    count4 = count
                    isVisit4 = True
                second.append(stringToInt)
                d = getDifference(l, "15:30", "16:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count4, l, r[1], d,sentence)

            if stringToInt > 1630 and stringToInt < 1730:
                if isVisit5 == False:
                    count = count + 1
                    count5 = count
                    isVisit5 = True
                second.append(stringToInt)
                d = getDifference(l, "16:30", "17:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count5, l, r[1], d,sentence)

            if stringToInt > 1730 and stringToInt < 1830:
                if isVisit6 == False:
                    count = count + 1
                    count6 = count
                    isVisit6 = True
                second.append(stringToInt)
                d = getDifference(l, "17:30", "18:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count6, l, r[1], d,sentence)

            if stringToInt > 1830 and stringToInt < 1930:
                if isVisit7 == False:
                    count = count + 1
                    count7 = count
                    isVisit7 = True
                second.append(stringToInt)
                d = getDifference(l, "18:30", "19:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count7, l, r[1], d,sentence)

            if stringToInt > 1930 and stringToInt < 2030:
                if isVisit8 == False:
                    count = count + 1
                    count8 = count
                    isVisit8 = True
                second.append(stringToInt)
                d = getDifference(l, "19:30", "20:30")
                list = findAllSentences(r[0])
                for sentence in list:
                    separateFile(r[0],count8, l, r[1], d,sentence)

    # print(link)
    # print(first)
    # print(second)

def separateFile(artlink,artFile,date,arttime,priceDifference,sentence):
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="oneHourChart")
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
        path = "/Users/yangkangou/Desktop/CSE485/JsonData/json/"
        dirs = os.listdir(path)
        list = ["1712","1801","1802","1803","1804","1805","1806","1807","1808","1809"]
        for fileName in dirs:
            if fileName in list:
                getTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(getTime)
                readAll(path+fileName)
                #print getDifference("2017.12.01","17:30","21:30")
                #print (findAllSentences("news_0000001.json"))
                currentTime(getTime)
                print "Update ", count," websites"
            findArticle(mergerNews())
            break
        break

timer(3600)