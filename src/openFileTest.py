'''
Created on 2016-8-26

@author: Administrator
'''

import re

myfile=open('d:/2.yml','r')
try:
    text=myfile.read()
finally:
    myfile.close()

print(text)
regex=re.compile(r'versionName:(.+?)')
match=regex.search(text)
print(match)
if match:
    code=match.group(1)
    print(code)