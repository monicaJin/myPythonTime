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
#from openpyxl.descriptors.base import Length
#from crash_test_V4 import devicemap # if usse this, will exec crash_test_V4 first

url = "http://medusalog.tvmore.com.cn/upload/"
date_url = ""
date=""
crash_summary = open("d:/test_crash_log2.txt", "a")
exception_type = []
exception_count = []
all_crash_list = [] 
date_code = [["no date_code",0],["20160326",0],["20160411",0],["20160425",0],["20160429",0],["20140418",0]]
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

def get_dist_crash_list(maclist):
    alist = []
    for crash_mac in maclist:
        crash_mac = crash_mac[0:17]
        if crash_mac in alist:
            continue
        else:
            alist.append(crash_mac)
    return alist

def get_detail(single_data):
    #result=['date_code','product_code','android_version','APP_VERSION_NAME','MAC','CRASH_KEY']
    result=['','','','','',''] 
    content=single_data.split('&')
    for each_content in content:
        little_list=each_content.split('=')
        if little_list[0]=='DATE_CODE':
            result[0]=little_list[1]
        elif little_list[0]=='PRODUCT_CODE':
            result[1]=little_list[1]
        elif little_list[0]=='ANDROID_VERSION':
            result[2]=little_list[1]
        elif little_list[0]=='APP_VERSION_NAME':
            result[3]=little_list[1]
        elif little_list[0]=='MAC':
            little_list[1]=little_list[1].replace('%3A',':')
            result[4]=little_list[1]         
        elif little_list[0]=='CRASH_KEY':
            result[5]=little_list[1]
    if result[0]=='':
        result[0]='no date_code'
    if result[1]=='':
        result[1]='no product_code'
    if result[2]=='':
        result[2]='no android version'
    if result[3]=='':
        result[3]='no app version name'
    if result[4]=='':
        result[4]='no mac'
    if result[5]=='':
        result[5]='no crash detail'   
    result[5]=result[5].replace('\n','')
    print(result)
    print("end 1")
    return result

def get_single_data(crash):
    #if fiddler2 is launched, will cause this steps incredibly slow
    url_request = urllib.request.urlopen(date_url + "/" + crash)
    single_data=url_request.read().decode("UTF-8")
    url_request.close() #不关闭容易导致服务器关闭socket连接。使urlopen方法hang住
    single_data=single_data.replace('<br/>',' ')
    return single_data

def set_date_code_stats(result_ins):
    global date_code
    if(result_ins!='no date_code'):
        tag=True
        index3=-1
        for date_code_ins in date_code:
            if (result_ins == date_code_ins[0]): 
                tag=False
                index3=date_code.index(date_code_ins)
        if(tag):
            index3=len(date_code)-1
            date_code[index3][1]=date_code[index3][1]+1
        else:
            date_code[index3][1]=date_code[index3][1]+1
    else:
        date_code[0][1]=date_code[0][1]+1
    return result_ins

def set_exception_count_stats(result_list):
    global exception_type,exception_count,date_code
    if (result_list[5]=='no crash detail'):
        print("there are crashes without details")
        exception_detail_list=['no crash detail','no crash detail']
    else:
        if 'Exception' in result_list[5]:
            index=result_list[5].find('Exception')+9
        elif 'Error' in result_list[5]:
            index=result_list[5].find('Error')+5
        else:
            index=0
        exception_detail_list=[result_list[5][0:index],result_list[5][index+1:len(result_list[5])]]
        print(exception_detail_list)
        print('end2')
    if exception_detail_list[0] in exception_type:
        #print("old exception: "+exception)
        index = exception_type.index(exception_detail_list[0])
        for date_code_ins in date_code:
            print('result_list[0]: %s'%result_list[0])
            if date_code_ins[0]==result_list[0]:
                index_2=date_code.index(date_code_ins)
                print('index_2: %d'%index_2)
        exception_count[index][index_2] = exception_count[index][index_2] + 1    
    else:
        #print("new exception: "+exception)
        exception_type.append(exception_detail_list[0])
        exception_count.insert(len(exception_count),[])
        n=0
        for date_code_ins in date_code:
            #print("date_code_ins per crash: %s"%date_code_ins)
            if date_code_ins[0]==result_list[0]:
                exception_count[len(exception_count)-1].insert(n,1)
            else:
                exception_count[len(exception_count)-1].insert(n,0)
            n=n+1
    return exception_detail_list

