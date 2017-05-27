import urllib,urllib3
#import requests
import json

def little_GET_test():
    http=urllib3.PoolManager()
    r=http.request('GET','http://httpbin.org/robots.txt')
    print(r.status)
    print(r.data)

def little_POST_test():
    http=urllib3.PoolManager()
    r=http.request(
                   'POST',
                   'http://httpbin.org/post',
                   fields={'hello': 'world'})
    print(r.status)
    print(r.data)
    data=json.loads(r.data.decode('utf-8'))
    print(data)
    
def little_jsonResponse_test():
    http=urllib3.PoolManager()
    r=http.request('GET','http://httpbin.org/ip')
    print(r.data)
    data=json.loads(r.data.decode('utf-8'))
    print(data)
    
def little_binaryResponse_test():
    http=urllib3.PoolManager()
    r=http.request('GET',"http://httpbin.org/bytes/8")
    print(r.data)
       
#little_GET_test()
#little_POST_test()
#little_jsonResponse_test()
little_binaryResponse_test()



