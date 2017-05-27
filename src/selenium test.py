'''
Created on 2016-3-30

@author: Administrator
'''

#!/usr/bin/python
# -*- coding: gbk -*-  

from selenium import webdriver
from pip._vendor.distlib.compat import raw_input
import time,re

url1='http://bus.moretv.cn/admin/login.html'
url2="http://bus.moretv.cn/admin/logUpload/logUpload.html"
account=['jianhlijun','hello']
browser = webdriver.Chrome('c:\chromedriver.exe')
mac=''

def initWindow():
    global browser
    browser.set_window_size(0, 0)
    browser.set_page_load_timeout(5)
    #智能等待
    browser.implicitly_wait(30)

def openPage():
    global browser
    #set window size
    browser.get(url1)
    
def login():
    global browser
    username = browser.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[2]/form/ul/li[2]/input')
    username.send_keys(account[0])
    psw=browser.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[2]/form/ul/li[3]/input')
    psw.send_keys(account[1])
    browser.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[2]/form/ul/li[4]/a').click()
    print("login successfully")
    #without this sleep, acion on next page will fail (cause next action will execute on this page)

def getMacfromInput():
    title = raw_input("pls input your log title: ")
    regex=re.compile('^[a-fA-F0-9]{12}_\d{14}.txt$')
    if (None==regex.search(title)):
        print("wrong title,pls check your title")
        title=getMacfromInput()
    return title[0:12]

def gotoLogPage():
    global browser,mac
    #browser.get(url2)
    browser.find_element_by_xpath('//*[@id="nav"]/li[6]/a').click()
    print("gotoLogPage successfully")
    mac=getMacfromInput()
    #print("mac is : %s"%mac)
    
def searchMac():
    global mac
    print("mac is %s"%mac)
    browser.find_element_by_xpath('//*[@id="mac"]').send_keys(mac)
    browser.find_element_by_xpath('//*[@id="condition_sub_btn"]').click()   
    result=browser.find_element_by_xpath('//*[@id="result_content"]')
    #print(result.get_attribute('id'))
    #texts=browser.find_element_by_xpath('//*[@id="id_430238415"]/div/div[10]/div[2]').text
    #print("text is %s"%texts)
    
def closeBrowser():
    #close方法关闭当前的浏览器窗口，quit方法不仅关闭窗口，还会彻底的退出webdriver，释放与driver server之间的连接。
    browser.quit()  

initWindow()      
openPage()
login()
gotoLogPage()
searchMac()
#closeBrowser()


        
        

