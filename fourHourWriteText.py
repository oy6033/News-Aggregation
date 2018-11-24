# coding:utf-8
#!/usr/bin/python
import mysql.connector
import os



def file_write(file_name,text,path):
    if os.path.exists(path + file_name)==False:
        f = open(path+file_name, 'w+')
        f.write(text+"\n")
        f.close()
    else:
        f = open(path+file_name, 'a+')
        f.write(text+"\n")
        f.close()

#four hour chart
def getFileID():
    db = mysql.connector.connect(host="localhost"
                                 , user="root", passwd="12345678", database="fourHourChart")
    cursor = db.cursor()
    sql = "SELECT artFile,sentence,priceDifference FROM separateFile"
    path = '/Users/yangkangou/Desktop/CSE485/JsonData/json/TrainingData_FourHour/'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            if(r[2]!="" and float(r[2])>0):
                file_write(str(r[0])+".txt",(r[1].lower().replace("down","")).encode('utf-8'),path+'up/')
            if(r[2]!="" and float(r[2])<0):
                file_write(str(r[0])+".txt",(r[1].lower().replace("up","")).encode('utf-8'),path+'down/')
            # if(r[2]=="" or float(r[2])==0):
            #     file_write(str(r[0])+".txt",(r[1]+"same").encode('utf-8'),path+'same/')
        db.commit()
    except:
        print "error get Link"
        db.rollback()
    db.close;

getFileID()
