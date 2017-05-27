'''
Created on 2017-3-10

@author: Administrator
'''

from pylsy import PylsyTable

#create able
attributes=["name","age","sex","id","time"]

table=PylsyTable(attributes)


# add data

table.add_data("name",name)

table.create_table()
