'''
Created on 2016-3-29

@author: Administrator
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-  

import re
import urllib.request
import datetime
from pip._vendor.distlib.compat import raw_input
#import time
import xlwt
import os
from xlwt.ExcelFormula import Formula
import socket

url = "http://medusalog.tvmore.com.cn/upload/"
date_url = ""
date=""
crash_summary = open("d:/test_crash_log2.txt", "a")
exception_type = []
exception_count = []
devicemap = [["泰捷20s", "00:04:a3"], ["华为荣耀M321", "1c:8e:5c", "bc:25:e0", "24:7f:3c"], ["天猫魔盒M13", "20:8B:37", "38:fa:ca"], ["乐视NewC1S", "c8:0e:77"], ["小米盒子3"], ["others"]]
all_crash_list = [] 
date_code = [["",0],["20160326",0],["20160411",0],["20160425",0],["20160429",0],["20160518",0]]
all_data_list=[]#格式： mac,device_name,date_code,exception,1
file=""
timeout_count=0
#class FoundException(Exception): pass

# select a date
def get_dateurl():
    global date_url
    date_url = url + date + "/"

# current date
def current_date():
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    # date_url=url+date+"/"
    return date

def get_device_name(mac):
    #print("get_device_name: %s"%mac)
    p1=re.compile("^(\w{2}[ ,:]?){5}\w{2}$")
    if(" " in mac):
        mac=mac.replace(" ",":")
    elif("%3A" in mac):
        mac=mac.replace("%3A",":")
    if(None==p1.search(mac)):
        return [mac,"others"]
    for device in devicemap:
        for detail in device:
            if (mac[0:8]== detail):
                return [mac,device[0]]
    len1=len(devicemap)-1
    len2=len(devicemap[len1])
    devicemap[len1].insert(len2,mac[0:8])
    return [mac,devicemap[len1][0]]

def get_dist_crash_list(maclist):
    alist = []
    for crash_mac in maclist:
        crash_mac = crash_mac[0:17]
        if crash_mac in alist:
            continue
        else:
            alist.append(crash_mac)
    return alist

def get_crash_type_stats():
    global date_code,all_crash_list,timeout_count
    print("waiting for counting crashes...")
    count = 0
    socket.setdefaulttimeout(10) #in case timeout in urlopen method
    #pls_delete_me_count=0
    for crash in all_crash_list:
        """pls_delete_me_count=pls_delete_me_count+1
        if(pls_delete_me_count>15):
            break"""
        # print("new crash: "+ crash)
        # print(date_url+"/"+crash)        
        #判断exception
        try:
            #if fiddler2 is launched, will cause this steps incredibly slow
            url_request = urllib.request.urlopen(date_url + "/" + crash)
            single_data=url_request.read().decode("UTF-8")
            #time.sleep(5)
            #print("here")
            url_request.close() #不关闭容易导致服务器关闭socket连接。使urlopen方法hang住
            #print("get new data done")
        except Exception:
            print("timeout~~~~")
            timeout_count=timeout_count+1
            continue
        count = count + 1       
        print("call back here: %d" % count)
        index1 = single_data.find("STACK_TRACE=") + 12
        index2 = single_data.find("Exception")
        boo = "DATE_CODE" in single_data
        if(boo):
            i1 = single_data.find("DATE_CODE=") + 10
            date_code2 = single_data[i1:(i1 + 8)]
            tag=True
            index3=-1
            for date_code_ins in date_code:
                if (date_code2 == date_code_ins[0]): 
                    tag=False
                    index3=date_code.index(date_code_ins)
            if(tag):
                index3=len(date_code)-1
                date_code[index3][1]=date_code[index3][1]+1
                date_code2="others"
            else:
                date_code[index3][1]=date_code[index3][1]+1
            #print("date_code: %s"%date_code+"; date_code2: %s"%date_code2)
        else:
            date_code2=""
            date_code[0][1]=date_code[0][1]+1
        if (index2 > 0):
            index2 = index2 + 9
        elif(single_data.find("Error") > 0):
            index2 = single_data.find("Error") + 5
        else:
            print("something wrong~~~" + crash)
            exception = ""
        if(index1 <= index2):
            exception = single_data[index1:index2]
        else:
            print("there are crashes with no details")
        #print("exception_type length: %d"%len(exception_type))
        if exception in exception_type:
            #print("old exception: "+exception)
            index = exception_type.index(exception)
            for date_code_ins in date_code:
                if date_code_ins[0]==date_code2:
                    index_2=date_code.index(date_code_ins)
            exception_count[index][index_2] = exception_count[index][index_2] + 1    
        else:
            #print("new exception: "+exception)
            exception_type.append(exception)
            exception_count.insert(len(exception_count),[])
            n=0
            for date_code_ins in date_code:
                #print("date_code_ins per crash: %s"%date_code_ins)
                if date_code_ins[0]==date_code2:
                    exception_count[len(exception_count)-1].insert(n,1)
                else:
                    exception_count[len(exception_count)-1].insert(n,0)
                n=n+1
        [mac,device_name]=get_device_name(crash[0:27].replace("%3A", ":"))
        len1=len(all_data_list)
        all_data_list.insert(len1,[mac,device_name,date_code2,1,exception,1])
        #print("done saving data %s"%crash)
        
def count_crash_by_device(device,tag):
    global date_code
    total_count=0
    #print("device: %s"%device)
    if(tag=="total"):
        for data in all_data_list:
            # print (data)
            if device in data:
                # print("total_count_by_device: %d"%total_count+"; count_with_date_code: %d"%count_with_date_code)
                total_count = total_count + 1
    else:
        for data in all_data_list:
            if (device in data)&(tag in data):
                total_count = total_count + 1
        
    return total_count

#all_data_list=[]#格式： mac,device_name,date_code,date_code_count,exception,1
def count_crash_per_device(device,exception,date_code):
    global all_data_list
    count=0
    for data in all_data_list :
        #print(data)
        #print("device: %s"%device+"; exception: %s"%exception+"; date_code: %s"%date_code)
        if (device==data[1])&(exception==data[4])&(date_code==data[2]):
            count=count+1
    return count
       
def create_data_excel(file):
    global date_code
    #print("here date_code: %s"%date_code)
    wb=xlwt.Workbook(encoding="utf-8")
    table=wb.add_sheet(file[18:26],cell_overwrite_ok=True)
    #set excel pattern
    style=xlwt.XFStyle() #create pattern
    pattern=xlwt.Pattern()
    pattern.pattern=xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour=20
    style.pattern=pattern #add pattern to style
    font1=xlwt.Font()
    font1.bold=True
    style.font=font1
    #another style
    style1=xlwt.XFStyle()
    style1.font=font1
    #another style
    style2=xlwt.XFStyle()
    style2.font=font1
    pattern.pattern=xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour=19
    style2.pattern=pattern #add pattern to style
    #set width
    table.col(0).width=7000
    table.col(1).width=4000
    table.col(2).width=3000
    table.col(3).width=7000
    table.col(4).width=4000
    #input first row_name      
    table.write(0,0,"mac",style)
    table.write(0,1,"device_name",style)
    table.write(0,2,"date_code",style)
    table.write(0,3,"exception_type",style)
    #stats column
    table.write(0,4,"stats",style)
    table.write(0,5,"total",style)
    table.write(0,6,"percentage",style)
    table.write(0,7,"count without date_code",style)
    table.write(0,8,"percentage",style)
    date_code_count=1
    col_2=9
    if len(date_code)>1:
        while(date_code_count<len(date_code)):
            table.write(0,col_2,"count with date_code: %s"%date_code[date_code_count][0],style)
            #print("n+1: %d"%(nn+1)+"; len(date_code): %d"%len(date_code)+"; count: %d"%count)
            table.write(0,col_2+1,"percentage",style)
            date_code_count=date_code_count+1
            col_2=col_2+2
    #save data in excel
    total_crash_count=len(all_data_list)
    index=0
    while(index<total_crash_count):
        index=index+1
        table.write(index,0,all_data_list[index-1][0])
        table.write(index,1,all_data_list[index-1][1])
        table.write(index,2,all_data_list[index-1][2])
        table.write(index,3,all_data_list[index-1][4])
    #stats counted by scripts
    row=1
    table.write(row,4,"total crash",style1)
    table.write(row,5,total_crash_count)
    table.write(row,6,"100%")
    # stats about date_code info
    date_code_count=0
    col_2=7
    if len(date_code)>1:
        while(date_code_count<len(date_code)):
            table.write(row,col_2,date_code[date_code_count][1])
            table.write(row,col_2+1,round(date_code[date_code_count][1]/total_crash_count,2))
            date_code_count=date_code_count+1
            col_2=col_2+2
    if ((len(exception_type) > 0) & (total_crash_count> 0)):
        row=row+1
        table.write(row,4,"exception list:",style2)
        for exception in exception_type:
            row=row+1
            if (not exception == ""):
                table.write(row,4,exception,style1)
            else:
                table.write(row,4,"crash with blank exception_type",style1)
            index = exception_type.index(exception)
            n=0
            single_count=0
            while(n<len(exception_count[index])):
                single_count = single_count+exception_count[index][n]
                n=n+1
            table.write(row,5,single_count)
            table.write(row,6,round(single_count/total_crash_count,2))
            n=0
            col=7
            #print(exception_type)
            #print(exception_count)
            while(n<len(date_code)):
                #print("exception_count[index][n]: %d"%exception_count[index][n])
                table.write(row,col,exception_count[index][n])
                if(date_code[n][1]!=0):
                    table.write(row,col+1,round(exception_count[index][n]/date_code[n][1],2))
                else: 
                    table.write(row,col+1,0)
                n=n+1
                col=col+2
    elif ((total_crash_count > 0) & (len(exception_type) == 0)):
        table.write(row,4,"no details in the all crash files~~~")
        row=row+1
    else:
        table.write(row,4,"something wrong,pls recheck")
        print("wrong!wrong!wrong!")
        return
    #stats counted by excel formular
    row=row+1
    table.write(row,4,"devce list: ",style2)
    for device in devicemap:
        row=row+1
        table.write(row,4,device[0],style1)
        total_count_by_device=count_crash_by_device(device[0],"total")
        #print("total_count_by_device: %d"%total_count_by_device+"; count_with_date_code: %d"%count_with_date_code)
        table.write(row,5,total_count_by_device)
        table.write(row,6,Formula("round(F%d/F2,2)"%(row+1)))
        col=7
        for date_code_ins in date_code:
            total_count_by_date_code=count_crash_by_device(device[0],date_code_ins[0])
            table.write(row,col,total_count_by_date_code)
            if(date_code_ins[1]!=0):
                table.write(row,col+1,round(total_count_by_date_code/date_code_ins[1],2))
            else:
                table.write(row,col+1,"no crash here")
            col=col+2
    #exception per device
    row=row+1
    for date_code_ins in date_code:
        table.write(row,4,"matrix: %s"%date_code_ins[0],style2)
        col=5
        for exception in exception_type:
            table.write(row,col,exception,style1)
            col=col+1
        col=5
        for device in devicemap:
            row=row+1
            col=5
            table.write(row,4,device[0],style1)
            for exception in exception_type:
                count=count_crash_per_device(device[0],exception,date_code_ins[0])
                table.write(row,col,count)
                col=col+1
        row=row+1  
    #print("file here: %s"%file)
    wb.save(file)
    
def write_into_excel():
    global date,file
    file="d:\\crash_log\\data\\"
    if(not os.path.exists(file)):
        os.makedirs(file)
    file=file+date+".xls"
    if(os.path.exists(file)):
        print("data with this date already exists,will overwrite with new data")
    #will overwrite old file
    print("file is %s"%file)
    create_data_excel(file)
    print("excel report on %s"%date+" is done")

def get_crash_stats():   
    crash_summary.write("------------------" + date_url + "----------------\n")
    # crash_list=get_dist_crash_list()
    # print("waiting for counting crashes...",end="") this steps sometimes will be blocked somehow, i don't know why
    get_crash_type_stats()
    #print(all_data_list)
    # output exception info to file   
    #write_into_file()
    print("date_code length: %d"%len(date_code))
    print(date_code)
    write_into_excel()
    print("timeout_count: %d"%timeout_count)
    # print("exception_type length: %d"%len(exception_type))
    # print("crash list length: %d"%len(all_crash_list))

def get_filelist(url_temp):
    print("getting file list, waiting...")
    total_data = urllib.request.urlopen(url_temp).read().decode("utf-8")
    alist = re.findall(r'href="(.+?)"', total_data) 
    alist = alist[1:len(alist)]
    return alist

def get_date_list():
    global url
    print("url: %s"%url)
    date_list = get_filelist(url)
    return date_list

#interation
def iteration_get_input(length):
    option = raw_input("pls select a date from above (input numbers only):")
    regex=re.compile("^\d+$")
    if (None==regex.search(option)):
        print("wrong date,numbers only")
        option=iteration_get_input(length)
    elif((int(option) >= length) | (int(option) < 0)):
        print("no such date in above list! pls try again")
        option=iteration_get_input(length)
    return option

def input_from_user():
    date_list = get_date_list()
    count = 0
    print("date list:")
    for date in date_list:
        print("%d" % count + ": %s" % date)
        count = count + 1
    print(len(date_list))
    option=iteration_get_input(len(date_list))
    return date_list[int(option)]

def init():
    global all_crash_list,date
    # init date
    date = input_from_user()
    date=date.replace("/", "")
    # init date_url
    get_dateurl()
    # init get all crash files
    all_crash_list = get_filelist(date_url)
    # crash total
    print("total crashes: %d" % len(all_crash_list))
 
# execution part 
print('this is v4 crash report')  
init()
print("crash report on date:%s" % date)
get_crash_stats()