def set_crash_type_stats():
    global date_code,all_crash_list,timeout_count
    socket.setdefaulttimeout(10) #in case timeout in urlopen method
    print("waiting for counting crashes...")
    count = 0
    for crash in all_crash_list:
        """pls_delete_me_count=pls_delete_me_count+1
        if(pls_delete_me_count>15):
            break"""      
        try:
            single_data=get_single_data(crash)
        except Exception:
            print("timeout~~~~")
            timeout_count=timeout_count+1
            continue
        count = count + 1
        print("call back here: %d" % count)
        #result=['date_code','product_code','android_version','APP_VERSION_NAME','MAC','CRASH_KEY']
        result_list=get_detail(single_data)
        #set date_code stats
        result_list[0] = set_date_code_stats(result_list[0])
        #set exception stats
        exception_detail_list=set_exception_count_stats(result_list)
        len1=len(all_data_list)
        #print(exception_detail_list)
        all_data_list.insert(len1,[result_list[4],result_list[1],result_list[0],1,exception_detail_list[0],1,exception_detail_list[1],1])
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

#all_data_list=[]#格式： mac,product_code,date_code,date_code_count,exception_type,1,exception_detail,1
def count_crash_per_device(device,exception,date_code):
    global all_data_list
    count=0
    for data in all_data_list :
        #print(data)
        #print("device: %s"%device+"; exception: %s"%exception+"; date_code: %s"%date_code)
        if (device==data[1])&(exception==data[4])&(date_code==data[2]):
            count=count+1
    return count

def count_device():
    global all_data_list
    devicemap=[]
    for data in all_data_list:
        print(data)
        tag=True
        for device in devicemap:
            if device[0]==data[1]:
                tag=False
                device[1]=device[1]+1
        if (tag):
            print("len: %d"%len(devicemap)+"; %s"%data[1])
            devicemap.insert(len(devicemap),[data[1],1])
    return devicemap
       
