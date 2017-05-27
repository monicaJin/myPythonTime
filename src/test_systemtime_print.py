#!/usr/bin/python
#-*- coding:GBK -*-

import sys
import os
import shutil
import io
import re
import time
import subprocess
import os.path


#input your ip adress
localip = '192.168.1.104'

#defination part  
#adb连接
def adbconnect():
    cmdconnect = 'adb connect %s'%(localip)
    device_status = subprocess.getstatusoutput(cmdconnect)
    #time.sleep(5)
    if "unable" in device_status[1]:
        print ("unable to connect to device. pls retry")
        exit()
    else:
        print ("---------  connected -----------")

def my_loop():
    cmd_date = 'date'
    cmd_time = 'time'
    while (True):
        date = os.popen(cmd_date).read()
        newdate=date[5:17]
        todaytime=os.popen(cmd_time).read()
        newtime=todaytime[5:17]
        systemtime=newdate+newtime+"\n"
        print(systemtime)
        myFile=open('d:/test_python2.txt','a')
        myFile.write(systemtime)
        myFile.close()
        time.sleep(1)

#execution part
my_loop()