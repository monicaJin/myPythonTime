'''
Created on 2016-3-30

@author: Administrator
'''

#!/usr/bin/python
# -*- coding: gbk -*-  

#from selenium import webdriver
import uuid
import urllib.request,json,time

count=10
datalist=[]
jKeys=[]
jValues=[]


def init_userid():
    userid=str(uuid.uuid1())
    return userid
    
def init_data():
    global datalist
    i=1
    while i <= count:
        userid=init_userid()
        userid=userid.replace('-','')
        print("userid: %s"%userid)
        #requesturl="http://rec.aiseewhaley.aisee.tv/config/abControl?userId="+str(userid)+"&version="+random.choice(version)
        requesturl="http://rec.aiseewhaley.aisee.tv/config/abControl?userId="+userid+"&version=3.1.4"
        data=getRequestDATA(requesturl)
        time.sleep(1)
        datalist.append([str(userid),data])
        i=i+1

def getRequestDATA(url):
    try:
        #if fiddler2 is launched, will cause this steps incredibly slow
        url_request = urllib.request.urlopen(url)
        data=url_request.read().decode("UTF-8")
        url_request.close() #不关闭容易导致服务器关闭socket连接。使urlopen方法hang住
    except Exception:
        print("timeout")
        #exit()
        data="timeout"
    return data

def checkDup(key,_array):
    if key in _array:
        return False
    else:
        return True
    
def parserJsonFile(jsonData):  
    global jValues,jKeys
    value = json.loads(jsonData)
    exist_flag=False
    data=value["abGroup"]
    for rootkey in data:
        exist_flag=False
        if checkDup(rootkey,jKeys):
            jValues.append([[data[rootkey],1]])
            jKeys.append(rootkey)
        else:
            index=jKeys.index(rootkey)
            value=data[rootkey]
            for element in jValues[index]:
                if value == element[0]:
                    element[1]=element[1]+1
                    exist_flag=True                    
                    break;
            if exist_flag==False:
                jValues[index].append([value,1])           
    
def calculate_func():
    global datalist,count
    timeout_count=0
    for data in datalist:
        if (data[1]!="timeout"):
            parserJsonFile(data[1])
        else: 
            timeout_count=timeout_count+1
    print("--------   样本数: %d （timeout: %d）  -----------"%(count,timeout_count))     
    for (element1,element2) in zip(jKeys,jValues):
        print("#############   %s  #############"%element1)
        for element in element2:
            print("[%s] : %.2f%%"%(element[0],element[1]/(count-timeout_count)*100)) 
    
init_data()
calculate_func()

        
        

