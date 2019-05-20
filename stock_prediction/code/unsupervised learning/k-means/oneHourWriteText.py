# coding:utf-8
#!/usr/bin/python
import mysql.connector
import os
from nltk.tokenize import word_tokenize
import nltk

def file_write(file_name,text,path):
    if os.path.exists(path + file_name)==False:
        f = open(path+file_name, 'w+')
        f.write(text+"\n")
        f.close()
    else:
        f = open(path+file_name, 'a+')
        f.write(text+"\n")
        f.close()

#one hour chart
def getFileID():
    db = mysql.connector.connect(host="127.0.0.1"
                                 , user="root", passwd="12345678", database="fourHourChart")
    cursor = db.cursor()
    sql = "SELECT artFile,sentence,priceDifference FROM separateFile"
    path = 'C:/Users/Michael/PycharmProjects/CSE573/'
    count = 0
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            print r
            if (r[2] != ""):
                tokens = word_tokenize(r[1])
                words = [word.lower() for word in tokens if word.isalpha()]
                # print ' '.join(words)
                tags_needed = ['VB','VBD','VBG','VBZ','RP','RB','IN']
                pos_tags = nltk.pos_tag(words)
                print pos_tags
                ret = []
                for word, pos in pos_tags:
                    if (pos in tags_needed):
                        ret.append(word)
                sentence = ' '.join(ret)
                if count % 2 == 1:
                    sentence = sentence + " up up up up up"
                else:
                    sentence = sentence + " down down down down"
                print sentence
                if(r[2]!="" and float(r[2])>0):
                    file_write(str(int(r[0]))+".txt",(sentence).encode('utf-8'),path+'AMZN/total/')
                if(r[2]!="" and float(r[2])<0):
                    file_write(str(int(r[0]))+".txt",(sentence).encode('utf-8'),path+'AMZN/total/')
            count += 1
        db.commit()
    except:
        print "error get Link"
        db.rollback()
    db.close

getFileID()