def create_data_excel(file):
    global date_code
    #print("here date_code: %s"%date_code)
    wb=xlwt.Workbook(encoding="utf-8")
    #table1=wb.add_sheet(file[18:26],cell_overwrite_ok=True)
    table1=wb.add_sheet(file[19:27],cell_overwrite_ok=True)
    table2=wb.add_sheet('stats',cell_overwrite_ok=True)
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
    table1.col(0).width=7000
    table1.col(1).width=4000
    table1.col(2).width=3000
    table1.col(3).width=7000
    table1.col(4).width=7000
    #input first row_name
    table1.write(0,0,"mac",style)
    table1.write(0,1,"product_mode",style)
    table1.write(0,2,"date_code",style)
    table1.write(0,3,"exception_type",style)
    table1.write(0,4,"exception_detail",style)
    #stats column
    table2.write(0,0,"stats",style)
    table2.write(0,1,"total",style)
    table2.write(0,2,"percentage",style)
    table2.write(0,3,"count without date_code",style)
    table2.write(0,4,"percentage",style)
    date_code_count=1
    col_2=5
    if len(date_code)>1:
        while(date_code_count<len(date_code)):
            table2.write(0,col_2,"count with date_code: %s"%date_code[date_code_count][0],style)
            #print("n+1: %d"%(nn+1)+"; len(date_code): %d"%len(date_code)+"; count: %d"%count)
            table2.write(0,col_2+1,"percentage",style)
            date_code_count=date_code_count+1
            col_2=col_2+2
    #save data in excel
    #all_data_list=[]#格式： mac,product_code,date_code,date_code_count,exception_type,1,exception_detail,1
    total_crash_count=len(all_data_list)
    index=0
    while(index<total_crash_count):
        index=index+1
        table1.write(index,0,all_data_list[index-1][0])
        table1.write(index,1,all_data_list[index-1][1])
        table1.write(index,2,all_data_list[index-1][2])
        table1.write(index,3,all_data_list[index-1][4])
        table1.write(index,4,all_data_list[index-1][6])
    #stats counted by scripts
    row=1
    table2.write(row,0,"total crash",style1)
    table2.write(row,1,total_crash_count)
    table2.write(row,2,"100%")
    # stats about date_code info
    date_code_count=0
    col_2=3
    if len(date_code)>1:
        while(date_code_count<len(date_code)):
            table2.write(row,col_2,date_code[date_code_count][1])
            table2.write(row,col_2+1,round(date_code[date_code_count][1]/total_crash_count,2))
            date_code_count=date_code_count+1
            col_2=col_2+2
    if ((len(exception_type) > 0) & (total_crash_count> 0)):
        row=row+1
        table2.write(row,0,"exception list:",style2)
        for exception in exception_type:
            row=row+1
            if (not exception == ""):
                table2.write(row,0,exception,style1)
            else:
                table2.write(row,0,"crash with blank exception_type",style1)
            index = exception_type.index(exception)
            n=0
            single_count=0
            while(n<len(exception_count[index])):
                single_count = single_count+exception_count[index][n]
                n=n+1
            table2.write(row,1,single_count)
            table2.write(row,2,round(single_count/total_crash_count,2))
            n=0
            col=3
            #print(exception_type)
            #print(exception_count)
            while(n<len(date_code)):
                #print("exception_count[index][n]: %d"%exception_count[index][n])
                table2.write(row,col,exception_count[index][n])
                if(date_code[n][1]!=0):
                    table2.write(row,col+1,round(exception_count[index][n]/date_code[n][1],2))
                else: 
                    table2.write(row,col+1,0)
                n=n+1
                col=col+2
    elif ((total_crash_count > 0) & (len(exception_type) == 0)):
        table2.write(row,0,"no details in the all crash files~~~")
        row=row+1
    else:
        table2.write(row,4,"something wrong,pls recheck")
        print("wrong!wrong!wrong!")
        return
    #stats counted by excel formular
    row=row+1
    table2.write(row,0,"devce list: ",style2)
    devicemap=count_device()
    for device in devicemap:
        row=row+1
        table2.write(row,0,device[0],style1)
        total_count_by_device=count_crash_by_device(device[0],"total")
        #print("total_count_by_device: %d"%total_count_by_device+"; count_with_date_code: %d"%count_with_date_code)
        table2.write(row,1,total_count_by_device)
        table2.write(row,2,Formula("round(F%d/F2,2)"%(row+1)))
        col=3
        for date_code_ins in date_code:
            total_count_by_date_code=count_crash_by_device(device[0],date_code_ins[0])
            table2.write(row,col,total_count_by_date_code)
            if(date_code_ins[1]!=0):
                table2.write(row,col+1,round(total_count_by_date_code/date_code_ins[1],2))
            else:
                table2.write(row,col+1,"no crash here")
            col=col+2
    #exception per device
    row=row+1
    for date_code_ins in date_code:
        table2.write(row,0,"matrix: %s"%date_code_ins[0],style2)
        col=1
        for exception in exception_type:
            table2.write(row,col,exception,style1)
            col=col+1
        col=1
        for device in devicemap:
            row=row+1
            col=1
            table2.write(row,0,device[0],style1)
            for exception in exception_type:
                count=count_crash_per_device(device[0],exception,date_code_ins[0])
                table2.write(row,col,count)
                col=col+1
        row=row+1  
    #print("file here: %s"%file)
    wb.save(file)
    
def write_into_excel():
    global date,file
    file="d:\\crash_log\\data2\\"
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
    #crash_summary.write("------------------" + date_url + "----------------\n")
    # crash_list=get_dist_crash_list()
    # print("waiting for counting crashes...",end="") this steps sometimes will be blocked somehow, i don't know why
    set_crash_type_stats()
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

def init2():
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
print('this is v5 crash report')
init2()
print("crash report on date:%s" % date)
get_crash_stats()

